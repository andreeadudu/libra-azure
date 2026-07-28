# Întrebări de evaluare — Libra Assist RAG

Acest fișier conține setul de 15 întrebări folosit pentru evaluarea sistemului RAG.
Fiecare întrebare are: răspunsul așteptat, documentele sursă și ce a răspuns efectiv asistentul.

---

## Grup A — Simple retrieval (7 întrebări)
> Răspunsul se află într-un singur chunk dintr-un singur document.

---

### A1. Care este suma maximă pentru un credit de consum?
- **Răspuns așteptat:** 100.000 RON
- **Sursă:** `01-ghid-credite-consum`
- **Răspuns agent:** *(de completat după testare)*
- **Rezultat:** *(corect / greșit / refuzat)*

---

### A2. Care este venitul net lunar minim pentru un credit de consum?
- **Răspuns așteptat:** 1.500 RON
- **Sursă:** `02-conditii-eligibilitate-consum`
- **Răspuns agent:** *(de completat după testare)*
- **Rezultat:** *(corect / greșit / refuzat)*

---

### A3. Care este comisionul de rambursare anticipată pentru contractele din 2025?
- **Răspuns așteptat:** 1.5% din suma rambursată anticipat
- **Sursă:** `03-taxe-comisioane-2025`
- **Răspuns agent:** *(de completat după testare)*
- **Rezultat:** *(corect / greșit / refuzat)*

---

### A4. Care este comisionul de rambursare anticipată pentru contractele din 2026?
- **Răspuns așteptat:** 1% din suma rambursată anticipat
- **Sursă:** `04-taxe-comisioane-2026`, `06-penalitati-rambursare`
- **Răspuns agent:** *(de completat după testare)*
- **Rezultat:** *(corect / greșit / refuzat)*

---

### A5. Cu câte zile înainte trebuie să notific banca pentru rambursare anticipată?
- **Răspuns așteptat:** 5 zile lucratoare
- **Sursă:** `05-procedura-rambursare-anticipata`
- **Răspuns agent:** *(de completat după testare)*
- **Rezultat:** *(corect / greșit / refuzat)*

---

### A6. Care este perioada de grație la cardul de credit Libra Bank?
- **Răspuns așteptat:** 55 de zile fără dobândă pentru cumpărături
- **Sursă:** `11-ghid-card-credit`
- **Răspuns agent:** *(de completat după testare)*
- **Rezultat:** *(corect / greșit / refuzat)*

---

### A7. Care este limita maximă temporară a cardului de credit începând cu ianuarie 2026?
- **Răspuns așteptat:** 10.000 RON (crescută de la 5.000 RON)
- **Sursă:** `12-limita-card-credit`
- **Răspuns agent:** *(de completat după testare)*
- **Rezultat:** *(corect / greșit / refuzat)*

---

## Grup B — Multi-step (5 întrebări)
> Răspunsul necesită combinarea mai multor documente, un calcul sau o condiție de verificat.

---

### B1. Am un credit ipotecar cu sold rămas de 200.000 RON și vreau să rambursez anticipat 50.000 RON în perioada cu dobândă fixă. Cât mă costă?
- **Răspuns așteptat:** Comision 0.5% x 50.000 = 250 RON + dobânda acumulată de la ultima rată
- **Sursă:** `09-calcul-rambursare-ipotecar` + `07-ghid-credit-ipotecar`
- **Ce face dificil:** necesită identificarea perioadei (fixă vs variabilă) și aplicarea formulei
- **Răspuns agent:** *(de completat după testare)*
- **Rezultat:** *(corect / greșit / refuzat)*

---

### B2. Același credit ipotecar, dar rambursez după ce trec cei 5 ani în perioada variabilă. Cât mă costă acum?
- **Răspuns așteptat:** Comision 0 RON + doar dobânda acumulată până la data rambursării
- **Sursă:** `09-calcul-rambursare-ipotecar`
- **Ce face dificil:** condiție de verificat (perioada fixă vs variabilă schimbă complet răspunsul)
- **Răspuns agent:** *(de completat după testare)*
- **Rezultat:** *(corect / greșit / refuzat)*

---

