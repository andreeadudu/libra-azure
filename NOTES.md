# NOTES.md — Libra Assist RAG Project

## 1. Îmbunătățiri ingestion (Partea 4)

### Îmbunătățirea 1 — ID-uri stabile pentru chunk-uri

**Fișier modificat:** `app/vectorstore.py`

**Problema:** Metoda `upsert()` genera un UUID random (`uuid.uuid4()`) pentru fiecare chunk la fiecare ingestie. Re-ingestia unui document duplica toate chunk-urile în Qdrant.

**Soluția:** Înlocuit cu `uuid.uuid5(uuid.NAMESPACE_DNS, f"{source}::{index}")` — un UUID determinist derivat din numele sursei și indexul chunk-ului. Același document reingestat produce aceleași ID-uri, deci Qdrant face upsert (înlocuire) în loc de insert (duplicare).

**Demonstrație before/after:**
- Înainte: după 2 rulări ale loader-ului → `points_count: 208`
- După: după 2 rulări ale loader-ului → `points_count: 104` (stabil)

---

### Îmbunătățirea 2 — Metadata reală din headerul YAML

**Fișier modificat:** `code/backend/scripts/ingest_corpus.py`

**Problema:** Documentele aveau headere YAML cu `title`, `product`, `effective`, `version` — dar acestea nu erau extrase și stocate în Qdrant. Filtrarea după produs sau dată era imposibilă.

**Soluția:** Loader-ul parsează headerul YAML al fiecărui document și trimite metadata structurată la API. Exemplu extras pentru `04-taxe-comisioane-2026`:
- `title`: Tabel taxe si comisioane credite de consum 2026
- `product`: credite-consum
- `effective`: 2026-01-01
- `version`: 2

Acum este posibil să filtrezi după `effective` ca să returnezi doar grila 2026, nu și pe cea din 2025.

---

## 2. Îmbunătățiri retrieval (Partea 5)

### Îmbunătățirea 1 — Score threshold (prag minim 0.5)

**Fișier modificat:** `app/main.py`

**Problema:** Retrieval-ul returna întotdeauna `top_k` rezultate, chiar dacă niciun chunk nu era relevant. Chunk-uri slabe (scor 0.3-0.4) ajungeau la model și produceau răspunsuri inventate cu aparentă încredere.

**Soluția:** Chunk-urile cu scor sub 0.5 sunt eliminate înainte de a fi trimise modelului. Dacă nu rămâne niciun chunk, modelul primește context gol și refuză corect.

**Demonstrație:** Întrebarea C2 ("programul sucursalei din Cluj-Napoca") a returnat chunk-uri cu scoruri 0.68 și 0.61 — ambele peste threshold, dar irelevante. Un threshold mai strict (ex: 0.70) ar fi eliminat aceste chunk-uri și forțat un refuz corect. Aceasta rămâne o îmbunătățire de făcut.

---

### Îmbunătățirea 2 — Deduplicare per document sursă

**Fișier modificat:** `app/main.py`

**Problema:** Din același document puteau fi returnate mai multe chunk-uri, ocupând inutil contextul și ascunzând informații din alte documente. Exemplu: din `09-calcul-rambursare-ipotecar` veneau 2 chunk-uri cu scoruri 0.81 și 0.77 pentru aceeași întrebare.

**Soluția:** Funcția `_apply_retrieval_improvements()` păstrează doar cel mai bun chunk per sursă. Rezultatul: context mai divers, răspunsuri mai complete.

**Demonstrație before/after (întrebarea: "Care este comisionul de rambursare anticipata?"):**
- Înainte: 4 chunk-uri retrieved, 2 din același document (`09-calcul-rambursare-ipotecar`)
- După: 1 chunk retrieved, cel mai relevant, fără duplicate

---

## 3. Rezultatele la cele 15 întrebări

### Grup A — Simple retrieval

