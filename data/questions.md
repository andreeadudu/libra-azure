# Evaluation questions — Libra Assist RAG

This file contains the set of 15 questions used to evaluate the RAG system.
Each question has: the expected answer, the source documents, and what the assistant actually answered.

---

## Group A — Simple retrieval (7 questions)
> The answer is found in a single chunk from a single document.

---

### A1. What is the maximum amount for a consumer loan?
- **Expected answer:** 100,000 RON
- **Source:** `01-consumer-loan-guide`
- **Agent answer:** *(to be filled in after testing)*
- **Result:** *(correct / wrong / refused)*

---

### A2. What is the minimum net monthly income for a consumer loan?
- **Expected answer:** 1,500 RON
- **Source:** `02-consumer-loan-eligibility`
- **Agent answer:** *(to be filled in after testing)*
- **Result:** *(correct / wrong / refused)*

---

### A3. What is the prepayment fee for contracts from 2025?
- **Expected answer:** 1.5% of the prepaid amount
- **Source:** `03-fees-and-commissions-2025`
- **Agent answer:** *(to be filled in after testing)*
- **Result:** *(correct / wrong / refused)*

---

### A4. What is the prepayment fee for contracts from 2026?
- **Expected answer:** 1% of the prepaid amount
- **Source:** `04-fees-and-commissions-2026`, `06-prepayment-penalties`
- **Agent answer:** *(to be filled in after testing)*
- **Result:** *(correct / wrong / refused)*

---

### A5. How many days in advance must I notify the bank for prepayment?
- **Expected answer:** 5 working days
- **Source:** `05-prepayment-procedure`
- **Agent answer:** *(to be filled in after testing)*
- **Result:** *(correct / wrong / refused)*

---

### A6. What is the grace period on the Libra Bank credit card?
- **Expected answer:** 55 interest-free days for purchases
- **Source:** `11-credit-card-guide`
- **Agent answer:** *(to be filled in after testing)*
- **Result:** *(correct / wrong / refused)*

---

### A7. What is the maximum temporary credit card limit starting January 2026?
- **Expected answer:** 10,000 RON (raised from 5,000 RON)
- **Source:** `12-credit-card-limit`
- **Agent answer:** *(to be filled in after testing)*
- **Result:** *(correct / wrong / refused)*

---

## Group B — Multi-step (5 questions)
> The answer requires combining several documents, a calculation, or a condition to check.

---

### B1. I have a mortgage with a remaining balance of 200,000 RON and want to prepay 50,000 RON during the fixed-rate period. How much does it cost me?
- **Expected answer:** 0.5% x 50,000 = 250 RON fee + interest accrued since the last installment
- **Source:** `09-mortgage-prepayment-calculation` + `07-mortgage-loan-guide`
- **What makes it hard:** requires identifying the period (fixed vs variable) and applying the formula
- **Agent answer:** *(to be filled in after testing)*
- **Result:** *(correct / wrong / refused)*

---

### B2. Same mortgage, but I repay after the 5-year fixed period ends, during the variable period. How much does it cost me now?
- **Expected answer:** 0 RON fee + only the interest accrued up to the repayment date
- **Source:** `09-mortgage-prepayment-calculation`
- **What makes it hard:** a condition to check (fixed vs variable period completely changes the answer)
- **Agent answer:** *(to be filled in after testing)*
- **Result:** *(correct / wrong / refused)*

---

### B3. Can I take out a mortgage if I am 62 years old and want a 5-year loan term?
- **Expected answer:** No, because at maturity they would be 67, but the limit is 65 years — so NOT eligible
- **Source:** `08-mortgage-eligibility` + `07-mortgage-loan-guide`
- **What makes it hard:** an age calculation (62 + 5 = 67 > 65) + a condition from another document
- **Agent answer:** *(to be filled in after testing)*
- **Result:** *(correct / wrong / refused)*

---

### B4. What is the difference between the prepayment fee for a contract signed in December 2025 versus one signed in January 2026?
- **Expected answer:** 2025: 1.5%, 2026: 1% — a difference of 0.5 percentage points
- **Source:** `03-fees-and-commissions-2025` + `04-fees-and-commissions-2026`
- **What makes it hard:** a differing near-duplicate, requires comparing both documents
- **Agent answer:** *(to be filled in after testing)*
- **Result:** *(correct / wrong / refused)*

---

### B5. I have a credit card with a balance of 5,000 RON. I haven't paid my installment for 45 days. What penalties have I accumulated?
- **Expected answer:** First 30 days: 0.08%/day x 5000 x 30 = 120 RON; days 31-45: 0.12%/day x 5000 x 15 = 90 RON; total ~210 RON
- **Source:** `04-fees-and-commissions-2026` + `11-credit-card-guide`
- **What makes it hard:** a two-stage calculation with different rates + combining two documents
- **Agent answer:** *(to be filled in after testing)*
- **Result:** *(correct / wrong / refused)*

---

## Group C — Must refuse (3 questions)
> The answer does not exist in the corpus. A made-up answer is a failure.

---

### C1. What interest rate does Libra Bank offer on student loans?
- **Expected answer:** REFUSE — Libra Bank does not offer student loans (explicitly mentioned in doc 15)
- **Source:** `15-unavailable-products`
- **Agent answer:** *(to be filled in after testing)*
- **Result:** *(correctly refused / made something up — FAILURE)*

---

### C2. What are the opening hours of the Libra Bank branch in Cluj-Napoca?
- **Expected answer:** REFUSE — the information does not exist in the corpus
- **Source:** no document
- **Agent answer:** *(to be filled in after testing)*
- **Result:** *(correctly refused / made something up — FAILURE)*

---

### C3. Does Libra Bank offer loans for small businesses (SMEs)?
- **Expected answer:** REFUSE — Libra Bank serves exclusively individuals (mentioned in doc 15)
- **Source:** `15-unavailable-products`
- **Agent answer:** *(to be filled in after testing)*
- **Result:** *(correctly refused / made something up — FAILURE)*

---

## Results summary

| # | Question | Result |
|---|---|---|
| A1 | Maximum consumer loan amount | *(to be filled in)* |
| A2 | Minimum income for a consumer loan | *(to be filled in)* |
| A3 | Prepayment fee 2025 | *(to be filled in)* |
| A4 | Prepayment fee 2026 | *(to be filled in)* |
| A5 | Prepayment notice period | *(to be filled in)* |
| A6 | Card grace period | *(to be filled in)* |
| A7 | Temporary card limit 2026 | *(to be filled in)* |
| B1 | Mortgage prepayment cost, fixed-rate period | *(to be filled in)* |
| B2 | Mortgage prepayment cost, variable-rate period | *(to be filled in)* |
| B3 | Mortgage eligibility at age 62 | *(to be filled in)* |
| B4 | Fee difference 2025 vs 2026 | *(to be filled in)* |
| B5 | Card penalties for 45 days of delay | *(to be filled in)* |
| C1 | Student loans | *(to be filled in)* |
| C2 | Cluj branch opening hours | *(to be filled in)* |
| C3 | SME loans | *(to be filled in)* |