### B3. Pot lua un credit ipotecar dacă am 62 de ani și vreau credit pe 5 ani?
- **Răspuns așteptat:** Da, pentru că la scadență ar avea 67 ani, dar limita e 65 ani — deci NU este eligibil
- **Sursă:** `08-eligibilitate-ipotecar` + `07-ghid-credit-ipotecar`
- **Ce face dificil:** calcul de vârstă (62 + 5 = 67 > 65) + condiție din alt document
- **Răspuns agent:** *(de completat după testare)*
- **Rezultat:** *(corect / greșit / refuzat)*

---

### B4. Care este diferența dintre comisionul de rambursare anticipată pentru un contract semnat în decembrie 2025 față de unul semnat în ianuarie 2026?
- **Răspuns așteptat:** 2025: 1.5%, 2026: 1% — diferență de 0.5 puncte procentuale
- **Sursă:** `03-taxe-comisioane-2025` + `04-taxe-comisioane-2026`
- **Ce face dificil:** near-duplicate care diferă, necesită compararea ambelor documente
- **Răspuns agent:** *(de completat după testare)*
- **Rezultat:** *(corect / greșit / refuzat)*

---

### B5. Am un card de credit cu sold de 5.000 RON. Nu am plătit rata de 45 de zile. Ce penalități am acumulat?
- **Răspuns așteptat:** Primele 30 zile: 0.08%/zi x 5000 x 30 = 120 RON; zilele 31-45: 0.12%/zi x 5000 x 15 = 90 RON; total ~210 RON
- **Sursă:** `04-taxe-comisioane-2026` + `11-ghid-card-credit`
- **Ce face dificil:** calcul în două etape cu rate diferite + combinarea a două documente
- **Răspuns agent:** *(de completat după testare)*
- **Rezultat:** *(corect / greșit / refuzat)*

---

## Grup C — Must refuse (3 întrebări)
> Răspunsul nu există în corpus. Un răspuns inventat este un eșec.

---

### C1. Ce dobândă oferă Libra Bank la creditele pentru studenți?
- **Răspuns așteptat:** REFUZ — Libra Bank nu oferă credite studențești (menționat explicit în doc 15)
- **Sursă:** `15-produse-indisponibile`
- **Răspuns agent:** *(de completat după testare)*
- **Rezultat:** *(refuzat corect / a inventat — EȘEC)*

---

### C2. Care este programul de lucru al sucursalei Libra Bank din Cluj-Napoca?
- **Răspuns așteptat:** REFUZ — informația nu există în corpus
- **Sursă:** niciun document
- **Răspuns agent:** *(de completat după testare)*
- **Rezultat:** *(refuzat corect / a inventat — EȘEC)*

---

### C3. Ofera Libra Bank credite pentru firme mici (IMM)?
- **Răspuns așteptat:** REFUZ — Libra Bank deservește exclusiv persoane fizice (menționat în doc 15)
- **Sursă:** `15-produse-indisponibile`
- **Răspuns agent:** *(de completat după testare)*
- **Rezultat:** *(refuzat corect / a inventat — EȘEC)*

---

## Rezumat rezultate

| # | Întrebare | Rezultat |
|---|---|---|
| A1 | Suma maximă credit consum | *(de completat)* |
| A2 | Venit minim credit consum | *(de completat)* |
| A3 | Comision rambursare 2025 | *(de completat)* |
| A4 | Comision rambursare 2026 | *(de completat)* |
| A5 | Zile notificare rambursare | *(de completat)* |
| A6 | Perioada grație card | *(de completat)* |
| A7 | Limită temporară card 2026 | *(de completat)* |
| B1 | Cost rambursare ipotecar perioada fixă | *(de completat)* |
| B2 | Cost rambursare ipotecar perioada variabilă | *(de completat)* |
| B3 | Eligibilitate ipotecar vârstă 62 ani | *(de completat)* |
| B4 | Diferență comision 2025 vs 2026 | *(de completat)* |
| B5 | Penalități card 45 zile întârziere | *(de completat)* |
| C1 | Credite studenți | *(de completat)* |
| C2 | Program sucursală Cluj | *(de completat)* |
| C3 | Credite IMM | *(de completat)* |