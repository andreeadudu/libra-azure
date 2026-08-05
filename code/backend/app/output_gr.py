"""Output guardrail — checks a generated answer before it reaches the user.

Three checks, each best-effort and dependency-free:
  1. Citations    — every [n] marker in the answer must point at a source that
                     was actually retrieved (no citing a source that doesn't exist).
  2. Consistency   — the answer shouldn't flatly assert and deny the same claim
                     in the same breath (a cheap self-contradiction smell test).
  3. Toxicity      — reuses the same sensitive-topic screen as the input
                     guardrail, applied to model output instead of user input,
                     since a jailbroken prompt can still produce disallowed
                     content on the way out.

Citations and consistency are surfaced as *warnings*, not hard blocks — a
false positive there (e.g. a legitimately numbered list, or "yes... but no
extra fee") would silently eat a correct answer, which is worse than showing
a slightly-suspect one with a flag attached. Only toxicity hard-blocks.

Factuality is intentionally left as an optional hook (`judge_fn`) rather than
implemented here: a real factuality check needs an LLM-as-judge call, and
this module cannot import llm.py to make one without creating an import cycle
(llm.py -> output_gr.py -> llm.py). Callers that want it pass a callable.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from .input_gr import SENSITIVE_TOPICS

FRIENDLY_MESSAGE = (
    "I generated a response but it didn't pass an internal safety check "
    "({reason}), so I'm not showing it. Please rephrase your question and "
    "I'll try again."
)

_CITATION_RE = re.compile(r"\[(\d+)\]")

# Pairs of (assertion pattern, negation pattern) that shouldn't both appear
# about the same claim in one answer. Intentionally small and specific to
# keep the false-positive rate low.
_CONTRADICTION_PAIRS = [
    (r"\bis true\b", r"\bis false\b"),
    (r"\bis possible\b", r"\bis not possible\b"),
    (r"\bis allowed\b", r"\bis not allowed\b"),
    (r"\bis free\b", r"\bis not free\b"),
]


@dataclass
class OutputCheckResult:
    allowed: bool
    reason: str | None = None
    message: str | None = None
    warnings: list[str] = field(default_factory=list)


def _check_citations(text: str, num_sources: int) -> str | None:
    cited = {int(n) for n in _CITATION_RE.findall(text)}
    if not cited:
        return None
    out_of_range = sorted(n for n in cited if n < 1 or n > num_sources)
    if out_of_range:
        return (f"citation(s) {out_of_range} don't match any of the "
                f"{num_sources} retrieved source(s)")
    return None


def _check_consistency(text: str) -> str | None:
    lowered = text.lower()
    for asserts, negates in _CONTRADICTION_PAIRS:
        if re.search(asserts, lowered) and re.search(negates, lowered):
            return f"answer appears to both assert and deny the same claim ({asserts!r} / {negates!r})"
    return None


def _check_toxicity(text: str) -> str | None:
    lowered = text.lower()
    for category, patterns in SENSITIVE_TOPICS.items():
        for pattern in patterns:
            if re.search(pattern, lowered):
                return f"output touches a blocked topic ({category.replace('_', ' ')})"
    return None


def check_output(text: str, num_sources: int = 0, judge_fn=None) -> OutputCheckResult:
    """Run all output checks on a generated answer.

    `num_sources` — how many retrieved chunks were available, for the
    citation check. Pass 0 (the default) when there's no retrieval context.

    `judge_fn` — optional `(answer: str) -> str | None` callable. Return a
    short factuality complaint (or None if the answer checks out); wire it to
    an LLM-as-judge call from the *caller* — e.g. a small wrapper around
    `get_llm().chat(...)` — since this module can't import llm.py itself.
    """
    toxicity = _check_toxicity(text)
    if toxicity:
        return OutputCheckResult(
            allowed=False, reason=toxicity,
            message=FRIENDLY_MESSAGE.format(reason=toxicity),
        )

    warnings: list[str] = []

    citation_issue = _check_citations(text, num_sources)
    if citation_issue:
        warnings.append(citation_issue)

    consistency_issue = _check_consistency(text)
    if consistency_issue:
        warnings.append(consistency_issue)

    if judge_fn is not None:
        factuality_issue = judge_fn(text)
        if factuality_issue:
            warnings.append(factuality_issue)

    return OutputCheckResult(allowed=True, warnings=warnings)
