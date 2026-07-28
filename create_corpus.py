import os

output_dir = r"C:\Users\andreea.dudu\Desktop\ai-acad-foundry-2026\data"
os.makedirs(output_dir, exist_ok=True)

files = {}

files["01-ghid-credite-consum.md"] = """---
title: Ghid general credite de consum
product: credite-consum
audience: retail
effective: 2026-01-01
version: 2
---

# Ghid general - Credite de consum

Libra Bank ofera credite de consum persoanelor fizice cu varsta intre 18 si 70 de ani, rezidente in Romania, cu venituri stabile si dovedite.

## Ce este un credit de consum?

Un credit de consum este un imprumut acordat pentru nevoi personale: achizitii de bunuri, renovari, vacante, cheltuieli medicale sau orice alta destinatie neprofesionala. Suma imprumutata se restituie in rate lunare egale pe durata convenita.

## Caracteristici principale

- Suma minima: 1.000 RON
- Suma maxima: 100.000 RON
- Durata minima: 6 luni
- Durata maxima: 60 de luni
- Moneda: RON
- Tipul dobanzii: fixa pe toata durata contractului

## Dobanda anuala efectiva (DAE)

DAE include dobanda nominala si toate comisioanele obligatorii:
- Clienti cu scor excelent: DAE intre 8% si 12%
- Clienti cu scor bun: DAE intre 12% si 18%
- Clienti cu scor standard: DAE intre 18% si 24%

## Cum se acorda creditul?

Creditul se acorda exclusiv in contul curent al clientului deschis la Libra Bank. Daca clientul nu are cont curent, deschiderea acestuia este obligatorie inainte de acordarea creditului.

## Unde poti aplica?

- Orice sucursala Libra Bank din Romania
- Aplicatia mobila Libra Mobile
- Prin partenerul de vanzari autorizat
"""

files["02-conditii-eligibilitate-consum.md"] = """---
title: Conditii de eligibilitate credite de consum
product: credite-consum
audience: retail
effective: 2026-01-01
version: 3
---

# Conditii de eligibilitate - Credite de consum

## Conditii obligatorii

1. Varsta minima 18 ani la data depunerii cererii
2. Varsta maxima 70 ani la data scadentei finale
3. Cetatenie romana sau permis de sedere permanent in Romania
4. Venit net lunar minim de 1.500 RON din surse acceptate
5. Vechime minima la actualul angajator: 3 luni pentru contract nedeterminat
6. Fara restante active in Biroul de Credit la data solicitarii
7. Fara executari silite active

## Surse de venit acceptate

- Salariu net din contracte de munca pe durata nedeterminata
- Pensie de stat sau pensie privata
- Venituri din chirii dovedite cu contracte inregistrate la ANAF
- Dividende dovedite cu ultimele doua declaratii fiscale

## Documente necesare

- Carte de identitate valabila
- Adeverinta de salariu emisa in ultimele 30 de zile
- Ultimele 3 fluturasi de salariu
- Extras de cont pentru ultimele 3 luni

## Conditii care duc la respingerea automata

- Restante curente in Biroul de Credit peste 30 de zile
- Dosar de insolventa sau faliment personal activ
- Venit exclusiv din activitati ocazionale nedovedite
"""

files["03-taxe-comisioane-2025.md"] = """---
title: Tabel taxe si comisioane credite de consum 2025
product: credite-consum
audience: retail
effective: 2025-01-01
version: 1
---

# Taxe si comisioane - Credite de consum (valabile in 2025)

## Comisioane la acordare

| Tip comision | Valoare |
|---|---|
| Comision de analiza dosar | 150 RON |
| Comision de acordare | 1% din suma creditata, minim 100 RON |
| Comision de administrare lunar | 0.15% din soldul curent |

## Comisioane pe parcursul creditului

| Tip comision | Valoare |
|---|---|
| Comision rambursare anticipata partiala | 1.5% din suma rambursata anticipat |
| Comision rambursare anticipata totala | 1.5% din soldul ramas |
| Comision modificare scadenta | 50 RON per operatiune |
| Comision extras de cont la ghiseu | 5 RON |
| Comision duplicat contract | 30 RON |

## Penalitati

| Situatie | Penalitate |
|---|---|
| Rata platita cu intarziere 1-30 zile | 0.1% pe zi din rata restanta |
| Rata platita cu intarziere peste 30 zile | 0.15% pe zi din rata restanta |

Valabil pentru contractele semnate intre 01.01.2025 si 31.12.2025.
"""

