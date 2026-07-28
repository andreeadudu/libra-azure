# Corpus bancar fictiv - Libra Bank

Acest corpus contine documente fictive create pentru testarea sistemului RAG Libra Assist.
Toate datele sunt inventate si nu reprezinta produse reale.

## Domeniu

Credite de consum, credite ipotecare si carduri de credit ale bancii fictive Libra Bank.

## Lista documente

| Fisier | Continut | Cazuri acoperite |
|---|---|---|
| 01-ghid-credite-consum.md | Prezentare generala credite consum | Informatii generale |
| 02-conditii-eligibilitate-consum.md | Conditii pentru aplicare credit consum | Informatii generale |
| 03-taxe-comisioane-2025.md | Grila de taxe valabila in 2025 | Near-duplicate, tabel |
| 04-taxe-comisioane-2026.md | Grila de taxe valabila in 2026 | Near-duplicate, tabel, contradictie versiuni |
| 05-procedura-rambursare-anticipata.md | Pasi pentru rambursare anticipata | Procedura lunga cu pasi |
| 06-penalitati-rambursare.md | Comisioane exacte rambursare | Numar precis (1%) |
| 07-ghid-credit-ipotecar.md | Prezentare generala credit ipotecar | Informatii generale |
| 08-eligibilitate-ipotecar.md | Conditii eligibilitate ipotecar | Doua documente de combinat |
| 09-calcul-rambursare-ipotecar.md | Calcul cost rambursare ipotecar | Doua documente de combinat |
| 10-dobanzi-fixe-variabile.md | Comparatie dobanzi | Informatii generale |
| 11-ghid-card-credit.md | Prezentare card de credit | Informatii generale |
| 12-limita-card-credit.md | Modificare limita card | Contradictie versiuni (ian 2026) |
| 13-procedura-reclamatii.md | Pasi pentru depunere reclamatie | Procedura lunga cu pasi |
| 14-intrebari-frecvente.md | FAQ credite | Informatii generale |
| 15-produse-indisponibile.md | Ce nu ofera banca | Absent intentionat |

## Cazuri acoperite (din cele 7 cerute)

1. Numar precis: comisionul de rambursare anticipata este exact 1% (doc 06)
2. Doua documente de combinat: eligibilitate ipotecar (08) + calcul rambursare (09)
3. Near-duplicate care difera: taxe 2025 (03) vs taxe 2026 (04)
4. Procedura lunga cu pasi: rambursare anticipata (05) si reclamatii (13)
5. Tabel: grila taxe din documentele 03 si 04
6. Contradictie intre versiuni: limita card crescuta de la 5.000 la 10.000 RON din ian 2026 (12)
7. Ceva absent intentionat: credite studentesti nu exista la Libra Bank (15)
