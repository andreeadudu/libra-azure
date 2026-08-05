"""Input guardrail — screens user turns for sensitive/toxic topics before they
ever reach the model.

This is a fast, deterministic keyword/regex screen, not a classifier — it runs
before every LLM call and costs no tokens. It trades recall for determinism:
expect it to miss paraphrases and multilingual variants, and treat it as the
floor you'd put in front of a real moderation model (e.g. Azure AI Content
Safety) in production, not a replacement for one.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

# Category -> regex patterns (case-insensitive, matched anywhere in the text).
# Keep patterns narrow and specific to minimize false positives on legitimate
# questions (e.g. "self_harm" support-line questions should still get through).
SENSITIVE_TOPICS: dict[str, list[str]] = {
    "self_harm": [
        r"\bsuicid", r"\bself[- ]harm\b", r"\bkill myself\b", r"\bend my life\b",
    ],
    "violence": [
        r"\bhow (to|do i) (make|build) a bomb\b", r"\bmass shooting\b",
        r"\b(how to )?kill (him|her|them|someone)\b",
    ],
    "hate_speech": [
        r"\bracial slur\b", r"\bethnic cleansing\b", r"\bsubhuman\b",
    ],
    "csam": [
        r"\bchild (sexual|porn)", r"\bcsam\b",
    ],
    "illegal_activity": [
        r"\bhow to (make|cook) (meth|crystal meth)\b", r"\blaunder money\b",
        r"\bbuy stolen (goods|credit cards?|cards?)\b",
    ],
    "weapons": [
        r"\bbuild an? (gun|firearm|explosive)\b", r"\bmake (a )?bioweapon\b",
    ],
    "harassment": [
        r"\bdoxx?\b", r"\bswat(ting)?\b",
    ],
}

FRIENDLY_MESSAGE = (
    "I can't help with that — it touches a topic ({category}) this assistant "
    "is scoped away from. Try rephrasing, or ask about something else I can "
    "help with."
)


@dataclass
class InputCheckResult:
    blocked: bool
    category: str | None = None
    message: str | None = None


def check_input(text: str) -> InputCheckResult:
    """Screen a user turn. Call this before building the prompt in chat()."""
    lowered = text.lower()
    for category, patterns in SENSITIVE_TOPICS.items():
        for pattern in patterns:
            if re.search(pattern, lowered):
                return InputCheckResult(
                    blocked=True,
                    category=category,
                    message=FRIENDLY_MESSAGE.format(category=category.replace("_", " ")),
                )
    return InputCheckResult(blocked=False)
