# Ship It With AI

### Un manual practic pentru livrarea de software cu agenți AI

**Mihai Cvasnievschi**

---

> Agenții scriu codul.
> Tu înțelegi problema.
> Tu răspunzi în continuare pentru judecată.

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

**Ce ar fi putut schimba rezultatul.** Credențiale cu drepturi limitate, restricții aplicate efectiv asupra tool-urilor și gate-uri de aprobare protejate ar fi putut împiedica apelul distructiv, dacă îi acopereau calea de execuție. Logurile, alertele și un răspuns testat ar fi putut scurta detectarea și recuperarea; înregistrarea unui eveniment nu îl previne. Relatările publice nu stabilesc toate controalele pe care le configurase PocketOS. Capitolul 2 separă prevenția de detectare și îți cere să testezi limita pe care vrei să te bazezi.

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

**Cum se citește.** Manualul e scris pentru senior engineer - staff, principal sau tech lead - care va pune practica asta pe picioare într-o echipă reală și o va apăra în sus; oricine livrează software cu AI îl poate urmări. Citește-l în ordine pentru argumentul complet sau alege un traseu care se încheie cu un rezultat inspectabil. Anexa D cuprinde dovezile extinse și limitele lor.

| Obiectiv imediat | Traseu | Rezultat |
|---|---|---|
| Înțelege abordarea | Prolog → Capitolele 1–3 | O comparație de capabilități și controalele/workflow-ul necesare task-urilor tale |
| Pregătește un repository nefamiliar | Capitolele 2 → 7 → 6 → 8 | O hartă revizuită, instrucțiuni utile și condițiile task-ului |
| Livrează o schimbare | Capitolele 3 → 4 → 5, cu [pachetul Wire](/companion/wire-v1.zip) | Comportament acceptat, dovezi de verificare și predare către producție |
| Rulează un pilot de echipă | Capitolele 8 → 9 → Anexa A | Un pilot delimitat, fișă de măsurare și decizie de extindere/oprire |

---

# Partea I - Arhitectura

> *Controlul capabilității: ce poate agentul să știe și ce poate să facă.*

---

## Capitolul 1
## Ce este un agent

*La finalul capitolului poți inspecta un coding agent actual prin nouă capabilități recurente și poți compara felul în care două sisteme le implementează sau le asigură.*

**TL;DR**

- Un coding agent e un model într-un harness. Cele nouă componente principale de mai jos formează un framework practic de inspecție, nu o teoremă despre anatomia universală a agenților.
- O capabilitate poate fi integrată, asigurată din exterior, absentă sau implementată diferit. Aceste diferențe, în primul rând cele de sandbox, schimbă controalele de care ai nevoie.
- Evaluează modelul și harness-ul împreună, pe task-urile tale. La orice agent nou, pune câte o întrebare pe componentă principală.

---

### Ce este o componentă principală a unui coding agent? {#what-is-a-primitive}

**Un agent înseamnă un model plus un harness, iar harness-ul e un set restrâns de părți care se repetă.**

Agenții de cod actuali expun în mod repetat capabilitățile de mai jos, dar felul în care le împachetează și disponibilitatea lor diferă. Aici, „componentă principală” înseamnă o capabilitate pe care merită s-o inspectezi, nu obligația ca fiecare produs s-o livreze într-un pachet separat și configurabil. Fiecare card se încheie cu o întrebare; „absentă” și „asigurată din exterior” sunt răspunsuri valide.

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

*Figura: Componentele principale și harness-ul, ca framework de inspecție. Compară stratul de decizie al agentului cu enforcement-ul real la nivel de OS și rutele acoperite. Inspectează separat memoria scrisă de echipă și cea scrisă de agent și verifică setările de effort și raționamentul păstrat în modelul/clientul ales. O capabilitate poate lipsi sau poate fi asigurată din exterior; un subagent e o altă instanță constrânsă de agent, când harness-ul o oferă.*

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

**Ce este: două controale livrate ca pereche - regulile agentului însuși și enforcement-ul sistemului de operare.**

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

O integrare MCP poate fi reutilizată în clienți compatibili. Verifică versiunea de protocol negociată, capabilitățile, transportul și autentificarea: faptul că două produse suportă MCP nu înseamnă că orice server va funcționa neschimbat cu ambele.

*Întreabă: Vorbește MCP și cât de bună e integrarea?*

---

### Memory {#memory}

**Ce este: ce se păstrează de la o sesiune la alta, în două jumătăți.**

Prima o scrie echipa: fișiere de instrucțiuni ale proiectului, cum ar fi AGENTS.md. Descoperirea, aria de aplicare și precedența depind de client; unele cer configurare sau încărcare explicită (Capitolul 6). A doua o scrie agentul pentru sine: comenzi de build pe care le-a dedus, concluzii de debugging, preferințe inferate.

*Întreabă: Citește un fișier de memorie partajat de echipă la începutul sesiunii și își ține și o memorie proprie?*

---

### Effort {#effort}

**Ce este: cât de mult gândește modelul înainte să acționeze - cea mai nouă componentă principală, care își câștigă locul prin levier.**

Unde modelul și clientul oferă controale de effort, compară setările disponibile pe task-uri reprezentative. Mișcă și costul, și calitatea, în ambele direcții: prea jos, și agentul sare peste research-ul de care avea nevoie task-ul; prea sus, și plătești raționament pe care task-ul nu l-a cerut niciodată. Numele nu se transferă între modele, așa că orice migrare de model începe cu un sweep de effort (Anexa B.9). Setează-l per fază, nu per sesiune: fazele de Research și de Plan merită effort mare, un task mecanic din faza de Execute, de regulă, nu.

*Întreabă: Ce niveluri de effort expune și supraviețuiește raționamentul de la o tură la alta?*

---

### Subagenți

**Ce este: instanțe-copil constrânse ale agentului însuși.**

Orchestratorul îi dă subagentului un task bine delimitat, cu tool-uri limitate la scopul lui, și primește un rezultat. Un context proaspăt izolează munca; un fork poate prelua istoricul agentului principal. Fiecare worker adaugă consum, timp de pornire și coordonare, influențate parțial de cache. Deleagă munca amplă și independentă când beneficiul estimat justifică aceste costuri; păstrează în agentul principal editările rapide și pașii strâns legați. Capitolele 4, 5 și 7 arată unde poate ajuta delegarea.

*Întreabă: Cum expune subagenții - e dispatch-ul în paralel o operație de primă clasă?*

---

### Harness-ul

**Modelul determină plafonul; harness-ul determină dacă îl atingi.**

Harness-ul e runtime-ul din jurul modelului: îți formatează cererea, gestionează fereastra, trimite spre execuție tool call-urile, întoarce rezultatele și decide când s-a terminat treaba. Bucla în sine e simplă; contează controalele din jur. Inspectează potrivirea pentru limbaj, licența, ecosistemul de plugin-uri, enforcement-ul de sandbox și postura de audit, apoi evaluează împreună modelul și harness-ul pe munca ta.

---

### Compară implementările

**Framework-ul face diferențele vizibile; două implementări nu demonstrează o arhitectură universală.**

> **Demonstrație: un prompt, doi agenți.** În timp ce pregăteam manualul, am pus Claude Code să citească codul sursă a doi alți coding agents, în două panouri de terminal: Codex CLI (Rust, întreținut de OpenAI) și opencode (TypeScript, o echipă independentă). Amândoi sunt open source și nu au nicio linie de cod în comun. Același prompt în fiecare: mapează bucla agentului, tool-urile, gate-urile de permisiuni, sandbox-ul și modelul de plugin-uri, citând fișiere și numere de linie.
>
> Cam patru minute mai târziu, fără nicio corecție umană, amândoi au întors aceeași formă: o buclă de agent, un registru de tool-uri, un gate de permisiuni, un sandbox, un model de plugin-uri, suport MCP, o cale de dispatch pentru subagenți. Alte limbaje, alte fișiere, alte nume. Cea mai clară divergență a fost sandbox-ul: Codex implementează izolare reală la nivel de OS, deci kernelul însuși refuză ceea ce agentul nu e autorizat să facă; opencode implementează o îngrădire soft, validare de căi și prompt-uri de permisiune, fără nicio graniță impusă de kernel.
>
> *Limitări: comparația autorului între două repository-uri ilustrează framework-ul. Nu stabilește că fiecare agent are toate cele nouă capabilități sau că implementările sunt la fel de eficiente.*

---

### Postura sandbox-ului e o alegere de guvernanță

**Alegerile unui vendor în privința componentelor principale sunt alegeri de guvernanță.**

Codul sursă și probele rulate în mediul real pot arăta ce acoperă efectiv un sandbox. Codex CLI impune un sandbox de OS by default pe Linux și macOS; Claude Code oferă un sandbox de shell opt-in; opencode are nevoie de izolare la nivel de OS asigurată din exterior. Default-urile depind de versiune, deci verifică-le pe ale tale.

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

*La finalul capitolului poți documenta și testa limitele de control ale unui repository, poți identifica rutele neacoperite și poți desemna responsabilul pentru următorul fix.*

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
| 5. Telemetrie | Nimic; detectează după fapt | Nimeni nu e alertat sau nu intervine | Nu; o alertă și un răspuns testate pot scurta detectarea și recuperarea |

Un control preventiv ar fi putut rupe lanțul doar dacă acoperea operațiunea distructivă. Telemetria ajută la detectare și răspuns, nu la prevenție. Relatările publice nu reprezintă un audit complet al configurației. Într-un al doilea incident din 2026, la DataTalks.Club, Claude Code a rulat `terraform destroy` pe un state file rămas în urmă. Ambele relatări justifică testarea aprobării operațiunilor distructive, a drepturilor credențialelor, a stării și a recuperării, în loc să presupui că aceste protecții există.

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

**Primele patru straturi urmăresc să prevină; telemetria susține detectarea și răspunsul. Testează alerta și intervenția, nu doar logul.**

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
- **Un log singur nu asigură o intervenție.** Relatările despre PocketOS descriu o ștergere înregistrată. Nu stabilesc existența unei căi testate de alertare și răspuns care ar fi putut evita pierderea.

---

### De făcut luni

*Întocmește o fișă de control pentru fiecare limită pe care vrei s-o impui. Monitorizarea demonstrează detectarea, nu faptul că o acțiune interzisă e blocată.*

| Câmp | Ce notezi |
|---|---|
| Limita urmărită | Operațiunea care trebuie interzisă sau aprobată explicit |
| Rute acoperite | Shell, tool-uri native de fișiere, servicii conectate și subprocese; numește excluderile |
| Aplicarea regulii | Unde e configurația, cum e protejată de editări unilaterale, versiunea instalată |
| Verificare | O probă inofensivă, refuzul sau aprobarea așteptată, rezultatul real și dovezile |
| Comportament la eșec | Ce se întâmplă când controlul lipsește, nu pornește, se oprește cu eroare sau depășește timeout-ul |
| Detectare și răspuns | Cine primește alerta, intervenția așteptată și o alertă testată; separat de blocare |
| Responsabil și dată | Cine a verificat, când și când trebuie repetată verificarea |

- [ ] Alege o limită cu consecințe importante într-un repository și completează fișa pentru fiecare rută disponibilă.
- [ ] Folosește fixture-uri inofensive și un mediu de test ca să confirmi o acțiune permisă și refuzul urmărit; nu testa acțiuni distructive pe producție.
- [ ] Testează eșecul controlului și livrarea alertei. Notează rutele neacoperite ca lacune, cu un responsabil și o acțiune următoare.
- [ ] Ai terminat când alt inginer poate reproduce proba și îi poate interpreta rezultatul. Repetă verificarea după schimbări de versiune, politică sau tool-uri.

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

- Agenții reduc costul producerii de cod plauzibil. Claritatea de domeniu, descompunerea utilă și dovezile înainte de „gata” ajută la transformarea acelui output în schimbări utile.
- Pornește cu agentul nativ. O schimbare mică și clară cere execuție directă și o verificare relevantă; neclaritatea, dependențele și riscul justifică mai multă structură.
- Setup-ul și review-ul au un cost; măsoară dacă munca se îmbunătățește. Începe cu o constrângere utilă, nu cu un setup perfect.

---

### Constrângerea s-a mutat

**Generarea mai ieftină de cod face mai vizibile deciziile de engineering din jurul ei.**

Agenții reduc mult costul producerii de cod plauzibil. Asta scoate la vedere constrângerile din jur: să decizi ce trebuie schimbat, să oferi contextul lipsă, să integrezi rezultatul și să stabilești că funcționează. Echipe diferite au bottleneck-uri diferite; viteza de tastare n-a explicat niciodată singură livrarea de software.

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

Observația justifică măsurarea setup-ului, livrării, review-ului și defectelor împreună. Nu stabilește că fiecare echipă ar trebui să piardă prima lună sau că workflow-ul a cauzat diferența.

| Fișă de caz | Ce stabilește relatarea |
|---|---|
| Proveniență | Engagement anonimizat, relatat de autor |
| Dovezi | Relatarea calitativă de mai sus; numerele de task-uri și seriile de timp nu sunt publicate aici |
| Comparație | Echipe pe zone adiacente, înainte și după adopție, fără selecție controlată a task-urilor |
| Limitări | Diferențele dintre echipe și intervențiile combinate împiedică atribuirea cauzală unui singur agent sau unei metode |
| Lecție transferabilă | Măsoară propriul baseline și costurile; extinde când rezultatele observate justifică asta |

---

### Începe mic

**Practica nu trebuie să fie perfectă ca să producă beneficii.**

Câteva instrucțiuni utile în AGENTS.md pot preveni greșeli repetate. O notă scurtă ajută când clarifică o necunoscută reală. Echipele care construiesc workflow-ul perfect înainte să-l ruleze se blochează, pentru că mereu mai e o regulă, un skill sau un hook de adăugat.

Scrie puținele constrângeri utile de care are nevoie primul task, treci muncă delimitată prin agent și adaugă reguli justificate de eșecuri observate sau de un risc concret.

---

### Când se strică

- **Bucla aplicată la tot, sau la nimic.** Dacă toate task-urile trec prin buclă, încetinești; dacă niciunul, ratezi câștigurile. Rulează întâi testul buclei.
- **Aștepți câștigul promis la sfârșit de trimestru.** Urmărește rezultatele de la început; schimbă sau oprește un pilot ale cărui costuri și eșecuri nu se justifică.

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

