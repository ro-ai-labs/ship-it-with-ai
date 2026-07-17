# Short 03 · Fluența nu e corectitudine

- Sursă: Capitolul 5, „Cum faci review pe un diff scris de agent?” · https://ship-it-with.ai/ro/chapter-5-six-phase-loop/
- Ce predă: bug-urile de agent eșuează la intenție, nu la execuție; inversează ordinea de citire
- Durată 28-30s · voce ~88 de cuvinte · 9:16 vertical, subtitrări arse în video

## ABC...D (validarea înainte de producție)

- **Audiență:** developeri care fac review pe cod scris de AI.
- **Beneficiu:** prinzi bug-urile pe care cititul de fluență nu le poate prinde.
- **Change (schimbarea):** de la „citesc linie cu linie” la „citesc întâi intenția, apoi liniile”.
- **Do:** aplică ordinea de citire inversată la următorul diff de agent.

## Hook (primele 2 secunde)

Rostit: „Bug-urile de AI nu arată ca niște bug-uri. Exact asta le face periculoase.”
Pe ecran: `bug-urile de AI nu arată ca bug-uri`

## Scenariul (RO)

| Beat | Timp | Voce | Pe ecran |
|------|------|------|----------|
| S | 0-2s | Bug-urile de AI nu arată ca niște bug-uri. Exact asta le face periculoase. | bug-urile de AI nu arată ca bug-uri |
| T | 2-10s | Un bug de om e o typo pe care o vânezi linie cu linie. Un diff de agent compilează, trece de lint și se citește ca un cod pe care l-ai face merge fără comentarii. | compilează · trece de lint · se citește curat |
| T | 10-15s | Eșuează la intenție: o regulă de business plauzibilă și greșită. | plauzibilă. și greșită. |
| O | 15-21s | Un bug de agent arată ca acel cod pe care un inginer bun l-ar scrie pentru un task ușor diferit. | cod bun... pentru un task ușor diferit |
| R | 21-27s | Așa că inversează review-ul: întâi forma diff-ului față de plan, apoi testele, apoi grep pe fiecare nume nou. | 1 forma vs plan · 2 testele întâi · 3 grep pe numele noi |
| Y | 27-30s | Fluența nu e corectitudine. Manualul, gratuit: ship-it-with.ai/ro | FLUENȚA NU E CORECTITUDINE |

## Slide-uri text (varianta text-pe-ecran)

1. (S) Faci review pe un diff scris de AI.
2. (T) Compilează. Trece de lint. Se citește curat.
3. (T) Și tot e greșit: regula de business e alta.
4. (O) Un bug de agent arată ca un cod bun pentru un task ușor diferit.
5. (R) Inversează cititul: forma vs plan, apoi testele, apoi grep pe numele noi.
6. (R) Abia apoi linie cu linie.
7. (Y) Fluența nu e corectitudine. ship-it-with.ai/ro

## Note vizuale

Deschide pe un diff verde superb care derulează - cod „perfect” vizual. La secunda 10, îngheață cadrul și încercuiește cu roșu o singură linie: regula de business greșită. Lista în 3 pași de la secunda 21 apare ca punch-uri de text stivuite. Ține aforismul de final pe tot ecranul pe ultimul beat; e screenshot-ul pe care îl vor distribui oamenii.

## Descriere (RO)

Un bug de om e o typo. Un bug de agent e cod perfect pentru un task ușor diferit: compilează, trece de lint și facturează greșit clienții. Ordinea de citire în 5 pași, în manualul gratuit: ship-it-with.ai/ro
`#ai #codereview #aiagents #programare #inginerie`

## De ce prinde

Insight de meserie, contraintuitiv, țintit direct la developerii activi. Aforismul e citabil, iar checklist-ul în 3 beat-uri dă utilitate imediată, ceea ce aduce save-uri și share-uri - cele două semnale care contează cel mai mult în distribuția de shorts.

## Versiunea EN (pentru canalul global)

| Beat | Time | Voiceover | On-screen |
|------|------|-----------|-----------|
| S | 0-2s | AI bugs don't look like bugs. That's what makes them dangerous. | AI bugs don't look like bugs |
| T | 2-10s | A human bug is a typo you hunt line by line. An AI diff compiles, passes lint, and reads like code you'd merge without comment. | compiles · passes lint · reads clean |
| T | 10-15s | It fails at intent: a business rule that's plausible and wrong. | plausible. and wrong. |
| O | 15-21s | An agent bug looks like the code a good engineer would write for a slightly different task. | good code... for a slightly different task |
| R | 21-27s | So flip the review: shape against the plan first, tests before code, grep every new name. | 1 shape vs plan · 2 tests first · 3 grep new names |
| Y | 27-30s | Fluency is not correctness. Free manual: ship-it-with.ai | FLUENCY IS NOT CORRECTNESS |

Text slides (EN):
1. (S) You're reviewing a diff written by AI.
2. (T) It compiles. Passes lint. Reads clean.
3. (T) And it's still wrong: the business rule is different.
4. (O) An agent bug looks like good code for a slightly different task.
5. (R) Flip the read: shape vs plan, then tests, then grep the new names.
6. (R) Only then, line by line.
7. (Y) Fluency is not correctness. ship-it-with.ai

Descriere (EN): A human bug is a typo. An agent bug is perfect code for a slightly different task - it compiles, passes lint, and charges the wrong customers. The 5-step read order is in the free manual: ship-it-with.ai
`#ai #codereview #aiagents #softwareengineering #programming`
