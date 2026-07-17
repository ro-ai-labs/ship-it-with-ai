# Short 07 · Semaforul

- Sursă: Capitolul 8, kill signals și semaforul · https://ship-it-with.ai/ro/chapter-8-readiness-kill-signals/
- Ce predă: numeri kill signals; 0-1 verde, 2-3 galben, 4+ roșu; semnalul șase atârnă cel mai greu
- Durată 28-30s · voce ~84 de cuvinte · 9:16 vertical, subtitrări arse în video

## ABC...D (validarea înainte de producție)

- **Audiență:** tech leads și manageri care decid unde intră agentul.
- **Beneficiu:** o regulă de decizie clară în locul unui sentiment vag.
- **Change (schimbarea):** de la „am o presimțire proastă” la un scor pe care îl poate apăra oricine.
- **Do:** punctează repo-ul cu cele opt semnale, în cincisprezece minute.

## Hook (primele 2 secunde)

Rostit: „Codebase-ul tău e verde, galben sau roșu pentru AI. Majoritatea echipelor nu verifică niciodată.”
Pe ecran: `verde · galben · roșu`

## Scenariul (RO)

| Beat | Timp | Voce | Pe ecran |
|------|------|------|----------|
| S | 0-2s | Codebase-ul tău e verde, galben sau roșu pentru AI. Majoritatea echipelor nu verifică niciodată. | verde · galben · roșu |
| T | 2-11s | Numără kill signals: fără teste, fără documentație, cuplare strânsă, reguli de business împrăștiate... opt în total. | fără teste · fără docs · cuplare strânsă · ... |
| R | 11-19s | Zero sau unu: verde. Lucru condus de agent, la viteză normală. Două sau trei: galben. Condus de om, cu sprijinul agentului. Patru sau mai multe: roșu. Stop. Repari întâi codebase-ul. | 0-1 VERDE · 2-3 GALBEN · 4+ ROȘU |
| O | 19-26s | Și un semnal atârnă mai greu decât toate: dacă echipa nu poate evalua output-ul agentului, ești pe roșu. Indiferent de scor. | nu puteți evalua output-ul? ROȘU. |
| Y | 26-30s | Punctează-ți repo-ul în cincisprezece minute. Manualul, gratuit: ship-it-with.ai/ro | punctează-l pe al tău: ship-it-with.ai/ro |

## Slide-uri text (varianta text-pe-ecran)

1. (S) Codebase-ul tău are o culoare pentru AI.
2. (T) 8 kill signals: fără teste, fără docs, cuplare strânsă...
3. (R) 0-1 = VERDE · 2-3 = GALBEN · 4+ = ROȘU
4. (O) Nu puteți evalua output-ul? ROȘU. Indiferent de scor.
5. (R) ROȘU nu înseamnă niciodată. Înseamnă repari întâi.
6. (Y) Punctează-ți repo-ul azi: ship-it-with.ai/ro

## Note vizuale

Grafică literală de semafor care se completează pe măsură ce grila aterizează la 11-19s - figura semaforului de pe site merge ca b-roll. Beat-ul de la secunda 19 primește un snap dur pe roșu. Cardul cu grila (0-1 / 2-3 / 4+) e declanșatorul de save; ține-l pe ecran.

## Descriere (RO)

Nu orice codebase e pregătit pentru agenți AI, iar prefăcătoria e felul în care eșuează proiectele de AI. Numără cele opt kill signals: 0-1 verde, 2-3 galben, 4+ roșu - iar dacă echipa nu poate evalua output-ul, e roșu indiferent de scor. Grila, în manualul gratuit: ship-it-with.ai/ro
`#ai #aiagents #inginerie #techlead #programare`

## De ce prinde

Le dă managerilor și lead-ilor o regulă de decizie pe care o pot rula azi într-un meeting. Framework-urile cu numere tari (0-1, 2-3, 4+) ajung screenshot și circulă în sus - ăsta e short-ul cu cele mai mari șanse să ajungă în canalele de Slack ale conducerii.

## Versiunea EN (pentru canalul global)

| Beat | Time | Voiceover | On-screen |
|------|------|-----------|-----------|
| S | 0-2s | Your codebase is green, yellow, or red for AI. Most teams never check. | green · yellow · red |
| T | 2-11s | Count the kill signals: no tests, no docs, tight coupling, scattered business rules... eight in total. | no tests · no docs · tight coupling · ... |
| R | 11-19s | Zero or one: green. Agent-led work at normal speed. Two or three: yellow. Human-led, agent supporting. Four or more: red. Stop. Fix the codebase first. | 0-1 GREEN · 2-3 YELLOW · 4+ RED |
| O | 19-26s | And one signal outweighs everything: if your team can't evaluate the agent's output, you're red. No matter the score. | can't evaluate the output? RED. |
| Y | 26-30s | Score your repo in fifteen minutes. Free manual: ship-it-with.ai | score yours: ship-it-with.ai |

Text slides (EN):
1. (S) Your codebase has a color for AI.
2. (T) 8 kill signals: no tests, no docs, tight coupling...
3. (R) 0-1 = GREEN · 2-3 = YELLOW · 4+ = RED
4. (O) Can't evaluate the output? RED. No matter the score.
5. (R) RED doesn't mean never. It means fix first.
6. (Y) Score your repo today: ship-it-with.ai

Descriere (EN): Not every codebase is ready for AI agents. Count the eight kill signals: 0-1 green, 2-3 yellow, 4+ red - and if the team can't evaluate the output, it's red regardless. Rubric in the free manual: ship-it-with.ai
`#ai #aiagents #softwareengineering #engineeringmanager #techlead`
