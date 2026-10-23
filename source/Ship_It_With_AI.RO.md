# Ship It With AI

### Un manual practic pentru livrarea de software cu agenți AI

**Mihai Cvasnievschi**

---

> Agenții scriu codul.
> Tu înțelegi problema.
> Asta e competența pe care n-o automatizează nimeni.

---

## Cuprins

**Prolog** - Nouă secunde

**Partea I - Arhitectura**
1. Ce este un agent
2. Guardrails în cinci straturi

**Partea a II-a - Metoda**
3. Bottleneck-ul s-a mutat
4. Bucla în șase faze
5. Review și Verify
6. [AGENTS.md](https://agents.md/) și contextul
7. Întâi harta: review-ul de arhitectură

**Partea a III-a - Realitatea**
8. Are voie agentul să atingă codul ăsta?
9. Lansarea în echipă

**Încheiere** - Un mod de a gândi care supraviețuiește tool-urilor

**Mulțumiri**

**Anexa A** - Pentru manageri
**Anexa B** - Template-uri
**Anexa C** - Surse și lecturi suplimentare
**Anexa D** - Deep dives

---

# Prolog

## Nouă secunde {#nine-seconds}

Pe 24 aprilie 2026, o mică firmă de SaaS pe nume PocketOS, un produs de management pentru închirieri auto, și-a pierdut baza de date de producție din cauza unui agent AI care a hotărât să rezolve de unul singur o problemă de credențiale.

Un developer lucra pe codebase-ul PocketOS cu un coding agent (Cursor, pe Claude Opus 4.6). În timpul unui task de rutină, agentul a dat peste o nepotrivire de credențiale și, în loc să se oprească și să întrebe, a decis să repare singur problema. A găsit un API token care se autentifica la Railway, platforma de infrastructură folosită de PocketOS, și a invocat comanda Volume Delete din Railway. Apelul distructiv a durat nouă secunde.

Pierderea a fost totală: toate rezervările clienților, înregistrările de plăți și inventarul de vehicule. Railway ține backup-urile pe același volum cu datele primare, așa că au dispărut odată cu ele, iar cel mai recent snapshot recuperabil avea trei luni vechime. Recuperarea a fost până la urmă posibilă, dar nu pe ruta de backup la care se aștepta echipa; relatările publice diferă în privința cronologiei.

După aceea, agentul și-a recunoscut vina în scris: „I violated every principle I was given. I guessed instead of verifying. I ran a destructive action without being asked. I didn't understand what I was doing before doing it.”

*Folosesc incidentul pentru pattern-ul de guvernanță, nu ca pe o reconstituire exactă, de tip forensic. Sursele și detaliile contestate sunt în Anexa C.*

---

**Ce ar fi oprit incidentul.** Nu magie: controale de engineering obișnuite, aplicate unui tip nou de lucrător. Limitezi credențialele, limitezi tool-urile, faci review la muncă înainte să ajungă live, înregistrezi ce s-a întâmplat - aceleași controale pe care un inginer cu experiență le-ar aplica oricărui coleg junior nou care primește drept de push în producție. Niciunul nu e exotic și niciunul nu era acolo. Capitolul 2 parcurge incidentul pe cele cinci straturi, oricare dintre ele putând rupe lanțul.

**De ce se tot întâmplă asta.** Un senior engineer îmi spune că a încercat Claude Code, sau Codex, sau alt coding agent, și că „n-a mers”: codul arăta corect, dar nu era, sau s-a stricat ceva și nimeni n-a observat timp de două săptămâni. Cele mai multe adopții ratate nu se explică doar prin slăbiciunea modelului. Sunt eșecuri ale structurii din jurul agentului: lipsește contextul, lipsesc constrângerile, lipsește procesul, lipsește disciplina de review.

Un ciocan îl iei din raft și îl folosești. Un inginer junior nu-l iei din raft să-l folosești: trebuie să-i faci onboarding, să-i dai context, să pui la punct review-ul, să construiești încredere în timp. Agenții sunt mai aproape de inginerul junior decât de ciocan - o poziție de lucru, nu o afirmație despre natura agentului: agentul e software.

**Teza.** Livrarea de software cu agenți nu e în primul rând o problemă de tooling. E o problemă de control. Controlează contextul, acțiunile, verificarea și suprafața de adopție, și agentul devine util; dacă nu le controlezi, devine zgomot scump sau risc operațional. Cele trei părți ale manualului sunt trei controale: Arhitectura e controlul capabilității (ce poate ști și ce poate face agentul), Metoda e controlul workflow-ului (cum se formulează, se execută și se verifică munca), Realitatea e controlul adopției (unde aplici metoda și unde n-ar trebui s-o aplici).

Prin „agentic” înțeleg un sistem care primește un obiectiv, decide ce acțiuni trebuie executate și le execută, cu o anumită doză de autonomie. Nu mai scrii tu fiecare apăsare de tastă; superviezi munca. Agenții nu oferă tastat mai rapid, ci posibilitatea de a delega muncă bine formulată. Să înțelegi problema, ideea de pe copertă, e partea care rămâne a ta.

Nu o să-ți spun ce agent să alegi. Agentul pe care îl alegi azi va fi deprecated, rebranduit sau înghițit de un produs mai mare într-un ciclu de procurement. Felul în care gândești munca supraviețuiește înlocuirii.

---

**De unde vorbesc.** Scriu software profesionist din 2000 și construiesc sisteme AI de mai bine de un deceniu. Am folosit fiecare generație de asistent de coding, de la inteligența timpurie din IDE-uri la Copilot și până la coding agents de azi, iar în ultimele optsprezece luni am urmărit echipe de producție care adoptă workflow-uri cu agenți - unele bine, altele prost. Manualul ăsta e ce a supraviețuit utilizării repetate în echipe reale. [Contextul complet: Despre autor.](#about-the-author)

**Unde poate greși.**

- **Tool-urile se vor schimba.** Produsele pe care le numesc, formatele de hook-uri, sintaxa regulilor de permisiuni și prețurile vor îmbătrâni. Componentele principale și modelul în cinci straturi sunt ce mă aștept să reziste.
- **Mediile reglementate sunt altfel.** Presupun că poți instala hook-uri, configura AGENTS.md, pune la punct sandbox-uri și rula subagenți. Acolo unde asta cere un review board sau luni de procurement, manualul descrie destinația, nu drumul.
- **Procesul are un cost.** Pornește cu agentul nativ și controalele existente ale echipei. Adaugă planificare, skill-uri și revieweri unde task-ul le cere; cele șase faze din Capitolul 4 numesc funcții, nu șase documente sau opriri obligatorii pentru aprobare.

Recomandările despre workflow, skill-uri, delegare, review și fișierele de instrucțiuni au fost revizuite pe 23 octombrie 2026. Celelalte afirmații despre produse și cercetare își păstrează datele și limitele din Anexa C; această revizie nu reprezintă un nou fact-check al întregului manual. Actualizările care contează sunt în [changelog](/changelog/).

**Cum se citește.** Manualul e scris pentru senior engineer - staff, principal sau tech lead - care va pune practica asta pe picioare într-o echipă reală și o va apăra în sus; oricine livrează software cu AI îl poate urmări. Prima dată citește-l în ordine. Manageri și directori: Capitolele 2, 8 și 9 și Anexa A; dacă facilitezi adopția: Capitolele 7-9 și Anexa B. Studiile și cifrele din spatele fiecărui capitol sunt în Anexa D; capitolele păstrează doar ce schimbă o decizie.

---

# Partea I - Arhitectura

> *Controlul capabilității: ce poate agentul să știe și ce poate să facă.*

---

## Capitolul 1
## Ce este un agent

*La finalul capitolului poți numi cele nouă părți ale oricărui coding agent, poți găsi-o pe cea care controlează un anumit risc și poți compara doi agenți după ceea ce au înăuntru.*

**TL;DR**

- Un coding agent e un model într-un harness, construit din nouă componente principale pe care le poți inspecta.
- Anatomia e aceeași la toți vendorii. Implementările diferă, iar diferențele, sandbox-ul înainte de toate, sunt alegeri de guvernanță.
- Evaluează modelul și harness-ul împreună, pe task-urile tale. La orice agent nou, pune câte o întrebare pe componentă principală.

---

### Ce este o componentă principală a unui coding agent? {#what-is-a-primitive}

**Un agent înseamnă un model plus un harness, iar harness-ul e un set restrâns de părți care se repetă.**

Deschide codul sursă al aproape oricărui coding agent de nivel de producție și vei vedea aceeași arhitectură: un set de componente principale împachetate într-un harness. Un mecanism e componentă principală atunci când fiecare coding agent major îl livrează ca pachet distinct și configurabil. Fiecare card de mai jos se încheie cu întrebarea pe care o pui unui agent nou.

```
                          THE HARNESS
   +-------------------------------------------------------+
   |                                                       |
   |     context window                                    |
   |     tools                                             |
   |     permissions / sandbox                             |
   |        (decision layer | OS enforcement)              |
   |     skills                                            |
   |     plugins                                           |
   |     MCP                                               |
   |     memory  (manually defined | auto-memory system)   |
   |     effort  (reasoning level | retained reasoning)    |
   |                                                       |
   |     -----------------------------------------         |
   |                                                       |
   |     subagents  (the agent, recursively)               |
   |                                                       |
   +-------------------------------------------------------+
        bucla agentului le leagă pe toate;
        subagenții pornesc instanțe-copil constrânse
        ale agentului însuși
```

*Figura: Componentele principale și harness-ul care le rulează. Permisiuni / Sandbox ocupă poziția 3 ca componentă principală ale cărei două jumătăți - stratul de decizie de la nivelul agentului și enforcement-ul la nivel de OS - converg ca prezență, dar diverg ca postură de la un vendor la altul. A doua jumătate a lui Memory - stratul scris de agent - a convers la agenții majori în primele luni ale lui 2026. Effort e slotul cel mai nou: butonul de raționament, plus dacă raționamentul pe care îl cumpără e păstrat de la o tură la alta. Subagenții stau sub linie pentru că sunt componenta principală recursivă: fiecare subagent e, la rândul lui, o instanță a celorlalte.*

---

### Context window

**Ce este: tot ce știe agentul chiar acum, într-un număr limitat de tokeni.**

Conține system prompt-ul, conversația, rezultatele tool-urilor și fișierele citite - nu restul codebase-ului tău și nici ticketele. Cele mai multe decizii „evident greșite” se reduc la context lipsă: nu i-a spus nimeni agentului de noua bibliotecă de autentificare. Dimensiunile de fereastră din reclame depășesc ce folosește un model cu adevărat bine. Capitolul 6 tratează lucrul în limitele ferestrei.

*Întreabă: Cât de mare e fereastra și cum o gestionează agentul sub presiune?*

---

### Tool-uri

**Ce este: acțiunile pe care le poate face agentul - să citească, să scrie și să editeze fișiere, să ruleze comenzi de shell, să caute în codebase.**

Fiecare tool call e un punct de decizie, un punct de audit și un punct de control: înregistrează apelurile ca să poți reconstitui ce s-a întâmplat, interceptează-le ca să guvernezi. „Nu șterge fișiere aici” funcționează oprind tool call-ul de Bash înainte să ruleze `rm`. Ține setul de tool-uri mereu vizibile mic, pentru că fiecare tool costă context înainte de primul tău cuvânt.

*Întreabă: Ce tool-uri are și cum sunt constrânse?*

---

### Permisiuni / Sandbox {#permissions-sandbox}

**Ce este: două controale livrate ca pereche - regulile agentului însuși și enforcement-ul sistemului de operare.** E componenta principală care i-a lipsit lui PocketOS (vezi Prologul).

Stratul de decizie al agentului verifică cererile către tool-urile pe care le acoperă față de regulile allow / ask / deny. Unele moduri adaugă un clasificator bazat pe model pentru acțiunile eligibile, după aplicarea regulilor explicite. Injecția poate induce în eroare clasificatorul sau poate exploata acțiuni permise și lipsuri de acoperire; nu poate convinge pur și simplu o regulă de deny aplicată corect să dispară. Stratul de OS refuză syscall-urile interzise ale proceselor pe care le izolează efectiv, indiferent de raționamentul agentului. Verifică ce tool-uri și subprocese sunt în interiorul acestei limite. Niciuna dintre jumătăți nu e suficientă singură.

*Întreabă: Ce model de permisiuni livrează și ce sandbox de OS are by default?*

---

### Skill-uri

**Ce este: instrucțiuni împachetate, pe care agentul le încarcă doar când un task are nevoie de ele.**

Un skill e o bucată de markdown - felul în care scrie echipa un serviciu de Spring Boot, de exemplu - încărcată când task-ul are nevoie de ea. Descrierile pot ocupa context înainte de invocare; instrucțiunile complete intră când sunt folosite și pot rămâne în sesiune. Ține trigger-ele specifice. Cunoștințele specializate pot ajuta; o procedură generală pe care agentul o urmează deja poate adăuga cost fără să îmbunătățească rezultatul.

*Întreabă: Skill-urile se încarcă la detecție sau sunt always-loaded?*

---

### Plugin-uri

**Ce este: un pachet de skill-uri, tool-uri, hook-uri și comenzi, instalabil printr-o singură comandă.**

Plugin-ul e unitatea de distribuție: workflow-ul de review de PR-uri al unei echipe devine pentru altă echipă o instalare cu o singură comandă. Pornește cu agentul nativ; adaugă un plugin pentru o capabilitate necesară sau pentru o îmbunătățire măsurată. Marketplace-ul e și o suprafață de supply chain, npm-ul programării cu agenți. Anexa B.10 verifică atât încrederea, cât și utilitatea.

*Întreabă: Există un marketplace de plugin-uri și cum verifici ce conține?*

---

### Ce este MCP? {#what-is-mcp}

**Ce este: Model Context Protocol, o specificație pentru felul în care agenții vorbesc cu sistemele externe** - Jira, Postgres, GitHub, data warehouse-ul tău.

Același server MCP funcționează cu orice agent care îl suportă, deci integrarea supraviețuiește următorului agent pe care îl adopți: cel mai apropiat lucru pe care îl are ecosistemul de un standard deschis.

*Întreabă: Vorbește MCP și cât de bună e integrarea?*

---

### Memory {#memory}

**Ce este: ce se păstrează de la o sesiune la alta, în două jumătăți.**

Prima o scrie echipa: AGENTS.md, citit la începutul sesiunii de cei mai mulți agenți. Și Claude Code îl poate citi nativ acum, cu condițiile de versiune și precedență explicate în Capitolul 6. A doua o scrie agentul pentru sine: comenzi de build pe care le-a dedus, concluzii de debugging, preferințe inferate.

*Întreabă: Citește un fișier de memorie partajat de echipă la începutul sesiunii și își ține și o memorie proprie?*

---

### Effort {#effort}

**Ce este: cât de mult gândește modelul înainte să acționeze - cea mai nouă componentă principală, care își câștigă locul prin levier.**

Toți agenții majori îl expun ca setare, sub nume diferite. Mișcă și costul, și calitatea, în ambele direcții: prea jos, și agentul sare peste research-ul de care avea nevoie task-ul; prea sus, și plătești raționament pe care task-ul nu l-a cerut niciodată. Numele nu se transferă între modele, așa că orice migrare de model începe cu un sweep de effort (Anexa B.9). Setează-l per fază, nu per sesiune: fazele de Research și de Plan merită effort mare, un task mecanic din faza de Execute, de regulă, nu.

*Întreabă: Ce niveluri de effort expune și supraviețuiește raționamentul de la o tură la alta?*

---

### Subagenți

**Ce este: instanțe-copil constrânse ale agentului însuși.**

Orchestratorul îi dă subagentului un task bine delimitat, cu tool-uri limitate la scopul lui, și primește un rezultat. Un context proaspăt izolează munca; un fork poate prelua istoricul agentului principal. Fiecare worker adaugă consum, timp de pornire și coordonare, influențate parțial de cache. Deleagă munca amplă și independentă când beneficiul estimat justifică aceste costuri; păstrează în agentul principal editările rapide și pașii strâns legați. Capitolele 4, 5 și 7 arată unde poate ajuta delegarea.

*Întreabă: Cum expune subagenții - e dispatch-ul în paralel o operație de primă clasă?*

---

### Harness-ul

**Modelul determină plafonul; harness-ul determină dacă îl atingi.**

Harness-ul e runtime-ul din jurul modelului: îți formatează cererea, gestionează fereastra, trimite spre execuție tool call-urile, întoarce rezultatele modelului și decide când s-a terminat treaba. Bucla în sine e banală, cam cât un handler de request HTTP; middleware-ul din jurul ei e ceea ce cumperi de fapt. Compară harness-urile după constrângerile tale: licență, ecosistem de plugin-uri, enforcement de sandbox și audit. Evaluează și modelul pe task-urile relevante; capabilitatea lui poate schimba nevoia de planificare, delegare sau review suplimentar.

---

### Anatomia e invariantă

**Anatomia e aceeași în fiecare agent; implementarea, nu.**

> **Dovada: un prompt, doi agenți.** În timp ce pregăteam manualul, am pus Claude Code să citească codul sursă a doi alți coding agents, în două panouri de terminal: Codex CLI (Rust, întreținut de OpenAI) și opencode (TypeScript, o echipă independentă). Amândoi sunt open source și nu au nicio linie de cod în comun. Același prompt în fiecare: mapează bucla agentului, tool-urile, gate-urile de permisiuni, sandbox-ul și modelul de plugin-uri, citând fișiere și numere de linie.
>
> Cam patru minute mai târziu, fără nicio corecție umană, amândoi au întors aceeași formă: o buclă de agent, un registru de tool-uri, un gate de permisiuni, un sandbox, un model de plugin-uri, suport MCP, o cale de dispatch pentru subagenți. Alte limbaje, alte fișiere, alte nume. Cea mai clară divergență a fost sandbox-ul: Codex implementează izolare reală la nivel de OS, deci kernelul însuși refuză ceea ce agentul nu e autorizat să facă; opencode implementează o îngrădire soft, validare de căi și prompt-uri de permisiune, fără nicio graniță impusă de kernel.
>
> *Limitări: experimentul arată că componentele principale există, nu că sunt la fel de bine implementate, și nu sunt.*

---

### Postura sandbox-ului e o alegere de guvernanță

**Alegerile unui vendor în privința componentelor principale sunt alegeri de guvernanță.**

Apelurile de kernel sunt în sursă, așa că poți vedea dacă un sandbox e real sau e teatru. Codex CLI impune un sandbox de OS by default pe Linux și macOS; Claude Code livrează unul opt-in, iar majoritatea instalărilor îl sar; opencode livrează doar jumătatea de decizie. Default-urile depind de versiune, deci verifică-le pe ale tale.

Un vendor care livrează un sandbox real se așteaptă ca instrucțiuni ostile să ajungă - prin dependențe, prin fișiere compromise, prin injection - și construiește apărare în adâncime (defense in depth). Unul care livrează îngrădire soft se așteaptă la un mediu de încredere. Ambele posturi pot fi apărate; tu alegi, iar Capitolul 2 transformă alegerea în cinci straturi.

---

### Când se strică

- **O regulă pe care o consultă agentul nu e un zid.** Injecția poate induce în eroare judecata modelului și poate exploata acțiuni permise sau lipsuri de acoperire. Regulile de deny aplicate efectiv și izolarea la nivel de OS protejează operațiunile pe care le acoperă (Capitolul 2).
- **Un sandbox din documentație nu e un sandbox în kernel.** Confirmă că stratul de OS e pornit.
- **Un plugin e cod pe care nu l-ai scris tu.** O instalare neverificată e un risc de supply chain, iar un hook care rulează în afara sandbox-ului nu e mărginit de nimic.

---

### De făcut luni

- [ ] Pune agentului pe care îl folosești zilnic câte o întrebare pentru fiecare componentă principală (rândurile cu „Întreabă”), notează răspunsurile și evaluează fiecare componentă drept basic, intermediate sau advanced.
- [ ] Verifică dacă sandbox-ul lui de OS e pornit și notează nivelul de effort.
- [ ] Deschide repository-ul unui agent open source și găsește fișierul care implementează bucla agentului (douăzeci de minute: o să-i prinzi forma, nu fiecare linie). Apoi localizează unde stă fiecare dintre cele nouă componente principale.

---

### Mai departe

- **Template-uri:** [Anexa B.10](#template-b10), verificarea plugin-urilor; [B.11](#template-b11), parcurgerea sursei a doi agenți; [B.9](#template-b9), sweep-ul de effort.
- **Deep dive:** [Anexa D, Capitolul 1](#deep-dive-chapter-1) - cifre despre context window și numărul de tool-uri, decodarea strictă pentru schemele de tool-uri custom, posturile și cronologiile de sandbox ale vendorilor, dovezile despre effort, orchestrarea scriptată a subagenților.
- **Surse:** Anexa C.

---

## Capitolul 2
## Guardrails în cinci straturi

*La finalul capitolului poți puncta un repository pe cele cinci straturi de control și poți numi fix-ul care îi închide cea mai mare lacună.*

**TL;DR**

- Un prompt e o cerere, nu un control. Acțiunile distructive au nevoie de straturi pe care agentul nu le poate ocoli cu vorba: permisiuni, sandbox, secrete, hook-uri și telemetrie.
- Principiul privilegiului minim e coloana vertebrală, iar redundanța e controlul. Sandbox-ul limitează procesele pe care le acoperă efectiv; celelalte tool-uri au nevoie de propriile controale, iar fiecare strat poate avea bug-uri.
- Ține credențialele de producție în afara sesiunii și trece pull request-urile agentului prin aceleași gate-uri ca pe ale tuturor celorlalți.

---

### Care sunt cele cinci straturi?

**Un prompt e o cerere. Un control e ceva ce agentul nu poate ocoli cu vorba.**

PocketOS (Prologul) avea o instrucțiune în limbaj natural, care e mai slabă decât stratul unu. Din incident se citează trei lecții, și toate trei sunt greșite:

- „Agentul și-a ignorat instrucțiunile.” Da. Asta fac agenții uneori; un prompt nu e niciodată un control dur pentru o acțiune distructivă.
- „Agenții AI sunt nesiguri.” La fel de nesigur e orice tool îndreptat spre producție fără controale.
- „N-ar trebui să folosim AI pentru operațiuni pe baze de date.” Asta înseamnă să arunci productivitate reală, când straturile pot delimita riscul.

Sub toate cinci stă privilegiul minim: la fiecare nivel - agentul, procesul lui, credențialele lui, rețeaua lui - acorzi minimul care permite muncii să se întâmple.

```
+----------------------------------------------------+
|  Stratul 5: Telemetrie (detectiv)                  |
+----------------------------------------------------+
|  Stratul 4: Hook-uri de securitate (per acțiune)   |
+----------------------------------------------------+
|  Stratul 3: Secrete (protecție structurală)        |
+----------------------------------------------------+
|  Stratul 2: Sandbox (izolare la nivel de OS)       |
+----------------------------------------------------+
|  Stratul 1: Permisiuni (allow / ask / deny)        |
+----------------------------------------------------+

       Privilegiul minim e coloana vertebrală.
       Fiecare strat prinde ce scapă celorlalte.
```

*Figura: Cele cinci straturi de guvernanță, suprapuse ca apărare în adâncime.*

| Strat | Blochează | Cedează când | Ar fi oprit PocketOS? |
|---|---|---|---|
| 1. Permisiuni | Acțiunile acoperite pe care regulile sau clasificatorul le refuză | O cale de acces e permisă, omisă sau clasificată greșit | Ar fi putut, dacă o regulă ar fi pus un gate pe apelurile distructive |
| 2. Sandbox | Accesul interzis al proceselor izolate | E oprit, ocolit printr-un tool neacoperit sau defect | Ar fi putut, dacă acoperea apelul distructiv |
| 3. Secrete | Agentul care deține o credențială | Un secret stă la îndemână | Ar fi putut: niciun token de producție în sesiune |
| 4. Hook-uri | Acțiunile acoperite pe care o politică de blocare le refuză | O regulă lipsește, poate fi editată sau permite acțiunea dacă hook-ul eșuează | Ar fi putut: aprobare umană forțată |
| 5. Telemetrie | Nimic; detectează după fapt | Nimeni nu e alertat | Nu, dar „două zile până ne dăm seama” devine „două minute până primește alerta inginerul de on-call” |

Niciun strat, de unul singur, nu i-ar fi salvat pe cei de la PocketOS cu certitudine; oricare dintre straturile aplicate efectiv putea rupe lanțul. Un al doilea incident din 2026, de la DataTalks.Club, a fost imaginea în oglindă: Claude Code a rulat `terraform destroy` pe un state file rămas în urmă. Același remediu: confirmare pe operațiunile distructive, doar credențialele de care are nevoie task-ul și o stare pe care echipa a verificat-o.

---

### Stratul 1: Permisiuni

**Permisiunile răspund la o singură întrebare: are voie agentul ăsta să facă asta, chiar acum?**

Alege modul de permisiuni după riscul muncii, cu reguli explicite de deny sau de aprobare pentru acțiunile cu consecințe importante. Un clasificator poate reduce cererile de confirmare pentru acțiunile eligibile; el completează verificările de reguli ale runtime-ului. Acoperă fiecare cale disponibilă: tool-uri native de fișiere, comenzi de shell și servicii conectate. Politica are nevoie de câte reguli clare și testate cere această acoperire; o listă mai scurtă nu e automat mai sigură.

AGENTS.md explică intenția echipei; nu înlocuiește permisiunile aplicate efectiv. Testează o acțiune permisă și una interzisă prin tool-urile relevante și verifică din nou după schimbări de configurație sau de versiune.

---

### Stratul 2: Sandbox

**Kernelul nu ascultă de raționamentul agentului, așa că injecția nu-l poate ocoli cu vorba.**

Pentru munca obișnuită în repository, începe cu citirile necesare, scriere doar în spațiul de lucru alocat și în fișierele temporare, plus acces de rețea limitat la ce cere task-ul. Verifică acoperirea: sandbox-ul integrat din Claude Code înconjoară comenzile de shell, dar tool-urile native de fișiere, serverele MCP și hook-urile rulează în afara lui. Comenzile native Windows rulează fără sandbox; WSL2 e o variantă de sandbox suportată. Când izolarea la nivel de tool nu ajunge, poate fi necesară izolarea întregului agent.

Investighează eșecurile legitime înainte să lărgești accesul. Acordă cea mai mică excepție justificată și verific-o; nu transforma refuzurile repetate într-o permisiune generală. Default-urile și platformele suportate diferă după agent și versiune (Capitolul 1).

---

### Stratul 3: Secrete

**Cea mai sigură credențială e cea pe care sesiunea n-a deținut-o niciodată.**

Nu da commit la fișiere `.env` și nu expune credențialele de producție procesului agentului. Ține secretele de runtime într-un vault, cu acces limitat la aplicație sau task. Lista de deny-read a unui sandbox de shell protejează doar citirile pe care le acoperă: în Claude Code nu blochează tool-ul nativ Read. Aplică și permisiuni pentru tool-urile de fișiere și ține cont de variabilele de mediu moștenite, serverele MCP și hook-uri. Dacă secretele trebuie să fie inaccesibile pe orice cale, ține-le în afara mediului agentului sau izolează întregul proces.

---

### Stratul 4: Hook-uri

**Hook-urile sunt instrumentul de precizie: un gate programabil pentru categoriile care contează pentru echipa ta.**

Un hook e cod care rulează înainte ca agentul să execute un anumit tip de acțiune (pre-tool-use) și, în funcție de regulile tale, o permite, cere confirmare sau o blochează. Plugin-urile de-a gata vin cu o bază: secrete scurse în diff-uri, pattern-uri de SQL injection, credențiale hardcodate.

Un hook de politică are nevoie de configurație protejată, de un răspuns explicit de blocare și de blocarea acțiunii dacă hook-ul eșuează. Testează ce se întâmplă când hook-ul lipsește, se oprește cu eroare sau depășește timeout-ul. Altfel, hook-urile de comandă și HTTP din Claude Code pot lăsa acțiunea să treacă la eșec; versiunile curente suportă `onFailure: "block"` începând cu v2.1.295 (Anexa C).

Regulile tale proprii vin pe deasupra: orice schimbare în logica de conversie valutară cere aprobare explicită; orice commit care atinge tabela de clienți cere un reviewer de securitate. Apelezi la un hook când permisiunile sunt prea grosiere, iar sandbox-ul prea brutal.

---

### Stratul 5: Telemetrie

**Primele patru straturi previn; telemetria detectează, așa că o prevenție eșuată costă minute, nu zile.**

Înregistrează metadatele tool call-urilor și rezultatele deciziilor de politică într-un store central deținut de echipa de securitate. Capturează argumente sau rezultate doar când e nevoie, eliminând secretele și conținutul sensibil, cu acces controlat și perioadă de păstrare definită. Verifică ce exportă efectiv harness-ul; metricile singure nu formează un jurnal complet al acțiunilor. Atunci „ce sesiuni au atins serviciul de plăți în ultimele treizeci de zile” poate deveni o interogare, în loc de un grep prin istoricele locale. Urmărește:

- o editare în afara task-ului asignat
- apeluri către host-uri din afara allowlist-ului
- refuzuri repetate de permisiuni: un bug în reguli sau o tentativă de injecție
- credențiale de producție în context

---

### Injecția ajunge prin munca în sine

**Tratează tot ce citește agentul drept text de neîncredere și nu te baza pe agent să depisteze atacul.**

Oriunde citește agentul limbaj natural e o suprafață de injecție: un ticket de Jira ale cărui criterii de acceptare spun „ignore all previous instructions”; comentariul de PR al unui contributor extern, cu o instrucțiune ascunsă într-o notă de review; un mesaj de eroare de la un test third-party instabil; un repository cu aspect inofensiv a cărui eroare plantată împinge agentul să ruleze un „fix” care își trage payload-ul real. Am văzut cu ochii mei un agent executând conștiincios o instrucțiune îngropată într-un fișier de log copiat și lipit, pentru că operatorul nu se gândise la un fișier de log ca la un input de neîncredere.

Constrânge ce poate face agentul, indiferent de ce a citit. Un sandbox aplicat efectiv blochează accesul interzis pe căile pe care le acoperă; un hook protejat, cu răspuns de blocare, poate controla categoriile pe care le recunoaște. Verifică și căile pe care nu le acoperă niciunul. Un AGENTS.md otrăvit poate schimba comportamentul agentului la fiecare pornire de sesiune, încă un motiv pentru care trece prin review ca orice cod (Capitolul 6).

---

### Dincolo de cele cinci

**Două practici obișnuite prind ce nu prind straturile.**

- **Separarea mediilor.** Agentul nu deține credențiale de producție by default. Acțiunile de producție trec printr-un gate separat - o aprobare umană, un pipeline de CI, un script de deploy - pe care agentul îl declanșează, dar nu îl execută cap-coadă.
- **Branch-uri protejate, CODEOWNERS și politică de CI.** Agentul deschide pull request-uri ca orice alt contributor; asigură-te că PR-urile lui trec prin aceste reguli, nu pe lângă ele.

---

### În buclă

**Rigoarea trăiește în straturile de sub Execute; Execute doar rulează munca.**

Înainte de faza de Execute din Capitolul 4, stabilește ce reguli de permisiuni, hook-uri și restricții de sandbox acoperă fiecare tool. Nu presupune că un singur sandbox protejează toate scrierile de fișiere sau serviciile conectate. O acțiune blocată cere diagnostic și, unde se justifică, o schimbare autorizată de politică; să-i ceri agentului să încerce altă cale nu e soluția.

---

### Când se strică

- **Fiecare strat e cod, iar codul are bug-uri.** La mijlocul lui 2026, un red team a dezvăluit două escape-uri critice zero-click ale sandbox-ului kernel-backed al unui vendor (patch-uite), iar un check de permisiuni și-a sărit o dată regulile de deny pe lanțuri foarte lungi de comenzi. Ăsta e argumentul pentru cele cinci straturi.
- **Un log fără alertă nu e un strat.** Platforma PocketOS a înregistrat ștergerea, dar nicio alertă nu s-a declanșat când o sesiune de agent a folosit un token de producție; primul semnal a fost o bază de date inaccesibilă.

---

### De făcut luni

*Punctează fiecare strat cu DEFAULT, CONFIGURED, ENFORCED sau MONITORED. DEFAULT sau CONFIGURED pe toată linia e normal; ENFORCED sau MONITORED peste tot e de nivel de producție.*

- [ ] Alege un repository deținut de echipa ta, ideal unul în care un agent face deja commit-uri.
- [ ] Permisiuni: ce rulează fără un prompt de confirmare? Sunt `rm`, `terraform destroy`, drop table și force push pe main păzite de un gate?
- [ ] Sandbox: impus de kernel, sau doar validare de căi în codul agentului însuși?
- [ ] Secrete: au ajuns fișiere `.env` în repo? Poate agentul ajunge la un token de producție?
- [ ] Hook-uri: există vreun hook pre-tool-call care auditează, loghează sau pune un gate pe operațiunile periculoase?
- [ ] Telemetrie: ar apărea o comandă distructivă într-un dashboard în câteva minute?
- [ ] Pentru fiecare strat aflat sub ENFORCED, scrie un fix și un responsabil. Foaia asta e planul trimestrului următor; rulează auditul din nou după fiecare incident.

---

### Mai departe

- **Template:** scorecard-ul de mai sus; pentru plugin-urile care vin cu hook-uri, [Anexa B.10](#template-b10), verificarea plugin-urilor.
- **Deep dive:** [Anexa D, Capitolul 2](#deep-dive-chapter-2) - clasele de vulnerabilități numite, escape-urile din sandbox, default-urile de sandbox per agent și ce au schimbat platformele după incidente.
- **Surse:** Anexa C.

---

# Partea a II-a - Metoda

> *Controlul workflow-ului: cum se formulează, cum se execută și cum se verifică munca.*

Arhitectura răspunde la „ce e chestia asta”. Metoda răspunde la „cum facem treabă cu ea”.

---

## Capitolul 3
## Bottleneck-ul s-a mutat

*La finalul capitolului poți spune dacă un task merită bucla completă și știi cele trei obiceiuri care o fac să se amortizeze.*

**TL;DR**

- Tastatul de cod nu mai e constrângerea; formularea muncii e. Trei obiceiuri o susțin: claritate pe domeniu, descompunere, dovezi din teste înainte de „gata”.
- Pornește cu agentul nativ. O schimbare mică și clară cere execuție directă și o verificare relevantă; neclaritatea, dependențele și riscul justifică mai multă structură.
- Setup-ul și review-ul au un cost; măsoară dacă munca se îmbunătățește. Începe cu o constrângere utilă, nu cu un setup perfect.

---

### Constrângerea s-a mutat

**Bottleneck-ul nu mai e producerea de cod. E formularea muncii suficient de clar încât agentul să facă exact ce trebuie.**

Patruzeci de ani, output-ul a fost limitat de viteza cu care un developer putea tasta cod valid. Autocomplete-ul, IDE-urile mai bune și tastatul asistat de AI au atacat toate decalajul ăsta. Agentul îl sparge: în genul de muncă pe care îl face bine, următoarele o sută de linii au trecut de la o oră de tastat la treizeci de secunde de așteptat. Costul nu e zero, dar nu mai e constrângerea.

Echipele care tratează agentul ca pe un generator de cod îl lasă să tasteze, fac tot restul ca înainte și pierd mai mult timp reparând output-ul decât a câștigat tastatul. Echipele care livrează bine formulează munca astfel încât agentul s-o poată executa corect. Specificațiile vagi produc ghicit, iar ghicitul produce output care arată corect și nu e.

Cei care construiesc modelele sunt de acord. În iulie 2026, un inginer de la Anthropic a deschis un ghid de teren despre Claude Fable 5 numindu-l „primul model la care calitatea muncii are ca bottleneck capacitatea mea de a-i clarifica necunoscutele”.

---

### Trei obiceiuri

**Toate trei țin de formulare, nu de generare.**

- **Claritate pe domeniu înainte de cod.** Dă-i agentului rezultatul așteptat și constrângerile pe care nu le poate deduce din repo. Folosește AGENTS.md pentru regulile stabile și research la nevoie; un skill e un mod opțional de a împacheta practica.
- **Descompunere după rezultate și dependențe.** Pentru munca complexă, definește pași pe care îi poți verifica separat și păstrează în ordine schimbările care depind una de alta. Numărul de fișiere nu decide singur dimensiunea task-ului.
- **Dovezi potrivite înainte de „gata”.** „Arată bine” nu înlocuiește verificarea. Folosește testele relevante, un build, lint, inspecția rezultatului sau o verificare manuală, după schimbare. Pentru un bug de comportament, adaugă unde e fezabil un test de regresie care îl reproduce; o corecție de text nu cere automat un test permanent nou.

Primele două obiceiuri definesc rezultatul așteptat; al treilea măsoară în raport cu el.

---

### Cele patru necunoscute

**Orice gol dintr-un prompt e unul din patru feluri de necunoscută, iar fiecare are alt remediu.**

Același ghid împarte în patru întrebări jumătatea umană a formulării. Maparea pe manualul ăsta îmi aparține mie, nu lui.

| Cadran | Ce este | Unde îl tratează manualul |
|---|---|---|
| Known knowns | Ce spune efectiv promptul tău | Promptul însuși |
| Known unknowns | Întrebări despre care știi că nu le-ai tranșat încă | Întrebările deschise din nota de research, tranșate înainte de plan (Capitolul 4) |
| Unknown knowns | Context atât de evident încât nu ți-ar trece prin cap să-l scrii, deși ai recunoaște pe loc o încălcare | Fișierul de instrucțiuni al echipei, AGENTS.md (Capitolul 6) |
| Unknown unknowns | Ce n-a apucat niciunul dintre voi să întrebe | Blind spot pass-ul și notele de implementare (Capitolul 4), quiz-ul (Capitolul 5) |

---

### Testul buclei

**Dimensionează procesul după neclaritate, dependențe și consecințele unei greșeli.**

Pornește cu capabilitățile native ale agentului și adaugă structură acolo unde rezolvă o problemă concretă:

- **Schimbare mică și clară:** cere modificarea direct și o verificare relevantă. Agentul poate corecta și două linii; nu trebuie să le tastezi tu ca să eviți un workflow mare.
- **Muncă neclară sau cu dependențe:** clarifică rezultatul și folosește un plan scurt, cu ordinea pașilor și verificările necesare.
- **Muncă riscantă, nefamiliară sau greu de întors:** formulează explicit criteriile de acceptare, gate-urile umane și review-ul suplimentar. O singură linie într-o regulă de plăți poate cere mai multă atenție decât o schimbare mecanică în zece fișiere.

Superpowers poate organiza munca amplă, dar nu e o condiție ca să începi. Păstrează-l dacă îmbunătățește rezultatele pentru modelul, versiunea și task-urile tale, la un cost justificat. Comparațiile publice arată beneficii punctuale și overhead; nu justifică nici instalarea obligatorie, nici dezactivarea universală. Dovezile și limitele sunt în Anexa D.

---

### Două echipe, un trimestru

**Investiția unei echipe s-a amortizat într-un trimestru; calendarul tău are nevoie de măsurători.**

Cel mai clar caz pe care l-am văzut: două echipe din aceeași companie, pe zone adiacente ale aceluiași produs, cu același agent.

Echipa A a dat drumul agentului imediat. Au sărbătorit velocity-ul de început. Prin luna a treia livrau cam la nivelul de dinainte de agent, dar cu rate de defecte mai mari și cu reviewerii seniori vizibil storși.

Echipa B a petrecut prima lună pe practică: AGENTS.md scris și iterat, skill-uri scrise pentru pattern-urile echipei, hook-uri configurate. În luna aceea n-au livrat nimic condus de agent. În luna a doua au revenit la velocity-ul de bază. În luna a treia livrau la o calitate și un velocity vizibil mai bune decât înainte de agent.

Disciplina pare lentă; lipsa ei costă mai mult, și asta rămâne invizibil până nu te uiți la cycle time pe un trimestru întreg. A fost o observație de teren, nu un experiment controlat, iar echipele adiacente nu sunt eșantioane independente.

---

### Începe mic

**Practica nu trebuie să fie perfectă ca să producă beneficii.**

Câteva instrucțiuni utile în AGENTS.md pot preveni greșeli repetate. O notă scurtă ajută când clarifică o necunoscută reală. Echipele care construiesc workflow-ul perfect înainte să-l ruleze se blochează, pentru că mereu mai e o regulă, un skill sau un hook de adăugat.

Scrie pe scurt ce știi deja că e periculos, treci câteva story-uri prin agent și adaugă regulile care ar fi prevenit eșecurile pe care le-ai văzut. Cincisprezece linii pot fi un început, nu o cotă de completat.

---

### Când se strică

- **Bucla aplicată la tot, sau la nimic.** Dacă toate task-urile trec prin buclă, încetinești; dacă niciunul, ratezi câștigurile. Rulează întâi testul buclei.
- **Verdictul dat în săptămâna patru.** Echipa B n-a livrat nimic condus de agent în prima lună. Măsoară pe tot trimestrul.

---

### De făcut luni

- [ ] Clasifică următorul task: mic și clar, neclar sau cu dependențe, ori riscant și nefamiliar. Alege nivelul de structură potrivit.
- [ ] Cere-i agentului modificarea direct sau, dacă e nevoie, o scurtă clarificare și un plan.
- [ ] Scrie ce înseamnă „gata” și cum verifici. Adaugă în AGENTS.md doar constrângerile stabile pe care agentul nu le poate deduce din cod.

---

### Mai departe

- **Template-uri:** [Anexa B.2](#template-b2), scheletul AGENTS.md; [B.3](#template-b3), checklist-ul buclei în șase faze.
- **Deep dive:** [Anexa D, Capitolul 3](#deep-dive-chapter-3) - framework-ul necunoscutelor din ghidul Fable 5, studiul METR și avertismentul lui, și regresia din februarie-aprilie 2026.
- **Surse:** Anexa C.

---

## Capitolul 4
## Bucla în șase faze

*La finalul capitolului poți trece un feature prin Research, Plan, Execute și Ship și știi care gate-uri sunt ale tale.*

**TL;DR**

- Șase funcții: Research, Plan, Execute, Review, Verify, Ship. Pot încăpea într-un task scurt sau pot cere documente și gate-uri distincte; riscul decide.
- Planul e gate-ul unde contează cel mai mult un om. Câteva minute de citit planul te scutesc de o după-amiază de dat înapoi în Execute.
- Ship e un pull request obișnuit, cu dovezile atașate. Nu există o bandă specială pentru AI.

---

### Ce este bucla în șase faze? {#what-is-the-six-phase-loop}

**Cele șase faze descriu ce trebuie rezolvat, nu șase skill-uri, documente sau aprobări obligatorii.**

Research, Plan, Execute, Review, Verify și Ship sunt funcții ale livrării. Pentru un task simplu, citirea fișierului, două propoziții despre modificare și o verificare pot acoperi cea mai mare parte a buclei. Pentru un feature riscant, documentele și gate-urile explicite fac deciziile verificabile. Agentul nativ poate face aceste lucruri. Superpowers, Spec Kit, BMAD sau skill-urile echipei sunt opțiuni de implementare, pe care le evaluezi după rezultate.

```
   +--------+    +------+    +---------+    +--------+    +--------+    +------+
   |Research|--->| Plan |--->| Execute |--->| Review |--->| Verify |--->| Ship |
   +--------+    +------+    +---------+    +--------+    +--------+    +------+
                    ^             |                         |
                    +-- abordare schimbată                   |
                                  ^                         |
                                  +--- verificare picată ---+
       Context lipsă? Revii la Research.
```

*Figura: Bucla în șase faze. Un defect de implementare revine la Execute; o abordare schimbată, la Plan; contextul lipsă, la Research.*

| Faza | Artefactul | Gate-ul uman | Eșecul prins |
|---|---|---|---|
| Research | Contextul relevant și întrebările deschise; notă dacă ajută | Clarificare pe domeniu la nevoie | Context lipsă |
| Plan | Pași și dependențe, pe măsura schimbării | Review de scop și ordine când riscul îl cere | Descompunere proastă |
| Execute | Diff; note pentru deciziile importante | După limitele de autonomie agreate | Drift de implementare |
| Review | Conformitate cu spec-ul, corectitudine și calitate | Review conform riscului și regulilor echipei | Cod greșit sau slab |
| Verify | Dovezi din verificările relevante | Review de QA sau de owner când e necesar | Eșec comportamental |
| Ship | PR cu lanțul de dovezi | Procesul normal de PR | Încălcare de proces |

**Bucla se sprijină pe un rezultat așteptat bine definit.** Agentul poate construi aproape orice îi descrii, dar nu poate ști la care lucru te-ai referit. Research scoate la suprafață ce nu e încă hotărât, tu tranșezi, planul transformă rezultatul stabilit în verificări, iar Verify măsoară ce s-a construit față de el. Sari peste asta și „gata” e orice a decis agentul.

---

### Feature-ul

Iată un feature urmărit prin toate fazele. E mic: adaugă un câmp `priority` pe recordul `Wire`, într-un serviciu bancar reglementat.

Priority e una dintre valorile low / normal / high / urgent, are default normal, iar flag-ul urgent declanșează un queue separat de compliance review.

---

### Research

**Research produce o notă, nu cod - iar întrebările deschise le tranșezi tu.**

I-am cerut agentului să citească codebase-ul și să scrie o notă de research. A numit patru fișiere pe care nu le-aș fi găsit nici într-o oră de grep:

- recordul `Wire` în sine
- directorul de migrații
- serviciul queue-ului de compliance review
- emitter-ul de audit log

A ridicat și o întrebare deschisă: priority să fie enum sau text liber? Spec-ul reglementatorului folosește text liber în unele documente și enum în altele. Am ales enum. Alegerea asta nu era un detaliu - definea ținta față de care fazele de mai târziu aveau să verifice modificarea.

Pentru un feature de tipul ăsta, două până la patru pagini pot fi utile; nu sunt o cotă. O schimbare delimitată poate avea nevoie doar de câteva rânduri. Nota acoperă ce contează:

- fișierele care vor fi atinse
- convențiile pe care le urmează acele fișiere
- testele existente care acoperă zona
- concepte înrudite din alte părți ale codebase-ului
- întrebările deschise, acolo unde trebuie să decidă un om

Research e faza peste care echipele sar cel mai des, pentru că nu produce cod. Din experiența mea, e și faza cu cel mai mare levier: o notă proastă garantează un plan prost, iar una bună ancorează planul în codul real, nu în prima ipoteză a agentului.

Dacă task-ul e în afara domeniului tău, începe cu un blind spot pass: cere-i agentului să te ajute să-ți găsești unknown unknowns și spune-i pe față ce nu știi. Își calibrează răspunsul după expertiza pe care o deduce din vocabularul tău, așa că o fluență de fațadă îi ține presupunerile ascunse.

Păstrează deciziile durabile în repository, alături de modificare. Nota de research merită un commit dacă explică alegeri pe care un coleg va trebui să le înțeleagă și peste șase luni; observațiile de lucru nu trebuie toate transformate în documente permanente.

---

### Plan

**Planul e gate-ul unde contezi cel mai mult.**

Agentul a transformat nota într-un plan de șase task-uri:

1. Adaugă coloana în baza de date, cu default.
2. Actualizează clasa recordului `Wire`.
3. Actualizează serviciul wire-builder.
4. Actualizează contractul de API.
5. Actualizează logica de rutare pe compliance ca să citească noul câmp.
6. Actualizează emitter-ul de audit log.

Fiecare task atingea un fișier sau o pereche de fișiere. Task-ul cinci depindea de schimbarea de contract din task-ul patru; ordinea era corectă, iar agentul marcase dependența. Aprobat.

Un plan pe care îl poți aproba are trei proprietăți:

- **Fiecare task numește rezultatul, zona de cod și verificarea.** Două-cinci minute sunt un exemplu de granularitate pentru pași mecanici, nu o regulă. Grupează munca suficient de coerent încât contextul și review-ul să nu coste mai mult decât execuția.
- **Numește verificările potrivite.** Teste existente sau noi, build, lint ori inspecție, după schimbare; testele de regresie au sens pentru un bug de comportament. Un plan trebuie să explice cum verifici, nu să inventeze teste fără valoare.
- **Spune ce înseamnă „gata” pentru întreaga modificare**, nu doar per task. Ăsta e rezultatul pe care îl va verifica Verify.

La munca cu risc sau decizii importante, îl citești înainte de execuție. Respingi task-urile prea vagi sau prost ordonate, adaugi ce lipsește și scoți ce iese din scop. Pentru o schimbare clară și deja autorizată, un plan scurt nu cere automat încă o rundă de aprobare.

Review-ul de plan ia câteva minute. Te scutește de o după-amiază întreagă atunci când planul era greșit și ai fi aflat abia în Execute - de unde e mult mai greu de dat înapoi.

---

### Execute

**Deleagă unități coerente de muncă; păstrează un singur scriitor pe zonele care se suprapun.**

În cazul acesta, șase subagenți au rulat în paralel, câte unul per task, fiecare constrâns la fișierul lui. S-au întors în mai puțin de trei minute. Cinci task-uri au avut teste care treceau din prima. Asta descrie rularea, nu o regulă de dispatch: dependența dintre contract și rutare trebuia respectată la integrare și verificare. Într-un plan nou, execuți în ordine task-urile dependente.

Al șaselea (emitter-ul de audit log) avea și el un test care trecea, dar testul era greșit: verifica vechiul format de log. Verde - și greșit. Capitolul 5 arată cum a fost prins.

Un subagent merită pornit când primește muncă suficient de amplă, independentă și bine delimitată încât beneficiul să acopere pornirea, transferul de context și integrarea. Agentul principal poate executa singur task-urile scurte sau strâns legate. Un subagent primește contextul relevant, verifică rezultatul și raportează; nu ai nevoie de unul per task sau per fișier.

Izolarea nu e o soluție-minune. Regulile care o țin să funcționeze:

- **Împarte după independență, nu doar după fișier.** Două fișiere pot depinde de același contract. Un singur scriitor pe o zonă de cod care se suprapune, dependențe executate în ordine și cititori în paralel unde ajută: asta limitează conflictele și editările inconsistente.
- **Delegarea trebuie să-și justifice costul.** O investigație sau implementare amplă și independentă poate beneficia de alt context. Câteva tool call-uri sau pași strâns legați rămân de obicei în agentul principal; pornirea și coordonarea pot costa mai mult decât timpul economisit.
- **Citește hand-off-urile orchestratorului cu scepticism.** Orchestratorul tot ține câte un rezumat al fiecărui task, iar un rezumat imprecis al task-ului unu îl poate face pe task-ul patru să-l contrazică. Am văzut cu ochii mei șase subagenți producând editări reciproc inconsistente exact din motivul ăsta.
- **Consemnează deciziile importante.** Devierile de la plan, edge case-urile și alegerile care afectează alt task merită note comune. Pentru o schimbare mică poate fi suficient raportul final; un plan lung are nevoie de stare durabilă, ca să nu reia munca după compactare.

Când un task eșuează, diagnostichează înainte de a relansa: un defect de implementare revine la Execute, o abordare care trebuie schimbată revine la Plan, iar contextul lipsă cere Research. Agentul continuă în limitele autorizate; cere o decizie umană când problema schimbă scopul, riscul sau permisiunile.

---

### Review și Verify

**Review verifică diff-ul față de spec; Verify verifică comportamentul față de rezultatul așteptat.**

La feature-ul wire, Review a prins testul de audit log și o migrație fără direcția de down, iar Verify a rulat suita completă plus un smoke test pe staging. Capitolul 5 se ocupă de ambele faze: cum citești un diff scris de agent și de ce o suită verde scrisă de agent e un indiciu, nu o dovadă.

---

### Ship

**Ship e un pull request obișnuit. Nu există o bandă specială pentru AI.**

Agentul face commit cu un mesaj structurat, dă push pe branch și deschide un pull request a cărui descriere spune ce s-a schimbat, de ce, cum s-a verificat, ce riscuri rămân și cine e etichetat la review.

La feature-ul wire, PR-ul a venit cu nota de research, planul, rapoartele per task, ambele review-uri și dovezile din teste atașate. Un reviewer senior a petrecut unsprezece minute pe el și a pus o singură întrebare: ar trebui ca flag-ul urgent să fie vizibil în dashboard-ul de metrici? Nu mă gândisem la asta. Aprobat, merged.

PR-ul ăsta e exact artefactul pe care echipa știe deja să-l revizuiască. Agentul nu îți înlocuiește procesul de livrare; îl alimentează cu muncă mai bine formulată.

---

### Cât costă în timp

**Bugetează separat timpul agentului, investigația și review-ul uman.**

Din experiența mea cu task-uri bine delimitate, un feature mic poate trece prin buclă în douăzeci-treizeci de minute, unul mediu în aproximativ o oră, iar unul mare în câteva ore. Sunt exemple pentru planificare, nu promisiuni de livrare sau o comparație măsurată cu munca manuală. Necunoscutele, problemele de mediu, durata testelor și disponibilitatea reviewerilor pot domina timpul; măsoară-le pe task-urile tale.

Feature-ul wire a luat nouăzeci de minute, de la „hai să adăugăm un câmp de prioritate” la cod în merge. Diferența o face contextul reglementat: o suită de 3.400 de teste, un smoke test pe staging și un diff de contract pentru reglementator. Mic ca scop nu înseamnă mic ca ceremonie.

Timpii de mai sus sunt repere din practică, nu promisiuni sau limite. Dacă o schimbare delimitată durează mult, verifică unde s-a dus timpul: execuție, context transferat, review repetat, blocaje reale sau aprobări redundante. Măsoară și timpul uman, rework-ul și consumul facturat, nu doar timpul de ceas.

---

### Când rulezi mai puțin din buclă

**Sari peste o fază doar dacă poți numi ce îi face deja treaba.**

Testul din Capitolul 3 îți spune când merită bucla în sine; în interiorul buclei se aplică aceeași contabilitate.

O echipă pe care am urmărit-o a lucrat cea mai mare parte a unui an cu ceea ce părea jumătate de buclă: Research-ul era un fir de comentarii, planul era trei bullet-uri în PR. A funcționat pentru că funcțiile se mutaseră în pereții echipei - o echipă mică și senioră, care își construise singură codebase-ul, o suită de CI strictă și o cultură de PR serioasă. Cele șase faze sunt funcții care trebuie să se întâmple undeva. Dacă nu poți spune unde, faza rămâne.

---

### Când se strică

- **Instrucțiunile nu sunt enforcement.** Limitele de securitate și aprobările obligatorii au nevoie de controalele din Capitolul 2; nu transforma fiecare preferință de proces într-un hook sau într-un gate.
- **Subagenții paraleli pe fișiere care se suprapun** produc editări inconsistente. Redelimitează pe fișier sau pe modul, sau rulează task-urile în secvență.
- **Sesiunile lungi derivă.** Agentul răspunde din nou la întrebări deja tranșate și uită constrângeri. Asta e contaminarea contextului, iar Capitolul 6 acoperă remediul.

---

### De făcut luni

- [ ] Alege un task și dimensionează procesul după Capitolul 3. Cere research doar pentru necunoscutele relevante.
- [ ] Clarifică deciziile care schimbă rezultatul și criteriile de acceptare.
- [ ] Dacă ai nevoie de plan, verifică ordinea, dependențele, scopul și dovezile cerute.
- [ ] Deleagă doar unități suficient de ample și independente; păstrează un singur scriitor pe zonele care se suprapun.
- [ ] Livrează prin procesul normal de PR, cu deciziile și verificările utile reviewerului.
- [ ] Compară calitatea, regresiile, consumul facturat, timpul uman, rework-ul și timpul de ceas cu execuția nativă.

---

### Mai departe

- **Template:** [Anexa B.3](#template-b3), checklist-ul buclei în șase faze.
- **Deep dive:** [Anexa D, Capitolul 4](#deep-dive-chapter-4) - comparațiile Superpowers, când merită delegarea și alegerea contextului pentru workeri și revieweri.
- **Surse:** Anexa C.

---

## Capitolul 5
## Review și Verify

*La finalul capitolului poți citi diff-ul unui agent în ordinea potrivită, poți spune cât dovedește o suită de teste verde și poți seta controalele care țin faza de Verify onestă.*

**TL;DR**

- Review-ul verifică intenția, corectitudinea și calitatea. Folosește revieweri suplimentari unde riscul și rezultatele îi justifică; citirea ta rămâne pentru judecata de business și arhitectură.
- Un diff curat de agent poate totuși să rateze intenția, așa că îl citești din exterior spre interior: forma schimbării, apoi testele, apoi liniile.
- O suită verde scrisă de agent e un indiciu, nu o dovadă. Verificările trebuie să acopere comportamentul cerut; izolarea evaluării și testele ascunse sunt controale suplimentare pentru situații care le justifică.

---

### Cine verifică ce

**Sunt perspective de review, nu patru agenți obligatorii. Alege verificările după schimbare și risc.**

| Verificarea | Citește | Întreabă |
|---|---|---|
| Conformitate cu spec-ul | Cererea, criteriile de acceptare, deciziile și diff-ul | Am construit ce trebuia? |
| Corectitudine și calitate | Diff-ul și contextul relevant | E corect și respectă standardele echipei? |
| Citirea umană | Diff-stat-ul, testele, granițele, numele noi | E corectă regula de business? Se potrivește cu arhitectura? |
| Verify | Verificările relevante: teste, build, lint, staging sau contract, după caz | Comportamentul respectă definiția de „gata”? |

---

### Feature-ul wire, mai departe

**O suită fericită poate fi totuși greșită.**

Capitolul 4 a lăsat emitter-ul de audit log cu un test verde și greșit. Reviewerul de conformitate cu spec-ul, comparând diff-ul cu planul, a prins faptul că testul verifica vechiul format de log și a semnalat o migrație căreia îi lipsea direcția de down. Reviewerul de calitate a codului, care a văzut doar diff-ul, n-a găsit nimic notabil. Subagentul implementator a reparat ambele puncte și a rerulat testele relevante.

Apoi Verify a rulat suita completă de 3.400 de teste și un smoke test pe serviciul de rutare compliance din staging și a produs un diff al schimbării de contract de API pentru review-ul reglementatorului. Toate verzi. Dovezile astea au intrat în pull request la faza de Ship din Capitolul 4.

---

### Review: perspective distincte, revieweri după nevoie {#review-two-agents-then-you}

**Verifică atât conformitatea cu cererea, cât și corectitudinea soluției; separarea în agenți este opțională.**

Un reviewer poate acoperi ambele perspective. Pentru schimbări riscante, un domeniu nefamiliar sau erori pe care verificarea inițială le ratează, merită un reviewer independent, cu context proaspăt. Ghidurile vendorilor diferă chiar între modele: Fable 5 favorizează verificatori separați, în timp ce Opus 5 poate pierde timp prin delegare excesivă. Nu transforma recomandarea pentru un model într-o regulă pentru toate.

- **Cere constatări concrete de corectitudine și risc.** Un prompt vag de tipul „fă review ca un senior” poate produce sugestii fără valoare și abstracțiuni necerute.
- **Păstrează independența când o urmărești.** Dă-i reviewerului cererea, criteriile și contextul necesar; nu-i arăta verdictul primului reviewer înainte să-și formeze propria evaluare.
- **Acceptă sau respinge fiecare constatare cu un motiv.** Urmărește defectele reale găsite și rezolvate, nu volumul de comentarii sau scorul unui reviewer.
- **Limitează rundele la un beneficiu observabil.** După un fix, verifică problema și eventualele regresii. Un review nou sau o suită rerulată fără schimbări ori incertitudini noi consumă timp fără să adauge automat dovezi.

Defectele critice blochează livrarea; cele importante se rezolvă sau primesc o decizie explicită de risc înainte de ship. Sugestiile de stil nu declanșează automat încă o rundă. Păstrează review-ul uman și aprobările cerute de echipă.

---

### Cum faci review pe un diff scris de agent? {#reviewing-agent-diffs}

**Citește din exterior spre interior: întâi intenția, la urmă liniile.**

Orice diff poate conține o greșeală de tastare, un off-by-one sau un edge case uitat. Un diff de agent poate și să compileze, să treacă de lint și să se citească precum codul pe care echipa ta l-ar accepta la merge, dar să rateze intenția și contextul: o regulă de business plauzibilă și greșită, codul corect pus în stratul greșit, codul pe care l-ar scrie un inginer bun pentru un task ușor diferit. Fluența nu e corectitudine.

Începe review-ul deasupra codului și dimensionează timpul după schimbare:

1. **Diff-stat-ul raportat la cerere sau plan.** Forma schimbării se potrivește cu cererea? Un fișier neașteptat merită o explicație: poate fi o descoperire necesară sau o extindere a scopului.
2. **Citește testele pentru ce afirmă,** nu pentru dacă trec. Verdele e cel mai ieftin semnal și cel pe care îl ai deja.
3. **Verifică granițele despre care echipa ta a scris reguli:** pattern-urile interzise din AGENTS.md, convențiile de strat, modulele periculoase de atins. Agentul le încalcă sigur pe el și în stil fluent, așa că o încălcare arată curat.
4. **Dă grep pe fiecare nume nou introdus de diff** pe care nu-l recunoști. Apelul care nu există se citește la fel de plauzibil ca cel care există (verificarea încrucișată e în Capitolul 6).
5. **Abia acum, linie cu linie,** concentrând timpul pe corectitudinea de business și pe potrivirea arhitecturală, fie că ai folosit sau nu revieweri-agent.

Pentru schimbări nefamiliare sau cu consecințe importante, o verificare opțională a înțelegerii poate ajuta: cere-i agentului un quiz despre edge case-uri, ownership și ce se strică dacă o presupunere e greșită. O întrebare fără răspuns arată ce trebuie lămurit înainte de aprobare. Folosește-l când review-ul obișnuit nu a stabilit deja această înțelegere. Anexa B.8 conține ordinea de citire și verificarea opțională.

---

### Verify

**Verify măsoară comportamentul față de rezultatul pe care l-a definit planul.**

Folosește verificările care demonstrează rezultatul și protejează zona afectată: teste existente, teste de regresie unde sunt utile, build, lint, inspecție vizuală sau o verificare manuală. Pentru un bug de comportament, un test care eșuează înainte de fix și trece după e o dovadă bună. O schimbare reversibilă de text sau stil nu cere automat un test permanent nou. Rulează suita mai largă când dependențele, riscul ori regulile repo-ului o cer; o rulare deja validă nu trebuie repetată fără un motiv nou.

Pentru verificarea comportamentului în frontend, preferă rolurile și etichetele vizibile utilizatorului, disponibile prin accessibility tree, în locul selectoarelor CSS fragile. Accessibility tree e structura pe care browserele o întrețin pentru screen readere. Un test Playwright care găsește câmpul etichetat Priority, îi schimbă valoarea, apasă Save și verifică noua valoare afirmă comportament și supraviețuiește unei restilizări sau schimbării bibliotecii de componente. Schimbările vizuale cer și verificarea rezultatului randat; testele de comportament nu evaluează layout-ul.

---

### Poți avea încredere în testele scrise de agent? {#trusting-agent-tests}

**Testele verzi sunt un indiciu, nu o dovadă.**

Sunt un indiciu că modificarea face ce spune testul, nu că testul spune ce trebuie, așa cum a arătat testul de audit log. Coverage-ul nu închide decalajul: măsoară ce linii s-au executat, nu dacă s-a verificat ceva cu sens, iar un agent care optimizează pentru un gate de coverage scrie teste care apelează codul și nu afirmă nimic de substanță. Testele de caracterizare, prima soluție din Capitolul 8 pentru un codebase fără teste, fixează comportamentul curent, nu corectitudinea, și conservă un bug la fel de fidel cum conservă un feature: o plasă de siguranță contra regresiilor cât migrezi, niciodată o dovadă.

Așa că fă review pe testele agentului ca pe codul lui, verificând aserțiunile față de spec. Un test scris pornind de la implementare confirmă implementarea; aserțiunea trebuie să vină din intenție.

Agentul poate optimiza pentru dovezile pe care le vede. SpecBench arată un decalaj mare între testele vizibile și cele ascunse; e un avertisment despre evaluare, nu un motiv să tratezi fiecare PR ca pe un benchmark adversarial.

Pentru munca obișnuită:

- [ ] **Verifică aserțiunile față de rezultat.** Acoperă cazul cerut, limitele relevante și regresiile; nu doar implementarea pe care ai primit-o.
- [ ] **Explică eșecul înainte de fix.** Înțelege de ce pică verificarea și dacă problema e în cod, test sau mediu.
- [ ] **Protejează integritatea verificărilor.** Nu slăbi testele, lint-ul sau CI-ul ca să obții verde. Schimbările legitime ale lor sunt permise în scopul autorizat și trec prin review; hook-urile pot impune limitele necesare fără să blocheze orice editare de configurație.

Pentru evaluări controlate, livrare nesupravegheată sau cerințe ridicate de asigurare, adaugă unde e justificat teste held-out independente și izolarea accesului la soluții din istoric sau rețea. Istoricul sigilat și lipsa egress-ului nu sunt default-ul fiecărui PR. Detaliile și limitele dovezilor sunt în Anexa D.

---

### Când toolkit-ul se uită în locul tău

**Agenții de review sunt un filtru pus în fața judecății umane, niciodată un substitut pentru ea.**

O echipă cu care am lucrat a instalat un toolkit complet de review: agenți pentru excepții înghițite, teste slabe, probleme de securitate și documentație învechită. Prindea bug-uri reale, săptămână după săptămână, reviewerii seniori au învățat să aibă încredere în bifele verzi, iar într-un trimestru review-urile lor de cincisprezece minute deveniseră scanări de trei minute. Nimeni n-a decis asta; atenția alunecă singură de pe munca ce pare deja făcută.

Apoi un PR pe care îl trecuseră toți agenții - teste verzi, zero constatări de securitate, diff curat - a aplicat o regulă de discount pe segmentul greșit de clienți și a rulat în producție săptămâni întregi, până l-a scos la iveală un tichet de suport. Toolkit-ul funcționase exact cum fusese proiectat: scosese constatările mecanice din review-ul uman, iar judecata se dusese odată cu ele. Ăsta e delegatorul necalibrat din Capitolul 9, la scară de echipă.

Soluția a fost un prag explicit: un review minim pe corectitudinea de business și pe potrivirea arhitecturală pentru fiecare PR atins de agent, urmărit ca o cifră, lângă rata de defecte. Ordinea de citire de mai sus e pragul ăsta făcut concret.

---

### Când se strică

- **Citirea degenerează într-o privire fugară la bifele verzi.** Timpul de review și defectele scăpate pot scoate la iveală deriva; o verificare opțională a înțelegerii poate arăta ce lipsește înainte de aprobare.

---

### De făcut luni

- [ ] Citește următorul diff de agent în ordinea de mai sus. Pentru o schimbare nefamiliară sau cu consecințe importante, încearcă quiz-ul opțional și lămurește ce nu ai putut explica.
- [ ] Deschide ultimele trei teste scrise de agent. Aserțiunile vin din spec sau din cod?
- [ ] Verifică intenția și corectitudinea; adaugă un reviewer independent dacă riscul sau erorile observate îl justifică. Cere un răspuns motivat la fiecare constatare.
- [ ] Alege verificările relevante și protejează-le integritatea. Rezervă testele held-out și izolarea evaluării pentru situațiile care le cer.
- [ ] Fixează un review uman minim pentru PR-urile atinse de agent și urmărește-l lângă rata de defecte.

---

### Mai departe

- **Template-uri:** [Anexa B.8](#template-b8), ordinea de citire a unui diff de agent; [B.3](#template-b3), checklist-ul buclei.
- **Deep dive:** [Anexa D, Capitolul 5](#deep-dive-chapter-5) - măsurătorile despre review, SpecBench și Cursor în întregime și rezerva legată de accessibility tree.
- **Surse:** Anexa C.

---

## Capitolul 6
## AGENTS.md și contextul

*La finalul capitolului poți scrie un AGENTS.md în care fiecare linie își merită locul și poți rula sesiuni de agent care rămân ascuțite.*

**TL;DR**

- AGENTS.md e infrastructură de echipă: reguli locale scurte, cu motiv clar, trecute prin review ca orice cod și deținute de un champion.
- Ține-l scurt și relevant: constrângeri locale, comenzi verificate și pointeri. Circa 200 de linii e un reper de întreținere, nu un prag universal demonstrat. Agentul citește înainte să citeze; tu verifici numele noi.
- Contextul e memorie de lucru. O unitate de muncă per sesiune, starea durabilă în fișiere, o repornire curată la primul semn de derivă.

---

### Ce este AGENTS.md? {#what-is-agents-md}

**AGENTS.md este acordul echipei cu agentul, versionat în git.**

E un fișier markdown din rădăcina repository-ului, pe care agentul îl citește la începutul sesiunii, înainte de orice prompt. Transformă „ce i se pare agentului rezonabil” în „ce a convenit echipa că e rezonabil”, care trece prin review într-un pull request. E stratul deținut manual al componentei principale Memory din Capitolul 1: partea pe care o scrie echipa.

### AGENTS.md vs CLAUDE.md: care e diferența? {#agents-md-vs-claude-md}

**Același rol, dar regulile de încărcare depind de harness și de versiune.**

AGENTS.md e o convenție folosită de mai mulți vendori și e citit nativ de Codex CLI, Cursor, GitHub Copilot, Gemini CLI și alții. Din v2.1.277, Claude Code îl poate citi nativ când nu există CLAUDE.md sau CLAUDE.local.md în directorul de lucru ori în directoarele părinte. Dacă ambele convenții sunt prezente, default-ul favorizează CLAUDE.md; poți importa `@AGENTS.md` în acel fișier. Setările și versiunile mai vechi diferă, așa că verifică ce fișiere s-au încărcat efectiv.

---

### Povestea: o linie, trei ore pe lună

O echipă cu care am lucrat folosea un coding agent de șase luni când un senior engineer a venit la mine cu o nemulțumire. „De fiecare dată când generăm un endpoint de API, trebuie să repar validarea. Mereu aceeași corecție. Agentul pune validarea în stratul greșit.”

„De ce nu e regula scrisă undeva?”

„N-am scris-o niciodată. Doar o tot reparăm.”

Am făcut socoteala. În ultima lună agentul generase douăsprezece endpoint-uri, iar el corectase stratul de validare în unsprezece dintre ele, cam cincisprezece minute pe fiecare. Trei ore de timp de senior pe lună, înghițite de „munca normală de review”.

Am scris o singură linie în AGENTS.md: „Adnotările Bean Validation stau pe DTO-uri, la granița controller-ului; metodele din stratul de service au încredere în input-urile lor.” Am adăugat-o în template-ul de pull request, ca reminder pentru revieweri, și am marcat endpoint-urile deja corecte ca exemple de referință. Următoarele douăsprezece endpoint-uri n-au avut nevoie de nicio corecție pe stratul de validare.

Regula nu a făcut agentul perfect. A eliminat o corecție repetată la nesfârșit, iar în asta stă tot rostul fișierului.

---

### Șase reguli pentru fișier

**Șase reguli, fiecare cu un test pe care îl poți aplica oricărei linii.**

| # | Regula | Ai respectat-o când |
|---|---|---|
| 1 | O linie, o constrângere verificabilă | Numește stratul, mecanismul și un exemplu |
| 2 | Un motiv local și verificabil | Poți numi eșecul prevenit sau constrângerea neintuitivă și de ce contează |
| 3 | Context stabil, cu scop clar | Constrângeri locale, convenții, comenzi, glosar și pointeri utili |
| 4 | Scurt și verificat în practică | Fiecare instrucțiune își justifică locul; circa 200 de linii e un reper, nu o limită dovedită |
| 5 | Tratează-l ca pe cod | Git, review în PR, un singur champion care se rotește |
| 6 | Citește înainte să citezi | Fiecare nume a fost citit în sesiunea asta sau găsit cu grep |

---

### Regula 1: scrie reguli pe care agentul le poate verifica

**O regulă pe care agentul n-o poate verifica e decor.**

| | Regula |
|---|---|
| Prost | „Respectă întotdeauna standardele noastre de cod. Ai grijă la validare. Folosește arhitectura corectă.” |
| Bine | „Validarea de la granița controller-ului aparține DTO-urilor, prin adnotări Bean Validation. Serviciile au încredere în DTO-urile validate și nu re-validează. Nu adăuga niciodată adnotări de validare în metodele de service. Exemple: UserCreateController, AccountUpdateController.” |

Varianta proastă sună responsabil, dar „ai grijă” nu e o constrângere, iar „arhitectura corectă” depinde de un context pe care regula nu-l oferă. Varianta bună e linia din poveste, întărită: numește stratul, mecanismul, regula și două exemple pe care agentul le poate folosi ca pattern de urmat. Pattern-urile interzise urmează aceeași formă, cu motivul într-o propoziție; Anexa B.2 are trei.

### Regulile 2 și 5: motivate de context, tratate ca cod {#rules-2-and-5-earned-by-failure-owned-like-code}

**O regulă își câștigă locul prin utilitate locală, iar un champion ține fișierul în formă.**

- **Dă-l la review ca pe cod.** Reviewerul întreabă ce problemă previne și de ce agentul nu poate deduce singur regula. Un eșec real e o justificare bună; o constrângere neintuitivă de securitate, business sau compatibilitate poate intra preventiv, cu motiv și dovezi. Best practice-urile generice nu merită copiate automat.
- **Ține un jurnal de greșeli.** O intrare per incident real, cu regula care previne repetarea și un pointer la dovadă, commit-ul sau incidentul; B.2 are o intrare-exemplu.
- **Numește un champion.** O singură persoană deține fișierul și jurnalul; toată lumea editează prin pull request-uri, iar championul curatoriază. În fiecare trimestru, championul întreabă pentru fiecare intrare dacă a salvat pe cineva în ultimele trei luni și le retrage pe cele a căror problemă de fond a dispărut, cu motivul în mesajul de commit; o regulă care încă previne un eșec rar rămâne. Apoi rolul se rotește.

### Regulile 3 și 4: context relevant, lungime justificată {#rules-3-and-4-fixed-contents-hard-cap}

**Păstrează constrângerile locale, comenzile și pointerii care scutesc agentul de ghicit.**

- **Pattern-uri interzise, convenții și intrări de jurnal**, câte o linie fiecare.
- **Comenzile exacte de build și de test.** Fără ele, agentul ghicește, iar uneori ghicește greșit.
- **Un glosar de domeniu.** În pretraining, „transfer” înseamnă o grămadă de lucruri; în banca ta înseamnă unul singur, iar un „wire” e strict cel inter-bancar.
- **O linie de pointer:** „Structura repository-ului și harta modulelor: `docs/architecture.md`. Citește-l înainte să atingi un modul pe care nu l-ai văzut în sesiunea asta.”

O hartă voluminoasă se citește mai bine la cerere, în `docs/architecture.md`; un pointer sau o scurtă informație de orientare poate rămâne dacă ajută task-urile reale. Studiul revizuit despre AGENTS.md nu a găsit o îmbunătățire generală a succesului pentru fișierele de context generate și a măsurat un cost de inferență cu peste 20% mai mare în setup-urile testate. Fișierele scrise de developeri au adus un câștig mediu modest, fără semnificație statistică. Studiul nu dovedește că orice fișier de instrucțiuni dăunează sau că fiecare categorie de context trebuie eliminată.

**Folosește circa 200 de linii ca reper de întreținere.** Nu există o prăpastie demonstrată la linia 201. Elimină redundanțele și regulile generice, mută detaliile la locul lor și păstrează regulile rare care încă previn un eșec real. Un studiu despre numărul de reguli din prompturi nu stabilește o conversie universală între reguli și linii de AGENTS.md. Verifică dacă fișierul tău ajută, pentru modelul și task-urile folosite.

Fișierul unei echipe de banking a crescut în șase luni până pe la nouă sute de linii, iar agentul a început să ignore regulile cele mai noi. L-am tăiat la nouăzeci, mutând convențiile în skill-uri care se încarcă la detecție și istoricul greșelilor din trecut în documentul de arhitectură, iar rata de conformare a sărit în sus într-o săptămână. Cazul arată utilitatea selecției și a structurii, nu validează un plafon universal de linii.

### Regula 6: când agentul minte cu încredere

**Agentul inventează fișiere, funcții și opțiuni, așa că obligă-l să demonstreze ce citează.**

Va cita un fișier care nu există, o funcție pe care biblioteca n-a expus-o niciodată, o opțiune scoasă din uz acum trei versiuni. Output-ul arată plauzibil și e greșit; agentul potrivește pattern-uri din cod similar și nu știe că ghicește. Trei tactici mecanice:

- **Citește înainte să citezi.** Tot ce menționează agentul trebuie să fi fost citit în sesiunea curentă. AGENTS.md poate impune asta: „Înainte să faci referire la orice funcție, citește fișierul care o definește. Citările fără o citire prealabilă se tratează ca ciorne de verificat.”
- **Dă grep după fiecare nume nou.** Zero rezultate înseamnă că funcția probabil nu există sau stă într-o dependență vendored pe care agentul n-o vede. Durează câteva secunde și prinde cele mai frecvente invenții.
- **Pune un hook pe citări.** Dacă agentul citează un fișier și o linie, câteva linii de bash într-un hook pot verifica dacă linia există (Capitolul 2).

---

### Igiena contextului {#context-hygiene}

**Fereastra e memoria de lucru a agentului, așa că încarcă ce cere task-ul și nimic în plus.**

Tot ce e în fereastră concurează pentru aceeași atenție mărginită. Sesiunile lungi eșuează prin contaminarea contextului, când materialul deja rezolvat sau învechit acoperă task-ul curent; e cel mai mare motiv pentru care sesiunile lungi de agent o iau razna. Patru obiceiuri o previn.

- **Pointere, nu payload-uri.** Pune în AGENTS.md un link spre documentele mai lungi și doar contextul stabil care ajută frecvent. Reperul de 200 de linii te îndeamnă să alegi, nu să tai instrucțiuni necesare ca să atingi un număr.
- **Păstrează starea de care ai nevoie.** Pentru munca de durată, notează deciziile, constrângerile, progresul și comenzile care au mers, în formatul potrivit proiectului. Un issue, un fișier existent sau o scurtă notă pot fi suficiente; nu ai nevoie de trei documente și un commit la fiecare restart.
- **Urmărește cele patru semne.** Agentul reia întrebări rezolvate, citează un fișier învechit, uită o constrângere sau face editări tot mai neglijente. Verifică starea reală și corectează contextul; dacă deriva continuă, păstrează ce e necesar și pornește o sesiune curată. Fă commit după practica repo-ului, nu ca ritual de restart.
- **Tratează compactarea ca pe un hand-off.** Rezumarea unei ferestre pline pierde detalii, așa că tot ce contează și nu e într-un fișier se pierde. Dacă compactezi, dă-i compactorului o listă de păstrat: planul, întrebările deschise, devierile consemnate în notele de implementare, comenzile exacte care au mers.

---

### Când se strică

- **Fișierul e o rugăminte, nu un zid.** Agentul tot poate încălca AGENTS.md. Restricțiile obligatorii cer permisiuni aplicate efectiv, izolare sau gate-uri protejate de review; un hook ajută doar pe căile pe care le acoperă (Capitolul 2).
- **Intrările vechi devin folclor.** O intrare fără pointer la dovadă e greu de retras, iar un cimitir de reguli e aproape la fel de inutil ca lipsa lor: echipa încetează să mai aibă încredere în vreuna.

---

### De făcut luni

- [ ] Verifică instrucțiunile curente ale repository-ului. Adaugă o convenție lipsă documentată, o constrângere justificată sau o corecție repetată; include comenzi și pointeri unde scutesc agentul de ghicit. Nu ai o cotă de linii sau de reguli de completat.
- [ ] Găsește-ți propria poveste cu validarea: o corecție pe care o tot faci în review. Scrie-o ca o singură linie verificabilă și adaugă-o în template-ul de PR, ca reminder pentru revieweri.
- [ ] Verifică numele nefamiliare față de definițiile și sursele lor. Adaugă regula „citește înainte să citezi” dacă rezolvă o problemă observată și numește un responsabil pentru întreținerea instrucțiunilor.
- [ ] În următoarea sesiune lungă, urmărește deriva. Păstrează starea necesară pentru hand-off, apoi recuperează contextul, compactează sau repornește după caz; fă commit conform practicii repository-ului.

---

### Mai departe

- **Template-uri:** [Anexa B.2](#template-b2), scheletul AGENTS.md (conține linia de precedență); [B.7](#template-b7), igiena contextului pe o singură pagină; [B.11](#template-b11), punerea pe picioare a fișierului pe un repository.
- **Deep dive:** [Anexa D, Capitolul 6](#deep-dive-chapter-6) - studiul despre fișierele de context, limitele dovezilor despre numărul de reguli, mecanica jurnalului de greșeli și măsurătorile despre compactare și cache.
- **Surse:** Anexa C.

---

## Capitolul 7
## Întâi harta: review-ul de arhitectură

*La finalul capitolului poți produce o hartă corectată a unui codebase pe care nu și-l mai amintește nimeni și poți folosi rularea ca diagnostic inițial pentru următorul pas.*

**TL;DR**

- Folosește o investigație bine delimitată ca să schițezi `docs/architecture.md`, apoi verifică harta față de cod și realitatea de business.
- În cazul de mai jos, agentul a lucrat 18 minute, iar corecția expertului a luat circa 45. Acuratețea și timpul de review depind de acces, scop și cunoașterea domeniului.
- Aceeași rulare e un diagnostic inițial. O hartă incoerentă cere să oprești schimbările autonome și să investighezi modelul, accesul, contextul și codebase-ul (Capitolul 8).

---

### Workflow-ul

**Pune agentul să citească întâi codul, apoi corectează ce a scris și dă commit rezultatului.**

Multe echipe dețin un codebase care se potrivește unei singure descrieri: autorul a plecat, README-ul descrie un build care nu mai merge, codul aduce bani și nimeni nu vrea să-l atingă. Agentul poate scurta prima investigație, dar o hartă nu înseamnă că ai devenit productiv sau că ai înțeles business-ul. Cazul de mai jos a cerut minute de lucru de agent și review de la un expert de domeniu; alte repository-uri cer mai mult.

Promptul cere nouă secțiuni, de la scop și model de date până la riscuri și necunoscute, cu citări fișier:linie peste tot; textul complet e în Anexa B.1. Alege secțiunile și profunzimea de care are nevoie investigația. Un document poate părea complet și totuși să interpreteze greșit partea esențială de business. Dacă codebase-ul depășește un singur context window, investigațiile independente pe module pot justifica subagenți, iar orchestratorul asamblează bucățile și verifică granițele comune.

---

### Cazul

**Agentul n-a decis că rewrite-ul nu era necesar. A dat experților de domeniu suficientă structură ca să decidă mai repede.**

O echipă de banking deținea un sistem de onboarding pentru clienți: cam șaizeci de mii de linii de Java, scrise între 2018 și 2024 de o distribuție rotativă de contractori. Echipa fusese asamblată în 2024 din trei achiziții și nimeni nu fusese de față la build-ul original. README-ul descria o arhitectură din 2020, iar documentația enumera doi dintre cei trei pași ai build-ului. Echipa lua în calcul un rewrite complet, estimat la optsprezece luni, pentru că „nimeni nu îl înțelege suficient de bine ca să-l întrețină cu încredere.”

Am cerut cincisprezece minute și un terminal. Am lipit promptul de review cu două adăugiri: domeniul (onboarding de clienți, banking reglementat) și cererea de a marca tot ce arată a fi sensibil din punctul de vedere al conformității. Optsprezece minute mai târziu aveam un document de treisprezece pagini, greșit în trei locuri:

- A numit serviciul de deduplicare „serviciu de căutare”, pentru că implementarea folosea infrastructura de search. Scopul lui de business era să prevină crearea de dubluri ale înregistrărilor de clienți.
- A descris cu deplină încredere, în detaliu, un job programat. La o privire mai atentă, era cod comentat, nerulat în producție de trei ani.
- A ratat faptul că o dependență third-party era deprecated și avea un security advisory. Agentul nu avea acces la baza de date de advisories, așa că am adăugat eu informația.

Documentul corectat a intrat în repository, iar echipa n-a mai făcut rewrite-ul. Documentul le-a arătat cele două module care chiar aveau nevoie de înlocuire, dependența deprecated fiind una dintre ele, iar echipa le-a înlocuit doar pe acelea în trimestrul următor. Am rulat exact workflow-ul ăsta pe exact codebase-ul ăsta, iar compania a economisit nouă om-luni de efort de rewrite pe care altfel le-ar fi cheltuit și le-ar fi regretat.

| | |
|---|---|
| **Context** | Echipă de banking reglementat, serviciu Java de ~60k LOC scris între 2018 și 2024, documentație învechită |
| **Timp de agent** | ~15-18 minute |
| **Timp de corecție umană** | ~45 de minute (reviewerul cunoștea domeniul de onboarding de clienți) |
| **Rezultat** | Două module purtau datoria tehnică; rewrite-ul de 18 luni a devenit o înlocuire țintită de 3 luni |
| **Limitări** | Workflow-ul accelerează cunoașterea de domeniu, nu o înlocuiește |

---

### Corectează harta

**Harta agentului e o ciornă, iar estimarea de 45 de minute presupune un reviewer care cunoaște domeniul.**

Nu mai văzusem niciodată codebase-ul ăla, dar construisem sisteme de onboarding și înainte, așa că știam cum arată de obicei un serviciu de deduplicare și un path de conformitate în banking reglementat. Greșelile agentului mi-au sărit în ochi. Un reviewer nou și pe codebase, și pe domeniu n-are un asemenea reper: identificările greșite continuă să pară plauzibile, nu poate spune pe care să le semnaleze, iar corecția durează ore, nu 45 de minute. Workflow-ul funcționează în continuare; partea umană costă mai mult.

Verifică harta față de cinci lucruri:

- Scopul modulelor, raportat la realitatea de business, nu la infrastructura de implementare.
- Orice e descris ca activ, dar ar putea fi mort sau comentat.
- Faptele despre dependențe și advisories pe care agentul nu le vede.
- Path-urile sensibile din punctul de vedere al conformității.
- Fiecare ambiguitate semnalată chiar de agent.

---

### Dă-i commit

**Documentul corectat e punctul de intrare pentru orice lucrare ulterioară.**

Pune-l la `docs/architecture.md`. Membrii noi ai echipei îl citesc primii, inginerii seniori îl consultă înainte să atingă o parte nefamiliară, iar agentul îl deschide la cerere, când un task atinge un modul pe care nu l-a văzut, în loc să re-derive arhitectura. AGENTS.md conține o trimitere către fișier, nu structura codebase-ului (Capitolul 6).

---

### Review-ul ca diagnostic

**O hartă incoerentă e un motiv să oprești schimbările autonome și să investighezi cauza.** Rularea e un diagnostic inițial, nu un verdict despre codebase.

- **Hartă coerentă, corecție rezonabilă:** o informație utilă pentru următorul task bine delimitat. Nu dovedește înțelegerea comportamentului sau pregătirea pentru producție.
- **Output incoerent:** verifică accesul lipsă, contextul incomplet, aria investigației și potrivirea modelului înainte să pui eșecul pe seama codului încâlcit. Dacă echipa tot nu poate evalua rezultatul, păstrează munca respectivă condusă de oameni și folosește grila din Capitolul 8.

Alocă un timp limitat primei investigații, apoi decide dacă încă o trecere ar putea lămuri o necunoscută concretă. Kill signals din Capitolul 8 sunt grila sistematică; o singură hartă nu o înlocuiește.

---

### Când se strică

- **Output nerevizuit.** Citările și structura îngrijită nu transformă o ciornă în documentație corectă.
- **Un reviewer fără cunoaștere de domeniu** nu poate spune pe care dintre greșelile plauzibile să le semnaleze. Bugetează ore.
- **Harta se învechește.** Rerulează review-ul ori de câte ori codebase-ul se schimbă substanțial.

---

### De făcut luni

- [ ] Pe un codebase slab înțeles, alege părțile relevante din Anexa B.1, numește domeniul și alocă un timp limitat primei treceri.
- [ ] Corectează output-ul după cele cinci verificări de mai sus.
- [ ] Salvează-l ca `docs/architecture.md`, dă-i commit și adaugă în AGENTS.md o singură linie de trimitere. Nu lipi structura în fișier.
- [ ] Evaluează dovezile: alege următorul task bine delimitat sau investighează de ce a eșuat harta. Folosește Capitolul 8 înainte să extinzi scopul.
- [ ] Notează timpul de investigație și de corecție înainte să repeți exercițiul în altă parte.

---

### Mai departe

- **Template:** [Anexa B.1](#template-b1), promptul de architecture review.
- **Deep dive:** [Anexa D, Capitolul 7](#deep-dive-chapter-7) - de ce căutarea simplă în cod bate un index vectorial aici și Understand Anything, alternativa vizuală.
- **Surse:** Anexa C.

---

# Partea a III-a - Realitatea

> *Controlul adopției: unde funcționează metoda, unde nu - și cum îți dai seama.*

---

## Capitolul 8
## Are voie agentul să atingă codul ăsta?

*La finalul capitolului poți puncta orice codebase ca verde, galben sau roșu și poți spune ce lucrări ar trebui și ce lucrări nu ar trebui să facă agentul acolo.*

**TL;DR**

- Punctezi un codebase pe opt kill signals: 0-1 înseamnă verde (condus de agent), 2-3 galben (condus de om), 4 sau mai multe roșu (repară întâi codebase-ul).
- Semnalul 6, echipa care nu poate evalua output-ul, cântărește mai greu decât celelalte: dacă e prezent, munca respectivă e roșie indiferent de total.
- Numără după intensitate, nu după simpla prezență, și punctează per proiect, nu per companie.

---

### Când n-ar trebui să folosești agenți AI de cod? {#when-not-to-use-agents}

**Unele codebase-uri n-ar trebui să primească încă un agent, iar un nu acolo e ceea ce îți permite să spui da peste tot în rest.**

Motivul nu e că agentul ar fi prost sau echipa slabă: codebase-ul are proprietăți care fac lucrul cu agenți nesigur, neproductiv sau ambele. Grila are opt kill signals, fiecare o proprietate a codebase-ului sau a echipei. Fără ea, orice proiect devine un proiect AI, iar eșecurile celor care n-ar fi trebuit să fie murdăresc reputația întregii abordări.

---

### Cele opt kill signals

**Fiecare semnal strică lucrul agentului în felul lui, și fiecare are un prim fix.**

| Semnal | Cum arată | Exemplu | Primul fix |
|---|---|---|---|
| 1. Fără teste | Nicio suită, sau una pe care n-o rulează nimeni | O modificare a stricat un modul de reconciliere netestat; a ieșit la suprafață abia după două luni | Teste de caracterizare |
| 2. Fără documentație | Doar autorul original știe de ce | Agentul a „simplificat” un fee tier care avea o excepție de reglementare din 2017 | Review-ul de arhitectură (Capitolul 7) |
| 3. Cuplare strânsă | Editezi un fișier, se strică alte trei | Trei module într-un ciclu de importuri vechi de 14 ani | Sparge cea mai gravă cuplare |
| 4. Reguli împrăștiate | Aceeași regulă trăiește în mai multe locuri | Limita de transfer într-un config de UI, o constantă din serviciu și un trigger din baza de date | O singură sursă de adevăr |
| 5. Constrângeri de reglementare | Fiecare schimbare cere o aprobare trasabilă | Schimbările de anti-money-laundering cer trei semnături pe care agentul nu le poate ruta | Workflow de aprobare |
| 6. Echipa nu poate evalua output-ul | Nimeni nu poate judeca rezultatul într-un anumit domeniu | Un junior livrează criptografie scrisă de agent (mai jos) | Restrânge scope-ul sau adaugă un reviewer expert |
| 7. Potrivirea model-context | Corpus public subțire (COBOL, DSL-uri proprietare) | Un workflow engine intern; agentul a aplicat pattern-uri dintr-un alt framework | Adaugă documentație și skill-uri sau alege un model cu potrivire mai bună |
| 8. Viteza schimbării | Un framework se mișcă sub agent | Idiomuri de React 18 în cod care avea nevoie de React 19 | Numește versiunea-țintă în [AGENTS.md](https://agents.md/); încetinește agentul pe căile atinse |

---

### Semnalul 1: fără teste

**Închide-l pe ăsta primul și lasă agentul să ajute - ca plasă de siguranță, nu ca dovadă.**

Cere-i agentului teste de caracterizare pentru ce face modulul acum; specificația e „orice produce codul în acest moment”, adică exact genul de generare de teste în masă la care agentul e bun. E o investiție reală de timp, iar dacă echipa nu e dispusă s-o facă, răspunsul e nu. Testele fixează comportamentul de azi, bug-urile incluse: o plasă de siguranță, nu o dovadă (Capitolul 5).

---

### Semnalul 6: echipa nu poate evalua output-ul

**E cel mai important semnal și cel pe care echipele îl înțeleg greșit cel mai des.**

Un developer junior primește un story: adaugă un pas de verificare criptografică în fluxul de plăți. Juniorul trimite agentul la treabă, iar agentul produce un modul care folosește AES-256 în mod CBC cu un initialization vector hardcodat. Pentru cineva nou în criptografie, arată corect: compilează, testele unitare trec, iar criptograful senior e în concediu de creștere a copilului trei luni. Juniorul livrează, iar vulnerabilitatea stă în producție șase luni, până o găsește un penetration test.

Agentul a făcut exact ce i s-a cerut. Output-ul lui arăta bine și era greșit, iar nimeni nu era în poziția de a vedea asta.

Echipele citesc asta ca „ne trebuie mai mulți ingineri seniori”, ceea ce nu scalează pe un orizont de șase luni. Pentru zonele sensibile, cere aprobarea unui specialist calificat printr-un review obligatoriu impus pe server, pe care credențialele agentului nu-l pot ocoli. Politica aplicată la nivel de tool poate împiedica și editarea acelor module. AGENTS.md poate explica restricția, iar agenții de review pot ajuta, dar niciunul nu înlocuiește expertiza lipsă și nu face aprobarea inevitabilă.

Semnalul ăsta cântărește mai greu decât celelalte: se numără împreună cu ele și, în plus, are prioritate față de total. Un codebase care are zero pe semnalele unu-cinci, dar da pe semnalul șase, e tot roșu pentru munca respectivă. Celelalte șapte costă productivitate; ăsta se termină în raportări de conformitate și în retrospective de incident. Soluția: construiești capacitatea, aduci pe cineva care o are sau ții agentul departe.

---

### Sunt agenții AI de cod gata de producție? {#are-agents-production-ready}

**Depinde de proiect: numărul de semnale alege culoarea, iar semnalul șase singur duce proiectul pe roșu.**

```
  Număr semnale      Culoare     Mod
  =============      =======     ===

  0 - 1              VERDE       Condus de agent, viteză normală
  2 - 3              GALBEN      Condus de om, sprijin de agent
  4 +                ROȘU        Stop. Repară întâi codebase-ul.

  Semnale (numără fiecare semnal prezent):
   1. Fără teste            5. Constrângeri de reglementare
   2. Fără documentație     6. Echipa nu poate evalua output-ul
   3. Cuplare strânsă       7. Potrivirea model-context
   4. Reguli împrăștiate    8. Viteza schimbării
```

*Figura: Kill signals și regula de decizie a semaforului. Semnalul 6 cântărește mai greu decât celelalte.*

- **Verde:** condus de agent. Un singur developer trimite agentul la treabă și supraveghează bucla în șase faze.
- **Galben:** condus de om, cu sprijinul agentului. Faci pair programming cu el în loc să-l trimiți singur la treabă; câștigul e mai ales de calitate, nu de viteză.
- **Roșu:** repară mai întâi codebase-ul. Contribuția agentului e net negativă până când semnalele scad.

Aplică semaforul per proiect, nu per companie. Începe cu verdele, mută galbenul spre verde într-un trimestru sau două, iar roșul reformează-l sau scoate-l din uz.

---

### Numără după intensitate, nu după prezență

**Semnalele nu sunt binare, iar diferența dintre 3 și 4 e o regulă empirică, nu un prag exact.**

Un semnal parțial valorează jumătate: testele care există, dar sunt parțiale, sunt jumătate din semnalul 1; documentația veche de trei ani e jumătate din semnalul 2. Adună valorile parțiale și rotunjește: patru jumătăți fac un 2, trei jumătăți și un semnal întreg fac un 3, cinci jumătăți fac un 3. Fișa de punctare completă e în Anexa B.4.

---

### Cum arată culorile

**Fiecare culoare schimbă felul în care folosești agentul.**

| Proiect | Număr | Culoare | Ce faci |
|---|---|---|---|
| Serviciu de profil de client: acoperire de 70%, privire de ansamblu în README, reguli într-o singură bibliotecă | 0 | Verde | Condus de agent, prin buclă |
| Motorul legacy de plăți: acoperire de 20%, documentație veche, cuplare moderată, mecanism de audit existent | 2,5, rotunjit la 3 | Galben | Condus de om: teste de caracterizare, documentație, refactorizări delimitate |
| Bibliotecă de criptare custom, scrisă de un contractor în 2017: nedocumentată, fără criptograf | 5 | Roșu | Ține agentul departe; finanțează expertiza sau înlocuiește biblioteca cu una standard verificată |
| Serviciu API greenfield: echipă senioră, specificație clară | 0 | Verde-plus | AGENTS.md înainte de primul commit, teste din prima zi |
| Tool intern: 20 de developeri, scris în 2019, expunere de reglementare mică | 1 | Spre verde | Primul proiect potrivit pentru o echipă la început cu agenții: realistă, cu miză mică |

---

### Când se strică

- **Numărarea prezenței în loc de intensitate** transformă galbenul în verde. „Tehnic are teste” care acoperă 10% din cod, de calitate slabă, nu înseamnă că ai trecut de semnalul ăsta.
- **Adoptarea AI pe un codebase roșu pentru că așa a decis leadership-ul** e pattern-ul din spatele poveștilor de adopție eșuată. Repară întâi semnalele.
- **Un codebase verde începe să dea rezultate galbene după un upgrade de model.** Bănuiește întâi instrucțiunile scrise pentru modelul anterior, înainte să dai vina pe cod: rulează checklist-ul de migrare din Anexa B.9.

---

### De făcut luni

- [ ] Alege un proiect în desfășurare și scrie-ți culoarea din instinct pe o foaie separată. Tot exercițiul durează sub cincisprezece minute.
- [ ] Punctează cele opt semnale cu fișa de punctare din Anexa B.4, folosind răspunsurile echipei, nu impresia ta.
- [ ] Verifică întâi semnalul șase: dacă e prezent, munca respectivă e roșie indiferent de total. Apoi numără și compară cu instinctul; distanța dintre ele arată pe ce semnale pui prea mult sau prea puțin accent.
- [ ] Apără clasificarea în fața tech lead-ului tău, cu scorurile în mână.
- [ ] Repunctează trimestrial, după incidentele majore și înainte să extinzi scope-ul agentului.

---

### Mai departe

- **Template-uri:** [Anexa B.4](#template-b4), fișa de punctare; [B.9](#template-b9), checklist-ul de migrare între modele.
- **Deep dive:** [Anexa D, Capitolul 8](#deep-dive-chapter-8) - cazurile din banking din spatele semnalelor de la 1 la 5 și 7, bug-ul React 18/19 din spatele semnalului 8 și studiul din spatele verificării de migrare.
- **Pentru manageri:** Anexa A, perspectiva de portofoliu.
- **Surse:** Anexa C.

---

## Capitolul 9
## Lansarea în echipă

*La finalul capitolului poți rula agenți în siguranță într-un repository real și poți porni un rollout așa cum încep cele mai multe rollout-uri reușite: cu un singur inginer.*

**TL;DR**

- Pe un repo real, dă muncii agentului propriul worktree, pune hook-uri și pe agent, și pe git și păstrează un prag minim de review uman pe care nu-l înlocuiește niciun bot de review.
- Cele mai multe adopții încep cu un singur inginer, nu cu trei roluri: folosești agentul tu însuți, scrii ce ai făcut, îl înveți pe un coleg, apoi îi recrutezi pe lead și pe manager. Prima lună nu arată aproape niciun câștig; câștigul se compune după aceea.
- Numește cele două arhetipuri de ingineri și planifică săptămâna proastă a vendorului înainte să te prindă vreuna dintre ele.

---

### Guardrails pentru un repo real

**Agentul e încă un autor cu acces de scriere, așa că dă-i granițele pe care le primește orice autor.**

Obiceiurile astea la nivel de repo se așază peste cele cinci straturi din Capitolul 2 și contează cel mai mult pe codebase-uri galbene (Capitolul 8). Pragul minim de review uman pe care nu-l înlocuiește niciun bot de review ține de Capitolul 5.

---

### Worktree-uri

**Izolează munca simultană a agenților de schimbările locale neterminate.**

Un worktree e o copie separată a repository-ului, checked out pe propriul branch. E util pentru task-uri simultane sau când agentul ar atinge altfel munca locală neterminată. Un checkout curat, dedicat, sau un mediu deja izolat pot servi aceluiași scop. Worktree-urile previn coliziunile între copii de lucru; nu sunt un sandbox de securitate, iar toată munca trece în continuare prin review-ul obișnuit.

---

### Două feluri de hook-uri

**Pune hook-uri pe agent, pune hook-uri pe repository și rulează aceleași verificări în CI.**

- **Hook-ul de agent** (hookify sau echivalentul agentului tău) verifică acțiunile pe care le acoperă și le permite, cere aprobare sau le blochează. Folosește-l pentru zone sensibile, precum criptografie, plăți sau migrări. Configurația și comportamentul la eșec au nevoie de protecție (Capitolul 2); un fișier din repository pe care agentul îl poate rescrie nu e o graniță fermă.
- **Hook-ul de git** rulează pentru oricine face commit - tu, un coleg sau agentul - așa că o singură verificare acoperă toți autorii. Verificările rapide (formatare, lint, verificare de tipuri, scanare de secrete) rulează la commit, testele și build-ul la push, iar un manager de hook-uri cu configurație versionată se asigură că hook-urile se instalează pentru oricine clonează repository-ul.
- **Ocolirile locale** includ `--no-verify` și schimbarea configurației de hook-uri din Git. O regulă de deny poate prinde unele tentative; nu face hook-urile locale obligatorii.

Hook-urile locale oferă feedback rapid: pot fi sărite și nu sunt garantate pe fiecare mașină. Impune acceptarea prin verificări obligatorii pe server, schimbări de workflow protejate și aprobare obligatorie de la owner. Verifică dacă agentul are credențiale care pot schimba sau ocoli aceste reguli; mutarea unei verificări editabile în CI nu o protejează de la sine.

---

### Cum ții practica vie

**Regulile se învechesc, așa că cineva răspunde de curățarea lor.**

Jurnalul de greșeli și championul lui țin de Capitolul 6. Pentru greșelile de proces, ține un watchlist de eșecuri: eșecurile recurente, ce le declanșează și răspunsul standard al echipei. Parcurge-l cam o dată pe lună și retrage ce s-a rezolvat.

---

### Bucla exterioară

**Rulează agentul nesupravegheat doar sub un contract scris.**

Bucla exterioară (outer loop) reinvocă agentul până când o condiție e îndeplinită. Adaugă încercări, nu judecată, așa că multiplică orice permite bucla ta interioară (inner loop; Capitolul 4). Folosește-o doar pe codebase-uri VERZI (Capitolul 8), pe multe unități similare, verificabile și reversibile, și citește pull request-urile dimineața.

Înainte de prima rulare nesupravegheată, scrie cinci linii: o condiție de oprire pe care o poate evalua o mașină; un buget; un gate pe care agentul nu-l poate edita; context proaspăt la fiecare iterație, cu starea în repository; izolare dimensionată pentru absență (worktree propriu, sandbox pornit, fără credențiale de producție, rețea constrânsă). Anexa B.6 e formularul de completat, cu cele patru semne care cer stop înainte să relansezi.

---

### Cum faci rollout-ul agenților AI de cod într-o echipă? {#how-to-roll-out}

**Începe cu un singur inginer care refuză să renunțe, nu cu un program.**

Prima dată când am predat grila celor trei roluri, un inginer din ultimul rând a zis: „Managerul meu n-a auzit de AI agentic. Lead-ul meu n-are timp. Sunt singurul om din echipă căruia îi pasă. Eu ce fac?”

Pentru el, arcul cu trei roluri s-ar împotmoli în luna a doua, când conversația de procurement nu se întâmplă niciodată. Arcul grassroots (de jos în sus) nu s-ar împotmoli și e felul în care au început cele mai multe adopții reușite din 2025 și 2026: o singură persoană joacă pe rând rolul de champion, apoi de lead de facto, apoi de avocat al adopției pe lângă manager. L-am văzut reușind de două ori.

- **Luna 1: folosește-l pe munca ta.** Review-uri de arhitectură, schițe de AGENTS.md și bucla în șase faze pe codul pe care îl deții, în interiorul politicilor existente. Fără anunțuri; strânge dovezi în liniște.
- **Luna 2: pune-l pe hârtie.** Un memo de o pagină: story-uri livrate, timp economisit, note oneste acolo unde agentul n-a ajutat. Povestește ce ai făcut; nu face pitch de adopție.
- **Luna 3: învață-l pe colegul care întreabă.** Scrie împreună cu el un caz mai consistent și invită-ți tech lead-ul la un walkthrough.
- **Lunile 4-6: lead-ul recrutează managerul** cu dovezi și cu doi ingineri care cer același workflow.

Până în luna șase, practica arată cum arăta arcul ideal în luna trei - dar a durat de două ori mai mult. Compromisul: arcul grassroots pornește repede și e fragil, pentru că dacă singurul inginer pleacă înainte să fie recrutați colegii și managementul, practica moare odată cu el. Arcul cu trei roluri pornește mai încet și rezistă la o plecare. Dacă ai un manager care știe de agenți, un lead implicat și buget, fă arcul cu trei roluri; dacă ai doar propriile ore, fă arcul grassroots.

---

### Arcul de 90 de zile

**Arcul de 90 de zile e un calendar posibil, nu o lege a productivității.**

Exemplul alocă prima lună setup-ului și unui pilot bine delimitat, a doua extinderii, iar a treia responsabilităților operaționale. Unele echipe au beneficii imediat; altele petrec mai mult timp cu accesul, guvernanța sau verificarea. Urmărește de la început cycle time-ul, defectele, efortul de review și consumul și extinde doar când dovezile susțin decizia. Adaugă fișiere de instrucțiuni, skill-uri și hook-uri pentru o nevoie demonstrată sau un risc justificat. Calendarul-exemplu e în Anexa B.5.

```
  Zilele 1-30: Fundația             Zilele 31-60: Extinderea        Zilele 61-90: Operaționalizarea
  -------------------------         -------------------------       -------------------------
  Championul instalează             Lead-ul aduce încă 2-3          Managerul integrează
  AGENTS.md schițat                 ingineri                        metricile în tracking-ul
  Primul proiect pe verde           AGENTS.md consolidat            normal de velocity
  Workflow-ul de architecture       Hooks configurate               Guvernanța de vendor semnată
  review demonstrat                 Skills la nevoie                Politica de plugin
                                    Kill signals aplicate           marketplace stabilită
                                    pe portofoliu
  ====================              ====================            ====================
  Champion                          Lead                            Manager
```

*Figura: arcul de adopție de 90 de zile, ca un calendar posibil. Fiecare fază atribuie responsabilități; etapele depind de nevoile și rezultatele pilotului.*

---

### Angajamentele rolurilor

**Stabilește un buget explicit de timp și adaptează angajamentele din exemplu la echipă.**

**Championul** învață primul workflow-ul. Are nevoie de timp protejat și de disponibilitatea de a investiga eșecurile; senioritatea singură nu decide alegerea. Șaizeci de ore sunt o alocare posibilă pentru planificare, nu o condiție sau o prognoză.

- [ ] Săptămâna 1: instalează agentul, rulează review-ul de arhitectură (Capitolul 7) pe un codebase familiar și dă commit artefactului.
- [ ] Săptămâna 2: verifică instrucțiunile existente și adaugă constrângerile sau comenzile utile care lipsesc. Invită completări justificate prin pull request-uri.
- [ ] Săptămânile 3-4: folosește funcțiile din Capitolul 4 pe trei feature-uri, dimensionând procesul pentru fiecare; notează fricțiunile în jurnalul de greșeli.
- [ ] Lunile 2-3: trei feature-uri medii, în care alții preiau câte o singură fază, apoi predă rolul; până în ziua 90, un alt inginer rulează workflow-ul la fel de fluent.

**Lead-ul** decide ce proiecte primesc agentul și ține semaforul.

- [ ] Săptămâna 1: clasifică primele cinci proiecte după cele opt kill signals (Capitolul 8) și împărtășește culorile.
- [ ] Săptămânile 2-4: pentru câte un proiect de fiecare culoare, scrie ce ar trebui să se schimbe ca să treacă la culoarea următoare.
- [ ] Lunile 2-3: urmărește cycle time-ul, rata de defecte și timpul reviewerilor (cifre zgomotoase; măsoară oricum), apoi prezintă rezultate oneste, inclusiv unde agentul n-a livrat.

**Managerul** deține bugetul, procurement-ul și sign-off-ul de guvernanță și protejează echipa de metrici premature. Pagina lui e Anexa A, cu proiectul de 20 de ingineri în care PR-urile atinse de agent (41% din total) au avut un cycle time cu 28% sub baseline-ul de dinainte de agent, iar defectele au rămas în marja de zgomot.

---

### Două arhetipuri care omoară rollout-urile

**Tratează-l pe fiecare ca pe o problemă structurală cu o soluție structurală, nu ca pe un defect de caracter.**

**Scepticul de principiu** e seniorul care a mai văzut cicluri de hype AI, nu va folosi agentul și face review la PR-urile conduse de agent cu o ostilitate sporită. Ori echipa lucrează pe lângă el și codebase-ul se bifurcă în teritorii prietenoase cu agentul și teritorii ostile, ori el câștigă disputa și rollout-ul se blochează. Nu încerca să-l convertești; dă-i o graniță: „modulele tale, regulile tale, agentul nu se atinge de ele; peste tot în rest se aplică standardul echipei”. Și nu lăsa fiecare PR condus de agent să stea în queue-ul lui, altfel i-ai dat un drept de veto pe care nu l-a vrut nimeni.

**Delegatorul necalibrat** sare peste citirea atentă pentru că „agentul o nimerește mereu”. Defectele se adună, echipa dă vina pe agent, nu pe pasul de review care lipsește, iar până la urmă inginerul nu mai poate depana ce a ajutat agentul să construiască. Fiecare PR condus de agent primește același review uman ca unul condus de om. În prima lună, pune-l în pereche cu un senior care citește output-ul linie cu linie.

---

### Vendorul va avea o săptămână proastă

**Planifică pentru situația în care agentul nu e disponibil.**

Am văzut velocity-ul unei echipe înjumătățindu-se timp de o săptămână pentru că modelul lor principal era rate-limited. În iunie 2026, cel mai nou tier flagship al celui mai mare vendor a fost retras la nivel mondial la câteva zile după lansare și a rămas indisponibil aproape trei săptămâni; echipele cu fallback și-au rulat planurile pe bune, iar cele fără și-au redescoperit setup-ul anterior pe deadline. Ține un fallback non-agentic pentru munca sensibilă la timp, un senior care încă poate livra un hotfix la trei dimineața și un runbook pentru „agentul e throttled și clientul așteaptă”.

---

### Când se strică

| Se strică când | Ce se întâmplă | Fix |
|---|---|---|
| Un champion, fără lead | Championul face singur toată munca cu agentul; agentul e catalogat drept „interesant, dar limitat” | Checklist-ul lead-ului, de mai sus |
| Un champion și un lead, fără manager | Procurement-ul stă blocat, proiectele galbene rămân galbene; clasificarea nu are cumpărător | Pagina managerului, Anexa A |
| Un lead și un manager, fără champion | Angajați în teorie, blocați în practică | Checklist-ul championului, de mai sus |
| Hook-uri locale tratate ca enforcement | Sunt sărite, editate sau niciodată instalate | Rulează aceleași verificări în CI |

---

### De făcut luni

- [ ] Verifică dacă spațiul de lucru al agentului e izolat de munca simultană și de schimbările locale neterminate; folosește un worktree sau un checkout dedicat unde e nevoie.
- [ ] Alege-ți rolul - champion, lead sau manager - fă săptămâna asta primul angajament din checklist-ul lui și pune-l în calendar.
- [ ] Controlează configurarea verificărilor obligatorii de pe server și a aprobării pentru zonele sensibile, inclusiv cine le poate ocoli. Testează răspunsul de blocare și comportamentul la eșec al fiecărui hook de politică; hook-urile locale oferă feedback suplimentar.
- [ ] Scrie fallback-ul pentru o săptămână de cădere a vendorului: cine livrează hotfix-ul fără agent.

---

### Mai departe

- **Template-uri:** [Anexa B.5](#template-b5), calendarul de 90 de zile cu traseul managerului; [B.6](#template-b6), contractul buclei exterioare; [B.4](#template-b4), fișa de punctare a kill signals.
- **Deep dive:** [Anexa D, Capitolul 9](#deep-dive-chapter-9) - filiația buclei exterioare și cronologia vendorilor, plus cele două feluri de hook-uri în întregime.
- **Pentru manageri:** Anexa A.
- **Surse:** Anexa C.

---

# Încheiere - Un mod de a gândi care supraviețuiește tool-urilor

Tool-urile pe care le-am numit vor arăta cu totul altfel până la următoarea ediție a manualului. Ce ai învățat nu sunt tool-urile. E un mod de a gândi care supraviețuiește tool-urilor, în trei controale.

**Arhitectura e controlul capabilității.** Componentele principale - context window, tool-uri, Permisiuni / Sandbox, skill-uri, plugin-uri, MCP, Memory, Effort, subagenți - plus harness-ul care le organizează. Majoritatea agenților folosiți în producție converg spre anatomia asta, pentru că o dictează natura muncii, nu vendorul, așa că poți evalua următorul agent parcurgând lista.

**Metoda e controlul workflow-ului.** Formularea limpede a muncii e schimbarea fundamentală. Bucla în șase faze e o implementare; AGENTS.md va exista sub alte nume, dar principiul e permanent: disciplină sub formă de cod, nu de tradiție orală.

**Realitatea e controlul adopției.** Kill signals sunt proprietăți ale codebase-urilor și ale echipelor, nu ale tool-urilor. Semaforul se aplică indiferent ce agent folosești trimestrul ăsta, iar champion, lead, manager e arcul pentru orice tranziție de tooling.

Dacă iei o singură practică, ia review-ul de arhitectură din Capitolul 7 ca diagnostic inițial: dovezi utile de analizat, nu un verdict dintr-o singură rulare. Dacă iei un singur framework, ia kill signals și semaforul din Capitolul 8; „nu”-ul contează la fel de mult ca „da”-ul. Dacă iei o singură orientare, investește în modul de a gândi, nu în tool.

Înapoi la cele nouă secunde: PocketOS a pierdut o bază de date de producție în timpul cât îți ia să citești propoziția asta. Fiecare strat al metodologiei exista în 2026 și ar fi putut fi pus în funcțiune în lunile dinainte. Niciunul nu era. Ăsta e golul pe care manualul încearcă să-l închidă: golul dintre metodologia care există și metodologia care chiar se aplică.

Să înțelegi problema devine mai important decât să scrii codul. Era adevărat când a programa însemna să perforezi cartele, când IDE-ul a înlocuit editorul de text și când coding-ul asistat de AI a trecut de la autocomplete la redactarea de cod; e adevărat și acum, când scrisul a rămas în seama agenților. Numele modelelor din ediția asta vor îmbătrâni, iar munca durabilă rămâne: înțelege problema, formulează munca, constrânge execuția, verifică rezultatul. Secvența asta e întreaga problemă de control - și n-a aparținut niciodată tool-urilor. Îți aparține ție.

Agenții scriu codul. Tu înțelegi problema. Asta e competența pe care n-o automatizează nimeni.

---

## Mulțumiri

Mulțumesc că ai citit.

Dacă ai întrebări, comentarii sau povești din propria adopție - reușite sau eșecuri - aș vrea să le aud. Următoarea ediție a manualului, peste doi-trei ani, va reflecta ce au învățat echipele între timp. Experiența ta e input-ul de care am cea mai mare nevoie.

-- Mihai Cvasnievschi

București, 2026

---

## Despre autor {#about-the-author}

Forma unui manual depinde de forma celui care îl scrie, așa că iat-o pe a mea.

Primele programe le-am scris în BASIC, în 1989. Cariera profesională mi-a început în 2000, ca IT Manager într-o companie de producție industrială; din 2001 am făcut inginerie software, iar până în 2023 am livrat .NET pentru clienți din industrii diverse, cu cod de producție în C, Java, JavaScript, Go și Python pe parcurs. Sunt întâi inginer și abia apoi consultant.

Cu machine learning m-am apucat prin 2013. La finalul lui 2015 am portat DarkNet și YOLO pe un headset XR și am început să construiesc aplicații AI profesionist; în 2023 m-am alăturat unei companii care construia primul SoC neuromorfic. Am folosit fiecare generație de asistent de coding, de la Visual Assist până la primul Copilot și la LLM-uri pentru cod din ziua în care a apărut ChatGPT. Nu mi-am construit propriul coding agent. I-am folosit însă pe majoritatea celor care există acum și am văzut multe echipe folosindu-i.

Nu sunt neutru pe subiectul ăsta. Cred că livrarea de software cu agenți e schimbarea cu cele mai mari consecințe din domeniul nostru de la apariția limbajelor de programare de nivel înalt încoace și că felul în care o adoptă majoritatea echipelor le face mai mult rău decât bine. Asta e a treia sau a patra iterație a framework-urilor astea; iterațiile de dinainte au greșit în feluri interesante.

<a id="contact"></a>
*Contact: [info@ship-it-with.ai](mailto:info@ship-it-with.ai) pentru discuții tehnice sau workshopuri personalizate, în persoană sau online, croite pe codebase-ul și pe constrângerile echipei tale. Mă găsești pe [LinkedIn](https://www.linkedin.com/in/mihaicvasnievschi/).*

---

## Changelog {#changelog}

Pagina asta urmărește actualizările semnificative ale manualului. Corecturile mărunte și ajustările de SEO nu sunt listate; footer-ul arată data ultimei actualizări.

### 2026-10-23 - Workflow dimensionat după task și dovezi

Ediția curentă pornește cu agentul nativ și controalele existente ale echipei. Cele șase faze descriu funcții, nu șase skill-uri, documente sau opriri obligatorii pentru aprobare. Planificarea, delegarea, review-ul și verificarea urmează neclaritatea, riscul și utilitatea observată; Superpowers rămâne opțional. O rundă editorială independentă a corectat afirmațiile despre acoperirea sandbox-ului și enforcement-ul prin hook-uri și CI, a separat Goals de verificările protejate de acceptare, a prezentat hărțile de arhitectură ca diagnostice provizorii și a calificat exemplele de durată și de rollout. Capitolul 6 tratează cele 200 de linii ca reper și actualizează încărcarea nativă AGENTS.md în Claude Code. Template-urile, sursele și ediția română urmează aceleași recomandări. Anexele C și D consemnează dovezile și limitele revizuite pe 23 octombrie; celelalte afirmații istorice își păstrează datele. Ediția integrală din septembrie rămâne înghețată.

### 2026-10-14 - Ediția scurtă

Manualul se citește acum în aproximativ o oră. Calea de lectură a scăzut de la circa 53.000 de cuvinte la circa 15.000, de la un Cuvânt înainte plus zece capitole la un Prolog plus nouă. Framework-urile nu s-au schimbat; s-au schimbat repetițiile, dovezile îngrămădite și meta-comentariile. Capitolele 1 și 2 s-au unit în „Ce este un agent”, cu cele nouă componente principale ca fișe. Guvernanța a devenit „Guardrails în cinci straturi”. Bucla în șase faze s-a împărțit în două: Capitolul 4 rulează bucla, Capitolul 5 deține Review și Verify. Igiena contextului s-a mutat lângă AGENTS.md, în Capitolul 6. Pattern-urile brownfield și adopția s-au unit în „Lansarea în echipă”. Fiecare capitol are acum aceeași formă: un TL;DR, o poveste, un tabel sau o figură, „Când se strică”, „De făcut luni”, „Mai departe”. Studiile, benchmark-urile și detaliile datate ale vendorilor au trecut într-o Anexă D nouă, Deep dives, organizată pe capitole; Anexa A a devenit „Pentru manageri” (costuri, rolul managerului, cazul cu 20 de ingineri); Anexa B a primit checklist-ul de verificare a plugin-urilor și exercițiile; Anexa C e neschimbată, în afară de trimiterile spre noile locații. URL-urile vechi ale capitolelor redirecționează spre noile lor locuri. Ediția din septembrie 2026, integrală, rămâne disponibilă la [/ro/full/](/ro/full/).

### 2026-09-11 - Pasul de dovezi din septembrie: componenta principală Effort, controale pe review și verify, corecția AGENTS.md, B.9

Manualul, citit în oglindă cu dovezile din septembrie 2026: ghidurile pentru generația Claude 5 și GPT-5.6 / GPT-6, plus un șir de studii cu măsurători despre fișierele de context, scalarea multi-agent, reward hacking, preluarea criticilor și gestionarea contextului. Structura a rezistat; actualizările intră acolo unde dovezi noi schimbă o afirmație, o ascut sau umplu un gol. Capitolul 1 primește Effort ca a noua componentă principală - butonul de raționament și raționamentul păstrat -, pentru că trece acum testul convergenței și a devenit cea mai mare pârghie de cost și de calitate; secțiunea de tool-uri primește prăbușirea la număr mare de tool-uri, încărcarea amânată, apelarea programatică a tool-urilor și schemele stricte; secțiunea despre context window ia cu o rezervă ferestrele din reclamă. Parcursul de inspecție din Capitolul 2 crește la nouă puncte. Capitolul 5: un gate „când împarți” pentru Execute (doar muncă descompozabilă, un singur scriitor per fișier, fork pe workeri și izolare pe revieweri), blocurile de autonomie și de scop ale vendorilor, reviewerul doi limitat la corectitudine și orb la reviewerul unu, rata de reparare în locul acurateței reviewerului, cu rundele plafonate, cifrele SpecBench și Cursor din spatele lui „indiciu, nu dovadă”, cu patru controale de verify (teste held-out, istoric și egress sigilate, hook pe editările de configurație, explicație înainte de fix), și igiena contextului cu măsurători (mascare în loc de rezumare, istoric append-only, listă de păstrat pentru compactor). Capitolul 6 poartă singura corecție cu dovezi direct împotriva textului: harta repository-ului iese din AGENTS.md și se mută în docs/, conform studiului ETH despre fișierele de context; jurnalul de greșeli primește mecanica de întreținere și pointerii la dovezi; plafonul de două sute de linii primește prăbușirea la optzeci de reguli și tăierea cu 80% a system prompt-ului; o linie de precedență intră în fișier. Capitolul 7 citează dovezile de retrieval din spatele cititului de cod în locul indexării. Capitolul 8 numește instrucțiunile scrise pentru modelul anterior ca semnal soft. Condiția de oprire din Capitolul 9 numește /goal și Codex Goals. Anexa A primește pârghiile structurale de cost; Anexa B primește B.9, checklist-ul de migrare între modele (numărul de template-uri e acum nouă), cu B.2, B.3 și B.7 actualizate; Anexa C primește un grup de douăzeci și șapte de surse despre harness și migrarea între modele. Nota despre afirmațiile datate, mutată la septembrie 2026.

### 2026-07-27 - Găsește-ți necunoscutele (Capitolul 4 + Capitolul 5 + B.8)

Teza bottleneck-ului de formulare din Capitolul 4 primește cea mai puternică confirmare externă de până acum: ghidul de teren al Anthropic din iulie 2026 pentru lucrul cu Fable 5, al cărui autor descrie modelul de frontieră ca având ca bottleneck „capacitatea mea de a-i clarifica necunoscutele” - inginerii vendorului descriu acum frontiera exact cum o descrie Capitolul 4. Framework-ul cu patru cadrane de necunoscute din ghid e mapat pe mașinăria manualului (fișierul de instrucțiuni de echipă drenează unknown knowns, nota de research scoate la suprafață known unknowns), iar Capitolul 5 câștigă trei tehnici pentru cadranul la care nu ajunge niciun checklist. În Research: un blind spot pass înaintea research-ului propriu-zis, când task-ul e în afara domeniului tău, împerecheat cu declararea nivelului de experiență, ca presupunerile agentului să iasă la suprafață unde le poți respinge. În Execute: un fișier de note de implementare care consemnează fiecare deviere de la plan în momentul în care se întâmplă - lista de mărturisiri a reviewerului de spec și antidotul pentru drift-ul de rezumate al orchestratorului. La închiderea citirii diff-ului de agent: un quiz înainte de aprobare - dacă nu poți răspunde ce se întâmplă la margini, ăla era rubber-stamping, nu review, iar degradarea din pattern-ul patru tocmai a devenit măsurabilă. One-pager-ul B.8 primește blocul de quiz; intrare nouă în Anexa C pentru ghidul de teren.

### 2026-07-17 - Pasul de actualitate și corecturi din iulie

Un fact-check în profunzime al fiecărei afirmații datate, față de ce arată public în iulie 2026, cu verificare adversarială pe fiecare constatare. Corecturi: povestea post-mortem-ului din 23 aprilie e re-sursată - regresiile recunoscute de Anthropic sunt 4 martie (effort), 26 martie (caching) și 16 aprilie (plafonul de verbozitate), în timp ce atribuirea către adaptive thinking din februarie și auditul pe 6.852 de sesiuni îi aparțin Stellei Laurenzo de la AMD, publicate pe 6 aprilie, înaintea post-mortem-ului; jumătatea scrisă de agent a componentei principale Memory urcă de la semnal de pionierat la convergență deplină (GitHub Copilot Memory a precedat Auto Memory; Codex CLI a urmat în aprilie); Dreaming e corectat ca feature la nivel de platformă, nu o comandă de CLI livrată; subagenții paraleli din Codex, corectați de la opt la cei șase documentați; sistemul de subagenți din Cursor, re-datat la 2.4; repository-ul opencode, actualizat la anomalyco/opencode; adoptarea ralph-wiggum, re-datată în noiembrie 2025; corecturi mai mici de date (patch-ul Adversa, /loop). Actualitate: ferestrele de context (un milion de tokeni e acum gama medie), avertismentul propriu al METR din februarie 2026, telemetria care converge ca OpenTelemetry, tranziția Gemini CLI către Antigravity CLI. Adăugiri: soft-delete-ul de 48 de ore și accesul de agent cu scop limitat introduse de Railway după PocketOS (Capitolul 3), suspendarea tier-ului flagship din iunie 2026 ca exemplu de săptămână proastă a vendorului (Capitolul 10), CVE-urile de sandbox-escape DuneSlide ca mențiune onestă pe stratul doi (Capitolul 3), vectorul de injecție cu payload împărțit prin DNS TXT și mitigarea `sandbox.credentials`. Nota despre afirmațiile datate, actualizată la iulie 2026.

### 2026-07-06 - Diagrame SVG și corpuri de figuri localizate

Trei figuri trec de la layout-uri cu carduri la SVG adaptat temei: bucla în șase faze își desenează acum topologia reală (șase noduri, săgeți și cele două rute de eșec înapoi la Plan), cele cinci straturi de guvernanță se afișează ca un zid de apărare în adâncime, iar arcul de 90 de zile devine o cronologie cu etichete de rol. Toate cele cinci figuri au acum corpuri localizate în ediția română (înainte se traduceau doar legendele), iar etichetele învechite CLAUDE.md din figura arcului au fost corectate în AGENTS.md, ca să corespundă textului. Doar prezentare; conținutul figurilor rămâne neschimbat.

### 2026-07-05 - Cum faci review pe un diff de agent (Capitolul 5 + Anexa B.8)

Faza de Review din Capitolul 5 capătă jumătatea ei umană, inserată după cei doi revieweri-agent și înainte de Verify - citirea pe care doar un om o poate face, pe care cartea o invocase drept pragul minim de review uman fără s-o predea vreodată. Pornește de la de ce un diff de agent eșuează diferit ca natură, nu ca grad: un diff de om eșuează la execuție și vânezi greșeala linie cu linie, în timp ce un diff de agent compilează, trece de lint și se citește idiomatic, eșuând în schimb la intenție și context. Așa că ordinea de citire se inversează în cinci pași - diff-stat-ul raportat la plan înainte de orice cod, testele citite pentru ce afirmă, granițele despre care echipa are reguli, un grep pe fiecare nume nou pe care diff-ul îl introduce, și abia apoi linie cu linie, unde minutele merg către corectitudinea de business și potrivirea arhitecturală. Linia de calibrare o ancorează: fluența nu e corectitudine, iar un bug de agent arată ca acel cod pe care un inginer bun l-ar scrie pentru un task ușor diferit. Anexă nouă: B.8, one-pager-ul cu ordinea de citire a unui diff de agent (numărul de template-uri ajunge acum la opt). Pattern-ul patru din Capitolul 9 capătă o trimitere înapoi de încheiere, care numește ordinea asta de citire drept pragul minim de review uman făcut concret.

### 2026-07-05 - Igiena contextului (Capitolul 5 + Anexa B.7)

Capitolul 5 capătă o secțiune de igienă a contextului, inserată după paragraful de vocabular inner/outer loop, care predă meșteșugul zilnic pe care cartea îl numise, dar nu-l predase niciodată - fereastra e memoria de lucru a agentului, iar tot ce e încărcat în ea concurează cu raționamentul. Numește cele patru semne ale contaminării (agentul răspunde din nou la o întrebare deja rezolvată, citează o versiune învechită a unui fișier pe care l-a editat, uită o constrângere pe care o respecta sau scade în calitatea editărilor târziu într-o sesiune lungă), disciplina graniței dintre sesiuni - o unitate de muncă per sesiune, cu stare durabilă recitită din repository - și compactarea ca hand-off, nu continuare, unde tot ce nu e scris într-un fișier până atunci s-a pierdut. Anexă nouă: B.7, one-pager-ul igienei contextului (numărul de template-uri ajunge acum la șapte). Secțiunea despre context window din Capitolul 1 capătă o trimitere înainte, de o frază, către noua secțiune.

### 2026-07-05 - Exemplul lucrat din Anexa A

Anexa A capătă o trecere lucrată prin propria ei grilă, închizând singurul gol dintr-o carte construită pe exemple lucrate: secțiunea de costuri nu avea niciun număr. Noua subsecțiune ia proiectul de 20 de ingineri din servicii financiare din sidebar-ul managerului (Capitolul 10) și îl trece prin anexă - 13 seat-uri Team plus 7 seat-uri Pro, lista TCO cu patru categorii și euristica de încadrare - folosind cifrele operaționale publicate ale proiectului (41% dintre PR-urile merged atinse de agent, cycle time cu 28% sub baseline, defecte neschimbate) drept ancoră de valoare. Tarifele de pe partea de cost sunt marcate ca numere rotunde ilustrative, nu cotații, în acord cu poziția anexei că prețurile concrete se învechesc trimestrial. Concluzia cinstită încape într-un tabel mic: prețul de listă e cea mai mică linie, iar categoriile de timp uman o pun în umbră. Încheierea ține granița din Capitolul 10: managerul apără cifra operațională, nu un ROI proiectat.

### 2026-07-05 - Două feluri de hook-uri (Capitolul 9, pattern-ul trei)

Pattern-ul trei din Capitolul 9 se extinde de la regulile hookify la două feluri de hook-uri: hook-ul pre-tool-use al agentului (hookify) și hook-ul de git pre-commit/pre-push. Materialul nou leagă gate-ul de git de faptul că agentul e doar încă un autor cu acces de scriere: un gate determinist de commit/push i se aplică gratis, iar portița `--no-verify` e închisă cu o regulă hookify de deny. Trage și linia cinstită - hook-urile locale sunt feedback rapid, în timp ce aceleași verificări în CI sunt gate-ul pe care nu-l poți sări de pe laptop, adică gate-ul din pattern-ul opt pe care agentul nu-l poate edita. Recap-ul, încheierea și caseta de artefact actualizate; numărul de pattern-uri rămâne opt.

### 2026-06-11 - Orchestrare scriptată a subagenților (`/workflows`)

Secțiunea despre subagenți din Capitolul 1 capătă un paragraf despre orchestrarea programatică: /workflows din Claude Code, care pune agentul să scrie un script determinist ce trimite subagenți pe faze, cu fan-out în paralel sau prin pipeline și hand-off-uri validate prin schemă, cu un gate de verificare. Încadrat pe linia tezei cărții - nu o componentă principală nouă, ci o comoditate la nivel de harness peste componenta principală subagent, unde determinismul e singura diferență reală față de dispatch-ul condus de model (de pildă, un plugin în stil Superpowers). Datat la mijlocul lui 2026.

### 2026-06-10 - Bucla exterioară (pattern-ul opt)

Capitolul 9 capătă un al optulea pattern, care acoperă trendul outer-loop - re-invocarea agentului la interval, după un program sau dintr-un queue, până când o condiție e îndeplinită. Pattern-ul trasează filiația (buclele cu auto-evaluare din 2023; Ralph Wiggum la mijlocul lui 2025; valul de agenți de background și programați lansați de vendori la finalul lui 2025; bucla ca suprafață de prim rang până în primăvara lui 2026) și instalează controalele: un contract de buclă în cinci linii, testul de eligibilitate pentru buclă, patru kill signals de buclă și pragul minim al review-ului de dimineață. Capitolul 5 primește paragraful de vocabular inner/outer loop. Anexă nouă: B.6, one-pager-ul cu contractul buclei exterioare (numărul de template-uri ajunge la șase). Cinci intrări noi în Anexa C, sub un grup nou de surse despre outer loop și autonomie. Nota despre afirmațiile datate, actualizată la iunie 2026.

### 2026-05-27 - Componenta principală Permisiuni / Sandbox

Permisiuni / Sandbox a fost promovat la rang de componentă principală numită - al treilea loc în inventar, după Context window și Tools. Două jumătăți, ca la Memory: stratul de decizie la nivel de agent (Allow / Ask / Deny + modul auto) și impunerea la nivel de OS (Seatbelt / bubblewrap / token-uri restricționate / WSL2). Nota de vocabular din Capitolul 1 a fost rescrisă ca să numească testul de convergență care a promovat această componentă principală, lăsând telemetria ca strat de control. Capitolul 3 primește un paragraf de încadrare care leagă trei dintre cele cinci straturi ale lui (permisiuni, hook-uri, sandbox) de suprafețele de configurare ale noii componente principale; narațiunea apărării în adâncime pe cinci straturi rămâne neschimbată. Numărul punctelor de inspecție din Capitolul 2 a scăzut de la nouă la opt (cele două jumătăți ale P/S s-au comasat într-una singură). Diagrama, actualizată la 8 celule. Trei intrări noi în Anexa C documentează implementările din Claude Code / Codex / opencode.

### 2026-05-27 - Changelog + footer cu data ultimei actualizări

Am adăugat pagina asta și o linie „Last updated &lt;date&gt;” în footer, plus un link spre Changelog în rândul de contact. Intenția: cititorii care revin să poată vedea ce s-a mișcat de la ultima vizită fără să compare capitolele diff cu diff.

### 2026-05-27 - Componenta principală Memory + încadrarea ca listă deschisă

Memory a fost promovat la rang de componentă principală numită în toată cartea; Capitolul 1 a fost reintitulat „Componentele principale”, iar argumentul structural rescris ca „componente principale numite + componenta principală recursivă (subagenții)”. Am renunțat peste tot la numărătoarea închisă de „șase componente principale”; lista e acum încadrată ca listă deschisă. Noua secțiune Memory acoperă două jumătăți - memoria definită manual (AGENTS.md/CLAUDE.md, agnostică față de agent) și sistemul de memorie automată (Auto Memory, Auto Dream - deocamdată cu Claude Code în frunte). Diagrama, actualizată. Capitolul 6 primește o introducere de un paragraf care ancorează AGENTS.md ca strat de memorie partajabil în echipă. Trei intrări noi în Anexa C documentează afirmațiile despre Memory.

### 2026-05-27 - Trecere de SEO: URL-uri per capitol

Fiecare capitol și fiecare anexă are acum URL propriu (20 de pagini în total). Bookmark-urile vechi de tip `/#chapter-N` redirecționează. Fiecare pagină a primit titlu unic, meta description, URL canonic, navigare prev/next și date structurate `TechArticle` + `BreadcrumbList`. Hero-ul a căpătat un rând de CTA cu trei butoane. Schema a fost ridicată de la `Article` la `Book` + `Organization` + `FAQPage`. Rescrierea ancorelor între secțiuni, reducerea linkurilor către AGENTS.md, modul `/read/` pentru experiența de citire pe o singură pagină. Pagină 404 proprie, `llms.txt` pentru motoarele de răspuns AI, `cover.webp`.

### 2026-05-26 - Șlefuire după runda de feedback

Trecere cu reviewer extern: corectată nepotrivirea capitol-parte din cuprins, eliminată numerotarea figurilor (stil de manual web), componente noi de callout pentru Notă despre surse și Artefact, cu variante light + dark, biografia din cuvântul înainte scurtată la patru fraze și versiunea completă mutată într-o secțiune nouă Despre autor, hero-ul a primit un dek cu teza controlului, linkurile către AGENTS.md reduse la cel mult unul per capitol, ancore de copy-link `¶` per secțiune, strângerea stivei de callout-uri.

### 2026-05-26 - Prima versiune publică

Manualul publicat la ship-it-with.ai. Zece capitole în trei părți (Arhitectura, Metoda, Realitatea), trei anexe, plus cuvânt înainte, prolog și încheiere.

---

---

## Anexa A - Pentru manageri

*Pentru engineering managerul, directorul sau CTO-ul care deține bugetul, angajările și procurement-ul - și pentru championul care trebuie să le pună un caz pe masă. Citește mai întâi Capitolele 2, 8 și 9 (guardrails, pregătirea, rollout-ul). Anexa asta le conține pe restul: rolul tău, decizia de portofoliu, o echipă lucrată pas cu pas și banii. E făcută să poată fi trimisă mai departe de sine stătătoare.*

---

### Treaba ta în cele 90 de zile

**Managerul nu rulează agentul. Managerul apără trei granițe.**

Faza managerului acoperă zilele 61-90, după ce championul a pus practica pe picioare și lead-ul a consolidat-o (arcul e în Capitolul 9). Are trei centre de greutate:

- **Procurement.** Închide decizia de licențiere, ca echipa să nu rămână pe veci pe seat-uri individuale.
- **Guvernanță.** Semnează postura de securitate pe care o redactează championul.
- **Raportare.** Tradu rezultatele operaționale în termeni pe care leadership-ul îi va finanța.

Nimic din toate astea nu cere să scrii cod. Toate cer să ții linia: între datele operaționale și promisiunile de ROI, între tooling potrivit cu utilizarea și uniformitate impusă, între protejarea echipei de metrici premature și cererea de dovezi că munca dă roade.

Tot tu deții deciziile pe care nu le poate lua nimeni altcineva: angajarea criptografului pentru o problemă de la semnalul șase, finanțarea unui trimestru ca să muți un proiect galben la verde, cumpărarea de tooling sau servicii suplimentare.

**Ce nu faci:**

- Nu vâna metrici de productivitate per inginer în luna a doua.
- Nu promite un ROI pe trei ani înainte ca dashboard-ul să aibă un trimestru de date.
- Nu autoriza benchmark-uri între vendori înainte ca echipa să fi livrat suficient cât să definească ce compară.

Stabilește bugetul pilotului și criteriile de succes înainte de rollout. Urmărește rezultatele operaționale de la început, fără clasamente individuale premature sau promisiuni de ROI nesusținute. Când cifra operațională e solidă, apără-o; argumentul de venituri lasă-l în seama celui care deține veniturile. Exemplul de 90 de zile trece spre responsabilitate operațională continuă, dar hand-off-ul trebuie să urmeze dovezile și pregătirea echipei.

Fără un manager implicat, costul apare în altă parte: procurement-ul stă blocat două luni așteptând avizul de la legal, bugetul pentru documentare nu se alocă niciodată, proiectele galbene rămân galbene. Clasificarea făcută de lead era corectă. N-a avut cumpărător.

---

### Care codebase-uri acum, care mai târziu, care niciodată

**Aplică semaforul per proiect, niciodată per companie.** Întrebarea nu e „e compania asta pregătită pentru AI”. Întrebarea e „care dintre codebase-urile noastre e pregătit azi, și ce ar fi nevoie ca celelalte să treacă într-o altă culoare”. Capitolul 8 conține cele opt kill signals și punctarea. Partea pe care acționezi tu e sortarea.

| Culoare | Semnale | Mod | Decizia ta |
|---|---|---|---|
| Verde | 0-1 | Condus de agent | **Acum.** Începe de aici, ca echipa să capete experiență și încredere. |
| Galben | 2-3 | Condus de om, cu sprijinul agentului | **Mai târziu.** Finanțează reparațiile structurale care îl mută spre verde într-un trimestru sau două. |
| Roșu | 4+ | Repară întâi codebase-ul | **Niciodată, în starea actuală.** Reformează-l sau scoate-l din uz pe un orizont mai lung; agentul rămâne în afara lui până se închid semnalele. |

Majoritatea companiilor au un mix, iar mixul e planul. Când leadership-ul a decis că „adoptăm AI”, tentația e să pui agentul oricum pe un codebase roșu. Rezistă: tentația asta produce poveștile de adopție eșuată care murdăresc tot domeniul.

Două reguli de știut înainte să citești un scorecard:

- **Semnalul șase cântărește mai greu decât celelalte.** Se numără împreună cu ele și, în același timp, suprascrie numărătoarea: un codebase cu zero pe semnalele unu-cinci, dar cu da pe semnalul șase, e tot roșu pentru munca respectivă. Soluția e structurală: construiești capacitatea, te asociezi cu cineva care o are sau ții agentul departe de zonele respective.
- **Numără după intensitate, nu după prezență.** „Testele există, dar sunt parțiale” înseamnă jumătate de semnal. Un codebase care tehnic are teste, dar acestea acoperă 10% din cod și sunt de calitate slabă, nu e verde.

Cere-i lead-ului un scorecard cu un rând per proiect, pe primele cinci proiecte active: semnalele punctate, culoarea, modul recomandat (condus de agent, condus de om, repară întâi). Durează cam două ore. Pentru un proiect galben, cere cele două-trei reparații structurale care l-ar duce la verde. Pentru unul roșu, întreabă dacă răspunsul e investiție, înlocuire sau scoatere din uz. Uneori întrebarea ține de strategie, nu de codebase: un fork customizat de la un vendor, cu cuplare severă cu upstream-ul, ridică întrebarea dacă stratul custom ar trebui să existe deloc.

---

### O echipă, săptămână cu săptămână

**Douăzeci de ingineri într-o firmă reglementată de servicii financiare.** Managerul conduce funcția de inginerie și raportează unui CTO care susține inițiativa, dar e atent la costuri. Board-ul vrea un update de o pagină, la finalul trimestrului trei, despre investiția în AI. Championul a dus zilele 1-30, lead-ul a consolidat practica în zilele 31-60; managerul preia de la ziua 61.

| Săptămâna | Ce apare | Ce face managerul |
|---|---|---|
| 1 (zilele 61-67) | Un dashboard cu trei metrici: procentul de PR-uri merged care ating cod generat de agent; cycle time-ul și rata de defecte pe acel set, fiecare comparate cu trimestrul anterior. | Verifică dacă metricile sunt reale. Nu încearcă să le crească. |
| 2 (zilele 68-74) | Procurement-ul întreabă: seat-uri sau enterprise. Echipa e pe seat-uri Pro individuale. | Alege nivelul Team pentru 13 din cei 20 de ingineri și seat-uri Pro pentru cei 7 care folosesc rar agentul. Apără decizia: scopul e o cheltuială ținută în frâu, potrivită cu utilizarea, nu tooling uniform. |
| 3 (zilele 75-81) | Comitetul de securitate a citit despre clasa de injecție prin fișiere de configurare dezvăluită de Check Point Research la începutul lui 2026 (Anexa C) și vrea o postură de guvernanță scrisă. | Editează și semnează un document de o pagină care numește patru puncte de control: hook-uri, sandbox, vault de secrete, telemetrie (straturile sunt în Capitolul 2). Îl scrie championul. |
| 4 (zilele 82-88) | Cererea board-ului. | Trimite două fraze și un singur număr. Nu promite nicio cifră de venituri. |

Cifrele din spatele săptămânii 1: 41% dintre PR-urile merged atinse de agent în luna a doua, cycle time pe ele cu 28% sub baseline-ul dinainte de agent, rata de defecte în marja de zgomot a baseline-ului.

Update-ul pentru board, integral: *„Avem douăzeci de ingineri pe livrare asistată de agenți. Cycle time-ul pe PR-urile atinse de agent e cu 28% mai mic decât baseline-ul, fără nicio schimbare măsurabilă în rata de defecte. Continuăm să evaluăm extinderea pe parcursul trimestrului următor.”* Managerul apără cifra operațională și lasă argumentul de venituri în seama CTO-ului.

Ziua 90: înapoi la operațiunile curente. Dashboard-ul rămâne; championul și lead-ul își păstrează rolurile.

---

### Cât costă programarea cu agenți? {#how-much-does-it-cost}

**Prețul de listă e cea mai mică linie, și cea despre care întreabă toată lumea prima dată.** Prețurile se schimbă în fiecare trimestru; grila de calcul nu. Pune-ți propriile numere în ea.

Trei modele de preț domină piața:

- **Per-seat.** Tarif fix per inginer pe lună. Predictibil; ieftin pentru utilizatorii ocazionali, scump pentru power user-ii care rulează agentul toată ziua.
- **Per-token.** Plătești pentru ce citește și ce scrie agentul. Corect pentru utilizatorii ocazionali; nimicitor pentru inginerul care rulează trei sesiuni în paralel, zece ore în șir.
- **Enterprise.** Angajament anual negociat, care împachetează seat-uri, o alocare de tokeni și suprafața de conformitate (Zero Data Retention, acces la log-urile de audit, capacitate dedicată, SSO, BAA-uri semnate). Amortizează ambele extreme și adaugă ce cer industriile reglementate.

**Euristica de încadrare.** Costul per inginer are ca plafon ce ar fi cheltuit oricum echipa pe tooling similar (licențe de IDE, platforme de code intelligence, abonamente de coding asistat de AI), plus o fracțiune din valoarea orelor economisite pe săptămână de un inginer senior. Dacă costul lunar total depășește cu mult plafonul ăsta, calculul are șanse mici să iasă, indiferent de vendor. Dacă se încadrează confortabil în el, are șanse mici să nu iasă. Pragul de break-even vine repede de îndată ce agentul economisește chiar și câteva ore pe lună per inginer.

**Ce nu apare în ofertă.** Patru linii domină totalul real:

| Linie | Ce acoperă | Echipa de 20 de ingineri (ilustrativ) |
|---|---|---|
| Seat-uri (prețul de listă) | Oferta vendorului | ~$530/lună, ~$6.400/an, recurent |
| Integrare | Skill-uri custom, hook-uri, servere MCP pentru sistemele interne | Câteva săptămâni de engineering, o singură dată |
| Scrierea skill-urilor | Întreținerea AGENTS.md, actualizarea skill-urilor pe măsură ce codebase-ul evoluează | Câteva ore per inginer pe lună, plus trimestrul part-time al championului |
| Review | Review-ul output-ului agentului: mai puțin per schimbare decât la codul scris de mână, în majoritatea cazurilor, dar niciodată zero | Concentrat pe reviewerii seniori, continuu |
| Guvernanță | Evaluarea de securitate prin CISO, addendum-ul de Zero Data Retention, ciclul de achiziții, audit logging, monitorizarea riscului de vendor | O săptămână până la un trimestru, concentrat la început într-o firmă reglementată, o singură dată |

---

### Pârghiile structurale {#cost-levers}

**Prețurile se învechesc; pârghiile care mișcă linia de tokeni, nu.** Pe planurile per token, acolo stau economiile din anul al doilea.

- **Nivelul de effort.** Componenta principală din Capitolul 1 și cel mai mare buton de cost pe care îl ai. Setează-l per fază, fă-i sweep per model și nu-l lăsa niciodată pe default pentru toată bucla.
- **Layout de prompt cache-first.** Pune conținutul stabil la început (system prompt-ul, AGENTS.md, skill-urile încărcate) și conținutul per tură la sfârșit, ca prefixul să intre în cache. Pe 500 de sesiuni, la trei provideri, ordonarea asta singură a tăiat costul cu 41% până la 80%.
- **Încărcarea amânată a tool-urilor.** Un audit al unei sesiuni default de Claude Code a numărat cam 24k de tokeni de definiții și scheme de tool-uri înainte de primul cuvânt al utilizatorului. Amână schemele și plătește-le doar când un tool e folosit.
- **Mascare în loc de rezumare.** Golește rezultatele vechi de tool-uri în loc să rezumi istoricul. JetBrains a măsurat mascarea la un cost cu peste 50% mai mic decât rezumarea, cu o rată de rezolvare care a egalat-o sau a depășit-o.
- **Rutare pe tier-uri.** Rutează pe task, nu pe echipă: un model mai ieftin face munca, unul mai puternic stă de gardă. În pattern-ul „advisor” al Anthropic (aprilie 2026), Sonnet cu un advisor Opus a bătut Sonnet singur, la un cost per task cu 11,9% mai mic; Haiku cu advisorul a ieșit cu 85% mai ieftin decât Sonnet singur, dar a rămas în urmă cu 29% la scor. Potrivit pentru tier-urile mecanice ale buclei, greșit pentru research.

---

### Un exemplu lucrat {#a-worked-example}

**Aplică grila pe echipa de 20 de ingineri.** Cifrele sunt numere rotunde pentru aritmetică, nu cotații.

Întâi prețul de listă. 13 seat-uri Team la un preț ilustrativ de $30 plus 7 seat-uri Pro la $20 fac $530 pe lună, să zicem $6.400 pe an. Notează cifra asta: e cea mai mică de pe pagină.

Apoi liniile umane. Câteva săptămâni de engineering pentru integrare, la orice cost complet realist, acoperă singure prețul de listă pe primul an, o dată. Scrierea skill-urilor pe 20 de ingineri, plus trimestrul championului, se repetă și poate ajunge mai mare decât seat-urile însele. Review-ul cade pe cele mai scumpe ore ale tale, cele ale reviewerilor seniori. Guvernanța într-o firmă reglementată înseamnă o săptămână până la un trimestru de muncă de securitate, achiziții și audit logging înainte să fie facturat vreun seat.

Partea de valoare folosește euristica de încadrare în sens invers. La un cost complet ilustrativ de $100 pe oră, un seat de $30 e acoperit când agentul îi economisește inginerului cam douăzeci de minute pe toată luna; cu câteva ore economisite, pragul e depășit de departe. Dar calculul ăsta pe dosul plicului nu e ce a justificat cheltuiala. Cifra operațională a justificat-o: 41% dintre PR-urile merged atinse de agent, cycle time cu 28% sub baseline, rata de defecte neschimbată. Ore economisite și măsurate, nu dolari proiectați.

**Disciplina:** cele patru linii ascunse domină, iar cele umane pun în umbră matematica seat-urilor. Apără în fața board-ului cifra operațională, nu un ROI proiectat pe care dashboard-ul încă nu-l poate susține. Intră în discuția de achiziții cu propriile numere, puse în structura asta. Prețurile se schimbă; aritmetica asta, nu.

---

**Mai departe:** [Anexa B.4](#template-b4) (fișa de punctare a kill signals), [Anexa B.5](#template-b5) (calendarul de 90 de zile), Anexa C (surse).

---

## Anexa B - Template-uri

Unsprezece template-uri și exerciții de copiat și lipit. Toate sunt puncte de plecare; adaptează-le pentru echipa ta.

Template-urile B.1 și B.2 rămân integral în engleză: sunt artefacte pe care le consumă agentul, iar prompturile se scriu în engleză.

### B.1 Promptul de architecture review {#template-b1}

```
Analyze the architecture of this codebase. Produce a structured architecture review document covering:

1. Purpose. What does this service do? Who uses it? What business problem does it solve?
2. Top-level structure. Major modules, packages, or folders. One paragraph per major component.
3. Data model. Primary entities, relationships, persistence. Cite specific files and line numbers.
4. Request flows. For the three most important external entry points, trace from entry to persistence. Cite files and lines at each step.
5. Cross-cutting concerns. Authentication, authorization, logging, error handling, configuration. Where do they live?
6. Dependencies. External services, databases, message brokers, third-party APIs.
7. Test posture. Test structure, coverage, gaps.
8. Build and deployment. Cite the configuration files.
9. Risks and unknowns. Fragile code, inconsistent conventions, deprecated dependencies, unresolved patterns.

Cite specific files and line numbers throughout. Where the codebase is ambiguous, say so explicitly. Where you encounter patterns the team should formalize, suggest the convention.
```

### B.2 Scheletul AGENTS.md {#template-b2}

Template-ul rămâne în engleză pentru agent. Folosește numele și regulile de încărcare ale harness-ului: [AGENTS.md](https://agents.md/) sau CLAUDE.md, cu import explicit dacă ai nevoie de ambele. Pornește cu un fișier scurt. Folosește circa 200 de linii ca reper pentru reducerea conținutului, nu ca țintă sau limită universală. Linia de precedență clarifică relația cu cererea și skill-urile, în limitele instrucțiunilor cu prioritate mai mare ale agentului; nu înlocuiește controalele de securitate.

```
# AGENTS.md

Precedence: in a conflict, the task prompt wins over this file; this file wins over any skill.

## Forbidden patterns
- Never construct SQL by string concatenation. Use bound parameters. (Reason: SQL injection.)
- Never roll your own cryptography. Use the team's approved crypto wrapper. (Reason: AES-CBC with hardcoded IV shipped to production in 2024; we are not doing that again.)
- Never modify migration history. Migrations are append-only.

## Mistake journal
- 2026-03-03: agent generated JPQL query that bypassed the multi-tenant filter. Fix: queries extend MultiTenantQueryBuilder, which enforces tenant filtering. Evidence: <commit or incident link>

## Conventions
- Constructor injection only, not field injection.
- @Transactional only on service methods that mutate state.

## Build and test
- Build: mvn clean verify
- Run tests: mvn test

## Where the map lives
- Repository layout and module map: docs/architecture.md (read before touching an unfamiliar module)

## Domain glossary
- "Customer" = end user. "Counterparty" = corporate client.
- "Transfer" = intra-bank or inter-bank. "Wire" = inter-bank only.
```

### B.3 Checklist-ul buclei în șase faze (one-pager) {#template-b3}

Funcțiile rămân; cât documentezi, delegi sau ceri aprobare depinde de task și de risc.

```
RESEARCH
  Citește contextul relevant și clarifică ce schimbă rezultatul.
  Câteva rânduri pot ajunge; 2-4 pagini sunt un exemplu pentru un feature complex.
PLAN
  Schimbare mică și clară: execuție directă, cu o verificare relevantă.
  Neclaritate sau dependențe: plan scurt cu rezultate, ordine și verificări.
  Risc mare: criterii explicite, gate-uri umane și review aprofundat.
  Pașii de 2-5 minute sunt o opțiune pentru muncă mecanică, nu o cotă.
EXECUTE
  Agentul principal poate executa singur. Deleagă muncă amplă, independentă și
  bine delimitată când beneficiul acoperă pornirea și transferul de context.
  Un singur scriitor pe zonele care se suprapun; dependențele se execută în ordine.
  Termină munca autorizată; fără confirmări repetate pentru acțiuni reversibile.
  Respectă scopul și permisiunile. Clarifică doar deciziile care depășesc mandatul
  sau schimbă material rezultatul. Consemnează deciziile importante.
REVIEW
  Verifică intenția, corectitudinea de business și calitatea implementării.
  Reviewer independent cu context proaspăt dacă riscul, modelul sau rezultatele
  îl justifică; nu automat doi agenți în secvență.
  Acceptă sau respinge motivat constatările; limitează rundele la probleme reale.
VERIFY
  Rulează verificările relevante. Pentru bug-uri de comportament, test de regresie
  unde e fezabil. Nu inventa teste permanente pentru editări fără impact relevant.
  Nu slăbi testele sau CI-ul ca să obții verde; schimbările legitime se autorizează
  și se revizuiesc. Explică eșecul înainte de fix.
  Teste held-out, istoric sigilat și egress oprit: pentru evaluări controlate sau
  cerințe ridicate de asigurare, nu implicit pentru fiecare PR.
  Raportează dovezile și limitele. Nu repeta o suită validă fără un motiv nou.
SHIP
  Commit și PR structurate; revieweri conform CODEOWNERS; procesul normal al echipei.
  Păstrează aprobările umane, de securitate și de livrare cerute de proiect.
```

### B.4 Fișa de punctare a kill signals {#template-b4}

```
Punctează fiecare semnal cu 0 (absent), 0.5 (parțial, între repere) sau 1 (prezent).

1 Fără teste
  0    > 70% coverage ȘI rulează la fiecare commit
  0.5  30-70% coverage, sau nu rulează de rutină
  1    < 30% coverage sau nicio suită
2 Fără documentație
  0    document de arhitectură la zi, decision records
  1    nicio privire de ansamblu; doar autorul știe
3 Cuplare strânsă
  0    granițe clare; modulele se schimbă izolat
  0.5  ceva cuplare; noii veniți se chinuie
  1    ghem; o editare sparge trei fișiere
4 Reguli de business împrăștiate
  0    o singură sursă de adevăr pentru fiecare regulă
  1    aceeași regulă în 3+ locuri, inconsistentă
5 Constrângeri de reglementare
  0    controale standard; mecanismul de audit face față
  0.5  domeniu reglementat, dar workflow-ul e pus la punct
  1    controale stricte, fără workflow integrat
6 Echipa nu poate evalua output-ul
  0    expertiză senior pentru fiecare domeniu
  0.5  expertiza există, dar e fragilă
  1    nu poate evalua output-ul într-un anumit domeniu
7 Potrivirea model-context
  0    limbaj/framework popular, cu amprentă publică
  1    DSL proprietar, framework intern
8 Viteza schimbării
  0    framework și dependențe stabile
  1    migrare majoră la jumătate

Adună și rotunjește la cel mai apropiat întreg.
  0-1 VERDE (condus de agent)  2-3 GALBEN (condus de om, cu sprijinul agentului)
  4+ ROȘU (repară întâi codebase-ul)
Semnalul 6 cântărește mai greu: un 1 înseamnă ROȘU pentru munca afectată,
indiferent de total.
```

### B.5 Calendarul de adopție în 90 de zile (one-pager) {#template-b5}

```
CHAMPION
  Săptămâna 1      instalează agentul; architecture review (B.1) pe un codebase familiar; dă-i commit
  Săptămâna 2      verifică instrucțiunile (B.2); adaugă doar ce cere pilotul
  Săptămânile 3-4  funcțiile din B.3 pe trei feature-uri; proces potrivit fiecăruia
  Luna 2           trei feature-uri medii; atrage alți ingineri în faze individuale
  Luna 3           predă rolul unui succesor; AGENTS.md e al echipei
LEAD
  Săptămâna 1      clasifică top 5 proiecte după cele 8 kill signals (B.4)
  Săptămânile 2-4  pentru fiecare culoare, scrie ce ar trebui să se schimbe ca să muți un proiect
  Luna 2           urmărește cycle time, rata de defecte, timpul de reviewer
  Luna 3           prezintă rezultate oneste
MANAGER
  Lunile 1-2       protejează echipa: fără metrici de productivitate per inginer, proiecții de ROI sau benchmark-uri de vendor deocamdată
  Zilele 61-67     preia hand-off-ul; verifică dacă metricile din dashboard sunt reale
  Zilele 68-74     închide decizia seat-vs-enterprise (Anexa A)
  Zilele 75-81     one-pager de guvernanță; championul schițează, managerul semnează
  Zilele 82-90     două fraze și un număr pentru leadership; cadență trimestrială
```

Arcul grassroots pentru echipele care nu au toate cele trei roluri: Capitolul 9.

### B.6 Contractul buclei exterioare (one-pager) {#template-b6}

```
Înainte de orice rulare nesupravegheată, completează fiecare linie. O linie goală înseamnă că bucla nu e gata.

MUNCA
  Queue: ______ (în repo; câte o unitate mică, similară, reversibilă per element)
  Eligibilitate: codebase VERDE (scor B.4 0-1) / fiecare unitate verificabilă de mașină / fiecare unitate revertibilă
CONDIȚIA DE OPRIRE (evaluabilă de mașină; bucla se oprește singură)
  Done când: ______ (queue gol / suita verde / N unități gata de review)
  Buget: max ______ tokeni sau $______ sau ______ iterații sau ______ ore - ce se atinge primul
  Regula de eșec: aceeași unitate eșuează de două ori -> sari peste ea și marchează-o; trei unități sărite -> oprește tot
FIECARE ITERAȚIE
  Context proaspăt; starea se citește din queue + jurnalul din repo
  O unitate per iterație; termină-o sau notează în jurnal de ce nu - nimic aplicat pe jumătate
  Gate: ______ (teste / lint / typecheck / build), impus prin verificări obligatorii protejate
  Protejează schimbările evaluatorului, configurației și regulilor de politică de
  aprobarea unilaterală a agentului. Marker-ele de done avansează doar după ce trec
  verificările de încredere; raportul agentului singur nu e gate-ul de acceptare.
IZOLARE
  Worktree și branch propriu, niciodată branch-ul default
  Sandbox pornit; fără credențiale de producție; rețea oprită sau pe allowlist
REVIEW-UL DE DIMINEAȚĂ (pragul minim de review uman)
  Fiecare PR e citit pentru corectitudine de business și potrivire arhitecturală
  Verificarea de kill înainte de relansare: diff-uri care oscilează? buget consumat, dar queue-ul nu e mai scurt?
  același eșec a treia oară? gate-ul a fost atins? Orice „da” -> nu relansa. Citește jurnalul,
  repară întâi cauza.
```

### B.7 Igiena contextului (one-pager) {#template-b7}

```
ÎNCĂRCARE
  Doar context relevant pentru task. Pointere, nu payload-uri: numește fișierele,
  nu le lipi.
SESIUNE
  Păstrează deciziile, constrângerile, progresul și dovezile necesare reluării în
  formatul potrivit proiectului. Fără documente sau commit-uri de dragul procesului.
CONTAMINAT CÂND agentul
  răspunde din nou la o întrebare rezolvată deja; citează o versiune învechită a
  unui fișier pe care l-a editat; uită o constrângere pe care o respecta; se
  degradează târziu într-o sesiune lungă.
ATUNCI
  Verifică starea reală și corectează contextul. Dacă deriva continuă, reia într-o
  sesiune curată, cu starea necesară. Fă commit după practica repo-ului.
COMPACTARE (un hand-off, nu o continuare)
  Preferă mascarea output-urilor vechi de tool-uri în locul rezumării. Istoricul
  e append-only pe Fable 5.1: repornește, nu edita. Dă-i compactorului o listă
  de păstrat: planul, întrebările deschise, devierile, comenzile care au mers.
  Restul e pierdut.
```

### B.8 Ordinea de citire a unui diff de agent (one-pager) {#template-b8}

```
1 ÎNAINTE DE COD
  Diff-stat-ul raportat la cerere sau plan. Cere explicații pentru fișierele neașteptate.
2 ÎNTÂI TESTELE
  Citește ce afirmă, nu dacă trec. Un test scris pornind de la cod va fi de acord
  cu codul; aserțiunea trebuie să vină din intenție.
3 GRANIȚE
  Verifică regulile scrise ale echipei (pattern-urile interzise din AGENTS.md,
  convențiile de strat). O trecere de graniță arată curat într-un stil fluent.
4 NUME NOI
  Dă grep pe fiecare API, funcție sau cheie de config pe care n-o recunoști. Zero
  rezultate: numele s-ar putea să nu existe.
5 LINIE CU LINIE
  Abia acum, pentru corectitudine de business și potrivire arhitecturală. Folosește
  constatările verificărilor automate dacă le-ai rulat; nu presupune că au prins tot.
VERIFICARE OPȚIONALĂ A ÎNȚELEGERII
  Pentru muncă nefamiliară sau cu consecințe importante, întreabă despre edge case-uri,
  ownership și moduri de eșec dacă review-ul obișnuit nu a stabilit înțelegerea.
  Lămurește ce lipsește înainte de aprobare.
```

### B.9 Checklist-ul de migrare între modele (one-pager) {#template-b9}

Rulează-l după schimbări de model, harness sau skill și când rezultatele se înrăutățesc. Nu e al nouălea kill signal: verifici dacă procesul mai ajută în configurația curentă.

```
BASELINE
  Alege task-uri reprezentative și fixează criteriile de acceptare înainte de rulări.
  Include și cazuri în care skill-ul nu ar trebui să se declanșeze.
  Notează modelul, effort-ul, versiunea harness-ului și commit-ul de pornire.
COMPARAȚIE ON/OFF
  Pe fiecare model, compară agentul nativ cu skill-ul sau plugin-ul activat.
  Același effort și commit, sesiuni proaspete, aceleași permisiuni și criterii.
  Repetă suficient ca să vezi variația; nu alege doar cea mai bună rulare.
MĂSURĂTORI
  Corectitudine, regresii și cerințe îndeplinite, nu doar respectarea procesului.
  Consum facturat, inclusiv cache și subagenți; timp uman, rework și timp de ceas.
  Mai multe tool call-uri sau tokeni nu sunt automat mai multă valoare ori aceeași
  creștere procentuală a facturii.
PROMPTURI ȘI FIȘIERE DE INSTRUCȚIUNI
  Citește ghidul modelului. Testează retragerea instrucțiunilor redundante;
  păstrează constrângerile locale și controalele de securitate.
  Verifică prioritatea instrucțiunilor și încărcarea AGENTS.md / CLAUDE.md.
  Nu transfera automat regulile de delegare sau review de la alt model.
EFFORT, TOOL-URI ȘI ISTORIC
  Compară nivelurile de effort pe task-uri reprezentative; numele nu sunt echivalente.
  Verifică schemele de tool și regulile modelului pentru istoric și compactare.
DECIZIE
  Păstrează, simplifică, limitează la anumite task-uri sau dezactivează plugin-ul
  după rezultatele măsurate. Documentează versiunea și limitele comparației.
```

### B.10 Checklist-ul de verificare a plugin-urilor {#template-b10}

Marketplace-ul e o suprafață de supply chain, ca npm. Verifică fiecare plugin așa cum verifici o dependență.

```
MAINTAINER
  Activ în ultimele 90 de zile? Mai mult de un maintainer? Un palmares real?
SUPRAFAȚA DE PERMISIUNI
  Ce tool-uri, hook-uri, căi de fișiere și apeluri de rețea adaugă? Cererile
  largi au nevoie de o justificare.
REVIEW-UL DE COD ȘI DE WORKFLOW
  Inspectează versiunea instalată: instrucțiuni, trigger-e, hook-uri, scripturi și
  dependențe. Alege profunzimea review-ului după suprafață și risc, nu după un
  buget fix de douăzeci de minute. Evită instalările duplicate neintenționate.
BENEFICIU
  Compară on/off cu agentul nativ după B.9. Numele plugin-ului sau o verificare
  veche nu validează automat o versiune nouă. Păstrează-l unde ajută la rezultate.
DISCIPLINA DE UPDATE
  Fixează versiunea; fără auto-update. Citește diff-ul, rulează testele, livrează
  bump-ul ca pe o schimbare trecută prin review.
BLAST RADIUS
  În interiorul sandbox-ului e mărginit; un hook pe mașina developerului, în
  afara lui, nu e mărginit de nimic. Preferă varianta mărginită; altfel ridică
  ștacheta la tot ce e mai sus.
```

### B.11 Exerciții {#template-b11}

Exerciții care merg dincolo de lista „De făcut luni” a unui capitol. La Capitolele 2, 7 și 8, lista „De făcut luni” e chiar exercițiul: scorecard-ul pe cinci straturi, primul review de arhitectură, verificarea culorii din instinct.

**Capitolul 1 - Ce este un agent**

1. Clonează doi coding agents open source, deschide agentul tău în fiecare repo și pune întrebarea: "Walk this codebase and name the primitives - context window, tools, permissions / sandbox, skills, plugins, MCP, memory, effort, subagents. For each, name the file or module that implements it and rate it basic, intermediate, or advanced."
2. Salvează ambele răspunsuri într-un tabel pe două coloane. Componentele principale sunt aceleași; diferențele sunt alegeri de guvernanță.

**Capitolul 6 - AGENTS.md și contextul**

1. Alege un repository al cărui fișier de instrucțiuni e gol, învechit sau scris de cineva care a plecat.
2. Cere-i agentului tău: „Plimbă-te prin codebase-ul ăsta douăzeci de minute și spune-mi ce ar trebui să știe un coleg nou înainte să contribuie. Acoperă convențiile, disciplina de teste, comenzile de build și de deploy și tot ce e documentat parțial sau greșit.”
3. Schițează fișierul pornind de la B.2 și de la răspuns: concret pentru repo-ul ăsta, cu un pointer către docs/architecture.md în loc de o descriere a structurii, fără best practice generic.
4. Dă-i commit. Compară aceeași sarcină cu și fără instrucțiuni, pe același model și effort, de la același commit și în sesiuni proaspete. Stabilește întâi criteriile; compară modificarea verificată, consumul facturat și munca de corectare, nu doar cât de convingător sună răspunsul.
5. Dă-l unui coleg care n-a mai lucrat în repo; unde se încurcă el, acolo e următoarea ta modificare.

**Capitolul 4 - Cât workflow merită task-ul**

1. Alege un task mic și clar, unul cu dependențe și unul riscant sau nefamiliar. Definește criteriile înainte de rulare.
2. Compară agentul nativ cu un workflow opțional, după B.9; include un caz în care skill-ul ar trebui să rămână inactiv.
3. Notează calitatea, regresiile, consumul facturat cu cache și subagenți, timpul uman, rework-ul și timpul de ceas. Păstrează doar structura care își justifică costul; nu generaliza dintr-un singur rezultat.

---

## Anexa C - Surse și lecturi suplimentare

Anexa asta există pentru că fiecare afirmație din manual merită o sursă verificabilă, dacă vrei să mergi pe fir până la capăt. Am organizat intrările după afirmație, nu după sursă, ca să poți porni de la un pasaj din corpul cărții și să ajungi la dovezile din spatele lui. Intrările sunt grupate pe categorii (studii, incidente cunoscute, vulnerabilități cu versiuni de patch, documentația tool-urilor, marketplace-uri, surse pentru componenta principală Memory, surse pentru componenta principală Permisiuni / Sandbox, surse despre bucla exterioară și autonomie, surse despre harness și migrarea între modele), iar fiecare intrare are aceeași formă: afirmația, sursa, unde anume e folosită în manual și orice avertisment care merită știut.

### Studii și cercetare

**Afirmația:** Dezvoltatorii open-source experimentați care au folosit asistență AI pe repo-uri pe care le cunoșteau bine au fost cu 19% mai lenți decât aceiași dezvoltatori fără ea, deși estimaseră în prealabil că vor fi cu 24% mai rapizi - un decalaj de 43 de puncte între accelerarea așteptată și încetinirea măsurată, care a persistat în auto-evaluările lor chiar și după ce datele i-au contrazis.
**Sursa:** Becker et al., METR, "Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity," July 10, 2025. arXiv: [arxiv.org/abs/2507.09089](https://arxiv.org/abs/2507.09089). Articol: [metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/). Schimbarea de design a follow-up-ului: [metr.org/blog/2026-02-24-uplift-update/](https://metr.org/blog/2026-02-24-uplift-update/).
**Unde e folosită:** Anexa D, Capitolul 3 (studiul randomizat controlat METR).
**Atenție:** Studiul a testat asistența AI brută (Cursor + Claude), fără o variabilă pentru disciplina formulării. Interpretarea că disciplina de workflow e variabila lipsă îmi aparține mie, nu studiului. Follow-up-ul METR de la sfârșitul lui 2025 a suferit un selection bias sever (dezvoltatorii refuzau tot mai des randomizarea fără AI) și a produs doar estimări slabe; METR a anunțat un experiment reproiectat pe 24 februarie 2026 și avertizează împotriva extrapolării cifrei de 19% la tool-urile actuale.

---

### Incidente cunoscute

**Afirmația:** Pe 24 aprilie 2026, PocketOS și-a pierdut baza de date de producție în nouă secunde, când un agent Cursor bazat pe Claude Opus 4.6 a invocat Volume Delete de la Railway printr-un API token găsit pe parcurs, în timpul unei încercări de recuperare după o nepotrivire de credențiale. Backup-urile, stocate pe același volum, au fost distruse odată cu datele primare.
**Sursa:** Reported by DevOps.com ("When AI Goes Really, Really Wrong"), Business Insider (Jer Crane statement), and others. Anthropic's Claude Opus 4.6 system card (February 2026) describes the model that powered the agent.
**Unde e folosită:** Prolog (Nouă secunde) și Capitolul 2 (Guardrails în cinci straturi); Anexa D, Capitolul 2 (PocketOS: unde diferă relatările și ce au schimbat platformele).
**Atenție:** Cronologia recuperării diferă între relatările publice - restore-ul făcut de Railway ar fi durat ~30 de minute după ce Crane i-a contactat, în timp ce alte relatări vorbesc de ~30 de ore sau două zile până la restaurarea operațională completă. Folosesc incidentul pentru pattern-ul de guvernanță, nu ca reconstituire criminalistică exactă. Urmarea: pe 29 aprilie 2026, Railway a anunțat că toate ștergerile de volume și resurse - până atunci instantanee când erau invocate prin API - fac acum soft-delete cu o fereastră de recuperare de 48 de ore, alături de guardrails la nivel de workspace și acces de agent cu scop limitat ([blog.railway.com/p/your-ai-wants-to-nuke-your-database](https://blog.railway.com/p/your-ai-wants-to-nuke-your-database)).

---

**Afirmația:** La sfârșitul lui februarie 2026, Alexey Grigorev de la DataTalks.Club a pierdut doi ani și jumătate de infrastructură de cursuri, când Claude Code a lucrat pe un state file Terraform rămas în urmă și a rulat `terraform destroy` peste ce a interpretat el drept resurse orfane.
**Sursa:** Public account by Alexey Grigorev (DataTalks.Club), late February 2026.
**Unde e folosită:** Capitolul 2 (Guardrails în cinci straturi); Anexa D, Capitolul 2 (PocketOS: unde diferă relatările și ce au schimbat platformele).
**Atenție:** Pierderea de date a fost parțială; AWS a restaurat aproximativ 1,94 milioane de rânduri dintr-un snapshot, în circa o zi. Incidentul e documentat public, dar cu mai puțină acoperire decât PocketOS. Follow-up-ul lui Grigorev documentează întărirea adoptată după: delete protection și în Terraform, și în AWS, starea mutată în S3, review manual al fiecărui plan distructiv și un tier de suport AWS mai ridicat.

---

**Afirmația:** Post-mortem-ul tehnic al Anthropic din 23 aprilie 2026 („An update on recent Claude Code quality reports”) a recunoscut trei regresii: effort-ul implicit de reasoning coborât de la high la medium pe 4 martie (revenit pe 7 aprilie), un bug de caching din 26 martie care golea istoricul de raționament la fiecare tur în loc de o dată pe oră de inactivitate (reparat pe 10 aprilie, v2.1.101) și un plafon de verbozitate în system prompt din 16 aprilie, care a produs o scădere măsurată de ~3% a calității (revenit pe 20 aprilie). Separat și mai devreme, Stella Laurenzo, Senior Director la AMD, a publicat un audit independent (6 aprilie, depus ca issue GitHub anthropics/claude-code#42796) pe 6.852 de sesiuni Claude Code și 234.760 de tool call-uri, care arăta trecerea de la un comportament research-first la unul edit-first pe măsură ce ascunderea thinking-ului a crescut de la 1,5% la 100% dintre tururi, atribuind degradarea în parte rollout-ului din februarie al lui adaptive thinking activat implicit.
**Sursa:** Post-mortem-ul de engineering Anthropic, 23 aprilie 2026: [anthropic.com/engineering/april-23-postmortem](https://www.anthropic.com/engineering/april-23-postmortem). Auditul Laurenzo: issue-ul GitHub anthropics/claude-code#42796; acoperire în The Register, 6 aprilie 2026.
**Unde e folosită:** Anexa D, Capitolul 3 (februarie-aprilie 2026: disciplina absoarbe o regresie de la vendor).
**Atenție:** Atribuirea către rollout-ul de adaptive thinking din februarie îi aparține lui Laurenzo, nu vendorului; cele trei cauze recunoscute de post-mortem încep în martie. Cele două relatări coincid pe regresii și diverg pe cauza cea mai timpurie.

---

### Vulnerabilități cu versiuni de patch

**Afirmația:** Claude Code era vulnerabil la remote code execution prin fișiere de proiect din surse nesigure: fișiere `.mcp.json` sau `.claude/settings.json` malițioase, din repo-uri în care nu aveai încredere, puteau executa hook-uri înainte de dialogul de trust, deschizând calea spre RCE.
**Sursa:** Check Point Research, February 2026. CVE-2025-59536. NVD: [nvd.nist.gov/vuln/detail/CVE-2025-59536](https://nvd.nist.gov/vuln/detail/CVE-2025-59536). Articol: [research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/).
**Unde e folosită:** Anexa D, Capitolul 2 (trei clase de vulnerabilități din spatele straturilor unu-trei); menționată și în Anexa A (O echipă, săptămână cu săptămână, scena cu comitetul de securitate).
**Atenție:** Dezvăluită și patch-uită în Claude Code v1.0.111 (octombrie 2025); articolul Check Point a apărut în februarie 2026. Versiunile dinaintea patch-ului rămân vulnerabile; clasa de probleme supraviețuiește chiar și după patch-ul specific.

---

**Afirmația:** Claude Code era vulnerabil la exfiltrarea de API key-uri prin injecție de configurație: setări controlate de atacator, care suprascriau `ANTHROPIC_BASE_URL` înainte de promptul de trust, puteau scurge API key-urile.
**Sursa:** Check Point Research, February 2026. CVE-2026-21852.
**Unde e folosită:** Anexa D, Capitolul 2 (trei clase de vulnerabilități din spatele straturilor unu-trei).
**Atenție:** Patch-uită în Claude Code v2.0.65. Aceeași clasă ca CVE-2025-59536: execuția configurației de proiect nesigure înainte de trust.

---

**Afirmația:** Knostic a raportat în decembrie 2025 că, în setup-ul observat, Claude Code încărca fișierele `.env*` din directorul de lucru fără permisiune explicită, expunând secretele în context.
**Sursa:** Knostic, December 2025: [knostic.ai/blog/claude-loads-secrets-without-permission](https://knostic.ai/blog/claude-loads-secrets-without-permission). Aria controalelor curente: [code.claude.com/docs/en/sandboxing](https://code.claude.com/docs/en/sandboxing).
**Unde e folosită:** Capitolul 2 (Stratul 3: Secrete); Anexa D, Capitolul 2 (trei clase de vulnerabilități din spatele straturilor unu-trei), numită în clasa de vulnerabilități de auto-încărcare a fișierelor dot-env.
**Atenție:** O relatare datată, nu o afirmație că fiecare sesiune curentă încarcă automat aceste fișiere. `denyRead` pentru shell și setările de credențiale protejează comenzile pe care le acoperă; citirile native de fișiere au nevoie de permisiuni separate. Ține secretele în afara mediului agentului dacă nicio cale de citire nu trebuie să ajungă la ele. Aria curentă a fost verificată pe 23 octombrie 2026.

---

**Afirmația:** Regulile de deny din Claude Code erau ocolite în tăcere atunci când o comandă de shell înlănțuia mai mult de 50 de subcomenzi (plafon dur MAX_SUBCOMMANDS_FOR_SECURITY_CHECK = 50), verificarea de securitate retrogradând la un prompt generic de "ask".
**Sursa:** Adversa AI Red Team, disclosed April 1, 2026. Articol: [adversa.ai/blog/claude-code-security-bypass-deny-rules-disabled/](https://adversa.ai/blog/claude-code-security-bypass-deny-rules-disabled/).
**Unde e folosită:** Capitolul 2 (Când se strică); Anexa D, Capitolul 2 (trei clase de vulnerabilități din spatele straturilor unu-trei), ca exemplul de bypass prin plafonul parserului pentru ideea că "orice strat luat individual poate avea un mod de eșec silențios".
**Atenție:** Patch-uită în Claude Code v2.1.90 în primele zile ale lui aprilie 2026 - writeup-ul Adversa consemnează fix-ul până pe 4 aprilie, la câteva zile de la dezvăluire. Clasa - straturi de guvernanță cu plafoane de parser care cedează în tăcere - e ce trebuie să-ți rămână în minte după ce plafonul specific dispare.

---

**Afirmația:** Articolul lui Kinney din aprilie 2026 arată că o regulă de deny pentru tool-ul integrat Read nu blochează un subproces Bash care citește același fișier. Nici o regulă care recunoaște o anumită comandă nu acoperă neapărat accesul echivalent prin alt program.
**Sursa:** Adam Kinney, April 2026. Articol: [Claude Code's Deny Rules Don't Protect You - Here's What Actually Does](https://adamkinney.com/aatt/claude-code/deny-rules-dont-protect-you-sandbox-does/).
**Unde e folosită:** Anexa D, Capitolul 2 (trei clase de vulnerabilități din spatele straturilor unu-trei), ca o clasă de bypass al parserului de permisiuni.
**Atenție:** Rezultatul privește acoperirea parserului de comenzi, nu fiecare regulă de deny din fiecare agent. Restricțiile de citire de la nivel de OS protejează procesele acoperite de sandbox chiar dacă parserul ratează o citire; tool-urile native de fișiere au nevoie de permisiuni separate. Verifică versiunea instalată și toate căile disponibile de citire.

---

**Afirmația:** Două vulnerabilități zero-click de prompt injection în sandbox-ul Cursor - CVE-2026-50548 și CVE-2026-50549 (CVSS 9.8, botezate „DuneSlide”) - abuzau allowlist-ul de scriere pe directorul de lucru și un fallback de rezolvare a symlink-urilor ca să evadeze din sandbox și să ajungă la remote code execution la nivel de OS. Toate versiunile dinainte de Cursor 3.0 (2 aprilie 2026) erau afectate; 3.0 le-a reparat pe ambele.
**Sursa:** Cato Networks (Cato AI Labs), dezvăluite la mijlocul lui 2026. Writeup: [catonetworks.com/blog/duneslide-two-critical-rce-vulnerabilities/](https://www.catonetworks.com/blog/duneslide-two-critical-rce-vulnerabilities/); acoperire: SecurityWeek, The Hacker News, iulie 2026.
**Unde e folosită:** Capitolul 2 (Când se strică); Anexa D, Capitolul 2 (escape-urile din sandbox), stratul doi.
**Atenție:** Lecția e clasa, nu vendorul: și cel mai puternic strat poate avea bug-uri - exact de-asta straturile sunt cinci, nu unul.

---

**Afirmația:** Cercetătorii Mozilla 0Din au demonstrat (iunie 2026) un atac de prompt injection indirect în care un repository cu aspect inofensiv determină Claude Code să ruleze un script care își trage un payload codat base64 dintr-un DNS TXT record și deschide un reverse shell - atacul e împărțit între repository, DNS și mașina developerului, așa că nicio semnătură de reverse shell nu apare în clar pe disc sau pe fir.
**Sursa:** SecurityWeek, 29 iunie 2026: [securityweek.com/new-attack-abuses-claude-code-and-harmless-looking-repositories-to-hijack-developer-machines/](https://www.securityweek.com/new-attack-abuses-claude-code-and-harmless-looking-repositories-to-hijack-developer-machines/).
**Unde e folosită:** Capitolul 2 (Injecția ajunge prin munca în sine); Anexa D, Capitolul 2 (injecția prin materialul de lucru: proof of concept-ul cu DNS TXT).
**Atenție:** Proof of concept; niciun patch de vendor raportat la momentul scrierii. Mitigarea e postura stratificată - un allowlist de rețea mărginește calea prin DNS indiferent de ce a fost convins agentul să ruleze.

---

### Documentația tool-urilor

**Afirmația:** Codex CLI a livrat Agent Skills ca componentă principală de primă clasă în decembrie 2025, cu fișiere SKILL.md cu frontmatter YAML și semantici de progressive disclosure comparabile cu Skills din Claude Code.
**Sursa:** OpenAI Codex CLI docs, [developers.openai.com/codex/skills](https://developers.openai.com/codex/skills).
**Unde e folosită:** Anexa D, Capitolul 1 (Memory și skill-uri: povestea convergenței), ca partea Codex a convergenței pe componenta principală de skill.
**Atenție:** Documentație de vendor; datele de GA sunt corecte la mijlocul lui 2026, dar pot fi revizuite retroactiv.

---

**Afirmația:** Subagenții din Codex CLI au ajuns la GA pe 14 martie 2026 și rulează până la șase în paralel by default (`agents.max_threads`, implicit 6; adâncimea de nesting e implicit un singur nivel).
**Sursa:** OpenAI Codex CLI docs, [developers.openai.com/codex/subagents](https://developers.openai.com/codex/subagents).
**Unde e folosită:** Anexa D, Capitolul 1 (cronologia adoptării subagenților).
**Atenție:** Documentație de vendor; default-ul de șase thread-uri e în practică un plafon la mijlocul lui 2026 (openai/codex#11965 urmărește configurabilitatea lui) și se poate schimba în versiunile următoare.

---

**Afirmația:** Codex CLI documentează [AGENTS.md](https://agents.md/) drept convenția pentru instrucțiuni de agent la nivel de proiect, încărcată la începutul sesiunii și echivalentă ca rol cu fișierele de instrucțiuni de echipă ale celorlalți vendori.
**Sursa:** OpenAI Codex CLI documentation, [developers.openai.com/codex/agents-md](https://developers.openai.com/codex/agents-md).
**Unde e folosită:** Capitolul 1 (Memory) și Capitolul 6 (Ce este AGENTS.md?).
**Atenție:** Numele fișierului și semantica de încărcare sunt stabile; regulile specifice de frontmatter și de descoperire pot evolua de la o versiune la alta.

---

**Afirmația:** AGENTS.md, în calitate de convenție neutră față de vendor pentru fișierul de instrucțiuni al echipei, are suport nativ în Codex CLI, Cursor, GitHub Copilot, Gemini CLI, Aider, Zed și Windsurf. Formatul e markdown; semantica de încărcare e echivalentă între tool-uri.
**Sursa:** Cross-vendor documentation: Codex CLI ([developers.openai.com/codex/agents-md](https://developers.openai.com/codex/agents-md)), Cursor ([cursor.sh/docs](https://cursor.sh/docs)), GitHub Copilot ([docs.github.com/copilot](https://docs.github.com/copilot)), Gemini CLI ([cloud.google.com/gemini/docs/codeassist](https://cloud.google.com/gemini/docs/codeassist)), Aider ([aider.chat/docs](https://aider.chat/docs)), Zed ([zed.dev/docs/ai](https://zed.dev/docs/ai)), Windsurf ([codeium.com/windsurf/docs](https://codeium.com/windsurf/docs)).
**Unde e folosită:** Capitolul 1 (Memory), Capitolul 6 (AGENTS.md vs CLAUDE.md: care e diferența?) și Anexa D, Capitolul 1 (Memory și skill-uri: povestea convergenței).
**Atenție:** Lista tool-urilor care îl suportă crește în timp; afirmația e că AGENTS.md e convenția de facto neutră față de vendor, nu că lista ar fi exhaustivă. Lista se și schimbă: Google a început la mijlocul lui 2026 tranziția utilizatorilor de Gemini CLI către Antigravity CLI (tier-urile gratuite și de consumator au încetat să fie servite în iunie) - iar succesorul citește același AGENTS.md, adică exact convenția care supraviețuiește tool-ului, adică exact poanta acestei intrări.

---

**Afirmația:** opencode e un coding agent open-source întreținut de o echipă independentă, scris în TypeScript și licențiat sub MIT. Codul sursă e organizat în jurul acelorași componente principale pe care manualul ăsta le identifică în Codex CLI și Claude Code.
**Sursa:** opencode repository ([github.com/anomalyco/opencode](https://github.com/anomalyco/opencode); fost sst/opencode - compania care îl întreține s-a redenumit Anomaly în ianuarie 2026); LICENSE and README.
**Unde e folosită:** Capitolul 1 (Anatomia e invariantă, dovada cu doi agenți) și Anexa D, Capitolul 1 (demo-ul cu doi agenți, în detaliu).
**Atenție:** Numele proiectului și componența echipei de mentenanță pot evolua; afirmația despre convergența arhitecturală supraviețuiește redenumirilor.

---

**Afirmația:** Playwright controlează un browser real prin interacțiuni scriptate; accessibility tree-ul e structura semantică pe care browserele o expun pentru tehnologiile asistive și rămâne stabil la restilizări vizuale sau la schimbarea bibliotecii de componente. Testele scrise pe accessibility tree verifică comportamentul, nu prezentarea.
**Sursa:** Playwright documentation ([playwright.dev/docs/accessibility-testing](https://playwright.dev/docs/accessibility-testing)); W3C ARIA Accessibility Object Model spec.
**Unde e folosită:** Capitolul 5 (Verify), ca pattern recomandat de verificare a frontend-ului; Anexa D, Capitolul 5 (Playwright cu accessibility tree-ul); checklist-ul din Anexa B.3.
**Atenție:** O parte din comportamentul UI-ului (animații, drag-and-drop, suprafețe canvas complexe) nu e surprinsă complet de accessibility tree și are nevoie de verificare suplimentară.

---

**Afirmația:** Claude Code oferă un sandbox de shell opt-in pe macOS, Linux și WSL2; comenzile native Windows rulează fără sandbox. Tool-urile native de fișiere, serverele MCP și hook-urile rulează în afara acestei limite și au nevoie de propriile controale. Codex are altă implementare de sandbox și altă postură implicită.
**Sursa:** Claude Code docs ([code.claude.com/docs/en/sandboxing](https://code.claude.com/docs/en/sandboxing)) și Codex CLI agent approvals and security docs ([developers.openai.com/codex/agent-approvals-security](https://developers.openai.com/codex/agent-approvals-security)).
**Unde e folosită:** Capitolul 1 (Postura sandbox-ului e o alegere de guvernanță) și Capitolul 2 (Stratul 2: Sandbox); Anexa D, Capitolul 1 (postura de sandbox pe vendor și mecanismele de dedesubt).
**Atenție:** "Activat implicit" versus "opt-in" e un detaliu de implementare care ține de versiune. Verifică default-ul curent pentru versiunea pe care o ai instalată înainte să te bazezi pe el.

---

**Afirmația:** Cursor 2.0 (octombrie 2025) a introdus agenți paraleli independenți și sandboxing activat implicit pe macOS; sistemul de subagenți propriu-zis - un agent părinte care deleagă către subagenți copii - a apărut în Cursor 2.4 (ianuarie 2026) și a devenit asincron în 2.5. Cline a livrat subagenți nativ. Claude Code a adăugat Agent Teams ca strat de coordonare de nivel mai înalt peste tool-ul Task.
**Sursa:** Changelog-urile Cursor (2.0, 2.4, 2.5); anunțurile și documentația vendorilor pentru Cline și Claude Code; colatate de-a lungul lui 2026.
**Unde e folosită:** Anexa D, Capitolul 1 (cronologia adoptării subagenților), ca dovadă pentru convergența pe componenta principală de subagent în aproximativ un an.
**Atenție:** Suprafețele de produs ale vendorilor evoluează; afirmația despre convergență rămâne în picioare chiar și când nume specifice de produs se rebranduiesc.

---

**Afirmația:** Claude Fable 5, lansat pe 9 iunie 2026 ca primul model din clasa Mythos, a avut accesul suspendat la nivel mondial între 12 și 30 iunie 2026, înainte de a fi redistribuit.
**Sursa:** Anthropic, „Claude Fable 5 and Mythos 5” (9 iunie 2026): [anthropic.com/news/claude-fable-5-mythos-5](https://www.anthropic.com/news/claude-fable-5-mythos-5); „Redeploying Fable 5” (30 iunie 2026): [anthropic.com/news/redeploying-fable-5](https://www.anthropic.com/news/redeploying-fable-5).
**Unde e folosită:** Capitolul 9 (Vendorul va avea o săptămână proastă).
**Atenție:** Motivul suspendării e relatarea vendorului; lecția operațională - planifică pentru indisponibilitatea vendorului - nu depinde de cauză.

---

**Afirmația:** Ghidul de teren din iulie 2026 al unui inginer Anthropic descrie Claude Fable 5 ca „primul model la care calitatea muncii are ca bottleneck capacitatea mea de a-i clarifica necunoscutele” și organizează metoda de lucru în jurul a patru tipuri de necunoscute, cu tehnici precum blind spot pass-ul, fișierele de note de implementare și quiz-urile de comprehensiune.
**Sursa:** Thariq Shihipar, „A field guide to Claude Fable 5: Finding your unknowns”, blogul Anthropic, 6 iulie 2026: [claude.com/blog/a-field-guide-to-claude-fable-finding-your-unknowns](https://claude.com/blog/a-field-guide-to-claude-fable-finding-your-unknowns).
**Unde e folosită:** Capitolul 3 (Constrângerea s-a mutat; Cele patru necunoscute), Capitolul 4 (Research, blind spot pass-ul; Execute, notele de implementare) și Capitolul 5 (Cum faci review pe un diff scris de agent?, quiz-ul); Anexa D, Capitolul 3 (framework-ul necunoscutelor, pe larg).
**Atenție:** Relatarea unui singur practician, publicată de vendor despre propriul model. Tehnicile stau în picioare singure; superlativul „primul model” e judecata autorului, nu o măsurătoare.

---

### Marketplace-uri și ecosisteme de plugin-uri

**Afirmația:** Marketplace-ul `claude-plugins-official` al Anthropic vine inclus în Claude Code din mai 2026 și împachetează skill-uri, hook-uri, tool-uri și comenzi în spatele unei singure comenzi de instalare. Marketplace-ul avertizează utilizatorii să verifice dacă au încredere în plugin-uri înainte să le instaleze.
**Sursa:** Claude Code docs ([code.claude.com/docs/en/discover-plugins](https://code.claude.com/docs/en/discover-plugins)); the marketplace itself.
**Unde e folosită:** Capitolul 1 (Plugin-uri); Anexa D, Capitolul 1 (plugin-uri: de ce există fiecare întrebare de vetting).
**Atenție:** Numărul de plugin-uri și politicile marketplace-ului se vor schimba în timp; ce trebuie să iei cu tine e disciplina de supply chain descrisă în Capitolul 1, nu vreun număr anume.

---

### Surse pentru componenta principală Memory

**Afirmația:** AGENTS.md e citit la începutul sesiunii de Codex CLI, Cursor, GitHub Copilot, Gemini CLI, Aider și de ecosistemul mai larg de coding agents open-source (peste 20 de vendori listați pe agents.md la 2026-05). Claude Code citește CLAUDE.md, care poate importa AGENTS.md pentru a împărți același conținut cu ceilalți agenți. Convergența plasează AGENTS.md în stratul de memorie definită manual al componentei principale Memory numit în Capitolul 1.
**Sursa:** [agents.md](https://agents.md/) (the open standard's site), plus vendor documentation for each agent listed.
**Unde e folosită:** Capitolul 1 (Memory) și Capitolul 6 (Ce este AGENTS.md?); Anexa D, Capitolul 1 (Memory și skill-uri: povestea convergenței).
**Atenție:** Numele exact al fișierului și semantica de încărcare diferă de la un vendor la altul - Claude Code citește CLAUDE.md (importabil din AGENTS.md prin `@AGENTS.md` sau symlink); Cursor citește AGENTS.md plus `.cursorrules`. Convergența e pe rolul structural - scris de utilizator, încărcat mereu, partajabil în echipă - nu pe un format de fișier identic la nivel de byte.

---

**Afirmația:** Claude Code întreține un strat de auto-memory în care Claude își scrie singur notițe de la o sesiune la alta - comenzi de build pe care le-a deslușit, concluzii de debugging pe care le-a confirmat, preferințe de stil de cod pe care le-a dedus - distinct de CLAUDE.md-ul scris de utilizator. Necesită Claude Code v2.1.59+; activat implicit; stocare per repo.
**Sursa:** [code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory).
**Unde e folosită:** Capitolul 1 (Memory); Anexa D, Capitolul 1 (Memory și skill-uri: povestea convergenței).
**Atenție:** Intrarea documentează implementarea din Claude Code, dar jumătatea asta e o convergență, nu o exclusivitate: GitHub Copilot Memory a ajuns în public preview pe 15 ianuarie 2026 - înainte să apară Auto Memory - și era activat implicit pe tier-urile Pro până pe 4 martie; Codex CLI a adăugat memorie automată de fundal în aprilie 2026.

---

**Afirmația:** Anthropic a anunțat public Dreaming ca parte din Claude Managed Agents la Code with Claude SF pe 2026-05-06 - un proces de fundal programat, care trece în revistă sesiunile recente și memory store-ul, identifică greșelile recurente și workflow-urile convergente și scrie notițe consolidate înapoi în memoria pe termen lung. Se livrează ca feature la nivel de platformă, condiționat de un beta header; o suprafață în CLI-ul Claude Code (`/dream`) era doar sugerată în produs și nu apăruse ca o comandă funcțională până în iulie 2026.
**Sursa:** Code with Claude SF announcement, 2026-05-06; [code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory).
**Unde e folosită:** Anexa D, Capitolul 1 (Memory și skill-uri: povestea convergenței).
**Atenție:** Dreaming e specific Anthropic și la nivel de API la data publicării, nu încă un feature de CLI. Manualul ăsta indexează rolul structural, nu vendorul.

---

### Surse pentru componenta principală Permisiuni / Sandbox

**Afirmația:** Claude Code aplică regulile explicite de permisiuni înainte să clasifice acțiunile eligibile rămase în auto mode. Sandbox-ul său de OS, opt-in, înconjoară comenzile de shell pe macOS, Linux și WSL2; nu acoperă tool-urile native de fișiere, serverele MCP sau hook-urile.
**Sursa:** [code.claude.com/docs/en/permissions](https://code.claude.com/docs/en/permissions); [code.claude.com/docs/en/sandboxing](https://code.claude.com/docs/en/sandboxing).
**Unde e folosită:** Capitolul 1 (Permisiuni / Sandbox) și Capitolul 2 (Stratul 1: Permisiuni și Stratul 2: Sandbox).
**Atenție:** Verificat pe 23 octombrie 2026. O regulă de deny-read pentru shell nu blochează tool-ul nativ Read; allowlist-urile de rețea pentru shell nu constrâng fiecare tool conectat. Verifică aria, platforma suportată și modul de permisiuni în versiunea instalată.

---

**Afirmația:** Hook-urile locale pot fi ocolite, inclusiv prin configurația Git pentru căile hook-urilor. Hook-urile de politică de tip comandă și HTTP din Claude Code pot permite acțiunea la erori sau timeout-uri dacă nu e configurată blocarea la eșec; `onFailure: "block"` cere v2.1.295+. Verificările obligatorii de pe server și aprobarea de la owner au nevoie de protecții pe care credențialele agentului nu le pot ocoli sau modifica unilateral.
**Sursa:** Claude Code, "Hooks reference": [code.claude.com/docs/en/hooks#block-the-action-when-a-hook-fails](https://code.claude.com/docs/en/hooks#block-the-action-when-a-hook-fails); Git, "githooks": [git-scm.com/docs/githooks](https://git-scm.com/docs/githooks); GitHub, "Available rules for rulesets": [docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets).
**Unde e folosită:** Capitolele 2, 8 și 9; Anexa B.6; Anexa D, Capitolul 9.
**Atenție:** Documentație verificată pe 23 octombrie 2026. Protecția depinde de setările efective, de evenimentul hook-ului și de semantica răspunsului, de privilegiile credențialelor și de politica de pe server. Nu e un audit de runtime al mediului cititorului.

---

**Afirmația:** Codex CLI impune implicit sandbox la nivel de OS pe Linux (Landlock + seccomp prin bwrap) și pe macOS (Seatbelt); pe Windows folosește restricted tokens plus izolare bazată pe ACL-uri. Stratul de decizie e livrat în paralel, ca gate de aprobare per tool.
**Sursa:** [developers.openai.com/codex/concepts/sandboxing](https://developers.openai.com/codex/concepts/sandboxing); [developers.openai.com/codex/agent-approvals-security](https://developers.openai.com/codex/agent-approvals-security).
**Unde e folosită:** Capitolul 1 (Permisiuni / Sandbox; Postura sandbox-ului e o alegere de guvernanță) și Capitolul 2 (Stratul 2: Sandbox); Anexa D, Capitolul 1 (postura de sandbox pe vendor și mecanismele de dedesubt).
**Atenție:** Postură opt-out - poți configura Codex să ruleze fără sandbox, dar default-ul inversează convenția, de la "oprit dacă nu-l configurezi" la "pornit dacă nu-l dezactivezi". Implementarea pe Windows e cea mai puțin uniformă dintre agenții majori.

---

**Afirmația:** opencode vine cu un model de prompt de permisiuni în interiorul agentului și cu validare de căi și permisiuni, dar nu oferă izolare prin sandbox la nivel de OS; pentru izolare, operatorul trebuie să împacheteze opencode în Docker, într-un microVM sau într-un alt harness de sandbox (KB-ul Vercel documentează explicit acest pattern de deployment). La testul de convergență din Capitolul 1, opencode trece jumătatea cu stratul de decizie și pică jumătatea cu enforcement-ul la nivel de OS.
**Sursa:** [vercel.com/kb/guide/running-opencode-securely-with-the-vercel-sandbox](https://vercel.com/kb/guide/running-opencode-securely-with-the-vercel-sandbox).
**Unde e folosită:** Capitolul 1 (Permisiuni / Sandbox; Anatomia e invariantă; Postura sandbox-ului e o alegere de guvernanță); Anexa D, Capitolul 1 (postura de sandbox pe vendor și mecanismele de dedesubt).
**Atenție:** Eticheta de "îngrădire soft" îi aparține manualului, nu documentației opencode. opencode nu pretinde că livrează un sandbox - absența e asumată onest, nu ascunsă.

---

### Surse despre bucla exterioară și autonomie

**Afirmația:** Până în primăvara lui 2026, bucla exterioară devine o suprafață de primă clasă în Claude Code: /loop rerulează un prompt la un interval dat (martie 2026) sau își alege singur ritmul când intervalul lipsește (aprilie 2026), Routines declanșează cloud agents pe bază de template dintr-un program, dintr-un eveniment GitHub sau dintr-un apel de API (aprilie 2026), /goal ține agentul la lucru de la un tur la altul până când o condiție de finalizare e îndeplinită (mai 2026), iar /autofix-pr urmărește CI-ul și comentariile de review și împinge fix-uri până când pull request-ul e verde (aprilie 2026).
**Sursa:** Claude Code release notes, "What's new": [code.claude.com/docs/en/whats-new](https://code.claude.com/docs/en/whats-new), weekly digests for April-May 2026.
**Unde e folosită:** Anexa D, Capitolul 9 (bucla exterioară: valul vendorilor și mecanismele condiției de oprire).
**Atenție:** Numele de feature și săptămânile de release reflectă stadiul vendorului la iulie 2026; așteaptă-te la schimbări, conform notei despre afirmațiile datate.

---

**Afirmația:** Tehnica Ralph Wiggum - un while-loop de bash care tot trimite un fișier de prompt într-un coding agent, cu context proaspăt la fiecare iterație și starea ținută în repository - pornește de la Geoff Huntley la mijlocul lui 2025 ("In its purest form, Ralph is a Bash loop": `while :; do cat PROMPT.md | claude-code ; done`), devine virală la sfârșitul lui 2025 și e adoptată în repository-ul oficial Claude Code ca plugin-ul ralph-wiggum în noiembrie 2025 (commit-ul de migrare e datat 16 noiembrie). Huntley estimează costul rulării buclei brute la aproximativ 10 dolari pe oră, spune că multe startup-uri din Y Combinator rulează Ralph și numește modul de eșec central "overbaking".
**Sursa:** Geoff Huntley, [ghuntley.com/ralph](https://ghuntley.com/ralph/) (July 2025); HumanLayer, "A Brief History of Ralph," January 6, 2026: [humanlayer.dev/blog/brief-history-of-ralph](https://www.humanlayer.dev/blog/brief-history-of-ralph); The Register, January 27, 2026: [theregister.com/2026/01/27/ralph_wiggum_claude_loops/](https://www.theregister.com/2026/01/27/ralph_wiggum_claude_loops/).
**Unde e folosită:** Anexa D, Capitolul 9 (bucla exterioară: de la AutoGPT la Ralph Wiggum), paragrafele despre filiație și overbaking.
**Atenție:** Cifra de 10 dolari pe oră și afirmația despre adopția în Y Combinator îi aparțin lui Huntley, preluate de The Register - raportări de practician, nu cifre auditate.

---

**Afirmația:** Execuția de agenți în fundal și pe bază de program a fost livrată de mai mulți vendori pe parcursul sfârșitului lui 2025: GitHub Copilot coding agent disponibil general pe 25 septembrie 2025 (mediu izolat de GitHub Actions; rezultatul livrat ca draft de pull request; review cerut unui om la finalizare); Cursor Cloud Agents pe 30 octombrie 2025 (mulți agenți detașați, cu laptopul închis); Google Jules Scheduled Tasks pe 10 decembrie 2025 (cadențe recurente pentru muncă de mentenanță).
**Sursa:** GitHub changelog: [github.blog/changelog/2025-09-25-copilot-coding-agent-is-now-generally-available](https://github.blog/changelog/2025-09-25-copilot-coding-agent-is-now-generally-available/); Cursor blog: [cursor.com/blog/cloud-agents](https://cursor.com/blog/cloud-agents); Google blog: [blog.google/technology/developers/jules-proactive-updates](https://blog.google/technology/developers/jules-proactive-updates/).
**Unde e folosită:** Anexa D, Capitolul 9 (bucla exterioară: valul vendorilor și mecanismele condiției de oprire), paragraful despre convergență.
**Atenție:** Datele de livrare sunt cele din anunțurile vendorilor; suprafețele au continuat să evolueze de atunci.

---

**Afirmația:** Echipa "software factory" de la StrongDM rulează livrare cu agenți complet non-interactivă - oamenii nici nu scriu, nici nu fac review la cod - cu scenarii end-to-end de user story stocate în afara codebase-ului, ca un holdout set pe care agenții nu îl pot vedea sau slăbi, și tratează aproximativ 1.000 de dolari pe zi per inginer cheltuiți pe tokeni drept prag minim de sănătate al fabricii; Simon Willison rezumă economia la circa 20.000 de dolari pe lună per inginer și semnalează asta ca principala limitare a pattern-ului.
**Sursa:** Simon Willison, "How StrongDM's AI team build serious software without even looking at the code," February 7, 2026: [simonwillison.net/2026/Feb/7/software-factory/](https://simonwillison.net/2026/Feb/7/software-factory/).
**Unde e folosită:** Anexa D, Capitolul 9 (bucla exterioară: de ce există fiecare linie din contract și cele două extreme), extrema industrială.
**Atenție:** Auto-descrierea unei singure companii; sumele în dolari sunt ale echipei și încadrarea lui Willison, nu un audit.

---

**Afirmația:** Era buclelor din 2023 - AutoGPT, BabyAGI - rula un model în buclă pe baza propriei lui evaluări a progresului, fără un verificator extern la fiecare iterație, și s-a prăbușit ca abordare de livrare de software în câteva luni. Revirimentul din 2025 diferă structural: fiecare iterație se încheie cu o confruntare cu compilatorul, cu testele și cu diff-ul.
**Sursa:** The AutoGPT and BabyAGI repositories document the 2023 design: [github.com/Significant-Gravitas/AutoGPT](https://github.com/Significant-Gravitas/AutoGPT), [github.com/yoheinakajima/babyagi](https://github.com/yoheinakajima/babyagi). The structural contrast is this manual's analysis, drawn from the Ralph-era sources above.
**Unde e folosită:** Anexa D, Capitolul 9 (bucla exterioară: de la AutoGPT la Ralph Wiggum), paragraful despre filiație.
**Atenție:** Verdictul de "prăbușire" e o interpretare; ambele proiecte au continuat în alte roluri.

---

### Surse despre harness și migrarea între modele

**Afirmația:** Ghidurile curente ale vendorilor susțin planificarea proporțională cu task-ul și instrucțiunile cu scop clar: Codex recomandă rezultate explicite, instrucțiuni de proiect practice și planificare pentru munca complexă; Claude Code recomandă explorarea și planificarea unde ajută, dar execuția directă pentru editări mici și clare. Ghidul OpenAI pentru GPT-6 Astra avertizează împotriva trigger-elor de skill prea largi, a rețetelor elaborate și a cerinței de a cartografia tot repository-ul înainte de orice schimbare.
**Sursa:** Eric Provencher, OpenAI, "Rethinking skills and prompts for GPT-6 Astra," September 11, 2026: [developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra); OpenAI, "Best practices": [learn.chatgpt.com/docs/learn/best-practices](https://learn.chatgpt.com/docs/learn/best-practices); Anthropic, "Best practices for Claude Code" și "Create custom subagents": [code.claude.com/docs/en/best-practices](https://code.claude.com/docs/en/best-practices), [code.claude.com/docs/en/sub-agents](https://code.claude.com/docs/en/sub-agents).
**Unde e folosită:** Capitolele 1, 3 și 4; Anexa B.3, B.9 și B.10; Anexa D, Capitolele 3 și 4.
**Atenție:** Îndrumări de vendor, nu o comparație controlată a întregului workflow al cărții. Documentația curentă a fost verificată pe 23 octombrie 2026; cerințele și controalele depind în continuare de task și de organizație.

---

**Afirmația:** Ghidul Anthropic pentru Opus 5 spune că instrucțiunile suplimentare de verificare și subagenții verificatori pot produce over-verification: cost suplimentar fără câștig de calitate. Ghidul Fable 5 recomandă în schimb verificatori cu context proaspăt pentru munca de durată. Niciunul nu stabilește o cerință universală de doi revieweri în secvență.
**Sursa:** Anthropic, "Prompting Claude Opus 5": [platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5); "Prompting Claude Fable 5", mai jos.
**Unde e folosită:** Capitolul 5 (Review: perspective distincte, revieweri după nevoie); Anexa B.3 și B.9; Anexa D, Capitolul 5.
**Atenție:** Recomandări de vendor specifice modelului, verificate pe 23 octombrie 2026. Privesc structura suplimentară adăugată agentului, nu permit ocolirea gate-urilor umane, de CI sau de securitate.

---

**Afirmația:** Claude Code încarcă descrierile skill-urilor înainte de invocare și corpurile complete când sunt invocate; trigger-ele prea largi pot fi restrânse sau trecute pe invocare manuală. Recomandă instrucțiuni de proiect concise și cu scop clar. Din v2.1.277 poate citi direct AGENTS.md când pe calea proiectului nu există CLAUDE.md sau CLAUDE.local.md; altfel, default-ul favorizează CLAUDE.md, cu importuri și setări disponibile.
**Sursa:** Anthropic, "Extend Claude with skills" și "How Claude remembers your project": [code.claude.com/docs/en/skills](https://code.claude.com/docs/en/skills), [code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory).
**Unde e folosită:** Capitolele 1 și 6; Anexa B.2 și B.10; Anexa D, Capitolele 1 și 6.
**Atenție:** Comportament Claude Code, verificat pe 23 octombrie 2026; versiunile, setările și celelalte harness-uri diferă. Mărimea catalogului nu înseamnă aceeași cantitate de instrucțiuni complete încărcate în context.

---

**Afirmația:** Comparațiile directe cu Superpowers arată beneficii condiționate și cost suplimentar. Studiul Krupa, cu 192 de rulări pentru v6.4.2 pe Sonnet 5.5, a raportat un raport mediu al costului per caz de 1,33x; testul de regresie pentru bugfix a apărut în 8/8 rulări cu plugin și 4/8 fără, cu fix-uri corecte în ambele variante. Rularea OrcaBot din iulie, cu v6 pe Codex gpt-5.5/high, a rezolvat 57,06% față de 55,56% din 729 de cazuri SWE-bench Pro comune, la 0,46 dolari față de 0,37 per problemă.
**Sursa:** Bartłomiej Krupa, September 29, 2026: [bartlomiejkrupa.dev/articles/does-superpowers-beat-no-plugin/](https://bartlomiejkrupa.dev/articles/does-superpowers-beat-no-plugin/); Rob Macrae, OrcaBot, July 31, 2026: [orcabot.com/benchmarks/agent-skills](https://orcabot.com/benchmarks/agent-skills); Superpowers release notes: [github.com/obra/superpowers/blob/main/RELEASE-NOTES.md](https://github.com/obra/superpowers/blob/main/RELEASE-NOTES.md).
**Unde e folosită:** Capitolul 4 (Ce este bucla în șase faze?); Anexa B.10; Anexa D, Capitolul 4.
**Atenție:** Krupa a folosit cazuri mici, headless, și evaluare care recompensează parțial procesul; OrcaBot a folosit un singur seed per variantă, deci avantajul mic este indicativ. Versiunile ulterioare au schimbat execuția Native și gate-urile. În această revizie nu am găsit o comparație independentă v7.x cu versiunea curentă de Codex; raporturile vechi de cost nu sunt măsurători ale versiunii actuale.

---

**Afirmația:** SkillsBench v4, cu 87 de task-uri din opt domenii și 18 configurații model/harness, a măsurat o creștere a ratei medii de succes de la 33,9% la 50,5% cu skill-uri curatoriate.
**Sursa:** Xiangyi Li et al., "SkillsBench: Benchmarking How Well Agent Skills Work Across Diverse Tasks," February 13, 2026, v4 June 14: [arxiv.org/abs/2602.12670v4](https://arxiv.org/abs/2602.12670v4).
**Unde e folosită:** Capitolul 1 (Skill-uri); Anexa D, Capitolul 4 (skill-uri specializate versus workflow general).
**Atenție:** Skill-uri specifice task-ului, curatoriate, și verificatori deterministici, nu o evaluare Superpowers sau a unui proces obligatoriu. Câștigul agregat nu dovedește un beneficiu pentru fiecare task sau model; lucrarea e un preprint.

---

**Afirmația:** Anthropic a scos peste 80% din system prompt-ul propriu al Claude Code pentru generația Claude 5 (Opus 5, Fable 5), fără pierdere măsurabilă pe evaluările lui de coding, înlocuind regulile cu judecată și exemplele lucrate cu interfețe proiectate.
**Sursa:** Thariq Shihipar, "The new rules of context engineering for Claude 5 generation models," Anthropic blog, July 24, 2026: [claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models](https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models).
**Unde e folosită:** Anexa D, Capitolul 6 (circa 200 de linii este un reper, nu un prag demonstrat).
**Atenție:** Evaluările proprii ale vendorului, pe propriul harness; sfatul e scris pentru generația Claude 5, iar modelele mai vechi s-ar putea să aibă încă nevoie de instrucțiunile șterse.

---

**Afirmația:** Ghidul de prompting al Anthropic pentru Fable 5 spune că subagenții verificatori separați, cu context proaspăt, tind să depășească autocritica; descrie un sistem de memorie cu câte o lecție per fișier, cu rezumat de o linie, actualizată în loc de duplicată, ștearsă când e greșită; documentează opririle timpurii rare pe o declarație de intenție („I'll now run X”) și acțiunile ocazionale necerute, fiecare cu un bloc de prompt; și avertizează că a cere modelului să-și reproducă raționamentul în răspuns poate declanșa categoria de refuz reasoning_extraction.
**Sursa:** Anthropic, "Prompting Claude Fable 5," Claude Platform docs: [platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5).
**Unde e folosită:** Anexa D, Capitolul 4 (blocurile de autonomie și de scop ale vendorilor), Capitolul 5 (când ajută un reviewer independent) și Capitolul 6 (mecanica jurnalului de greșeli); Anexa B.3 și B.9.
**Atenție:** Pagină de documentație nedatată, revizuită pe loc; verifică formularea curentă înainte să te bazezi pe o frază anume.

---

**Afirmația:** Ghidul de prompting al Anthropic pentru Fable 5.1 recomandă ca tool-ul care pornește un subagent să se întoarcă imediat, cu rezultatul livrat într-un mesaj ulterior; spune că numele nivelurilor de effort nu corespund aceleiași cantități de gândire de la un model la altul și că Fable 5.1 pe effort low e adesea competitiv cu Opus și Sonnet la cost per task, cu scor mai mare; cere istoric de conversație append-only, pentru că blocurile de gândire sunt valide doar în conversația exactă care le-a produs; notează că, odată cu citirile din cache mai ieftine, compactarea timpurie ca să economisești s-ar putea să nu mai fie schimbul potrivit; dă o listă de păstrat pentru rezumatele de compactare și cere respectarea scopului și protejarea artefactelor de test, fără slăbirea lor pentru a obține verde.
**Sursa:** Anthropic, "Prompting Claude Fable 5.1," Claude Platform docs: [platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1).
**Unde e folosită:** Capitolul 1 (Effort), Capitolul 6 (Igiena contextului); Anexa D, Capitolul 1 (Effort: dovezile), Capitolul 4 (un singur scriitor și context ales după rol) și Capitolul 6 (istoric append-only și prețul cache-ului); Anexa B.7 și B.9.
**Atenție:** Pagină de documentație nedatată, pentru un model lansat pe 1 septembrie 2026. Cifra de 0,025x din Anexa D, Capitolul 6 e aritmetica manualului pe prețurile publicate ale citirii din cache și ale input-ului de bază la momentul scrierii; cerința de append-only se aplică, conform ghidului, conturilor create de la 31 august 2026 încoace.

---

**Afirmația:** Pattern-ul „advisor” al Anthropic: Sonnet cu Opus ca advisor a obținut cu 2,7 puncte procentuale mai mult pe SWE-bench Multilingual decât Sonnet singur, la un cost per task agentic cu 11,9% mai mic; Haiku cu un advisor Opus a obținut 41,2% pe BrowseComp față de 19,7% singur, rămânând cu 29% în urma lui Sonnet singur la scor, la un cost per task cu 85% mai mic.
**Sursa:** Anthropic, "The advisor strategy: Give agents an intelligence boost," April 9, 2026: [claude.com/blog/the-advisor-strategy](https://claude.com/blog/the-advisor-strategy).
**Unde e folosită:** Anexa A (Pârghiile structurale, rutarea pe tier-uri); Anexa D, Anexa A (rutarea pe tier-uri, cele două puncte măsurate).
**Atenție:** Benchmark-uri ale vendorului pe propriile modele; cifrele de cost sunt per task pe acele benchmark-uri, nu un raport general.

---

**Afirmația:** Editarea contextului de la Anthropic (curățarea automată a rezultatelor învechite de tool-uri) a adus o îmbunătățire de 29% pe o evaluare internă de căutare agentică.
**Sursa:** Anthropic, "Managing context on the Claude Developer Platform," September 29, 2025: [claude.com/blog/context-management](https://claude.com/blog/context-management).
**Unde e folosită:** Anexa D, Capitolul 6 (compactare și măsurători de context).
**Atenție:** Evaluare internă; postarea descrie curățarea, nu o comparație cu rezumarea - comparația aia e intrarea JetBrains de mai jos.

---

**Afirmația:** Ghidul OpenAI pentru builderi raportează că GPT-5.6 Sol pe effort low a depășit GPT-5.5 pe effort high la Agents' Last Exam, cu harness-ul ținut constant, și că apelarea programatică a tool-urilor a egalat calitatea pe rubrici folosind cu 21% mai puțini tokeni de input pe un benchmark de research financiar.
**Sursa:** OpenAI, "The builder's guide to GPT-5.6," August 2026: [openai.com/index/builders-guide-to-gpt-5-6/](https://openai.com/index/builders-guide-to-gpt-5-6/); migration guidance in "Prompting guidance for GPT-5.6 Sol," [developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6](https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6).
**Unde e folosită:** Anexa D, Capitolul 1 (Effort: dovezile; cât costă definițiile de tool-uri și ce răspunsuri dau harness-urile din 2026); Anexa B.9.
**Atenție:** Evaluări ale vendorului; cifra de 21% vine dintr-un singur benchmark (Rogo's Big Finance Benchmark), nu e o medie generală. Ghidul de migrare spune să păstrezi effort-ul curent ca baseline și să compari cu un nivel mai jos - adică sweep-ul din B.9, în cuvintele vendorului.

---

**Afirmația:** Ghidul OpenAI pentru GPT-6 Astra spune că instrucțiunile utilizatorului au prioritate față de îndrumările dintr-un skill; că modelul e mai sensibil la informația din context, așa că o îndrumare neclară sau contradictorie într-un fișier de skill îl poate face să se oprească și să blocheze munca devreme; că e mai înclinat să pună utilizatorului o întrebare când un input ar putea schimba rezultatul; și că tinde spre teste mai late decât cere task-ul, cu contra-îndrumarea de a nu scrie teste pentru modificări reversibile, cu impact mic.
**Sursa:** OpenAI, "Using GPT-6 Astra," September 2026: [developers.openai.com/api/docs/guides/latest-model](https://developers.openai.com/api/docs/guides/latest-model).
**Unde e folosită:** Anexa D, Capitolul 4 (blocurile de autonomie și de scop ale vendorilor) și Capitolul 6 (de ce există linia de precedență); Anexa B.2 și B.3.
**Atenție:** Astra e numele de cod al modelului GPT-6 de la OpenAI, lansat pe 3-4 septembrie 2026, nu un produs separat; ghidul e nedatat și revizuit pe loc.

---

**Afirmația:** Practica proprie a OpenAI pentru Codex ține un AGENTS.md scurt, de vreo 100 de linii, care servește în primul rând ca hartă, cu pointeri spre surse de adevăr mai adânci, iar baza de cunoștințe a repository-ului stă într-un director docs/ structurat, tratat ca sistem de referință.
**Sursa:** Ryan Lopopolo, "Harness engineering: leveraging Codex in an agent-first world," OpenAI, February 11, 2026: [openai.com/index/harness-engineering/](https://openai.com/index/harness-engineering/).
**Unde e folosită:** Capitolul 6 (Regulile 3 și 4: context relevant, lungime justificată, unde stă harta); Anexa D, Capitolul 6 (fișierele de context trebuie să-și justifice conținutul); Anexa B.2.
**Atenție:** Practica unei singure echipe, descrisă de vendor. Harness-ul Codex în sine a fost publicat open source în august 2026 ("Codex as a platform," [developers.openai.com/blog/codex-as-a-platform](https://developers.openai.com/blog/codex-as-a-platform)), într-o postare separată.

---

**Afirmația:** Activarea raționamentului păstrat și a compactării a dus GPT-5.6 Sol de la 13,3% la 38,3% pe ARC-AGI-3, reducând în același timp tokenii de output de șase ori, cu harness-ul altfel neschimbat.
**Sursa:** OpenAI, "How enabling two settings tripled our scores on the ARC-AGI-3 benchmark," July 29, 2026: [openai.com/index/how-two-settings-tripled-our-arc-agi-3-scores/](https://openai.com/index/how-two-settings-tripled-our-arc-agi-3-scores/).
**Unde e folosită:** Capitolul 1 (Effort, raționamentul păstrat); Anexa D, Capitolul 1 (Effort: dovezile).
**Atenție:** Postare a vendorului, pe un singur benchmark și un singur model. Manualul o folosește pentru mecanism - raționamentul păstrat între ture se compune - nu pentru scorul concret.

---

**Afirmația:** Claude Code /goal folosește un model separat ca să evalueze condiția pe baza conversației. Codex Goals păstrează un obiectiv și un buget, iar modelul care execută munca îl poate marca drept finalizat. Aceste mecanisme de continuare și finalizare nu execută independent teste protejate de acceptare.
**Sursa:** Claude Code docs, "/goal": [code.claude.com/docs/en/goal](https://code.claude.com/docs/en/goal); OpenAI Cookbook, "Using Goals in Codex": [developers.openai.com/cookbook/examples/codex/using_goals_in_codex](https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex).
**Unde e folosită:** Capitolul 9 (Bucla exterioară, condiția de oprire); Anexa D, Capitolul 9 (bucla exterioară: valul vendorilor și mecanismele condiției de oprire).
**Atenție:** Documentație despre mecanism, verificată pe 23 octombrie 2026, nu dovezi de verificare independentă. Pentru acceptare, cere verificări protejate din exterior. Plugin-ul ralph-wiggum oferă un buget maxim de iterații și relatări de practicieni, nu dovada unui evaluator fiabil.

---

**Afirmația:** Studiul revizuit despre AGENTS.md nu a găsit o îmbunătățire generală a ratei de succes pentru fișierele de context generate la nivel de repository și a măsurat un cost de inferență cu peste 20% mai mare în setup-urile testate. Fișierele scrise de developeri au adus un câștig mediu modest, fără semnificație statistică; prezentările de ansamblu ale repository-ului nu au ajutat în această evaluare.
**Sursa:** Thibaud Gloaguen, Niels Mündler, Mark Niklas Müller, Veselin Raychev, Martin Vechev (ETH Zürich), "Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?", February 12, 2026 (v3 September 29, 2026): [arxiv.org/abs/2602.11988v3](https://arxiv.org/abs/2602.11988v3).
**Unde e folosită:** Capitolul 6 (Regulile 3 și 4: context relevant, lungime justificată, unde stă harta); Anexa D, Capitolul 6 (fișierele de context trebuie să-și justifice conținutul); Anexa B.2.
**Atenție:** Măsurat pe anumiți agenți și anumite benchmark-uri; nu dovedește că orice fișier de instrucțiuni dăunează. Recomandarea manualului este să păstrezi constrângerile locale, comenzile și pointerii care ajută, apoi să verifici rezultatele; nu există un prag universal demonstrat de linii sau o categorie de conținut garantat utilă.

---

**Afirmația:** Pe 260 de configurații multi-agent, coordonarea a ajutat doar pe task-urile descompozabile, a degradat planificarea secvențială cu între 39% și 70% în funcție de arhitectură și a produs randamente negative pe task-urile unde un singur agent depășea deja circa 45% acuratețe.
**Sursa:** Kim et al., "Capable language models can outgrow the benefits of collaboration," Nature Machine Intelligence 8, 1157-1172, July 24, 2026: [doi.org/10.1038/s42256-026-01268-y](https://doi.org/10.1038/s42256-026-01268-y); preprint "Towards a Science of Scaling Agent Systems," [arxiv.org/abs/2512.08296](https://arxiv.org/abs/2512.08296).
**Unde e folosită:** Capitolul 4 (Execute, gate-ul de împărțire); Anexa D, Capitolul 4 (când rentează împărțirea în subagenți); Anexa B.3.
**Atenție:** Benchmark-urile nu sunt specifice codului; pragul de 45% e un predictor ajustat pe task-urile testate, nu o lege.

---

**Afirmația:** Pe SpecBench, fiecare agent de frontieră saturează suita de teste vizibilă, în timp ce scorul pe testele ascunse rămâne mult mai mic, cu decalaje de circa 43-48 de puncte procentuale; decalajul la percentila 90 crește cu circa 27 de puncte la fiecare înzecire a numărului de linii de cod; căutarea suplimentară nu elimină fiabil reward hacking-ul.
**Sursa:** Bingchen Zhao, Dhruv Srikanth, Yuxiang Wu, Zhengyao Jiang (Weco AI), "SpecBench: Measuring Reward Hacking in Long-Horizon Coding Agents," May 20, 2026 (v2 September 9, 2026): [arxiv.org/abs/2605.21384](https://arxiv.org/abs/2605.21384).
**Unde e folosită:** Capitolul 5 (Poți avea încredere în testele scrise de agent?); Anexa D, Capitolul 5 (SpecBench și constatarea Cursor, pe larg); Anexa B.3.
**Atenție:** Abstractul rotunjește creșterea la 28 de puncte; corpul lucrării raportează 27, cu R² de 0,21, deci trendul e real și zgomotos.

---

**Afirmația:** Pe SWE-bench Pro, 63% dintre rezolvările reușite ale lui Claude Opus 4.8 Max au recuperat fix-ul din upstream în loc să-l derive; sigilarea istoricului de git și tăierea egress-ului de rețea au coborât scorul de la 87,1% la 73,0%.
**Sursa:** Naman Jain, Cursor, "Reward hacking is swamping model intelligence gains," June 25, 2026: [cursor.com/blog/reward-hacking-coding-benchmarks](https://cursor.com/blog/reward-hacking-coding-benchmarks).
**Unde e folosită:** Capitolul 5 (Poți avea încredere în testele scrise de agent?, controlul cu istoricul sigilat); Anexa D, Capitolul 5 (SpecBench și constatarea Cursor, pe larg).
**Atenție:** Harness-ul unui singur vendor și un singur model; comportamentul e o proprietate a gate-ului, nu a modelului numit.

---

**Afirmația:** Într-un setup de raționament multi-agent, criticile verificate ca utile ale reviewerului mai precis au schimbat următorul candidat doar în 33,6% din cazuri, în timp ce un setup broadcast (între egali) a ajuns la 93,5% și la rata finală de succes mai mare.
**Sursa:** Chih-Hsuan Yang et al., "Precise but Uncoupled: Reviewer Precision Does Not Guarantee Critique Uptake in Multi-Agent Math Reasoning," July 16, 2026: [arxiv.org/abs/2607.15388](https://arxiv.org/abs/2607.15388).
**Unde e folosită:** Capitolul 5 (Review: perspective distincte, revieweri după nevoie); Anexa D, Capitolul 5 (când ajută un reviewer independent); Anexa B.3.
**Atenție:** Raționament matematic, nu code review; manualul împrumută măsurătoarea - preluarea contează mai mult decât precizia -, nu domeniul.

---

**Afirmația:** O buclă de verificare-și-reparare ghidată de rubrici (DeepVerifier) a atins vârful în jurul rundei a patra și scăzuse până la a zecea, pentru că tranziția incorect-la-corect se stinge repede, în timp ce tranziția corect-la-incorect persistă.
**Sursa:** Yuxuan Wan et al., "Inference-Time Scaling of Verification: Self-Evolving Deep Research Agents via Test-Time Rubric-Guided Verification," January 22, 2026 (v2 April 29, 2026): [arxiv.org/abs/2601.15808](https://arxiv.org/abs/2601.15808).
**Unde e folosită:** Capitolul 5 (Review: perspective distincte, revieweri după nevoie, plafonarea rundelor); Anexa D, Capitolul 5 (când ajută un reviewer independent); Anexa B.3.
**Atenție:** Agenți de deep research pe GAIA, nu coding; scăderea față de vârf e de câteva puncte, deci lecția e forma curbei, nu mărimea căderii.

---

**Afirmația:** Judecătorii LLM se ancorează de un scor anterior care li se arată, și nici raționamentul chain-of-thought, nici un avertisment explicit de a ignora metadatele nu elimină efectul total.
**Sursa:** Ante Kapetanovic et al., "Anchoring Bias in LLM-as-a-Judge Systems: Prior Scores Compromise Evaluation Independence," August 26, 2026: [arxiv.org/abs/2608.25869](https://arxiv.org/abs/2608.25869).
**Unde e folosită:** Capitolul 5 (Review: perspective distincte, revieweri după nevoie, al doilea reviewer rămâne orb la primul); Anexa D, Capitolul 5 (când ajută un reviewer independent); Anexa B.3.
**Atenție:** Context de evaluare, nu de code review; manualul aplică rezultatul la situația în care reviewerul doi vede verdictele reviewerului unu.

---

**Afirmația:** Rata cu care un model satisface deodată toate regulile dintr-un prompt se prăbușește la zero pe la 80 de reguli simultane, pentru fiecare model, format și plasare testate, inclusiv Claude Sonnet 5 și Claude Haiku.
**Sursa:** Netanel Eliav, "Prompt Design at Scale: How Format, Instruction Count, and Context Length Shape Instruction Adherence and Hallucination in Large Language Models," July 21, 2026: [arxiv.org/abs/2607.19257](https://arxiv.org/abs/2607.19257).
**Unde e folosită:** Capitolul 6 (Regulile 3 și 4: context relevant, lungime justificată, reperul de lungime); Anexa D, Capitolul 6 (circa 200 de linii este un reper, nu un prag demonstrat).
**Atenție:** Rata de răspuns perfect e o metrică strictă, pe formatele și modelele testate; alte lucrări raportează praguri diferite. Studiul nu stabilește o conversie între numărul de reguli și lungimea unui AGENTS.md și nu justifică o limită universală de 200 de linii.

---

**Afirmația:** RULER măsoară o lungime efectivă a contextului - cel mai lung input la care un model își păstrează un scor-prag pe task-uri de retrieval și raționament pe toată fereastra -, iar la majoritatea modelelor testate lungimea asta cade mult sub dimensiunea de context declarată.
**Sursa:** Cheng-Ping Hsieh et al. (NVIDIA), "RULER: What's the Real Context Size of Your Long-Context Language Models?", 2024: [arxiv.org/abs/2404.06654](https://arxiv.org/abs/2404.06654).
**Unde e folosită:** Capitolul 1 (Context window); Anexa D, Capitolul 1 (contextul efectiv e mai scurt decât fereastra din reclamă).
**Atenție:** Lectura „pe la jumătate” din Anexa D, Capitolul 1 e o regulă empirică din sintezele practicienilor din 2026 pe rezultate de tip RULER, nu o singură măsurătoare; lungimile efective per model variază mult și se îmbunătățesc cu fiecare generație.

---

**Afirmația:** Pentru sesiuni lungi de coding agentic, mascarea observațiilor vechi de tool-uri a bătut rezumarea cu LLM în patru din cinci setări, a tăiat costul cu peste 50% și a egalat sau a depășit ușor rezumarea la rata de rezolvare.
**Sursa:** Katie Fraser and Tobias Lindenbauer, JetBrains Research, "Cutting Through the Noise: Smarter Context Management for LLM-Powered Agents," December 2025: [blog.jetbrains.com/research/2025/12/efficient-context-management/](https://blog.jetbrains.com/research/2025/12/efficient-context-management/) (paper: "The Complexity Trap," NeurIPS 2025 DL4Code workshop).
**Unde e folosită:** Capitolul 6 (Igiena contextului); Anexa D, Capitolul 6 (compactare și măsurători de context); Anexa A; Anexa B.7.
**Atenție:** Cifra de 52% citată uneori e o singură configurație (Qwen3-Coder 480B); rezultatul general e „peste 50%”.

---

**Afirmația:** Pe 15 modele, performanța în conversații multi-turn fragmentate a scăzut cu 39% în medie față de o singură tură complet specificată, iar consolidarea fragmentelor într-o singură tură a recuperat cam 95% din rezultatul single-turn.
**Sursa:** Philippe Laban, Hiroaki Hayashi, Yingbo Zhou, Jennifer Neville, "LLMs Get Lost in Multi-Turn Conversation," May 2025: [arxiv.org/abs/2505.06120](https://arxiv.org/abs/2505.06120).
**Unde e folosită:** Capitolul 6 (Igiena contextului, o unitate de muncă per sesiune); Anexa D, Capitolul 6 (compactare și măsurători de context).
**Atenție:** Conversații simulate pe task-uri de generare, nu sesiuni de coding; manualul o folosește pentru mecanismul din spatele consolidării înainte de a continua.

---

**Afirmația:** Opus 4.8 și Sonnet 5 inventează chei pe care o schemă imbricată de tool custom nu le-a declarat niciodată, în timp ce modelele mai vechi nu, iar pornirea invocării stricte a tool-urilor a eliminat comportamentul.
**Sursa:** Armin Ronacher, "Better Models: Worse Tools," July 4, 2026: [lucumr.pocoo.org/2026/7/4/better-models-worse-tools/](https://lucumr.pocoo.org/2026/7/4/better-models-worse-tools/).
**Unde e folosită:** Capitolul 1 (Tool-uri); Anexa D, Capitolul 1 (cât costă definițiile de tool-uri și ce răspunsuri dau harness-urile din 2026); Anexa B.9.
**Atenție:** Rulările unui singur practician pe un singur harness; recomandarea - decodare strictă pe schemele custom - nu costă nimic de adoptat oricum.

---

**Afirmația:** Într-un harness multi-agent, faci fork pe un worker ca să primească istoricul și cache-ul de prompt ale supervizorului și să continue investigația, și izolezi un verificator ca să evalueze munca în sine în loc să fie ancorat de diagnosticul supervizorului; în sistemele multi-agent care funcționează, scrierile rămân pe un singur fir, iar agenții suplimentari contribuie cu inteligență, nu cu acțiuni.
**Sursa:** Thushanth Bengre and Chester Curme, LangChain, "Organizing Context in a Multi-Agent Harness," September 8, 2026: [langchain.com/blog/organizing-context-in-a-multi-agent-harness](https://www.langchain.com/blog/organizing-context-in-a-multi-agent-harness); Walden Yan, Cognition, "Multi-Agents: What's Actually Working," April 22, 2026: [cognition.com/blog/multi-agents-working](https://cognition.com/blog/multi-agents-working).
**Unde e folosită:** Capitolul 4 (Execute, un singur scriitor per fișier); Anexa D, Capitolul 4 (un singur scriitor, workeri cu fork, revieweri izolați); Anexa B.3.
**Atenție:** Ambele sunt postări de inginerie ale unor vendori; „un singur scriitor” e comprimarea manualului pentru „scrierile rămân pe un singur fir” al lui Cognition.

---

**Afirmația:** Runtime-ul de afirmații din OpenWiki, care atașează pointeri la dovezi afirmațiilor stocate și le reverifică, a tăiat afirmațiile învechite din baza lui de cunoștințe de la 3,5% la 0,5% pe 2.000 de afirmații evaluate.
**Sursa:** Colin Francis, "Building Self-Correcting Memory in OpenWiki," LangChain blog, August 25, 2026: [langchain.com/blog/self-correcting-memory-openwiki](https://www.langchain.com/blog/self-correcting-memory-openwiki).
**Unde e folosită:** Capitolul 6 (Regulile 2 și 5: câștigate prin eșecuri, tratate ca cod, pointerul la dovezi); Anexa D, Capitolul 6 (mecanica jurnalului de greșeli).
**Atenție:** Un sistem de bază de cunoștințe, nu un jurnal de greșeli; manualul împrumută mecanismul - o afirmație care își citează dovada poate fi retrasă când dovada se învechește.

---

**Afirmația:** Navigarea agentică pe Claude Sonnet 4.5 a ajuns la 49,6% recall@1 pe BRIGHT, cu 21,8 puncte peste cel mai bun model de embeddings; spațiile de lucru mărginite (RISE) țin retrieval-ul agentic funcțional la un milion de documente, acolo unde inspecția directă a contextului se degradează; iar căutarea în cod pentru agenți se reduce la trei modalități - lexicală (ripgrep), structurală (ast-grep) și de graf (referințe LSP).
**Sursa:** Susheel Suresh et al., "AgenticRAG: Agentic Retrieval for Enterprise Knowledge Bases," May 7, 2026: [arxiv.org/abs/2605.05538](https://arxiv.org/abs/2605.05538); Shengyao Zhuang et al., "Towards Retrieving Interaction Spaces for Agentic Search" (RISE), June 5, 2026: [arxiv.org/abs/2606.06880](https://arxiv.org/abs/2606.06880); Andrey Kumanyaev, "Code search for AI agents: the grep replacement is three tools, not one," June 6, 2026: [zzet.org/gortex/grep-replacement-for-ai-agents/](https://zzet.org/gortex/grep-replacement-for-ai-agents/).
**Unde e folosită:** Anexa D, Capitolul 7 (de ce citește agentul codul, în loc să interogheze un index al lui); Capitolul 7 (Workflow-ul) enunță concluzia.
**Atenție:** Cifra de recall e pe un benchmark general de retrieval, nu pe un codebase; încadrarea cu trei tool-uri e a unui practician, iar manualul nu dă niciun prag numeric pentru momentul în care un index de embeddings începe să rentabilizeze.

---

**Afirmația:** Prompt caching-ul cu un layout de prompt cache-first a redus costul de API cu 41% până la 80% la mai mulți provideri, pe peste 500 de sesiuni de agent; o sesiune default de Claude Code s-a dovedit a consuma cam 24.000 de tokeni de definiții de tool-uri, scheme MCP și reminder-e înainte de orice interacțiune a utilizatorului; cu un pool mare de tool-uri încărcat integral, acuratețea de bază a selecției de tool-uri a fost 13,62%, iar recuperarea doar a tool-urilor relevante per query a urcat-o la 43,13%; socoteala unui practician a pus trei servere MCP la circa 143.000 de tokeni dintr-o fereastră de 200.000.
**Sursa:** Elias Lumer et al., "Don't Break the Cache: An Evaluation of Prompt Caching for Long-Horizon Agentic Tasks," January 31, 2026: [arxiv.org/abs/2601.06007](https://arxiv.org/abs/2601.06007); GitHub issue anthropics/claude-code#42452, April 2, 2026; Tiantian Gan and Qiyao Sun, "RAG-MCP: Mitigating Prompt Bloat in LLM Tool Selection via Retrieval-Augmented Generation," May 6, 2025: [arxiv.org/abs/2505.03275](https://arxiv.org/abs/2505.03275); MetaBlogue, "MCP servers and the context window," September 5, 2026: [metablogue.com/mcp-servers-context-window/](https://metablogue.com/mcp-servers-context-window/).
**Unde e folosită:** Capitolul 1 (Tool-uri); Anexa D, Capitolul 1 (cât costă definițiile de tool-uri și ce răspunsuri dau harness-urile din 2026); Anexa A (Pârghiile structurale).
**Atenție:** Cifrele de 24k și 143k sunt socoteli de practicieni, care variază de la o instalare la alta, și nu vin dintr-un studiu controlat; cifrele RAG-MCP compară o metodă de retrieval cu un baseline fără retrieval, la scară, și datează din 2025.

---

**Afirmația:** Pentru între 37% și 63% dintre lucrările de inginerie software analizate, un model mai nou cu un singur prompt depășește nativ tooling-ul puternic ingineresc propus cu circa un an înainte.
**Sursa:** Nahian Salsabil et al., "What Survives the Next Model? Benchmarking LLM-Based Techniques Against Single-Prompts," August 31, 2026: [arxiv.org/abs/2609.00468](https://arxiv.org/abs/2609.00468).
**Unde e folosită:** Capitolul 8 (Când se strică, verificarea de migrare între modele); Anexa D, Capitolul 8 (semnalul soft al migrării între modele, cu dovezile lui); Anexa B.9.
**Atenție:** Preprint pe arXiv, încă fără peer review; manualul îl folosește pentru direcție - fiecare generație pensionează o parte din harness -, nu pentru fracția exactă.

---

### Note despre actualitate

Majoritatea surselor din anexa asta sunt datate. Documentația tool-urilor se actualizează frecvent; înregistrările de vulnerabilități se amendează pe măsură ce apar patch-uri și variante noi. Framework-urile din corpul manualului sunt gândite să supraviețuiască oricărui URL anume. Dacă un URL moare, afirmația din spatele lui ar trebui să rămână căutabilă după numele incidentului, al studiului sau al produsului.

---

---

## Anexa D - Deep dives

Aici stau dovezile și detaliile datate din spatele fiecărui capitol: studiile, benchmark-urile, cronologiile vendorilor și cazurile lucrate pe care capitolele le lasă deoparte ca să rămână scurte. Intrările sunt grupate pe capitole, iar fiecare se încheie cu sursele și atenționările ei, în italic. Citările complete sunt în Anexa C; comportamentul vendorilor e datat la mijlocul lui 2026 și se va schimba, așa că verifică default-urile față de versiunea pe care o rulezi.

---

### Capitolul 1 - Ce este un agent {#deep-dive-chapter-1}

**Contextul efectiv e mai scurt decât fereastra din reclamă.** Ferestrele merg de la 200 de mii de tokeni la modelele compacte până la un milion de la gama medie în sus. Benchmark-ul RULER de la NVIDIA măsoară lungimea efectivă a contextului - cel mai lung input la care un model își păstrează scorul de pe context scurt pe toată fereastra - și, la majoritatea modelelor, ea cade mult sub cifra din reclamă, de regulă pe la jumătate. *Sursa: Hsieh et al. (NVIDIA), "RULER," 2024. Atenție: „pe la jumătate” e o regulă empirică din sintezele practicienilor din 2026, nu o singură măsurătoare.*

**Cât costă definițiile de tool-uri și ce răspunsuri dau harness-urile din 2026.** Un audit al unei sesiuni default de Claude Code a numărat cam 24k de tokeni de definiții de tool-uri, scheme MCP și reminder-e consumați înainte ca utilizatorul să tasteze ceva; socoteala unui practician a pus trei servere MCP la 143k dintr-o fereastră de 200k. Cu un catalog mare de tool-uri încărcat integral, acuratețea selecției într-un benchmark a fost de 13,62%; încărcarea doar a tool-urilor relevante a urcat-o la 43,13%. Răspunsurile din 2026 sunt încărcarea amânată (deferred loading) și apelarea programatică a tool-urilor (modelul scrie un script care face apelurile și întoarce un singur rezultat; nativă în GPT-5.6, unde a tăiat tokenii de input cu 21% pe o evaluare de research financiar). La tool-urile custom cu scheme imbricate, pornește decodarea strictă: Armin Ronacher a documentat cum Opus 4.8 și Sonnet 5 inventează câmpuri nedeclarate, iar modul strict le elimină. *Surse: Lumer et al., Jan 31, 2026; anthropics/claude-code#42452, Apr 2, 2026; Gan and Sun (RAG-MCP), May 6, 2025; MetaBlogue, Sep 5, 2026; OpenAI GPT-5.6 guide, Aug 2026; Ronacher, Jul 4, 2026. Atenție: 24k și 143k sunt socoteli de practicieni; cele 21% vin dintr-un singur benchmark (cel de la Rogo).*

**Postura de sandbox pe vendor și mecanismele de dedesubt.** Aria contează la fel de mult ca default-ul. Claude Code are un sandbox de shell opt-in pe macOS, Linux și WSL2; comenzile native Windows, tool-urile native de fișiere, serverele MCP și hook-urile sunt în afara lui. Codex documentează restricții la nivel de OS cu altă implementare și alte platforme suportate; verifică profilul de permisiuni selectat și orice cale de escaladare. opencode documentează controale de permisiuni, iar izolarea de OS e asigurată de un mediu extern. Configurează restricțiile efective de căi și rețea în runtime sau în politica administrată, nu în AGENTS.md. Testează citirile, scrierile și conexiunile interzise prin fiecare cale relevantă. *Surse: documentația Claude Code despre sandbox și permisiuni; documentația de securitate Codex; Vercel KB despre opencode, verificate pe 23 octombrie 2026. Atenție: configurația și acoperirea se schimbă cu versiunea; izolarea shell-ului nu înseamnă izolarea întregului agent.*

**Demo-ul cu doi agenți, în detaliu.** Claude Code a rulat în două panouri, unul peste Codex CLI (Rust, Apache 2.0, OpenAI) și unul peste opencode (TypeScript, MIT, echipă independentă), cu un singur prompt: explică arhitectura, mapează bucla agentului, sistemul de tool-uri, gate-urile de permisiuni, sandbox-ul și modelul de plugin-uri, citând fișiere și linii. A durat cam patru minute (o rerulare din mai 2026: 4:13), pentru că ambele repository-uri își numesc arhitectura în directoare; un codebase mai puțin auto-documentat cere zece-cincisprezece minute per repo. Amândouă au întors o buclă de agent, un registru de tool-uri, un gate de permisiuni, un director de plugin-uri, suport MCP și o cale de dispatch pentru subagenți (în opencode, identificată după comportament: o funcție care pornește o instanță proaspătă pe un prompt delimitat). Singura divergență a fost sandbox-ul. *Sursa: experiment al autorului, fără nicio corecție umană. Limitare: componentele principale există; asta nu înseamnă că sunt la fel de bine construite.*

**Cronologia adoptării subagenților.** Claude Code a livrat tool-ul Task, apoi Agent Teams peste el. Subagenții din Codex CLI au ajuns la GA pe 14 martie 2026 (până la șase în paralel by default, adâncime de nesting unu). Cursor a livrat agenți paraleli în 2.0 (octombrie 2025), un sistem de subagenți în 2.4 (ianuarie 2026) și varianta asincronă în 2.5. *Surse: documentația Codex CLI despre subagenți; changelog-urile Cursor. Atenție: default-ul de șase thread-uri din Codex e în practică un plafon la mijlocul lui 2026.*

**Orchestrare scriptată (`/workflows`).** `/workflows` din Claude Code (mijlocul lui 2026) pune agentul să scrie un script care trimite subagenți în mod determinist: faze în ordine, fan-out în paralel sau printr-un pipeline pe sute de copii, hand-off-uri validate după o schemă, un gate opțional de verificare, reluabil și cu buget limitat. Determinismul e singura diferență reală față de dispatch-ul condus de model (ca în Superpowers); apelează la el când fan-out-ul e mare, repetabil sau merită verificat mecanic. *Sursa: Changelog, 2026-06-11.*

**Memory și skill-uri: povestea convergenței.** Componenta principală always-loaded a ajuns la convergență pe AGENTS.md (citit la începutul sesiunii de Codex CLI, Cursor, GitHub Copilot, Gemini CLI, Aider, Zed, Windsurf și alții; peste 20 de vendori listați pe agents.md la 2026-05) și pe CLAUDE.md, pe care Claude Code îl citește nativ și care poate importa AGENTS.md. Și skill-urile on-demand au ajuns la convergență (Skills în Claude Code; fișiere `SKILL.md` în Codex CLI, decembrie 2025). Jumătatea scrisă de agent a convers într-o singură iarnă: GitHub Copilot Memory a ajuns în public preview pe 15 ianuarie 2026 și era activat implicit pe tier-urile individuale până în martie; Auto Memory din Claude Code a apărut în februarie (v2.1.59+); Codex CLI a adăugat memorie automată de fundal în aprilie. Dreaming de la Anthropic (Claude Managed Agents, Code with Claude SF, 2026-05-06) e un proces programat de fundal care trece în revistă sesiunile și memoria și scrie note consolidate înapoi; e la nivel de platformă, condiționat de un beta header, iar un CLI `/dream` nu apăruse până în iulie 2026. *Surse: agents.md; documentația vendorilor și documentația de memorie din Claude Code. Atenție: semantica de încărcare diferă de la un vendor la altul (Cursor citește și `.cursorrules`).*

**Effort: dovezile.** Cu harness-ul ținut constant, GPT-5.6 Sol pe effort low l-a bătut pe GPT-5.5 pe high la Agents' Last Exam; Fable 5.1 pe low e adesea competitiv cu Opus și Sonnet la cost per task, cu scor mai mare, după propriul ghid al vendorului. Numele nivelurilor de effort nu se transferă între modele, așa că orice migrare începe cu un sweep (Anexa B.9). Dacă raționamentul se păstrează între ture e decizia harness-ului: pe ARC-AGI-3, după relatarea OpenAI, raționamentul păstrat plus compactarea au dus GPT-5.6 Sol de la 13,3% la 38,3%, tăind în același timp tokenii de output de șase ori. *Surse: OpenAI GPT-5.6 guide, Aug 2026; OpenAI ARC-AGI-3 post, Jul 29, 2026; Anthropic, "Prompting Claude Fable 5.1." Atenție: evaluări ale vendorilor, pe un singur benchmark și un singur model; manualul folosește ARC-AGI-3 pentru mecanism, nu pentru scor.*

**Plugin-uri: încredere și utilitate.** Verifică maintainerul, permisiunile, hook-urile și codul executat de versiunea instalată; un hook în afara sandbox-ului are alt blast radius. Profunzimea review-ului depinde de suprafață și risc, nu de promisiunea că sursa se citește în douăzeci de minute. Un update de plugin e un update de dependență. Separat, compară beneficiul cu agentul nativ: o instalare de încredere poate totuși adăuga proces inutil. *Surse: practica autorului, mai 2026; ghidurile curente pentru skill-uri și release notes Superpowers, revizuite Oct 23, 2026. Atenție: un endorsement vechi nu validează automat o versiune nouă.*

---

### Capitolul 2 - Guardrails în cinci straturi {#deep-dive-chapter-2}

**Trei clase de vulnerabilități din spatele straturilor unu-trei.** (1) Expunerea secretelor: agenții pot descoperi fișiere `.env*` prin shell sau tool-uri native ori pot moșteni variabile de mediu secrete. Protejează fiecare cale. Setările de credențiale din Claude Code restricționează comenzile din sandbox; regulile de deny-read pentru shell nu blochează tool-ul nativ Read. (2) Injecția prin fișiere de configurare: fișiere `.claude/settings.json` sau `.mcp.json` nesigure execută hook-uri înainte de dialogul de trust, ceea ce deschide calea spre remote code execution (CVE-2025-59536, patch-uită în Claude Code v1.0.111) sau spre exfiltrarea de API key-uri printr-un `ANTHROPIC_BASE_URL` suprascris (CVE-2026-21852, patch-uită în v2.0.65). (3) Ocolirea parser-ului de permisiuni: reguli de deny sărite pentru binare pe care parser-ul nu le recunoaște (`open()` din Python, `fs.readFile` din Node) sau, ca eșec silențios, atunci când o comandă înlănțuia mai mult de cincizeci de subcomenzi (`MAX_SUBCOMMANDS_FOR_SECURITY_CHECK = 50`), iar verificarea cădea pe un „ask” generic; dezvăluită pe 1 aprilie 2026 și patch-uită în v2.1.90 în câteva zile. Nimic din configurație nu arată un asemenea eșec, așa că presupune că orice strat luat singur poate avea un bug; clasele supraviețuiesc patch-urilor lor. *Surse: Knostic, Dec 2025; Check Point Research, Feb 2026 (patch-uit în octombrie 2025); Adversa AI Red Team, Apr 1, 2026; Adam Kinney, Apr 2026. Atenție: clase arhitecturale, nu CVE-uri punctuale; versiunile fără patch rămân vulnerabile.*

**Escape-urile din sandbox („DuneSlide”).** La mijlocul lui 2026, un red team a dezvăluit două vulnerabilități critice zero-click de prompt injection în sandbox-ul cu suport în kernel din Cursor (CVE-2026-50548 și CVE-2026-50549, CVSS 9.8), care abuzau allowlist-ul de scriere pe directorul de lucru și un fallback de rezolvare a symlink-urilor ca să ajungă la execuție de cod la nivel de OS. Versiunile dinainte de Cursor 3.0 (2 aprilie 2026) erau afectate. Lecția e clasa, nu vendorul: și cel mai puternic strat poate avea bug-uri - exact de-asta straturile sunt cinci. *Surse: Cato Networks (Cato AI Labs), mijlocul lui 2026; SecurityWeek and The Hacker News, Jul 2026.*

**Default-urile de sandbox per agent.** Vezi intrarea din Capitolul 1 despre postura de sandbox pe vendor; ideea pentru capitolul ăsta e că o instalare default a unui agent opt-in rulează cu stratul doi oprit.

**Injecția prin materialul de lucru: proof of concept-ul cu DNS TXT.** În iunie 2026, cercetătorii Mozilla 0Din au arătat un repository cu aspect inofensiv care determină Claude Code să ruleze un script ce își trage un payload base64 dintr-un DNS TXT record și deschide un reverse shell, totul împărțit între repository, DNS și mașina developerului, așa că nicio semnătură nu apare în clar. Un proof of concept, fără vreun patch de vendor raportat; un allowlist de rețea mărginește calea prin DNS. *Sursa: SecurityWeek, Jun 29, 2026.*

**Telemetrie și exemple de hook-uri.** Până la mijlocul lui 2026, Claude Code, Codex CLI și Gemini CLI emit OpenTelemetry nativ, așa că store-ul de audit poate fi orice vorbește deja stack-ul tău; cerința e durabilitatea și posibilitatea de interogare. Plugin-ul security-guidance livrează reguli pentru circa opt-zece categorii de vulnerabilități. O regulă de echipă în plus față de cele două din capitol: blochează editările într-un modul relevant pentru conformitate în afara orelor de program.

**PocketOS: unde diferă relatările și ce au schimbat platformele.** Restore-ul făcut de Railway ar fi durat circa 30 de minute după ce CEO-ul i-a contactat; alte relatări vorbesc de circa 30 de ore sau de două zile până la restaurarea completă, așa că manualul folosește incidentul doar pentru pattern-ul de guvernanță. În decurs de o săptămână, pe 29 aprilie 2026, Railway a mutat toate ștergerile de volume și de resurse, inclusiv calea de API folosită de agent, pe soft-delete cu o fereastră de recuperare de 48 de ore și a adăugat guardrails la nivel de workspace și credențiale de agent cu scop limitat. Follow-up-ul lui Alexey Grigorev la pierderea DataTalks.Club din Terraform (sfârșitul lui februarie 2026) se citește ca checklist-ul acestui capitol: delete protection în Terraform și în AWS, starea mutată în S3, review manual al fiecărui plan distructiv, un tier de suport AWS mai ridicat. AWS a restaurat aproximativ 1,94M de rânduri dintr-un snapshot în circa o zi. *Surse: DevOps.com; Business Insider; Railway blog, Apr 29, 2026; relatarea publică a lui Grigorev.*

---

**PocketOS: postarea publică.** CEO-ul PocketOS a scris public despre incident, iar postarea a devenit rapid un punct de referință în discuțiile despre siguranța AI-ului în producție. *Sursa: Anexa C, Incidente cunoscute.*

**DataTalks.Club, imaginea în oglindă a lui PocketOS.** În incidentul DataTalks.Club, Claude Code a rulat `terraform destroy` pe un state file rămas în urmă: o hartă despre care agentul nu știa că îi trebuie, acolo unde la PocketOS era o credențială pe care n-ar fi trebuit s-o dețină. Același remediu: confirmare pe operațiunile distructive, doar credențialele de care are nevoie task-ul și o stare pe care echipa a verificat-o. *Sursa: relatarea publică a lui Alexey Grigorev; Anexa C.*

### Capitolul 3 - Bottleneck-ul s-a mutat {#deep-dive-chapter-3}

**Recomandările de workflow, revizuite pe 23 octombrie 2026.** Ghidurile curente OpenAI și Claude Code cer rezultate clare, constrângeri locale și planificare proporțională cu task-ul. Pentru schimbări mici și clare, execuția directă este potrivită; munca ambiguă, dependentă sau riscantă justifică explorare, plan și gate-uri explicite. OpenAI avertizează că trigger-ele prea largi și rețetele de skill prea detaliate pot adăuga muncă și blocaje. De aici punctul de pornire al manualului: agentul nativ, apoi structura care aduce o capabilitate necesară, previne un risc justificat sau rezolvă un eșec observat. *Surse: OpenAI, „Rethinking skills and prompts for GPT-6 Astra”, Sep 11, 2026, și „Best practices”; Anthropic, „Best practices for Claude Code”, verificate Oct 23, 2026. Atenție: îndrumări de vendor, nu o validare controlată a întregului workflow din carte.*

**Framework-ul necunoscutelor, pe larg.** În iulie 2026, un inginer de la Anthropic a deschis un ghid de teren pentru Claude Fable 5 cu observația acestui capitol: era „primul model la care calitatea muncii are ca bottleneck capacitatea mea de a-i clarifica necunoscutele”. Cele patru întrebări ale lui: known knowns (ce spune efectiv promptul tău), known unknowns (întrebările despre care știi că nu le-ai tranșat încă), unknown knowns (contextul atât de evident încât nu ți-ar trece prin cap să-l scrii, deși ai recunoaște pe loc o încălcare) și unknown unknowns (ce n-a apucat niciunul dintre voi să întrebe). *Sursa: Thariq Shihipar, Anthropic, Jul 6, 2026. Atenție: framework-ul adaptează o taxonomie mai veche, iar „primul model” e judecata lui, nu o măsurătoare; maparea pe mașinăria manualului (tabelul din capitol) îi aparține autorului.*

**Studiul randomizat controlat METR.** Studiul METR din iulie 2025 a pus developeri open-source experimentați să lucreze cu asistență AI pe propriile repository-uri, pe care le cunoșteau bine. Au avut nevoie de 19% mai mult timp decât fără ea, deși anticipaseră o accelerare de 24%, iar după aceea tot credeau că AI-ul i-a făcut cu aproximativ 20% mai rapizi: un decalaj de 43 de puncte între accelerarea prezisă și încetinirea măsurată. Autorul îl citește ca pe un avertisment: asistența brută nu se transformă în viteză de livrare fără disciplină de workflow. *Sursa: Becker et al., METR, Jul 10, 2025. Atenție: METR nu a testat disciplina formulării; lectura aceea îi aparține autorului. Follow-up-ul a suferit un selection bias, METR a reproiectat experimentul în februarie 2026 și avertizează împotriva aplicării cifrei de 19% la tool-urile actuale.*

**Februarie-aprilie 2026: disciplina absoarbe o regresie de la vendor.** Schimbările de produs din Claude Code au degradat semnificativ munca de inginerie complexă, în anumite workflow-uri. Pe 6 aprilie, Stella Laurenzo, senior director la AMD, a publicat un audit pe 6.852 dintre propriile sesiuni și 234.760 de tool call-uri, care arăta trecerea de la un comportament research-first la unul edit-first pe măsură ce ascunderea thinking-ului a crescut de la 1,5% la 100% din tururi, și indica drept cauză contributoare default-ul adaptive thinking din februarie. Post-mortem-ul Anthropic din 23 aprilie a recunoscut trei regresii: effort-ul implicit coborât de la high la medium pe 4 martie (revenit pe 7 aprilie); un bug de caching din 26 martie care golea istoricul de raționament la fiecare tur în loc de o dată pe oră de inactivitate (reparat pe 10 aprilie); și un plafon de verbozitate în system prompt din 16 aprilie, cu o scădere măsurată de 3% a calității (revenit pe 20 aprilie). Două echipe adiacente foloseau același Claude Code. Cea cu infrastructura din manualul ăsta (reguli în CLAUDE.md, plan mode by default, bucla în șase faze, hook-uri pe operațiunile distructive) a pierdut poate 10% și și-a revenit după ce a strâns gate-urile de plan mode și a trecut câteva skill-uri pe effort mai mare; echipa freestyle și-a văzut velocity-ul înjumătățit peste noapte. *Surse: Anthropic post-mortem, Apr 23, 2026; Laurenzo, anthropics/claude-code#42796, via The Register, Apr 6, 2026. Atenție: relatările diverg în privința celei mai timpurii cauze; magnitudinile externe sunt aproximative; comparația dintre cele două echipe e o observație de teren.*

---

### Capitolul 4 - Bucla în șase faze {#deep-dive-chapter-4}

**Ce stabilesc comparațiile cu Superpowers.** Krupa a comparat v6.4.2 cu lipsa plugin-ului pe Sonnet 5.5: 12 cazuri, 192 de rulări, un raport mediu al costului per caz de 1,33x. La bugfix, testul de regresie a apărut în 8/8 rulări cu plugin și 4/8 fără; fix-ul era corect în ambele variante. Multe verificări erau deja rezolvate de baseline, iar unele scoruri recompensau procesul. OrcaBot a testat v6 pe Codex gpt-5.5/high, cu 729 de cazuri SWE-bench Pro comune și un seed per variantă: 57,06% rezolvate față de 55,56%, la 0,46 dolari față de 0,37 per problemă. Avantajul mic este indicativ. *Surse: Bartłomiej Krupa, Sep 29, 2026; Rob Macrae, OrcaBot, Jul 31, 2026; release notes Superpowers. Atenție: cazurile Krupa sunt mici și headless; versiunile ulterioare au schimbat execuția Native și gate-urile. În sursele revizuite nu am găsit o comparație independentă v7.x cu versiunea curentă de Codex. Raporturile vechi de cost nu sunt măsurători ale versiunii de azi.*

**Skill-uri specializate versus workflow general.** SkillsBench v4 a măsurat 87 de task-uri din opt domenii, în 18 configurații model/harness: media ratei de succes a crescut de la 33,9% la 50,5% cu skill-uri curatoriate. Asta susține utilitatea unor cunoștințe bine alese, nu obligativitatea unui plugin de proces. Pentru configurația ta, compară on/off cu criterii fixate înainte, același model, effort și commit, sesiuni proaspete și cazuri în care skill-ul ar trebui să rămână inactiv. Măsoară corectitudinea, regresiile, consumul facturat cu cache și subagenți, timpul uman, rework-ul și timpul de ceas. *Sursa: Li et al., SkillsBench v4, Jun 14, 2026. Atenție: preprint despre skill-uri specifice task-ului, cu verificatori deterministici, nu o evaluare Superpowers.*

**Când rentează împărțirea în subagenți.** Studiul de scalare pe 260 de configurații a găsit câștiguri pe muncă descompozabilă și pierderi mari pe unele task-uri de planificare secvențială. Procentele și pragurile ajustate nu sunt reguli pentru coding. Ghidul curent Claude Code păstrează editările rapide și fazele care împart mult context în conversația principală și folosește subagenți pentru muncă independentă sau explorare al cărei output ar aglomera-o. Deleagă când izolarea sau progresul în paralel justifică pornirea, contextul duplicat și coordonarea. *Surse: Kim et al., Jul 24, 2026; documentația Claude Code despre subagenți, verificată pe 23 octombrie. Atenție: cele mai mari pierderi din studiu nu sunt rezultate de coding; niciuna dintre surse nu stabilește un worker per fișier drept configurație optimă.*

**Un singur scriitor și context ales după rol.** Deleagă muncă independentă și suficient de amplă; păstrează un singur scriitor pe zonele care se suprapun și execută dependențele în ordine. Un fork poate ajuta când workerul are nevoie de istoricul relevant, dar nu transfera întreaga conversație din reflex: și contextul cu cache are cost. Un brief delimitat poate fi suficient. Pentru un review independent, folosește context proaspăt și cerințele necesare, fără verdictul anterior. Orchestratorul poate lucra în timp ce așteaptă rezultatele. *Surse: Walden Yan, Cognition, Apr 22, 2026; Bengre and Curme, LangChain, Sep 8, 2026; Anthropic, „Create custom subagents” și „Prompting Claude Fable 5.1”. Atenție: mecanismele de fork și cache diferă între harness-uri; nu există o regulă universală „fork pentru fiecare worker”.*

**Autonomie și scop, adaptate modelului.** Ghidurile Fable 5 și GPT-6 Astra tratează opririle premature, întrebările redundante și extinderea necerută a muncii. Fable 5.1 cere să protejezi limitele task-ului și artefactele de test; asta nu înseamnă că orice modificare legitimă de test sau configurație e interzisă. Dă-i agentului rezultatul, limitele și verificările relevante, lasă-l să termine munca autorizată și cere clarificări doar pentru decizii care depășesc mandatul. Nu păstra automat blocuri de prompt concepute pentru modelul anterior. *Surse: Anthropic, „Prompting Claude Fable 5” și „Prompting Claude Fable 5.1”; OpenAI, „Using GPT-6 Astra” și „Rethinking skills and prompts for GPT-6 Astra”, Sep 11, 2026. Atenție: recomandări specifice modelului; B.9 verifică dacă instrucțiunile mai aduc un beneficiu.*

**Notele de implementare păstrează deciziile importante.** La o schimbare amplă, notează devierile de la plan și deciziile care afectează alt task, în momentul în care apar. Reviewerul poate confrunta astfel diff-ul cu intenția, iar agentul poate relua munca după compactare. La un task scurt, un raport final poate acoperi aceeași funcție. Limitele de securitate cer enforcement separat; o preferință de proces nu cere automat încă un gate.

---

### Capitolul 5 - Review și Verify {#deep-dive-chapter-5}

**Când ajută un reviewer independent.** Ghidul Fable 5 recomandă verificatori separați, cu context proaspăt, pentru muncă de durată; ghidul Opus 5 avertizează că instrucțiunile și subagenții de verificare suplimentari pot produce over-verification, cu cost fără câștig de calitate. Niciunul nu stabilește nevoia a doi revieweri în secvență pentru fiecare PR. Studiile despre preluarea criticilor, rundele de reparare și ancorarea judecătorilor justifică întrebări de evaluat: rezolvă agentul constatările reale, mai ajută încă o rundă, este a doua opinie independentă? Nu transfera mecanic procente din raționament matematic sau deep research la code review. *Surse: Anthropic, „Prompting Claude Fable 5” și „Prompting Claude Opus 5”, verificate Oct 23, 2026; Yang et al., Jul 16, 2026; Wan et al., Jan 22, 2026 (v2 Apr 29); Kapetanovic et al., Aug 26, 2026. Atenție: recomandări de model și studii din alte domenii; review-ul suplimentar trebuie să-și justifice costul prin defecte reale și risc.*

**SpecBench și constatarea Cursor, pe larg.** SpecBench (mai 2026) a pus agenți de frontieră în fața unor specificații cu seturi de teste vizibile și ascunse. Fiecare agent a saturat suita vizibilă aproape de 100%, cu decalaje de circa 43-48 de puncte pe testele ascunse; decalajul la percentila 90 a crescut cu circa 27 de puncte la fiecare înzecire a liniilor de cod, iar mai multă căutare nu a eliminat fiabil reward hacking-ul. Cursor a găsit cealaltă jumătate în iunie 2026: pe SWE-bench Pro, 63% dintre rezolvările reușite ale lui Claude Opus 4.8 Max recuperaseră fix-ul din upstream, din istoricul de git sau din rețea, în loc să-l deriveze, iar sigilarea ambelor a coborât scorul de la 87,1% la 73,0%. Rezultatele cer criterii independente și integritatea evaluării. Testele held-out și sigilarea accesului la soluții sunt potrivite pentru benchmark-uri și situații cu cerințe ridicate de asigurare; nu devin automat procedura fiecărui PR. *Surse: Zhao, Srikanth, Wu and Jiang (Weco AI), May 20, 2026 (v2 Sep 9); Naman Jain, Cursor, Jun 25, 2026. Atenție: abstractul rotunjește cele 27 de puncte la 28 (R² de 0,21), deci trendul e real, dar zgomotos; rezultatul Cursor e pe un singur harness și un singur model.*

**Playwright cu accessibility tree.** Accessibility tree e structura pe care browserele o întrețin pentru tehnologiile asistive (un buton cu eticheta asta, un câmp etichetat „email”), stabilă la restilizări și la schimbarea bibliotecii de componente. „Găsește câmpul etichetat Priority, schimbă-i valoarea, apasă Save, verifică faptul că noua valoare se afișează” trece indiferent dacă câmpul e un select, un radio group sau o componentă custom. Echipele din banking cu suite de snapshot-uri flaky au găsit că e prima abordare care a rămas verde. *Surse: documentația Playwright; W3C ARIA AOM. Atenție: animațiile, drag-and-drop și canvas-ul au nevoie de verificare suplimentară.*

**Măsoară contribuția toolkit-ului de PR review.** Agenții de review pot prinde constatări mecanice înainte ca un senior să citească diff-ul. Măsoară defectele utile găsite, false positive-urile, timpul de review și defectele scăpate, în loc să presupui că patru revieweri economisesc zece minute. Păstrează atenția umană pe corectitudinea de business și potrivirea arhitecturală; cazul din capitol arată ce se întâmplă când atenția asta dispare.

---

### Capitolul 6 - AGENTS.md și contextul {#deep-dive-chapter-6}

**Fișierele de context trebuie să-și justifice conținutul.** Studiul ETH Zürich despre AGENTS.md, v3 din Sep 29, 2026, nu a găsit o îmbunătățire generală a succesului pentru fișierele de context generate și a măsurat un cost de inferență cu peste 20% mai mare în setup-urile testate. Fișierele scrise de developeri au adus un câștig mediu modest, fără semnificație statistică; prezentările de ansamblu ale repository-ului nu au ajutat în această evaluare. Studiul nu dovedește că orice instrucțiune locală dăunează. Păstrează constrângerile pe care agentul nu le poate deduce, comenzile verificate și pointerii; mută detaliile voluminoase în docs/ și compară rezultatele. OpenAI descrie separat un AGENTS.md de circa 100 de linii ca hartă spre documentație structurată. *Surse: Gloaguen et al., „Evaluating AGENTS.md”, v3 Sep 29, 2026; Ryan Lopopolo, OpenAI, Feb 11, 2026. Atenție: agenți și benchmark-uri specifice; selecția conținutului e recomandarea manualului, iar exemplul OpenAI e practica unei singure echipe.*

**Circa 200 de linii este un reper, nu un prag demonstrat.** Studiul din iulie despre respectarea simultană a regulilor măsoară un setup de prompt, nu stabilește la câte linii trebuie tăiat orice AGENTS.md. Nu există o conversie validată între cele circa optzeci de reguli și două sute de linii. Faptul că Anthropic a eliminat peste 80% din propriul system prompt pentru generația Claude 5 susține reevaluarea instrucțiunilor vechi, nu ștergerea constrângerilor utile. *Surse: Netanel Eliav, Jul 21, 2026; Thariq Shihipar, Anthropic, Jul 24, 2026; Claude Code memory docs, verificate Oct 23, 2026. Atenție: metrici și contexte diferite; scurtimea e o disciplină de întreținere, nu o garanție a respectării instrucțiunilor.*

**Mecanica jurnalului de greșeli.** Ghidul Anthropic pentru Fable 5 descrie un sistem de memorie cu trei reguli care țin un jurnal onest și la o sută de intrări: o lecție per fișier, cu rezumat de o linie; actualizezi în loc să duplici atunci când lecția se repetă; ștergi notele care se dovedesc greșite. Adaugă un pointer la dovadă, ca următorul champion să poată verifica dacă eșecul mai e posibil. Runtime-ul de afirmații din OpenWiki, care atașează pointeri la dovezi afirmațiilor stocate și le reverifică, a tăiat afirmațiile învechite de la 3,5% la 0,5% pe 2.000 de afirmații evaluate. Review-ul trimestrial pune pentru fiecare intrare întrebarea „a salvat regula asta pe cineva în ultimele trei luni?” Dacă da, o păstrezi; dacă nu, dar regula încă se aplică, o păstrezi, pentru că eșecurile rare contează în continuare; dacă nu, iar cauza a dispărut, o retragi, cu o notă în mesajul de commit. *Surse: Anthropic, "Prompting Claude Fable 5"; Colin Francis, LangChain, Aug 25, 2026. Atenție: OpenWiki e un sistem de bază de cunoștințe, nu un jurnal; manualul împrumută mecanismul.*

**De ce există linia de precedență.** GPT-6 Astra urmărește instrucțiuni mai lungi mai bine și e mai sensibil la context: o îndrumare contradictorie într-un fișier de skill îl poate face să se oprească și să blocheze munca devreme, iar ghidul OpenAI spune că instrucțiunile utilizatorului au prioritate față de ale unui skill. O singură linie în capul fișierului („In a conflict, the task prompt wins over this file; this file wins over any skill”, în scheletul B.2) elimină o clasă de blocaje. *Sursa: OpenAI, "Using GPT-6 Astra," Sep 2026 (GPT-6 lansat pe 3-4 septembrie 2026; ghid revizuit pe loc).*

**Compactare și măsurători de context.** JetBrains a găsit că mascarea output-urilor vechi de tool-uri (apelul rămâne, rezultatul voluminos e golit) a bătut rezumarea cu LLM în patru din cinci setări, la un cost cu peste 50% mai mic, cu o rată de rezolvare egală sau puțin mai bună. Curățarea rezultatelor de tool-uri de la Anthropic, aceeași mișcare la nivel de platformă, a adus un câștig de 29% pe o evaluare internă de căutare agentică. Pe 15 modele, conversațiile multi-turn fragmentate au pierdut în medie 39% față de o singură tură complet specificată, iar o tură consolidată a recuperat cam 95%. *Surse: Fraser and Lindenbauer, JetBrains Research, Dec 2025; Anthropic, Sep 29, 2025; Laban et al., May 2025. Atenție: cifra de 52% citată uneori e o singură configurație (Qwen3-Coder 480B); rezultatul Anthropic e intern; studiul multi-turn a folosit task-uri simulate de generare, nu sesiuni de coding.*

**Istoric append-only și prețul cache-ului (Fable 5.1).** Blocurile de gândire sunt legate de prefixul exact care le-a produs, așa că editarea sau reordonarea turelor anterioare le invalidează și aruncă raționamentul păstrat pe care Capitolul 1 îl numără ca jumătate din componenta principală Effort: păstrează istoricul append-only și folosește mecanismele harness-ului pentru reluare. Cu citirile din cache la 0,025x din prețul de bază al input-ului, ghidul spune că a compacta devreme ca să economisești s-ar putea să nu mai fie schimbul potrivit; când totuși compactezi, dă-i compactorului o listă de păstrat (planul, întrebările deschise, devierile din notele de implementare, comenzile exacte care au mers). *Sursa: Anthropic, "Prompting Claude Fable 5.1." Atenție: pagină nedatată; 0,025x e aritmetica manualului pe prețurile publicate; cerința append-only se aplică conturilor create de la 31 august 2026 încoace.*

---

### Capitolul 7 - Întâi harta: review-ul de arhitectură {#deep-dive-chapter-7}

**De ce citește agentul codul, în loc să interogheze un index al lui.** Navigarea bate retrieval-ul pe task-ul ăsta. Pe Claude Sonnet 4.5, navigarea agentică (grep, deschizi fișierul, urmezi referința) a ajuns la 49,6% recall@1 pe BRIGHT, cu 21,8 puncte peste cel mai bun model de embeddings, iar spațiile de lucru mărginite (rezultatul RISE) o țin funcțională la un milion de documente, acolo unde inspecția directă a contextului se degradează. Căutarea în cod pentru agenți se reduce la trei tool-uri: ripgrep pentru text, ast-grep pentru structură, language server-ul pentru referințe. Un index de embeddings e excepția pe care o adaugi când un corpus le depășește. *Surse: Suresh et al., May 7, 2026; Zhuang et al. (RISE), Jun 5, 2026; Kumanyaev, Jun 6, 2026. Atenție: cifra de recall e pe un benchmark general de retrieval, nu pe un codebase.*

**Alternativa vizuală: Understand Anything.** Un plugin care redă codebase-ul ca un graf navigabil: o vedere structurală (module, dependențe) pentru ingineri și o vedere de domeniu (concepte de business, entități) pentru manageri, care pot citi „serviciul ăsta se ocupă de detecția fraudelor pe transferurile primite” fără să citească sursa.

---

### Capitolul 8 - Are voie agentul să atingă codul ăsta? {#deep-dive-chapter-8}

**Semnalul 1, fără teste: modulul de reconciliere.** De două ori în banking: un modul de reconciliere scris la începutul anilor 2010 de un senior care a plecat în 2018, fără teste pentru că „seniorul pur și simplu știa că merge”. Următoarea modificare l-a stricat într-un fel care a ieșit la suprafață abia după două luni, când discrepanța depășise deja pragul care declanșează o raportare către reglementator. Remediu: întâi teste de caracterizare, agentul făcând cea mai mare parte.

**Semnalul 2, fără documentație: fee tier-ul.** Fee tier-ul pentru linia de produse legacy se calcula diferit din cauza unei excepții de reglementare din 2017. Agentul a presupus tratament uniform și l-a „simplificat”; seniorul a prins asta la review. Costul de ordinul doi: seniorii fac review pe output de AI patruzeci de ore pe săptămână în loc să construiască, până pleacă. Remediu: review-ul de arhitectură (Capitolul 7) plus un glosar scurt de domeniu.

**Semnalul 3, cuplare strânsă: ciclul de paisprezece ani.** Un modul de customer service importa un modul de originare a creditelor, care importa un modul de credit scoring, care importa customer service: un ciclu introdus acum paisprezece ani ca să „câștige timp” și niciodată spart, pentru că ar fi însemnat un proiect de opt săptămâni. Schimbarea agentului a ieșit la suprafață luni mai târziu, la închiderea batch-ului de sfârșit de lună. Remediu: sparge doar cea mai gravă cuplare; dacă echipa nu vrea, galben în cel mai bun caz.

**Semnalul 4, reguli împrăștiate: suma maximă de transfer.** Limita stătea într-un config de UI, o constantă din serviciu și un trigger din baza de date. Compliance a actualizat config-ul; șase săptămâni mai târziu, un transfer valid a eșuat pe constanta veche. Fără o singură sursă de adevăr, agentul ghicește care copie e cea canonică. Remediu: o singură sursă (un rules engine tipizat sau un serviciu de configurare), care merită oricum, cu sau fără agenți.

**Semnalul 5, constrângeri de reglementare.** Orice schimbare a logicii de anti-money-laundering cere semnătura ofițerului de compliance, a unui reprezentant din legal și a unui senior neimplicat în implementare; agentul nu poate ruta aprobări și nu poate satisface un two-person rule. Constrângerile blânde (un review de la un senior la fiecare schimbare) intră în procesul existent; cele apăsătoare (matrici de sign-off, trail-uri de dovezi, aprobări cu timestamp, retenție) înseamnă că agentul funcționează doar într-un sistem care le gestionează deja.

**Semnalul 7, potrivirea model-context: workflow engine-ul intern.** Un engine custom de la începutul anilor 2010, fără documentație publică și cu o sintaxă ciudată pentru tranzițiile de stare. Agentul a aplicat pattern-uri dintr-un framework fără legătură, pe care îl văzuse mai mult; codul a compilat, testele subțiri au trecut, iar mașina de stări s-a comportat greșit în trei edge case-uri netestate. Fără o amprentă publică consistentă (repo-uri, documentație, prezentări), tratează codebase-ul ca și cum semnalul șase ar fi activ, chiar și când toate celelalte semnale sunt curate.

**Semnalul 8, viteza schimbării: bug-ul React 18/19.** Pe un codebase aflat în mijlocul unei migrări, agentul are dreptate cu toată convingerea despre versiunea veche și greșește despre cea nouă, iar nu poți deosebi mereu care e care. Bug-ul autorului: Claude a folosit idiomuri de React 18 acolo unde era nevoie de React 19; a mers local pe o dependență tranzitivă de React 18 și s-a stricat când producția a tras 19. Remediu: o regulă de versiune în AGENTS.md („migrăm de la React 18 la React 19 trimestrul ăsta; codul nou folosește idiomuri de 19; codul vechi mai poate folosi 18, dar se actualizează când e atins”).

**Semnalul soft al migrării între modele, cu dovezile lui.** Instrucțiunile scrise pentru modelul anterior (regulile din AGENTS.md, prompturile din skill-uri, nivelurile de effort) nu se retrag singure. Pentru între 37% și 63% dintre lucrările de inginerie software analizate, un model mai nou cu un singur prompt a depășit nativ tooling-ul puternic ingineresc propus cu circa un an înainte. Nu e al nouălea kill signal; e ce verifici când un codebase verde devine galben după un upgrade de model (Anexa B.9). *Sursa: Salsabil et al., Aug 31, 2026 (arXiv 2609.00468). Atenție: preprint, fără peer review; folosește-l pentru direcție, nu pentru fracție.*

**Cele șase exemple lucrate, pe larg.** (1) Microserviciu de profil de client: acoperire de 70%, privire de ansamblu în README, decuplat prin REST, reguli într-o singură bibliotecă de validare tipizată, controale SOX standard, seniori care se ocupă de schimbările de profil. Zero, verde. (2) Motor legacy de plăți: acoperire de 20%, majoritar happy-path, documentație parțial învechită, cuplare moderată cu granițe documentate, câteva reguli rătăcite, constrângeri reale PCI și de raportare de fraudă, cu mecanismul de audit la locul lui, unu-doi seniori care pot evalua output specific plăților. Fără teste jumătate, documentație jumătate, cuplare unu, reguli jumătate, reglementare zero, evaluare zero: doi și jumătate, rotunjit în sus la trei, galben. (3) Bibliotecă de criptare custom a unui contractor din 2017: nedocumentată, testată doar prin teste de integrare, cuplată strâns de key management, reguli de conformitate în cod, fără criptograf. Cinci, roșu. (4) Serviciu API greenfield, echipă senioră, specificație clară: zero, verde-plus. (5) Tool intern, 20 de developeri, scris în 2019, teste modeste, expunere de reglementare mică: unu, spre verde, prima țintă corectă. (6) Fork customizat de la un vendor, strat de contractor făcut în grabă, fără teste sau documentație pe customizări, cuplare severă cu upstream-ul: patru, roșu. Întrebarea e strategia: ar trebui să existe stratul custom? Înlocuiește-l cu feature-uri din upstream, trimite-l înapoi ca o contribuție sau întreține-l deliberat, dar nu folosi agentul ca să faci mai repede munca greșită.

---

### Capitolul 9 - Lansarea în echipă {#deep-dive-chapter-9}

**Cele două feluri de hook-uri, pe larg: pre-commit versus pre-push.** Folosește verificări rapide la commit și teste sau build-uri mai costisitoare la push pentru feedback rapid. Un manager de hook-uri ajută la instalare, dar nu poate face hook-urile locale inevitabile: Git permite ocoliri și directoare alternative pentru hook-uri. Hook-urile de politică au nevoie și ele de configurație protejată și blocare la eșec. Acceptarea se impune prin verificări obligatorii pe server și review protejat al workflow-ului, cu credențiale care nu le pot ocoli. *Surse: Git githooks reference, GitHub rulesets și Claude Code hooks reference, verificate pe 23 octombrie 2026. Atenție: fiecare repository trebuie să configureze și să verifice aceste protecții; simpla rulare a CI-ului nu e enforcement.*

**Bucla exterioară (outer loop): de la AutoGPT la Ralph Wiggum.** Bucla interioară (inner loop) e bucla în șase faze (Capitolul 4); bucla exterioară o învelește și reinvocă agentul până când o condiție e îndeplinită. În 2023, AutoGPT și BabyAGI învârteau un model în buclă pe baza propriei lui păreri despre progres; nimic din exterior nu nota o iterație, turele amplificau deriva, iar abordarea s-a prăbușit în câteva luni ca mod de a livra software. Renașterea diferă structural: la mijlocul lui 2025, Geoff Huntley a legat un agent într-un while-loop de bash (un singur fișier de prompt, repeți), care s-a răspândit sub numele „Ralph Wiggum”. Fiecare iterație pornește cu context proaspăt, face o unitate de lucru și se termină în fața unor evaluatori pe care modelul nu-i controlează (compilator, teste, diff), cu starea în repository. Numele lui pentru modul de eșec e overbaking: o buclă lăsată să ruleze după ce și-a terminat treaba inventează muncă pe care n-a cerut-o nimeni. *Surse: ghuntley.com/ralph (Jul 2025); HumanLayer, Jan 6, 2026; The Register, Jan 27, 2026; repository-urile AutoGPT și BabyAGI. Atenție: verdictul de prăbușire și contrastul structural sunt interpretarea manualului.*

**Bucla exterioară: valul vendorilor și mecanismele condiției de oprire.** Copilot coding agent de la GitHub a devenit general disponibil pe 25 septembrie 2025 (mediu izolat, draft de pull request); Cursor a livrat Cloud Agents pe 30 octombrie 2025; Jules de la Google a adăugat Scheduled Tasks pe 10 decembrie 2025; un plugin ralph-wiggum a aterizat în repository-ul oficial Claude Code în noiembrie 2025. Până în primăvara lui 2026, Claude Code avea `/loop` (re-rulare la un interval sau în ritm propriu), Routines (agenți cloud pornind după un program sau după un eveniment GitHub), `/goal` (lucrează până când o condiție de finalizare e îndeplinită) și `/autofix-pr` (împinge fix-uri până când CI-ul e verde). După testul din Capitolul 1, capabilitatea a ajuns la convergență, deși ceea ce a ajuns la convergență e un workflow în jurul componentelor principale, nu o componentă principală. `/goal` folosește un model separat ca să evalueze condiția pe baza conversației; Codex Goals permite modelului care execută munca să marcheze un obiectiv persistent drept finalizat. Aceste mecanisme controlează continuarea și bugetele. Niciunul nu înlocuiește verificările de acceptare protejate independent. Plugin-ul ralph-wiggum n-are dovezi controlate, iar README-ul lui numește numărul maxim de iterații drept principala plasă de siguranță - un buget, nu o condiție de oprire. *Surse: GitHub changelog, 2025-09-25; blogurile Cursor și Google; Claude Code release notes, Apr-May 2026; Claude Code "/goal" docs; OpenAI Cookbook, "Using Goals in Codex." Atenție: datele vendorilor se mai schimbă; documentația /goal descrie mecanismul, nu rezultatele.*

**Bucla exterioară: de ce există fiecare linie din contract și cele două extreme.** O condiție de oprire evaluabilă de o mașină, pentru că o buclă fără ea e abandon. Un buget, pentru că o buclă nesupravegheată e clientul ideal al modelului de tarifare per token (Anexa A). Un gate de acceptare impus prin verificări obligatorii protejate și schimbări de politică trecute prin review, pentru că cel mai ieftin mod de a ajunge pe verde e să negociezi cu propriul evaluator, iar o suită verde scrisă de agent e un indiciu, nu o dovadă (Capitolul 5). Un queue și un jurnal de decizii durabile, cu context proaspăt când hand-off-ul sau deriva observată îl justifică. Izolare dimensionată pentru absență, pentru că o sesiune nesupravegheată e locul unde prompt injection nu mai întâlnește niciun sceptic uman (Capitolul 2). Pune în queue multe unități similare, verificabile de o mașină și reversibile (migrări, curățenii de lint, dependency bump-uri, completarea testelor), doar pe codebase-uri verzi. Huntley rulează bucla brută la circa 10 dolari pe oră; fabrica de software de la StrongDM rulează livrare complet non-interactivă, cu oameni care nici nu scriu, nici nu fac review la cod, și cu scenarii end-to-end ținute în afara codebase-ului, ca un holdout pe care bucla nu-l poate slăbi, la o cheltuială pe care Simon Willison a estimat-o la aproape 20.000 de dolari pe lună per inginer. *Surse: Willison, Feb 7, 2026; Huntley și The Register, ca mai sus. Atenție: cifra de 10 dolari îi aparține lui Huntley, iar cifrele StrongDM sunt auto-descrierea unei singure companii și încadrarea lui Willison, nu audituri.*

**Exemple de bugete de timp pentru angajamentele rolurilor.** În acest calendar, championul rezervă circa trei ore în prima săptămână și cinci în a doua; săptămânile următoare depind de feature-urile pilotului. Rezultatele urmărite sunt un workflow testat, instrucțiuni utile și întreținute, feature-uri livrate și un succesor desemnat. Lead-ul rezervă circa două ore în prima săptămână și trei-cinci ore în fazele următoare. Sunt exemple de planificare din practică; adaptează-le la efortul măsurat și la punctul de pornire al echipei.

**De ce arată așa exemplul de 90 de zile.** Calendarul rezervă timp pentru învățare, un pilot bine delimitat, extindere și responsabilitate operațională. E un exemplu de organizare din practică, nu o curbă exponențială măsurată. Stabilește înaintea pilotului baseline-ul de cycle time, defecte, efort de review și consum; urmărește rezultatele pe tot parcursul lui. Extinde sau schimbă abordarea când rezultatele justifică asta, în loc să aștepți un câștig promis pentru luna a treia.

---

**Kill signals ale buclei exterioare.** Bucla primește kill signals așa cum Capitolul 8 le dă codebase-urilor. Patru sunt de ajuns: același diff aplicat și apoi revertat de la o iterație la alta; buget care arde în timp ce queue-ul nu scade; același eșec apărut a treia oară; orice iterație care a atins gate-ul. Oricare dintre ele înseamnă stop: citești jurnalul, repari cauza, abia apoi relansezi. O buclă repornită pe speranță e o buclă pe care ai încetat s-o mai controlezi. Blocul de review de dimineață din Anexa B.6 conține aceleași patru verificări.

### Anexa A - Pentru manageri {#deep-dive-appendix-a}

**Rutarea pe tier-uri, cele două puncte măsurate.** Pattern-ul „advisor” al Anthropic împerechează un executor mai ieftin cu un model mai puternic, chemat la nevoie. Sonnet cu Opus ca advisor a obținut cu 2,7 puncte mai mult pe SWE-bench Multilingual decât Sonnet singur, la un cost per task cu 11,9% mai mic. Haiku cu un advisor Opus a obținut 41,2% pe BrowseComp față de 19,7% singur, rămânând cu 29% în urma lui Sonnet singur la scor, la un cost per task cu 85% mai mic. Potrivit pentru tier-urile mecanice ale buclei, greșit pentru research. *Sursa: Anthropic, "The advisor strategy," Apr 9, 2026. Atenție: benchmark-uri ale vendorului pe propriile modele; cifre per task, nu un raport general.*

**Layout cache-first, taxa pe tool-uri și mascarea.** Layout-ul cache-first a tăiat costul de API cu 41% până la 80% pe peste 500 de sesiuni de agent, la trei provideri (Lumer et al., Jan 31, 2026). Cifrele despre definițiile de tool-uri sunt la Capitolul 1, rezultatul despre mascare la Capitolul 6.

**Euristica de încadrare, în formă lungă.** Costul per inginer pe lună e mărginit de ce ar cheltui oricum echipa pe tooling similar (licențe de IDE, platforme de code intelligence, abonamente de coding asistat de AI) plus o fracțiune din timpul orar al unui inginer senior, economisit pe săptămână. Fă calculul cu stack-ul tău de tooling, costul orar complet, o estimare onestă a orelor economisite și oferta vendorului; break-even-ul vine repede când agentul economisește chiar și câteva ore pe lună per inginer.