files["04-taxe-comisioane-2026.md"] = """---
title: Tabel taxe si comisioane credite de consum 2026
product: credite-consum
audience: retail
effective: 2026-01-01
version: 2
---

# Taxe si comisioane - Credite de consum (valabile in 2026)

## Comisioane la acordare

| Tip comision | Valoare |
|---|---|
| Comision de analiza dosar | 100 RON |
| Comision de acordare | 0.5% din suma creditata, minim 50 RON |
| Comision de administrare lunar | 0.10% din soldul curent |

## Comisioane pe parcursul creditului

| Tip comision | Valoare |
|---|---|
| Comision rambursare anticipata partiala | 1% din suma rambursata anticipat |
| Comision rambursare anticipata totala | 1% din soldul ramas |
| Comision modificare scadenta | 35 RON per operatiune |
| Comision extras de cont la ghiseu | 5 RON |
| Comision duplicat contract | 30 RON |

## Penalitati

| Situatie | Penalitate |
|---|---|
| Rata platita cu intarziere 1-30 zile | 0.08% pe zi din rata restanta |
| Rata platita cu intarziere peste 30 zile | 0.12% pe zi din rata restanta |

ATENTIE: Fata de grila 2025, comisionul de rambursare anticipata a scazut de la 1.5% la 1%.
Valabil exclusiv pentru contractele noi semnate incepand cu 01.01.2026.
"""

files["05-procedura-rambursare-anticipata.md"] = """---
title: Procedura de rambursare anticipata credit de consum
product: credite-consum
audience: retail
effective: 2026-01-01
version: 2
---

# Procedura de rambursare anticipata - Credit de consum

## Pasul 1: Notificarea bancii

Clientul notifica Libra Bank cu cel putin 5 zile lucratoare inainte de data dorita. Notificarea se face prin:
- Cerere scrisa depusa la orice sucursala Libra Bank
- Mesaj securizat prin aplicatia Libra Mobile
- Email la credite@librabank.ro cu subiectul: RAMBURSARE ANTICIPATA + numarul contractului

## Pasul 2: Primirea ofertei de rambursare

In maximum 2 zile lucratoare, banca transmite o oferta scrisa cu:
- Soldul ramas la data rambursarii
- Comisionul de rambursare anticipata aplicabil
- Dobanda acumulata pana la data rambursarii
- Suma totala de plata
- Contul in care trebuie efectuata plata
- Termenul de valabilitate al ofertei: 5 zile lucratoare

## Pasul 3: Confirmarea acceptarii ofertei

Clientul confirma acceptarea prin:
- Semnatura pe oferta la ghiseu
- Confirmare prin aplicatia Libra Mobile
- Raspuns email la oferta primita

## Pasul 4: Efectuarea platii

Clientul efectueaza plata sumei totale din oferta in contul indicat, prin:
- Ordin de plata la ghiseu
- Transfer bancar din aplicatia Libra Mobile
- Transfer interbancar din alta banca

## Pasul 5: Confirmarea rambursarii

In maximum 1 zi lucratoare de la primirea platii, banca:
- Inchide creditul in sistem (pentru rambursare totala)
- Recalculeaza noul grafic de rambursare (pentru rambursare partiala)
- Emite o adeverinta de rambursare / inchidere credit

## Pasul 6: Ridicarea documentelor

Pentru rambursare totala, clientul primeste:
- Adeverinta de inchidere credit
- Originalul contractului de credit

## Atentie

Daca plata nu este efectuata in termenul de valabilitate al ofertei, procedura se reia de la Pasul 1.
"""

