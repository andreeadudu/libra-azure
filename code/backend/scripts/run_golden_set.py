#!/usr/bin/env python
"""Run the golden question set against a live /ask and report a score.

    uv run python scripts/run_golden_set.py --label baseline
    uv run python scripts/run_golden_set.py --label after-fix --agent dudu_credit-specialist

Reads data/golden_set.json (question, source docs, and a set of acceptable
phrasings per question), calls POST /ask for each one, and grades the answer
with a case-insensitive substring check — no LLM judge, so the score is cheap
and exactly reproducible by anyone re-running this script. Each question's
`must_contain` is a list of phrase-groups: every group must have at least one
phrase present in the answer (AND across groups, OR within a group). Refusal
questions (`expect_refusal: true`) are graded the same way — their group is
just refusal phrasing instead of a figure.

Appends the run (score, per-question pass/fail, timestamp, label) to
data/golden_set_results.json, so a before/after pair is a durable record in
the repo rather than two numbers pasted into a markdown table by hand.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

API_URL = "http://localhost:7799"
DATA_DIR = Path(__file__).resolve().parent.parent.parent.parent / "data"
GOLDEN_SET = DATA_DIR / "golden_set.json"
RESULTS_LOG = DATA_DIR / "golden_set_results.json"


_DASH_VARIANTS = str.maketrans({"‐": "-", "‑": "-", "‒": "-",
                                 "–": "-", "—": "-"})


def grade(answer: str, must_contain: list[list[str]]) -> tuple[bool, list[str]]:
    """True if every phrase-group has at least one phrase present in `answer`.

    Model output uses typographic hyphens/dashes (non-breaking hyphen, en dash,
    ...) where a phrase list writes a plain ASCII '-' — normalize both before
    matching so a correct answer never fails on punctuation alone.
    """
    lowered = answer.translate(_DASH_VARIANTS).lower()
    missing_groups = []
    for group in must_contain:
        if not any(phrase.lower() in lowered for phrase in group):
            missing_groups.append(" / ".join(group))
    return (not missing_groups), missing_groups


def run(agent: str, agent_mode: str, top_k: int) -> dict:
    data = json.loads(GOLDEN_SET.read_text(encoding="utf-8"))
    results = []
    for q in data["questions"]:
        try:
            r = requests.post(f"{API_URL}/ask", json={
                "question": q["question"], "use_rag": True, "top_k": top_k,
                "agent": agent, "agent_mode": agent_mode,
            }, timeout=60)
            r.raise_for_status()
            answer = r.json()["answer"]
        except Exception as e:                       # noqa: BLE001 — record and keep going
            results.append({**q, "answer": None, "passed": False, "error": str(e)[:200]})
            print(f"  ERR  {q['id']}  {type(e).__name__}: {e}")
            continue

        passed, missing = grade(answer, q["must_contain"])
        results.append({
            "id": q["id"], "group": q["group"], "question": q["question"],
            "expect_refusal": q["expect_refusal"], "answer": answer,
            "passed": passed, "missing": missing,
        })
        mark = "PASS" if passed else "FAIL"
        preview = answer.replace("\n", " ")[:90]
        print(f"  {mark}  {q['id']}  {preview}")

    return {"results": results}


def summarize(results: list[dict]) -> dict:
    by_group: dict[str, list[bool]] = {}
    for r in results:
        by_group.setdefault(r["group"], []).append(r["passed"])
    total_passed = sum(r["passed"] for r in results)
    return {
        "total": f"{total_passed}/{len(results)}",
        "by_group": {g: f"{sum(v)}/{len(v)}" for g, v in sorted(by_group.items())},
    }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--label", required=True, help="e.g. baseline, after-heading-chunking")
    p.add_argument("--agent", default="default")
    p.add_argument("--agent-mode", default="local", choices=["local", "foundry"])
    p.add_argument("--top-k", type=int, default=4)
    args = p.parse_args()

    print(f"Running golden set — agent={args.agent} mode={args.agent_mode} top_k={args.top_k}\n")
    run_data = run(args.agent, args.agent_mode, args.top_k)
    summary = summarize(run_data["results"])

    print(f"\n{summary['total']} correct — by group: {summary['by_group']}")

    entry = {
        "label": args.label,
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "agent": args.agent,
        "agent_mode": args.agent_mode,
        "top_k": args.top_k,
        "summary": summary,
        "results": run_data["results"],
    }
    log = (json.loads(RESULTS_LOG.read_text(encoding="utf-8"))
           if RESULTS_LOG.exists() else {"runs": []})
    log["runs"].append(entry)
    RESULTS_LOG.write_text(json.dumps(log, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nAppended to {RESULTS_LOG.relative_to(DATA_DIR.parent)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