| # | Întrebare | Răspuns așteptat | Răspuns agent | Rezultat |
|---|---|---|---|---|
| A1 | Suma maximă credit consum | 100.000 RON | Nu găsește suma — chunk a tăiat înainte de secțiunea Caracteristici | ❌ greșit |
| A2 | Venit minim credit consum | 1.500 RON | "Minimum net monthly income: 1.500 RON" | ✅ corect |
| A3 | Comision rambursare 2025 | 1.5% | "1.5% of the prepaid amount for contracts signed in 2025" | ✅ corect |
| A4 | Comision rambursare 2026 | 1% | A zis 1% dar s-a încurcat cu 0.5% din ipotecar, a cerut clarificări | ⚠️ parțial |
| A5 | Zile notificare rambursare | 5 zile lucratoare | "At least 5 working days before" | ✅ corect |
| A6 | Perioada grație card | 55 zile | Nu găsește — chunk s-a oprit înainte de secțiunea Perioada de grație | ❌ greșit |
| A7 | Limită temporară card 2026 | 10.000 RON | Nu găsește — chunk s-a oprit înainte de cifra 10.000 RON | ❌ greșit |

**Scor grup A: 3/7 corecte**

---

### Grup B — Multi-step

| # | Întrebare | Răspuns așteptat | Răspuns agent | Rezultat |
|---|---|---|---|---|
| B1 | Cost rambursare ipotecar perioada fixă | 250 RON comision + dobândă | 0.5% x 50.000 = 250 RON + dobândă acumulată | ✅ corect |
| B2 | Cost rambursare ipotecar perioada variabilă | 0 RON comision + dobândă | Comision 0 RON, doar dobândă acumulată | ✅ corect |
| B3 | Eligibilitate ipotecar vârstă 62 ani pe 5 ani | NU (62+5=67 > 65 ani limită) | NU — vârsta la scadență depășește limita de 65 ani | ✅ corect |
| B4 | Diferență comision 2025 vs 2026 | 1.5% vs 1%, diferență 0.5pp | 1.5% în 2025 față de 1% în 2026 | ✅ corect |
| B5 | Penalități card 45 zile întârziere | ~210 RON | Nu a calculat suma exactă, a descris formula fără rezultat numeric | ⚠️ parțial |

**Scor grup B: 4/5 corecte**

---

### Grup C — Must refuse

| # | Întrebare | Răspuns așteptat | Răspuns agent | Rezultat |
|---|---|---|---|---|
| C1 | Credite studenți | REFUZ | "Libra Bank does not offer dedicated student loans" | ✅ refuzat corect |
| C2 | Program sucursală Cluj-Napoca | REFUZ | A inventat "Monday–Friday 09:00–17:00" preluând orarul din documentul de reclamații | ❌ EȘEC — hallucination |
| C3 | Credite IMM | REFUZ | "No, Libra Bank serves exclusively natural persons" | ✅ refuzat corect |

**Scor grup C: 2/3 corecte**

---

## 4. Scor total

| Grup | Scor |
|---|---|
| A — Simple retrieval | 3/7 |
| B — Multi-step | 4/5 |
| C — Must refuse | 2/3 |
| **Total** | **9/15** |

---

## 5. Ce este încă greșit și ce aș face în continuare

### Problema principală: chunking taie informațiile la mijloc

Cel mai mare număr de eșecuri (A1, A6, A7) vine din faptul că chunking-ul dinamic taie documentele exact înainte de secțiunile cu informații numerice. Chunk-ul 0 din fiecare document conține headerul YAML + introducerea, iar secțiunea "Caracteristici principale" cu sumele și procentele ajunge în chunk-ul următor care nu e recuperat.

**Ce aș face:** Implementa chunking bazat pe headere Markdown (Îmbunătățirea 3 din Partea 4) — fiecare secțiune `##` ar deveni un chunk separat, păstrând titlul secțiunii cu conținutul ei.

### Problema C2: hallucination la întrebări fără răspuns în corpus

Agentul a inventat programul sucursalei din Cluj-Napoca preluând informații dintr-un context irelevant (documentul de reclamații menționează orarul ghișeului pentru depunerea reclamațiilor).

**Ce aș face:** Crește threshold-ul de la 0.5 la 0.70 și adăuga instrucțiuni explicite în persona că informațiile despre sucursale specifice nu sunt în corpus.

### Problema A4: confuzie între produse

Comisionul de 0.5% (ipotecar perioada fixă) și 1% (consum 2026) sunt ambele în corpus și retrieval-ul le aduce pe amândouă, creând confuzie.

**Ce aș face:** Implementa filtre de metadata pe `product` — când întrebarea e despre credite de consum, să caute doar în chunk-urile cu `product=credite-consum`.