files["06-penalitati-rambursare.md"] = """---
title: Penalitati si comisioane rambursare anticipata
product: credite-consum
audience: retail
effective: 2026-01-01
version: 2
---

# Penalitati si comisioane - Rambursare anticipata

## Comisionul de rambursare anticipata

Conform contractelor semnate incepand cu 01.01.2026, comisionul de rambursare anticipata este de 1% din suma rambursata anticipat, indiferent daca rambursarea este partiala sau totala.

Exemplu concret: daca soldul ramas este 20.000 RON si clientul ramburseaza anticipat intregul sold, comisionul este 1% x 20.000 RON = 200 RON.

## Exceptii - situatii fara comision

Comisionul de rambursare anticipata NU se aplica in urmatoarele situatii:
- Creditul are dobanda variabila
- Suma rambursata anticipat intr-o perioada de 12 luni este mai mica decat echivalentul a 3 rate lunare

## Dobanda pentru perioada ramasa

Pe langa comision, clientul plateste dobanda acumulata de la ultima rata lunara pana la data efectiva a rambursarii. Aceasta suma este inclusa in oferta de rambursare.

## Comparatie 2025 vs 2026

Atentie: pentru contractele semnate in 2025, comisionul de rambursare anticipata era de 1.5%. Comisionul de 1% se aplica exclusiv contractelor noi din 2026.
"""

files["07-ghid-credit-ipotecar.md"] = """---
title: Ghid general credit ipotecar
product: credit-ipotecar
audience: retail
effective: 2026-01-01
version: 3
---

# Ghid general - Credit ipotecar Libra Bank

Creditul ipotecar Libra Bank este destinat achizitiei, constructiei sau renovarii unei proprietati imobiliare rezidentiale situate in Romania.

## Caracteristici principale

- Suma minima: 50.000 RON
- Suma maxima: 1.500.000 RON
- Durata: intre 5 si 30 de ani
- Moneda: RON sau EUR
- Tipul dobanzii: fixa primii 5 ani, apoi variabila (ROBOR 3M + marja fixa)
- Avans minim: 15% din valoarea proprietatii

## Garantii acceptate

Garantia principala este ipoteca de rang I asupra proprietatii finantate.

## Asigurari obligatorii

- Asigurare de viata a debitorului (cesionata in favoarea bancii)
- Asigurare a proprietatii impotriva riscurilor (PAD + asigurare facultativa)

## Evaluarea proprietatii

Proprietatea trebuie evaluata de un evaluator agreat de Libra Bank. Costul evaluarii este suportat de client.
"""

files["08-eligibilitate-ipotecar.md"] = """---
title: Conditii de eligibilitate credit ipotecar
product: credit-ipotecar
audience: retail
effective: 2026-01-01
version: 2
---

# Conditii de eligibilitate - Credit ipotecar

## Conditii personale

- Varsta minima: 21 ani la data acordarii
- Varsta maxima: 65 ani la data scadentei finale
- Rezidenta in Romania
- Co-debitor acceptat

## Conditii financiare

- Venit net lunar minim: 3.000 RON pentru debitor singular
- Rata lunara totala nu poate depasi 40% din venitul net lunar
- Vechime minima la angajator: 6 luni pentru contract nedeterminat, 12 luni pentru PFA
- Fara restante in Biroul de Credit in ultimii 3 ani

## Conditii privind proprietatea

- Situata in Romania
- Destinatie rezidentiala
- Libera de sarcini
- LTV maxim 85% (avans minim 15%)

## Ce inseamna LTV?

LTV (Loan-to-Value) reprezinta raportul dintre suma creditului si valoarea proprietatii evaluate. La Libra Bank, LTV maxim este 85%.
"""

files["09-calcul-rambursare-ipotecar.md"] = """---
title: Calculul costului rambursarii anticipate - Credit ipotecar
product: credit-ipotecar
audience: retail
effective: 2026-01-01
version: 2
---

# Calculul costului rambursarii anticipate - Credit ipotecar

## Perioada cu dobanda fixa (primii 5 ani)

Comisionul de rambursare anticipata este de 0.5% din suma rambursata anticipat.

Exemplu: sold ramas 200.000 RON, rambursare anticipata 50.000 RON in perioada fixa:
- Comision = 0.5% x 50.000 = 250 RON
- Plus dobanda acumulata de la ultima rata pana la data rambursarii

## Perioada cu dobanda variabila (dupa 5 ani)

Conform legislatiei, comisionul de rambursare anticipata este 0 RON.

Exemplu: sold ramas 150.000 RON, rambursare anticipata totala in perioada variabila:
- Comision = 0 RON
- Se plateste doar dobanda acumulata pana la data rambursarii

## Cum se calculeaza dobanda acumulata?

Dobanda zilnica = (Sold ramas x Dobanda anuala nominala) / 365

Aceasta se inmulteste cu numarul de zile de la ultima rata platita pana la data rambursarii.

## Nota importanta

Pentru suma exacta, clientul solicita o oferta de rambursare conform procedurii standard. Oferta este valabila 5 zile lucratoare.
"""

