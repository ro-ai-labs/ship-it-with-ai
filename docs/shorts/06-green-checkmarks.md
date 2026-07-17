# Short 06 · Capcana bifelor verzi

- Sursă: Capitolul 9, pattern-ul patru (toolkit-ul de review pe PR-uri) · https://ship-it-with.ai/ro/chapter-9-brownfield-patterns/
- Ce predă: agenții verifică stratul mecanic; corectitudinea de business rămâne la oameni
- Durată 28-30s · voce ~84 de cuvinte · 9:16 vertical, subtitrări arse în video

## ABC...D (validarea înainte de producție)

- **Audiență:** echipe care și-au automatizat review-ul cu agenți AI.
- **Beneficiu:** prinzi erorile de business înainte să ajungă în producție.
- **Change (schimbarea):** bifele verzi nu mai înseamnă „corect”; înseamnă „mecanic curat”.
- **Do:** păstrează cititul uman pe fiecare PR - mai scurt, dar obligatoriu.

## Hook (primele 3 secunde)

Rostit: „PR-ul ăsta a trecut de fiecare review făcut de AI. Și tot a facturat greșit clienții, săptămâni întregi.”
Pe ecran: `toate check-urile trecute. clienți facturați greșit.`

## Scenariul (RO)

| Beat | Timp | Voce | Pe ecran |
|------|------|------|----------|
| S | 0-3s | PR-ul ăsta a trecut de fiecare review făcut de AI. Și tot a facturat greșit clienții, săptămâni întregi. | toate check-urile trecute. clienți facturați greșit. |
| T | 3-11s | Poveste reală din manual. Teste verzi. Scanare de securitate curată. Doi revieweri-agent au aprobat. Iar codul aplica o reducere pe tier-ul greșit de clienți. | teste: verzi · securitate: curată · revieweri: aprobat |
| O | 11-18s | Săptămâni în producție. Găsit de un tichet de suport. Nu de o mașină. | găsit de un TICHET DE SUPORT |
| R | 18-25s | Pentru că agenții verifică stratul mecanic. Corectitudinea de business - e asta regula pe care am vrut-o? - o poate verifica doar un om. | mașinile: mecanica · oamenii: sensul |
| Y | 25-30s | Review-ul cu AI îți scurtează cititul. Nu-l face opțional. Manualul, gratuit: ship-it-with.ai/ro | mai scurt. nu opțional. |

## Slide-uri text (varianta text-pe-ecran)

1. (S) Teste verzi. Securitate curată. Doi revieweri AI: aprobat.
2. (T) Reducerea a mers pe tier-ul greșit de clienți. Săptămâni.
3. (O) A găsit-o un tichet de suport. Nu o mașină.
4. (R) Mașinile verifică mecanica. Sensul rămâne la oameni.
5. (R) Review-ul uman: mai scurt, dar niciodată opțional.
6. (Y) Cine verifică sensul la voi? ship-it-with.ai/ro

## Note vizuale

Deschide pe un perete de bife verzi - cea mai de încredere imagine din software - apoi ștampilează „TIER GREȘIT” cu roșu peste el la secunda 11. Contrastul dintre UI-ul verde și realitatea roșie duce tot clipul. End card cu URL-ul.

## Descriere (RO)

Teste verzi, securitate curată, doi revieweri AI au aprobat - și reducerea tot a mers săptămâni întregi pe tier-ul greșit de clienți. Mașinile verifică mecanica. Oamenii răspund de sens. Pattern-ul de review care supraviețuiește e în manualul gratuit: ship-it-with.ai/ro
`#ai #codereview #aiagents #programare #inginerie`

## De ce prinde

Un eșec concret cu bani la mijloc, povestit împotriva celui mai de încredere simbol din cultura dev: bifa verde. „Mașinile: mecanica, oamenii: sensul” e un framework în patru cuvinte pe care oamenii îl vor repeta în standup-uri.

## Versiunea EN (pentru canalul global)

| Beat | Time | Voiceover | On-screen |
|------|------|-----------|-----------|
| S | 0-3s | This pull request passed every AI review. It still overcharged customers for weeks. | every check passed. customers overcharged. |
| T | 3-11s | True story from the manual. Tests green. Security scan clean. Two agent reviewers approved. And the code applied a discount rule to the wrong customer tier. | tests: green · security: clean · reviewers: approved |
| O | 11-18s | Production for weeks. Found by a support ticket. Not by a machine. | found by a SUPPORT TICKET |
| R | 18-25s | Because agents check the mechanical layer. Business correctness - is this the rule we actually meant - only a human can check that. | machines: mechanics · humans: meaning |
| Y | 25-30s | AI review makes your read shorter. Not optional. Free manual: ship-it-with.ai | shorter. not optional. |

Text slides (EN):
1. (S) Tests green. Security clean. Two AI reviewers: approved.
2. (T) The discount went to the wrong customer tier. For weeks.
3. (O) A support ticket found it. Not a machine.
4. (R) Machines check mechanics. Meaning stays with humans.
5. (R) The human read: shorter, never optional.
6. (Y) Who checks meaning on your team? ship-it-with.ai

Descriere (EN): Tests green, security clean, two AI reviewers approved - and the discount still went to the wrong customer tier for weeks. Machines check mechanics. Humans own meaning. Free manual: ship-it-with.ai
`#ai #codereview #aiagents #softwareengineering #devtok`
