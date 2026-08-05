"""Provider-agnostic chat: lmstudio | openai | anthropic | azure.

One interface, four backends — switching is two lines in .env. The returned
ChatResult always carries the token usage when the provider reports it.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from functools import lru_cache

from . import input_gr, model_gr, output_gr
from .config import settings


@dataclass
class ChatResult:
    text: str
    provider: str
    model: str
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    # Non-fatal output-guardrail findings (citation mismatches, possible
    # self-contradiction, ...). Empty unless check_output() flagged something.
    warnings: list[str] = field(default_factory=list)


class LLM:
    def __init__(self, provider: str, model: str, client) -> None:
        self.provider = provider
        self.model = model
        self._client = client

    def chat(self, system: str, user: str, temperature: float, max_tokens: int,
             extras: dict | None = None, history: list[dict] | None = None,
             num_sources: int = 0) -> ChatResult:
        """Provider-agnostic chat, wrapped by three guardrails:

          1. model_gr  — the provider/model pair must be on the approved list,
                          checked once up front so an unapproved model never
                          gets a chance to run.
          2. input_gr  — the user turn is screened for sensitive topics before
                          it is sent anywhere; a hit short-circuits the call
                          entirely (no tokens spent) and returns a friendly
                          refusal in place of a real response.
          3. output_gr — the model's own reply is checked before it's handed
                          back to the caller: toxicity hard-blocks and swaps
                          in a friendly message, citation/consistency issues
                          are attached as `ChatResult.warnings` instead of
                          blocking (a false positive there would eat a
                          correct answer).

        `num_sources` is how many retrieved chunks were available — pass it
        through from a RAG caller (e.g. len(chunks) in local_agent.run) so the
        output guardrail's citation check has something to validate against.
        """
        model_gr.ensure_approved(self.provider, self.model)

        input_check = input_gr.check_input(user)
        if input_check.blocked:
            return ChatResult(text=input_check.message, provider=self.provider, model=self.model)

        result = self._dispatch(system, user, temperature, max_tokens, extras, history)

        output_check = output_gr.check_output(result.text, num_sources=num_sources)
        if not output_check.allowed:
            result.text = output_check.message
        else:
            result.warnings = output_check.warnings
        return result

    def _dispatch(self, system: str, user: str, temperature: float, max_tokens: int,
                  extras: dict | None, history: list[dict] | None) -> ChatResult:
        # Prior turns go in as their own real messages, each with its own role — never
        # flattened into "User: ...\nAssistant: ..." text. That shape mimics impersonated
        # conversation turns, which Azure's jailbreak filter treats as a prompt-injection
        # signature and rejects outright.
        extras = extras or {}
        history = history or []
        if self.provider in ("lmstudio", "openai"):
            kwargs: dict = {
                "model": self.model,
                "temperature": temperature,
                "messages": [
                    {"role": "system", "content": system},
                    *history,
                    {"role": "user", "content": user},
                ],
            }
            # OpenAI's gpt-5.x family renamed the cap; LM Studio still speaks the classic name
            if self.provider == "openai":
                kwargs["max_completion_tokens"] = max_tokens
            else:
                kwargs["max_tokens"] = max_tokens
            kwargs.update(extras)
            r = self._client.chat.completions.create(**kwargs)
            u = getattr(r, "usage", None)
            return ChatResult(
                text=r.choices[0].message.content or "",
                provider=self.provider,
                model=self.model,
                prompt_tokens=getattr(u, "prompt_tokens", None),
                completion_tokens=getattr(u, "completion_tokens", None),
            )

        if self.provider == "anthropic":
            r = self._client.messages.create(
                model=self.model,
                system=system,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[*history, {"role": "user", "content": user}],
            )
            return ChatResult(
                text="".join(block.text for block in r.content if block.type == "text"),
                provider=self.provider,
                model=self.model,
                prompt_tokens=r.usage.input_tokens,
                completion_tokens=r.usage.output_tokens,
            )

        # azure — azure-ai-inference ChatCompletionsClient
        messages = [
            {"role": "system", "content": system},
            *history,
            {"role": "user", "content": user},
        ]
        try:
            r = self._client.complete(
                model=self.model, temperature=temperature,
                max_tokens=max_tokens, messages=messages,
                **({"model_extras": extras} if extras else {}),
            )
        except Exception as e:
            # The gpt-5 family renamed the output cap. Retry with the new name
            # rather than making every caller know which generation they are on.
            if "max_completion_tokens" not in str(e):
                raise
            r = self._client.complete(
                model=self.model, messages=messages,
                model_extras={"max_completion_tokens": max_tokens, **extras},
            )
        u = getattr(r, "usage", None)
        return ChatResult(
            text=r.choices[0].message.content or "",
            provider=self.provider,
            model=self.model,
            prompt_tokens=getattr(u, "prompt_tokens", None),
            completion_tokens=getattr(u, "completion_tokens", None),
        )

    def describe(self) -> dict:
        return {"provider": self.provider, "model": self.model}


@lru_cache(maxsize=1)
def get_llm() -> LLM:
    provider = settings.llm_provider.lower()

    if provider == "lmstudio":
        from openai import OpenAI

        return LLM(provider, settings.lmstudio_model,
                   OpenAI(base_url=settings.lmstudio_base_url, api_key="lm-studio"))

    if provider == "openai":
        from openai import OpenAI

        return LLM(provider, settings.openai_model, OpenAI(api_key=settings.openai_api_key))

    if provider == "anthropic":
        from anthropic import Anthropic

        return LLM(provider, settings.anthropic_model,
                   Anthropic(api_key=settings.anthropic_api_key))

    if provider == "azure":
        if not settings.azure_ai_endpoint:
            raise ValueError(
                "AZURE_AI_ENDPOINT is not set — put your Foundry endpoint in .env "
                "(README § Credentials · Azure Foundry)"
            )
        from azure.ai.inference import ChatCompletionsClient

        client = ChatCompletionsClient(
            endpoint=settings.azure_ai_endpoint,
            credential=_azure_credential(),
            credential_scopes=["https://cognitiveservices.azure.com/.default"],
        )
        return LLM(provider, settings.azure_ai_chat_deployment, client)

    raise ValueError(
        f"LLM_PROVIDER='{provider}' is not supported — use lmstudio, openai, anthropic or azure"
    )


def _azure_credential():
    if settings.azure_ai_auth.lower() == "key":
        from azure.core.credentials import AzureKeyCredential

        return AzureKeyCredential(settings.azure_ai_api_key)
    from azure.identity import DefaultAzureCredential

    return DefaultAzureCredential()