files["10-dobanzi-fixe-variabile.md"] = """---
title: Comparatie dobanzi fixe vs variabile
product: credite-consum,credit-ipotecar
audience: retail
effective: 2026-01-01
version: 1
---

# Dobanzi fixe vs variabile - Ghid comparativ

## Dobanda fixa

Dobanda fixa ramane constanta pe toata durata stabilita. Rata lunara este predictibila.

Avantaje:
- Predictibilitate: stii exact cat platesti lunar
- Protectie impotriva cresterilor de dobanda
- Planificare financiara mai usoara

Dezavantaje:
- De obicei mai mare decat dobanda variabila initiala
- Nu beneficiezi de scaderile de dobanda
- Comision de rambursare anticipata aplicabil

## Dobanda variabila

Se modifica periodic in functie de ROBOR 3M (pentru RON) sau EURIBOR 3M (pentru EUR) plus o marja fixa.

Avantaje:
- De obicei mai mica la momentul contractarii
- Beneficiezi de scaderile indicelui de referinta
- Fara comision de rambursare anticipata

Dezavantaje:
- Rata lunara poate creste
- Impredictibilitate pe termen lung

## Situatia in 2026

- ROBOR 3M (ianuarie 2026): 5.85% pe an
- Marja fixa Libra Bank pentru ipotecar RON: 2.5%
- Dobanda variabila rezultata: 8.35% pe an
"""

files["11-ghid-card-credit.md"] = """---
title: Ghid card de credit Libra Bank
product: card-credit
audience: retail
effective: 2026-01-01
version: 4
---

# Ghid card de credit - Libra Bank

## Ce este cardul de credit?

Cardul de credit Libra Bank pune la dispozitie o linie de credit revolving pentru cumparaturi, plati online sau retrageri de numerar, pana la limita aprobata.

## Limite disponibile

- Limita minima: 500 RON
- Limita maxima: 30.000 RON

## Perioada de gratie

55 de zile fara dobanda pentru cumparaturi, cu conditia achitarii integrale a soldului la scadenta.

## Dobanda

- Dobanda pentru cumparaturi (dupa perioada de gratie): 24% pe an
- Dobanda pentru retrageri de numerar: 30% pe an (fara perioada de gratie)

## Comisioane principale

- Comision anual card: 50 RON
- Comision retragere numerar: 1% din suma, minim 10 RON
- Comision interogare sold la ATM strain: 2 RON

## Cum activezi cardul?

1. Prima retragere la ATM Libra Bank cu PIN-ul primit separat
2. Prima plata la POS cu PIN
3. Activare prin aplicatia Libra Mobile
"""

files["12-limita-card-credit.md"] = """---
title: Modificarea limitei cardului de credit
product: card-credit
audience: retail
effective: 2026-01-15
version: 3
---

# Modificarea limitei cardului de credit

## Modificare permanenta a limitei

Presupune o noua analiza de bonitate. Clientul depune cerere si documente de venit actualizate. Procesul dureaza 3-5 zile lucratoare.

## Modificare temporara a limitei

Disponibila pentru clientii cu istoric pozitiv de minimum 12 luni. Limita temporara se acorda pentru maximum 90 de zile si poate fi solicitata prin aplicatia Libra Mobile fara documente suplimentare.

## Limita maxima temporara

Incepand cu 15 ianuarie 2026, limita maxima pentru majorarea temporara a fost crescuta de la 5.000 RON la 10.000 RON, pentru clientii cu scor intern de credit peste 750 de puncte.

Atentie: pana la 14 ianuarie 2026, limita maxima temporara era de 5.000 RON. Clientii cu contracte anterioare acestei date beneficiaza automat de noua limita de 10.000 RON fara o noua cerere.

## Reducerea limitei

Clientul poate solicita reducerea limitei oricand, fara costuri, prin aplicatia Libra Mobile sau cerere la ghiseu. Banca poate reduce limita din proprie initiativa cu notificare de 30 de zile.
"""

