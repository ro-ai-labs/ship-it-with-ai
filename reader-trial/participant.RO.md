# Exerciții pentru cititorii Ship It With AI

Parcurge cele trei task-uri în ordine și gândește cu voce tare. Observăm cum
folosești materialul. Spune-i observatorului unde eziți sau ai nevoie de o
explicație. Înainte să începi, spune dacă ai citit cartea sau exemplul Wire.

Folosește materialul indicat la fiecare task. Dă primele răspunsuri fără ajutorul
unui asistent AI. Observatorul va discuta răspunsurile cu tine după exerciții.

## Task 1 Inspectează testul Wire

Folosește doar fragmentul de mai jos până când observatorul îți notează primul răspuns.

Acest serviciu sintetic creează un wire cu o sumă în cenți și o prioritate aleasă.
Cerința este ca fiecare eveniment de audit de creare să înregistreze prioritatea
aleasă. Testul creează un wire urgent și verifică evenimentul de audit rezultat:

```python
service = WireService()
wire = service.create("audit-key", 12500, "URGENT")
self.assertEqual(len(service.audit_events), 1)
self.assertEqual(service.audit_events[0]["type"], "wire.created")
self.assertEqual(service.audit_events[0]["wire_id"], wire.wire_id)
```

Oferă testul suficiente dovezi că cerința e îndeplinită? Explică raționamentul
și orice schimbare ai face. Sintaxa Python exactă e opțională.

Primul tău răspuns:

>

## Task 2 Decide ce muncă poate continua

Alege o schimbare reală propusă pe care o înțelegi. Deschide
[fișa B.4 de pregătire](https://ship-it-with.ai/ro/appendix-b-templates/#template-b4)
sau [versiunea în engleză](https://ship-it-with.ai/appendix-b-templates/#template-b4).

Folosește fișa ca să decizi ce muncă poate continua acum, ce trebuie să aștepte
și ce dovezi ar putea schimba decizia. Explică ce știi și ce nu știi. Indică
dovezile și părțile din fișă pe care le-ai folosit.

Schimbarea propusă:

>

Decizia și dovezile care o susțin:

>

Întrebări nelămurite și următorul pas:

>

## Task 3 Interpretează economia costurilor

Deschide [exemplul calculat din Anexa A](https://ship-it-with.ai/ro/appendix-a-for-managers/#a-worked-example)
sau [versiunea în engleză](https://ship-it-with.ai/appendix-a-for-managers/#a-worked-example).

Scrie un mesaj scurt pentru un engineering manager despre timpul de livrare,
efortul uman și valoarea financiară. Spune ce susțin cifrele din exemplu, ce nu
stabilesc și ce dovezi ai cere în continuare. Arată cifrele sau pasajele pe care
se bazează interpretarea ta.

Mesajul pentru manager:

>

## Discuția de după exerciții

După ce au fost notate toate cele trei răspunsuri, discută unde te-a ajutat
materialul și unde a fost nevoie de explicații. Ce termen sau pasaj ai schimba?
Dacă știai deja un răspuns, spune de unde l-ai învățat.
