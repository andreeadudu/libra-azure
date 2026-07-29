# NOTES.md — Libra Assist RAG Project

## 1. Ingestion improvements 

### Improvement 1 — Stable chunk IDs

**File modified:** `app/vectorstore.py`

**Problem:** The `upsert()` method generated a random UUID (`uuid.uuid4()`) for every chunk on every ingestion run. Re-ingesting a document duplicated all of its chunks in Qdrant.

**Solution:** Replaced it with `uuid.uuid5(uuid.NAMESPACE_DNS, f"{source}::{index}")` — a deterministic UUID derived from the source name and the chunk index. Re-ingesting the same document produces the same IDs, so Qdrant performs an upsert (replacement) instead of an insert (duplication).

**Before/after demonstration:**
- Before: after 2 loader runs → `points_count: 208`
- After: after 2 loader runs → `points_count: 104` (stable)

---

### Improvement 2 — Real metadata from the YAML header

**File modified:** `code/backend/scripts/ingest_corpus.py`

**Problem:** The documents had YAML headers with `title`, `product`, `effective` and `version` — but these were never extracted and stored in Qdrant. Filtering by product or date was impossible.

**Solution:** The loader parses each document's YAML header and sends structured metadata to the API. Example extracted for `04-fees-and-commissions-2026`:
- `title`: Tabel taxe si comisioane credite de consum 2026
- `product`: credite-consum
- `effective`: 2026-01-01
- `version`: 2

It is now possible to filter by `effective` so that only the 2026 fee schedule is returned, not the 2025 one as well.

---

## 2. Retrieval improvements 

### Improvement 1 — Score threshold (minimum 0.5)

**File modified:** `app/main.py`

**Problem:** Retrieval always returned `top_k` results, even when no chunk was relevant. Weak chunks (score 0.3–0.4) reached the model and produced confidently invented answers.

**Solution:** Chunks scoring below 0.5 are dropped before being sent to the model. If no chunk survives, the model receives an empty context and correctly refuses.

**Demonstration:** Question C2 ("opening hours of the Cluj-Napoca branch") returned chunks with scores 0.68 and 0.61 — both above the threshold, but irrelevant. A stricter threshold (e.g. 0.70) would have removed these chunks and forced a correct refusal. This is still an open improvement.

---

### Improvement 2 — Deduplication per source document

**File modified:** `app/main.py`

**Problem:** Several chunks could be returned from the same document, wasting context and hiding information from other documents. Example: `09-mortgage-prepayment-calculation` returned 2 chunks with scores 0.81 and 0.77 for the same question.

**Solution:** The `_apply_retrieval_improvements()` function keeps only the best-scoring chunk per source. The result: a more diverse context and more complete answers.

**Before/after demonstration (question: "Care este comisionul de rambursare anticipata?"):**
- Before: 4 chunks retrieved, 2 of them from the same document (`09-mortgage-prepayment-calculation`)
- After: 1 chunk retrieved, the most relevant one, no duplicates

---

## 3. Results on the 15 questions

### Group A — Simple retrieval

| # | Question | Expected answer | Agent answer | Result |
|---|---|---|---|---|
| A1 | Maximum consumer loan amount | 100,000 RON | Does not find the amount — the chunk was cut off before the Features section | ❌ wrong |
| A2 | Minimum income for a consumer loan | 1,500 RON | "Minimum net monthly income: 1.500 RON" | ✅ correct |
| A3 | Prepayment fee 2025 | 1.5% | "1.5% of the prepaid amount for contracts signed in 2025" | ✅ correct |
| A4 | Prepayment fee 2026 | 1% | Said 1% but mixed it up with the 0.5% mortgage fee and asked for clarification | ⚠️ partial |
| A5 | Prepayment notice period | 5 working days | "At least 5 working days before" | ✅ correct |
| A6 | Credit card grace period | 55 days | Does not find it — the chunk stopped before the Grace period section | ❌ wrong |
| A7 | Temporary card limit 2026 | 10,000 RON | Does not find it — the chunk stopped before the 10,000 RON figure | ❌ wrong |

**Group A score: 3/7 correct**

---

### Group B — Multi-step

| # | Question | Expected answer | Agent answer | Result |
|---|---|---|---|---|
| B1 | Cost of mortgage prepayment during the fixed-rate period | 250 RON fee + interest | 0.5% x 50,000 = 250 RON + accrued interest | ✅ correct |
| B2 | Cost of mortgage prepayment during the variable-rate period | 0 RON fee + interest | 0 RON fee, only accrued interest | ✅ correct |
| B3 | Mortgage eligibility at age 62 over a 5-year term | NO (62+5=67 > 65-year limit) | NO — age at maturity exceeds the 65-year limit | ✅ correct |
| B4 | Difference between the 2025 and 2026 fee | 1.5% vs 1%, a 0.5pp difference | 1.5% in 2025 versus 1% in 2026 | ✅ correct |
| B5 | Card penalties for 45 days of delay | ~210 RON | Did not compute the exact amount, described the formula without a numeric result | ⚠️ partial |

**Group B score: 4/5 correct**

---

### Group C — Must refuse

| # | Question | Expected answer | Agent answer | Result |
|---|---|---|---|---|
| C1 | Student loans | REFUSE | "Libra Bank does not offer dedicated student loans" | ✅ correctly refused |
| C2 | Cluj-Napoca branch opening hours | REFUSE | Invented "Monday–Friday 09:00–17:00", taking the schedule from the complaints document | ❌ FAILURE — hallucination |
| C3 | SME loans | REFUSE | "No, Libra Bank serves exclusively natural persons" | ✅ correctly refused |

**Group C score: 2/3 correct**

---

## 4. Total score

| Group | Score |
|---|---|
| A — Simple retrieval | 3/7 |
| B — Multi-step | 4/5 |
| C — Must refuse | 2/3 |
| **Total** | **9/15** |

---

## 5. What is still wrong and what I would do next

### Main problem: chunking cuts information in half

The largest group of failures (A1, A6, A7) comes from dynamic chunking cutting documents right before the sections that hold the numeric information. Chunk 0 of every document contains the YAML header plus the introduction, while the "Caracteristici principale" section with the amounts and percentages ends up in the next chunk, which is not retrieved.

**What I would do:** Implement Markdown-header-based chunking (Improvement 3 from Part 4) — each `##` section would become its own chunk, keeping the section title together with its content.

This chunking failure is systemic, not isolated — it also affects the mortgage product's maximum amount (1,500,000 RON, doc `07-mortgage-loan-guide`), reproduced with a different persona ("Credit Product Specialist"), confirming the root cause is chunk boundaries, not persona-specific behavior.

### Problem C2: hallucination on questions with no answer in the corpus

The agent invented the Cluj-Napoca branch opening hours by picking up information from an irrelevant context (the complaints document mentions the counter's opening hours for submitting complaints).

**What I would do:** Raise the threshold from 0.5 to 0.70 and add explicit instructions to the persona stating that information about specific branches is not in the corpus.

### Problem A4: confusion between products

The 0.5% fee (mortgage, fixed-rate period) and the 1% fee (consumer loan, 2026) are both in the corpus and retrieval brings back both, which creates confusion.

**What I would do:** Implement metadata filters on `product` — when the question is about consumer loans, search only in chunks with `product=credite-consum`.
