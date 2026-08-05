# Fictional bank corpus - Libra Bank

This corpus contains fictional documents created for testing the Libra Assist RAG system.
All data is invented and does not represent real products.

## Domain

Consumer loans, mortgage loans, and credit cards of the fictional bank Libra Bank.

## Document list

| File | Content | Cases covered |
|---|---|---|
| 01-consumer-loan-guide.md | General overview of consumer loans | General information |
| 02-consumer-loan-eligibility.md | Conditions for applying for a consumer loan | General information |
| 03-fees-and-commissions-2025.md | Fee schedule valid in 2025 | Near-duplicate, table |
| 04-fees-and-commissions-2026.md | Fee schedule valid in 2026 | Near-duplicate, table, version contradiction |
| 05-prepayment-procedure.md | Steps for early repayment | Long step-by-step procedure |
| 06-prepayment-penalties.md | Exact repayment fees | Precise figure (1%) |
| 07-mortgage-loan-guide.md | General overview of mortgage loans | General information |
| 08-mortgage-eligibility.md | Mortgage eligibility conditions | Two documents to combine |
| 09-mortgage-prepayment-calculation.md | Calculating the mortgage prepayment cost | Two documents to combine |
| 10-fixed-vs-variable-interest.md | Interest rate comparison | General information |
| 11-credit-card-guide.md | Credit card overview | General information |
| 12-credit-card-limit.md | Card limit change | Version contradiction (Jan 2026) |
| 13-complaints-procedure.md | Steps for filing a complaint | Long step-by-step procedure |
| 14-frequently-asked-questions.md | Loan FAQ | General information |
| 15-unavailable-products.md | What the bank does not offer | Intentionally absent |

## Cases covered (out of the 7 required)

1. Precise figure: the prepayment fee is exactly 1% (doc 06)
2. Two documents to combine: mortgage eligibility (08) + repayment calculation (09)
3. Differing near-duplicate: 2025 fees (03) vs 2026 fees (04)
4. Long step-by-step procedure: prepayment (05) and complaints (13)
5. Table: fee schedule in documents 03 and 04
6. Contradiction between versions: card limit raised from 5,000 to 10,000 RON as of Jan 2026 (12)
7. Something intentionally absent: student loans do not exist at Libra Bank (15)

## Evaluation — golden question set

- `questions.md` — the 15 questions in prose (question / expected answer / source doc),
  grouped A (simple retrieval, 7), B (multi-step, 5), C (must refuse, 3).
- `golden_set.json` — the same 15 questions, structured for
  `code/backend/scripts/run_golden_set.py`: each question carries the acceptable
  phrasings its answer must contain (English and Romanian, since the agent sometimes
  answers in Romanian even for an English question), so the score is machine-checked
  and reproducible instead of filled in by hand.
- `golden_set_results.json` — every run of the script, appended, not overwritten: label,
  timestamp, per-question pass/fail and the full answer text. This is the before/after
  record — see `NOTES.md` for the numbers and what changed in between.

Run it yourself:

```bash
cd code/backend
uv run python scripts/ingest_corpus.py         # loads the 15 docs into Qdrant
uv run python scripts/run_golden_set.py --label "my-run" --agent default
```