Iată un feature urmărit prin toate fazele: adaugă un câmp `priority` pe recordul `Wire`, într-un serviciu bancar. Povestea de mai jos e un exemplu relatat de autor; codul și logurile rulării originale nu sunt publicate. [Sursa companionului Wire](https://github.com/ro-ai-labs/ship-it-with-ai/tree/main/companion/wire) și [pachetul executabil versionat](/companion/wire-v1.zip) sunt un exemplu practic sintetic pentru exercițiu, etichetat explicit, nu dovezi ale colaborării originale. Modelul mic în Python face deciziile inspectabile, fără pretenția de a implementa infrastructură bancară de producție.

Priority e una dintre valorile low / normal / high / urgent, are default normal, iar flag-ul urgent declanșează un queue separat de compliance review. Companionul stabilește într-un tabel de acceptare, înainte de cod, ce se întâmplă cu priority absent sau null, clienții vechi, queue-urile indisponibile, conținutul de audit și retry-urile. Sunt decizii explicite pentru exercițiu, nu afirmații despre politica unui client nenominalizat.

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

Research ancorează abordarea în codul real, nu în prima ipoteză a agentului. La o editare familiară, citirea funcției relevante poate ajunge; exemplul bancar avea nevoie de o notă durabilă pentru că deciziile de domeniu trebuiau să supraviețuiască handoff-urilor.

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

Relatarea inițială menționa șase workeri simultani, deși exista dependența dintre task-urile patru și cinci. Fără o înregistrare păstrată a handoff-ului, relatarea nu stabilește că dependența a fost respectată; descrie un risc de coordonare, nu un calendar de copiat. Companionul arată ordinea sigură: stabilești întâi contractele priority/API/audit; implementezi zonele independente pe baza acelor contracte; integrezi apoi rutarea dependentă și verifici întregul comportament. Un singur implementator poate urma aceleași etape fără subagenți.

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

La feature-ul wire, Review a pus sub semnul întrebării aserțiunea de audit log și planul de recuperare al migrației. Lipsa unei migrații down e un defect doar dacă politica de recuperare a proiectului o cere; deployment-ul compatibil cu versiunile anterioare, reparația prin roll-forward sau restaurarea testată pot fi alternative valide. Verify evaluează apoi comportamentul și recuperarea alese. Capitolul 5 arată direct aserțiunea insuficientă, iar companionul îți permite să rulezi etapele roșii și verzi.

---

### Ship

**Ship e un pull request obișnuit. Nu există o bandă specială pentru AI.**

Agentul face commit cu un mesaj structurat, dă push pe branch și deschide un pull request a cărui descriere spune ce s-a schimbat, de ce, cum s-a verificat, ce riscuri rămân și cine e etichetat la review.

La feature-ul wire, PR-ul a venit cu nota de research, planul, rapoartele per task, ambele review-uri și dovezile din teste atașate. Un reviewer senior a petrecut unsprezece minute pe el și a pus o singură întrebare: ar trebui ca flag-ul urgent să fie vizibil în dashboard-ul de metrici? Nu mă gândisem la asta. Aprobat, merged.

PR-ul e un artefact pe care echipa știe să-l revizuiască, dar merge-ul nu încheie livrarea. Completează predarea către producție prin procesul existent de release:

| Întrebare | Ce trebuie predat |
|---|---|
| Cum ajunge în producție? | Ordinea deployment-ului, compatibilitatea cu datele și clienții existenți, responsabilul de release |
| Ce confirmă succesul? | Comportament observabil sau semnal operațional, inclusiv rutarea urgentă și priority în audit |
| Ce declanșează intervenția? | O condiție de eșec numită și persoana care o primește |
| Cum se face recuperarea? | Abordarea testată de rollback, roll-forward sau restore potrivită schimbării |
| Ce urmează după release? | O perioadă delimitată de observație, responsabilul și decizia de închidere |

Companionul completează aceste câmpuri și distinge check-urile simulate de dovezile din staging și producție. Agentul alimentează procesul de livrare; nu îi înlocuiește responsabilii.

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

Pentru contrast, companionul ilustrează un workflow proporțional pentru un typo din textul de ajutor: găsești textul, îi confirmi aria, îl editezi, inspectezi diff-ul și textul afișat, apoi urmezi procesul normal de PR și release. Research, planificarea, execuția, review-ul, verificarea și livrarea sunt acoperite într-o interacțiune scurtă. Nu ai nevoie de un agent suplimentar sau de un fișier de plan ca munca să poată fi inspectată.

---

### Când se strică

- **Gate-urile sunt cereri, nu ziduri.** Instrucțiunile skill-urilor cer disciplină. Controalele obligatorii aparțin politicii de runtime protejate sau gate-urilor de server; un hook ajută doar pe rutele pe care le acoperă (Capitolul 2).
- **Subagenții paraleli pe fișiere care se suprapun** produc editări inconsistente. Redelimitează pe fișier sau pe modul, sau rulează task-urile în secvență.
- **Sesiunile lungi pot pierde firul task-ului.** Agentul răspunde din nou la întrebări deja tranșate sau uită constrângeri. Verifică dacă informațiile sunt învechite ori contradictorii și dacă lipsește accesul necesar; Capitolul 6 arată cum diagnostichezi și refaci contextul.

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

Capitolul 4 a lăsat emitter-ul de audit log cu un test verde și incomplet. Review-ul a găsit că aserțiunea omitea noua cerință de priority și a cerut o abordare documentată de recuperare a migrației. Aceasta e o decizie de proiect, nu o cerință universală pentru migrații down. Implementatorul a rezolvat constatările și a rerulat check-urile relevante.

În companionul sintetic, testul vechi verifică existența unui singur eveniment `wire.created` și identificarea wire-ului:

```python
self.assertEqual(len(service.audit_events), 1)
self.assertEqual(service.audit_events[0]["type"], "wire.created")
self.assertEqual(service.audit_events[0]["wire_id"], wire.wire_id)
```

Înainte să citești mai departe, întreabă-te: ce criteriu nou de acceptare poate eșua deși aceste check-uri trec?

Evenimentul poate omite complet priority. Aserțiunea mai puternică observă valoarea aleasă:

```python
self.assertEqual(event.get("priority"), "URGENT")
```

Pe implementarea defectă, eșuează cu `None != 'URGENT'`; includerea valorii priority normalizate o repară. Testarea tuturor celor patru valori exclude și un fix cu URGENT hardcodat. Rulează `python3 verify.py` din [pachetul companion](/companion/wire-v1.zip) ca să vezi testul slab verde, testul corectat roșu și implementarea reparată verde. Experimentul cu modelul nu stabilește comportamentul sistemului bancar original.

Revenind la proiectul bancar original descris aici, Verify a rulat suita completă de 3.400 de teste și un smoke test pe serviciul de rutare compliance din staging și a produs un diff al schimbării de contract de API pentru review-ul reglementatorului. Toate verzi. Dovezile astea au intrat în pull request la faza de Ship din Capitolul 4.

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

Pentru verificarea comportamentului în frontend, preferă rolurile și etichetele vizibile utilizatorului în locul selectoarelor CSS fragile. Rezistă multor schimbări de stil și DOM dacă rămâne stabil contractul de accesibilitate. Un select nativ folosește `selectOption()`; un radio folosește `check()`; un combobox custom poate cere o altă interacțiune. Înlocuirea unui control cu altul poate cere actualizarea testului chiar dacă rezultatul de business rămâne același. Verifică acel rezultat și inspectează schimbările vizuale randate; locatorii semantici nu evaluează layout-ul.

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

Soluția a fost un prag de judecată, nu o cotă de timp. Înainte de aprobare, reviewerul ar trebui să poată explica regula de business, edge case-ul cu consecințe importante, de ce schimbarea aparține acestei granițe arhitecturale și ce dovezi ar expune cea mai gravă greșeală plauzibilă. Timpul de review și defectele scăpate sunt indicii utile. Un review scurt poate răspunde bine acestor întrebări; unul lung le poate rata.

---

### Când se strică

- **Citirea degenerează într-o privire fugară la bifele verzi.** Timpul de review și defectele scăpate pot scoate la iveală deriva; o verificare opțională a înțelegerii poate arăta ce lipsește înainte de aprobare.

---

### De făcut luni

- [ ] Citește următorul diff de agent în ordinea de mai sus. Pentru o schimbare nefamiliară sau cu consecințe importante, încearcă quiz-ul opțional și lămurește ce nu ai putut explica.
- [ ] Deschide ultimele trei teste scrise de agent. Aserțiunile vin din spec sau din cod?
- [ ] Verifică intenția și corectitudinea; adaugă un reviewer independent dacă riscul sau erorile observate îl justifică. Cere un răspuns motivat la fiecare constatare.
- [ ] Alege verificările relevante și protejează-le integritatea. Rezervă testele held-out și izolarea evaluării pentru situațiile care le cer.
- [ ] Confirmă că review-ul răspunde întrebărilor despre regula de business, edge case-ul important, granița arhitecturală și greșeala cu cel mai mare impact. Urmărește timpul ca indiciu, alături de defectele scăpate, nu ca o cotă de calitate.

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

E un fișier Markdown cu instrucțiunile proiectului. Un client compatibil îl încarcă după propriile reguli de descoperire și configurare; unii clienți cer încărcare explicită. Textul consemnează ce vrea echipa să urmeze agentul și poate trece prin review într-un pull request. E stratul Memory deținut manual din Capitolul 1, nu o politică de permisiuni aplicată efectiv.

### AGENTS.md vs CLAUDE.md: care e diferența? {#agents-md-vs-claude-md}

**Același rol, dar regulile de încărcare depind de harness și de versiune.**

Un nume de fișier comun nu înseamnă reguli identice de încărcare. Rezumatul de compatibilitate de mai jos a fost verificat pe 23 octombrie 2026; verifică versiunea instalată și contextul efectiv.

| Client | Nume de fișier și configurare | Arie și precedență | Cum verifici ce s-a încărcat |
|---|---|---|---|
| Codex CLI | `AGENTS.md`; `AGENTS.override.md` are prioritate în același director; numele de fallback sunt configurabile | Instrucțiuni globale, apoi din rădăcina repository-ului spre directorul de lucru; instrucțiunile mai apropiate le suprascriu pe cele anterioare; limita totală de dimensiune e configurabilă | Cere sursele active și inspectează logurile de sesiune/TUI la audit |
| Claude Code | `CLAUDE.md` implicit; `AGENTS.md` direct din v2.1.277 | Fallback-ul AGENTS implicit se aplică doar dacă directorul de lucru și părinții nu conțin `CLAUDE.md`, `.claude/CLAUDE.md` sau `CLAUDE.local.md`; un fișier CLAUDE poate importa `@AGENTS.md`; numele AGENTS override/local nu au semantica din Codex | `/memory`; afișarea fișierelor AGENTS încărcate direct cere v2.1.280+, cu excepții timpurii rezolvate în v2.1.281 |
| Gemini CLI | `GEMINI.md` implicit; configurează `context.fileName` să includă `AGENTS.md` | Context global, de workspace/directoare părinte și de director relevant, cu reguli de trusted root; nu modelul de precedență din Codex | `/memory show`, apoi `/memory reload` după schimbări |
| Aider | Explicit `aider --read AGENTS.md`; păstrează `read: AGENTS.md` în `.aider.conf.yml` | Context de chat inclus read-only; fără o ierarhie implicită de descoperire AGENTS în directoarele părinte | Confirmarea de pornire și `/ls` |

Documentația primară și limitele de versiune sunt în Anexa C. Testează o instrucțiune distinctivă într-o sesiune nouă, în loc să presupui că fișierul a fost descoperit sau că are aceeași autoritate în fiecare client.

---

### Povestea: o convenție, trei forme de sprijin

O echipă cu care am lucrat folosea un coding agent de șase luni când un senior engineer a venit la mine cu o nemulțumire. „De fiecare dată când generăm un endpoint de API, trebuie să repar validarea. Mereu aceeași corecție. Agentul pune validarea în stratul greșit.”

„De ce nu e regula scrisă undeva?”

„N-am scris-o niciodată. Doar o tot reparăm.”

Seniorul corecta repetat aceeași amplasare a validării la review-urile de endpoint-uri. Relatarea inițială includea numere de endpoint-uri și o estimare de timp, dar înregistrările review-urilor nu sunt disponibile aici, așa că ediția aceasta nu susține o economie lunară precisă.

Am documentat convenția în AGENTS.md, am adăugat un reminder în template-ul de PR și am identificat endpoint-uri corecte ca exemple de referință. Potrivit relatării, review-urile ulterioare au cerut mai puține corecții de acest fel. Intervenția a fost combinația celor trei; relatarea nu izolează contribuția instrucțiunii.

| Fișă de caz | Ce stabilește relatarea |
|---|---|
| Proveniență | Engagement anonimizat, relatat de autor |
| Dovezi | O problemă recurentă de review și o îmbunătățire raportată; înregistrările de review/timp nu sunt publicate |
| Comparație | Observații înainte/după schimbarea combinată de instrucțiune, reminder și exemple de referință |
| Limitări | Fără efect izolat al instrucțiunii, mix controlat de task-uri sau economie lunară de timp demonstrabilă |
| Lecție transferabilă | Scrie o convenție delimitată, susține reviewerii și exemplele, apoi măsoară corecțiile recurente |

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
| Bine, pentru intrarea HTTP a acestui proiect | „DTO-urile controller-ului stabilesc garanțiile de formă ale request-ului prin Bean Validation înainte de apelul de service; urmează UserCreateController. Alte puncte de intrare stabilesc aceleași garanții. Codul de service/domain impune în continuare invariantele de business; folosește validarea metodelor de service unde acea graniță o cere.” |

Varianta proastă nu specifică arhitectura. Varianta delimitată identifică o graniță de intrare, garanția ei, un mecanism și un exemplu fără să declare că serviciile pot avea încredere universală în orice input. Spring suportă și validarea metodelor de service. Un pattern portabil este: „În [scope], [granița de intrare] stabilește [garanția de input] prin [mecanism]; urmează [referința]. Alte intrări stabilesc aceeași garanție; [responsabilul] păstrează invariantele de domeniu.” Anexa B.2 e un punct de pornire specific unui proiect.

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

Tot ce e în fereastră concurează pentru aceeași atenție mărginită. Contextul învechit sau contradictoriu e una dintre cauzele pentru care o sesiune lungă poate pierde firul task-ului. Patru obiceiuri te ajută să păstrezi contextul util.

- **Pointere, nu payload-uri.** Pune în AGENTS.md un link spre documentele mai lungi și doar contextul stabil care ajută frecvent. Reperul de 200 de linii te îndeamnă să alegi, nu să tai instrucțiuni necesare ca să atingi un număr.
- **Păstrează starea de care ai nevoie.** Pentru munca de durată, notează deciziile, constrângerile, progresul și comenzile care au mers, în formatul potrivit proiectului. Un issue, un fișier existent sau o scurtă notă pot fi suficiente; nu ai nevoie de trei documente și un commit la fiecare restart.
- **Folosește cele patru semne pentru diagnostic.** Agentul reia întrebări rezolvate, citează un fișier învechit, uită o constrângere sau face editări tot mai neglijente. Acestea pot indica un context contaminat, dar și cerințe contradictorii, surse învechite ori acces lipsă. Verifică starea reală și corectează cauza; dacă deriva continuă, păstrează ce e necesar și pornește o sesiune curată. Fă commit după practica repo-ului, nu ca ritual de restart.
- **Tratează compactarea ca pe un hand-off.** Rezumarea poate omite sau deforma detalii, așa că salvează durabil deciziile, constrângerile și dovezile indispensabile. Dă-i compactorului o listă de păstrat: planul, întrebările deschise, devierile consemnate în notele de implementare, comenzile exacte care au mers. Apoi verifică dacă în contextul rezultat se află tot ce cere pasul următor.

Clientul stabilește ce rezumă, ce păstrează și ce reîncarcă; [documentația Claude Code despre compactare](https://code.claude.com/docs/en/context-window#what-survives-compaction) descrie aceste diferențe. Verifică comportamentul clientului și al versiunii pe care le folosești.

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

Documentul corectat a intrat în repository, iar echipa a ales muncă țintită în locul propunerii de rewrite amplu. Au înlocuit două module în trimestrul următor, inclusiv dependența deprecated. Propunerea de optsprezece luni și înlocuirea de trei luni descriu calendare, nu totaluri comparabile de muncă. Fără ipotezele inițiale despre numărul de oameni și un scenariu contrafactual credibil, relatarea nu stabilește om-luni economisite și nu izolează efectul agentului de judecata experților.

| | |
|---|---|
| **Context** | Echipă de banking reglementat, serviciu Java de ~60k LOC scris între 2018 și 2024, documentație învechită |
| **Timp de agent** | ~15-18 minute |
| **Timp de corecție umană** | ~45 de minute (reviewerul cunoștea domeniul de onboarding de clienți) |
| **Rezultat** | Două module purtau datoria tehnică; rewrite-ul de 18 luni a devenit o înlocuire țintită de 3 luni |
| **Limitări** | Workflow-ul accelerează cunoașterea de domeniu, nu o înlocuiește |

| Fișă de caz | Ce stabilește relatarea |
|---|---|
| Proveniență | Engagement de banking anonimizat, relatat de autor |
| Dovezi | Relatarea, cele trei greșeli corectate și timpii raportați de investigație; artefactele originale nu sunt publicate |
| Comparație | Calendarul estimat al unui rewrite amplu față de munca țintită aleasă de echipă; numărul de oameni nu e specificat |
| Limitări | Efortul evitat e un scenariu contrafactual nemăsurat; experții au corectat harta și au ales alternativa |
| Lecție transferabilă | Folosește o hartă revizuită ca să verifici scope-ul, apoi estimează explicit alternativele |

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

*La finalul capitolului poți stabili condițiile necesare unui task, poți identifica lipsurile de pregătire și poți decide ce muncă poate continua în limite testate.*

**TL;DR**

- Înainte de punctare, definește task-ul, reviewerul calificat, dovezile care ar expune o greșeală cu consecințe importante și permisiunile și recuperarea potrivite.
- Condițiile lipsă sau necunoscute restrâng task-ul afectat la investigație sau pregătire supravegheată. Un repository verde nu autorizează orice task din el.
- Folosește cele opt semnale ca ghid euristic de pregătire. Notează explicit necunoscutele; procentul de coverage singur nu stabilește dacă verificarea e suficientă.

---

### Când n-ar trebui să folosești agenți AI de cod? {#when-not-to-use-agents}

**Unele codebase-uri n-ar trebui să primească încă un agent, iar un nu acolo e ceea ce îți permite să spui da peste tot în rest.**

Motivul nu e că agentul ar fi prost sau echipa slabă: schimbarea propusă poate depăși capacitatea echipei de a o evalua, verifica sau limita consecințele. Stabilește întâi aceste condiții. Cele opt semnale ajută apoi la prioritizarea pregătirii; sunt un sprijin pentru discuție, desprins din practică, nu un model de risc validat.

### Înainte de punctare: definește task-ul

| Condiție | Dovezi necesare |
|---|---|
| Scope | Comportamentul vizat, modulul și mediul afectate; acțiunile permise |
| Capacitate de evaluare | O persoană calificată care poate recunoaște un rezultat plauzibil, dar greșit |
| Verificare | Check-uri care expun greșelile cu consecințe importante pentru această schimbare, cu aserțiuni relevante și eșecuri interpretabile |
| Limite și recuperare | Accesul, aprobarea, deployment-ul și recuperarea potrivite consecințelor |

Dacă un răspuns lipsește sau e necunoscut, restrânge munca respectivă până rezolvi lacuna. Agentul poate totuși investiga un modul netestat sau poate propune teste de caracterizare sub supraveghere. Asta nu îl autorizează să schimbe comportamentul de business al modulului. Restricția urmărește task-ul afectat, nu orice activitate din repository.

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

**Stabilește verificarea relevantă înainte de schimbări de comportament; lasă agentul să ajute la pregătirea ei.**

Cere-i agentului să propună teste de caracterizare pentru comportamentul actual, apoi pune un reviewer calificat să distingă comportamentul intenționat de bug-urile existente. Verifică rezultatele importante, cazurile de eșec, fiabilitatea și capacitatea echipei de a interpreta eșecurile. Dacă nicio dovadă disponibilă nu ar expune o greșeală cu consecințe importante, restrânge munca afectată la investigație sau pregătire supravegheată până există acele dovezi. Testele sunt o plasă de regresie, nu o dovadă de corectitudine (Capitolul 5).

---

### Semnalul 6: echipa nu poate evalua output-ul

**E cel mai important semnal și cel pe care echipele îl înțeleg greșit cel mai des.**

Un developer junior primește un story: adaugă un pas de verificare criptografică în fluxul de plăți. Juniorul trimite agentul la treabă, iar agentul produce un modul care folosește AES-256 în mod CBC cu un initialization vector hardcodat. Pentru cineva nou în criptografie, arată corect: compilează, testele unitare trec, iar criptograful senior e în concediu de creștere a copilului trei luni. Juniorul livrează, iar vulnerabilitatea stă în producție șase luni, până o găsește un penetration test.

Agentul a făcut exact ce i s-a cerut. Output-ul lui arăta bine și era greșit, iar nimeni nu era în poziția de a vedea asta.

Echipele citesc asta ca „ne trebuie mai mulți ingineri seniori”, ceea ce nu scalează pe un orizont de șase luni. Pentru zonele sensibile, cere aprobarea unui specialist calificat printr-un review obligatoriu impus pe server, pe care credențialele agentului nu-l pot ocoli. Politica aplicată la nivel de tool poate împiedica și editarea acelor module. AGENTS.md poate explica restricția, iar agenții de review pot ajuta, dar niciunul nu înlocuiește expertiza lipsă și nu face aprobarea inevitabilă.

Semnalul ăsta încalcă condiția de evaluare, indiferent de total. Și alte semnale pot bloca un anumit task, inclusiv verificarea absentă sau o cale de aprobare indisponibilă. Construiește capacitatea lipsă, adu pe cineva care o are sau restrânge munca afectată. Un total mic nu anulează niciodată o condiție neîndeplinită.

---

### Sunt agenții AI de cod gata de producție? {#are-agents-production-ready}

**Pregătirea ține de un task și de controalele lui; culoarea repository-ului ajută doar la prioritizarea pregătirii.**

```
  Verifică întâi condițiile task-ului. Necunoscut nu înseamnă zero.
  Fără necunoscute, adună și rotunjește jumătățile în sus înainte să alegi culoarea.

  Număr semnale      Culoare     Ghid de pregătire
  =============      =======     =================

  0 - 1              VERDE       Puține lacune de pregătire
  2 - 3              GALBEN      Pregătire substanțială
  4 +                ROȘU        Pregătire mai amplă înainte

  Semnale (punctează fiecare lacună cunoscută):
   1. Fără teste            5. Constrângeri de reglementare
   2. Fără documentație     6. Echipa nu poate evalua output-ul
   3. Cuplare strânsă       7. Potrivirea model-context
   4. Reguli împrăștiate    8. Viteza schimbării
```

*Figura: Kill signals și semaforul ca ghid de pregătire. Condițiile neîndeplinite ale task-ului au prioritate față de culoare; răspunsurile necunoscute cer investigație.*

- **Verde:** un posibil punct de pornire, după ce task-ul propus îndeplinește toate condițiile.
- **Galben:** prioritizează lacunele concrete și folosește muncă atent supravegheată acolo unde condițiile sunt îndeplinite.
- **Roșu:** probabil ai nevoie de pregătire mai amplă. Investigația și reparațiile delimitate pot fi în continuare utile; culoarea nu e permisiune pentru schimbări de comportament.

Aplică ghidul zonei relevante din proiect. Un scor verde al repository-ului te ajută să alegi un punct de pornire. Nu autorizează fiecare task din acel repository.

---

### Numără după intensitate, nu după prezență

**Punctează dovezile din zona afectată; păstrează necunoscute proprietățile neinvestigate.**

Folosește 0 pentru o lacună absentă, 0,5 pentru una parțială și 1 pentru una substanțială, cu o scurtă notă despre dovezi. Folosește `?` pentru ce n-ai investigat; nu calcula un total liniștitor trecând necunoscutele ca zero. Fără necunoscute, adună și rotunjește jumătățile în sus înainte să aplici benzile 0-1 / 2-3 / 4+. Sunt reguli euristice ale autorului, nu praguri de siguranță măsurate. Anexa B.4 oferă repere de comportament; procentul de line coverage e doar o informație de sprijin.

---

### Cum arată culorile

**Fiecare culoare schimbă felul în care folosești agentul.**

| Proiect și dovezi | Număr | Pregătire | Ce faci |
|---|---|---|---|
| Serviciu de profil de client: rezultate și eșecuri relevante testate fiabil, prezentare actuală, reguli canonice, reviewer calificat | 0 | Verde | Alege un task delimitat și stabilește celelalte condiții necesare |
| Plăți legacy: cazuri de eșec relevante absente (1), documentație veche (0,5), cuplare costisitoare (1), reguli împrăștiate (0,5); aprobare și expertiză disponibile | 3 | Galben | Pregătește întâi verificarea; supraveghează investigația și refactorizarea delimitate |
| Bibliotecă de criptare custom: nedocumentată, fără reviewer calificat în criptografie | Nu decide | Condiție neîndeplinită | Restrânge schimbările criptografice; obține expertiză sau evaluează un înlocuitor verificat |
| API greenfield: cerere clară, verificare și deployment neinvestigate | ? | Necunoscută | Definește comportamentul, check-urile, reviewerul și recuperarea înainte să alegi un mod de lucru |
| Tool intern: check-uri relevante stabilite, câteva lacune de documentație și cuplare (0,5 fiecare), expunere mică | 1 | Verde | Un posibil pilot, cu condițiile task-ului îndeplinite și limite de cheltuieli |

---

### Când se strică

- **Numărarea coverage-ului în locul aserțiunilor** ascunde verificarea lipsă. Verifică comportamentul afectat și cazurile de eșec cu consecințe importante.
- **Un total verde maschează o necunoscută.** Investighează necunoscuta și condițiile task-ului înainte să extinzi scope-ul.
- **Leadership-ul impune un mod de lucru deși lipsește o condiție necesară.** Restrânge task-ul afectat și numește pregătirea de care are nevoie.
- **Un codebase verde începe să dea rezultate galbene după un upgrade de model.** Bănuiește întâi instrucțiunile scrise pentru modelul anterior, înainte să dai vina pe cod: rulează checklist-ul de migrare din Anexa B.9.

---

### De făcut luni

- [ ] Numește un task propus, comportamentul afectat și mediul.
- [ ] Completează cele patru condiții din B.4; restrânge munca afectată oriunde un răspuns lipsește sau e necunoscut.
- [ ] Notează dovezi pentru cele opt semnale de pregătire. Folosește `?` pentru necunoscute și check-uri relevante în locul pragurilor de coverage.
- [ ] Dă-i lead-ului o acțiune următoare delimitată, un responsabil și un criteriu de finalizare. Ai terminat când alt inginer poate reproduce decizia din fișă.
- [ ] Repetă verificarea când se schimbă task-ul, modelul, controalele sau sistemul din jur.

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

- Izolează munca simultană sau în conflict, folosește check-urile locale pentru feedback și gate-uri protejate pe server pentru enforcement și păstrează review-ul uman obișnuit.
- Un inginer poate porni un rollout: folosește agentul tu însuți, notează rezultatele, învață un coleg, apoi recrutează lead-ul și managerul. Măsoară ritmul în loc să presupui o curbă fixă de productivitate.
- Folosește scepticismul pentru a defini probele pilotului, păstrează responsabilitatea review-ului și pregătește o variantă de lucru pentru întreruperile vendorului.

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

Bucla exterioară (outer loop) reinvocă agentul până când o condiție e îndeplinită. Adaugă încercări, nu judecată, așa că multiplică orice permite bucla ta interioară (inner loop; Capitolul 4). Folosește-o doar când fiecare unitate îndeplinește condițiile din Capitolul 8, poate fi verificată independent și recuperată și are controale potrivite muncii nesupravegheate. Un scor verde de pregătire nu ajunge. Fă review la pull request-urile rezultate înainte de release.

Înainte de prima rulare nesupravegheată, consemnează o condiție de oprire evaluabilă automat, un buget, un gate de acceptare protejat, stare durabilă și un handoff de context, plus izolare dimensionată pentru absență. Folosește un branch și o copie de lucru dedicate, verifică acoperirea sandbox-ului pentru fiecare tool, ține credențialele de producție în afară și testează restricțiile de rețea. Anexa B.6 e formularul de completat, cu cele patru semne care cer stop înainte să relansezi.

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

Înainte să începi, stabilește serviciul și contul aprobate, repository-urile și datele permise, un responsabil, controalele inițiale testate și o limită de cheltuieli. Politica existentă se aplică și unui pilot grassroots. Exemplul alocă apoi prima lună setup-ului și unui pilot delimitat, a doua extinderii, iar a treia responsabilităților operaționale. Guvernanța ulterioară verifică extinderea și responsabilitățile recurente; nu e prima aprobare. Urmărește de la început timpul de ceas și timpul uman efectiv, calitatea, review-ul/rework-ul și costul total. Adaugă instrucțiuni, skill-uri și hook-uri pentru o nevoie demonstrată sau un risc justificat. Calendarul reutilizabil și fișa de măsurare sunt în Anexa B.5.

```
  ÎNAINTE SĂ ÎNCEPI: serviciu/cont aprobate; repository-uri/date permise;
  responsabil; controale inițiale testate; limită de cheltuieli și baseline.

  Zilele 1-30: Fundația             Zilele 31-60: Extinderea        Zilele 61-90: Operaționalizarea
  -------------------------         -------------------------       -------------------------
  Championul instalează             Lead-ul aduce încă 2-3          Managerul integrează
  AGENTS.md schițat                 ingineri                        metricile în tracking-ul
  Primul proiect pe verde           AGENTS.md consolidat            normal de velocity
  Workflow-ul de architecture       Hooks configurate               Guvernanța extinderii verificată
  review demonstrat                 Skills la nevoie                Politică și ownership
                                    Kill signals aplicate           de marketplace recurente
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

**Managerul** deține eligibilitatea pilotului și bugetul înainte de începerea muncii, apoi procurement-ul, deciziile de extindere și guvernanța recurentă. Anexa A oferă un scenariu ilustrativ cu douăzeci de ingineri și un calcul complet de cost ipotetic; nu oferă rezultate măsurate de adopție sau cycle time.

---

### Dezacord și încredere excesivă

**Tratează-l pe fiecare ca pe o problemă structurală cu o soluție structurală, nu ca pe un defect de caracter.**

**Scepticul de principiu** poate identifica un mod real de eșec. Invită-l să definească task-uri reprezentative, greșeli cu consecințe importante, dovezile necesare pentru extindere și condițiile de oprire. Un reviewer exigent poate îmbunătăți pilotul fără să aleagă personal să folosească agentul. Distinge dezacordul susținut de dovezi de obstrucție prin procesul normal de engineering. Rezolvă acolo disputele de ownership și conduită; nu ocoli expertiza sau aprobările necesare doar ca să păstrezi ritmul adopției.

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
| Hook-uri locale tratate ca enforcement | Sunt sărite, editate sau niciodată instalate | Check-uri obligatorii protejate pe server și schimbări de politică trecute prin review |

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

**Arhitectura e controlul capabilității.** Inspectează contextul, tool-urile, Permisiuni / Sandbox, skill-urile, plugin-urile, MCP, Memory, Effort și subagenții, plus harness-ul care le asigură. Lista ajută la compararea sistemelor actuale; capabilitățile absente sau asigurate din exterior sunt constatări legitime.

**Metoda e controlul workflow-ului.** Formularea limpede a muncii e schimbarea fundamentală. Bucla în șase faze e o implementare; AGENTS.md va exista sub alte nume, dar principiul e permanent: disciplină sub formă de cod, nu de tradiție orală.

**Realitatea e controlul adopției.** Kill signals sunt proprietăți ale codebase-urilor și ale echipelor, nu ale tool-urilor. Semaforul se aplică indiferent ce agent folosești trimestrul ăsta, iar champion, lead, manager e arcul pentru orice tranziție de tooling.

Dacă iei o singură practică, ia review-ul de arhitectură din Capitolul 7 ca diagnostic inițial: dovezi utile de analizat, nu un verdict dintr-o singură rulare. Dacă iei un singur framework, ia kill signals și semaforul din Capitolul 8; „nu”-ul contează la fel de mult ca „da”-ul. Dacă iei o singură orientare, investește în modul de a gândi, nu în tool.

Înapoi la cele nouă secunde: relatarea PocketOS arată de ce o instrucțiune împotriva comportamentului distructiv nu ajunge. Limitele preventive cer verificări pe fiecare rută; detectarea cere un răspuns testat. Relatările publice lasă nerezolvate detalii de configurație. Manualul îți cere să faci propriile controale și decizii inspectabile.

Să înțelegi problema devine mai important decât să scrii codul. Era adevărat când a programa însemna să perforezi cartele, când IDE-ul a înlocuit editorul de text și când coding-ul asistat de AI a trecut de la autocomplete la redactarea de cod; e adevărat și acum, când scrisul a rămas în seama agenților. Numele modelelor din ediția asta vor îmbătrâni, iar munca durabilă rămâne: înțelege problema, formulează munca, constrânge execuția, verifică rezultatul. Secvența asta e întreaga problemă de control - și n-a aparținut niciodată tool-urilor. Îți aparține ție.

Agenții te pot ajuta să înțelegi sistemul. Tu răspunzi în continuare pentru a înțelege suficient cât să alegi munca, să evaluezi dovezile și să accepți consecințele.

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

Cu machine learning m-am apucat prin 2013. La finalul lui 2015 am portat DarkNet și YOLO pe un headset XR și am început să construiesc aplicații AI profesionist; în 2023 m-am alăturat unei companii care dezvolta SoC-uri neuromorfice. Am folosit fiecare generație de asistent de coding, de la Visual Assist până la primul Copilot și la LLM-uri pentru cod din ziua în care a apărut ChatGPT. Nu mi-am construit propriul coding agent. I-am folosit însă pe majoritatea celor care există acum și am văzut multe echipe folosindu-i.

Nu sunt neutru pe subiectul ăsta. Cred că livrarea de software cu agenți e schimbarea cu cele mai mari consecințe din domeniul nostru de la apariția limbajelor de programare de nivel înalt încoace și că felul în care o adoptă majoritatea echipelor le face mai mult rău decât bine. Asta e a treia sau a patra iterație a framework-urilor astea; iterațiile de dinainte au greșit în feluri interesante.

<a id="contact"></a>
*Contact: [info@ship-it-with.ai](mailto:info@ship-it-with.ai) pentru discuții tehnice sau workshopuri personalizate, în persoană sau online, croite pe codebase-ul și pe constrângerile echipei tale. Mă găsești pe [LinkedIn](https://www.linkedin.com/in/mihaicvasnievschi/).*

---

## Changelog {#changelog}

Pagina asta urmărește actualizările semnificative ale manualului. Corecturile mărunte și ajustările de SEO nu sunt listate; footer-ul arată data ultimei actualizări.

### 2026-10-23 - Dovezi, condiții de task și livrare reproductibilă

Edițiile întreținute pornesc cu agentul nativ și un proces dimensionat după task; Superpowers rămâne opțional. Condițiile task-ului preced acum scorul euristic de pregătire, cu necunoscute explicite și repere de verificare bazate pe comportament. Fișele de control separă prevenția, detectarea, comportamentul la eșec și acoperirea testată. Fișele de caz disting relatările autorului, înregistrările de măsurare indisponibile și economiile contrafactuale; procentele de rollout și precizia economiilor de efort fără suport au fost eliminate. Economia include toate încercările, setup amortizat, întreținere și guvernanță recurentă, separând capacitatea de bani. Un companion Wire sintetic și executabil demonstrează testul insuficient verde, cel corectat roșu și implementarea reparată verde, planificarea după dependențe și predarea către producție. Corecțiile tehnice acoperă descoperirea instrucțiunilor, concurența, baseline-urile studiilor de context, rutele DNS, acțiunile Playwright, RULER, MCP și Spring. Template-urile, rezumatele, sursele și recomandările românești se aliniază; traseele de lectură, etichetele template-urilor și datele arhivelor sunt mai clare. Sursele noi sau reverificate își precizează aria și data; nu se afirmă că fiecare fapt istoric a fost revalidat. Manuscrisele din septembrie rămân înghețate.

Ultimul pas editorial elimină certitudinea rămasă despre controalele PocketOS, precizează limitele disponibilității setărilor de effort și ale compactării și marchează revenirea de la experimentul Wire sintetic la proiectul original. B.9 acoperă acum evaluarea modelelor, harness-urilor și skill-urilor în ambele limbi, păstrând verificările de migrare. B.11 adaugă un protocol de observare a cititorilor; nu raportează rezultate de trial.

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

Capitolul 5 capătă o secțiune de igienă a contextului, inserată după paragraful de vocabular inner/outer loop, care predă meșteșugul zilnic pe care cartea îl numise, dar nu-l predase niciodată - fereastra e memoria de lucru a agentului, iar tot ce e încărcat în ea concurează cu raționamentul. Numește cele patru semne ale contaminării (agentul răspunde din nou la o întrebare deja rezolvată, citează o versiune învechită a unui fișier pe care l-a editat, uită o constrângere pe care o respecta sau scade în calitatea editărilor târziu într-o sesiune lungă), disciplina graniței dintre sesiuni - o unitate de muncă per sesiune, cu stare durabilă recitită din repository - și compactarea ca hand-off. **Corectat pe 23 octombrie:** rezumatul poate păstra decizii din conversație; riscul este să omită sau să deformeze detalii, nu pierderea sigură a tot ce nu e într-un fișier. Semnele cer diagnostic, nu stabilesc singure cauza. Anexă nouă: B.7, one-pager-ul igienei contextului (numărul de template-uri ajunge acum la șapte). Secțiunea despre context window din Capitolul 1 capătă o trimitere înainte, de o frază, către noua secțiune.

### 2026-07-05 - Exemplul lucrat din Anexa A

Anexa A a primit un exemplu de cost cu tarife ilustrative și cifrele de rollout raportate atunci. **Înlocuit pe 23 octombrie:** definițiile și înregistrările măsurătorilor nu sunt disponibile aici; cifrele nu mai sunt prezentate ca dovezi de pilot măsurat. Anexa întreținută conține acum o comparație explicit ipotetică de cost complet și o fișă de măsurare reutilizabilă.

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

*Pentru engineering managerul, directorul sau CTO-ul care deține bugetul, oamenii și procurement-ul și pentru championul care trebuie să-i prezinte un caz. Citește Capitolele 2, 8 și 9 pentru controale, pregătirea task-ului și rollout. Anexa acoperă deciziile tale, o echipă ilustrativă și o comparație de cost în care poți pune propriile numere. Poate fi trimisă separat.*

---

### Treaba ta în cele 90 de zile

**Managerul deține condițiile de pornire, decizia de extindere și costul recurent.** Responsabilitățile încep înainte de primul pilot. Exemplul de 90 de zile din Capitolul 9 acordă mai multă atenție managerului mai târziu; nu amână procurement-ul sau guvernanța până în ziua 61.

Înainte să începi, numește responsabilul și stabiliți:

- Serviciul și contul aprobate, repository-urile și datele permise și termenii contractuali necesari.
- Permisiunile inițiale, controalele pentru secrete, izolarea și recuperarea potrivite pilotului. Verifică rutele acoperite în loc să presupui că funcționează configurația.
- O limită de cheltuieli, muncă comparabilă de observat, criterii de succes și condiții de oprire sau restrângere a pilotului.
- Cine poate judeca comportamentul afectat, face review la schimbări cu consecințe importante și decide extinderea.

În timpul pilotului, protejează timpul de investigație, review și întreținere. Ajută lead-ul să rezolve lacunele de acces, documentație și expertiză. O echipă care nu poate evalua un algoritm de plăți are nevoie de ajutor calificat sau de un task mai restrâns; un abonament nu îi oferă acea expertiză.

Mai târziu, decide dacă dovezile susțin extinderea, alt workflow sau oprirea. Atribuie responsabilități permanente pentru instrucțiuni, integrări, riscul de vendor, controale și evaluare. Sunt responsabilități operaționale și după terminarea setup-ului inițial.

Urmărește rezultatele de la început. Evită clasamentele individuale după numărul de PR-uri, promisiunile premature de venituri și un calendar care extinde scope-ul indiferent de rezultate. Un pilot mic și bine înțeles e mai ușor de evaluat decât o țintă de adopție pentru toată compania.

---

### Ce codebase-uri acum, mai târziu, niciodată

**Decide pentru task-ul propus înainte să sortezi portofoliul.** Definește comportamentul și mediul afectate. Stabilește un evaluator calificat, dovezi care ar expune o greșeală cu consecințe importante și permisiuni și recuperare potrivite. Dacă o condiție lipsește sau e necunoscută, restrânge task-ul la investigație sau pregătire supravegheată până rezolvi lacuna.

Cele opt semnale din Capitolul 8 ajută apoi la prioritizarea pregătirii. Culorile sunt o euristică, nu o politică de delegare. Fără necunoscute, adună și rotunjește jumătățile în sus înainte să aplici o culoare:

| Scorul repository-ului | Ghid de pregătire | Decizia managerului |
|---|---|---|
| Verde, 0–1 lacune cunoscute | Puține lacune de pregătire | Ia în calcul muncă delimitată ale cărei condiții sunt îndeplinite. |
| Galben, 2–3 lacune cunoscute | Pregătire substanțială | Finanțează lacunele cu impact și alege muncă pe care echipa o poate evalua acum. |
| Roșu, 4+ lacune cunoscute | Pregătire mai amplă | Restrânge munca afectată în timp ce decizi ce investighezi, îmbunătățești, înlocuiești sau retragi. |
| Necunoscut, `?` | Lipsesc dovezi | Investighează; nu îl număra tacit ca zero. |

Un repository verde nu autorizează fiecare task. Un scor mare nu interzice investigația utilă read-only. Lipsa evaluării calificate încalcă o condiție a task-ului, indiferent de total. Coverage-ul poate informa discuția, dar aserțiunile relevante, cazurile de eșec, rularea fiabilă și capacitatea echipei de a interpreta rezultatele contează mai mult decât un procent.

Cere-i lead-ului o fișă scurtă de portofoliu: task propus, condiții, lacune cunoscute și necunoscute, scope permis, pregătire necesară și responsabil. Pentru fiecare investiție, întreabă ce decizie sau capacitate de verificare cumpără. „Niciodată” ar trebui să descrie muncă pe care echipa nu o poate autoriza responsabil în constrângerile actuale, nu o etichetă permanentă pentru o companie sau un repository.

---

### O echipă, săptămână cu săptămână

**Scenariu ilustrativ de planificare:** douăzeci de ingineri într-o firmă de servicii financiare reglementată, cu un engineering manager și un CTO atent la costuri. Nu e un pilot măsurat sau relatarea unei colaborări cu un client. Calendarul ilustrează decizii și responsabilități; nu oferă rezultate observate de adopție, cycle time sau rată de defecte. Folosește secvența unde se potrivește și schimbă datele după dovezi.

| Etapă | Ce aduce echipa | Ce face managerul |
|---|---|---|
| Înainte de pilot | O propunere delimitată, un responsabil, cont/date aprobate, controale inițiale și un plan de evaluare | Confirmă eligibilitatea, expertiza, limita de cheltuieli și condițiile de oprire înainte să înceapă munca. |
| Prima lună | Un eșantion mic de încercări acceptate și eșuate, constatări de review, consum facturat și lacune nerezolvate | Protejează timpul de evaluare; rezolvă accesul sau expertiza lipsă; nu cere un procent de adopție. |
| A doua lună | O comparație de muncă similară, cu efort uman, timp de livrare, observații de calitate și costuri înregistrate separat | Verifică selecția task-urilor și dacă rezultatele justifică un alt grup delimitat de utilizatori sau task-uri. |
| Faza ulterioară a managerului | O recomandare de extindere, schimbare sau oprire, cu limitări și responsabilități operaționale | Rezolvă licențierea pentru scope-ul aprobat, atribuie guvernanța și întreținerea recurente și raportează rezultatele susținute de dovezi. |

Un update util pentru board numește ce s-a comparat, ce s-a observat și ce rămâne incert. De exemplu: *„Am comparat [numere și tipuri de task-uri] în [perioadă], prin [metodă de selecție]. Timpul uman efectiv a fost [rezultat], timpul de livrare a fost [rezultat], iar [observațiile despre defecte] acoperă [fereastra]. Costul suplimentar a fost [sumă]. Recomandăm [decizie], cu rezerva [incertitudinii rămase].”* Completează din înregistrări; elimină afirmațiile fără suport.

Păstrează o fișă de măsurare împreună cu raportul:

| Câmp | Ce înregistrezi |
|---|---|
| Proveniență și perioadă | Pilot observat sau exemplu ilustrativ; date, versiuni de serviciu/model, workflow și responsabil. |
| Muncă și comparație | Numere brute de task-uri încercate, finalizate și acceptate; tipuri, selecție, baseline/grup de comparație, excluderi și diferențe importante. |
| Timp de livrare | Timpul de ceas de la început până la acceptare, cu definiția începutului/sfârșitului și așteptarea precizate. Separat, timpul uman efectiv. |
| Efort uman | Investigație, implementare, review și rework în ambele grupuri; include încercările eșuate sau abandonate. Precizează cum ai măsurat timpul. |
| Calitate | Defecte scăpate, pe severitate, cu numitor și perioadă de observație. Notează criteriile de acceptare și check-urile relevante; declară lipsa urmăririi ulterioare. |
| Review | Efortul reviewerului, constatări utile, rework rezultat și expertiza de domeniu necesară. |
| Cost | Licențe, tot consumul facturat inclusiv eșecurile, infrastructură, setup, întreținere și guvernanță/evaluare recurente. Precizează ipotezele de alocare și amortizare. |
| Independență | Dacă alt inginer poate opera workflow-ul și interpreta dovezile fără champion. |
| Decizie și limite | Ce susține extinderea, schimbarea sau oprirea; incertitudine, factori de confuzie și următoarea observație necesară. |

Ponderea PR-urilor atinse de agent descrie adopția. Nu e o țintă de rezultat. O schimbare de cycle time nu stabilește capacitate eliberată, bani economisiți sau calitate neschimbată. Cu un eșantion mic sau o fereastră scurtă de observare a defectelor, spune ce ai observat; nu înlocui dovezile lipsă cu „în marja de zgomot”.

---

### Cât costă programarea cu agenți? {#how-much-does-it-cost}

**Numără costul complet al livrării, apoi compară munca utilă acceptată.** O ofertă de abonament e ușor de găsit; investigația, review-ul, încercările eșuate și întreținerea sunt mai ușor de ratat. Prețurile și contractele se schimbă. Folosește structura de mai jos cu propriul acord și propriile înregistrări.

- **Licențe fixe.** O taxă lunară cu adevărat fixă rămâne aceeași când crește utilizarea. Costul efectiv per task util scade pe măsură ce crește utilizarea utilă. Asta nu face valoros orice output suplimentar generat. Plafoanele de consum, depășirile și schimbările de tier se verifică separat.
- **Consum contorizat.** Numără tot ce se facturează pe toate încercările, inclusiv retry-uri, muncă abandonată și agenți suplimentari. Folosește facturi sau înregistrări de consum, nu numărul de tokeni al răspunsului final.
- **Termeni enterprise.** Angajamentele, alocările, controalele de acces, retenția, facilitățile de audit și protecțiile contractuale diferă. Verifică ce oferă acordul și ce cere pilotul; eticheta nu stabilește termenii.

Separă setup-ul inițial de munca recurentă:

| Cost | Ce incluzi |
|---|---|
| Livrarea task-urilor | Investigație umană, implementare, review și rework, inclusiv încercări eșuate, în ambele părți ale comparației. |
| Tooling și infrastructură | Licențe suplimentare, consum contorizat, medii și servicii conectate. |
| Setup inițial | Munca inițială pe instrucțiuni, integrări și controale; precizează perioada de amortizare. |
| Întreținere continuă | Actualizarea instrucțiunilor, skill-urilor, integrărilor și controalelor pe măsură ce sistemul se schimbă. |
| Guvernanță și evaluare recurente | Review de risc de vendor, review de acces, măsurare, verificarea controalelor și procurement care continuă după setup. |

Separă trei rezultate: timp de livrare mai scurt, capacitate utilă de engineering eliberată și economii efective de bani. Un tarif orar complet atribuie o valoare capacității în comparație; nu înseamnă că scade payroll-ul când un task durează mai puține ore. Notează cum folosești timpul eliberat.

---

### Pârghiile structurale {#cost-levers}

**Schimbă o pârghie de cost doar verificând și rezultatele pe care trebuie să le păstreze.** O rulare mai ieftină care ratează cerința e o încercare eșuată, nu o economie.

- **Effort și alegerea modelului.** Compară setările pe task-uri reprezentative. Folosește mai mult raționament sau un model mai puternic unde schimbă rezultatul suficient cât să-și justifice costul; folosește o setare mai ieftină unde dovezile susțin alegerea.
- **Prefixuri stabile și caching.** Unde providerul suportă prefix caching, instrucțiunile stabile înaintea conținutului variabil pot reduce costul input-ului repetat. Verifică eligibilitatea, cache hit-urile reale și tarifele facturate.
- **Încărcarea tool-urilor.** Încarcă ce cere task-ul. Schemele amânate pot reduce contextul inițial unde clientul le suportă; confirmă că tool-urile necesare rămân descoperibile.
- **Gestionarea contextului.** Studiul JetBrains citat a comparat mascarea observațiilor și rezumarea cu istoricul negestionat, în cinci configurații. Ambele au redus substanțial costul în majoritatea setup-urilor; mascarea a fost mai ieftină decât rezumarea în patru din cinci. Configurația Qwen3-Coder 480B a economisit 52.7%, respectiv 50.4%, față de istoricul negestionat. Nu e o economie universală de 50% din înlocuirea rezumării cu mascarea.
- **Workflow și rutare.** Compară workflow-ul nativ cu skill-uri, revieweri sau aranjamente de tip advisor opționale, pe task-uri comparabile. Include pornirea, review-ul și coordonarea. Aranjamentul potrivit depinde de task și model.

Anexa C înregistrează sursele și aria lor. Verifică din nou rezultatul relevant înainte să-l transformi într-o ipoteză de buget.

---

### Un exemplu complet {#a-worked-example}

**Comparație lunară ipotetică, nu rezultat măsurat sau ofertă de vendor.** O echipă de douăzeci de ingineri acceptă douăzeci de schimbări comparabile în pilot. Calculul presupune rezultate utile comparabile pentru aritmetică; nu stabilește calitate egală și nu dovedește că agenții au cauzat diferența de efort.

Pentru aceste schimbări, baseline-ul folosește **200 de ore umane de task**, iar workflow-ul asistat de agent **160**. Ambele includ investigație, implementare, review, rework și încercări eșuate sau abandonate. Evaluează timpul uman la un tarif complet ilustrativ de **$100 pe oră**. Costurile comune neschimbate sunt omise din ambele părți.

| Cost lunar pentru 20 de schimbări acceptate | Baseline | Asistat de agent |
|---|---:|---:|
| Timp uman de task: 200h / 160h la $100/h | $20,000 | $16,000 |
| Licențe suplimentare | — | $530 |
| Consum contorizat, inclusiv încercări eșuate | — | $270 |
| Infrastructură suplimentară | — | $100 |
| Setup inițial: 120h × $100 = $12,000, amortizat pe 12 luni | — | $1,000 |
| Întreținerea instrucțiunilor/integrărilor: 10h × $100 | — | $1,000 |
| Guvernanță/evaluare recurente: 4h × $100 | — | $400 |
| **Total lunar modelat** | **$20,000** | **$19,300** |
| **Cost modelat per schimbare comparabilă acceptată** | **$1,000** | **$965** |

Orele de întreținere și guvernanță sunt muncă operațională suplimentară, separată de cele 160 de ore de task. Review-ul și rework-ul task-urilor apar doar în timpul de task. Setup-ul inițial apare doar în linia amortizată. Toate încercările contribuie la efort și consum, chiar dacă doar schimbările acceptate formează numitorul.

Calculul valorii este:

**$4,000 valoarea capacității de task eliberate − $900 tooling/infrastructură − $1,000 setup amortizat − $1,000 întreținere continuă − $400 guvernanță recurentă = $700 valoare netă modelată a capacității pe lună.**

Acei $700 nu sunt economii de bani sau o prognoză. Setup-ul inițial consumă 120 de ore la început; amortizarea îi distribuie valoarea în comparație, fără să schimbe momentul muncii. Altă durată de utilizare, mai mult review, mai puține task-uri acceptate, calitate mai slabă sau capacitate eliberată rămasă nefolosită pot schimba rezultatul. Timpul de livrare nu e specificat de aceste totaluri de ore umane.

Într-un pilot real, înlocuiește fiecare ipoteză cu o înregistrare sau eticheteaz-o ca estimare. Compară fișa de măsurare împreună cu aritmetica. Costul per task acceptat e util doar când munca și rezultatele acceptate sunt comparabile; douăzeci de fix-uri ușoare și douăzeci de schimbări cu consecințe importante nu devin echivalente fiindcă ambele seturi au douăzeci de elemente.

---

**Vezi și:** [Anexa B.4](#template-b4) (condițiile task-ului și fișa de pregătire), [Anexa B.5](#template-b5) (calendarul ilustrativ de rollout), [Anexa B.10](#template-b10) (comparație de workflow-uri pe task-uri similare), Anexa C (surse).

---

## Anexa B - Template-uri

Unsprezece template-uri și exerciții de copiat și lipit. Toate sunt puncte de plecare; adaptează-le pentru echipa ta.

Template-urile B.1 și B.2 rămân integral în engleză: sunt artefacte pe care le consumă agentul, iar prompturile se scriu în engleză.

### B.1 Promptul de architecture review {#template-b1}

```
Analyze the architecture of this codebase. Produce a structured architecture review document covering:

Repository and scope: [repository, affected areas and exclusions]
Business domain: [known domain and owner who can correct inferences]
Authorization: read-only investigation by default; other actions only [explicit scope]
Time budget: [bounded first pass]
Evidence available: [code, tests, docs, runtime access]
Evidence unavailable: [production state, advisories, business decisions, other gaps]
Commit reviewed: [actual git SHA; state dirty/untracked files separately]
Human review owner: [name/role]

1. Purpose. What does this service do? Who uses it? What business problem does it solve?
2. Top-level structure. Major modules, packages, or folders. One paragraph per major component.
3. Data model. Primary entities, relationships, persistence. Cite specific files and line numbers.
4. Request flows. For the three most important external entry points, trace from entry to persistence. Cite files and lines at each step.
5. Cross-cutting concerns. Authentication, authorization, logging, error handling, configuration. Where do they live?
6. Dependencies. External services, databases, message brokers, third-party APIs.
7. Test posture. Test structure, coverage, gaps.
8. Build and deployment. Cite the configuration files.
9. Risks and unknowns. Fragile code, inconsistent conventions, deprecated dependencies, unresolved patterns.

Cite specific files and line numbers throughout. Separate observed code facts,
inferred business purpose, and unverified operational claims. Configuration is not
proof of production behavior. State ambiguity and unavailable evidence. Suggest
conventions for human review; do not implement them without authorization.
```

### B.2 Scheletul AGENTS.md {#template-b2}

Acesta e un schelet ilustrativ pentru un proiect Java/Spring. Înlocuiește numele, datele incidentelor, comenzile și restricțiile din exemple cu fapte verificate ale proiectului; incidentele din exemplu nu sunt relatări despre repository-ul tău.

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
- In this project's persistence services, use transactions where consistency requires them; use @Transactional(readOnly = true) for appropriate reads and explicit write transactions for mutations. Follow the reviewed service example; this is not a universal Spring restriction.

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
  Păstrează evaluările independente fără verdictele anterioare.
  Acceptă sau respinge constatări cu dovezi; urmărește defecte utile și fals pozitive.
  Oprește repararea când nu mai rămâne o problemă importantă; altă rundă cere dovezi noi.
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
  Notează responsabilul/ordinea de release, compatibilitatea, semnalul de succes,
  declanșatorul intervenției, recuperarea și observația înainte de predarea în producție.
```

### B.4 Fișa de punctare a kill signals {#template-b4}

```
CONDIȚIILE TASK-ULUI — completează înainte de punctare
  Comportamentul/modulul/mediul propus: ______
  Responsabil calificat pentru evaluare: ______
  Greșeala cu consecințe importante și dovezile care ar expune-o: ______
  Acțiuni permise, aprobare necesară, deployment și recuperare: ______
Ceva lipsește sau e necunoscut? Restrânge munca afectată la investigație sau
pregătire supravegheată până rezolvi. Un repository verde nu autorizează singur un task.

SEMNALE DE PREGĂTIRE — 0 lacună absentă / 0.5 parțială / 1 substanțială / ? necunoscut
Pentru fiecare, notează dovezi, responsabil și acțiunea următoare. Nu transforma ? în 0.

1 Verificare insuficientă
  0    rezultate/eșecuri importante asertate; rulări fiabile; eșecuri înțelese
  0.5  câteva check-uri relevante, cu lacune delimitate și numite
  1    check-uri absente sau nefiabile nu expun greșelile cu consecințe importante
  ?    comportament sau aserțiuni neinvestigate; coverage-ul singur nu decide
2 Fără documentație
  0    explicație și decizii actuale pentru comportamentul afectat
  0.5  explicație utilizabilă cu lacune numite
  1    comportamentul/deciziile necesare nu sunt disponibile
3 Cuplare strânsă
  0    contracte clare și efecte înțelese ale schimbării
  0.5  câteva efecte între module, cu puncte de separare cunoscute
  1    efectele nu pot fi delimitate fără investigație mai amplă
4 Reguli de business împrăștiate
  0    responsabil/sursă canonică pentru regulile relevante
  0.5  reguli duplicate cu reconciliere cunoscută
  1    reguli contradictorii fără autoritate cunoscută
5 Constrângeri de reglementare
  0    aprobări și dovezi necesare susținute de un workflow stabilit
  0.5  task-ul cere pregătire suplimentară pentru aprobare/dovezi
  1    calea necesară de aprobare sau dovezi nu e disponibilă
6 Echipa nu poate evalua output-ul
  0    reviewer calificat disponibil pentru domeniul afectat
  0.5  expertiză disponibilă, dar handoff fragil
  1    niciun evaluator calificat: condiție neîndeplinită indiferent de total
7 Potrivirea model-context
  0    modelul folosește contextul oferit pe task-uri reprezentative și delimitate
  0.5  lacune cunoscute cer documentație sau supraveghere suplimentară
  1    neînțelegeri importante persistă în munca propusă
8 Viteza schimbării
  0    versiuni-țintă și compatibilitate înțelese
  0.5  limitele migrării sunt cunoscute, dar cer grijă
  1    ținte în schimbare sau compatibilitate nerezolvată

Fără necunoscute, adună și rotunjește jumătățile în sus. Euristică, nu scor de siguranță:
  0-1 VERDE puține lacune / 2-3 GALBEN pregătire substanțială / 4+ ROȘU pregătire amplă
Condițiile task-ului au prioritate față de culoare. Investighează necunoscutele întâi.
Următorul task permis: ______  Restricție: ______  Responsabil/check/dată: ______
```

### B.5 Calendarul de adopție în 90 de zile (one-pager) {#template-b5}

```
ÎNAINTE SĂ ÎNCEPI
  Serviciu/cont aprobate: ______  Repository-uri/date permise: ______
  Responsabil și reviewer calificat: ______
  Controale/recuperare inițiale verificate: ______  Limită de cheltuieli: ______
  Baseline, eșantion de task-uri comparabile și criterii de oprire/extindere: ______
CHAMPION
  Săptămâna 1      instalează agentul; architecture review (B.1) pe un codebase familiar; dă-i commit
  Săptămâna 2      verifică instrucțiunile (B.2); adaugă doar ce cere pilotul
  Săptămânile 3-4  funcțiile din B.3 pe trei feature-uri; proces potrivit fiecăruia
  Luna 2           trei feature-uri medii; atrage alți ingineri în faze individuale
  Luna 3           predă rolul unui succesor; AGENTS.md e al echipei
LEAD
  Săptămâna 1      clasifică top 5 proiecte după cele 8 kill signals (B.4)
  Săptămânile 2-4  pentru fiecare culoare, scrie ce ar trebui să se schimbe ca să muți un proiect
  De la început    notează timpul de ceas și uman efectiv, calitatea, review/rework și toate costurile
  Luna 3           prezintă rezultate oneste
MANAGER
  De la început    confirmă eligibilitatea/bugetul; evaluează rezultate fără cote de PR-uri individuale
  Zilele 61-67     preia hand-off-ul; verifică dacă metricile din dashboard sunt reale
  Zilele 68-74     închide decizia seat-vs-enterprise (Anexa A)
  Zilele 75-81     verifică extinderea și guvernanța recurentă; aprobarea inițială a fost înainte de pilot
  Zilele 82-90     raportează observații, costuri și limite; decide extindere/schimbare/oprire
```

Reutilizează fișa de măsurare; datele sunt exemple, nu un calendar obligatoriu de extindere. Ponderea PR-urilor atinse de agent măsoară adopția, nu rezultatul.

| Măsură | Ce notezi |
|---|---|
| Comparație | Date, versiuni de model/workflow, tipuri/selecție de task-uri, numere brute încercate/finalizate/acceptate și baseline |
| Livrare | Definiția timpului de la început până la acceptare; separat timpul uman efectiv |
| Calitate | Defecte scăpate pe severitate, numitor și fereastră de observație; urmărire ulterioară necunoscută |
| Review | Efortul reviewerului, constatări utile, rework și expertiză necesară |
| Cost | Tot consumul facturat și încercările eșuate, licențe/infrastructură, setup amortizat, întreținere și guvernanță recurentă |
| Independență | Alt inginer poate opera workflow-ul și interpreta check-urile |
| Decizie | Extindere/schimbare/oprire, limitări și următoarele dovezi necesare |

Arcul grassroots pentru echipele care nu au toate cele trei roluri: Capitolul 9. Anexa A completează o comparație ipotetică de cost; nu înlocui efortul sau banii economisiți cu cycle time-ul PR-urilor.

### B.6 Contractul buclei exterioare (one-pager) {#template-b6}

```
Înainte de orice rulare nesupravegheată, completează fiecare linie. O linie goală înseamnă că bucla nu e gata.

MUNCA
  Queue: ______ (în repo; câte o unitate mică, similară, reversibilă per element)
  Eligibilitate: fiecare unitate îndeplinește condițiile din B.4; verificabilă independent
  și recuperabilă în controalele rulării nesupravegheate. Un scor verde nu ajunge.
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
  Copie de lucru și branch dedicate, niciodată branch-ul default
  Acoperire tool/sandbox verificată; fără credențiale de producție; testează rutele de rețea/DNS
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
SEMNE DE INVESTIGAT când agentul
  răspunde din nou la o întrebare rezolvată deja; citează o versiune învechită a
  unui fișier pe care l-a editat; uită o constrângere pe care o respecta; se
  degradează târziu într-o sesiune lungă.
ATUNCI
  Verifică starea reală, cerințele contradictorii, sursele învechite și accesul lipsă.
  Corectează cauza. Dacă deriva continuă, reia într-o sesiune curată, cu starea necesară.
  Fă commit după practica repo-ului.
COMPACTARE (trateaz-o ca pe un handoff)
  Compară strategiile suportate de mascare/rezumare după rezultate și consum. Istoricul
  e append-only pe Fable 5.1: repornește, nu edita. Rezumarea poate omite sau deforma
  detalii; salvează durabil deciziile, constrângerile și dovezile indispensabile.
  Dă-i compactorului o listă de păstrat: planul, întrebările deschise, devierile,
  comenzile care au mers. Nu presupune că detaliile din afara listei vor supraviețui;
  verifică handoff-ul înainte să continui.
```

Exemplu complet de handoff, un checkpoint sintetic de exercițiu, nu logul unei sesiuni reale:

```
Obiectiv: adaugă Wire priority păstrând răspunsurile v1 și comportamentul de retry.
Decizii acceptate: patru valori enum; absent/null => NORMAL; doar URGENT intră în queue;
  refuză crearea urgentă când queue-ul e indisponibil; audit priority ales; replay o dată.
Revizie curentă: snapshot didactic wire-v1; nu se pretinde un SHA de commit Git.
Fișiere schimbate: wire.py, defective.py, tests.py, verify.py, README.md; baseline.py păstrat.
Nerezolvat: durabilitate/atomicitate reală de queue și compatibilitatea consumatorilor din producție.
Abordare eșuată: aserțiunea de existență a evenimentului trecea când priority lipsea.
Check-uri rulate: slab-verde, corectat-roșu așteptat, suită reparată verde prin verify.py.
Următorul pas: reviewer calificat inspectează dovezile de acceptare și ipotezele de release;
  aceste teste de model nu autorizează deployment în producție.
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

### B.9 Checklist-ul de evaluare a modelelor, harness-urilor și skill-urilor (one-pager) {#template-b9}

Rulează-l după schimbări de model, harness sau skill și când rezultatele se înrăutățesc. Nu e al nouălea kill signal: verifici dacă workflow-ul mai ajută în configurația curentă. Migrarea la alt model cere și verificările de compatibilitate de mai jos.

```
BASELINE
  Alege task-uri reprezentative și fixează criteriile de acceptare înainte de rulări.
  Include și cazuri în care skill-ul nu ar trebui să se declanșeze.
  Notează modelul, effort-ul, versiunile harness-ului/workflow-ului, commit-ul
  de pornire și permisiunile.
COMPARAȚIE
  Compară configurația curentă și cea propusă pe task-uri similare; documentează
  ce s-a schimbat. Pentru un skill sau plugin opțional, compară execuția nativă
  cu el activat/dezactivat pe fiecare model: același effort, commit, aceleași
  permisiuni și criterii, sesiuni proaspete. Repetă suficient ca să vezi variația;
  nu alege doar cea mai bună rulare.
MĂSURĂTORI
  Corectitudine, cerințe îndeplinite și regresii, nu doar respectarea procesului.
  Consum total facturat, inclusiv cache și subagenți; timp de ceas, review uman
  și rework.
  Mai multe tool call-uri sau tokeni nu sunt automat mai multă valoare ori aceeași
  creștere procentuală a facturii.
PROMPTURI ȘI FIȘIERE DE INSTRUCȚIUNI
  Citește ghidul modelului. Retestează regulile imperative, delegarea și prompturile
  de verificare; încearcă să retragi instrucțiunile redundante, păstrând constrângerile
  locale și controalele de securitate. Verifică trigger-ele și prescripțiile excesive
  din skill-uri. Verifică descoperirea și prioritatea instrucțiunilor (B.2);
  nu presupune că AGENTS.md sau CLAUDE.md se încarcă identic în alt client.
COMPATIBILITATE LA MIGRARE
  Elimină parametrii API respinși de noul model; verifică formatele de output suportate.
  Unde există controale de effort, compară nivelurile după task sau fază; numele nu se
  transferă între modele. Păstrează setarea curentă ca baseline de comparație.
  Retestează schemele de tool-uri custom, inclusiv decodarea strictă unde e suportată;
  verifică limitele schemelor și numără tool-urile vizibile. Verifică cerințele clientului
  pentru istoric și compactare, apoi compară rezultatele, folosirea cache-ului și costul facturat.
DECIZIE
  Păstrează, simplifică, limitează la anumite task-uri sau la invocare manuală ori
  dezactivează workflow-ul opțional, după beneficiul observat. Notează versiunile și
  limitele comparației. Dacă rezultatele continuă să scadă, revino la semnalele din Capitolul 8.
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

Exercițiile testează judecata, nu numărul de documente. Capitolele 2, 7 și 8 adaugă o fișă de control reproductibilă, o hartă de arhitectură revizuită și o fișă de pregătire a task-ului. [Pachetul Wire](/companion/wire-v1.zip) oferă exemple executabile și răspunsuri explicate mai amplu.

**Capitolul 1 - Ce este un agent**

1. Inspectează doi coding agents open source: „Găsește context, tool-uri, Permisiuni / Sandbox, skill-uri, plugin-uri, MCP, Memory, Effort și subagenți. Citează fișierul/modulul care le implementează sau raportează absent/extern/necunoscut. Distinge afirmațiile documentate de comportamentul observat.”
2. Compară dovezile. Împachetarea diferită și capabilitățile absente sunt constatări valide; nu forța implementarea să se potrivească framework-ului.

**Capitolul 6 - AGENTS.md și contextul**

1. Alege un repository al cărui fișier de instrucțiuni e gol, învechit sau scris de cineva care a plecat.
2. Inspectează instrucțiunile existente și un modul relevant. Întreabă ce convenții neintuitive, comenzi sau capcane i-ar scăpa altfel unui agent; verifică răspunsul în cod și cu un coleg care cunoaște proiectul.
3. Schițează doar completările utile pornind de la B.2. Pune linkuri către documentele detaliate în loc să copiezi harta repository-ului; evită best practice-urile generice.
4. Compară o sarcină reprezentativă cu și fără fișierul propus, în sesiuni proaspete, de la același commit și cu aceleași criterii de acceptare. Compară rezultatele, efortul de review și consumul, nu doar cât de convingător sună răspunsul.
5. Dă-l unui coleg care n-a mai lucrat în repo; unde se încurcă el, acolo e următoarea ta modificare.

**Capitolul 4 - Cât workflow merită task-ul**

1. Alege un task mic și clar, unul cu dependențe și unul riscant sau nefamiliar. Definește criteriile înainte de rulare.
2. Compară agentul nativ cu un workflow opțional, după B.9; include un caz în care skill-ul ar trebui să rămână inactiv.
3. Notează calitatea, regresiile, consumul facturat cu cache și subagenți, timpul uman, rework-ul și timpul de ceas. Păstrează doar structura care își justifică costul; nu generaliza dintr-un singur rezultat.

**Găsește eroarea de dependență**

Plan propus: rulează simultan workerii de rutare, API și audit; lasă-i să aleagă fiecare reprezentarea priority; stabilește recordul/default-ul după aceea. Ce trebuie schimbat?

*Răspuns:* stabilește reprezentarea comună, default-urile și politica de eșec înaintea implementării dependente. Apoi folosește etape care respectă dependențele sau un singur implementator, un singur scriitor pe zonele suprapuse și un check de integrare. Explorarea independentă poate propune alternative mai devreme; nu poate impune tacit contracte contradictorii.

**Găsește aserțiunea insuficientă**

Criteriul de acceptare cere priority ales în eveniment. Testul verifică doar un eveniment, tipul și ID-ul wire-ului. Ce poate rămâne greșit?

*Răspuns:* priority poate lipsi sau poate fi incorect. Verifică valoarea față de input-ul ales, demonstrează eșecul pe defect, apoi repară și rerulează. Exercită toate valorile ca să excluzi un fix hardcodat. Și egalitatea exactă a evenimentului poate fi validă dacă o cere contractul acceptat.

**Alege dimensiunea workflow-ului**

Compară un typo în textul de ajutor, un câmp priority care traversează stocare/API/audit/rutare și un algoritm de ledger nefamiliar, fără reviewer calificat.

*Răspuns:* typo-ul cere inspecție directă, editare, verificare focalizată și livrare obișnuită. Schimbarea priority cere decizii explicite, dependențe ordonate, dovezi pentru eșec/retry și predare către producție. Restrânge schimbarea ledger-ului până stabilești evaluarea și verificarea. Artefacte și numere de agenți alternative sunt acceptabile când acoperă deciziile și controalele.

**Observă doi sau trei cititori din publicul-țintă**

Dă-i fiecărui inginer aceste task-uri fără să-i explici răspunsurile înainte:

1. În exercițiul Wire, identifică ce nu dovedește aserțiunea slabă, înainte să citești răspunsul sau să rulezi verifier-ul.
2. Aplică B.4 unei schimbări reale propuse. Explică ce muncă poate continua, ce trebuie să aștepte și ce dovezi ar schimba decizia.
3. Folosește Anexa A ca să distingi timpul de livrare, efortul uman și valoarea financiară modelată; explică de ce exemplul de cost nu stabilește economii de bani.

Cere-le cititorilor să gândească cu voce tare. Notează prima lor interpretare, ezitările, dovezile citate și orice ajutor oferit; un răspuns obținut cu indicii nu e un succes independent. Discută răspunsurile după exerciții și revizuiește pasajele care cer în mod repetat explicații verbale. Tabelul este o fișă goală de observație, nu rezultatul unui trial.

| Cititor / task | Prima interpretare sau ezitare | Dovezi citate / ajutor oferit | Editare propusă |
|---|---|---|---|
| | | | |

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
**Unde e folosită:** Anexa D, Capitolul 2 (trei clase de vulnerabilități din spatele straturilor unu-trei).
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

**Afirmația:** Cercetătorii Mozilla 0Din au demonstrat un proof of concept de prompt injection indirect în care un repository determină Claude Code să preia un payload printr-un DNS TXT record și să-l execute.
**Sursa:** June 2026 report: [SecurityWeek](https://www.securityweek.com/new-attack-abuses-claude-code-and-harmless-looking-repositories-to-hijack-developer-machines/). Documentație curentă despre acoperirea rețelei: [Anthropic sandbox-runtime README](https://github.com/anthropics/sandbox-runtime/blob/main/README.md#network-isolation-architecture).
**Unde e folosită:** Capitolul 2; Anexa D, Capitolul 2 (proof of concept-ul DNS TXT).
**Atenție:** Relatarea incidentului e acoperire secundară a unui proof of concept. Un allowlist de proxy nu stabilește izolarea DNS: verifică separat conexiunile directe, resolverul de sistem și tool-urile DNS directe. Runtime-ul documentează cereri neîngrădite prin resolverul de sistem pe ruta sa Windows și comportament similar pe macOS. Suportul Windows al runtime-ului separat nu înseamnă suport de sandbox nativ Windows în Claude Code. Aria curentă a fost verificată pe 23 octombrie 2026.

---

### Documentația tool-urilor

**Afirmația:** Codex CLI a livrat Agent Skills ca componentă principală de primă clasă în decembrie 2025, cu fișiere SKILL.md cu frontmatter YAML și semantici de progressive disclosure comparabile cu Skills din Claude Code.
**Sursa:** OpenAI Codex CLI docs, [developers.openai.com/codex/skills](https://developers.openai.com/codex/skills).
**Unde e folosită:** Anexa D, Capitolul 1 (Memory și skill-uri: povestea convergenței), ca partea Codex a convergenței pe componenta principală de skill.
**Atenție:** Documentație de vendor; datele de GA sunt corecte la mijlocul lui 2026, dar pot fi revizuite retroactiv.

---

**Afirmația:** Codex CLI suportă concurență configurabilă de subagenți prin `agents.max_concurrent_threads_per_session`, excluzând thread-ul principal. `agents.max_threads` e un alias legacy; fără setare, Codex alege default-ul. Un default istoric de șase nu era un plafon fix al platformei.
**Sursa:** OpenAI, Configuration Reference: [learn.chatgpt.com/docs/config-file/config-reference#agentsmax_concurrent_threads_per_session](https://learn.chatgpt.com/docs/config-file/config-reference#agentsmax_concurrent_threads_per_session); [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents).
**Unde e folosită:** Anexa D, Capitolul 1 (cronologia adoptării subagenților).
**Atenție:** Documentație oficială de CLI verificată pe 23 octombrie 2026. Setările clientului, resursele și politica limitează în continuare concurența reală. Sunt setări CLI, nu limite ale Agents API; documentația curentă citată nu stabilește data GA de 14 martie menționată anterior.

---

**Afirmația:** Codex CLI documentează [AGENTS.md](https://agents.md/) drept convenția pentru instrucțiuni de agent la nivel de proiect, încărcată la începutul sesiunii și echivalentă ca rol cu fișierele de instrucțiuni de echipă ale celorlalți vendori.
**Sursa:** OpenAI Codex CLI documentation, [developers.openai.com/codex/agents-md](https://developers.openai.com/codex/agents-md).
**Unde e folosită:** Capitolul 1 (Memory) și Capitolul 6 (Ce este AGENTS.md?).
**Atenție:** Numele fișierului și semantica de încărcare sunt stabile; regulile specifice de frontmatter și de descoperire pot evolua de la o versiune la alta.

---

**Afirmația:** AGENTS.md e o convenție comună pentru instrucțiunile proiectului, dar descoperirea și precedența diferă. Codex îl încarcă nativ, cu precedență pe directoare; Claude are comportament de fallback/import dependent de versiune; Gemini CLI folosește implicit GEMINI.md și poate configura AGENTS.md; Aider suportă includere explicită read-only.
**Sursa:** [Codex project instructions](https://learn.chatgpt.com/docs/agent-configuration/agents-md); [Claude Code memory](https://code.claude.com/docs/en/memory#agentsmd); [Gemini CLI context files](https://geminicli.com/docs/cli/gemini-md/); [Aider conventions](https://aider.chat/docs/usage/conventions.html).
**Unde e folosită:** Capitolele 1 și 6 (tabelul de compatibilitate a instrucțiunilor); Anexa D, Capitolul 1.
**Atenție:** Verificat pe 23 octombrie 2026. Un nume Markdown comun nu înseamnă arie, ierarhie, precedență sau încărcare automată identice. Inspectează sursele efective în clientul instalat; tabelul nu e un inventar exhaustiv de vendori.

---

**Afirmația:** opencode e un coding agent open-source întreținut de o echipă independentă, scris în TypeScript și licențiat sub MIT. Codul sursă e organizat în jurul acelorași componente principale pe care manualul ăsta le identifică în Codex CLI și Claude Code.
**Sursa:** opencode repository ([github.com/anomalyco/opencode](https://github.com/anomalyco/opencode); fost sst/opencode - compania care îl întreține s-a redenumit Anomaly în ianuarie 2026); LICENSE and README.
**Unde e folosită:** Capitolul 1 (Anatomia e invariantă, dovada cu doi agenți) și Anexa D, Capitolul 1 (demo-ul cu doi agenți, în detaliu).
**Atenție:** Numele proiectului și componența echipei de mentenanță pot evolua; afirmația despre convergența arhitecturală supraviețuiește redenumirilor.

---

**Afirmația:** Locatorii semantici Playwright pot rezista schimbărilor de stil și DOM cât timp contractul de accesibilitate rămâne stabil. Acțiunile depind de control: selectOption vizează select-uri native; check vizează checkbox-uri/radio-uri.
**Sursa:** Playwright [locators](https://playwright.dev/docs/locators#locating-elements), [select options](https://playwright.dev/docs/input#select-options), [checkboxes and radios](https://playwright.dev/docs/input#checkboxes-and-radio-buttons).
**Unde e folosită:** Capitolul 5 (Verify); Anexa D, Capitolul 5; Anexa B.3.
**Atenție:** Documentație curentă verificată pe 23 octombrie 2026. Schimbarea bibliotecii de componente sau a modelului de interacțiune poate cere noi acțiuni/locatori. Aserțiunile de comportament nu verifică layout-ul randat.

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

**Afirmația:** Clienții și serverele MCP negociază versiuni de protocol și capabilități. Reutilizarea integrării depinde și de transporturile și autentificarea suportate; suportul MCP singur nu stabilește interschimbabilitatea.
**Sursa:** Versioned MCP specification, June 18, 2025: [lifecycle](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#version-negotiation), [transports](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports), [authorization](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization).
**Unde e folosită:** Capitolul 1 (Ce este MCP?).
**Atenție:** Specificația versionată a fost verificată pe 23 octombrie 2026; nu se afirmă că iunie 2025 e cea mai recentă ediție a protocolului. Verifică ambele endpoint-uri și capabilitățile necesare.

---

**Afirmația:** Spring suportă tranzacții read-only în service, pe lângă cele de scriere, și validare la nivel de metodă. O convenție de validare în controller trebuie să-și precizeze scope-ul fără să elimine responsabilitatea de service/domain pentru invariantele de business.
**Sursa:** Spring Framework 7.0.10 reference: [transaction annotations](https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative/annotations.html), [service method validation](https://docs.spring.io/spring-framework/reference/core/validation/beanvalidation.html#validation-beanvalidation-spring-method).
**Unde e folosită:** Capitolul 6 (convenții delimitate); Anexa B.2.
**Atenție:** Verificat pe 23 octombrie 2026. Granițele de tranzacție și validare sunt alegeri arhitecturale; comportamentul proxy/cale de apel și exemplele proiectului trebuie verificate. Documentația nu stabilește un efect în colaborarea privată din carte.

---

**Afirmația:** O migrație undo e opțională și nu poate inversa fiabil orice schimbare distructivă de date sau eșec parțial. Recuperarea poate folosi în schimb deployment compatibil cu versiunile anterioare, corecție roll-forward sau restaurare testată.
**Sursa:** Redgate Flyway, [Undo migrations](https://documentation.red-gate.com/flyway/flyway-concepts/migrations/undo-migrations), updated May 21, 2026.
**Unde e folosită:** Capitolele 4–5 (review-ul migrației Wire); companionul practic.
**Atenție:** Verificat pe 23 octombrie 2026. Strategia potrivită depinde de sistem și de obiectivele necesare de recuperare. Documentația nu dovedește politica unei colaborări cu clientul care nu a fost publicată.

---

### Marketplace-uri și ecosisteme de plugin-uri

**Afirmația:** Marketplace-ul `claude-plugins-official` al Anthropic vine inclus în Claude Code din mai 2026 și împachetează skill-uri, hook-uri, tool-uri și comenzi în spatele unei singure comenzi de instalare. Marketplace-ul avertizează utilizatorii să verifice dacă au încredere în plugin-uri înainte să le instaleze.
**Sursa:** Claude Code docs ([code.claude.com/docs/en/discover-plugins](https://code.claude.com/docs/en/discover-plugins)); the marketplace itself.
**Unde e folosită:** Capitolul 1 (Plugin-uri); Anexa D, Capitolul 1 (plugin-uri: de ce există fiecare întrebare de vetting).
**Atenție:** Numărul de plugin-uri și politicile marketplace-ului se vor schimba în timp; ce trebuie să iei cu tine e disciplina de supply chain descrisă în Capitolul 1, nu vreun număr anume.

---

### Surse pentru componenta principală Memory

**Afirmația:** Instrucțiunile proiectului asigură un strat de memorie întreținut manual în tool-urile de coding. AGENTS.md e una dintre convenții; unii clienți au alt nume implicit sau cer configurare/încărcare explicită. Un fișier CLAUDE.md poate importa instrucțiunile comune prin `@AGENTS.md`.
**Sursa:** [agents.md](https://agents.md/); documentația de încărcare specifică fiecărui client din intrarea de compatibilitate de mai sus și din Capitolul 6.
**Unde e folosită:** Capitolele 1 și 6; Anexa D, Capitolul 1 (Memory și skill-uri).
**Atenție:** Descoperirea a fost verificată pe 23 octombrie 2026. Rolul structural e comun; încărcarea automată, precedența și numele disponibile nu sunt. Nu deduce suport pentru AGENTS.override.md într-un client din comportamentul Codex.

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

**Afirmația:** Codex folosește izolare la nivel de OS specifică platformei. Documentația curentă descrie Seatbelt pe macOS, `bwrap` plus `seccomp` implicit pe Linux și MXC pe Windows, cu implementările legacy `elevated` și `unelevated` ca fallback. WSL2 folosește implementarea Linux. Aprobările sunt un control separat.
**Sursa:** OpenAI, "Agent approvals & security," [OS-level sandbox](https://learn.chatgpt.com/docs/agent-approvals-security#os-level-sandbox); [Windows sandbox](https://learn.chatgpt.com/docs/windows/windows-sandbox).
**Unde e folosită:** Capitolul 1 (Permisiuni / Sandbox; Postura sandbox-ului e o alegere de guvernanță) și Capitolul 2 (Stratul 2: Sandbox); Anexa D, Capitolul 1 (postura de sandbox pe vendor și mecanismele de dedesubt).
**Atenție:** Documentație verificată pe 23 octombrie 2026. Verifică versiunea instalată, backend-ul selectat și profilul efectiv de permisiuni; suportul pe platforme și mecanismele de enforcement diferă. Codex poate fi configurat și să ruleze fără sandbox-ul propriu. Descrierea unui backend nu stabilește acoperirea tuturor tool-urilor sau serviciilor conectate.

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

**Afirmația:** RULER definește contextul efectiv prin cea mai mare lungime testată care depășește un prag fix de benchmark derivat din Llama2-7B la 4K; Tabelul 3 folosește 85.6%. Nu e păstrarea scorului propriu de context scurt al fiecărui model.
**Sursa:** Cheng-Ping Hsieh et al., "RULER: What's the Real Context Size of Your Long-Context Language Models?", v3, August 6, 2024: [effective context and Table 3](https://arxiv.org/html/2404.06654v3#S4).
**Unde e folosită:** Capitolul 1 (Context window); Anexa D, Capitolul 1.
**Atenție:** Treisprezece task-uri sintetice și modelele din 2024 testate. Rezultatele nu stabilesc o regulă universală de jumătate de fereastră sau fracția utilizabilă a contextului unui model actual de coding. Reverificat pe 23 octombrie 2026.

---

**Afirmația:** În cinci configurații SWE-agent/SWE-bench Verified, mascarea observațiilor a fost mai ieftină decât rezumarea în patru. Ambele au redus substanțial costul față de istoricul negestionat în majoritatea setup-urilor; pentru Qwen3-Coder 480B, reducerile au fost 52.7%, respectiv 50.4%, față de acel baseline.
**Sursa:** Tobias Lindenbauer, Igor Slinko, Ludwig Felder, Egor Bogomolov and Yaroslav Zharov, "The Complexity Trap", August 2025, camera-ready October 27: [paper v3](https://arxiv.org/abs/2508.21433v3); [primary Table 1](https://kairos.jetbrains.com/research/articles/the-complexity-trap); [JetBrains December explanation](https://blog.jetbrains.com/research/2025/12/efficient-context-management/).
**Unde e folosită:** Capitolul 6 (Igiena contextului); Anexa A; Anexa B.7; Anexa D, Capitolul 6.
**Atenție:** Exemplul cu peste 50% compară fiecare metodă cu istoricul negestionat, nu mascarea cu rezumarea. Economiile variază mult între configurații. Tabelul 1 nu susține o reducere universală de peste 50%; verificat pe 23 octombrie 2026.

---

**Afirmația:** Pe 15 modele, performanța în conversații multi-turn fragmentate a scăzut cu 39% în medie față de o singură tură complet specificată, iar consolidarea fragmentelor într-o singură tură a recuperat cam 95% din rezultatul single-turn.
**Sursa:** Philippe Laban, Hiroaki Hayashi, Yingbo Zhou, Jennifer Neville, "LLMs Get Lost in Multi-Turn Conversation," May 2025: [arxiv.org/abs/2505.06120](https://arxiv.org/abs/2505.06120).
**Unde e folosită:** Capitolul 6 (Igiena contextului, o unitate de muncă per sesiune); Anexa D, Capitolul 6 (compactare și măsurători de context).
**Atenție:** Conversații simulate pe task-uri de generare, nu sesiuni de coding; manualul o folosește pentru mecanismul din spatele consolidării înainte de a continua.

---

**Afirmația:** Opus 4.8 și Sonnet 5 inventează chei pe care o schemă imbricată de tool custom nu le-a declarat niciodată, în timp ce modelele mai vechi nu, iar pornirea invocării stricte a tool-urilor a eliminat comportamentul.
**Sursa:** Armin Ronacher, "Better Models: Worse Tools," July 4, 2026: [lucumr.pocoo.org/2026/7/4/better-models-worse-tools/](https://lucumr.pocoo.org/2026/7/4/better-models-worse-tools/). Pentru constrângerile providerului: Anthropic, [Structured outputs: important considerations](https://platform.claude.com/docs/en/build-with-claude/structured-outputs#important-considerations) și [Strict tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/strict-tool-use#data-retention); OpenAI, [Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs#supported-schemas).
**Unde e folosită:** Capitolul 1 (Tool-uri); Anexa D, Capitolul 1 (cât costă definițiile de tool-uri și ce răspunsuri dau harness-urile din 2026); Anexa B.9.
**Atenție:** Rulările unui singur practician pe un singur harness. Decodarea strictă poate preveni încălcarea schemei acolo unde e disponibilă; nu stabilește corectitudinea semantică. Verifică compatibilitatea schemei, limitele de complexitate și eventuala latență de compilare pentru providerul și modelul folosite. Anthropic documentează latența de compilare la prima utilizare și limitele comune pentru schemele stricte de tool-uri; OpenAI documentează și limitele schemelor. Documentația providerilor a fost verificată pe 23 octombrie 2026.

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

Sursele își păstrează datele de publicare/versiune. Intrările reverificate în această revizie numesc explicit 23 octombrie 2026; asta nu înseamnă că fiecare afirmație istorică a fost revalidată independent. Pentru o afirmație cu consecințe importante, păstrează sursa directă, versiunea/data, data verificării, setup-ul relevant și interpretarea dedusă. Documentația care se modifică trebuie reverificată înainte să te bazezi pe ea. Fișele de caz relatate de autor nu sunt măsurători controlate, iar companionul sintetic și economia ipotetică sunt artefacte didactice, nu dovezi ale colaborărilor.

---

---

## Anexa D - Deep dives

Aici stau dovezile și detaliile datate din spatele fiecărui capitol: studiile, benchmark-urile, cronologiile vendorilor și cazurile lucrate pe care capitolele le lasă deoparte ca să rămână scurte. Intrările sunt grupate pe capitole, iar fiecare se încheie cu sursele și atenționările ei, în italic. Citările complete sunt în Anexa C; comportamentul vendorilor e datat la mijlocul lui 2026 și se va schimba, așa că verifică default-urile față de versiunea pe care o rulezi.

---

### Capitolul 1 - Ce este un agent {#deep-dive-chapter-1}

**Contextul efectiv depinde de benchmark.** RULER v3 folosește un prag fix derivat din Llama2-7B la 4K (85.6% în Tabelul 3), nu păstrarea scorului propriu de context scurt al fiecărui model. Cele treisprezece task-uri sintetice și modelele din 2024 testate nu stabilesc o regulă universală de jumătate de fereastră pentru agenții actuali de cod. Evaluează lungimile și task-urile pe care intenționezi să le folosești. *Sursa: Hsieh et al., August 6, 2024, Section 4/Table 3; Anexa C. Definiție reverificată pe 23 octombrie 2026.*

**Cât costă definițiile de tool-uri și ce răspunsuri dau harness-urile din 2026.** Un audit al unei sesiuni default de Claude Code a numărat cam 24k de tokeni de definiții de tool-uri, scheme MCP și reminder-e consumați înainte ca utilizatorul să tasteze ceva; socoteala unui practician a pus trei servere MCP la 143k dintr-o fereastră de 200k. Cu un catalog mare de tool-uri încărcat integral, acuratețea selecției într-un benchmark a fost de 13,62%; încărcarea doar a tool-urilor relevante a urcat-o la 43,13%. Răspunsurile din 2026 sunt încărcarea amânată (deferred loading) și apelarea programatică a tool-urilor (modelul scrie un script care face apelurile și întoarce un singur rezultat; nativă în GPT-5.6, unde a tăiat tokenii de input cu 21% pe o evaluare de research financiar). La tool-urile custom cu scheme imbricate, ia în calcul decodarea strictă unde e suportată și verifică limitele schemelor și latența (Anexa C): Armin Ronacher a documentat cum Opus 4.8 și Sonnet 5 inventează câmpuri nedeclarate, iar modul strict le elimină. *Surse: Lumer et al., Jan 31, 2026; anthropics/claude-code#42452, Apr 2, 2026; Gan and Sun (RAG-MCP), May 6, 2025; MetaBlogue, Sep 5, 2026; OpenAI GPT-5.6 guide, Aug 2026; Ronacher, Jul 4, 2026. Atenție: 24k și 143k sunt socoteli de practicieni; cele 21% vin dintr-un singur benchmark (cel de la Rogo).*

**Postura de sandbox pe vendor și mecanismele de dedesubt.** Aria contează la fel de mult ca default-ul. Claude Code are un sandbox de shell opt-in pe macOS, Linux și WSL2; comenzile native Windows, tool-urile native de fișiere, serverele MCP și hook-urile sunt în afara lui. Codex documentează restricții la nivel de OS cu altă implementare și alte platforme suportate; verifică profilul de permisiuni selectat și orice cale de escaladare. opencode documentează controale de permisiuni, iar izolarea de OS e asigurată de un mediu extern. Configurează restricțiile efective de căi și rețea în runtime sau în politica administrată, nu în AGENTS.md. Testează citirile, scrierile și conexiunile interzise prin fiecare cale relevantă. *Surse: documentația Claude Code despre sandbox și permisiuni; documentația de securitate Codex; Vercel KB despre opencode, verificate pe 23 octombrie 2026. Atenție: configurația și acoperirea se schimbă cu versiunea; izolarea shell-ului nu înseamnă izolarea întregului agent.*

**Demo-ul cu doi agenți, în detaliu.** Claude Code a rulat în două panouri, unul peste Codex CLI (Rust, Apache 2.0, OpenAI) și unul peste opencode (TypeScript, MIT, echipă independentă), cu un singur prompt: explică arhitectura, mapează bucla agentului, sistemul de tool-uri, gate-urile de permisiuni, sandbox-ul și modelul de plugin-uri, citând fișiere și linii. A durat cam patru minute (o rerulare din mai 2026: 4:13), pentru că ambele repository-uri își numesc arhitectura în directoare; un codebase mai puțin auto-documentat cere zece-cincisprezece minute per repo. Amândouă au întors o buclă de agent, un registru de tool-uri, un gate de permisiuni, un director de plugin-uri, suport MCP și o cale de dispatch pentru subagenți (în opencode, identificată după comportament: o funcție care pornește o instanță proaspătă pe un prompt delimitat). Singura divergență a fost sandbox-ul. *Sursa: experiment al autorului, fără nicio corecție umană. Limitare: comparația ilustrează capabilități din două repository-uri, nu o anatomie universală sau un rezultat de eficacitate.*

**Configurarea subagenților și istoricul adopției.** Codex CLI expune `agents.max_concurrent_threads_per_session` pentru thread-urile pornite, excluzându-l pe cel principal; `agents.max_threads` e un alias legacy. Default-urile nespecificate sunt alese de client, nu un plafon fix de șase. Alți agenți expun orchestrare proprie, dependentă de versiune. *Surse: OpenAI config reference și Subagents docs, verificate pe 23 octombrie 2026; changelog-uri istorice ale vendorilor. Atenție: documentația curentă nu stabilește data GA de 14 martie menționată anterior; inspectează setările instalate și limitele de resurse.*

**Orchestrare scriptată (`/workflows`).** `/workflows` din Claude Code (mijlocul lui 2026) pune agentul să scrie un script care trimite subagenți în mod determinist: faze în ordine, fan-out în paralel sau printr-un pipeline pe sute de copii, hand-off-uri validate după o schemă, un gate opțional de verificare, reluabil și cu buget limitat. Determinismul e singura diferență reală față de dispatch-ul condus de model (ca în Superpowers); apelează la el când fan-out-ul e mare, repetabil sau merită verificat mecanic. *Sursa: Changelog, 2026-06-11.*

**Memory și skill-uri: roluri comune, încărcare diferită.** Instrucțiunile proiectului au un rol comun, nu descoperire identică. Codex are precedență pe directoare; Claude are fallback/import dependent de versiune; Gemini CLI folosește implicit GEMINI.md și poate configura AGENTS.md; Aider suportă includere explicită read-only. Capitolul 6 consemnează aria și metodele de inspecție. Corpurile de skill și memoria scrisă de agent sunt mecanisme separate, cu propriile reguli de încărcare și retenție. *Surse: documentația oficială Codex, Claude Code, Gemini CLI și Aider, verificată pe 23 octombrie 2026; Anexa C. Atenție: numele comune nu implică încărcare automată sau autoritate egală.*

**Effort: dovezile.** Cu harness-ul ținut constant, GPT-5.6 Sol pe effort low l-a bătut pe GPT-5.5 pe high la Agents' Last Exam; Fable 5.1 pe low e adesea competitiv cu Opus și Sonnet la cost per task, cu scor mai mare, după propriul ghid al vendorului. Numele nivelurilor de effort nu se transferă între modele, așa că orice migrare începe cu un sweep (Anexa B.9). Dacă raționamentul se păstrează între ture e decizia harness-ului: pe ARC-AGI-3, după relatarea OpenAI, raționamentul păstrat plus compactarea au dus GPT-5.6 Sol de la 13,3% la 38,3%, tăind în același timp tokenii de output de șase ori. *Surse: OpenAI GPT-5.6 guide, Aug 2026; OpenAI ARC-AGI-3 post, Jul 29, 2026; Anthropic, "Prompting Claude Fable 5.1." Atenție: evaluări ale vendorilor, pe un singur benchmark și un singur model; manualul folosește ARC-AGI-3 pentru mecanism, nu pentru scor.*

**Plugin-uri: încredere și utilitate.** Verifică maintainerul, permisiunile, hook-urile și codul executat de versiunea instalată; un hook în afara sandbox-ului are alt blast radius. Profunzimea review-ului depinde de suprafață și risc, nu de promisiunea că sursa se citește în douăzeci de minute. Un update de plugin e un update de dependență. Separat, compară beneficiul cu agentul nativ: o instalare de încredere poate totuși adăuga proces inutil. *Surse: practica autorului, mai 2026; ghidurile curente pentru skill-uri și release notes Superpowers, revizuite Oct 23, 2026. Atenție: un endorsement vechi nu validează automat o versiune nouă.*

---

### Capitolul 2 - Guardrails în cinci straturi {#deep-dive-chapter-2}

**Trei clase de vulnerabilități din spatele straturilor unu-trei.** (1) Expunerea secretelor: agenții pot descoperi fișiere `.env*` prin shell sau tool-uri native ori pot moșteni variabile de mediu secrete. Protejează fiecare cale. Setările de credențiale din Claude Code restricționează comenzile din sandbox; regulile de deny-read pentru shell nu blochează tool-ul nativ Read. (2) Injecția prin fișiere de configurare: fișiere `.claude/settings.json` sau `.mcp.json` nesigure execută hook-uri înainte de dialogul de trust, ceea ce deschide calea spre remote code execution (CVE-2025-59536, patch-uită în Claude Code v1.0.111) sau spre exfiltrarea de API key-uri printr-un `ANTHROPIC_BASE_URL` suprascris (CVE-2026-21852, patch-uită în v2.0.65). (3) Ocolirea parser-ului de permisiuni: reguli de deny sărite pentru binare pe care parser-ul nu le recunoaște (`open()` din Python, `fs.readFile` din Node) sau, ca eșec silențios, atunci când o comandă înlănțuia mai mult de cincizeci de subcomenzi (`MAX_SUBCOMMANDS_FOR_SECURITY_CHECK = 50`), iar verificarea cădea pe un „ask” generic; dezvăluită pe 1 aprilie 2026 și patch-uită în v2.1.90 în câteva zile. Nimic din configurație nu arată un asemenea eșec, așa că presupune că orice strat luat singur poate avea un bug; clasele supraviețuiesc patch-urilor lor. *Surse: Knostic, Dec 2025; Check Point Research, Feb 2026 (patch-uit în octombrie 2025); Adversa AI Red Team, Apr 1, 2026; Adam Kinney, Apr 2026. Atenție: clase arhitecturale, nu CVE-uri punctuale; versiunile fără patch rămân vulnerabile.*

**Escape-urile din sandbox („DuneSlide”).** La mijlocul lui 2026, un red team a dezvăluit două vulnerabilități critice zero-click de prompt injection în sandbox-ul cu suport în kernel din Cursor (CVE-2026-50548 și CVE-2026-50549, CVSS 9.8), care abuzau allowlist-ul de scriere pe directorul de lucru și un fallback de rezolvare a symlink-urilor ca să ajungă la execuție de cod la nivel de OS. Versiunile dinainte de Cursor 3.0 (2 aprilie 2026) erau afectate. Lecția e clasa, nu vendorul: și cel mai puternic strat poate avea bug-uri - exact de-asta straturile sunt cinci. *Surse: Cato Networks (Cato AI Labs), mijlocul lui 2026; SecurityWeek and The Hacker News, Jul 2026.*

**Default-urile de sandbox per agent.** Vezi intrarea din Capitolul 1 despre postura de sandbox pe vendor; ideea pentru capitolul ăsta e că o instalare default a unui agent opt-in rulează cu stratul doi oprit.

**Injecția prin materialul de lucru: proof of concept-ul cu DNS TXT.** Relatarea din iunie 2026 descrie un repository care determină Claude Code să preia un payload prin DNS TXT și să-l execute. Un allowlist de proxy HTTP/domenii nu stabilește izolarea DNS. Verifică separat conexiunile directe, tool-urile DNS directe și cererile prin resolverul de sistem, folosind endpoint-uri proprii inofensive. README-ul runtime-ului documentează cereri neîngrădite prin resolverul de sistem pe ruta sa Windows și comportament similar pe macOS. Suportul runtime-ului separat nu înseamnă suport de sandbox shell nativ Windows în Claude Code. *Surse: relatarea din 29 iunie și documentația de rețea Anthropic sandbox-runtime, Anexa C; aria curentă verificată pe 23 octombrie 2026. Atenție: platformele și rutele de rezoluție diferă; un proof of concept nu e o frecvență măsurată.*

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

**Locatori și interacțiuni semantice în Playwright.** Rolurile și etichetele pot rezista schimbărilor de stil/DOM cât timp contractul de accesibilitate e stabil. Acțiunile depind de control: `selectOption()` vizează un select nativ; `check()` selectează un radio/checkbox; un widget custom poate cere alte interacțiuni. Înlocuirea unei componente poate cere actualizarea testului. Verifică comportamentul de business și inspectează schimbările vizuale randate. *Surse: documentația Playwright de locatori/input, verificată pe 23 octombrie 2026; Anexa C. Atenție: stabilitatea semantică nu stabilește compatibilitatea modelului de interacțiune sau corectitudinea vizuală.*

**Măsoară contribuția toolkit-ului de PR review.** Agenții de review pot prinde constatări mecanice înainte ca un senior să citească diff-ul. Măsoară defectele utile găsite, false positive-urile, timpul de review și defectele scăpate, în loc să presupui că patru revieweri economisesc zece minute. Păstrează atenția umană pe corectitudinea de business și potrivirea arhitecturală; cazul din capitol arată ce se întâmplă când atenția asta dispare.

---

### Capitolul 6 - AGENTS.md și contextul {#deep-dive-chapter-6}

**Fișierele de context trebuie să-și justifice conținutul.** Studiul ETH Zürich despre AGENTS.md, v3 din Sep 29, 2026, nu a găsit o îmbunătățire generală a succesului pentru fișierele de context generate și a măsurat un cost de inferență cu peste 20% mai mare în setup-urile testate. Fișierele scrise de developeri au adus un câștig mediu modest, fără semnificație statistică; prezentările de ansamblu ale repository-ului nu au ajutat în această evaluare. Studiul nu dovedește că orice instrucțiune locală dăunează. Păstrează constrângerile pe care agentul nu le poate deduce, comenzile verificate și pointerii; mută detaliile voluminoase în docs/ și compară rezultatele. OpenAI descrie separat un AGENTS.md de circa 100 de linii ca hartă spre documentație structurată. *Surse: Gloaguen et al., „Evaluating AGENTS.md”, v3 Sep 29, 2026; Ryan Lopopolo, OpenAI, Feb 11, 2026. Atenție: agenți și benchmark-uri specifice; selecția conținutului e recomandarea manualului, iar exemplul OpenAI e practica unei singure echipe.*

**Circa 200 de linii este un reper, nu un prag demonstrat.** Studiul din iulie despre respectarea simultană a regulilor măsoară un setup de prompt, nu stabilește la câte linii trebuie tăiat orice AGENTS.md. Nu există o conversie validată între cele circa optzeci de reguli și două sute de linii. Faptul că Anthropic a eliminat peste 80% din propriul system prompt pentru generația Claude 5 susține reevaluarea instrucțiunilor vechi, nu ștergerea constrângerilor utile. *Surse: Netanel Eliav, Jul 21, 2026; Thariq Shihipar, Anthropic, Jul 24, 2026; Claude Code memory docs, verificate Oct 23, 2026. Atenție: metrici și contexte diferite; scurtimea e o disciplină de întreținere, nu o garanție a respectării instrucțiunilor.*

**Suportul nativ AGENTS.md din Claude Code.** Încărcarea directă începe din v2.1.277 prin setarea Project instructions. Fallback-ul implicit verifică CLAUDE.md, .claude/CLAUDE.md și CLAUDE.local.md pe ruta directorului de lucru/directoarelor părinte. Un fișier CLAUDE poate importa @AGENTS.md. Nu sunt regulile de override din Codex; Capitolul 6 include limitele de inspecție/versiune. *Sursa: documentația curentă de memorie, verificată pe 23 octombrie 2026. Atenție: versiunile și setările anterioare diferă.*

**Mecanica jurnalului de greșeli.** Ghidul Anthropic pentru Fable 5 descrie un sistem de memorie cu trei reguli care țin un jurnal onest și la o sută de intrări: o lecție per fișier, cu rezumat de o linie; actualizezi în loc să duplici atunci când lecția se repetă; ștergi notele care se dovedesc greșite. Adaugă un pointer la dovadă, ca următorul champion să poată verifica dacă eșecul mai e posibil. Runtime-ul de afirmații din OpenWiki, care atașează pointeri la dovezi afirmațiilor stocate și le reverifică, a tăiat afirmațiile învechite de la 3,5% la 0,5% pe 2.000 de afirmații evaluate. Review-ul trimestrial pune pentru fiecare intrare întrebarea „a salvat regula asta pe cineva în ultimele trei luni?” Dacă da, o păstrezi; dacă nu, dar regula încă se aplică, o păstrezi, pentru că eșecurile rare contează în continuare; dacă nu, iar cauza a dispărut, o retragi, cu o notă în mesajul de commit. *Surse: Anthropic, "Prompting Claude Fable 5"; Colin Francis, LangChain, Aug 25, 2026. Atenție: OpenWiki e un sistem de bază de cunoștințe, nu un jurnal; manualul împrumută mecanismul.*

**De ce există linia de precedență.** GPT-6 Astra urmărește instrucțiuni mai lungi mai bine și e mai sensibil la context: o îndrumare contradictorie într-un fișier de skill îl poate face să se oprească și să blocheze munca devreme, iar ghidul OpenAI spune că instrucțiunile utilizatorului au prioritate față de ale unui skill. O singură linie în capul fișierului („In a conflict, the task prompt wins over this file; this file wins over any skill”, în scheletul B.2) elimină o clasă de blocaje. *Sursa: OpenAI, "Using GPT-6 Astra," Sep 2026 (GPT-6 lansat pe 3-4 septembrie 2026; ghid revizuit pe loc).*

**Compactare și măsurători de context.** JetBrains a comparat istoricul negestionat, mascarea și rezumarea în cinci configurații SWE-agent/SWE-bench Verified. Mascarea a fost mai ieftină decât rezumarea în patru; Qwen3-Coder 480B a economisit 52.7% cu mascarea și 50.4% cu rezumarea față de istoricul negestionat. Alte configurații au economisit mai puțin; nu rezultă nici o reducere universală de peste 50%, nici acel raport între metode. Anthropic a raportat separat un câștig de 29% din curățarea rezultatelor de tool-uri pe evaluarea internă de căutare. Studiul multi-turn a găsit degradare medie față de o tură complet specificată și recuperare prin consolidare. *Surse: Lindenbauer et al., The Complexity Trap, Table 1; Anthropic, September 29, 2025; Laban et al., May 2025; Anexa C. Atenție: intervenții și setup-uri diferite, nu o comparație controlată de handoff în coding. Baseline de cost reverificat pe 23 octombrie 2026.*

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

**Semnalul 7, potrivirea model-context: workflow engine-ul intern.** Un workflow engine proprietar îi poate fi nefamiliar modelului chiar dacă experții de domeniu îl înțeleg. Verifică tranziții de stare și edge case-uri reprezentative față de comportamentul documentat; investighează contextul lipsă sau alege un model mai potrivit. Documentația publică puțină creează incertitudine de potrivire a modelului, nu automat lipsa unui evaluator calificat. Dacă nici echipa nu poate judeca acel comportament, condiția de evaluare e încălcată separat. *Pattern de caz relatat de autor, nu o regulă măsurată despre popularitatea limbajelor.*

**Semnalul 8, viteza schimbării: bug-ul React 18/19.** Pe un codebase aflat în mijlocul unei migrări, agentul are dreptate cu toată convingerea despre versiunea veche și greșește despre cea nouă, iar nu poți deosebi mereu care e care. Bug-ul autorului: Claude a folosit idiomuri de React 18 acolo unde era nevoie de React 19; a mers local pe o dependență tranzitivă de React 18 și s-a stricat când producția a tras 19. Remediu: o regulă de versiune în AGENTS.md („migrăm de la React 18 la React 19 trimestrul ăsta; codul nou folosește idiomuri de 19; codul vechi mai poate folosi 18, dar se actualizează când e atins”).

**Semnalul soft al migrării între modele, cu dovezile lui.** Instrucțiunile scrise pentru modelul anterior (regulile din AGENTS.md, prompturile din skill-uri, nivelurile de effort) nu se retrag singure. Pentru între 37% și 63% dintre lucrările de inginerie software analizate, un model mai nou cu un singur prompt a depășit nativ tooling-ul puternic ingineresc propus cu circa un an înainte. Nu e al nouălea kill signal; e ce verifici când un codebase verde devine galben după un upgrade de model (Anexa B.9). *Sursa: Salsabil et al., Aug 31, 2026 (arXiv 2609.00468). Atenție: preprint, fără peer review; folosește-l pentru direcție, nu pentru fracție.*

**Exemple de pregătire și restricții de task.** (1) Serviciu de profil de client: aserțiuni/cazuri de eșec relevante rulează fiabil, prezentare actuală, reguli canonice și reviewer calificat. Zero lacune cunoscute, candidat verde; stabilește totuși scope-ul și recuperarea task-ului. (2) Plăți legacy: check-uri lipsă pentru cazuri de eșec (1), documentație veche (0.5), cuplare costisitoare (1), reguli împrăștiate (0.5), cu expertiză și mecanism de aprobare disponibile. Total 3, pregătire galbenă; stabilește verificarea înaintea schimbărilor de comportament. (3) Criptografia custom fără reviewer calificat încalcă evaluabilitatea indiferent de total. (4) API-ul greenfield cu check-uri/deployment neinvestigate e necunoscut, nu automat verde. (5) Tool-ul intern cu check-uri relevante și lacune delimitate de documentație/cuplare (0.5 fiecare) are total 1, posibil pilot cu condițiile task-ului îndeplinite. (6) Un fork customizat de vendor cu efecte upstream necunoscute cere investigație și o decizie despre păstrarea stratului custom. Sunt aplicări ilustrative ale fișei, nu clasificări validate de siguranță; procentele de coverage singure nu decid niciuna.

---

### Capitolul 9 - Lansarea în echipă {#deep-dive-chapter-9}

**Cele două feluri de hook-uri, pe larg: pre-commit versus pre-push.** Folosește verificări rapide la commit și teste sau build-uri mai costisitoare la push pentru feedback rapid. Un manager de hook-uri ajută la instalare, dar nu poate face hook-urile locale inevitabile: Git permite ocoliri și directoare alternative pentru hook-uri. Hook-urile de politică au nevoie și ele de configurație protejată și blocare la eșec. Acceptarea se impune prin verificări obligatorii pe server și review protejat al workflow-ului, cu credențiale care nu le pot ocoli. *Surse: Git githooks reference, GitHub rulesets și Claude Code hooks reference, verificate pe 23 octombrie 2026. Atenție: fiecare repository trebuie să configureze și să verifice aceste protecții; simpla rulare a CI-ului nu e enforcement.*

**Bucla exterioară (outer loop): de la AutoGPT la Ralph Wiggum.** Bucla interioară (inner loop) e bucla în șase faze (Capitolul 4); bucla exterioară o învelește și reinvocă agentul până când o condiție e îndeplinită. În 2023, AutoGPT și BabyAGI învârteau un model în buclă pe baza propriei lui păreri despre progres; nimic din exterior nu nota o iterație, turele amplificau deriva, iar abordarea s-a prăbușit în câteva luni ca mod de a livra software. Renașterea diferă structural: la mijlocul lui 2025, Geoff Huntley a legat un agent într-un while-loop de bash (un singur fișier de prompt, repeți), care s-a răspândit sub numele „Ralph Wiggum”. Fiecare iterație pornește cu context proaspăt, face o unitate de lucru și se termină în fața unor evaluatori pe care modelul nu-i controlează (compilator, teste, diff), cu starea în repository. Numele lui pentru modul de eșec e overbaking: o buclă lăsată să ruleze după ce și-a terminat treaba inventează muncă pe care n-a cerut-o nimeni. *Surse: ghuntley.com/ralph (Jul 2025); HumanLayer, Jan 6, 2026; The Register, Jan 27, 2026; repository-urile AutoGPT și BabyAGI. Atenție: verdictul de prăbușire și contrastul structural sunt interpretarea manualului.*

**Bucla exterioară: valul vendorilor și mecanismele condiției de oprire.** Copilot coding agent de la GitHub a devenit general disponibil pe 25 septembrie 2025 (mediu izolat, draft de pull request); Cursor a livrat Cloud Agents pe 30 octombrie 2025; Jules de la Google a adăugat Scheduled Tasks pe 10 decembrie 2025; un plugin ralph-wiggum a aterizat în repository-ul oficial Claude Code în noiembrie 2025. Până în primăvara lui 2026, Claude Code avea `/loop` (re-rulare la un interval sau în ritm propriu), Routines (agenți cloud pornind după un program sau după un eveniment GitHub), `/goal` (lucrează până când o condiție de finalizare e îndeplinită) și `/autofix-pr` (împinge fix-uri până când CI-ul e verde). După testul din Capitolul 1, capabilitatea a ajuns la convergență, deși ceea ce a ajuns la convergență e un workflow în jurul componentelor principale, nu o componentă principală. `/goal` folosește un model separat ca să evalueze condiția pe baza conversației; Codex Goals permite modelului care execută munca să marcheze un obiectiv persistent drept finalizat. Aceste mecanisme controlează continuarea și bugetele. Niciunul nu înlocuiește verificările de acceptare protejate independent. Plugin-ul ralph-wiggum n-are dovezi controlate, iar README-ul lui numește numărul maxim de iterații drept principala plasă de siguranță - un buget, nu o condiție de oprire. *Surse: GitHub changelog, 2025-09-25; blogurile Cursor și Google; Claude Code release notes, Apr-May 2026; Claude Code "/goal" docs; OpenAI Cookbook, "Using Goals in Codex." Atenție: datele vendorilor se mai schimbă; documentația /goal descrie mecanismul, nu rezultatele.*

**Bucla exterioară: de ce există fiecare linie din contract și cele două extreme.** O condiție de oprire evaluabilă de o mașină, pentru că o buclă fără ea e abandon. Un buget, pentru că o buclă nesupravegheată e clientul ideal al modelului de tarifare per token (Anexa A). Un gate de acceptare impus prin verificări obligatorii protejate și schimbări de politică trecute prin review, pentru că cel mai ieftin mod de a ajunge pe verde e să negociezi cu propriul evaluator, iar o suită verde scrisă de agent e un indiciu, nu o dovadă (Capitolul 5). Un queue și un jurnal de decizii durabile, cu context proaspăt când hand-off-ul sau deriva observată îl justifică. Izolare dimensionată pentru absență, pentru că o sesiune nesupravegheată e locul unde prompt injection nu mai întâlnește niciun sceptic uman (Capitolul 2). Pune în queue unități similare, verificabile independent și recuperabile doar după ce fiecare îndeplinește condițiile task-ului și controalele de rulare nesupravegheată; verdele singur nu ajunge. Huntley rulează bucla brută la circa 10 dolari pe oră; fabrica de software de la StrongDM rulează livrare complet non-interactivă, cu oameni care nici nu scriu, nici nu fac review la cod, și cu scenarii end-to-end ținute în afara codebase-ului, ca un holdout pe care bucla nu-l poate slăbi, la o cheltuială pe care Simon Willison a estimat-o la aproape 20.000 de dolari pe lună per inginer. *Surse: Willison, Feb 7, 2026; Huntley și The Register, ca mai sus. Atenție: cifra de 10 dolari îi aparține lui Huntley, iar cifrele StrongDM sunt auto-descrierea unei singure companii și încadrarea lui Willison, nu audituri.*

**Exemple de bugete de timp pentru angajamentele rolurilor.** În acest calendar, championul rezervă circa trei ore în prima săptămână și cinci în a doua; săptămânile următoare depind de feature-urile pilotului. Rezultatele urmărite sunt un workflow testat, instrucțiuni utile și întreținute, feature-uri livrate și un succesor desemnat. Lead-ul rezervă circa două ore în prima săptămână și trei-cinci ore în fazele următoare. Sunt exemple de planificare din practică; adaptează-le la efortul măsurat și la punctul de pornire al echipei.

**De ce arată așa exemplul de 90 de zile.** Calendarul rezervă timp pentru învățare, un pilot bine delimitat, extindere și responsabilitate operațională. E un exemplu de organizare din practică, nu o curbă exponențială măsurată. Stabilește înaintea pilotului baseline-ul de cycle time, defecte, efort de review și consum; urmărește rezultatele pe tot parcursul lui. Extinde sau schimbă abordarea când rezultatele justifică asta, în loc să aștepți un câștig promis pentru luna a treia.

---

**Kill signals ale buclei exterioare.** Bucla primește kill signals așa cum Capitolul 8 le dă codebase-urilor. Patru sunt de ajuns: același diff aplicat și apoi revertat de la o iterație la alta; buget care arde în timp ce queue-ul nu scade; același eșec apărut a treia oară; orice iterație care a atins gate-ul. Oricare dintre ele înseamnă stop: citești jurnalul, repari cauza, abia apoi relansezi. O buclă repornită pe speranță e o buclă pe care ai încetat s-o mai controlezi. Blocul de review de dimineață din Anexa B.6 conține aceleași patru verificări.

### Anexa A - Pentru manageri {#deep-dive-appendix-a}

**Rutarea pe tier-uri, cele două puncte măsurate.** Pattern-ul „advisor” al Anthropic împerechează un executor mai ieftin cu un model mai puternic, chemat la nevoie. Sonnet cu Opus ca advisor a obținut cu 2,7 puncte mai mult pe SWE-bench Multilingual decât Sonnet singur, la un cost per task cu 11,9% mai mic. Haiku cu un advisor Opus a obținut 41,2% pe BrowseComp față de 19,7% singur, rămânând cu 29% în urma lui Sonnet singur la scor, la un cost per task cu 85% mai mic. Aceste benchmark-uri de vendor sugerează o opțiune de comparat pe task-uri reprezentative, nu o regulă universală de rutare pentru implementare sau research. *Sursa: Anthropic, "The advisor strategy," Apr 9, 2026. Atenție: benchmark-uri ale vendorului pe propriile modele; cifre per task, nu un raport general.*

**Layout cache-first, taxa pe tool-uri și mascarea.** Layout-ul cache-first a tăiat costul de API cu 41% până la 80% pe peste 500 de sesiuni de agent, la trei provideri (Lumer et al., Jan 31, 2026). Cifrele despre definițiile de tool-uri sunt la Capitolul 1, rezultatul despre mascare la Capitolul 6.

**Comparația de cost complet.** Compară munca utilă acceptată și efortul uman în ambele variante, inclusiv investigație, implementare, review, rework și încercări eșuate. Adaugă tooling/infrastructură suplimentare, setup amortizat, întreținere continuă și guvernanță/evaluare recurente. Calculul ipotetic din Anexa A evaluează capacitatea eliberată; nu stabilește economii de bani sau livrare mai rapidă. Înlocuiește ipotezele cu înregistrări înainte să susții o investiție.
