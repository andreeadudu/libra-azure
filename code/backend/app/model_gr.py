"""Model guardrail — restricts LLM calls to an explicit allowlist of approved models.

Purpose: stop the app from silently talking to a model nobody signed off on —
whether from a typo'd .env value, a provider default drifting under you, or
someone swapping ANTHROPIC_MODEL to something untested. This module owns the
allowlist and the check only; it knows nothing about HTTP, chunks, or prompts.

Matching is by regex against the model id, grouped per provider (the same
model family can mean a different string per provider — e.g. Azure deployment
*names* are arbitrary and don't have to start with "gpt-").
"""
from __future__ import annotations

import re

# Provider -> list of regex patterns (case-insensitive) matched against the
# model id. Extend this as new approved model families are rolled out.
APPROVED_MODELS: dict[str, list[str]] = {
    "openai": [
        r"^gpt-4(\.\d+)?(-.*)?$",     # ChatGPT 4.x family (gpt-4, gpt-4.1, gpt-4o, gpt-4-turbo, ...)
        r"^gpt-5(\.\d+)?(-.*)?$",     # ChatGPT 5.x family (gpt-5, gpt-5.1, gpt-5.4-nano, ...)
    ],
    "azure": [
        # Azure deployment *names* are chosen by whoever deployed them and don't
        # have to match the underlying model — adjust these patterns (or the
        # deployment naming convention) if that's the case in your resource.
        r"^gpt-4(\.\d+)?(-.*)?$",
        r"^gpt-5(\.\d+)?(-.*)?$",
    ],
    "anthropic": [
        r"^claude-opus(-.*)?$",       # Claude Opus family
        r"^claude-fable(-.*)?$",      # Claude Fable family
        # NOTE: Claude Sonnet/Haiku are intentionally NOT approved. The repo's
        # default ANTHROPIC_MODEL (claude-sonnet-5) will fail this guardrail
        # until it's changed to an approved model or this list is extended.
    ],
    # NOTE: "lmstudio" has no entry, so every local/dev model is rejected by
    # design (no cost/compliance guarantees on arbitrary local weights). For
    # local dev, either flip ENFORCE to False below, or add an explicit entry:
    #   APPROVED_MODELS["lmstudio"] = [r".*"]
}

# Master switch — flip to False to log-and-allow instead of hard-blocking
# (useful while iterating locally without touching the allowlist above).
ENFORCE = True


class ModelNotApproved(ValueError):
    """Raised when the configured provider/model pair isn't on the allowlist."""


def is_approved(provider: str, model: str) -> bool:
    patterns = APPROVED_MODELS.get(provider.lower(), [])
    return any(re.match(p, model, re.IGNORECASE) for p in patterns)


def ensure_approved(provider: str, model: str) -> None:
    """Call this before dispatching a chat request to a provider.

    Raises ModelNotApproved (a ValueError) naming the offending pair and the
    full allowlist, so a misconfigured provider/model fails loud instead of
    quietly calling out to something unapproved. No-op when ENFORCE is False.
    """
    if not ENFORCE or is_approved(provider, model):
        return
    allowed = ", ".join(
        f"{prov}:{pattern}" for prov, patterns in APPROVED_MODELS.items() for pattern in patterns
    )
    raise ModelNotApproved(
        f"Model '{model}' (provider={provider}) is not on the approved list. "
        f"Approved provider:pattern pairs — {allowed}"
    )