files["13-procedura-reclamatii.md"] = """---
title: Procedura de depunere si solutionare reclamatii
product: general
audience: retail
effective: 2026-01-01
version: 5
---

# Procedura de depunere si solutionare reclamatii

## Pasul 1: Pregatirea reclamatiei

Clientul aduna:
- Numarul de contract sau de cont afectat
- Data si descrierea evenimentului reclamat
- Sumele implicate
- Documentele justificative

## Pasul 2: Alegerea canalului de depunere

- La ghiseu: orice sucursala Libra Bank, L-V 09:00-17:00
- Online: www.librabank.ro/reclamatii
- Email: reclamatii@librabank.ro
- Posta: Libra Bank SA, Str. Exemplu nr. 1, Bucuresti
- Telefon: 0800 123 456 (linie gratuita, L-V 08:00-20:00)

## Pasul 3: Primirea confirmarii

In maximum 1 zi lucratoare, banca transmite o confirmare cu un numar unic de inregistrare.

## Pasul 4: Analiza reclamatiei

Termenul de solutionare este de maximum 30 de zile calendaristice. Pentru cazuri complexe, termenul poate fi prelungit cu 15 zile, cu notificarea clientului.

## Pasul 5: Comunicarea raspunsului

Raspunsul contine:
- Concluzia analizei
- Masurile luate sau motivele respingerii
- Informatii despre caile de atac disponibile

## Pasul 6: Cai de atac

- SAL-Fin: www.salfin.ro
- Autoritatea Nationala pentru Protectia Consumatorilor (ANPC)
- Banca Nationala a Romaniei
- Instantele judecatoresti competente
"""

files["14-intrebari-frecvente.md"] = """---
title: Intrebari frecvente despre credite
product: credite-consum,credit-ipotecar,card-credit
audience: retail
effective: 2026-01-01
version: 2
---

# Intrebari frecvente - Credite Libra Bank

## Pot sa am doua credite de consum simultan?

Da, Libra Bank permite maximum doua credite de consum active simultan, cu conditia ca rata lunara totala sa nu depaseasca 40% din venitul net lunar.

## Cat dureaza aprobarea unui credit de consum?

- Clienti existenti: decizie in maximum 24 de ore lucratoare
- Clienti noi: maximum 3 zile lucratoare de la depunerea dosarului complet

## Pot rambursa anticipat oricand?

Da, oricand, cu notificare prealabila de 5 zile lucratoare. Comisionul pentru contractele din 2026 este de 1%.

## Ce se intampla daca nu platesc rata la timp?

De la prima zi: penalitati de 0.08% pe zi din rata restanta. Dupa 30 zile: raportare la Biroul de Credit. Dupa 90 zile: banca poate declara scadenta anticipata.

## Pot lua un credit daca sunt pe lista Biroului de Credit?

Depinde de tipul si vechimea informatiei. Restantele stinse de peste 4 ani nu mai influenteaza decizia. Restantele active duc la respingerea automata.

## Ofera Libra Bank credite in valuta?

Creditele ipotecare se acorda in EUR si RON. Creditele de consum se acorda exclusiv in RON.

## Ce este DAE?

DAE (Dobanda Anuala Efectiva) reprezinta costul total al creditului exprimat ca procent anual. Include dobanda nominala, comisionul de acordare si comisionul de administrare.
"""

files["15-produse-indisponibile.md"] = """---
title: Produse nedisponibile la Libra Bank
product: general
audience: retail
effective: 2026-01-01
version: 1
---

# Produse nedisponibile la Libra Bank

## Credite pentru studenti

Libra Bank nu ofera credite studentesti sau produse de finantare dedicate exclusiv studentilor. Studentii cu venituri dovedite pot aplica pentru un credit de consum standard daca indeplinesc conditiile generale.

## Credite pentru firme

Libra Bank deserveste exclusiv persoanele fizice. Nu se acorda credite pentru persoane juridice, PFA-uri sau alte forme profesionale.

## Credite auto dedicate

Libra Bank nu are un produs de credit auto cu garantie pe vehicul. Clientii pot folosi un credit de consum standard pentru achizitia unui autovehicul.

## Factoring si leasing

Libra Bank nu ofera servicii de factoring sau leasing financiar.

## Conturi si credite in criptomonede

Libra Bank nu ofera niciun produs denominat in criptomonede.
"""

files["README.md"] = """# Corpus bancar fictiv - Libra Bank

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
"""

for filename, content in files.items():
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created: {filename}")

print("\nDone! All 16 files created in data/")