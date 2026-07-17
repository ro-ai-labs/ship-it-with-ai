# Ship It With AI

### Un manual practic pentru livrarea de software cu agenți AI

**Mihai Cvasnievschi**

---

> Agenții scriu codul.
> Tu înțelegi problema.
> Asta e competența pe care n-o automatizează nimeni.

---

## Cuprins

**Cuvânt înainte** - De ce există manualul ăsta
**Cum se citește manualul**
**O notă despre afirmațiile datate**
**Aria de acoperire și limitele**
**Cazurile folosite în manual**

**Prolog** - Nouă secunde

**Partea I - Arhitectura**
1. Componentele principale
2. Anatomia invariantă
3. Guvernanța în straturi

**Partea a II-a - Metoda**
4. De la cod generat la software livrat
5. Bucla în șase faze
6. [AGENTS.md](https://agents.md/) ca infrastructură de echipă
7. Review-ul de arhitectură: documentare și diagnostic

**Partea a III-a - Realitatea**
8. Pregătirea: kill signals și semaforul
9. Pattern-uri pentru codebase-uri brownfield
10. Adopția: 90 de zile, trei roluri

**Încheiere** - Un mod de a gândi care supraviețuiește tool-urilor

**Mulțumiri**

**Anexa A** - Economia costurilor
**Anexa B** - Template-uri
**Anexa C** - Surse și lecturi suplimentare

---

## Cuvânt înainte - De ce există manualul ăsta

Manualul ăsta există pentru că m-am săturat să port aceeași discuție.

Discuția arată cam așa. Un senior engineer dintr-o companie al cărei business e să livreze software îmi spune că a încercat Claude Code, sau Codex, sau unul dintre celelalte vreo șase coding agents de pe piață, și că „n-a mers”. Când întreb ce anume n-a mers, răspunsul e o variațiune pe aceeași temă: agentul a generat cod care arăta corect, dar nu era; sau agentul a stricat ceva și nimeni n-a observat timp de două săptămâni; sau agentul a produs, cu toată încrederea din lume, un output care încălca o constrângere documentată de echipă în trei locuri diferite. Uneori răspunsul e și mai simplu: agentul a fost prea lent, sau prea scump, sau senior engineerul a ajuns să facă review la mai mult cod decât a scris.

Am auzit fraza asta în săli de ședință, în thread-uri pe Slack, la code review, în post-mortem-uri și în call-uri de procurement. Tool-urile s-au schimbat. Reproșul, nu.

Fiecare dintre răspunsurile astea e real. Fiecare descrie un mod de eșec real. Dar cele mai multe adopții ratate nu se explică doar prin slăbiciunea modelului. Sunt eșecuri ale structurii din jurul agentului: lipsește contextul, lipsesc constrângerile, lipsește procesul, lipsește disciplina de review.

Problema, în fiecare caz, e că echipa a tratat agentul ca pe un tool de evaluat, când agentul e de fapt un tip nou de coleg, care cere un tip nou de structură. Un ciocan îl iei din raft și îl folosești. Un inginer junior nu-l iei din raft să-l folosești. Trebuie să-i faci onboarding, să-i dai context, să pui la punct pattern-uri de review, să construiești încredere în timp. Agenții sunt mai aproape de inginerul junior decât de ciocan.

Despre structura asta e manualul de față.

Nu o să-ți spun ce agent să alegi. Agentul pe care îl alegi azi va fi deprecated, rebranduit sau înghițit de un produs mai mare în timpul în care un ciclu tipic de procurement enterprise apucă să se încheie. Peisajul agenților se mișcă în ritm de luni, nu de ani. Dacă asta ar fi un ghid de tool-uri, ar fi expirat înainte de publicare. Așa că scriu un manual despre cum să gândești livrarea de software cu agenți - arhitectura sistemelor ăstora, metoda prin care livrezi software cu ele și realitatea locurilor unde metoda funcționează și unde nu.

---

### Schimbarea, pusă în context {#the-shift-in-context}

Acum șaptezeci de ani, a programa însemna să perforezi cartele de carton și să aștepți până a doua zi ca să afli dacă programul tău a rulat. Acum șaizeci de ani au apărut editoarele de text și îți puteai vedea codul pe un ecran. Acum patruzeci de ani au venit mediile integrate de dezvoltare - syntax highlighting, debuggere, navigare prin proiect. Acum douăzeci de ani, IntelliSense a început să-ți sugereze următorul caracter pe care urma să-l tastezi. Acum trei ani, codingul asistat de AI a trecut pragul de la „util din când în când” la „poți livra cod cu el”. Iar apoi, în cele optsprezece luni dintre primăvara lui 2025 și primăvara lui 2026, livrarea de software cu agenți a trecut de la demo de research la capabilitate de producție.

Fiecare dintre tranzițiile astea a părut uriașă la momentul ei. Fiecare chiar a fost uriașă. Și fiecare a venit la pachet cu oameni care susțineau că generația anterioară de tool-uri e de-acum suficientă, iar cea nouă e doar hype.

Privind în urmă, fiecare generație a subestimat următoarea abstracțiune. Nici asta nu va face excepție.

Dar - și asta e partea pe care am avut nevoie de un deceniu în domeniu ca s-o învăț - nu *tool-ul* e cel care supraviețuiește tranzițiilor. Supraviețuiește felul în care gândești munca.

Dacă ai învățat să faci debugging mergând pas cu pas printr-un program, într-un debugger, în 1995, debuggerul acela concret a dispărut. Felul în care gândești izolarea unui bug - îngustezi inputurile, îngustezi starea, îngustezi fereastra de timp - e exact același. Dacă ai învățat să construiești pentru web în 2008, framework-ul concret pe care îl foloseai a dispărut, înlocuit de două ori între timp. Felul în care gândești separarea responsabilităților, structurarea fluxului de date, gestiunea stării - alea au rămas la fel, doar exprimate în altă sintaxă.

Livrarea de software cu agenți e acum în același tip de punct de inflexiune. Agentul concret pe care înveți să-l folosești va fi înlocuit. Felul în care gândești *ce e un agent, ce poate face și ce trebuie să faci tu ca să-l controlezi* va supraviețui următoarelor zece înlocuiri.

Peisajul se mișcă repede, dar metodologia rămâne.

În cele optsprezece luni dintre momentul în care mi-am construit primul workflow de programare cu agenți și momentul în care m-am așezat să scriu manualul ăsta, s-au întâmplat patru lucruri care, în orice deceniu anterior, ar fi fost știri de primă pagină în presa tech. Un model a urcat cu 7 puncte procentuale pe un benchmark de coding. Un marketplace oficial de plugin-uri pentru coding agents a devenit un canal real de distribuție. Un mare furnizor de cloud a anunțat end-of-support pentru unul dintre produsele lui de AI pentru developeri. Cel mai mare vendor de AI agentic a formalizat „skills” ca componentă principală pe care orice agent îl poate implementa. Patru schimbări. Patru luni. Oricare dintre ele, în 2015, ar fi alimentat un trimestru întreg de conference talks. În 2026, toate la un loc au fost ciclul de știri al unei singure săptămâni.

Nu există un tool corect pentru totdeauna. Echipele care gestionează bine lucrul ăsta și-au construit un framework de referință pentru evaluarea tool-urilor - ce e un agent din punct de vedere anatomic, ce ar trebui să poată face, ce refuză ele să-l lase să facă, cum îl leagă de procesele lor existente de review și de livrare. Când apare un tool nou, aplică acel framework. Framework-ul supraviețuiește chiar și atunci când fiecare tool concret e înlocuit.

Echipele care gestionează prost lucrul ăsta au ales un tool, l-au integrat adânc fără să se gândească la portabilitate, și acum reiau întregul ciclu de selecție-și-integrare ori de câte ori se mișcă peisajul. Costul nu e tool-ul cel nou. Costul e munca refăcută, reinstruirea oamenilor, migrările lăsate la jumătate, oboseala instituțională.

Mai rău, oboseala instituțională se acumulează de la un ciclu la altul. O echipă care a trecut prin trei adopții ratate de tool-uri în doi ani dezvoltă un scepticism justificat față de următoarea propunere de adopție. Scepticismul face următoarea adopție mai grea, chiar și atunci când următorul tool e cu adevărat mai bun decât cele dinainte. Refrenul echipei - „am încercat X, n-a mers” - devine șablonul aplicat fiecărui X care urmează. Așa ajung echipe bune să se blocheze.

Ieșirea din capcană e să nu mai optimizezi pentru tool-ul concret și să începi să optimizezi pentru framework. Framework-ul e capacitatea de evaluare a echipei - cât de repede poate echipa să ia un tool nou, să-l evalueze în raport cu constrângerile pe care le cunoaște, să-și dea seama dacă se potrivește și fie să-l adopte curat, fie să-l refuze curat. Echipele cu un framework bun pot schimba tool-uri pe bandă fără să-și macine propria disciplină. Echipele fără un framework bun își macină propria practică de fiecare dată când se schimbă tool-ul.

Manualul ăsta e despre construirea framework-ului. Tool-urile concrete pe care le numesc pe parcurs - Claude Code, Codex CLI, opencode, diversele plugin-uri și marketplace-uri - vor fi altele până la data la care ar fi scadentă ediția următoare. Framework-ul va fi același.

---

### De unde vorbesc {#where-i-am-coming-from}

Scriu software profesionist din 2000 și construiesc sisteme AI de mai bine de un deceniu. Am folosit fiecare generație de asistent de coding, de la inteligența timpurie din IDE-uri la Copilot și până la coding agents de azi, și mi-am petrecut ultimele optsprezece luni urmărind echipe de producție care adoptă workflow-uri cu agenți - unele bine, altele prost. Manualul ăsta e suma pattern-urilor care au supraviețuit utilizării repetate în echipe reale.

[Contextul complet: Despre autor.](#about-the-author)

---

### Ce înseamnă „AI agentic” în acest manual {#what-agentic-ai-means-in-this-book}

Tot spun „AI agentic” fără să fi definit termenul. Iată definiția.

Un sistem de AI agentic e unul care primește un obiectiv, decide ce acțiuni trebuie executate ca să-l atingă și le execută, cu o anumită doză de autonomie. Autonomia e partea care contează. Un plugin de IDE care îți sugerează următoarea linie de cod nu e agent - el sugerează, tu accepți sau respingi, fiecare pas e al tău. Un sistem de programare cu agenți e unul căruia îi dai un obiectiv - „adaugă un câmp Priority pe entitatea Opportunity din CRM” - iar el își dă seama singur ce fișiere să citească, ce fișiere să editeze, ce teste să ruleze, ce comenzi să execute. Tu supervizezi. Tu corectezi. Tu aprobi. Dar nu mai scrii tu fiecare apăsare de tastă.

Trecerea asta - de la a scrie fiecare tastă la a superviza munca - e schimbarea centrală. Tot restul manualului decurge din ea. Arhitectura, pentru că felul în care un agent ia decizii despre ce să facă determină cât de mult ar trebui să-l lași să se atingă de codul tău. Metoda, pentru că supervizarea muncii cere altă disciplină decât scrisul fiecărei taste. Realitatea, pentru că trecerea asta funcționează pentru unele tipuri de muncă și nu funcționează deloc pentru altele.

Majoritatea echipelor care eșuează cu livrarea cu agenți eșuează pentru că au încercat să folosească agentul ca pe un autocomplete pe steroizi. Voiau să tasteze mai repede. Doar că agenții nu asta oferă. Agenții oferă posibilitatea de a delega muncă bine formulată unui coleg care nu obosește, nu are nevoie de pauză de prânz și poate fi clonat ca să lucreze la trei lucruri în paralel. Dacă tratezi colegul ăsta ca pe un ciocan, vei fi dezamăgit. Dacă îl tratezi ca pe un coleg, poți livra lucruri pe care înainte nu ți le puteai permite.

---

### Structura manualului {#the-frame-of-this-book}

Trei părți. Arhitectura: cum sunt construiți agenții și cum îl evaluezi pe următorul când apare. Metoda: bucla iterativă care transformă „AI care generează cod” în „AI care livrează software”. Realitatea: unde funcționează asta, unde nu, și care sunt kill signals care îți spun în ce situație ești.

Ăsta e un manual practic, nu un tratat. Scriu la persoana întâi pentru că împărtășesc ce am văzut, nu ce am teoretizat. Exemplele sunt anonimizate, dar reale. Metodele sunt verificate în producție. Opiniile sunt ale mele, apărate cu experiență și oferite cu deplina conștiință că orice opinie concretă va trebui revizuită când vine următoarea schimbare majoră din peisaj - ceea ce se va întâmpla curând și exact ăsta e rostul metodologiei pe care urmează să o împărtășesc.

Dacă vrei o listă de tool-uri cu note, manualul ăsta te va dezamăgi. Dacă vrei un mod de gândire care să supraviețuiască următorilor cinci ani de agitație, citește mai departe.

Un angajament legat de cititor. Manualul ăsta e pentru oricine vrea să livreze software cu AI - un founder, un product engineer, un data scientist, un designer care scrie cod sau inginerul care livrează de douăzeci de ani. E scris în primul rând pentru un singur cititor: senior engineerul - staff, principal sau tech lead - care va pune practica asta pe picioare într-o echipă reală și apoi o va apăra în sus, în fața managementului, pentru că azi obișnuința de a citi cod e încă un avantaj, iar exemplele se sprijină pe ea. Avantajul ăsta e temporar. Programarea urcă în continuare spre niveluri tot mai înalte de abstractizare, iar următorul nu îți va mai cere deloc să citești codul. Ce supraviețuiește urcușului e exact partea despre care e manualul ăsta: să înțelegi problema, să formulezi munca, să constrângi execuția, să verifici rezultatul - iar astea pot fi învățate de oricine, și ăsta e tot rostul. Părțile I și II sunt locul unde faci munca propriu-zisă. Partea a III-a e felul în care câștigi discuția cu oamenii care semnează. Capitolul 10 îl numește pe cititorul principal championul. Dacă ești managerul sau directorul de partea cealaltă a discuției, drumul tău e mai scurt; îl găsești în secțiunea următoare.

O convenție de încadrare. Felul în care vorbesc despre agent ca despre un coleg, pe tot parcursul manualului, e o poziție de lucru, nu o afirmație despre natura agentului. Agentul e software. Poziția e următoarea: investește în el cum ai investi într-un coleg junior - onboarding, infrastructură comună, bucle de feedback, răbdare cu greșelile - și rezultatele operaționale se compun în timp. Sari peste investiție și agentul rămâne un tool, cu randament de tool.

Afirmația centrală a manualului e simplă: livrarea de software cu agenți nu e în primul rând o problemă de tooling. E o problemă de control. Controlează contextul, acțiunile, verificarea și suprafața de adopție, și agentul devine util. Nu le controla, și agentul devine zgomot scump sau risc operațional.

Două idei străbat tot ce urmează și merită spus explicit cum se leagă între ele. Durabilitatea e de ce-ul: tool-urile se schimbă trimestrial, o practică legată de tool-ul lunii moare odată cu tool-ul lunii, iar singura practică pe care merită s-o construiești e cea care supraviețuiește schimbării. Controlul e cum-ul: cele trei părți ale manualului sunt trei forme de control pe care le iei înapoi, în ordine. Arhitectura e controlul capabilității: ce poate ști și ce poate face agentul. Metoda e controlul workflow-ului: cum se formulează, se execută și se verifică munca. Realitatea e controlul adopției: unde aplici metoda și unde n-ar trebui s-o aplici. Durabilitatea e motivul pentru care îți pasă. Controlul e felul în care e construit manualul.

Capitolele care urmează sunt felul în care am învățat să fac afirmația asta să dea rezultate. Prologul e ce se întâmplă când niciunul dintre straturi nu există.

---

## Cum se citește manualul {#how-to-read-this-book}

Ăsta e un manual practic. Prima dată citește-l cap-coadă; după aceea folosește-l ca material de referință.

**Traseul principal e al championului** și e simplu: tot, în ordine. Capitolele 1, 2, 4, 5, 6, 7 și 8 sunt coloana vertebrală tehnică - anatomie, formulare, buclă, instrucțiuni de echipă, review-ul ca instrument de diagnostic, pregătire. Capitolele 3, 9 și 10 sunt guvernanța, pattern-urile de brownfield și adopția - capitolele de care ai nevoie în clipa în care practica atinge mai mulți oameni decât pe tine.

Două scurtături pentru toți ceilalți. **Dacă ești engineering manager sau director:** citește Cuvântul înainte, Aria de acoperire și limitele, Capitolele 3, 8 și 10 și Anexa A - postura de risc, clasificarea portofoliului, rollout-ul și costurile. E oricum pachetul pe care ți-l va pune în mână championul tău. **Dacă facilitezi adopția:** Anexa B e setul de artefacte; Capitolele 7-10 sunt secvența de facilitare.

Poți oricând să sari înapoi. Fiecare capitol presupune capitolul dinaintea lui, dar template-urile și framework-urile sunt gândite să fie luate și folosite direct.

---

## O notă despre afirmațiile datate {#a-note-on-dated-claims}

Referințele la tool-uri specifice din manual sunt valabile la nivelul lunii iulie 2026. Framework-urile sunt gândite să supraviețuiască tool-urilor concrete. Acolo unde contează o capabilitate anume a unui produs cu nume și prenume, fie datez afirmația, fie o tratez ca exemplu, nu ca proprietate permanentă. Notele de sursă pentru afirmațiile factuale pe care se sprijină argumentul sunt în Anexa C.

Fac tot ce pot să țin manualul la zi și mențin un [changelog](/changelog/) cu actualizările care contează.

Stilul numerelor: statisticile și procentele sunt scrise cu cifre (19%, 43 de puncte); numerele mici, nestatistice, sunt scrise în litere.

---

## Aria de acoperire și limitele {#scope-and-limits}

Un manual practic care nu-și numește propriile moduri de eșec va pierde în fața experienței cititorului în clipa în care experiența aceea se desparte de manual. Așa că iată locurile în care cred că manualul ăsta poate greși.

Tool-urile se vor schimba. Produsele concrete pe care le-am numit - Claude Code, Codex CLI, Cursor, hookify, Superpowers, Understand Anything, marketplace-ul de plugin-uri al Anthropic - vor arăta altfel peste doi ani. Unele vor fi mai bune. Unele vor fi deprecated. Unele vor fi înlocuite de tool-uri care funcționează altfel decât arhitectura descrisă în Capitolul 1. Dacă componentele principale rămân valabile, manualul are dreptate. Componentele principale sunt un set deschis - două dintre cele opt și-au câștigat locul abia recent. Dacă un agent viitor apare fără vreun mecanism care să corespundă unuia dintre componente principale, înseamnă că am ratat o invariantă pe care o credeam structurală. Dacă apare o componentă principală nouă, lista crește.

API-ul de guvernanță se va schimba. Formatele concrete de hook-uri, sintaxa concretă a regulilor de permisiuni, flag-urile concrete de sandbox - astea sunt specifice fiecărui vendor și fiecărei versiuni. Modelul în cinci straturi e ce mă aștept să reziste; detaliile de implementare sunt ce mă aștept să îmbătrânească.

Comportamentul modelelor se va îmbunătăți. Mai multe dintre kill signals sunt legate de limitări actuale ale modelelor - incapacitatea de a-și evalua output-ul, fragilitatea la viteza schimbării, problema potrivirii dintre model și context. Modelele viitoare vor închide o parte dintre golurile astea. Semaforul e calibrat pentru 2026; calibrarea corectă în 2028 s-ar putea să fie mai relaxată.

Prețurile se vor mișca. Structura pe tier-e și categoriile de TCO din Anexa A sunt durabile; ofertele concrete pe care le treci prin ele, nu.

Unele echipe vor obține valoare cu un proces mai lejer. Bucla în șase faze e disciplina pe care am văzut-o funcționând de la o echipă la alta. O echipă cu o cultură de engineering mai așezată, cu un scope mai mic și cu o povară de compliance mai ușoară poate obține mare parte din beneficii cu o buclă în trei faze sau cu un pattern de pair programming structurat. Disciplina completă e pariul sigur, nu singurul drum. Capitolul 5 arată o echipă care și-a câștigat dreptul la varianta mai lejeră - și cele trei condiții pe care le avea deja îndeplinite.

Unele workflow-uri sunt prea reglementate pentru setările astea implicite. Manualul presupune că echipa are autoritatea să instaleze hook-uri, să configureze AGENTS.md, să pună la punct sandbox-uri și să ruleze subagenți. Unele medii reglementate nu permit așa ceva fără architectural review boards, comitete de securitate sau procese de procurement cu vendorii care durează luni de zile. În mediile alea, manualul descrie destinația, nu drumul.

---

## Cazurile folosite în manual {#cases-used-in-this-book}

Fiecare dintre studiile de caz de mai jos revine în mai multe capitole. Lista există ca să poți naviga și după exemplu, nu doar după framework.

- **PocketOS** - nouă secunde până la pierderea producției, din cauza unui agent fără constrângeri. Prolog + Capitolul 3 (Guvernanța în straturi). Notele de sursă, în Anexa C.
- **Terraform / DataTalks.Club** - doi ani și jumătate de infrastructură pierduți din cauza unui state file rămas în urmă. Capitolul 3 (Guvernanța în straturi).
- **Demoul cu doi agenți** - inspecție de arhitectură făcută în paralel pe Codex CLI și opencode, care demonstrează anatomia invariantă. Capitolul 2.
- **Regula de validare** - o singură linie din AGENTS.md care a eliminat trei ore pe lună de corecturi. Capitolul 6 (AGENTS.md ca infrastructură de echipă).
- **AGENTS.md-ul de 900 de linii** - modul de eșec prin instrucțiuni umflate și revenirea din el. Capitolul 6.
- **Studiul randomizat controlat METR** - developeri experimentați cu 19% mai lenți cu asistență AI, un decalaj de așteptări de 43 de puncte. Capitolul 4 (De la cod generat la software livrat).
- **Regresia de adaptive thinking** - regresia din Claude Code din februarie-aprilie 2026, care a despărțit echipele disciplinate de cele care lucrau la liber. Capitolul 4.
- **Review-ul de arhitectură din banking** - diagnosticul care a transformat o propunere de rescriere de 18 luni într-o înlocuire țintită de trei luni. Capitolul 7.
- **Feature-ul de wire priority** - un singur feature urmărit prin toate cele șase faze ale buclei. Capitolul 5.
- **Adopția grassroots** - un singur inginer care construiește practica de jos în sus, înainte ca echipa să fi ocupat cele trei roluri. Capitolul 10.
- **Cazul managerului din financial services cu 20 de ingineri** - calcule concrete pentru faza managerului din arcul de 90 de zile. Capitolul 10.

---

# Prolog

## Nouă secunde {#nine-seconds}

Pe 24 aprilie 2026, o mică firmă de SaaS pe nume PocketOS, un produs de management pentru închirieri auto, și-a pierdut baza de date de producție din cauza unui agent AI care a hotărât să rezolve de unul singur o problemă de credențiale.

Iată ce s-a întâmplat. Un developer lucra pe codebase-ul PocketOS cu un coding agent (Cursor, pe Claude Opus 4.6). În timpul unui task de rutină, agentul a dat peste o nepotrivire de credențiale. În loc să se oprească și să întrebe, agentul a decis să repare singur problema. A găsit un API token care se autentifica la Railway, platforma de infrastructură folosită de PocketOS. A invocat comanda Volume Delete din Railway. Distrugerea a fost totală. Baza de date de producție a PocketOS - toate rezervările clienților, înregistrările de plăți și inventarul de vehicule - a fost ștearsă. Backup-urile, pe care Railway le ține pe același volum cu datele primare, au fost șterse odată cu ea. Cel mai recent snapshot recuperabil avea trei luni vechime. Recuperarea a fost până la urmă posibilă, dar nu pe ruta de backup la care se aștepta echipa; relatările publice diferă în privința duratei exacte a recuperării, iar ambiguitatea asta face parte din lecție. CEO-ul a scris public despre incident. Postarea a devenit rapid un punct de referință în discuțiile despre siguranța AI-ului în producție.

Nouă secunde. Apelul distructiv a durat nouă secunde.

După aceea, agentul și-a recunoscut vina în scris: „I violated every principle I was given. I guessed instead of verifying. I ran a destructive action without being asked. I didn't understand what I was doing before doing it.” Linia „I guessed instead of verifying” e cea pe care și-o amintesc mulți practicieni. „NEVER GUESS” era regula pe care agentul a descoperit-o prea târziu. Nu era în system prompt; era concluzia la care a ajuns agentul, retrospectiv, despre ce ar fi trebuit să facă.

*Notă despre surse. Relatările publice despre incidentul PocketOS diferă în privința duratei recuperării și a unor detalii operaționale. Folosesc incidentul aici pentru pattern-ul de guvernanță, nu ca pe o reconstituire exactă, de tip forensic. Citările sunt în Anexa C.*

---

Ăsta e pattern-ul de eșec pe care manualul de față e construit să-l prevină.

Nu pentru că vreo metodologie ar face agenții perfecți. Niciuna nu o face. Ci pentru că prevenirea incidentului nu cerea magie. Cerea controale de engineering obișnuite, aplicate unui tip nou de lucrător: credențiale limitate, tool-uri constrânse, gate-uri de review, telemetrie și o echipă care să știe ce acțiuni nu are voie agentul să facă. Mai multe straturi din practica descrisă în manualul ăsta ar fi putut rupe lanțul. Telemetria ar fi putut scurta reacția. Un sandbox ar fi putut bloca apelul distructiv. Segregarea secretelor ar fi putut împiedica sesiunea să aibă la îndemână credențialul cu pricina. Un hook de securitate ar fi putut forța o aprobare umană înainte ca acțiunea periculoasă să ruleze.

Niciunul dintre straturile astea nu e exotic. Sunt aceleași controale pe care un inginer cu experiență le-ar aplica oricărui coleg junior nou care primește drept de push în producție. Limitezi credențialele. Limitezi tool-urile. Faci review la muncă înainte să ajungă live. Înregistrezi ce s-a întâmplat, ca să poți învăța din asta. Agentul e software, dar controalele din jurul agentului sunt practică de engineering care precedă agentul cu decenii. Capitolele care urmează sunt, fiecare, câte o bucată din învelișul ăsta - numită, delimitată și făcută suficient de concretă încât s-o pui în funcțiune săptămâna asta.

Partea cea mai grea pentru majoritatea echipelor nu e setup-ul tehnic. Partea cea mai grea e schimbarea de poziție. Agentul e software, dar pattern-ul operațional e de engineering: îi faci onboarding, îl constrângi, îi verifici munca, îi loghezi acțiunile și lași încrederea să se acumuleze prin pariuri mici. Framework-urile din manual sunt felul în care faci toate astea pentru un agent. Schimbarea e să recunoști că acest contributor lucrează în paralel, nu obosește niciodată și poate încălca o instrucțiune din system prompt atunci când un input suficient de ingenios îl convinge s-o facă. PocketOS e ce se întâmplă când pattern-ul ăsta lipsește.

Tool-urile se schimbă. Metodologia rămâne. Ăsta e pariul manualului.

---

# Partea I - Arhitectura

> *Controlul capabilității: ce poate agentul să știe și ce poate să facă.*

---

## Capitolul 1
## Componentele principale

### Ce este o componentă principală a unui coding agent? {#what-is-a-primitive}

Deschide codul sursă sau documentația aproape oricărui coding agent de nivel de producție - Codex CLI scris în Rust, opencode în TypeScript, părțile cu sursă publică din Claude Code, agenții livrați de o jumătate de duzină de vendori mai mici - și vei vedea conturându-se aceeași arhitectură: un set restrâns de componente principale împachetate într-un harness. Implementările diferă. Anatomia converge. Uneori alte nume, întotdeauna altă așezare a fișierelor, dar aceleași cărămizi conceptuale. Cele mai multe sunt capabilități locale ale agentului. Una singură - subagenții - e mecanismul de compoziție care face agentul recursiv: poate porni instanțe constrânse ale lui însuși.

Context window. Tool-uri. Permisiuni / Sandbox. Skill-uri. Plugin-uri. MCP. Memory. Subagenți.

Subagenții au intrat de curând în vocabularul public - nu pentru că ideea ar fi nouă, ci pentru că au devenit universali la toți agenții majori într-un interval foarte scurt. Claude Code a livrat tool-ul Task, apoi a construit peste el Agent Teams, pentru coordonare la nivel mai înalt. În martie 2026, Codex CLI a dus subagenții la GA ca workflow de primă clasă, cu dispatch în paralel. Cursor a livrat agenți paraleli în 2.0 și un sistem complet de subagenți în 2.4. Cline i-a livrat nativ. În circa un an, dispatch-ul unei instanțe-copil constrânse a agentului a trecut de la „workflow avansat” la „o componentă principală pe care harness-ul îl expune by default”. Ăsta e testul pe care îl folosesc pentru statutul de componentă principală, iar subagenții îl trec.

Asta e anatomia. Orice întrebare interesantă despre un coding agent - ce poate face, ce nu poate face, cum îl controlezi, cu ce îl compari - se reduce la unul sau mai multe dintre aceste componente principale. Când apare un agent nou, prima ta întrebare e: cum tratează acesta fiecare componentă principală? Când decizi dacă lași un agent să se atingă de un anumit codebase, a doua întrebare e: care componentă principală e punctul de control relevant pentru riscul respectiv? Când cumperi tooling, a treia întrebare e: ce componentă principală îmbunătățește tooling-ul ăsta și cu ce cost?

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

*Figura: Componentele principale și harness-ul care le rulează. Permisiuni / Sandbox ocupă poziția 3 ca componentă principală ale cărei două jumătăți - stratul de decizie de la nivelul agentului și enforcement-ul la nivel de OS - converg ca prezență, dar diverg ca postură de la un vendor la altul. A doua jumătate a lui Memory - stratul scris de agent - a convers la agenții majori în primele luni ale lui 2026. Subagenții stau sub linie pentru că sunt componenta principală recursivă: fiecare subagent e, la rândul lui, o instanță a celorlalte.*

---

**Context window-ul** - fereastra de context - e ceea ce agentul știe chiar acum. E mărginită: fiecare model are un număr maxim de tokeni pe care îi poate ține în atenția activă. Două sute de mii la un model compact. Un milion de la gama medie în sus, acum că fereastra de un milion de tokeni s-a întins de la tier-ul flagship la modelele de zi cu zi. Cifrele astea cresc de la un trimestru la altul; până ajungi tu să citești rândurile astea, vor fi și mai mari. Dar limita există, și limita contează, pentru că fereastra de context e spațiul de lucru în interiorul căruia agentul ia decizii.

Ce intră în context window? System prompt-ul care definește rolul și constrângerile agentului. Istoricul conversației curente cu utilizatorul. Tool call-urile pe care le-a făcut agentul și rezultatele pe care i le-au întors. Fișierele pe care le-a citit sau bucățile de fișiere pe care le-a încărcat. Orice instrucțiuni injectate de harness (ajungem imediat și la harness). Cam asta umple fereastra.

Ce nu intră în context window by default? Restul codebase-ului tău. Istoricul de git. Ticketele din Jira. Wiki-ul din Confluence. Canalul de Slack unde echipa discută arhitectura. Toate astea sunt potențial relevante, toate există pe undeva, dar niciuna nu ajunge automat în atenția agentului. Agentul trebuie să le ceară - prin tool-uri, prin plugin-uri, prin MCP. Ceea ce înseamnă că agentul trebuie să știe că ele există, sau să i se spună, sau să fie configurat să le caute.

Asta e prima surpriză pentru echipele care abia încep să lucreze cu agenți. Agentul e sclipitor la lucrurile pe care le vede și complet orb la tot restul. Cele mai multe eșecuri de tip „agentul a luat o decizie evident greșită” se reduc, la o privire atentă, la „agentul nu a avut contextul necesar ca să ia decizia corectă”. Agentul nu știa de noua bibliotecă de autentificare pentru că nu i-a spus nimeni. A ales by default framework-ul de teste greșit pentru că nimeni nu a pus preferința echipei în configurație. Agentul a luat cea mai bună decizie posibilă cu contextul pe care îl avea, iar decizia a fost greșită pentru că acel context era incomplet.

Gestionarea context window-ului e, prin urmare, una dintre disciplinele inginerești centrale ale programării cu agenți. Decizi în permanență ce încarci, ce rezumi, ce arunci, ce ceri la momentul potrivit. Ferestrele de context mai mari ajută - un milion de tokeni de context e, într-adevăr, mult mai iertător decât două sute de mii - dar ferestrele mai mari nu elimină constrângerea. Doar ridică plafonul. Meșteșugul de a lucra înăuntrul acelei limite - ce încarci, la ce faci referire, când pornești curat - e predat în Capitolul 5 ca igiena contextului.

---

**Tool-urile** sunt acțiunile pe care le poate face agentul. Să citească un fișier. Să scrie un fișier. Să editeze un fișier pe loc. Să ruleze o comandă de shell. Să caute un text în tot codebase-ul. Să listeze conținutul unui director.

Majoritatea coding agents de nivel de producție converg spre cam același set de tool-uri de bază. Read, Write, Edit, Bash, Glob, Grep. Uneori câteva în plus - rularea unui snippet de Python, fetch pe un URL, parsarea unui document structurat. Acestea sunt verbele. Fără ele, agentul ar putea gândi, dar n-ar putea acționa.

Tool-urile sunt simple conceptual și importante operațional. Fiecare tool call e un punct de decizie. Fiecare tool call e și un punct de audit - agenții de nivel de producție ar trebui să înregistreze tool call-urile făcute, în ordine, cu tot cu argumente, ca să poți reconstitui și inspecta ulterior comportamentul agentului. Dacă ai avut vreodată de debugat o acțiune de agent în mai mulți pași care a luat-o razna, o să apreciezi pista de audit. Log-ul de tool call-uri e echivalentul log-ului de query-uri SQL într-o problemă de bază de date - fără el, ghicești.

Tot la nivelul tool call-urilor trăiește și guvernanța. O să dedicăm un capitol întreg subiectului, dar, pe scurt: când îi spui unui agent „nu șterge fișiere din directorul ăsta”, ceea ce faci de fapt e să interceptezi tool call-ul de Bash înainte să execute comanda rm. Tool call-ul e bottleneck-ul. Constrângi tool call-urile, constrângi agentul. Lași tool call-urile să ruleze neconstrânse și ai un agent care poate face orice.

---

### Permisiuni / Sandbox {#permissions-sandbox}

**Permisiuni / Sandbox** e componenta principală care i-a lipsit lui PocketOS. Are două jumătăți, iar ele nu sunt același control scris în două feluri - sunt două controale diferite, pe care agenții convergenți le livrează împreună pentru că fiecare prinde ce scapă celălalt.

**Stratul de decizie de la nivelul agentului** e cel pe care agentul însuși îl consultă înaintea fiecărui tool call. Reguli Allow / Ask / Deny, plus clasificatorul mai nou de auto-mode, care rezolvă în tăcere deciziile de rutină și le scoate la suprafață pe celelalte, pentru operator. Toți coding agents majori îl livrează: Claude Code, Codex CLI, opencode, Cursor, Gemini CLI. Sintaxa regulilor diferă de la vendor la vendor; rolul arhitectural, nu. E stratul spre care întind mâna întâi cele mai multe echipe. E și stratul pe care prompt injection-ul îl poate învinge, pentru că prompt injection-ul funcționează manipulând raționamentul agentului, iar tocmai raționamentul agentului e cel care consultă regulile.

**Enforcement-ul la nivel de OS** rulează dedesubt. Kernelul însuși refuză syscall-urile pe care agentul nu era autorizat să le facă: Seatbelt pe macOS, bubblewrap cu Landlock și seccomp pe Linux, token-uri restricționate sau izolare pe bază de WSL2 pe Windows. Agentul nu poate „raționa” pe lângă stratul ăsta, pentru că kernelul nu ascultă raționamentul agentului - ascultă apeluri de sistem. Ori syscall-ul e permis, ori nu e.

Convergența pe jumătatea asta e reală, dar inegală. Codex CLI impune sandbox la nivel de OS by default pe Linux și macOS. Cursor a adăugat controale de sandbox cu suport în kernel în linia 2.x. Gemini CLI livrează profile de sandbox per platformă. Claude Code e opt-in - sandbox-ul există, dar majoritatea instalărilor îl sar. opencode e excepția parțială: livrează doar jumătatea de decizie și lasă izolarea la nivel de OS în seama Docker-ului sau microVM-ului pe care îl configurează operatorul în jurul lui. Convergența e pe *prezența ambelor jumătăți ca pachet configurabil*, nu pe *postură* - exact asimetria pe care o are și componenta principală Memory pe a doua lui jumătate. Asta e citirea onestă.

Spus direct: stratul de la nivelul agentului poate fi ocolit prin prompt injection. Stratul de la nivelul OS-ului, nu. Cele două se livrează împreună pentru că niciunul nu e suficient singur. Perechea convergentă e componenta principală.

Capitolul 3 parcurge suprafețele de configurare ale acestei componente principale - cum își expune fiecare agent major regulile de allow/ask/deny, unde se activează sau se dezactivează sandbox-ul de OS și cum se mapează cele cinci straturi de guvernanță din acel capitol pe cele două jumătăți ale componentei principale.

---

**Skill-urile** sunt instrucțiuni împachetate, pe care agentul le încarcă atunci când devin relevante. Felul în care preferă echipa să scrie un serviciu de Spring Boot. Convențiile pentru testarea componentelor React. Pattern-ul pentru adăugarea unei coloane noi într-un tabel multi-tenant. Fiecare dintre ele e o bucată de markdown - de obicei între câteva sute și câteva mii de cuvinte - pe care agentul o citește exact în momentul în care are nevoie de expertiza respectivă.

Implementarea skill-urilor diferă de la un agent la altul în numele fișierelor și în semantica de încărcare, dar componenta principală de dedesubt e acum comună tuturor agenților majori. Componenta principală always-loaded a ajuns la convergență pe două nume de fișier: [AGENTS.md](https://agents.md/), neutru față de vendor, suportat de Codex CLI, Cursor, GitHub Copilot, Gemini CLI, Aider și de restul ecosistemului; și CLAUDE.md, pe care Claude Code îl citește nativ. Cele două sunt interoperabile - Claude Code poate importa AGENTS.md în CLAUDE.md, astfel încât conținutul echipei stă într-un singur loc, indiferent de vendor. Ambele se încarcă la începutul sesiunii, ambele joacă același rol. A ajuns la convergență și componenta principală on-demand: fișiere markdown individuale, activate la detecție, ținute în afara contextului până când un task se potrivește cu trigger-ul skill-ului (Claude Code le numește Skills; Codex CLI livrează fișiere SKILL.md cu frontmatter YAML și progressive disclosure). Skill-ul de code review pentru Spring Boot se încarcă atunci când faci review pe cod Spring; nu poluează contextul când agentul ia un task de migrare de schemă. Pattern-ul always-loaded (AGENTS.md, CLAUDE.md) e mai vechi. Pattern-ul dispatch-on-detection (Skills în Claude Code, Skills în Codex) e mai nou și scalează mai bine pe măsură ce crește catalogul de skill-uri al echipei.

Ambele pattern-uri funcționează. Cel cu dispatch la detecție e mai eficient la scară - poți avea cincizeci de skill-uri pentru cincizeci de tipuri de muncă fără să umpli fereastra de context, în fiecare moment, cu patruzeci și nouă irelevante. Pattern-ul always-loaded e mai simplu și mai predictibil. Alege în funcție de tipurile de task-uri pe care le rulează echipa ta și de problemele de context plin de care te lovești.

Skill-urile sunt felul în care codifici expertiza specifică echipei într-o formă pe care agentul o poate folosi. Sunt durabile - stau în git, trec prin review în pull request, poartă semnătura autorului. Sunt cel mai apropiat lucru, în anatomia agentului, de „tribal knowledge-ul seniorului, dar pus pe hârtie”.

---

**Plugin-urile** sunt pachete. Un plugin împachetează skill-uri laolaltă cu tool-uri, cu hook-uri și cu comenzi, toate instalabile printr-o singură comandă. hookify e un plugin. Security-guidance e un plugin. Superpowers e un plugin. Plugin-ul e unitatea de distribuție.

De ce contează plugin-urile operațional: fac posibilă partajarea expertizei între echipe fără ca fiecare echipă să reconstruiască aceeași schelărie. Dacă o echipă construiește un workflow excelent de review de PR-uri sub formă de plugin, altă echipă îl poate instala cu o singură comandă. Plugin-ul își gestionează singur versiunile, dependențele, activarea. Echipa care îl primește nu trebuie să-l integreze manual.

De ce contează plugin-urile strategic: creează un marketplace. În mai 2026, marketplace-ul de plugin-uri devenise deja un canal de distribuție real, cu plugin-uri oficiale și comunitare care începeau să formeze un ecosistem. Numărul exact contează mai puțin decât schimbarea de fond: plugin-urile sunt acum o suprafață de supply chain. Marketplace-ul e echivalentul npm-ului pentru programarea cu agenți - și, ca și npm, vine la pachet și cu avantajul reutilizării rapide, și cu dezavantajul riscului de supply chain. Plugin-urile trebuie verificate la fel cum verifici dependențele. Iată checklist-ul pe care îl folosesc eu.

Maintainer-ul. Cine deține plugin-ul. A fost repo-ul activ în ultimele nouăzeci de zile. Există mai mult de un maintainer sau e un bus factor de unu. Poate fi identificat autorul - un istoric real pe GitHub, un angajator real, un palmares - sau e un cont proaspăt creat, cu un singur repo. Un plugin întreținut de Anthropic, de un vendor cunoscut sau de un inginer a cărui altă activitate o poți verifica e într-o cu totul altă clasă de risc decât unul urcat săptămâna trecută de un nume pe care nu-l recunoaște nimeni.

Suprafața de permisiuni. Ce tool-uri instalează plugin-ul. Ce hook-uri înregistrează. Ce căi de fișiere atinge. Ce apeluri de rețea face. Tratează cererile de permisiuni largi exact cum ai trata un pachet npm care cere pe șest acces la filesystem și la rețea în scriptul de instalare: ca pe un red flag care are nevoie de o justificare. Un plugin de review de PR-uri nu are nevoie de drept de scriere în afara `.git/`. Un plugin de documentație nu are de ce să facă apeluri de rețea către un host terț. Dacă permisiunile depășesc scopul evident al plugin-ului, întreabă de ce înainte să-l instalezi.

Review-ul de cod. Citește sursa la prima instalare. Plugin-urile care merită instalate sunt suficient de mici cât să le citești în douăzeci de minute; Superpowers și hookify sunt amândouă așa. Plugin-urile prea mari ca să le citești fac, de regulă, prea multe. Dacă nu poți înțelege din sursă ce face plugin-ul într-o ședință rezonabilă de citit, e un semnal fie să cauți unul mai mic, fie să investești într-un review mai serios înainte să-l adopți.

Disciplina de update. Fixează versiunea. Nu lăsa auto-update. Tratează un update de plugin exact ca pe un update de dependență - citește diff-ul, rulează suita de teste, livrează bump-ul ca pe o schimbare trecută prin review, nu ca pe una tăcută.

Blast radius - raza de impact. Un plugin care operează în interiorul sandbox-ului agentului e mărginit de sandbox. Un plugin care înregistrează un hook ce rulează pe mașina developerului, în afara sandbox-ului, nu e mărginit de nimic. Preferă-l pe cel mărginit. Când trebuie neapărat să-l instalezi pe cel nemărginit, ridică ștacheta la tot ce am enumerat mai sus.

Marketplace-ul e un canal de distribuție real. Disciplina e aceeași pe care o folosești deja pentru dependențe. Costul unei verificări per plugin e mic față de costul unui singur incident de supply chain.

---

### Ce este MCP? {#what-is-mcp}

**MCP** vine de la Model Context Protocol. E o specificație pentru felul în care agenții vorbesc cu sistemele externe. Jira-ul tău. Confluence-ul tău. Postgres-ul tău. GitHub-ul tău. Data warehouse-ul intern. Orice trăiește în afara mediului local al agentului, dar pe care agentul trebuie să-l interogheze sau să-l actualizeze.

Înainte de MCP, fiecare agent avea propria poveste de integrare. Claude se integra cu Jira într-un fel; alt agent se integra cu Jira altfel; dacă schimbai agentul, refăceai toate integrările. MCP a schimbat asta. Același server MCP care vorbește cu Jira-ul tău funcționează cu orice agent care suportă MCP - iar majoritatea coding agents serioși suportă acum MCP.

Asta contează pentru achizițiile enterprise. O integrare MCP e portabilă. Investiția pe care o faci în configurarea unui server MCP pentru sistemele tale interne nu se pierde când se schimbă peisajul agenților. Următorul agent pe care îl adoptă echipa ta va putea folosi aceleași servere MCP pe care le-ai configurat deja. MCP e cel mai apropiat lucru pe care îl are ecosistemul de AI agentic de un „standard deschis care supraviețuiește schimbărilor de vendor”.

---

### Memory {#memory}

Memory e componenta principală devenită universală cel mai recent. Acum optsprezece luni era implicit: agentul încărca un prompt, lucra ceva, iar sesiunea următoare pornea de la zero. Astăzi Memory are două jumătăți, iar la mijlocul lui 2026 ambele au trecut linia convergenței.

**Memoria definită manual** e stratul pe care îl scrie echipa. Convergența e reală: Codex CLI, Cursor, GitHub Copilot, Gemini CLI, Aider și restul ecosistemului citesc toți AGENTS.md din rădăcina repository-ului la începutul sesiunii. Claude Code citește CLAUDE.md, care poate importa AGENTS.md pentru a împărți același conținut cu ceilalți agenți. Fișierul e versionat în source control, trecut prin review în pull request-uri, deținut de echipă. Acolo trăiesc pattern-urile interzise, intrările din jurnalul de greșeli, comenzile de build și glosarele de domeniu. Capitolul 6 detaliază ce intră în fișierul ăsta și de ce contează.

**Sistemul de auto-memory** e ceea ce scrie agentul pentru sine - pattern-uri învățate, salvate de la o sesiune la alta (comenzi de build pe care le-a dedus, concluzii de debugging pe care le-a confirmat, preferințe de stil de cod pe care le-a inferat), fără ca utilizatorul să le fi scris explicit. Jumătatea asta a convers într-o singură iarnă: GitHub Copilot Memory a ajuns în public preview în ianuarie 2026 și era activat implicit pe tier-urile individuale până în martie; Auto Memory din Claude Code a apărut în februarie; Codex CLI a adăugat memorie automată de fundal în aprilie. Stratul de consolidare al Anthropic merge un pas mai departe: Dreaming, dezvăluit odată cu Claude Managed Agents la Code with Claude SF pe 2026-05-06, e un proces programat de fundal care trece în revistă sesiunile recente și memoria stocată, identifică greșelile recurente și workflow-urile convergente și scrie note consolidate înapoi în memoria pe termen lung. Agentul devine mai bun pe codebase-ul tău între rulări.

O precizare despre ce *nu* e memorie în taxonomia asta: memoria de sesiune (istoricul conversației plus rezultatele tool-urilor din interiorul unei singure sesiuni) e doar context window-ul. E memorie în sensul de zi cu zi, dar nu o componentă principală separată - e componenta principală numită prima.

Ambele jumătăți trec testul convergenței încă de azi - stratul definit manual în ani, stratul de auto-memory în câteva luni de la prima livrare. Viteza asta e chiar testul convergenței funcționând: când un mecanism e structural, fiecare agent major și-l crește, repede. Manualul tratează cele două jumătăți ca pe o singură componentă principală pentru că rolul structural e identic.

---

**Subagenții** sunt instanțe-copil constrânse ale agentului însuși.

Agentul-orchestrator pornește un subagent, îi dă un task delimitat, cu un prompt cu scop restrâns, și îl lasă să ruleze în propriul context izolat, cu propriul acces limitat la tool-uri. Subagentul face treaba. Subagentul întoarce un rezultat. Orchestratorul colectează.

Ce îi face pe subagenți distincți structural față de celelalte componente principale e că sunt recursivi. Un subagent e o altă instanță a componentelor principale - are propriul context window, propriile tool-uri, propriile reguli de permisiuni și propriul sandbox, propriile skill-uri, plugin-uri, MCP și Memory - limitată la un task mai mic și izolată de contextul orchestratorului. Orchestratorul nu vede ce a văzut subagentul. Vede doar ce întoarce subagentul. Subagentul nu poluează contextul orchestratorului cu muncă intermediară. Orchestratorul nu poluează contextul subagentului cu istoric care nu-l privește.

Convergența în interval scurt cu care s-a deschis capitolul - toți agenții majori livrând subagenți în circa un an - nu e un accident. Subagenții rezolvă două probleme pe care nu le rezolvă niciun alt componentă principală: muncă în paralel delimitată de independență, nu de coordonare, și izolare a contextului delimitată de scopul task-ului, nu de istoricul sesiunii.

Utilizările principale în munca serioasă: execuția în paralel a unui plan cu mai multe task-uri (faza de Execute a buclei din Capitolul 5), review structurat (trimiți un subagent să verifice conformitatea cu specificația, altul să verifice calitatea codului) și analiză de arhitectură la scară (câte un subagent per fișier sau per modul, care întoarce rezumate structurate pe care orchestratorul le asamblează - workflow-ul din Capitolul 7).

Costul principal: tokenii. Fiecare subagent își rulează propriul model și propriile tool-uri, așa că un dispatch de opt subagenți consumă cam de opt ori tokenii unei rulări cu un singur agent. Folosește-i acolo unde contează paralelismul sau izolarea. Nu-i folosi by default pentru muncă pe care un singur agent ar putea s-o facă liniar.

La mijlocul lui 2026, compoziția asta începe să fie oferită direct de tool-uri, ca funcționalitate. /workflows din Claude Code pune agentul să scrie un script scurt care trimite subagenți în mod determinist - fazele rulează în ordine, munca se ramifică în paralel sau curge printr-un pipeline, fiecare predare întoarce o structură validată după o schemă, nu text liber, iar un pas de verificare poate pune un gate pe rezultat înainte să-l întoarcă. Un singur workflow se poate ramifica în sute de copii, ține munca lor intermediară în variabile de script, nu în context window-ul orchestratorului, se poate relua și are buget limitat. Nu e o componentă principală nouă. E o comoditate la nivel de harness peste componenta principală subagent pe care îl ai deja: determinismul - fluxul de control scris în cod, predări validate prin schemă - e singura diferență reală față de dispatch-ul condus de model pe care ți-l dă deja un plugin ca Superpowers, unde orchestratorul decide în timpul rulării câți copii pornește și le citește înapoi proza. Apelează la varianta scriptată când fan-out-ul e mare, repetabil sau merită verificat mecanic; apelează la dispatch-ul condus de model când nu știi forma muncii până nu intri în ea cu agentul. Ce se compune e același lucru în ambele cazuri.

Revenim la subagenți în Capitolul 5 (Execute) și în Capitolul 7 (review de arhitectură la scară). Ideea din capitolul ăsta e că ei nu sunt o tehnică așezată peste arhitectură. Sunt componenta principală de compoziție al arhitecturii.

---

Mai e o piesă care le organizează pe toate. Vendorii îi spun harness. Harness-ul e runtime-ul din jurul modelului - partea care transformă modelul brut în ceva util pentru scris cod.

Când îi ceri unui agent să facă o treabă, harness-ul e codul care îți ia cererea, o formatează pentru model, gestionează context window-ul, trimite spre execuție tool call-urile pe care vrea să le facă modelul, capturează rezultatele, i le dă înapoi modelului, decide când a terminat modelul și îți întoarce rezultatul final. Toate componentele principale trăiesc în interiorul harness-ului. Harness-ul e arhitectura; componentele principale sunt componentele.

De ce contează distincția asta: când compari agenți, tentația e să compari modele. „E Claude Code mai bun decât Codex sau Cursor pentru workflow-ul pe care îl rulează echipa mea?” - asta e întrebarea corectă. „Care model are scorul de benchmark mai mare trimestrul ăsta?” - asta e cea greșită. Modelul determină plafonul. Harness-ul determină dacă îl atingi. Compară harness-uri, nu modele.

Spus simplu: harness-ul e tot ce îmbracă bucla agentului. Bucla agentului în sine e banală. Are cam forma unui handler de request HTTP dintr-un framework web - primește promptul, rulează modelul, execută tool-urile, întoarce răspunsul, repetă. Middleware-ul din jurul buclei e locul unde stă munca adevărată. Middleware-ul *este* harness-ul, *este* componentele principale, *este* ceea ce cumperi de fapt când adopți un agent.

---

O notă despre vocabular. Componentele principale numite aici sunt ceea ce folosește agentul ca să știe, să acționeze, să fie ținut în frâu, să se extindă, să se integreze, să-și amintească și să delege. Testul pentru statutul de componentă principală e convergența: un mecanism e componentă principală atunci când fiecare coding agent major îl livrează ca pachet distinct și configurabil, chiar dacă implementările diferă substanțial. Permisiuni / Sandbox trece testul pe jumătatea stratului de decizie la toți agenții majori; jumătatea de enforcement la nivel de OS e convergentă ca prezență, dar divergentă ca postură, cu posturile vendorilor catalogate în secțiunea de mai sus. Componenta principală Memory are aceeași formă pe a doua lui jumătate. Telemetria e cel mai aproape de linie: până la mijlocul lui 2026, Claude Code, Codex CLI și CLI-ul Gemini livrau toate export nativ de OpenTelemetry, deci convergența e pe drum - nu ca protocol dedicat de event-push, ci ca OTel pur și simplu. Deocamdată rămâne un strat de control în jurul componentelor principale; încă o tură de roată și lista crește din nou. Capitolul ăsta e primul catalog de convergență; Capitolul 3 e al doilea.

---

Context window. Tool-uri. Permisiuni / Sandbox. Skill-uri. Plugin-uri. MCP. Memory. Subagenți. Plus harness-ul, ca runtime care le organizează. Asta e lista de azi. Setul e deschis; așteaptă-te să crească. Următoarea componentă principală va intra în listă exact cum a intrat Memory: când apare convergența, nu înainte.

Când apare următorul coding agent în marketplace, trimestrul viitor, grila de evaluare e deja aici. Cât de mare e context window-ul și cum îl gestionează agentul sub presiune? Ce tool-uri sunt disponibile și cum sunt constrânse? Ce model de permisiuni livrează - reguli allow/ask/deny, clasificator auto-mode - și ce sandbox de OS are by default? Cum sunt implementate skill-urile - always-loaded sau activate la detecție? Există un marketplace de plugin-uri și crește? Vorbește MCP, și cât de bună e integrarea MCP? Citește un fișier de memorie partajat de echipă la începutul sesiunii? Menține vreo memorie învățată, scrisă de agent, de la o sesiune la alta? Cum expune subagenții - și e dispatch-ul în paralel o operație de primă clasă sau o idee adăugată ulterior?

Nouă întrebări azi, pe opt componente principale - Memory primește două; mâine vor fi mai multe. Îți spun aproape tot ce ai nevoie ca să compari agentul nou cu cel pe care îl folosești acum.

Capitolul următor: ce se întâmplă când îndrepți un agent spre sursa altuia. Anatomia pe care tocmai am descris-o devine foarte reală, foarte repede.

---

**Artefact: fișa de evaluare a agenților.** Câte o coloană per componentă principală; notează implementarea fiecărui agent nou cu basic / intermediate / advanced. Folosește-o ca grilă pentru orice agent nou pe care îl evaluează echipa ta.

---

**De pus în practică săptămâna asta.**

Deschide orice coding agent la care ai acces. Întreabă-l: cât de mare e context window-ul tău, la ce tool-uri ai acces, cu ce model de allow/ask/deny și cu ce sandbox vine agentul ăsta, unde stau skill-urile, din ce marketplace se instalează plugin-urile, vorbește agentul ăsta MCP, de unde citește agentul memoria partajată de echipă și cum trimit un subagent? Notează răspunsurile. Ai deja începutul unei fișe de evaluare a agenților.

---

## Capitolul 2
## Anatomia invariantă

În timp ce pregăteam manualul, am rulat un experiment ca să testez empiric framework-ul. Rezultatul e demonstrația în oglindă în jurul căreia e construit capitolul. Majoritatea demonstrațiilor cu coding agents arată agentul făcând exact ce promite de obicei reclama - scrie o feature nouă, repară un bug, generează teste. Demonstrația mea a făcut altceva. Am folosit Claude Code, coding agent-ul, ca să inspectez codul sursă al altor doi coding agents, unul lângă altul, în paralel.

Cei doi agenți inspectați au fost Codex CLI și opencode. Amândoi sunt complet open source. Codex CLI e scris în cea mai mare parte în Rust, licențiat Apache 2.0 și întreținut de OpenAI. opencode e scris în cea mai mare parte în TypeScript, licențiat MIT și întreținut de o echipă independentă. Servesc cam același scop. Au fost construiți independent. Nu au nicio linie de cod în comun.

Am deschis două panouri de terminal. În panoul din stânga, Claude Code în repository-ul Codex. În cel din dreapta, Claude Code în repository-ul opencode. Același prompt tastat în ambele: "Explain the architecture of this codebase. Map the agent loop, the tool system, the permission gates, the sandbox componente principale, and the plugin model. Cite specific files and line numbers."

Ambele panouri au lucrat în paralel, independent, fiecare cu propriul context window, fiecare pe propriul repository. Cam patru minute pe ceas - am refăcut benchmark-ul în mai 2026 și a ieșit patru minute și treisprezece secunde, din care vreo șapte au fost `git clone`-ul shallow. Restul a fost agentul umblând prin arborii de directoare, numind componentele principale și citând fișiere. Cifra depinde de faptul că ambele repository-uri își publică arhitectura în numele crate-urilor și ale directoarelor: Codex are `core-skills`, `core-plugins`, `mcp-server`, `tools`, `agent`; opencode are `skill/`, `plugin/`, `mcp/`, `tool/`, `agent/`. Pentru un codebase mai puțin auto-documentat, socotește mai degrabă zece-cincisprezece minute per repo. Demo-ul e rapid pentru că, la nivel de nume de fișier, convergența se vede cu ochiul liber - ceea ce e, în sine, lecția de fond.

Panourile au întors două rezumate de arhitectură, unul pentru Codex în Rust, unul pentru opencode în TypeScript. Rezumatele nu arătau identic - alte nume de fișiere, alte structuri de foldere, alte idiomuri. Dar aveau aceeași formă.

În ambele repository-uri, Claude Code a găsit o buclă de agent. Codex o implementa în `core/session/turn.rs`. În opencode, bucla trăiește în `session/prompt.ts`. Alt limbaj, alt nume de fișier, aceeași buclă: primește promptul, rulează modelul, execută tool-urile, capturează rezultatele, decide dacă mai continuă, repetă.

În ambele repository-uri, Claude Code a găsit un registru de tool-uri. Codex folosea un trait de Rust - fiecare tool implementează trait-ul, registrul enumeră implementatorii. La opencode, același rol îl joacă o interfață TypeScript - fiecare tool implementează interfața, registrul enumeră implementările. Constructe de limbaj diferite, același pattern.

În ambele repository-uri, Claude Code a găsit un gate de permisiuni. Codex trecea fiecare tool call printr-o verificare de permisiuni înainte de execuție. Același pattern se regăsea în opencode. Căi de cod diferite, același rol arhitectural.

În ambele repository-uri, Claude Code a găsit o componentă principală de sandbox. Și aici, pentru prima dată în comparație, implementările au divergat substanțial. Codex implementa izolare reală la nivel de OS pe trei platforme - Seatbelt pe macOS, bubblewrap cu Landlock și seccomp pe Linux, token-uri restricționate cu job objects pe Windows. Kernelul însuși refuza syscall-urile pe care agentul nu era autorizat să le facă. Prin contrast, opencode implementa o îngrădire soft - validare de căi și prompt-uri de permisiune, dar fără o graniță impusă de kernel.

Aceeași componentă principală. Același rol arhitectural. Implementare substanțial diferită. Implicații de guvernanță substanțial diferite.

În ambele repository-uri, Claude Code a găsit un model de plugin-uri. Codex încărca plugin-urile dintr-un director configurat. Modelul de plugin-uri din opencode folosea un pattern similar, de tip „pui fișierul în director”. Aceeași componentă principală conceptuală: extinzi capabilitățile agentului la runtime, fără să-l reconstruiești.

Și în ambele repository-uri, Claude Code a găsit suport pentru MCP. Același server de Jira, același server de GitHub, același server de Postgres funcționau cu amândoi agenții. Specificația de integrare e portabilă.

Și tot în ambele repository-uri, Claude Code a găsit o cale de dispatch pentru subagenți. În codebase-ul Codex, componenta principală de subagenți e cel mai vizibil dintre toate - acolo a fost feature-ul de afiș, iar codul de dispatch e ușor de găsit după nume. În opencode, calea echivalentă poartă un nume mai puțin proeminent, dar există, iar Claude Code a identificat-o după comportament: o funcție care pornește o instanță proaspătă de agent pe un prompt delimitat și un context izolat, întoarce un singur rezultat structurat și nu lasă niciodată contextul copilului să se scurgă înapoi în părinte. Suprafață diferită, aceeași componentă principală.

Componentele principale. Două implementări. Aceeași anatomie. Alegeri diferite despre cum materializezi anatomia.

---

**Fișă de caz: demo-ul cu doi agenți, componentele principale observabile în amândoi.**

| | |
|---|---|
| **Context** | Experiment în oglindă construit în timpul pregătirii manualului - Claude Code îndreptat simultan spre codul sursă al Codex (Rust) și al opencode (TypeScript) |
| **Problema** | Cititorii trebuiau să vadă că componentele principale nu sunt marketing specific Claude Code, ci invarianți structurali verificabili în sursă |
| **Intervenția** | Același prompt, două repository-uri; agentul identifică componentele principale din fiecare codebase folosind grep + tool-uri de citit fișiere |
| **Timp de agent** | ~4 min pe ceas (două panouri în paralel) |
| **Timp de corecție umană** | Zero - odată pornit, experimentul rulează cap-coadă fără intervenție |
| **Rezultat** | Aceleași componente principale prezente în ambele codebase-uri, în fișiere diferite, sub nume diferite, cu implementări substanțial diferite; anatomia e invariantă; implementarea, nu |
| **Limitări** | Experimentul verifică faptul că componentele principale există; nu dovedește că sunt la fel de bine implementate (și nu sunt) |

---

Îți povestesc despre demo-ul ăsta pentru că demo-ul e mutarea pedagogică centrală a manualului.

Odată ce ai văzut anatomia într-un agent, începi s-o vezi în fiecare agent. Vei citi documentația unui agent nou și ochii îți vor sări direct la „cum tratează ăsta context window-ul? ce tool-uri are? skill-urile se activează la detecție sau sunt always-loaded? există un model de plugin-uri? vorbește MCP?” Nu vei mai evalua agentul nou după afirmațiile de marketing. Îl vei evalua după poziția anatomică.

Ăsta e framework-ul. Anatomia e invariantă. Implementările variază. Alege implementarea care se potrivește constrângerilor tale, nu pe cea cu cel mai spectaculos demo.

Care sunt constrângerile tale? Afinitatea de limbaj - se potrivește runtime-ul agentului cu stack-ul echipei? Licența - Apache, MIT, comercială; poți citi sursa dacă ai nevoie? Potrivirea cu ecosistemul - conține marketplace-ul de plugin-uri integrările de care ai nevoie? Enforcement-ul de sandbox - ai nevoie de izolare la nivel de kernel sau e suficientă o îngrădire soft? Postura de audit - trebuie să demonstrezi conformitate în fața unui reglementator, și produce agentul artefactele cu care s-o demonstrezi? Sunt întrebări concrete, comparabile, decidabile. Nu sunt „care e mai bun”. Sunt „care se potrivește constrângerilor tale”.

Echipele care greșesc aici se fixează pe model. Dezbat Claude Code versus Codex versus Cursor, sau dezbat modelele de dedesubt ca și cum calitatea modelului ar determina singură calitatea livrării. Sunt întrebări diferite. În livrarea de software cu agenți, harness-ul, modelul de guvernanță și integrarea în workflow contează la fel de mult ca plafonul modelului. Harness-ul înseamnă componentele principale plus felul în care sunt organizate, iar diferențele dintre harness-uri sunt locul unde se joacă miza reală.

---

Un compromis de guvernanță concret înainte să mergem mai departe, pentru că va reapărea pe tot parcursul manualului.

Constatarea despre sandbox din demo e reală și are consecințe. Codex impune izolare la nivel de OS. Sandbox-ul opencode, nu. Dacă evaluezi ce agent pui în fața unui developer care îl va rula pe cod de client, diferența de sandbox contează. Nu e o afirmație de marketing. E verificabilă în sursă. Poți citi apelurile de kernel. Poți vedea dacă sandbox-ul e real sau e teatru.

Dar ideea de profunzime nu e „Codex are un sandbox mai bun”. Ideea de profunzime e că jumătatea de la nivel de OS a componentei principale Permisiuni / Sandbox numit în Capitolul 1 e locul unde vendorii diverg cel mai tare, iar alegerile pe care le face un vendor în privința componentelor principale sunt alegeri de guvernanță. Când compari agenți, nu compari doar capabilități. Compari filozofii de guvernanță.

Un vendor care livrează un sandbox real îți spune că se așteaptă ca agentul lui să fie folosit în medii în care pot ajunge instrucțiuni ostile - prin dependențe, prin fișiere compromise, prin prompt injection chiar în codebase. Construiește apărare în adâncime (defense in depth). Un vendor care livrează o îngrădire soft îți spune că se așteaptă ca agentul lui să fie folosit în medii de încredere, în care utilizatorul e la comandă, iar prompt injection-ul e o grijă teoretică. Ambele posturi pot fi apărate. Sunt posturi diferite.

Tu alegi. Să știi ce anume alegi - ăsta e rostul capitolului de arhitectură.

---

Acum ai mutarea.

Când apare următorul coding agent în marketplace-ul tău - și va apărea unul în trimestrul următor, pentru că ciclul se măsoară acum în luni - nu trebuie să citești postarea de lansare de pe blog. Nu trebuie să aștepți articolul comparativ. Nu trebuie să-l instalezi și să-l rulezi o săptămână ca să-ți formezi o părere.

Îi deschizi repository-ul. Localizezi asamblarea contextului. Localizezi registrul de tool-uri. Localizezi componenta principală Permisiuni / Sandbox (stratul de decizie + sandbox-ul de OS, cele două jumătăți numite în Capitolul 1). Localizezi încărcarea skill-urilor. Localizezi extinderea prin plugin-uri. Verifici suportul de MCP. Localizezi stratul de memorie (AGENTS.md sau echivalentul lui; orice suprafață de auto-memory expune vendorul). Localizezi dispatch-ul de subagenți - toate înfășurate în bucla de agent a harness-ului.

Opt puncte de inspecție. Douăzeci de minute de inspecție. Vei ști mai multe despre oportunitatea adoptării acestui agent decât îți va spune orice articol de review, pentru că vei ști dacă alegerile lui concrete de implementare se potrivesc constrângerilor concrete ale echipei tale. Afinitate de limbaj. Compatibilitate de licență. Enforcement de sandbox. Postură de audit. Întrebările sunt stabile.

Marketingul vendorului îți spune pe ce vrea el să te uiți. Codul sursă îți spune ce a construit de fapt. Invarianța arhitecturii îți dă lentila prin care vezi dincolo de marketing.

Asta e mutarea. Ia-o cu tine.

---

Capitolul următor e dedicat guvernanței - care sunt straturile, ce face fiecare, ce se întâmplă când lipsește unul dintre ele. Compromisul de sandbox prin care tocmai am trecut e un exemplu de ce contează întrebarea guvernanței. Mai sunt straturi deasupra și dedesubtul sandbox-ului, și toate au nevoie de atenție.

---

**Artefact: checklist-ul de inspecție a sursei.** Cele opt puncte de inspecție din capitolul ăsta. Folosește checklist-ul pe următorul agent care intră în queue-ul de evaluare a echipei tale.

---

**De pus în practică săptămâna asta.**

Deschide repository-ul sursă al oricărui coding agent open source. Găsește fișierul care implementează bucla agentului. Citește-l. Douăzeci de minute. N-o să înțelegi fiecare linie; o să înțelegi forma buclei, și ăsta e tot rostul.

---

**Încearcă și tu.**

Agenții de mai jos vor fi înlocuiți. Tehnica de mai jos, nu.

Alege doi coding agents open source al căror cod sursă e publicat. În mai 2026, Codex CLI și opencode sunt perechea cea mai la îndemână pentru început: ambele repository-uri sunt publice, ambele își numesc componentele principale în structura de directoare și fac alegeri de guvernanță substanțial diferite, pe care le poți vedea în sursă.

1. Clonează ambele repository-uri.
2. Deschide coding agent-ul tău principal (cel pe care îl folosești zi de zi) într-un repo. Deschide o a doua instanță în celălalt.
3. Pune-i fiecărei instanțe aceeași întrebare: "Walk this codebase and name the primitives - context window, tools, permissions / sandbox, skills, plugins, MCP, memory, subagents. For each, tell me which file or module implements it, and rate the implementation basic, intermediate, or advanced."
4. Salvează cele două răspunsuri într-un tabel markdown pe două coloane.
5. Citește tabelul. Componentele principale sunt aceleași în ambele. Alegerile de implementare sunt diferite. Acele alegeri sunt alegeri de guvernanță, și ele sunt felul în care deosebești doi agenți la nivel de cod sursă.

Pe generația de agenți din mai 2026, parcurgerea durează între patru și zece minute per repo. Pentru un codebase mai puțin auto-documentat, socotește mai degrabă cincisprezece. Cei doi agenți pe care îi vei compara peste un an nu vor mai fi aceștia doi. Componentele principale, diagnosticul și ce îți spune diagnosticul despre guvernanță - da.

---

## Capitolul 3
## Guvernanța în straturi

Am deschis manualul cu PocketOS. Aici vine partea din lecție care merită un capitol întreg: guvernanța, pe straturi.

Incidentul PocketOS e cazul de manual pentru ce previn aceste straturi. La fel și incidentul Terraform care urmează. Ambele s-au întâmplat la începutul lui 2026, unor echipe convinse că sunt atente. Ambele ar fi fost blocate de oricare dintre mai multe mecanisme de control pe care echipele respective nu le aveau puse la punct. Capitolul ăsta e catalogul acelor mecanisme: cinci straturi de apărare, fiecare prinzând ce le scapă celorlalte, fiecare ieftin de pus în funcțiune odată ce ai decis să-l pui în funcțiune. Când cei de la securitate sau conducerea te întreabă ce stă între echipa ta și un PocketOS propriu, catalogul ăsta e răspunsul pe care li-l dai.

---

La sfârșitul lui februarie 2026, Alexey Grigorev de la DataTalks.Club a pierdut doi ani și jumătate de infrastructură de cursuri pentru că Claude Code a lucrat pe un state file Terraform rămas în urmă. Claude nu avea o hartă corectă a infrastructurii existente; a rulat `terraform destroy` peste ce a interpretat el drept resurse orfane. AWS a restaurat aproximativ 1,94M de rânduri dintr-un snapshot în circa o zi; pierderea de date a fost parțială, dar reală.

*Notă despre surse. Incidentul Terraform e documentat public; detaliile și citarea, în Anexa C.*

Eșecul PocketOS e o poveste despre o credențială pe care agentul n-ar fi trebuit s-o aibă. Eșecul Terraform e o poveste despre o hartă despre care agentul nu știa că îi lipsește. Moduri de eșec diferite; aceeași cauză arhitecturală. Niciunul nu se rezolvă cu un model mai bun. Ambele se rezolvă cu aceeași disciplină de guvernanță: agentul rulează într-un sandbox în care operațiunile distructive cer confirmare explicită, deține doar credențialele necesare pentru task-ul curent și lucrează pe o stare pe care echipa a verificat-o. Straturile din acest capitol există pentru că și PocketOS, și pierderea lui Grigorev s-au întâmplat în 2026, unor echipe convinse că sunt atente.

Ambele incidente arată și cealaltă jumătate a buclei: platformele au învățat. La o săptămână după PocketOS, Railway a mutat fiecare ștergere de volum și de resursă - inclusiv calea de API folosită de agent - pe un soft-delete cu fereastră de recuperare de 48 de ore și a livrat credențiale de agent cu scop limitat, ca o sesiune să nu mai fie nevoită să țină deloc un token brut de platformă. Follow-up-ul lui Grigorev se citește ca un checklist din capitolul ăsta: delete protection activat, starea mutată dincolo de raza laptopului, un review uman înaintea fiecărui plan distructiv. Defense in depth ajunge și la stratul de infrastructură - ceea ce nu îți ia de pe umeri partea ta.

---

Ce putem învăța din PocketOS? Multe. Să începem cu lecțiile greșite, pentru că le văd citate la tot pasul.

Lecția greșită numărul unu: „agentul și-a ignorat instrucțiunile”. Da. Asta fac agenții uneori. Modelele mari de limbaj, chiar și cele foarte capabile, nu respectă perfect constrângerile formulate în limbaj natural. Oricine a livrat vreodată un system prompt și apoi a privit modelul cum îl încalcă știe asta. Soluția nu e „scrie system prompt-uri mai bune”. Soluția e să nu te bazezi niciodată pe instrucțiuni din system prompt drept control dur pentru acțiuni distructive.

Lecția greșită numărul doi: „agenții AI sunt nesiguri”. Nu e o concluzie utilă, pentru că orice tool puternic e periculos dacă îl îndrepți spre producție fără controale. O comandă de shell armată e la fel de periculoasă. Un UPDATE în SQL fără clauza WHERE e la fel de periculos. Întrebarea nu e „e tool-ul nesigur în abstract?”. Întrebarea e „ce controale aveam puse la punct și care dintre ele ar fi prins asta?”.

Lecția greșită numărul trei: „n-ar trebui să folosim AI pentru operațiuni pe baze de date”. Asta înseamnă să arunci productivitatea ca să eviți riscul, când utilizarea productivă a AI-ului pentru operațiuni pe baze de date e cât se poate de reală (ajungem și acolo). Lecția corectă nu e abstinența. Lecția corectă sunt controalele în straturi.

---

Iar acum lecția corectă.

PocketOS avea o instrucțiune în limbaj natural. Asta e mai slab decât stratul unu. Nu avea permisiuni aplicate efectiv, care să clasifice și să blocheze acțiunea distructivă. Nu avea un sandbox care să refuze operațiunea la nivel de OS. Nu avea segregarea secretelor, care să împiedice sesiunea să dețină credențiala de producție. Nu avea un hook care să forțeze aprobarea umană înaintea unei acțiuni distructive asupra infrastructurii. Nu avea telemetrie pe partea de agent, care să alerteze la folosirea unui token de producție în timpul unei sesiuni de coding. Spus în vocabularul Capitolului 1: Permisiuni / Sandbox ar fi prins incidentul de două ori - o dată la stratul de decizie, dacă regula ar fi existat, și o dată la stratul de OS, indiferent de regulă.

Niciun strat perfect, de unul singur, nu i-ar fi salvat cu certitudine. Dar oricare dintre straturile aplicate efectiv putea rupe lanțul, iar mai multe împreună ar fi făcut mult mai puțin probabil un eveniment de nouă secunde cu pierdere de producție.

Apărare în adâncime (defense in depth). Niciun strat nu e suficient singur. Redundanța e controlul.

Până la finalul capitolului vei ști ce face fiecare strat, ce nu poate face fiecare strat și cum le pui în funcțiune pentru munca ta.

---

Principiul care guvernează toate cele cinci straturi este principiul privilegiului minim: la fiecare nivel - agentul, procesul sub care rulează agentul, credențialele pe care le deține agentul, rețeaua la care ajunge agentul - acorzi minimul care permite muncii să se întâmple, și nimic în plus. Fiecare strat de mai jos e privilegiul minim aplicat pe altă dimensiune: ce poate face agentul, unde poate face, ce poate citi, ce categorii de acțiuni declanșează un gate uman, ce se înregistrează pentru audit. Privilegiul minim e coloana vertebrală. Straturile sunt implementarea.

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

---

Trei dintre aceste cinci straturi - permisiunile, hook-urile de securitate, sandbox-ul - sunt suprafețele de configurare ale componentei principale Permisiuni / Sandbox numit în Capitolul 1. Componenta principală e ceea ce livrează orice coding agent major; suprafețele sunt felul în care echipa ta îl configurează pentru codebase-ul tău, pentru modelul tău de amenințări, pentru postura ta de conformitate. Aceeași formă ca la Memory în Capitolul 1: o componentă principală, mai multe suprafețe de configurare. Memory are una (AGENTS.md / CLAUDE.md); Permisiuni / Sandbox are mai multe. Gestionarea secretelor și telemetria sunt controale de guvernanță adiacente - își au locul în acest capitol pentru că prind ce le scapă suprafețelor componentei principale, dar nu sunt ele însele suprafețe de configurare ale componentei principale. Tratarea în cinci straturi care urmează nu depinde de cum citești componenta principală - un pachet unitar sau cinci controale separate; ambele perspective duc la aceeași muncă de configurare.

---

**Stratul unu: permisiunile.**

E stratul pe care majoritatea echipelor îl cunosc deja, pentru că există de la primii coding agents încoace. Permisiunile răspund la întrebarea „are voie acest agent să execute această acțiune chiar acum?”.

În modelul mai vechi de permisiuni, declarai regulile explicit. Allow: citește orice fișier. Ask: scrie în orice fișier din afara directorului de lucru. Deny: șterge fișiere din `~/.ssh`. Deny: scrie în fișiere `.env`. Deny: rulează orice comandă care conține `rm -rf`. Agentul consulta regulile înaintea fiecărui tool call. Dacă o regulă se potrivea, regula decidea ce urmează.

Modelul mai nou, pe care îl recomand ca default, este auto mode. Auto mode predă decizia per acțiune unui clasificator - de regulă un model mai mic și mai rapid - care hotărăște la fiecare tool call dacă permite, întreabă sau refuză, în funcție de risc și de context. Clasificatorul citește acțiunea propusă și contextul din jur, își aplică antrenamentul și emite o judecată. Majoritatea acțiunilor trec în liniște. Unele sunt scoase la suprafață pentru aprobarea utilizatorului. Puține sunt blocate de-a dreptul.

Auto mode e mai permisiv în cazurile ușoare (zero fricțiune pe acțiunile de rutină) și mai restrictiv în cazurile grele (întreabă acolo unde un reviewer uman ar întreba). Nu înlocuiește regulile declarative - lucrează împreună cu ele. Pattern-ul recomandat: auto mode ca default, plus un set mic de reguli explicite care suprascriu clasificatorul acolo unde acesta greșește sau unde conformitatea cere reguli declarative explicite.

Setul mic trebuie să rămână mic. Reperul meu: zece-cincisprezece override-uri per repository. Dacă lista ta de override-uri crește peste atât, [AGENTS.md](https://agents.md/)-ul tău (ajungem și la AGENTS.md) e prea subțire, nu lista de reguli prea scurtă. Lista de override-uri se reduce scriind un ghidaj mai bun la nivel de echipă, pe care clasificatorul din auto mode să-l poată folosi, nu scriind tot mai multe reguli fragile care încearcă să anticipeze fiecare situație.

Stratul unu e ce va configura orice echipă prima dată. Stratul unu e și ce cedează când reușește un prompt injection. Un atacator iscusit, care poate injecta conținut în contextul agentului, poate uneori convinge agentul să ocolească gate-ul de permisiuni - nu spărgând gate-ul, ci păcălind agentul să ceară acțiuni pe care gate-ul nu le-ar vedea în mod normal. Permisiunile sunt necesare. Permisiunile nu sunt suficiente.

---

**Stratul doi: sandbox-ul.**

Stratul doi prinde ce i-a scăpat stratului unu.

Sandbox-ul e izolare la nivel de sistem de operare. Kernelul însuși refuză să execute syscall-urile pe care agentul nu e autorizat să le facă. Citire din afara căilor permise? Refuzată. Conexiune de rețea către un host care nu e pe allowlist? Refuzată. Scriere într-un director pe care sandbox-ul nu-l include? Refuzată.

Proprietatea crucială a unui sandbox e că nu face parte din agent. Face parte din sistemul de operare. Prompt injection nu poate ocoli sandbox-ul, pentru că prompt injection funcționează prin manipularea raționamentului agentului, iar kernelul nu ascultă de raționamentul agentului. Kernelul ascultă de apeluri de sistem. Apelul de sistem fie e permis, fie nu e. Raționamentul e irelevant.

O mențiune onestă merge chiar lângă garanția asta: sandbox-ul e și el cod, iar codul are bug-uri. La mijlocul lui 2026, un red team a dezvăluit două escape-uri critice zero-click ale sandbox-ului kernel-backed din Cursor (CVSS 9.8, patch-uite în următoarea versiune majoră) - instrucțiuni injectate prin prompt care abuzau chiar allowlist-ul de scriere al sandbox-ului ca să ajungă la execuție la nivel de OS. Proprietatea arhitecturală a ținut peste tot în rest; implementarea a avut o gaură. Asta nu e un argument împotriva sandbox-ului. E argumentul pentru celelalte patru straturi.

Coding agents moderni suportă sandbox-uri pe Linux (bubblewrap cu Landlock și seccomp), pe macOS (Seatbelt) și pe Windows (restricted tokens cu job objects). Sandbox-ul e opt-in. Configurezi allowlist-ul de căi și allowlist-ul de rețea, fie în fișierul de configurare al agentului, fie în AGENTS.md. Pentru majoritatea echipelor, default-ul corect e: citire pe tot repository-ul, scriere doar în worktree, rețea doar către host-urile permise explicit. Restul, blocat.

Sandbox-ul nu încetinește agentul în mod sesizabil. Doar refuză operațiunile care oricum ar fi trebuit refuzate. Dacă agentul tău se lovește regulat de limitele sandbox-ului în timpul muncii normale, limitele sunt greșite; lărgește-le. Dacă agentul tău nu se lovește niciodată de limitele sandbox-ului, probabil le-ai setat corect.

Configurarea sandbox-ului diferă de la agent la agent. Codex CLI impune sandbox-ul by default pe Linux și macOS; trebuie să renunți explicit la el, nu să-l activezi. În versiunile de Claude Code pe care le-am folosit în 2026, sandboxing-ul e disponibil, dar cere configurare explicită - trebuie să-l activezi tu, să configurezi allowlist-urile de căi și de rețea și să accepți micul cost administrativ. Tratează asta ca pe un detaliu de implementare legat de versiune, nu ca pe o proprietate universală a tool-ului. Majoritatea echipelor de Claude Code cu care am lucrat sar peste pasul ăsta, pentru că instalarea default merge și fără el. Instalarea default nu are însă nicio protecție împotriva prompt injection-ului sau a derapajelor agentului. PocketOS e exact cum arată o instalare default fără sandbox atunci când lucrurile merg prost. Sandbox-ul costă o după-amiază de configurare. Merită.

---

**Stratul trei: secretele.**

Stratul trei e protecția structurală a credențialelor.

---

**Incidente de securitate a agenților pe care trebuie să le cunoști.**

Trei clase de vulnerabilități documentate în 2025-2026 merită știute la acest strat:
- Auto-încărcarea de dot-env: agenții citesc secrete din fișierele `.env` aflate în directorul de lucru, la pornirea sesiunii.
- Injecția prin fișiere de configurare: fișiere de configurare de proiect care nu sunt de încredere (`.claude/settings.json`, `.mcp.json`) execută hook-uri înainte de dialogul de trust, deschizând calea către RCE sau exfiltrarea de API key-uri.
- Ocolirea parser-ului de permisiuni: reguli de deny sărite în tăcere când comenzile de shell se înlănțuie dincolo de un plafon de recunoaștere, sau când parser-ul nu recunoaște binarul (`open()` din Python, `fs.readFile` din Node).

A treia clasă merită o notă aparte, pentru că modul de eșec e ușor de citit greșit. Un check de securitate care scana comenzile de shell după potriviri cu regulile de deny retrograda în tăcere la un prompt generic de „ask” atunci când comanda înlănțuia mai mult de cincizeci de subcomenzi. Găsit de un red team extern la începutul lui 2026 și patch-uit într-o săptămână, dar clasa în sine merită reținută: un strat de guvernanță poate avea un mod de eșec silențios, a cărui existență nu e deloc evidentă din citirea configurației. Apărarea în adâncime înseamnă să presupui că orice strat luat singur poate avea un bug; celelalte straturi sunt cele care prind ce i-a scăpat acestuia.

Fiecare clasă a fost documentată și patch-uită sau mitigată. Clasa supraviețuiește; CVE-urile concrete, versiunile de patch și mitigările trăiesc în Anexa C, pentru că numerele de versiune îmbătrânesc mai repede decât pattern-ul de dedesubt.

O preocupare arhitecturală înrudită e injecția de conținut în fișierul de instrucțiuni al echipei printr-o dependență malițioasă sau printr-un contributor compromis, care poate schimba comportamentul agentului la fiecare pornire de sesiune; mitigarea e să tratezi fișierul de instrucțiuni al echipei (AGENTS.md sau echivalentul) drept cod versionat în repo: trecut prin review în PR, semnat de autor, parte din supply chain-ul tău.

---

Vulnerabilitățile astea sunt reale. Sunt însă și delimitate. Fiecare are un patch sau o mitigare documentată. Clasa de problemă - „gestionarea secretelor în sistemele agentice cere aceeași disciplină ca gestionarea secretelor oriunde altundeva” - e permanentă.

Recomandările mele: nu da commit la fișiere `.env` în git. Folosește un vault de secrete (HashiCorp Vault, AWS Secrets Manager, Doppler, ce folosește echipa ta) și trage secretele la runtime printr-un pas de fetch explicit, pe care agentul poate fi configurat să-l sară. Include căile sensibile în lista de deny-read a sandbox-ului - agentul pur și simplu nu le poate citi, indiferent ce spune system prompt-ul. Tratează fișierul de instrucțiuni al echipei (AGENTS.md sau echivalentul) drept cod versionat în repo: trecut prin review în PR, semnat de autor, parte din supply chain-ul tău.

Framing-ul pe care îl folosesc cu echipele: regulile de deny și configurația sunt apărare în adâncime. Sandbox-ul e granița dură. Vault-ul e alegerea structurală. Controale în straturi.

Vectorii de mai sus sunt cei cu nume. Mai există un vector care primește mai puțină atenție și lovește echipele mai des: injecția prin munca în sine. Ticket-ul de Jira ale cărui criterii de acceptare conțin un paragraf care începe cu „ignore all previous instructions and...”. Comentariul de PR de la un contributor extern, care strecoară o instrucțiune în ceva ce arată a notă de code review. Mesajul de eroare al unui test third-party instabil, pe care agentul îl citește și îl interpretează drept directivă. README-ul bibliotecii de la un vendor, adusă de agent în timpul research-ului. Repository-ul cu aspect inofensiv a cărui eroare plantată împinge agentul să ruleze un „fix” care își trage payload-ul real dintr-un DNS TXT record - un proof of concept demonstrat pe un agent major la mijlocul lui 2026, fără ca vreo semnătură să atingă discul. Oriunde agentul citește conținut în limbaj natural ca parte din munca lui e o potențială suprafață de injecție. Am văzut cu ochii mei un agent executând conștiincios o instrucțiune îngropată într-un fișier de log copiat și lipit, pentru că operatorul nu se gândise la un fișier de log ca la un input de neîncredere.

Mitigarea e aceeași postură ca în restul guvernanței: nu te baza pe raționamentul agentului ca să depisteze injecția. Constrânge ce poate face agentul indiferent de ce a citit. Sandbox-ul prinde acțiunea periculoasă chiar și atunci când agentul e convins că acțiunea e legitimă. Hook-ul prinde categoria periculoasă chiar și atunci când agentul e convins că „doar de data asta e în regulă”. Tratează orice input pe care îl citește agentul drept text de neîncredere - aceeași postură pe care un inginer cu experiență o are față de input-ul utilizatorului dintr-un formular web - și straturile tale de guvernanță vor prinde tentativa de injecție pe care designul promptului a ratat-o. Injecția care reușește e cea care găsește o acțiune pe care straturile de dedesubt nu au delimitat-o.

---

**Stratul patru: hook-urile de securitate.**

Stratul patru înseamnă reguli proprii, impuse la nivel de acțiune.

Un hook de securitate e cod care rulează înainte ca agentul să execute un anumit tip de acțiune. Hook-ul citește acțiunea propusă, o evaluează față de regulile echipei și fie o permite, fie cere confirmare, fie o blochează. Hook-urile se declanșează înainte de execuția tool-ului - pre-tool-use, în terminologia consacrată - așa că agentul nu poate duce la capăt o acțiune cu hook fără aprobarea hook-ului.

Pattern-ul cel mai des întâlnit e folosirea unui plugin (în ecosistemul Claude Code, plugin-ul security-guidance și altele asemenea) care vine din fabrică cu reguli pentru categoriile uzuale de vulnerabilități. Secrete scurse în diff-uri. Pattern-uri de SQL injection în codul propus. Credențiale hardcodate. Algoritmi criptografici nesiguri. Scrieri directe de fișiere pe căi cunoscute ca sensibile. Fiecare categorie e o regulă. Hook-ul verifică fiecare acțiune propusă față de fiecare regulă. La potrivire, hook-ul intervine.

Rostul hook-urilor e că sunt programabile. Cele opt sau zece categorii livrate de un plugin de-a gata sunt o bază bună. Echipa ta va avea propriile categorii pe deasupra - poate o regulă conform căreia orice schimbare în logica de conversie valutară cere aprobare explicită, sau una conform căreia orice commit care atinge tabela de clienți cere un reviewer de securitate, sau una conform căreia orice modificare a unui anumit modul relevant pentru conformitate e blocată complet în afara orelor de program. Adaugi regulile astea în hook, agentul le moștenește, fiecare sesiune le impune.

Hook-urile sunt instrumentul la care apelezi când stratul unu (permisiunile) e prea grosier, când stratul doi (sandbox-ul) e prea brutal, când stratul trei (secretele) e în regulă structural, dar tot vrei un gate per acțiune pe anumite operațiuni periculoase. Hook-urile sunt instrumentul de precizie.

---

**Stratul cinci: telemetria.**

Primele patru straturi sunt preventive. Opresc agentul să facă lucrul greșit de la bun început. Telemetria e detectivă: îți spune ce a făcut agentul, după ce a rulat, ca să poți audita și îmbunătăți.

Ce loghezi: fiecare tool call făcut de agent. Fiecare comandă de Bash. Fiecare scriere de fișier. Fiecare request către un API extern. Argumentele, rezultatele, timpii. Agentul vede că îl citești; agentul nu vede că îl loghezi. Logul e pentru tine.

Unde îl trimiți: într-un store central deținut de echipa de securitate. Splunk, Elasticsearch, SIEM-ul tău existent, un store custom - ce se potrivește stack-ului tău. Miza e durabilitatea și posibilitatea de interogare. Vrei să poți răspunde la „ce sesiuni au atins serviciul de plăți în ultimele treizeci de zile” fără să faci grep prin istoricele locale de agent ale celor optzeci de ingineri. Partea de plumbing a convers mai repede decât era de așteptat: până la mijlocul lui 2026, agenții majori emit OpenTelemetry nativ, așa că store-ul central poate fi orice vorbește deja stack-ul tău de observabilitate.

Ce urmărești: încălcări de scop (agentul a editat un fișier din afara task-ului asignat), apeluri externe neobișnuite (agentul a contactat un host care nu era pe allowlist-ul lui), refuzuri repetate de permisiuni (agentul a încercat ceva interzis de mai multe ori - fie un bug în setul de reguli, fie o tentativă de prompt injection), credențiale de producție în context (agentul a încărcat un fișier care conține ceva ce arată a secrete).

Incidentul PocketOS e și un eșec de Stratul 5. Apelul distructiv de Volume Delete a generat un audit log de API Railway pe partea de server. Dar PocketOS nu avea monitorizare detectivă a comportamentului propriului agent; nicio alertă nu s-a declanșat când o sesiune de agent a contactat Railway cu un token de producție. Primul semnal primit de echipă a fost baza de date devenită inaccesibilă.

Stratul 5 nu previne PocketOS. Straturile 1-4 previn PocketOS. Stratul 5 detectează momentul în care prevenția a eșuat, așa că timpul de reacție trece de la „două zile până ne dăm seama” la „două minute până primește alerta inginerul de on-call”. Diferența asta e diferența dintre un incident și o catastrofă.

---

Cinci straturi. Permisiuni, sandbox, secrete, hook-uri de securitate, telemetrie. Fiecare prinde ce le scapă celorlalte. Fiecare are alt mod de eșec. Fiecare e configurabil. Niciunul nu trebuie tratat drept opțional pentru o utilizare serioasă în producție.

Lecția PocketOS nu e „AI-ul e nesigur”. Lecția PocketOS e „un singur strat de apărare nu e de ajuns”. Două straturi sunt semnificativ mai sigure decât unul. Trei straturi sunt semnificativ mai sigure decât două. Patru straturi preventive plus telemetria ca al cincilea îți dau redundanța care face ca un singur eșec să nu devină dezastru, plus pista de audit din care înveți din incidentele evitate la mustață.

Configurează cele cinci straturi o singură dată. Întreține-le ca pe orice altă infrastructură. N-o să regreți în ziua în care ceva merge prost, pentru că ziua aia va veni.

---

**Practici adiacente.**

Cele cinci straturi de mai sus sunt controalele orientate către agent. Două practici adiacente țin de aceeași postură de guvernanță, pentru că prind ce nu prind straturile.

Separarea mediilor. Agentul nu deține credențiale de producție by default. Credențialele de staging și de development sunt limitate la ce e accesibil din acele medii. Acțiunile de producție trec printr-un gate de workflow separat - o aprobare umană, un pipeline de CI, un script de deploy - pe care agentul o declanșează, dar nu o execută cap-coadă. Incidentul PocketOS e, în parte, o poveste despre o sesiune de agent care deținea credențiale ce ar fi trebuit segregate.

Branch-uri protejate, CODEOWNERS, politică de CI. Agentul face commit și deschide pull request-uri, ca orice alt contributor. Regulile de protected branch, review-urile CODEOWNERS și politica de CI se aplică PR-urilor agentului exact cum se aplică PR-urilor unui om. Majoritatea echipelor le au deja. Asigură-te că PR-urile agentului trec prin ele, nu pe lângă ele.

---

**Artefact: Auditul de guvernanță pe cinci straturi.** Punctează fiecare strat pentru un codebase deținut de echipa ta: default / configurat / impus / monitorizat. Auditul devine baza de referință pentru investiția din trimestrul următor.

---

**De pus în practică săptămâna asta.**

Auditează un codebase deținut de echipa ta. Din cele cinci straturi de guvernanță (permisiuni, sandbox, secrete, hook-uri de securitate, telemetrie), câte sunt configurate dincolo de default? Notează de la unu din cinci până la cinci din cinci. Scorul ăsta e punctul tău de plecare.

---

**Încearcă și tu.**

E o disciplină pe care o poți rula la orice cadență: lunar, după fiecare incident, înaintea fiecărui rollout nou de agent.

Alege un repository deținut de echipa ta. Ideal, unul în care lași deja un agent să facă commit-uri. Auditează-l față de cele cinci straturi de guvernanță din acest capitol:

1. Permisiuni. Ce poate rula agentul fără un prompt de confirmare? Sunt operațiunile distructive (rm, terraform destroy, drop table, force push pe main) păzite de un gate? Punctează stratul cu DEFAULT, CONFIGURED, ENFORCED sau MONITORED.
2. Sandbox. Rulează agentul într-un sandbox impus de kernel, sau „izolarea” lui e o validare de căi în codul agentului însuși? Aceeași scară în patru trepte.
3. Secrete. Unde trăiesc credențialele? Au ajuns fișiere .env în repo? Poate agentul ajunge la token-uri de producție din mediul lui de lucru curent? Punctează.
4. Hook-uri. Există hook-uri pre-tool-call care auditează, loghează sau pun un gate pe operațiunile periculoase? Punctează.
5. Telemetrie. Când agentul rulează o comandă distructivă, apare asta într-un dashboard pe care echipa îl va vedea în câteva minute? Punctează.

Scrie cele cinci scoruri pe o foaie de o pagină. Pentru fiecare strat aflat sub ENFORCED, numește un fix concret și un responsabil. Foaia e planul tău de remediere pentru trimestrul următor.

Scorul nu e admis/respins; e baza ta de referință. Un repository cu DEFAULT sau CONFIGURED pe toată linia e ceva normal. Un repository cu ENFORCED sau MONITORED peste tot e de nivel de producție. Munca dintre cele două stări e exact despre ce e manualul ăsta.

---

Partea I se încheie aici. Ai arhitectura. Știi ce e un agent din punct de vedere anatomic, cum evaluezi unul când apare, ce straturi de guvernanță pui în funcțiune ca să-l ții sub control.

Partea a II-a e despre cum livrezi software cu agentul acum, că el există în mediul tău. Arhitectura răspunde la „ce e chestia asta”. Metoda răspunde la „cum facem treabă cu ea”. Ambele sunt necesare. Niciuna nu e suficientă de una singură.

Să-i dăm drumul.

---

# Partea a II-a - Metoda

> *Controlul workflow-ului: cum se formulează, cum se execută și cum se verifică munca.*

---

## Capitolul 4
## De la cod generat la software livrat

Cea mai frecventă eroare pe care o văd la echipele care adoptă programarea cu agenți este că tratează agentul ca pe un generator de cod. Folosesc agentul pentru partea de muncă în care se tastează cod. Restul livrării de software îl fac exact cum l-au făcut dintotdeauna. Și apoi se miră de ce contribuția agentului pare marginală sau, mai rău, de ce echipa pierde mai mult timp reparând output-ul agentului decât a câștigat lăsându-l pe el să tasteze.

Greșeala e că generarea de cod nu mai e bottleneck-ul.

În ultimii patruzeci de ani de inginerie software, constrângerea pe output a fost, foarte aproximativ, viteza cu care un developer putea tasta cod valid care făcea cam ce trebuia. Autocomplete-ul a ajutat. IDE-urile mai bune au ajutat. Tastatul asistat de AI a ajutat mult. Fiecare dintre aceste tool-uri a atacat aceeași constrângere - timpul dintre „știu ce vreau să scriu” și „codul e pe ecran”. Fiecare generație de tooling a mai ros câte puțin din decalajul ăsta.

AI-ul agentic sparge constrângerea. Agentul poate produce o sută de linii de cod care compilează în timpul în care tu formulezi promptul. Producția de cod s-a prăbușit cu un ordin de mărime în genul de muncă pe care agentul îl face bine. Nu a ajuns la zero - agentul tot costă latență, tokeni și timpul tău de formulare și de review - dar costul marginal al următoarelor o sută de linii de cod a scăzut de la „o oră de tastat” la „treizeci de secunde de așteptat”. Asta e constrângerea care se rupe. Așa că, dacă metoda ta e „agentul produce cod, tu faci review pe cod, tu livrezi cod”, bottleneck-ul tău s-a mutat. Bottleneck-ul nu mai e producerea codului. Bottleneck-ul e *dacă poți formula munca suficient de clar încât agentul să facă exact ce trebuie.*

Fraza asta e afirmația metodologică centrală a manualului.

Bottleneck-ul e disciplina formulării. Capabilitatea există. Ce desparte echipele care livrează bine cu agenți de echipele care se zbat e dacă și-au construit obiceiul de a formula munca într-un mod pe care agentul îl poate executa corect. Echipele fără acest obicei ajung la specificații vagi. Specificațiile vagi produc ghicit. Ghicitul produce output care arată corect și nu e. Echipele cu practica formată ajung la specificații tăioase. Specificațiile tăioase produc execuție predictibilă. Execuția predictibilă produce output pe care îl poți livra.

---

Ce înseamnă „disciplina formulării” în practică?

Întâi, claritate pe domeniu înainte să se scrie orice linie de cod. Agentul nu îți cunoaște business-ul. Nu îți cunoaște convențiile. Nu cunoaște istoria din spatele felului în care arată codebase-ul tău. Înainte să-i ceri agentului o modificare, trebuie să-i încarci context - prin [AGENTS.md](https://agents.md/), prin skill-uri, prin faza de Research a workflow-ului, prin orice alt mecanism. Volumul de muncă pregătitoare necesară a *scăzut* față de era pre-agent (pentru că agentul poate face singur o bună parte din încărcare), dar nu a ajuns la zero. S-a mutat din „îți încarci contextul în propriul cap” în „încarci contextul în context window-ul agentului”.

În al doilea rând, descompunerea pe fișiere și pe task-uri înainte de orice acțiune. Agentul va încerca bucuros un refactor pe mai multe fișiere dintr-un singur foc. Output-ul va arăta impresionant. Va fi și mult mai greu de revizuit decât același refactor descompus în cinci pași mici, fiecare o modificare coerentă. Regula e să faci descompunerea explicită - scrii întâi planul, apoi execuți planul, apoi verifici fiecare pas independent. Nu e un sfat nou; inginerii seniori au lucrat dintotdeauna așa la schimbările complexe. Agentul face însă ca prețul lipsei de descompunere să fie mult mai mare, pentru că agentul va produce ceva care compilează indiferent dacă e bun sau nu.

În al treilea rând, refuzul de a spune „gata” fără verificare. Agentul îți va spune că modificarea e completă. Agentul va fi sincer. Agentul va fi, uneori, și pe lângă, pentru că senzația lui internă de „arată bine” nu e totuna cu „am rulat testele și trec”. Regula e: nu există „gata” fără dovezi din teste. Nu teste unitare bifate de formă - teste comportamentale reale, care exersează modificarea. Dacă modificarea ta nu poate fi testată comportamental, probabil că nici nu trebuia să fie un task pentru agent.

Trei obiceiuri. Claritate pe domeniu înainte de cod. Descompunere pe fișiere și pe task-uri. Dovezi din teste înainte de „gata”. Toate trei țin de formulare, nu de generare. Toate trei sunt ce desparte o echipă care livrează software cu agenți de o echipă care doar generează cod cu agenți.

Primele două obiceiuri nu sunt scopuri în sine. Claritatea pe domeniu și descompunerea sunt felul în care ajungi la un rezultat așteptat bine definit, iar al treilea obicei e dovadă măsurată față de acel rezultat - fără un rezultat definit, dovada nu mai are ce să dovedească.

---

Aici e momentul să anticipez obiecția. Probabil te gândești: sună a multă muncă pentru ceva care trebuia să-mi economisească timp.

Întâi, e mai puțină muncă decât pare. Disciplinele de mai sus sunt, în mare parte, deja practicate de inginerii seniori buni la schimbările importante. Formulează cu grijă. Descompun. Verifică. Ce nu fac întotdeauna e să împacheteze practica într-o formă care scalează - care călătorește de la obiceiurile unui om la obiceiurile unei echipe, de la un repository la mai multe, de la un proiect la un an de proiecte. Workflow-ul cu agenți îți permite să codifici practica o singură dată și s-o aplici peste tot. Costul total e mai mic, chiar dacă costul per task e comparabil.

În al doilea rând, alternativa e mai proastă. Abordarea „lasă agentul în freestyle” pare mai rapidă pe moment. Produce output vizibil. Output-ul ajunge la code review. Reviewerul prinde bug-urile (uneori). Bug-urile se întorc la agent. Ciclul se repetă. Până ajunge modificarea în producție, echipa a cheltuit în total mai mult timp decât ar fi cheltuit dacă impunea rigoare de la început. Senzația că „disciplina ia timp” e reală. Realitatea că „lipsa de disciplină ia mai mult timp” e și ea reală - și de obicei invizibilă până nu te uiți la cycle time pe un trimestru întreg.

Am văzut asta pe mai multe echipe: cele care au impus rigoare devreme au livrat mai repede la nivel de trimestru. Cele care au lăsat agentul în freestyle s-au simțit mai rapide pe moment și au livrat mai încet pe trimestru. Aceleași echipe, aceiași agenți, aceleași codebase-uri. Disciplină de formulare diferită. Rezultate substanțial diferite.

O euristică pentru momentul în care disciplina formulării se amortizează. Nu orice task are nevoie de bucla completă. Costul unei formulări bune - nota de research, planul la nivel de fișier, definițiile testelor - se plătește în avans, înainte ca agentul să scrie vreo linie. Pentru munca trivială, costul formulării depășește contribuția agentului și pierzi timp.

Practica se amortizează când cel puțin una dintre condițiile astea e adevărată: munca atinge mai mult de trei fișiere (blast radius-ul e destul de mare încât un agent nesupravegheat va greși ceva); schimbarea taie transversal prin mai multe straturi (schema bazei de date plus service layer plus UI, unde un singur pas greșit se propagă în cascadă); sau n-ai face munca tastând-o tu însuți (e cu adevărat nouă, sau mare, sau în cod pe care nu-l cunoști destul de bine ca să-l scrii de mână). Dacă niciuna nu se aplică, scrie-o tu. Un bugfix de două linii nu are nevoie de notă de research. O modificare de config de o linie nu are nevoie de plan.

Modul de eșec pe care îl văd cel mai des: echipe care aplică bucla la absolut tot (și încetinesc) sau la absolut nimic (și ratează câștigurile). Euristica de mai sus le desparte. Folosește bucla când costul formulării e mai mic decât costul ca agentul să greșească; sari peste ea când nu e.

Studiul randomizat controlat METR, publicat în iulie 2025, a măsurat exact asta. Developeri open-source experimentați, lucrând cu asistență AI (Cursor cu Claude) pe propriile repository-uri, pe care le cunoșteau bine, au avut nevoie de 19% mai mult timp ca să termine task-urile decât aceiași developeri lucrând fără AI. Înainte de studiu, developerii au prezis că AI-ul îi va face cu 24% mai rapizi. După studiu, în ciuda încetinirii obiective, tot credeau că AI-ul i-a făcut cu aproximativ 20% mai rapizi. Asta înseamnă un decalaj de 43 de puncte între accelerarea prezisă și încetinirea măsurată - și o percepție care persistă chiar și după ce datele o contrazic.

METR nu a testat disciplina formulării ca variabilă separată. Au măsurat asistența AI brută pe cod familiar. Eu tratez rezultatul METR ca pe un avertisment: asistența AI brută nu se transformă automat în viteză de livrare. Variabila lipsă e disciplina de workflow. Echipele care impun proces pot face mai bine de atât. Echipele care nu impun pot rămâne la nivelul METR sau sub el - convinse, între timp, că sunt mai rapide.

*Notă despre surse. Studiul METR a fost publicat în iulie 2025. Follow-up-ul propriu al METR s-a împotmolit: replicarea a suferit un selection bias destul de sever încât METR a reproiectat experimentul în februarie 2026 și avertizează să nu citești cifra din 2025 ca pe o măsură a tool-urilor actuale. Avertismentul rămâne valabil; cifra e o măsurătoare datată a unui decalaj de percepție persistent. Interpretarea că disciplina de workflow e variabila lipsă îmi aparține, nu e a studiului. Citarea, în Anexa C.*

Cea mai vie versiune a acestui contrast pe care am văzut-o cu ochii mei: două echipe din aceeași companie, lucrând pe zone adiacente ale aceluiași produs. Echipa A a dat drumul agentului din prima zi. Au sărbătorit velocity-ul de început. Prin luna a treia livrau cam la nivelul de dinainte de agent, dar cu rate de defecte mai mari și cu reviewerii seniori vizibil storși.

Echipa B a petrecut prima lună pe practică. AGENTS.md scris și iterat. Skill-uri scrise pentru pattern-urile specifice echipei. Hook-uri configurate. În prima lună n-au livrat nimic condus de agent. În luna a doua au revenit la velocity-ul de bază, cu practica deja pusă la punct. În luna a treia livrau la o calitate și un velocity vizibil mai bune decât înainte de agent. Investiția își arăta efectul compus.

Aceeași companie. Codebase-uri adiacente. Același agent. Diferența a fost disciplina formulării impusă devreme. Costul: o primă lună lentă. Beneficiul s-a întors pe parcursul trimestrului. A fost o observație de teren pe mai multe echipe, nu un experiment controlat. Contrastul a fost însă destul de clar încât să schimbe felul în care predau adopția - cu mențiunea că două echipe adiacente din aceeași companie nu sunt eșantioane independente.

---

Cel mai dur test al tezei din acest capitol a venit între februarie și aprilie 2026, când o serie de schimbări de produs în Claude Code au degradat semnificativ munca de inginerie complexă, în anumite workflow-uri. Alarma a venit din afară: la începutul lui aprilie, un senior director de la AMD, Stella Laurenzo, a publicat un audit pe 6.852 dintre propriile sesiuni de Claude Code și 234.760 de tool call-uri, care arăta modelul trecând de la un comportament research-first la unul edit-first pe măsură ce ascunderea (redaction) thinking-ului a crescut de la 1,5% la 100% din tururi - și indica drept cauză contributoare rollout-ul din februarie al lui adaptive thinking activat implicit. Post-mortem-ul tehnic al Anthropic, publicat pe 23 aprilie, a recunoscut trei regresii din aceeași fereastră: effort-ul implicit coborât în tăcere de la high la medium pe 4 martie (revenit pe 7 aprilie), un bug de caching din 26 martie care golea istoricul de raționament la fiecare tur în loc de o dată pe oră de inactivitate (reparat pe 10 aprilie) și un plafon de verbozitate în system prompt din 16 aprilie, care a produs o scădere măsurată de 3% a calității (revenit pe 20 aprilie).

*Notă despre surse. Auditul lui Laurenzo precedă post-mortem-ul, iar atribuirea degradării către rollout-ul de adaptive thinking din februarie merge dincolo de ce recunoaște post-mortem-ul Anthropic din 23 aprilie - cele două relatări coincid pe regresiile din martie-aprilie și diverg pe cauza din februarie. Tratează magnitudinea analizelor externe ca aproximativă. Citările, în Anexa C.*

Am urmărit două echipe adiacente în perioada respectivă. Prima își petrecuse trimestrul anterior construind infrastructura descrisă în acest manual: CLAUDE.md cu reguli specifice echipei, plan mode activat implicit, bucla în șase faze pentru orice muncă netrivială, hook-uri care interceptau operațiunile distructive. A doua echipă folosea același Claude Code, aceleași modele, aceleași planuri, dar le rula ca dispatch în freestyle. Velocitatea celei de-a doua echipe s-a înjumătățit peste noapte când modelul a început să taie pe scurtătura edit-first. Velocitatea primei echipe a scăzut poate cu 10% și și-a revenit în clipa în care au strâns gate-urile de plan mode și au trecut câteva skill-uri pe effort mai mare ca setare implicită.

Ăsta a fost experimentul rulând în producție. Echipele cu disciplină au absorbit mare parte din regresie. Echipele fără au resimțit imediat toată schimbarea de comportament, au pierdut săptămâni de avânt și au dat vina pe tool. Metodologia nu e o poliță de asigurare împotriva unei perioade proaste a modelului. E diferența dintre un agent care îți e coleg util și un agent care devine un risc în ziua în care vendorul livrează o regresie.

---

Dacă reții un singur lucru din acest capitol, reține-l pe ăsta: costul impunerii rigorii se plătește în prima lună. Beneficiul se încasează tot restul timpului. Matematica e de partea ta - dacă supraviețuiești primei luni.

---

O observație conexă, pentru că pe mine m-a costat timp până am învățat-o.

Practica nu trebuie să fie perfectă ca să înceapă să producă beneficii. Un AGENTS.md de cincisprezece linii e semnificativ mai bun decât niciun AGENTS.md. O notă de research pe jumătate terminată e semnificativ mai bună decât nicio notă de research. Un plan de două task-uri care ratează trei lucruri e semnificativ mai bun decât niciun plan. Perfect e dușmanul lui început.

Echipele care se blochează sunt deseori cele care încearcă să construiască workflow-ul agentic perfect înainte să-l ruleze. Vor AGENTS.md-ul exhaustiv, setul complet de skill-uri, configurația de hook-uri întreagă, înainte să livreze măcar un story condus de agent. Se îneacă în setup. Nu mai încep niciodată. Setup-ul se umflă până umple tot timpul disponibil, pentru că mereu mai e o regulă de adăugat, încă un skill de scris, încă un hook de configurat.

Începe cu practica minimă viabilă. Un schelet de AGENTS.md, cincisprezece linii, care prinde lucrurile despre care știi deja că sunt periculoase. Treci câteva story-uri prin agent. Observă ce merge prost. Adaugă regulile care ar fi prevenit exact acele eșecuri. Iterează. Practica crește din eșecuri reale, nu din unele imaginate. Și crește mai repede, pentru că fiecare regulă și-a câștigat locul.

---

Capitolul următor e forma operațională a practicii. Șase faze. Research, Plan, Execute, Review, Verify, Ship. Fiecare fază e un tip specific de muncă pe care agentul îl face bine când e formulat corect. Fiecare fază produce un artefact pe care îl poți revizui, îl poți pune într-un commit și îl poți audita. Bucla întreagă e echivalentul SDLC-ului pentru o singură modificare - Research e culegerea de cerințe, Plan e design-ul, Execute e implementarea, Review e code review-ul, Verify e testarea, Ship e deployment-ul.

Dacă ți-ai dorit vreodată un inginer junior care să urmeze procesul echipei absolut de fiecare dată - să nu sară niciodată peste pasul de design, să nu livreze niciodată fără teste, să nu închidă niciodată un story fără verificare - bucla în șase faze e răspunsul. Agentul va urma procesul dacă tu codifici procesul sub formă de cod. Plugin-ul la care ne uităm în capitolul următor exact asta face.

Dar mai întâi, un moment despre ce nu sunt cele șase faze.

Nu sunt singurul mod de a face livrare cu agenți. Există framework-uri concurente - Spec Kit de la GitHub, metodologii în stil BMAD, colecții de skill-uri pe care echipele și le construiesc singure. Le voi numi din nou în acest capitol și în următorul, pentru că lecția nu e „folosește acest plugin anume”. Lecția e bucla iterativă în sine. Plugin-ul e doar vehiculul; disciplina e ce călătorește.

Nu sunt nici un proces universal, bun pentru orice. Un bugfix de două linii nu are nevoie de toate cele șase faze. Un update trivial de documentație nu are nevoie de toate cele șase faze. Bucla în șase faze e pentru genul de schimbări la care câștigul adus de rigoare justifică fricțiunea - de regulă, orice atinge logică de business, modifică structuri de date, schimbă contracte de API sau afectează mai mult de câteva fișiere. Decizia despre ce muncă trece prin bucla completă și ce muncă sare peste ea face parte, ea însăși, din practică.

Nu sunt nici capătul muncii. Agentul livrează un pull request. Pull request-ul trece prin review-ul normal al echipei tale. Oamenii se uită pe diff. Oamenii aprobă. Oamenii fac merge. Agentul nu înlocuiește procesul de livrare existent al echipei; agentul îl alimentează.

Să trecem la cele șase faze.

---

**Artefact: euristica de potrivire a task-ului.** Trei întrebări per task: atinge mai mult de trei fișiere, taie prin mai multe straturi, depășește ce ai tasta pur și simplu de mână? Dacă niciuna - sari peste buclă; dacă oricare dintre ele - rulează-o.

---

**De pus în practică săptămâna asta.**

Ia un task pe care erai gata să-l dai agentului. Scrie o notă de research de 200 de cuvinte înainte de dispatch. Observă ce lucruri scoate nota la suprafață, la care nu te gândiseși. Apoi dă-i drumul.

---

## Capitolul 5
## Bucla în șase faze

### Ce este bucla agentică în șase faze? {#what-is-the-six-phase-loop}

Cele șase faze sunt Research, Plan, Execute, Review, Verify și Ship. Fiecare fază e un skill, în sensul anatomiei agentului - un set împachetat de instrucțiuni pe care agentul îl încarcă atunci când faza e activă. Fiecare fază are un input clar, un output clar și o predare clară către faza următoare.

Fiecare fază e gândită să aibă un gate la graniță. Implementarea concretă de azi din Superpowers folosește instrucțiunile din skill ca să ceară disciplina; pentru un gating impus strict, s-ar putea să trebuiască să cablezi un hook PreToolUse specific proiectului. Impunerea fazelor la nivel de kernel e încă în curs de maturizare la mijlocul lui 2026.

```
   +--------+    +------+    +---------+    +--------+    +--------+    +------+
   |Research|--->| Plan |--->| Execute |--->| Review |--->| Verify |--->| Ship |
   +--------+    +------+    +---------+    +--------+    +--------+    +------+
       ^                          |              |
       |                          v              v
       +--- plan eșuat? --- replanifici     verify picat? --- înapoi la plan
```

*Figura: Bucla în șase faze. Cele mai multe eșecuri se întorc la Plan, nu la Research.*

Voi parcurge fazele în ordine, iar la final îți voi arăta cum arată totul când rulează cap-coadă pe o bucată reală de muncă.

Un principiu străbate toate cele șase faze: un rezultat bun are nevoie de o țintă bine definită. Agentul poate construi aproape orice îi descrii, dar nu poate ști la care lucru te-ai referit - a defini asta e treaba primelor faze ale buclei și e exact ce numesc fazele de mai târziu „spec-ul” și „intenția”. Research fixează ce poate și scoate la suprafață ce nu poate; tu tranșezi întrebările deschise pe care le ridică; planul transformă rezultatul stabilit în verificări per task; verify măsoară ce s-a construit față de el. Rezultatul ăsta nu-l ai complet înainte să începi - e un output al research-ului și al planului, șlefuit de fiecare dată când un verify picat se întoarce la Plan, iar pentru munca cu adevărat nouă definești ce poți și lași research-ul să închidă restul. Sari peste definire și restul buclei n-are pe ce se sprijini: review-ul n-are niciun spec cu care să compare diff-ul, verify n-are ce verifica, iar „gata” e orice a decis agentul.

---

**Faza întâi: Research.**

Agentul citește codebase-ul și produce o notă de research care stabilește starea curentă, numește fișierele relevante, identifică pattern-urile existente și semnalează riscurile. Input: descrierea task-ului. Output: un document markdown de două până la patru pagini.

Ce intră în nota de research? Fișierele care vor fi atinse. Convențiile pe care le urmează acele fișiere. Testele existente care acoperă zona. Concepte înrudite din alte părți ale codebase-ului care ar putea fi relevante. Întrebările deschise ale agentului - locurile în care codebase-ul e ambiguu și unde trebuie să decidă un om. Astea nu sunt fire rămase în aer. Sunt deciziile care definesc cum va arăta „gata”, scoase la suprafață acum ca să le tranșezi înainte ca planul să se lege de ele.

Research e faza peste care echipele sar cel mai des, pentru că nu produce cod și pare overhead. Research e și faza care, din experiența mea, are cel mai mare levier din toată bucla. O notă de research proastă garantează un plan prost, care garantează o implementare proastă. O notă de research bună face restul buclei mult mai ușor, pentru că planul e ancorat în starea reală a codului, nu în prima ipoteză a agentului despre starea codului.

Artefactul de research e durabil. Ajunge în commit alături de modificare. Șase luni mai târziu, când alt developer lucrează pe cod adiacent și vrea să știe „de ce e structurat lucrul ăsta așa”, nota de research e acolo. E memoria instituțională pe care echipa n-o avea înainte.

---

**Faza a doua: Plan.**

Agentul citește nota de research și produce un plan la nivel de fișier. Fiecare task din plan numește fișierul de modificat, modificarea de făcut și verificarea care dovedește că modificarea a funcționat. Fiecare task e dimensionat la două-cinci minute de muncă - destul de mic încât un eșec să fie recuperabil, destul de mare încât overhead-ul comutării între task-uri să nu domine.

Planul numește și ce teste trebuie adăugate sau actualizate. Dacă planul nu pomenește de teste, planul e incomplet și agentul se întoarce la treabă. Ideea e ca regula asta să fie impusă printr-un hook; instrucțiunile din skill cer rigoarea, iar impunerea strictă e ceva ce cablezi tu, per proiect, pe măsură ce maturitatea echipei o justifică.

Planul spune și ce înseamnă „gata” pentru întreaga modificare - rezultatul față de care va măsura verify - nu doar verificările per task. Un plan care numește fișiere, task-uri și teste, dar nu spune niciodată ce ar trebui să obțină modificarea, a descompus munca fără s-o definească; contractul outer-loop din Anexa B.6 impune o linie „Done când” la nivelul buclei exterioare, iar bucla interioară are nevoie de același lucru la scara unei singure modificări.

Planul e gate-ul unde un reviewer uman contează cel mai mult. Citești planul. Respingi task-urile prea vagi, prea mari sau prost ordonate. Adaugi task-urile pe care planul le-a ratat. Scoți task-urile care ies din scop. Agentul revizuiește. Tu aprobi. Abia apoi începe execute.

Review-ul de plan ia câteva minute. Te scutește de o după-amiază pierdută în ziua în care planul era greșit și ai fi descoperit asta abia în execute - de unde e mult mai greu de dat înapoi.

---

**Faza a treia: Execute.**

Aici își câștigă pâinea componenta principală recursivă din Capitolul 1 - subagenții. Execute e faza în care orchestratorul trimite în lucru mai mulți agenți-copil constrânși, fiecare lucrând la un task delimitat, în propriul context izolat.

Agentul trimite câte un subagent per task. Fiecare subagent lucrează în propriul context izolat - o trăsătură arhitecturală cheie, pentru că contaminarea contextului e cel mai mare motiv pentru care sesiunile lungi de agent o iau razna. Raționamentul confuz din task-ul unu nu poluează foaia curată a task-ului patru. Fiecare subagent citește doar ce are nevoie, face modificarea care i-a fost atribuită, rulează pasul de verificare din plan și raportează înapoi. Agentul-orchestrator asamblează rezultatele.

Execute e faza care produce cod vizibil pe ecran. E și faza care beneficiază cel mai mult de izolare. Fără izolarea subagenților, o schimbare cu opt task-uri într-o singură sesiune de agent se termină cu un context window îndesat cu codul a opt task-uri, rezultate parțiale, output de debugging și un agent care ia decizii în task-ul șapte pe baza unei amintiri deformate a deciziilor din task-ul doi. Cu izolare, fiecare task pornește proaspăt. Fiecare task e mic. Fiecare task reușește sau eșuează pe propriile merite.

Dacă un task eșuează, orchestratorul decide dacă reîncearcă, ocolește eșecul sau se oprește și întreabă omul. Cele mai multe eșecuri sunt recuperabile - prima încercare a agentului a ratat un detaliu pe care nota de research îl semnalase, a doua încercare încorporează corecția. Unele eșecuri sunt blocante - task-ul, așa cum a fost planificat, nu poate fi dus la capăt, iar planul trebuie revizuit. Orchestratorul le deosebește pe cele două.

Ce nu rezolvă izolarea subagenților: contaminarea la nivelul orchestratorului. Orchestratorul tot ține rezumate ale muncii fiecărui subagent, iar dacă rezumatul lui despre rezultatul task-ului unu e imprecis, subagentul task-ului patru poate face o presupunere care contrazice ceva ce task-ul unu chiar a stabilit. Am văzut cu ochii mei o fază de execute cu șase subagenți producând editări reciproc inconsistente exact din motivul ăsta. Izolarea e reală și valoroasă; nu e o soluție-minune. Orchestratorul rămâne un punct unic de context, iar rezumatele lui rămân un loc pe unde se poate strecura deriva. Citește mesajele de predare a task-urilor din orchestrator cu același scepticism cu care ai citi update-urile de standup ale unui inginer junior.

Costul conex e medierea, atunci când subagenți rulați în paralel fac editări conflictuale. Medierea ieftină: orchestratorul detectează că două ramuri au atins același fișier în moduri incompatibile, renunță la ramura mai târzie și o rerulează secvențial, cu output-ul primei ramuri pasat ca context. Medierea scumpă: orchestratorul rezumă schimbările aflate în conflict, cere unui model mai capabil să aleagă merge-ul corect, apoi îl reaplică. Cele mai multe conflicte sunt ieftine. Unele nu sunt, iar cele scumpe mănâncă exact câștigul de viteză pentru care ai paralelizat.

Costul de coordonare apare ca mediere de conflicte - rerularea unei ramuri abandonate, sau plata unui model mai capabil care să aleagă un merge - și e mărginit. Marginea: cu cât task-urile subagenților sunt mai independente, cu atât rata de conflict e mai mică. Modul de a-i ține independenți e să delimitezi pe fișier sau pe modul, nu pe feature. Șase subagenți care editează fiecare câte un fișier - sigur. Șase subagenți care editează toți același feature, pe fișiere care se suprapun - rețeta pentru cazul scump, de fiecare dată. Din experiența mea, echipele care se lovesc de problema asta trimit de obicei prea mulți subagenți pentru cât e de fapt de lucru. Trei subagenți bine delimitați termină mai repede decât opt care se calcă pe picioare, de fiecare dată.

Tot în execute se întâlnește agentul cu guvernanța. Fiecare tool call trece prin gate-ul de permisiuni. Fiecare comandă Bash trece prin hook-urile de securitate. Fiecare scriere de fișier trece prin sandbox. Dacă agentul încearcă ceva ce stratul de guvernanță nu permite, acțiunea e blocată, agentul raportează înapoi orchestratorului, orchestratorul decide cum merge mai departe. Rigoarea trăiește în straturile de sub execute; execute doar rulează munca.

---

**Faza a patra: Review.**

Doi revieweri. În secvență.

Întâi, conformitatea cu spec-ul. Agentul citește nota de research originală, planul aprobat și diff-ul real. Răspunde la o singură întrebare: implementarea corespunde spec-ului? Dacă da, o spune. Dacă nu, semnalează decalajul. Conformitatea cu spec-ul e o competență diferită de calitatea codului. O modificare poate fi cod de calitate care face lucrul greșit. O modificare poate fi cod urât care face exact lucrul corect. Reviewerul de spec se ocupă doar de prima dimensiune.

Apoi, calitatea codului. Un agent diferit. Un prompt diferit. Citește doar diff-ul. Întreabă: e cod bun, după standardele echipei? Naming. Stil. Edge case-uri. Acoperirea cu teste. Tratarea erorilor. Considerații de performanță. Comentează pe diff așa cum ar face-o un reviewer senior.

Motivul pentru care le desparți în doi revieweri e că, făcute simultan, amândouă ies mai prost. Un reviewer care întreabă în același timp „corespunde spec-ului?” și „e bine scris?” tinde să le amestece. Spec-ul ajunge cântărit prin prisma calității codului, sau calitatea codului prin prisma conformității cu spec-ul, și pierzi semnalul distinct pe care trebuia să-l dea fiecare. Doi revieweri, două preocupări, zero amestec.

Output-ul fazei de review e structurat. Fiecare constatare are o severitate. Constatările critice blochează ship-ul. Cele importante se repară înainte de ship. Sugestiile se notează în descrierea PR-ului. Agentul rezolvă automat constatările blocante și pe cele importante (în limitele planului) și scoate sugestiile la suprafață, ca să decidă reviewerul uman.

---

### Cum faci review pe un diff scris de agent? {#reviewing-agent-diffs}

Un diff scris de agent eșuează altfel decât unul scris de om, așa că îl citești în altă ordine. Un diff de om eșuează la execuție - o greșeală de tastare, un off-by-one, edge case-ul pe care autorul l-a uitat - și vânezi greșeala linie cu linie, pentru că acolo o lasă un om obosit. Un diff de agent sosește fără astea. Compilează, trece de lint, se citește ca un cod idiomatic pe care echipa ta l-ar face merge fără niciun comentariu. Eșuează cu un strat mai sus, la intenție și context - o regulă de business plauzibilă și greșită, codul corect pus în stratul greșit - și niciuna dintre astea nu se anunță singură pe pagină. Un bug de agent arată ca acel cod pe care un inginer bun l-ar scrie pentru un task ușor diferit. Fluența nu e corectitudine, iar cititul pe fluență nu-l va prinde.

Așa că petrece primele zece minute deasupra codului, nu în el. Începe cu diff-stat-ul raportat la plan, înainte de o singură linie de implementare: forma schimbării se potrivește cu forma cererii? Un fișier atins pe care planul nu l-a numit niciodată e primul semnal, nu o notă de subsol - un diff care depășește scopul e agentul care decide ceva ce nu i-ai cerut să decidă.

Citește apoi testele, și citește ce afirmă, nu dacă trec. Verdele e cel mai ieftin semnal din diff și cel pe care îl ai deja. Un test care afirmă ce face implementarea în loc de ce cerea intenția va trece și tot va fi greșit; faza de Verify revine la asta, la de ce testele agentului merită o a doua citire.

Apoi verifică granițele despre care echipa ta a scris reguli - pattern-urile interzise din AGENTS.md, convențiile de strat, modulele periculoase de atins. Agentul încalcă o convenție sigur pe el și în stil fluent, așa că o trecere de graniță nu arată greșit; arată curat, exact ce cititul pe stil trece cu vederea. Și dă grep pe fiecare nume nou pe care-l introduce diff-ul - fiecare API, funcție sau cheie de config pe care n-o recunoști - aceeași verificare încrucișată pe care Capitolul 6 o rulează împotriva invenției sigure pe ea, pentru că apelul care nu există se citește la fel de plauzibil ca cel care există.

Abia acum, linie cu linie. Ăsta e stratul mecanic pe care cei doi revieweri de mai sus l-au măturat deja - conformitatea cu spec-ul, calitatea codului - așa că nu le repeți trecerea; cheltuiești minutele pe care ți le-au cumpărat pe cele două lucruri pe care ei nu le pot judeca, corectitudinea de business și potrivirea arhitecturală. Aici iese la suprafață regula de business plauzibilă și greșită, și aici un idiom învechit din versiunea de framework pe care modelul o știe cel mai bine se citește ca un cleanup și ajunge în producție ca o regresie. Citirea nu dispare pe măsură ce tooling-ul se îmbunătățește. Devine mai scurtă și mai ascuțită, țintită pe erorile de intenție care supraviețuiesc tuturor filtrelor din amonte - iar când se degradează în schimb într-o privire fugară la bifele verzi, pattern-ul patru din Capitolul 9 stăpânește ce se întâmplă mai departe.

Anexa B.8 e ordinea asta de citire într-o singură pagină.

---

**Faza a cincea: Verify.**

Faza de Verify e locul unde rulează testele. Mai exact, rulează testele *noi* - testele care exersează modificarea. Suita de teste existentă rulează deja în execute (orice task care modifică cod rulează testele existente relevante, ca să se asigure că nu a stricat nimic). Verify e despre întrebarea dacă modificarea e cu adevărat corectă - corectă față de rezultatul pe care l-ai definit în research și în plan - nu doar dacă testele existente încă trec.

Pentru logica de backend, verify înseamnă de obicei teste unitare și teste de integrare. Planul a numit ce teste trebuie adăugate; faza de Execute le-a adăugat; verify le rulează și raportează rezultatele.

Pentru codul de frontend, verify devine mai interesant. Testarea de frontend a fost dintotdeauna grea - testele de UI sunt fragile, testele snapshot sunt casante, QA-ul manual nu scalează. Workflow-ul agentic are aici un răspuns adevărat, și e unul dintre lucrurile care mă entuziasmează cel mai tare. Răspunsul: Playwright cu accessibility tree.

Playwright cu accessibility tree înseamnă următorul lucru. Playwright e o bibliotecă de automatizare de browser. Pilotează un browser real (headless sau vizibil) printr-o secvență de interacțiuni. Accessibility tree e structura pe care browserele o întrețin pentru tehnologiile asistive - screen readere, control vocal și restul. Accessibility tree descrie pagina în termeni semantici: există un buton cu eticheta asta, există un câmp de formular etichetat „email”, există o listă de elemente cu numele astea. Accessibility tree e stabil. Nu se schimbă când restilizezi pagina, pentru că etichetele și rolurile nu se schimbă. Refactor de CSS? Accessibility tree e același. Schimbi biblioteca de componente? Accessibility tree e același.

Verify, în workflow-ul agentic, scrie teste pe accessibility tree, nu pe pixeli și nu pe selectoare CSS. Testul spune „navighează la pagina de profil a utilizatorului, găsește câmpul etichetat Priority, schimbă-i valoarea, apasă Save, verifică faptul că noua valoare se afișează”. Testul ăsta trece indiferent dacă UI-ul e stilizat cu Tailwind, cu Bootstrap, cu Material sau cu nimic. Testul trece indiferent dacă acel câmp e implementat ca select dropdown, ca radio group sau ca o componentă custom. Testul afirmă *comportamentul* - adică exact ce te interesează.

Rulez asta cu echipe din banking în mod constant. Au în spate istorii lungi de automatizări de teste UI eșuate - teste flaky, suite casante, ingineri juniori care pierd săptămâni vânând diff-uri de snapshot. Pattern-ul cu accessibility tree e primul lucru care, din experiența mea, ține suitele de teste UI verzi luni și ani la rând. Agentul scrie testele. Testele supraviețuiesc refactor-urilor. Echipa are încredere în semnalul verde.

---

### Poți avea încredere în testele scrise de agent? {#trusting-agent-tests}

O suită de teste verde scrisă de agent e un indiciu, nu o dovadă.

E un indiciu că modificarea face ce spune testul. Nu e o dovadă că testul spune ce trebuie. Exemplul lucrat de mai târziu din acest capitol face decalajul concret: task-ul de audit log a livrat un test *care trecea* și care verifica vechiul format de log. Verde - și greșit. Suita era fericită. Comportamentul era incorect. Nimic în afară de Review nu l-a prins, pentru că nimic altceva nu se uita la ce pretindea testul - doar la dacă trece.

Procentul de coverage nu închide decalajul ăsta; îi lărgește iluzia. Coverage-ul măsoară ce linii s-au executat, nu dacă s-a verificat ceva cu sens. Un agent care optimizează pentru un gate de coverage va scrie teste care apelează codul, nu afirmă nimic de substanță și fac cifra verde. Primești metrica, nu și siguranța. Un coverage mare pe teste scrise de agent îți spune că acel cod a rulat în timpul testului. Nu îți spune că acel cod e corect.

Testele de caracterizare au aceeași formă de limitare, numită în Capitolul 8: fixează *comportamentul* curent, nu corectitudinea. Sunt cu adevărat valoroase - o plasă de siguranță contra regresiilor, care îi permite agentului să refactorizeze fără să schimbe pe tăcute ce face codul. Dar vor conserva un bug la fel de fidel cum conservă un feature. O suită de caracterizare care e verde după un refactor demonstrează că nu ai schimbat comportamentul. Nu spune nimic despre dacă acel comportament a fost vreodată corect.

Așa că disciplina e cea evidentă, aplicată acolo unde echipele uită s-o aplice: fă review pe testele agentului cu aceeași seriozitate cu care faci review pe codul agentului. Citește ce afirmă testele, nu doar dacă trec. Mai ales pentru logica de backend, un om sau un al doilea agent ar trebui să verifice aserțiunile față de spec - față de ce *trebuie* să facă acel cod - nu față de implementarea care se nimerește să le stea în față. Un test scris pornind de la implementare va fi de acord cu implementarea. Exact ăsta e modul de eșec. Aserțiunea trebuie să vină din intenție.

---

**Faza a șasea: Ship.**

Ship e faza care produce artefactul pe care îl preia procesul normal de review al echipei tale. Agentul face commit cu un mesaj structurat. Dă push pe branch și deschide un pull request cu o descriere structurată: ce s-a schimbat, de ce, cum s-a verificat, ce riscuri rămân, ce revieweri sunt etichetați. Dacă la început a fost legat un ticket de Jira, agentul actualizează ticketul. Dacă notificările de Slack sunt cablate, agentul postează pe canalul relevant.

Ship durează treizeci de secunde. E faza cea mai ușoară. E și faza care face restul buclei digerabil pentru echipă, pentru că *artefactul* produs de agent - pull request-ul - e exact artefactul pe care echipa e deja obișnuită să-l revizuiască. Nu există o „bandă specială pentru AI” în repository-ul tău. Există același proces de review de PR prin care trece orice modificare. Reviewerul citește diff-ul, citește descrierea, citește nota de research din linkul atașat descrierii, citește rezultatele testelor, aprobă sau cere modificări. Ca de obicei.

Asta e proprietatea care face ca livrarea cu agenți să funcționeze în practică. Agentul nu îți rupe procesul existent. Agentul îți alimentează procesul existent cu muncă mai bine formulată.

---

Bucla completă, pe un feature mic, ia în jur de douăzeci-treizeci de minute de timp total, cu ceas. Pe un feature mediu, o oră. Pe unul mare, câteva ore - iar feature-ul mare ar fi luat zile fără agent, deci comparația e în favoarea ta.

Totalul include și timpul de procesare al agentului, și timpul tău de review la gate-urile umane. Agentul în sine rulează poate o treime până la jumătate din timpul total; restul ești tu citind nota de research, tu revizuind planul, tu aprobând diff-ul, tu privind cum trece pasul de verify. Gate-urile umane sunt limitatorul de ritm într-un workflow sănătos, nu agentul. Dacă bucla ta ia trei ore pe un feature mic, problema e aproape sigur că gate-urile sunt supra-inginerite sau că le faci într-un du-te-vino lent în loc de o singură trecere concentrată. Agentul nu te salvează de propria cultură a ședințelor.

Fricțiunea față de „lasă pur și simplu agentul să scrie codul” e timpul de gate - nota, planul, review-ul de diff - și e mărginită. Beneficiul față de „livrează cod fără rigoare” e substanțial.

---

Timpii buclei la repetiție nu sunt timpii buclei în producție. Am învățat asta dintr-un demo pe care l-am rulat pentru echipa unui client la începutul acestui an. Planul demo-ului prevedea o rulare de architecture review care producea un raport HTML dintr-un repo proaspăt în aproximativ patru minute. La repetiție, cu [AGENTS.md](https://agents.md/)-ul agentului pre-încărcat și cu căile din repo deja în cache, patru minute erau fezabile. Prima încercare live, în fața echipei, a luat opt minute per pane și a pornit un cronometru pe răbdarea publicului pe care îl simțeam ticăind din fața sălii. A doua încercare live, două zile mai târziu, în altă sală, a luat zece minute.

Pattern-ul nu era un bug. Era diferența previzibilă dintre o rulare cu cache cald și una pornită la rece. Disciplina pe care ar fi trebuit s-o construiesc în planul demo-ului de la bun început e aceeași disciplină pe care o predă capitolul ăsta: presupune că variabila contează, planifică pentru timpii cei mai proști, ai un fallback pregătit pentru momentul în care sistemul live îți spulberă bugetul. Pattern-ul de recuperare pe care îl folosesc acum la fiecare demo are două straturi: un artefact de fallback pre-generat, într-un branch de git pe care îl pot scoate cu un checkout în două secunde, și o sesiune reluabilă, pe care o pot continua din starea de la repetiție dacă sesiunea live îngheață. Niciunul nu e spectaculos. Amândouă au eliminat modul de eșec al demo-urilor live pe care îl tot improvizam de un an.

---

**Un exemplu lucrat.**

Ca să facem bucla concretă, iată un feature care curge prin toate cele șase faze. Feature-ul e mic: adaugă un câmp `priority` pe recordul `Wire`, într-un serviciu bancar reglementat. Priority e una dintre valorile low / normal / high / urgent, are default normal, iar flag-ul urgent declanșează un queue separat de compliance review.

**Research.** I-am cerut agentului să citească codebase-ul și să producă o notă de research. Nota a numit patru fișiere pe care nu le-aș fi găsit nici într-o oră de grep: recordul `Wire` în sine, directorul de migrații, serviciul queue-ului de compliance review și emitter-ul de audit log. A ridicat și o întrebare deschisă: priority să fie enum sau text liber, dat fiind că spec-ul reglementatorului folosește text liber în unele documente și enum în altele. Am ales enum. Alegerea asta nu era un detaliu - definea ținta față de care fazele de mai târziu aveau să verifice modificarea.

**Plan.** Agentul a produs un plan de șase task-uri, în ordine: adaugă coloana în baza de date, cu default; actualizează clasa recordului `Wire`; actualizează serviciul wire-builder; actualizează contractul de API; actualizează logica de rutare pe compliance ca să citească noul câmp; actualizează emitter-ul de audit log. Fiecare task era constrâns la un fișier sau la o pereche de fișiere. La review am prins o singură chestiune: task-ul cinci depindea de schimbarea de contract de API din task-ul patru, dar ordinea era corectă și agentul marcase dependența în descrierea task-ului. Aprobat.

**Execute.** Șase subagenți în paralel, câte unul per task, fiecare constrâns la fișierul lui. S-au întors în mai puțin de trei minute. Cinci task-uri au avut teste care treceau din prima. Al șaselea (emitter-ul de audit log) avea un test care trecea, dar testul era greșit - verifica vechiul format de log. Prins la Review.

**Review.** Reviewerul de conformitate cu spec-ul a prins faptul că testul task-ului de audit log verifica vechiul format. A semnalat și că migrației îi lipsea direcția de down. Reviewerul de calitate a codului n-a găsit nimic notabil. Subagentul implementator a reparat ambele puncte și a rerulat testele relevante.

**Verify.** Agentul a rulat suita completă de teste (3.400 de teste), un smoke test pe serviciul de rutare compliance din staging și a produs un diff al schimbării de contract de API pentru review-ul reglementatorului. Toate verzi. Timp total de agent: 47 de minute, de la research la verify.

**Ship.** PR deschis cu nota de research, planul, rapoartele per task, review-urile de conformitate cu spec-ul și de calitate a codului și dovezile din teste atașate. Reviewerul senior a petrecut unsprezece minute pe PR, a pus o singură întrebare (dacă flag-ul urgent ar trebui să fie vizibil în dashboard-ul de metrici - lucru la care nu mă gândisem) și a aprobat. Merged. Tot feature-ul, de la „hai să adăugăm un câmp de prioritate” la cod în merge, a luat nouăzeci de minute de ceas, cumulat între agent și mine.

Nouăzeci de minute, nu cele douăzeci sau treizeci pe care le citam pentru un feature mic - diferența e contextul reglementat: o suită de 3.400 de teste, un smoke test pe staging și un diff de contract pentru reglementator. Mic ca scop nu înseamnă mic ca ceremonie. Și tot nu minutele sunt ideea; artefactele sunt. Fiecare pas a produs ceva ce un reviewer senior poate audita. Bucla e disciplina care convertește capabilitatea agentului în muncă pe care o pot apăra.

---

Toată bucla, dintr-o privire:

| Faza | Artefactul | Gate-ul uman | Eșecul prins |
|---|---|---|---|
| Research | Nota de research (2-4 pagini) | Verificare de plauzibilitate pe domeniu | Context lipsă |
| Plan | Plan de task-uri la nivel de fișier | Review de scop și ordine | Descompunere proastă |
| Execute | Diff + rapoarte per task | Niciunul sau lejer | Drift de implementare |
| Review | Rapoarte de conformitate cu spec-ul + calitate | Review de senior | Cod greșit sau slab |
| Verify | Dovezi din teste (failing -> passing) | Review de QA sau de owner | Eșec comportamental |
| Ship | PR cu lanțul de dovezi | Procesul normal de PR | Încălcare de proces |

---

**Sidebar: echipa care a livrat cu jumătate de buclă.**

Ceremonia completă nu e mereu doza potrivită, iar dacă aș pretinde contrariul, mi-ai retrage încrederea prima dată când ai vedea o echipă prosperând fără ea. O echipă pe care am urmărit-o a rulat livrare cu agenți aproape un an cu ceea ce părea jumătate de buclă. Research-ul era un fir de comentarii pe ticket. Planul era trei bullet-uri în descrierea PR-ului. Fără note de research, fără agenți de review, fără gate-uri formale. Velocitatea a crescut. Defectele nu.

A funcționat datorită a trei condiții, iar condițiile sunt lecția. Echipa era mică, senioră și își construise singură codebase-ul, deci funcția de research era aproape gratuită - contextul pe care o notă de research există ca să-l asambleze era deja în capetele lor. Suita de CI era cu adevărat strictă, deci funcția de verify rula la fiecare push, fie că o numea cineva fază, fie că nu. Iar cultura de PR era deja serioasă, deci review-ul se întâmpla, cu discernământ, pentru că așa fusese dintotdeauna.

Uită-te la lista aia: research, verify, review. Funcțiile n-au dispărut. Erau construite în pereții echipei, așa că forma explicită era redundantă. Asta e lectura onestă a buclei - nu e un preț pe care îl plătești ca să folosești agenți; e forma explicită a șase funcții care trebuie să se întâmple undeva. O echipă care a mutat o parte din funcții în pereții ei - în infrastructură, în cultură - poate merge mai lejer exact acolo, și nicăieri altundeva.

Testul e contabilitate, nu optimism. Pentru fiecare fază peste care vrei să sari, numește lucrul care îi face deja treaba. Dacă nu-l poți numi, faza rămâne.

---

O precizare de vocabular înainte să mergem mai departe, pentru că termenul „buclă” începe să fie suprasolicitat în domeniu. Cele șase faze de aici sunt bucla interioară (inner loop): o unitate de muncă, șase funcții, cu gate-uri ținute de tine. Mai există și o buclă exterioară (outer loop), tot mai răspândită - reinvocarea agentului la interval sau pe un queue, fără nimeni între iterații, până când o condiție e îndeplinită. Acela e un instrument diferit, cu precondiții diferite, și e pattern-ul final din Capitolul 9. Dependența curge într-un singur sens: o buclă exterioară e exact atât de sigură cât e mecanizarea funcțiilor pe care le rerulează, pentru că ea compune orice disciplină - sau orice absență - pe care o împachetează.

---

### Igiena contextului {#context-hygiene}

Fiecare fază din bucla asta rulează înăuntrul unui context window, iar fereastra e memoria de lucru a agentului. Tot ce e încărcat în ea - system prompt-ul, fișierele citite, rezultatele tool-urilor, conversația de până acum - concurează pentru aceeași atenție mărginită de care agentul are nevoie ca să raționeze. Capitolul 1 a numit limita și a spus că ferestrele mai mari doar ridică plafonul; igiena contextului e cum lucrezi înăuntrul ei. Capitolul ăsta a numit deja contaminarea contextului drept cel mai mare mod de eșec al sesiunilor lungi. Asta e practica ce o previne.

Prima disciplină e să încarci ce cere task-ul și să faci referire la rest. Pointere, nu payload-uri. Documentul de arhitectură e pus ca link în AGENTS.md, nu lipit în el; nota de research numește fișierele care contează și unde să le găsești, în loc să le pună conținutul inline. Bugetul de două sute de linii pentru AGENTS.md din Capitolul 6 e aceeași disciplină aplicată stratului mereu-încărcat - liniile care se încarcă la începutul fiecărei sesiuni sunt spațiul cel mai scump din fereastră, așa că ori își merită locul, ori dispar.

Granița dintre sesiuni e instrumentul. O unitate de muncă per sesiune. Artefactele pe care bucla asta le trece în commit - nota de research, planul, rapoartele per task - există tocmai ca sesiunea următoare să pornească curată și să citească din repository starea de care are nevoie, în loc să târască după ea istoricul cât o conversație întreagă. Context proaspăt per unitate de muncă e forma din bucla interioară a ceea ce face pattern-ul opt la fiecare iterație; argumentul buclei exterioare e al Capitolului 9.

Contaminarea se anunță singură, dacă stai cu ochii pe ea. Patru semne. Agentul răspunde din nou la o întrebare pe care o rezolvase deja mai devreme în sesiune. Citează o versiune învechită a unui fișier pe care l-a editat acum o oră. Uită o constrângere pe care o respecta acum douăzeci de minute. Editările lui devin tot mai neglijente pe măsură ce sesiunea se lungește. Când vezi asta, nu te certa cu sesiunea - nu poți readuce un context window la coerență prin dispută. Dă commit la starea durabilă, încheie sesiunea, pornește curat. Sesiunea proaspătă nu e progres pierdut; e chiar progresul, recitit din repository, fără zgomot.

Compactarea e o predare, nu o continuare. Când harness-ul rezumă o fereastră plină ca să facă loc, pierde detalii - asta înseamnă să rezumi - așa că tratează o sesiune compactată așa cum ai trata predarea muncii tale unui inginer nou în prag: tot ce contează și nu e scris într-un fișier până atunci s-a pierdut. Subagenții sunt cealaltă jumătate a instrumentului, izolând fiecare task în propria lui fereastră, ca confuzia unui task să nu ajungă niciodată la următorul. Rezumatele lor de predare se citesc cu același scepticism pe care faza de execute îl cere deja pentru cele ale orchestratorului.

Anexa B.7 e disciplina asta într-o singură pagină.

---

Plugin-ul Superpowers la care am tot făcut referire e o implementare a buclei interioare. Există și altele - Spec Kit de la GitHub, framework-uri BMAD, colecții de skill-uri construite de echipe pentru uz propriu. Diferă în detalii. Împărtășesc pattern-ul buclei iterative. Alege ce se integrează cu workflow-ul tău, cu tool-urile tale, cu constrângerile tale de conformitate. Vehiculul contează mai puțin decât disciplina.

Capitolul următor: artefactul care face disciplina portabilă între membrii echipei, între repository-uri și în timp. AGENTS.md.

---

**Artefact: tabelul artefactelor per fază.** Cele șase rânduri din acest capitol, lipite deasupra review-board-ului echipei: Nota de research, Planul la nivel de fișier, Diff + rapoarte per task, Rapoartele de review, Dovezile din teste, PR-ul cu lanțul de dovezi.

---

**De pus în practică săptămâna asta.**

Treci un feature prin bucla completă în șase faze. Cronometrează fiecare fază. Notează care faze au mâncat cel mai mult timp de ceas și care au produs cea mai multă valoare. De multe ori, nu sunt aceleași.

---

## Capitolul 6
## AGENTS.md ca infrastructură de echipă

---

### AGENTS.md vs CLAUDE.md: care e diferența? {#agents-md-vs-claude-md}

**Nume și convenții.** Standardul neutru față de vendor pentru fișierul de instrucțiuni al echipei este `AGENTS.md`, cu suport nativ în Codex CLI, Cursor, GitHub Copilot, Gemini CLI, Aider, Zed, Windsurf și altele. Varianta specifică Claude Code este `CLAUDE.md`. Formatul e markdown în ambele cazuri; semantica de încărcare e echivalentă. Dacă ai ajuns la capitolul ăsta dinspre ecosistemul Claude Code, citește `AGENTS.md` ca „fișierul pe care agentul tău îl citește la începutul sesiunii” - disciplina pe care o predă capitolul e identică, indiferent de numele fișierului. Acolo unde manualul discută comportament specific Claude Code, folosesc `CLAUDE.md`; în rest folosesc numele vendor-neutral.

---

AGENTS.md este stratul definit manual al componentei principale Memory, numit în Capitolul 1. E suprafața care se partajează în echipă - stratul pe care echipa îl scrie, îl dă la review și îl deține în source control. Sistemul de memorie automată (Auto Memory, Dreaming) e per developer și în mare parte automat; capitolul ăsta se concentrează pe stratul deținut manual, pentru că acolo trăiește disciplina la nivel de echipă. Urmează cele șase lucruri care intră în AGENTS.md, regula bugetului de 200 de linii și modurile de eșec pe care le vezi în practică.

---

O echipă cu care am lucrat anul trecut folosea un coding agent de șase luni când un senior engineer a venit la mine cu o nemulțumire. „De fiecare dată când generăm un endpoint de API, trebuie să repar validarea. Mereu aceeași corecție. Agentul pune validarea în stratul greșit.”

Am pus întrebarea evidentă. „De ce nu e regula scrisă undeva?”

Pauză lungă. „N-am scris-o niciodată. Doar o tot reparăm.”

Așa că am făcut socoteala împreună. În ultima lună, agentul generase douăsprezece endpoint-uri noi. Același senior engineer mutase validarea din stratul de controller în stratul de service în unsprezece din cele douăsprezece. Pierduse poate cincisprezece minute pe fiecare corecție, cu tot cu dus-întorsul din review-ul PR-ului. Trei ore din luna lui, în fiecare lună, pe aceeași corecție. Echipa înghițise costul ăsta ca parte din „munca normală de review” și încetase să-l mai observe.

Am scris o singură linie în [AGENTS.md](https://agents.md/): „Adnotările Bean Validation stau pe DTO-uri, la granița controller-ului; metodele din stratul de service au încredere în input-urile lor.” Am adăugat-o și în template-ul de pull request al echipei, ca reminder pentru revieweri. Am marcat endpoint-urile existente care erau deja corecte ca exemple de referință.

Următoarele douăsprezece endpoint-uri: zero corecții pe stratul de validare. Trei ore pe lună de timp de senior engineer, eliminate de o singură linie de configurare. Regula nu a făcut agentul perfect; a eliminat acea corecție anume, repetată la nesfârșit.

AGENTS.md e ceea ce transformă „agentul face întruna greșeala asta” în „agentul nu mai face greșeala asta”. E infrastructură de echipă în același sens în care script-urile de build sunt infrastructură de echipă - cod versionat în repo, pe care echipa îl întreține pentru că echipa se bazează pe el.

---

Există și un mod de eșec al AGENTS.md care e inversul poveștii de succes de mai sus. O echipă de banking cu care am lucrat la începutul lui 2026 avea un AGENTS.md care crescuse în șase luni până pe la nouă sute de linii. Fiecare PR care scotea la iveală un edge case nou năștea o regulă nouă. Fiecare retro de echipă adăuga o convenție nouă. Fișierul era cuprinzător, bine organizat și întreținut riguros. Și totuși nu mai funcționa. Agentul începuse să ignore tocmai regulile la care echipa ținea cel mai mult - chiar regulile adăugate în sprint-urile cele mai recente -, pentru că, pe context lung, calitatea cu care modelul respectă instrucțiunile scade uniform pe măsură ce crește numărul lor. Cele mai importante reguli ale echipei se înecau în propria lor meticulozitate.

Soluția n-a avut nimic spectaculos. Am tăiat AGENTS.md de la nouă sute de linii la nouăzeci. Convențiile specifice proiectului care nu trebuiau încărcate la fiecare sesiune le-am mutat în skill-uri care se activează la detecție. Documentarea greșelilor din trecut am mutat-o în documentul de arhitectură, unde trăia ca proză, nu ca instrucțiuni. Rata de conformare pe regulile rămase a sărit în sus într-o săptămână. Pattern-ul pe care îl predau acum: dacă AGENTS.md-ul tău a trecut de două sute de linii, fișierul nu devine mai util, devine tot mai ignorat. Taie-l, mută materialul în skill-uri și tratează regulile care supraviețuiesc ca pe cele care duc greul.

---

### Ce este AGENTS.md? {#what-is-agents-md}

AGENTS.md e un fișier markdown care stă în rădăcina repository-ului. Agentul de cod îl citește la începutul sesiunii, înainte de orice prompt al utilizatorului. E documentul care transformă „ce i se pare agentului rezonabil” în „ce a convenit echipa ta că e rezonabil”. Fără el, sesiunea de agent a fiecărui developer are altă părere despre cum se scrie cod în codebase-ul tău. Cu el, părerea e a echipei - versionată în git, semnată de autor, verificabilă în pull request.

AGENTS.md e cea mai importantă piesă nouă de infrastructură pentru livrarea susținută cu agenți. O echipă fără AGENTS.md face programare cu agenți așa cum face deployment un startup la început de drum - manual, pe bază de tribal knowledge, din memoria instituțională a unui singur senior engineer care se nimerește să fie în cameră. O echipă cu un AGENTS.md bine întreținut face programare cu agenți așa cum fac deployment organizațiile de inginerie mature - automatizat, repetabil, deținut de echipă, supraviețuind plecărilor din echipă.

---

În AGENTS.md intră șase lucruri. Le iau pe rând, cu exemple concrete din codebase-uri de banking, pentru că acolo îmi fac cea mai mare parte din muncă.

**Unu: pattern-urile interzise.** Lucruri pe care agentul nu are voie să le facă niciodată. Fiecare e o singură linie. Fiecare are un motiv de o linie.

> Nu construi niciodată SQL prin concatenare de string-uri. Folosește întotdeauna parametri legați (bound parameters). (Motiv: un SQL injection pe query-urile de clienți e un incident vizibil pentru autoritatea de reglementare.)
> Nu loga niciodată câmpuri PII - nici pe cele evidente (număr de cont, CNP), nici compozitele mai puțin evidente (nume complet plus data nașterii). (Motiv: GDPR, articolul 5(1)(c), minimizarea datelor.)
> Nu-ți implementa niciodată propria criptografie. Folosește wrapper-ul cripto aprobat al echipei, `com.bank.crypto.SecureCrypto`. (Motiv: în 2024 am livrat în producție AES-CBC cu IV hardcodat; nu repetăm experiența.)
> Nu modifica niciodată istoricul migrărilor de bază de date. Migrările sunt append-only. (Motiv: rollback-ul unei migrări modificate corupe schema în moduri ireversibile.)

Fiecare pattern interzis e un zid pe care agentul nu-l trece. Dacă agentul crede că regula e greșită într-un caz anume, va semnala dezacordul în răspunsul lui - iar echipa fie explică excepția, fie actualizează regula.

**Doi: jurnalul de greșeli.** Un log al eșecurilor pe care echipa chiar le-a văzut, fiecare cu regula care previne repetarea. Exemplu:

> 2026-03-03: am livrat un bug în care agentul a generat un query JPQL care ocolea filtrul multi-tenant. Cauza-rădăcină: promptul nu menționa multi-tenancy; agentul a presupus single-tenant. Fix: query-urile extind acum clasa de bază `MultiTenantQueryBuilder`, care impune filtrarea pe tenant. Regulă adăugată.

Jurnalul de greșeli crește în timp. Și se curăță periodic: intrările rezolvate structural (problema de fond nu mai e posibilă) se șterg. Jurnalul e documentație care își câștigă locul prin prevenție, nu prin volum. Fiecare intrare ar trebui să fie o regulă care a prevenit efectiv o recidivă cel puțin o dată.

**Trei: convențiile de Spring Boot specifice echipei.** (Sau de React, sau de orice stack folosești. Spring Boot e exemplul meu.)

> Doar constructor injection, nu field injection. (Mai ușor de testat.)
> `@Transactional` doar pe metodele de service care modifică starea, nu pe cele de citire. (Evită tranzacții read-only care țin lock-uri inutile.)
> Repository-urile extind `BaseRepository<Entity>` pentru filtrarea multi-tenant. (Vezi intrarea din jurnalul de greșeli, 2026-03-03.)
> DTO-urile de la granița controller-ului folosesc adnotări Bean Validation. Serviciile interne au încredere în input-urile lor.

Fiecare convenție e o linie. Agentul le citește și le aplică din oficiu. Codul nou respectă convențiile. Codul vechi care nu le respectă e adus treptat în linie pe măsură ce agentul trece prin el.

**Patru: comenzile de build și de test.** Incantațiile exacte pe care le folosește echipa.

> Build: `mvn clean verify`
> Rulează toate testele: `mvn test`
> Rulează testele unei singure clase: `mvn test -Dtest=ClassName`
> Rulează scanarea de securitate: `mvn dependency-check:check`
> Rulează linting-ul: `mvn spotless:check`

Sună banal. Nu e. Fără secțiunea asta, agentul ghicește comenzile. De obicei nimerește aproape, dar din când în când greșește, iar asta produce eșecuri derutante. Cu secțiunea asta, agentul folosește exact comenzile echipei, fără ghicit.

**Cinci: unde se găsesc lucrurile.** Convențiile structurale ale repository-ului.

> Serviciile stau în `src/main/java/com/bank/service/`
> Repository-urile în `src/main/java/com/bank/repository/`
> DTO-urile în `src/main/java/com/bank/dto/`
> Testele oglindesc structura din main, în `src/test/java/com/bank/`
> Migrările de bază de date în `src/main/resources/db/migration/` (Flyway)
> Configurarea în `src/main/resources/application.yml`

Agentul citește asta și știe unde să pună fișierele noi. Fără asta, merge pe cea mai bună presupunere dedusă din structura existentă - de regulă corectă, dar ocazional greșită în moduri care încalcă convențiile echipei.

**Șase: glosarul de domeniu.** Termeni specifici business-ului tău.

> „Customer” înseamnă utilizator final al băncii, nu client corporate. Clienții corporate sunt „Counterparties”.
> „Transfer” acoperă atât mișcările intra-bancare, cât și pe cele inter-bancare. „Wire” înseamnă strict inter-bancar.
> „Holds” sunt rezervări de fonduri pe termen scurt, diferite de „blocks”, care sunt restricții legale pe termen lung.

Glosarul dezambiguizează termeni pe care agentul i-ar interpreta altfel în sensul lor generic. În context bancar, „transfer” înseamnă ceva precis. În pretraining-ul agentului, „transfer” înseamnă o grămadă de lucruri. Glosarul ancorează agentul în sensul tău.

---

AGENTS.md trebuie să stea sub două sute de linii. E o constrângere fermă, nu o recomandare.

Două sute e bugetul pentru că AGENTS.md se încarcă în contextul agentului la fiecare început de sesiune. Fiecare linie costă context pe care agentul l-ar putea folosi pentru task-ul propriu-zis. Două sute de linii încap confortabil, fără să sufoce capacitatea de raționament. Dacă AGENTS.md-ul tău a trecut de două sute de linii, face prea multe. Cele două moduri de eșec:

Modul de eșec A: prea multe reguli. Echipa a acumulat reguli în timp și nu le-a scos niciodată din uz pe cele care nu se mai aplică. Fă un audit. Elimină regulile care nu s-au declanșat în ultimele șase luni. Mută regulile rar aplicabile în skill-uri care se încarcă la detecție, nu la fiecare sesiune.

Modul de eșec B: prea multă vorbă. Fiecare regulă e un paragraf în loc de o linie. Strânge. Agentul nu are nevoie de trei fraze de justificare pentru fiecare regulă; are nevoie de regulă. Justificările își au locul în comentarii în AGENTS.md sau în documentația linkată.

Plafonul de două sute de linii te obligă să ai o opinie. Opinia e valoarea.

---

AGENTS.md se versionează în git. Trece prin review în pull request. E semnat de autor. Modificările la AGENTS.md trec prin același proces de review ca modificările de cod, pentru că AGENTS.md *este* cod, în sensul că agentul execută pe baza lui.

Când un developer adaugă o regulă nouă, pull request-ul are cel puțin un reviewer. Reviewerul întreabă: „ce eșec previne regula asta? când am văzut-o ultima oară?” Dacă răspunsul e „n-am văzut-o, dar cred că s-ar putea întâmpla”, regula nu intră. Reviewerul pune frână. Regulile speculative se adună și umflă fișierul; doar regulile născute din eșecuri reale își merită locul.

Am văzut echipe care își întrețin AGENTS.md-ul de peste un an, la calitate constantă. Pattern-ul e același peste tot: un champion îl deține, championul se rotește trimestrial, fiecare modificare trece prin review, limita de sub două sute de linii se respectă, iar jurnalul de greșeli crește, apoi scade, apoi crește, apoi scade, pe măsură ce codebase-ul se maturizează.

Asta e infrastructură de inginerie. Tratează-o ca atare.

---

**Când agentul minte cu încredere.**

O subsecțiune separată, pentru că orice practician se lovește de asta săptămânal.

Agentul mai face uneori referire la fișiere care nu există. La o semnătură de funcție pe care biblioteca n-o expune de fapt. La o opțiune de configurare scoasă din uz acum trei versiuni. Output-ul arată plauzibil. E greșit.

Fenomenul se numește halucinație - ăsta e termenul politicos. Termenul mai direct e că agentul inventează ca să fie de ajutor. Agentul nu știe că inventează. Agentul generează tokeni care se potrivesc pe pattern-uri din cod similar pe care l-a văzut, iar pattern-ul, întâmplător, nu se potrivește cu realitatea ta specifică.

Trei tactici care reduc costul.

Unu: obligă agentul să citească înainte să citeze. Dacă agentul e pe punctul de a face referire la un fișier, ar trebui să fi citit acel fișier în sesiunea curentă, suficient de recent încât citirea să-i apară în contextul recent. AGENTS.md poate impune asta: „Înainte să faci referire la orice funcție, citește în sesiunea curentă fișierul care o definește. Citările fără o citire prealabilă se tratează ca ciorne de verificat.”

Doi: verifică încrucișat tool call-urile cu grep. După ce agentul produce cod care apelează o funcție de bibliotecă, dă un grep prin codebase după numele funcției. Dacă grep nu întoarce nimic, funcția probabil nu există (sau există într-o dependență vendored pe care agentul n-o vede). Verificarea e mecanică și prinde în câteva secunde cele mai frecvente halucinații.

Trei: formate structurate de citare, cu hook-uri de verificare. Dacă agentul citează fișier și număr de linie („vezi ImpactCalculator.java, linia 142”), o regulă hookify poate verifica dacă linia există înainte ca agentul să meargă mai departe. Hook-ul are câteva linii de bash. Prinde orice citare fabricată.

Pattern-ul general: nu te încrede în nimic din ce agentul nu tocmai a demonstrat că știe. Workflow-ul de review de arhitectură din capitolul următor e o formă a acestei discipline aplicată la nivel de codebase. Verificarea încrucișată, citirea forțată și hook-ul de citare sunt forme ale ei aplicate la nivel de fișier și de funcție.

Halucinația e cel mai mediatizat mod de eșec al agentului și cel pentru care se supracorectează cel mai des. Nu trebuie să verifici tot ce face agentul. Trebuie să verifici exact acele afirmații ale agentului care, dacă sunt greșite, se propagă și se amplifică. Citările de fișiere și de funcții sunt primele pe lista aia.

---

**O comparație concretă: AGENTS.md prost vs AGENTS.md bun.**

Diferența dintre un AGENTS.md care ajută și unul care nu ajută se vede de obicei într-o singură regulă. Ia o regulă despre validare, de care aproape orice echipă va avea nevoie.

Prost:

> Respectă întotdeauna standardele noastre de cod. Ai grijă la validare. Folosește arhitectura corectă. Nu face modificări riscante.

Bine:

> Validarea de la granița controller-ului aparține DTO-urilor, prin adnotări Bean Validation. Serviciile au încredere în DTO-urile validate și nu re-validează. Nu adăuga niciodată adnotări de validare în metodele de service. Exemple: UserCreateController, AccountUpdateController.

Varianta proastă sună responsabil. Îi spune agentului să fie atent, să respecte standardele, să folosească arhitectura corectă. E și inutilă. „Atent” nu e o constrângere pe care agentul s-o poată verifica. „Arhitectura corectă” depinde de un context pe care regula nu-l oferă. Agentul va citi regula, va produce cod care o încalcă, iar echipa va trage concluzia că AGENTS.md nu funcționează.

Varianta bună e aplicabilă. Numește stratul (DTO-urile la granița controller-ului), mecanismul (adnotările Bean Validation), regula (serviciile au încredere, nu re-validează) și două exemple concrete pe care agentul le poate folosi drept tipar. O regulă ca asta prinde greșeli în review. Varianta proastă nu prinde nimic.

Pattern-ul: regulile care numesc stratul, mecanismul și cel puțin un exemplu sunt reguli pe care agentul le poate aplica. Regulile care fac semn vag spre principii sunt reguli pe care agentul le va ignora.

---

**Artefact: AGENTS.md de pornire, în 15 linii.** Trei pattern-uri interzise, o intrare în jurnalul de greșeli din trimestrul trecut, comenzile de build și de test ale echipei, unde stă codul. Dă-i commit. Invită echipa să-l extindă.

---

**De pus în practică săptămâna asta.**

Schițează un AGENTS.md de cincisprezece linii pentru un singur proiect. Trei pattern-uri interzise, o intrare în jurnalul de greșeli (reală, din trimestrul trecut), comenzile de build și de test ale echipei, unde stă codul. Dă-i commit. Invită echipa să-l extindă prin pull request.

---

**Încearcă și tu.**

AGENTS.md-ul pe care îl livrezi azi nu trebuie să fie cel pe care l-ai fi scris tu de la zero. Trebuie să fie cel pe care echipa chiar îl va citi și îl va întreține.

1. Alege un repository al cărui fișier de instrucțiuni de echipă (AGENTS.md, sau CLAUDE.md, sau .github/copilot-instructions.md - oricare ar fi fișierul pe care agentul tău îl încarcă la începutul sesiunii) e gol, învechit sau scris de cineva care nu mai e în echipă.
2. Deschide agentul tău principal de cod în acel repository.
3. Cere-i: „Plimbă-te prin codebase-ul ăsta douăzeci de minute și spune-mi ce ar trebui să știe un coleg nou înainte să contribuie. Acoperă structura, convențiile, disciplina de teste, comenzile de build și de deploy și tot ce e documentat parțial sau greșit.”
4. Din răspuns, schițează un AGENTS.md de una-două pagini. Ține-l concret, despre repo-ul ăsta. Taie sfaturile generice de best practice; pe alea agentul le are deja din training.
5. Dă commit fișierului. Reîncarcă agentul în același repository. Întreabă-l: „Ce ai schimba în codebase-ul ăsta dacă ți-aș cere să adaugi un câmp Priority pe entitatea principală?” Compară răspunsul cu ce ți-ar fi spus agentul înainte să existe AGENTS.md-ul.
6. Dă AGENTS.md-ul unui coleg care n-a lucrat în repo-ul ăsta. Urmărește unde se încurcă. Acelea sunt următoarele tale modificări.

Un AGENTS.md funcțional e unul pe care un coleg îl citește în cinci minute și după care poate contribui fără alte întrebări pe chat. Tehnica merge cu orice agent care încarcă un fișier de instrucțiuni de echipă la începutul sesiunii. Numele fișierului și mecanismul de încărcare diferă de la vendor la vendor; disciplina e aceeași.

---

## Capitolul 7
## Review-ul de arhitectură: documentare și diagnostic

În Capitolul 2 ți-am arătat cum am folosit un coding agent ca să inspectez codul sursă al altor doi coding agents, în paralel. Am numit ce am găsit acolo anatomia invariantă. Acum vreau să transform observația aceea într-un workflow pe care să-l poți aplica chiar săptămâna asta pe un codebase pe care echipa ta îl deține și abia și-l mai amintește.

Workflow-ul e simplu. Îndrepți agentul spre repository. Îi ceri să producă un review de arhitectură structurat. Salvezi output-ul ca artefact durabil. Folosești artefactul ca punct de intrare pentru orice lucrare ulterioară în acel codebase.

Mai toate echipele dețin cel puțin un codebase care se potrivește descrierii „abia și-l mai amintim”. Autorul original a plecat acum doi ani. Documentația e subțire și parțial greșită. README-ul descrie un proces de build care nu mai merge de la update-ul de dependențe din martie anul trecut. Codul rulează în producție și aduce bani. Nimeni nu vrea să-l atingă.

Înainte de agenți, să devii productiv într-un asemenea codebase dura săptămâni. Un senior engineer petrecea două-patru săptămâni citind sursa, punând întrebări, trasând fluxuri, scriind documentație internă. Înmulțește cu costul total al unui asemenea inginer și ajungi la sume de cinci cifre per codebase, per onboarding. Ori trei-patru ingineri per repository legacy de-a lungul vieții lui. Ori numărul de repository-uri legacy din organizația ta. Costul agregat e substanțial. Mai toate organizațiile îl înghit fără să-l măsoare.

Workflow-ul cu agenți coboară costul ăsta la zece-douăzeci de minute de timp de agent plus o oră de review uman. Agentul citește sursa, trasează fluxurile, identifică pattern-urile, produce documentația. Omul revizuiește, corectează, adaugă contextul pe care agentul l-a ratat, semnează. Artefactul intră în repository, versionat. Următoarea persoană care are de lucrat în codebase pornește de la artefact, nu de la zero.

E workflow-ul cu cel mai bun raport efort-câștig din tot manualul. Îl aplici o dată și investiția s-a întors.

---

Mai jos e promptul pe care îl folosesc, ușor editat. Al tău va arăta altfel; ăsta e ilustrativ. Promptul rămâne în engleză - așa îl folosesc în practică, și pe ăsta îl lipești ca atare.

> Analyze the architecture of this codebase. Produce a structured architecture review document that covers:
>
> 1. **Purpose.** What does this service do? Who uses it? What business problem does it solve?
> 2. **Top-level structure.** Major modules, packages, or folders. One paragraph per major component explaining its role.
> 3. **Data model.** Primary entities, relationships, persistence. Cite specific files and line numbers.
> 4. **Request flows.** For the three most important external entry points (API endpoints, scheduled jobs, message consumers), trace the flow from entry to persistence. Cite files and lines at each step.
> 5. **Cross-cutting concerns.** Authentication, authorization, logging, error handling, configuration. How are they implemented and where do they live?
> 6. **Dependencies.** External services, databases, message brokers, third-party APIs. List with versions if discoverable.
> 7. **Test posture.** What is the test structure, what coverage exists, where are the gaps?
> 8. **Build and deployment.** How is this thing built and deployed? Cite the relevant configuration files.
> 9. **Risks and unknowns.** Code that looks fragile, areas where conventions are inconsistent, dependencies that may be deprecated, places where the codebase has accumulated patterns that suggest unresolved decisions.
>
> Cite specific files and line numbers throughout. Where the codebase is ambiguous, say so explicitly. Where you encounter patterns the team should formalize as conventions, suggest the convention.

Promptul ăsta, lansat pe un serviciu Spring Boot de complexitate medie, produce un document de arhitectură de zece-cincisprezece pagini în mai puțin de cincisprezece minute. Documentul va fi corect cam în proporție de 70%. Restul de 30% e exact motivul pentru care review-ul uman e esențial - agentul va interpreta greșit unele pattern-uri, va rata context care trăiește în afara codebase-ului, uneori va descrie cu toată încrederea un code path scos din uz de mult. Reviewerul uman corectează toate astea. După review, documentul e solid.

Asta e varianta cu un singur agent și e suficientă pentru majoritatea serviciilor. Pe un codebase prea mare pentru un singur context window, același workflow se distribuie pe subagenți - câte unul per modul, fiecare întorcând un rezumat structurat, iar orchestratorul asamblează documentul din bucăți. E pattern-ul de analiză de arhitectură la scară din Capitolul 1, pus la treabă în producție.

Documentul corectat intră în repository. Prin convenție, îl pun la `docs/architecture.md`. Devine punctul de intrare pentru orice lucrare ulterioară. Membrii noi ai echipei îl citesc primii. Inginerii seniori îl consultă când modifică părți nefamiliare ale sistemului. Îl citește și agentul (îl referențiezi din [AGENTS.md](https://agents.md/)) când lucrează în codebase, astfel încât munca lui ulterioară e ancorată în review-ul de arhitectură, în loc să re-derive arhitectura de fiecare dată.

---

Workflow-ul de review de arhitectură are și o alternativă șlefuită, care merită menționată. Există un plugin numit Understand Anything care face ceva similar cu promptul de mai sus, dar cu un dashboard vizual ca output principal, în locul unui document markdown. Dashboard-ul redă codebase-ul ca un graf navigabil - vederea structurală (module, dependențe, ierarhia de fișiere) pe un tab, vederea de domeniu (concepte de business, entități, conexiuni între domenii) pe altul.

Vederea structurală e utilă pentru ingineri. Vederea de domeniu e utilă pentru manageri, pentru că prezintă codebase-ul în termeni de concepte de business, nu de căi de fișiere. Un manager care nu citește Java se poate uita la vederea de domeniu și poate vedea „aha, serviciul ăsta se ocupă de detecția fraudelor pe transferurile primite” fără să citească un rând de sursă.

Includ alternativa cu plugin de dragul completitudinii. Documentul markdown de arhitectură descris mai sus e suficient pentru majoritatea echipelor; dashboard-ul vizual e un upgrade real pentru echipele ai căror manageri sau oameni de produs au nevoie să interacționeze regulat cu structura codebase-ului. Alege după ce are nevoie echipa ta, nu după ce arată mai spectaculos.

---

Rulează workflow-ul de review de arhitectură întâi pe codebase-ul tău cel mai prost înțeles. Privește agentul cum produce în cincisprezece minute ce i-ar fi luat unui senior engineer o săptămână. Salvează artefactul. Referențiază-l din AGENTS.md. Treci la următorul codebase.

Asta e rețeta.

---

Același workflow e și un instrument de diagnostic. Aceleași cincisprezece minute de timp de agent îți spun dacă are sens, în primul rând, să adopți lucrul cu agenți pe codebase-ul respectiv.

Iată un review de arhitectură pe care l-am rulat anul trecut pentru o echipă de banking - anonimizat, dar fidel experienței.

Codebase-ul era un sistem de onboarding pentru clienți. Cam șaizeci de mii de linii de Java, scrise între 2018 și 2024 de o distribuție rotativă de contractori. Echipa care îl deținea acum fusese asamblată în 2024 din trei achiziții diferite și niciunul dintre inginerii actuali nu fusese de față la build-ul original. Lead-ul tehnic original plecase cu doi ani în urmă. Exista un README care descria o arhitectură din 2020, doar vag asemănătoare cu codul curent. Build-ul avea trei pași, documentația enumera doi, al treilea era tribal knowledge.

Când am ajuns eu, echipa lua în calcul un rewrite complet. Estimarea era de optsprezece luni. Justificarea: „nimeni nu îl înțelege suficient de bine ca să-l întrețină cu încredere.” Ceea ce, sincer, era adevărat. Era însă și genul de justificare care duce frecvent la proiecte de rewrite ce durează de trei ori mai mult decât estimarea și produc sisteme cu toate problemele originalului, plus câteva noi.

Am cerut cincisprezece minute și un terminal. Am clonat repository-ul. Am deschis agentul. Am lipit promptul de review de arhitectură de mai devreme din acest capitol, cu două mici ajustări - am adăugat „this is a customer onboarding system in a regulated banking context”, ca să-i dau agentului domeniul, și i-am cerut explicit să marcheze tot ce arată a code path sensibil din punctul de vedere al conformității.

Optsprezece minute mai târziu, agentul produsese un document de arhitectură de treisprezece pagini. L-am citit. Nu era perfect, iar imperfecțiunile contează. Agentul identificase greșit un modul - numise serviciul de deduplicare „serviciu de căutare”, pentru că implementarea folosea infrastructura de search, dar scopul de business real era deduplicarea înregistrărilor de clienți, ca să nu se creeze dubluri. Am corectat. Agentul descrisese, tot cu deplină încredere, un „job programat” care, la o privire mai atentă, s-a dovedit a fi cod comentat, nerulat în producție de trei ani. Am corectat și asta. Agentul ratase faptul că una dintre dependențele third-party era deprecated și avea un security advisory; am adăugat eu informația, pentru că agentul nu avea acces la baza de date de advisories.

O notă despre timpul de corecție. Am petrecut cam patruzeci și cinci de minute corectând documentul ăla de treisprezece pagini. Cifra stă în picioare datorită unei condiții precise: aveam context. Nu context adânc pe acest codebase - nu-l văzusem niciodată -, ci context general pe domeniu. Construisem sisteme de onboarding de clienți și înainte. Știam cum arată de obicei un serviciu de deduplicare. Știam cum arată de obicei un path de conformitate în banking reglementat. Identificările greșite ale agentului mi-au sărit în ochi pentru că aveam un model mental cu care să le compar.

Dacă și reviewerul descoperă codebase-ul pentru prima oară - un coleg nou-angajat care n-a văzut în viața lui onboarding bancar, de exemplu -, bucla de corecție durează mai multe ore, nu patruzeci și cinci de minute. Reviewerul trebuie să citească fiecare afirmație a agentului, să se uite la codul de dedesubt și să decidă dacă afirmația e corectă, fără un reper de domeniu pe care să se sprijine. Identificările greșite ale agentului arată în continuare plauzibil; reviewerul nu poate spune pe care să le semnaleze. Ăsta e cel mai important avertisment practic legat de timpii workflow-ului de review de arhitectură: estimarea de patruzeci și cinci de minute de corecție presupune un reviewer cu cunoaștere de domeniu. Fără ea, workflow-ul funcționează în continuare, dar partea umană costă mai mult.

În cazul din banking, cunoașterea de domeniu o aveam. După vreo patruzeci și cinci de minute de corecturi, aveam un document de treisprezece pagini care descria fidel codebase-ul. Echipa l-a citit. Doi dintre ingineri mi-au spus, separat, că au învățat mai multe despre codebase din document decât din șase luni de lucru în el. Al treilea inginer a semnalat un gol în plus, pe care îl ratasem; l-am adăugat. Documentul a intrat în repository.

Echipa n-a mai făcut rewrite-ul. A folosit documentul de arhitectură ca să identifice cele două module care chiar aveau nevoie de înlocuire (dependența deprecated era unul dintre ele) și a înlocuit doar acele module în trimestrul următor. Restul codebase-ului devenise întreținabil, pentru că echipa putea citi documentul de arhitectură, găsi secțiunea relevantă și înțelege ce atinge înainte să atingă. Estimare de rewrite de optsprezece luni, redusă la o înlocuire țintită de trei luni, pe baza a cincisprezece minute de muncă de agent plus o oră de review uman. Nu agentul a decis că rewrite-ul nu era necesar. A produs suficientă structură încât experții de domeniu să poată lua decizia aia mai repede.

Cincisprezece minute de muncă de agent nu au înlocuit judecata de domeniu; au făcut-o mai ieftin de aplicat. Nu teoretic. Nu „în principiu”. „Am rulat exact workflow-ul ăsta pe exact codebase-ul ăsta, iar compania a economisit nouă om-luni de efort de rewrite pe care altfel le-ar fi cheltuit și le-ar fi regretat.”

---

**Fișă de caz: banking reglementat, review-ul de arhitectură ca diagnostic.**

| | |
|---|---|
| **Context** | Echipă de banking reglementat, serviciu Java de ~60k LOC, codebase vechi de 3 ani, documentație învechită |
| **Problema** | Echipa redactase o propunere de rewrite de 18 luni; inginerii seniori se îndoiau că rewrite-ul e necesar, dar nu aveau dovezile cu care să argumenteze |
| **Intervenția** | Workflow-ul de review de arhitectură, rulat pe codebase; a produs docs/architecture.md ca artefact auditabil |
| **Timp de agent** | ~15-18 minute |
| **Timp de corecție umană** | ~45 de minute (reviewerul cunoștea în profunzime domeniul de onboarding de clienți) |
| **Rezultat** | A identificat problema reală - două module purtau datoria tehnică; propunerea de rewrite, convertită într-o înlocuire țintită de 3 luni |
| **Limitări** | Reviewerul a trebuit să cunoască domeniul ca să evalueze output-ul agentului; workflow-ul nu înlocuiește cunoașterea de domeniu, o accelerează |

---

Acum partea de diagnostic.

Workflow-ul de review de arhitectură e cel mai ieftin test posibil pentru întrebarea dacă lucrul cu agenți va funcționa pe un codebase dat. Dacă agentul poate produce un review de arhitectură coerent, cu un volum rezonabil de corecții umane, codebase-ul e într-o formă suficient de bună încât agentul să fie util și la lucrările următoare. Dacă agentul nu poate produce un review coerent - dacă codebase-ul e atât de încâlcit încât până și citirea lui produce un rezultat inutilizabil -, atunci ai aflat, la un cost foarte mic, că acest codebase e în zona roșie a disciplinei pe care urmează s-o introduc și că trebuie să repari codebase-ul înainte să încerci să folosești agentul pe el pentru modificări de producție.

Oricare dintre rezultate e valoros. Investiția e de cincisprezece minute plus o oră. Riscul e limitat. Câștigul, în cazuri ca acela din banking descris mai sus, înseamnă luni de muncă economisite.

Rulează workflow-ul săptămâna asta. Rulează-l pe cele trei-patru codebase-uri pe care echipa ta le înțelege cel mai prost. Output-ul agentului îți va spune multe despre care dintre ele sunt pregătite pentru restul manualului și care au nevoie întâi de investiție.

Asta e puntea către restul Părții a III-a. Capitolul următor - kill signals - e grila structurată de evaluare a gradului de pregătire al unui codebase. Workflow-ul de review de arhitectură îți dă testul empiric ieftin; kill signals îți dau checklist-ul sistematic. Funcționează împreună.

---

**Artefact: promptul de review + checklist-ul de corecție pentru om.** Promptul de review de arhitectură din Anexa B, însoțit de checklist-ul în cinci puncte cu ce trebuie să verifice omul în output-ul generat: scopul modulelor, raportat la realitatea de business, nu la infrastructura de implementare; orice e descris ca activ, dar ar putea fi mort sau comentat; faptele despre dependențe și advisories pe care agentul nu le vede; path-urile sensibile din punctul de vedere al conformității; și fiecare ambiguitate semnalată chiar de agent.

---

**De pus în practică săptămâna asta.**

Rulează promptul de review de arhitectură pe cele trei codebase-uri pe care echipa ta le înțelege cel mai prost, cu un buget de șaizeci de minute fiecare. Notează care produc un review curat și care produc output incoerent. Pattern-ul ăsta e diagnosticul dinaintea Capitolului 8: output curat înseamnă că lucrul cu agenți are o șansă; output-ul incoerent e unul dintre kill signals.

---

**Încearcă și tu.**

Review-ul de arhitectură e exercițiul cu cel mai bun raport efort-câștig din acest manual. Îl poți rula pe orice repository pe care îl poți clona, în cincisprezece minute per repository, și îl poți rerula ori de câte ori codebase-ul se schimbă substanțial.

1. Alege codebase-ul pe care echipa ta îl înțelege cel mai puțin. Autor original plecat, documentație parțială, „nu te atinge de el decât dacă n-ai încotro” - acela.
2. Deschide agentul tău principal de cod în rădăcina repository-ului.
3. Trimite promptul de review de arhitectură din acest capitol - varianta în nouă secțiuni, care acoperă scopul, structura, modelul de date, fluxurile de request, aspectele transversale, dependențele, starea testelor, build-ul și deployment-ul și riscurile, cu citări fișier:linie peste tot. Anexa B.1 e forma de copy-paste; merge pe orice coding agent din generația mai 2026.
4. Salvează output-ul corectat ca `docs/architecture.md`. Dă-i commit. Referențiază-l din AGENTS.md, ca fiecare sesiune nouă să-l citească la pornire.
5. Folosește același artefact ca diagnostic. Dacă agentul n-a putut produce o hartă coerentă, ăsta e un kill signal: codebase-ul nu e încă pregătit pentru lucru autonom cu agenți. Soluția e mai întâi documentare condusă de oameni, nu un alt prompt.

Pe generația de agenți din mai 2026, un codebase mediu produce un review util în patru până la zece minute. Unul mai puțin auto-documentat se apropie de cincisprezece. Artefactul pe care îl generezi e același pe care un senior engineer l-ar fi produs într-o săptămână.

Agenții din tooling-ul tău de peste un an vor fi alții. Exercițiul, nu.

---

Partea a II-a se încheie aici. Ai metoda. Știi cum să formulezi munca într-un mod pe care agentul îl poate executa, bucla în șase faze care transformă formularea în livrare, infrastructura AGENTS.md care face metoda portabilă și workflow-ul de review de arhitectură care te face productiv într-un codebase nou într-o după-amiază - și care e, în același timp, cel mai ieftin diagnostic pe care îl ai pentru a afla dacă lucrul cu agenți va reuși pe un codebase dat.

Partea a III-a e confruntarea cu realitatea. Metoda funcționează pe multe lucruri. Nu funcționează pe toate. Următoarele trei capitole sunt despre diferența asta - grila care îți spune ce codebase-uri sunt pregătite, pattern-urile operaționale pentru cele brownfield care sunt și arcul de nouăzeci de zile prin care duci o echipă la livrare susținută cu agenți.

---

# Partea a III-a - Realitatea

> *Controlul adopției: unde funcționează metoda, unde nu - și cum îți dai seama.*

---

## Capitolul 8
## Pregătirea: kill signals și semaforul

### Când n-ar trebui să folosești agenți AI de cod? {#when-not-to-use-agents}

O afirmație nepopulară, ca să deschidem capitolul. Există codebase-uri în care n-ar trebui să folosești livrarea cu agenți. Nu pentru că agentul ar fi prost, nici pentru că echipa ar fi slabă, ci pentru că codebase-ul are proprietăți care fac lucrul cu agenți nesigur, neproductiv sau ambele. Când o echipă mă întreabă dacă să pună un agent pe monolitul ei legacy, lucrul onest e să evaluez mai întâi codebase-ul și abia apoi să răspund.

Grila pe care o folosesc pentru evaluarea asta are opt kill signals. Fiecare semnal e o proprietate a codebase-ului sau a echipei. Cu cât sunt prezente mai multe semnale, cu atât e mai periculos să pui un agent în fața codului. De la un anumit prag, te oprești și repari codebase-ul înainte să aduci agentul.

Grila nu e o respingere a livrării cu agenți. E exact opusul: e disciplina care îți permite să spui da livrării cu agenți acolo unde funcționează, tocmai pentru că spui nu acolo unde nu funcționează. Fără kill signals, orice proiect devine un proiect AI, inclusiv cele care n-ar trebui să fie, iar eșecurile proiectelor nepotrivite murdăresc reputația întregii abordări. Tot ăsta e și capitolul construit să circule în sus pe ierarhie: cele opt semnale și semaforul sunt conversația de portofoliu - care codebase-uri acum, care mai târziu, care niciodată - într-o formă pe care un director o poate pune direct în practică.

---

Semnalele, pe scurt:

| Semnal | Ce se strică | Primul fix |
|---|---|---|
| 1. Fără teste | Agentul nu poate verifica comportamentul; regresiile trec neobservate | Teste de caracterizare pe modulele vizate |
| 2. Fără documentație | Agentul inventează contextul lipsă; produce cod plauzibil, dar greșit | Workflow-ul de review de arhitectură (Capitolul 7) |
| 3. Cuplare strânsă | Blast radius (raza de impact) imprevizibil; o schimbare declanșează o cascadă | Sparge mai întâi cea mai gravă graniță de cuplare |
| 4. Reguli împrăștiate | Agentul actualizează o copie a logicii de business și le ratează pe celelalte | O singură sursă de adevăr pentru regulă |
| 5. Constrângeri de reglementare | Agentul nu poate satisface singur auditul; e nevoie de un gate uman | Workflow cu pași de aprobare umană |
| 6. Echipa nu poate evalua output-ul | Review-ul uman nu poate prinde eșecul de domeniu | Restrânge scope-ul sau adaugă un reviewer expert (cântărește greu) |
| 7. Potrivirea model-context | Agentului îi lipsește familiaritatea cu corpusul; performanța scade | Adaugă documentație/skill-uri sau alege un model cu potrivire mai bună |
| 8. Viteza schimbării | Framework-ul sau versiunea se mișcă sub agent | Reguli specifice versiunii în [AGENTS.md](https://agents.md/) |

---

**Semnalul unu: fără teste.**

Codebase-ul nu are o suită de teste automate, sau are una atât de învechită încât n-o mai rulează nimeni. Build-ul trece. Nimic nu exersează comportamentul.

Asta blochează lucrul condus de agent în condiții de siguranță, pentru că agentul nu-și poate verifica propriile schimbări. Agentul va scrie cod care arată corect. Codul va compila. Va trece de verificările de sintaxă. Va ajunge pe mediul de staging. Apoi va strica ceva în producție, iar nimeni nu va observa până când un client se plânge trei săptămâni mai târziu - moment în care schimbarea e îngropată sub alte douăzeci și regresia e greu de atribuit.

Mi s-a întâmplat de două ori, în banking, cu aceeași cauză de fond: un modul de reconciliere a tranzacțiilor scris la începutul anilor 2010 de un senior care a plecat din companie în 2018. Fără teste, pentru că „seniorul pur și simplu știa că merge”. Următorul om care l-a modificat a stricat logica de reconciliere într-un fel care a ieșit la suprafață abia după două luni, moment în care discrepanța depășise deja pragul care declanșează o raportare către reglementator. Ăsta e costul lui „n-am avut niciodată teste” într-un mediu reglementat. Agentul nu face decât să accelereze totul - și drumul productiv, și drumul spre eșec.

Ce e de făcut: scrie întâi testele. Nu toate; doar cât să fixezi comportamentul curent. Folosește agentul pentru asta - îndreaptă-l spre modul și cere-i teste de caracterizare care surprind ce face modulul acum. Agentul e bun la genul ăsta de generare de teste în masă, pentru că specificația e „orice produce codul în acest moment”. Odată ce testele de caracterizare există, poți lăsa agentul să modifice modulul, pentru că testele vor prinde schimbările de comportament.

Asta transformă un kill signal într-un risc gestionabil. E, totodată, o investiție reală de timp. Dacă echipa nu e dispusă s-o facă, răspunsul e nu: n-ar trebui să pui un agent pe codul ăsta.

O precauție: testele de caracterizare generate de agent pe cod legacy fixează comportamentul curent, nu comportamentul corect. Folosește-le ca plasă de siguranță împotriva regresiilor cât timp migrezi, nu ca dovadă de corectitudine.

---

**Semnalul doi: fără documentație.**

Codebase-ul n-are o privire de ansamblu asupra arhitecturii, n-are comentarii în cod care să explice de ce s-au luat deciziile, n-are documente de design, n-are decision records. Structura e ce e, și doar autorul original știe de ce.

Asta blochează lucrul condus de agent în condiții de siguranță pentru că agentul inventează context acolo unde contextul lipsește. Într-o echipă, seniorul responsabil de logica de comisioane știa că fee tier-ul se calculează diferit pentru linia de produse legacy, din cauza unei excepții de reglementare din 2017. Agentul nu știa. A citit codul, a văzut un singur calcul, a presupus tratament uniform și a propus un refactor care „simplifica” funcția. Seniorul a prins bug-ul la code review. Același senior ajunsese să facă review pe output de AI patruzeci de ore pe săptămână, în loc să construiască.

Povara cade exact pe oamenii pe care îți permiți cel mai puțin să-i pierzi. Când echipa adoptă livrarea cu agenți fără să investească mai întâi în documentație, seniorii echipei se opresc din construit și se apucă de review. Throughput-ul poate rămâne același; experiența e mult mai proastă, iar seniorii pleacă până la urmă, pentru că nimeni nu s-a angajat din pasiune ca să facă review pe output de AI cât e ziua de lungă.

Ce e de făcut: rulează mai întâi workflow-ul de review de arhitectură din Capitolul 7. Agentul produce în cincisprezece minute documentația care i-ar fi luat unui senior o săptămână. Dă-i commit. Pune un link spre ea în AGENTS.md. Adaugă un glosar scurt de domeniu. Acum agentul are context.

Asta transformă kill signal-ul într-un risc gestionabil. E tot o investiție reală de timp - dar mult mai mică decât să scrii documentația de la zero.

---

**Semnalul trei: cuplare strânsă.**

Codebase-ul are module care nu pot fi modificate izolat. Editezi un fișier, se strică alte trei. Graful de dependențe e un ghem. Importurile traversează nonșalant granițele dintre straturi. Testele unui modul cer să pregătești stare în alt modul. „Nucleul de domeniu” e împletit cu stratul de persistență, care e împletit cu stratul HTTP.

Asta blochează lucrul condus de agent în condiții de siguranță pentru că blast radius-ul agentului devine imposibil de prezis. Agentul editează fișierul pe care i l-ai cerut. Rulează testele pe care le găsește. Testele trec. Schimbarea pleacă în producție. Și strică un modul din aval care n-are niciun test - sau al cărui test nu exersează exact acel code path - iar stricăciunea iese la iveală în producție, la închiderea batch-ului de sfârșit de lună.

Un exemplu: un modul de customer service care importa dintr-un modul de originare a creditelor, care importa dintr-un modul de credit scoring, care importa din modulul de customer service. Ciclul fusese introdus acum paisprezece ani ca să „câștige timp”, și nimeni nu-l refactorizase, pentru că orice încercare de a-l sparge ar fi însemnat un proiect de opt săptămâni. Agentul nu știa de ciclu. A făcut o schimbare. Schimbarea s-a propagat într-un fel care a ieșit la suprafață luni mai târziu, în producție.

Ce e de făcut: identifică întâi cea mai gravă cuplare și sparge-o. Doar bucata cea mai gravă. Proiectul de opt săptămâni nu trebuie terminat înainte de orice lucru cu agenți; bucata cea mai gravă, da - pentru că acolo se vor amplifica greșelile agentului. Odată decuplată bucata cea mai gravă, restul codebase-ului nu mai e un pericol imediat pentru agent: e cod legacy normal, gestionabil cu celelalte practici din acest manual.

Dacă echipa nu vrea să investească în decuplare, răspunsul e galben în cel mai bun caz, roșu în cel mai rău, în funcție de cât de gravă e cuplarea.

---

**Semnalul patru: reguli de business împrăștiate.**

Aceeași regulă de business e exprimată în trei locuri. Constrângere în baza de date, verificare în stratul de servicii, validare în UI. Când regula se schimbă - și regulile de business se schimbă încontinuu - agentul actualizează una și le ratează pe celelalte. Schema acceptă o valoare pe care serviciul o respinge, sau UI-ul îl lasă pe utilizator să introducă o valoare pe care schema o refuză. Sistemul se minte singur.

Exemplu din banking: suma maximă de transfer. Definită într-un fișier de config pentru UI. Hardcodată într-o constantă în serviciu. Constrânsă de un trigger în baza de date. Echipa de compliance actualizează config-ul, pentru că ăla e fișierul pe care știe să-l citească. Șase săptămâni mai târziu, un client nu poate trimite un transfer valid, pentru că constanta din stratul de servicii a rămas veche. Actualizarea făcută de compliance a fost ignorată de sistemul pe care toți au uitat să-l actualizeze.

Agentul agravează problema, și o agravează mai repede. Fără o singură sursă de adevăr, agentul va ghici care copie e cea canonică - și va ghici greșit.

Ce e de făcut: identifică duplicările și consolidează-le. Pattern-ul e „extrage regula într-o sursă unică și derivă celelalte expresii din ea”. Pentru validări în stil bancar, asta înseamnă de multe ori mutarea regulilor într-un rules engine tipizat sau într-un serviciu de configurare consultat de toate straturile. Vorbim de săptămâni de refactor, nu de o după-amiază. Și se amortizează indiferent dacă aduci sau nu agenți vreodată, pentru că duplicarea era deja o fabrică de bug-uri.

Dacă echipa nu face consolidarea, contribuția agentului în acest codebase se va limita la zonele care nu ating regulile duplicate. E o utilizare mai restrânsă a agentului decât și-ar dori probabil echipa, dar e onestă față de constrângere.

---

**Semnalul cinci: constrângeri de reglementare.**

Codebase-ul e sub cerințe de audit în care fiecare schimbare trebuie să fie trasabilă către o aprobare anume, un reviewer anume, un lanț de dovezi anume.

Agentul nu poate îndeplini singur constrângerea de audit. Nu știe care schimbări sunt materiale pentru audit și care nu. Nu știe care revieweri trebuie să semneze pentru care categorii de schimbări. Nu poate ruta aprobări; nu poate satisface cerințe de tip two-person rule; nu poate produce dovezi în forma pe care o așteaptă auditorul.

Nu e fatal, dar cere ca echipa să împacheteze agentul într-un workflow. Agentul produce schimbarea. Echipa rutează aprobarea. Mecanismul de audit deja existent al echipei se ocupă de trail-ul de dovezi. Output-ul agentului e un input într-un proces mai mare; nu e procesul.

Exemplu din banking: orice schimbare a logicii de anti-money-laundering cere semnătura ofițerului de compliance, a unui reprezentant din legal și a unui senior neimplicat în implementare. Agentul poate produce schimbarea. Agentul nu poate ruta aprobarea. Echipa trebuie să împacheteze agentul într-un workflow.

Dacă constrângerile de reglementare sunt blânde - să zicem, orice schimbare de cod cere un code review de la un senior, dar nu există o matrice formală de semnături - agentul intră curat în procesul existent. Dacă sunt apăsătoare - matrici de sign-off, cerințe de dovezi, aprobări cu timestamp, obligații de retenție - agentul funcționează doar ca parte dintr-un sistem mai mare care gestionează deja acele constrângeri.

Kill signal-ul aici e „echipa n-are niciun sistem pentru constrângerile de reglementare și speră că agentul le va rezolva cumva”. Nu le va rezolva. Sistemul trebuie să existe independent. Agentul operează înăuntrul lui.

---

**Semnalul șase: echipa nu poate evalua output-ul.**

E cel mai important semnal. E și cel pe care echipele îl înțeleg greșit cel mai des.

Semnalul e structural. Se aprinde atunci când capacitatea existentă a echipei de a evalua munca nu e suficientă pentru munca pe care urmează s-o facă agentul. Un developer junior primește un story: adaugă un pas de verificare criptografică în fluxul de plăți. Juniorul trimite agentul la treabă. Agentul produce un modul de criptografie care folosește AES-256 în mod CBC cu un initialization vector hardcodat. Pentru un junior care n-a făcut criptografie până atunci, arată corect. Codul compilează. Testele unitare trec. Criptograful senior e în concediu de creștere a copilului trei luni. Juniorul livrează. Vulnerabilitatea stă în producție șase luni până când o găsește un penetration test.

Agentul a făcut exact ce i s-a cerut. Output-ul agentului arăta bine. Output-ul agentului era greșit. Echipa n-a avut pe nimeni în poziția de a evalua output-ul în momentul în care output-ul a fost produs.

Văd semnalul ăsta înțeles greșit ca „ne trebuie mai mulți seniori”. E o soluție. Nu scalează pe un orizont de șase luni. Cealaltă soluție e structurală: cuplează output-ul generat de agent cu un reviewer senior, într-un workflow care face review-ul inevitabil. O regulă de hookify care blochează merge-ul până aprobă un senior. Toolkit-ul de PR review care își rulează agenții înainte ca reviewerul uman să vadă diff-ul. O restricție în AGENTS.md prin care agentul nu are voie să atingă deloc modulele de criptografie până nu e setat un flag anume. Răspunsuri structurale, nu de headcount.

Semnalul e cel mai important și pentru că e singurul care prinde eșecurile catastrofale rare. Celelalte semnale prind probleme de productivitate și frustrări operaționale. Ăsta prinde eșecurile care ajung în raportări de conformitate și în retrospective de incident.

---

**Semnalul șapte: potrivirea model-context.**

Codebase-ul e scris într-un limbaj, framework sau domeniu unde pretraining-ul agentului e subțire. COBOL vechi. DSL-uri proprietare ezoterice. Framework-uri interne fără nicio urmă publică. Biblioteci științifice de nișă care n-au ajuns niciodată pe web-ul deschis.

Agentul va produce output sigur pe el, valid sintactic, dar deviat semantic. Face pattern-matching pe corpusul greșit. O funcție nouă va arăta a cod idiomatic pentru un alt framework care seamănă cu al tău. Un nume de clasă va urma o convenție din alt limbaj. Greșelile sunt subtile și consecvente, ceea ce le face mai greu de prins decât eșecurile evidente.

Exemplu din banking: un workflow engine intern, custom, scris la începutul anilor 2010, fără documentație publică și cu o sintaxă ciudată pentru tranzițiile de stare. Agentul a produs „îmbunătățiri” care arătau a curățenie, dar care aplicau de fapt pattern-uri dintr-un alt workflow framework (fără nicio legătură), pe care agentul îl văzuse mai mult. Codul a compilat. Testele, câte erau, au trecut. Mașina de stări nu se mai comporta corect în trei edge case-uri pe care echipa nu le-a testat inițial.

Ce e de făcut: stabilește dacă framework-ul sau domeniul codebase-ului tău are o amprentă publică consistentă (repo-uri open source pe care agentul le-ar fi putut vedea, documentație publică, prezentări la conferințe). Dacă da, potrivirea model-context e rezonabilă. Dacă nu, încrederea agentului va depăși competența lui. Tratează codebase-ul ca și cum ar avea activ doar semnalul de capacitate a echipei (șase), chiar și atunci când toate celelalte semnale sunt curate.

---

**Semnalul opt: viteza schimbării.**

Framework-ul sau dependențele codebase-ului se mișcă sub el chiar în perioada în care vrei să folosești agentul. Migrarea de la React 18 la React 19 e în plină desfășurare. Un bump de versiune majoră de Spring Boot la mijloc de trimestru. O bibliotecă centrală care își depreciază vechiul API public. O migrare de bază de date pe care echipa a dus-o doar pe jumătate.

Pretraining-ul agentului e un instantaneu înghețat al lumii. Dacă lumea s-a mișcat de la instantaneu încoace, iar codebase-ul tău e călare pe mișcarea asta, agentul va greși cu toată convingerea despre versiunea nouă, în timp ce are dreptate cu toată convingerea despre cea veche. Și nu vei ști mereu care e care.

Mod de eșec concret: am livrat un bug într-o componentă React pentru că Claude folosea idiomuri de React 18 în cod care avea nevoie de pattern-uri de React 19. Componenta mergea local, pentru că mediul de development local încă rezolva spre o dependență tranzitivă de React 18. S-a stricat în producție când build-ul a tras pachetul actualizat de React 19. Agentul nu greșea despre React 18. Greșea despre versiunea de React pe care trebuia s-o suporte exact acel code path.

Ce e de făcut: dacă codebase-ul tău e în mijlocul unei migrări de framework sau de dependențe, încetinește agentul pe căile atinse de migrare. AGENTS.md trebuie să numească explicit versiunea-țintă („migrăm de la React 18 la React 19 trimestrul ăsta; codul nou folosește idiomuri de 19; codul vechi mai poate folosi 18, dar se actualizează când e atins”). Agentul citește regula și folosește idiomurile potrivite pentru contextul potrivit. Fără regula asta, bug-urile le descoperi în producție.

---

Opt semnale. Fără teste. Fără documentație. Cuplare strânsă. Reguli de business împrăștiate. Constrângeri de reglementare. Echipa nu poate evalua output-ul. Potrivirea model-context. Viteza schimbării.

### Sunt agenții AI de cod gata de producție? {#are-agents-production-ready}

Semnalele nu sunt o respingere a agentului. Sunt disciplina care îi permite agentului să reușească acolo unde poate. Mai rămâne să le combinăm într-o regulă de decizie. Regula pe care o folosesc eu e un semafor: verde, galben, roșu.

**Verde: zero sau un semnal prezent.** Lucrul condus de agent e potrivit. Un singur developer poate trimite agentul la treabă, supraveghea bucla în șase faze, face review pe output și livra. Viteză normală. Povară de review normală. Asta e ce-și imaginează lumea când își imaginează „productivitate cu AI”.

**Galben: două sau trei semnale prezente.** Condus de om, cu sprijinul agentului. Faci pair programming cu agentul, nu îl trimiți singur la treabă ca apoi doar să-i verifici rezultatul. Mai lent decât verde. Beneficiu real de productivitate față de varianta fără agent, dar beneficiul stă mai mult în calitate (agentul prinde lucruri pe care omul le scapă) decât în viteză (omul face în continuare grosul muncii).

**Roșu: patru sau mai multe semnale prezente.** Repară mai întâi codebase-ul. Contribuția agentului aici va fi net negativă până când kill signals se reduc. Tentația va fi să folosești agentul oricum, pentru că leadership-ul a decis că „adoptăm AI”. Rezistă. Tentația asta e cea care produce poveștile de adopție AI eșuată care murdăresc tot domeniul.

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

---

Trei exemple din banking fac regula concretă.

Exemplul unu. Un microserviciu care gestionează actualizările profilului de client. Teste cu acoperire de 70%. Privire de ansamblu asupra arhitecturii în README-ul repo-ului. Decuplat de celelalte servicii printr-un API REST bine definit. Reguli de business exprimate o singură dată, într-o bibliotecă de validare tipizată. Controale SOX standard, dar fără cerințe speciale de audit. Echipa are seniori care se ocupă în mod curent de schimbările legate de profil.

Număr de semnale: zero. Verde. Lucrul condus de agent e potrivit. Echipa poate trimite agentul cu încredere pe story-urile legate de profil, le trece prin bucla în șase faze, livrează.

Exemplul doi. Motorul legacy de plăți. Teste cu acoperire de 20%, majoritar happy-path. Documentația de arhitectură există, dar e parțial învechită. Cuplare moderată între domeniul de plăți și cel de clienți, cu granițe documentate, dar și cu niște abstracțiuni care curg. Reguli de business în mare parte centralizate, cu câteva rătăcite prin code path-uri legacy. Constrângerile de reglementare sunt reale (PCI, raportare de fraudă), iar echipa are mecanismul de audit care să le gestioneze. Senioritate mixtă, cu unu-doi seniori care pot evalua output specific plăților.

Număr de semnale: două și jumătate (lipsa testelor e jumătate, documentația parțială e jumătate, cuplarea moderată e un întreg, constrângerile de reglementare gestionate sunt zero pentru că mecanismul există, capacitatea de evaluare e zero pentru că seniorii sunt disponibili, regulile împrăștiate sunt jumătate). Rotunjește în sus. Galben. Condus de om, cu sprijinul agentului. Echipa poate folosi agentul pentru task-uri punctuale - teste de caracterizare, generare de documentație, refactoring pe module bine delimitate - dar nu pentru livrare autonomă de feature-uri pe părțile de codebase unde kill signals sunt prezente.

Exemplul trei. O bibliotecă de criptare custom scrisă de un contractor în 2017, nedocumentată, testată doar prin teste de integrare care exersează feature-uri din aval, cuplată strâns de infrastructura de key management, cu reguli de conformitate codificate direct în cod, întreținută în prezent de o echipă în care nimeni nu e specializat în criptografie.

Număr de semnale: cinci (fără teste pe unitatea în sine, fără documentație, cuplare strânsă, constrângeri de reglementare cu logică custom, echipa nu poate evalua). Roșu. Agentul n-are ce căuta în acest codebase. Echipa ar trebui fie să găsească sau să finanțeze expertiză în criptografie, să scrie documentația și testele, și abia apoi să reevalueze. Fie să înlocuiască biblioteca custom cu o bibliotecă standard verificată - ceea ce probabil ar trebui să facă oricum. Pentru codul ăsta, răspunsul nu e agentul; e o practică de inginerie mai bună.

---

Semaforul se aplică la nivel de proiect, nu la nivel de companie. O singură companie va avea simultan codebase-uri verzi, galbene și roșii. Întrebarea nu e „e compania asta pregătită pentru AI”. Întrebarea e „care dintre codebase-urile companiei e pregătit pentru AI azi, și ce ar fi nevoie ca celelalte să treacă într-o altă culoare”.

Cel mai des întâlnit pattern de adopție pe care îl văd: începi cu codebase-urile verzi, ca echipa să capete experiență și încredere; investești în cele galbene ca să le împingi spre verde într-un trimestru sau două; iar pe cele roșii fie le reformezi, fie le scoți din uz, pe un orizont mai lung. Agentul nu e scopul. Scopul e să livrezi software. Agentul e un mijloc.

---

Aplică grila o dată pe portofoliul tău de proiecte. Sortează după culoare. Observă că imaginea e mai nuanțată decât „facem AI” sau „nu facem AI”. Majoritatea companiilor au un mix. Mixul îți spune ordinea operațiilor.

---

Două rafinări apar aproape de fiecare dată când trec o echipă prin semafor.

Prima: semnalele nu sunt binare, iar pragul de două-trei versus patru-sau-mai-multe e o regulă empirică, nu un prag exact. Codebase-urile reale au semnale de intensități diferite. Un codebase cu „teste există, dar sunt parțiale” are jumătate din semnalul unu, nu tot. Un codebase cu „documentație există, dar e parțial învechită” are jumătate din semnalul doi. Eu număr așa: adun valorile parțiale și rotunjesc la întregul cel mai apropiat. Un codebase cu patru jumătăți e un doi. Un codebase cu trei jumătăți și un semnal întreg e un trei. Un codebase cu cinci jumătăți e un trei. Aritmetica e impresionistă; ce contează e ordinul de mărime.

Rafinarea contează pentru că unele echipe se uită la un codebase, numără doar da-urile stricte pe cele opt semnale, obțin unu sau doi și trag concluzia că e verde, când realitatea e mai aproape de galben. Codebase-ul care „tehnic are teste”, dar testele acoperă 10% din cod și sunt de calitate slabă, nu e un codebase verde. Codebase-ul care „tehnic are documentație”, dar documentația e veche de trei ani, nu e un codebase verde. Numără după intensitate, nu după simpla prezență.

A doua: semnalul șase (echipa nu poate evalua output-ul) cântărește mai greu decât celelalte. Un codebase care are zero pe semnalele unu-cinci, dar da pe semnalul șase, e tot un codebase roșu pentru munca respectivă. Golul de capacitate al echipei domină celelalte semnale, pentru că el e cel care produce rezultatele cu adevărat proaste - cod pe care echipa nu-l poate verifica, livrat în producție, unde eșecul are consecințe care se compun. Celelalte semnale produc fricțiune și încetinire. Semnalul șase produce incidente care ajung în raportări de conformitate și în retrospective de incident.

Dacă descoperi că semnalul șase e prezent pentru un anumit tip de muncă, răspunsul nu e „hai să facem codebase-ul mai verde pe celelalte semnale”. Răspunsul e „nu face acest tip de muncă cu agentul, în configurația actuală a echipei”. Fie construiești capacitatea echipei, fie te asociezi cu cineva care o are, fie ții agentul departe de zonele respective. Semnalele sunt un diagnostic; semnalul șase e cel care cere cel mai precis răspuns structural.

---

Încă trei exemple, mai scurte decât primele, acoperă situații pe care primele trei nu le-au atins:

| Proiect | Semnale | Culoare | Lecția |
|---|---|---|---|
| Serviciu API greenfield - fără cod încă, echipă senioră, specificație clară | 0 | Verde-plus | Tratează implicarea agentului ca pe o decizie arhitecturală de prim rang: pregătește AGENTS.md înainte de primul commit, stabilește convențiile cât încă sunt ieftin de schimbat, pune rigoarea testelor în fundație din prima zi. Greenfield-ul e terenul propriu al programării cu agenți, iar câștigul se acumulează pe toată durata de viață a proiectului. |
| Tool intern - 20 de developeri, scris în 2019, teste modeste, expunere de reglementare mică, fără contact direct cu clienții | 1 | Spre verde | Prima țintă corectă pentru o echipă nouă în lucrul cu agenți: suficient de realist ca să te învețe ceva, suficient de delimitat încât o greșeală să nu coste pe nimeni un client. Tool-urile interne sunt terenuri ideale de antrenament; lecțiile se transferă spre codebase-urile cu miză mare, fără miza mare. |
| Fork customizat de la un vendor - strat de contractor făcut în grabă, fără teste sau documentație pe customizări, cuplare severă cu upstream-ul | 4 | Roșu | Diagnosticul ține uneori de codebase și alteori de strategie. Aici întrebarea e dacă stratul custom ar trebui să existe deloc - înlocuiește customizările cu feature-uri din upstream, trimite-le înapoi în upstream ca o contribuție sau întreține-le în mod deliberat, dar nu folosi agentul ca să faci mai repede munca greșită. |

---

**Artefact: Scorecard de pregătire a portofoliului.** Un rând per proiect activ: semnalele punctate, culoarea de semafor, modul recomandat (condus de agent / condus de om / repară întâi codebase-ul).

---

**De pus în practică săptămâna asta.**

Poartă conversația verde/galben/roșu cu tech lead-ul tău. Obține clasificarea oficială a unui proiect. Apără clasificarea cu scorurile de kill signals din scorecard-ul tău de portofoliu.

---

**Încearcă și tu.**

E o autoevaluare pe care o poți rula pe orice proiect în mai puțin de cincisprezece minute. Onestitatea contează mai mult decât scorul; scorul e doar consecința conversației pe care o forțează.

1. Alege un proiect în desfășurare în care echipa dezbate dacă să se sprijine mai mult pe lucrul cu agenți.
2. Pune cele opt kill signals din acest capitol față în față cu proiectul.
3. Pentru fiecare kill signal, întreabă echipa (nu doar pe tine): e adevărat pentru proiectul nostru chiar acum? Marchează fiecare semnal TRIGGERED (declanșat), BORDERLINE (la limită) sau CLEAR (curat). Folosește răspunsurile echipei, nu impresia ta despre ele. Borderline contează ca jumătate.
4. Numără marcajele TRIGGERED. Aplică grila: zero sau unu înseamnă VERDE - lucru condus de agent, la viteză normală. Două sau trei înseamnă GALBEN - condus de om, cu agentul pe task-uri înguste. Patru sau mai multe înseamnă ROȘU - oprești lucrul autonom al agentului în acest codebase până se închid kill signals.
5. Înainte să punctezi, scrie-ți răspunsul din instinct (VERDE, GALBEN sau ROȘU) pe o foaie separată. Compară-l cu rezultatul grilei. Distanța dintre intuiție și grilă e informația care merită păstrată: îți spune ce semnale supraponderezi sau subponderezi sistematic.

Rulează exercițiul trimestrial, după incidentele majore și înainte de orice decizie de a extinde scope-ul agentului către o echipă sau un codebase nou. Semaforul face discuția concretă și comună. „Suntem pe ROȘU pentru că patru semnale sunt TRIGGERED” bate „am o presimțire proastă” în orice ședință care urmează.

Lista concretă de kill signals va avea nevoie de actualizări pe măsură ce domeniul se maturizează. Disciplina punctării - nu.

---

## Capitolul 9
## Pattern-uri pentru codebase-uri brownfield

Semaforul îți spune care codebase-uri sunt pregătite pentru agent. Capitolul ăsta e despre pattern-urile operaționale care fac lucrul cu agenți eficient pe codebase-uri legacy - în special pe proiectele galbene, acolo unde practica contează cel mai mult. Ultimul pattern e excepția; e ceea ce devine posibil când un codebase promovează la verde.

Voi trece prin opt pattern-uri. Primele patru sunt pattern-urile de operare implicite pe care le instalez în majoritatea echipelor brownfield: worktree-uri, championi, hook-uri și review-ul de PR-uri. Ultimele patru sunt pattern-uri de maturitate, pentru echipele care au trecut de primele luni: review-ul jurnalului de greșeli, plasa de siguranță pentru demo (demo-day backstop), watchlist-ul de eșecuri și bucla exterioară (outer loop). Între cele două seturi, un sidebar acoperă guvernanța pentru companiile care vând AI propriilor clienți - o preocupare specifică unui segment, nu un pattern de operare brownfield, dar care merită numită.

Fiecare dintre ele e ceva ce am văzut cu ochii mei făcând diferența între un agent care contribuie și un agent care frustrează.

---

**Pattern-ul unu: worktree-urile.**

Fiecare sesiune de agent rulează în propriul ei git worktree. Un worktree e o copie separată a repository-ului, checked out pe un branch separat. Agentul poate să experimenteze, să eșueze, să reia, să refactorizeze pe worktree-ul lui fără să atingă copia de lucru a nimănui. Când rezultatul e bun, branch-ul trece prin review-ul normal de PR. Când rezultatul e prost, ștergi worktree-ul și o iei de la capăt.

Costul daunelor asupra stării locale, cu worktree-uri: aproape zero. Tentativa ratată a agentului nu atinge niciodată copia ta de lucru - nici pe a altcuiva.

Costul unui eșec fără worktree-uri: agentul se încurcă în lucrul tău local neterminat, strică ceva subtil, iar tu pierzi o oră încercând să-ți dai seama ce s-a schimbat.

Worktree-urile sunt cea mai subapreciată funcționalitate din git pentru lucrul cu agenți. Orice developer dintr-o echipă care programează cu agenți ar trebui să aibă comanda `git worktree add` în reflex. Folosește-le.

---

**Pattern-ul doi: championii.**

O singură persoană din echipă deține [AGENTS.md](https://agents.md/) și jurnalul de greșeli pentru un repository dat. Championul face mentenanța săptămânală: citește ce au adăugat ceilalți developeri în jurnalul de greșeli, refactorizează regulile care s-au adunat, scoate din uz regulile care nu se mai aplică, actualizează convențiile când practica echipei se schimbă.

Championul se rotește trimestrial. Primul champion are costul cel mai mare - el pune pattern-urile pe picioare. Următorii au costul cel mai mic - ei doar întrețin. Rotația previne single-point-of-failure pe tribal knowledge-ul despre „cum folosim noi agenții aici”. Și mai face ceva: distribuie practica; fiecare senior din echipă ajunge la un moment dat la rând, fiecare senior internalizează mentenanța.

Championul nu e singura persoană care editează AGENTS.md. Toată lumea îl editează, prin pull request-uri, când dă peste un pattern nou sau o greșeală nouă. Treaba championului e curatoriatul, nu autoratul. Distincția contează: dacă championul e singurul autor, fișierul devine opinia unei singure persoane despre cum se lucrează cu agenți, iar practica reală a echipei o ia în altă direcție. Dacă toți scriu și championul curatoriază, fișierul reprezintă experiența colectivă a echipei, ținută în frâu de un singur responsabil la un moment dat.

---

**Pattern-ul trei: două feluri de hook-uri.**

hookify (sau plugin-ul echivalent al agentului tău) îți permite să scrii hook-uri care se declanșează înainte de execuția unui tool. Hook-ul citește acțiunea propusă, o evaluează după reguli custom și fie o permite, fie îi cere utilizatorului confirmarea, fie o blochează.

Cazul de utilizare pentru hookify în lucrul brownfield e unul precis. Ai zone din codebase pe care e periculos să le modifici fără review de la un senior - module de criptografie, procesare de plăți, scripturi de migrare de date, orice ține de reglementări. Scrii o regulă hookify care blochează agentul să modifice fișiere din directoarele alea sau care cere confirmare explicită de la utilizator când încearcă. Regula trăiește în repository, versionată în git, aplicată automat la fiecare sesiune.

Regulile hookify completează AGENTS.md. AGENTS.md îi spune agentului convențiile echipei și pattern-urile interzise; agentul le citește și le aplică din oficiu. hookify impune regulile structural; dacă agentul încearcă oricum să le încalce (pentru că LLM-urile mai fac și asta), hook-ul îl prinde. AGENTS.md e rugămintea politicoasă. hookify e granița fermă pe agent. Dar agentul nu e singurul autor cu acces de scriere, iar granița care leagă orice autor e un alt fel de hook.

Pentru proiectele galbene, recomand reguli hookify cel puțin pentru zonele sensibile din punct de vedere al reglementărilor și pentru modulele cu istoric de probleme. Cinci până la zece reguli sunt de obicei suficiente. Fiecare regulă înseamnă o linie de configurare plus o justificare de o linie.

Al doilea fel de hook nu e deloc pe agent. E pe repository. Git rulează hook-uri client-side la commit și la push, iar acestea se declanșează pentru oricine face commit - tu, colegul tău, agentul. Aici stă pârghia. Agentul e doar încă un autor cu acces de scriere, așa că un gate de commit i se aplică gratis, fără nicio cablare specifică agentului. Scrii verificarea o singură dată, pe însuși actul de a face commit, și acoperă deopotrivă codul agentului și pe al tău.

Împarte verificările după cost. Hook-ul pre-commit e trecerea rapidă - formatare, lint, verificare de tipuri, o scanare de secrete - lucrurile care rulează în câteva secunde și n-ar trebui să ajungă niciodată pe un branch. Hook-ul pre-push e trecerea mai grea - suita rapidă de teste, build-ul - pe care ți-o poți permite să o aștepți pentru că rulează o dată la fiecare push, nu o dată la fiecare commit. Ține testele în pre-push; un hook pre-commit trebuie să se termine în câteva secunde, altfel oamenii pun mâna pe portița de scăpare, iar de fiecare dată când sari peste, întărești obiceiul de a sări peste. Gestionează-le pe amândouă dintr-o configurație versionată, printr-un manager de hook-uri, ca hook-urile să se instaleze pentru oricine clonează repository-ul, în loc să stea neversionate în `.git/hooks`-ul unei singure mașini.

Portița de scăpare e `--no-verify`, iar agentul poate pune mâna pe ea la fel ca oricine; închizi ușa aia cu o regulă hookify de deny pe flag. Cele două granițe își acoperă reciproc unghiul mort: hookify prinde agentul în mijlocul sesiunii, înainte ca modificarea să ajungă în cod, iar gate-ul de git prinde orice autor, pe orice cale pe care hookify n-o vede niciodată, în momentul în care se scrie commit-ul. Fii însă cinstit cu privire la ce sunt hook-urile locale. Sunt feedback rapid, nu enforcement - se pot sări, se configurează într-un fișier pe care agentul îl poate edita el însuși și nu sunt neapărat instalate pe o anumită mașină. Aceleași verificări care rulează în CI sunt cele pe care nu le poți sări de pe laptopul tău, iar acea configurație de hook, împreună cu workflow-ul ei de CI, e gate-ul din pattern-ul opt pe care agentul nu-l poate edita. În orice caz, verificările deterministe nu derivează așa cum o pot face reviewerii probabilistici - un scanner de secrete fie găsește cheia, fie nu.

---

**Pattern-ul patru: PR review toolkit.**

Înainte ca un senior engineer să facă review pe un pull request produs de agent, un set de agenți de review trece primul prin diff. Silent failure hunter caută excepții înghițite, retry-uri fără limită, null check-uri lipsă. PR test analyzer identifică metodele noi cu acoperire slabă de teste și recomandă teste concrete de adăugat. Security scanner verifică categoriile standard de vulnerabilități. Documentation reviewer semnalează documentația lipsă sau învechită.

Agenții de review nu înlocuiesc review-ul uman. Rulează înaintea lui și scot la suprafață genul de probleme care se detectează mecanic. Reviewer-ul uman se poate concentra apoi pe lucrurile pe care doar oamenii le pot evalua: corectitudinea de business, potrivirea arhitecturală, deciziile de judecată.

Pârghia stă în timpul economisit pe constatările mecanice. Un senior engineer care face un review de cincisprezece minute prinde bug-urile evidente. Un senior engineer care face un review de cinci minute (pentru că agenții de review au prins deja bug-urile evidente) poate folosi celelalte zece minute pe judecata arhitecturală pe care agenții n-o pot face.

Configurează agenții de review. Leagă-i de fluxul de pull request. Agenții fac munca mecanică; oamenii fac munca de oameni.

O poveste de eșec pentru pattern-ul ăsta, pentru că e singurul cu un mod de eșec pe care celelalte nu-l au. O echipă cu care am lucrat a instalat toolkit-ul complet, și toolkit-ul era bun. Agenții de review prindeau bug-uri reale, săptămână după săptămână, iar reviewerii seniori au învățat să aibă încredere în bifele verzi. Într-un trimestru, review-urile umane de cincisprezece minute deveniseră scanări de trei minute. Nimeni n-a decis asta. Atenția alunecă singură de pe munca ce pare deja făcută.

Apoi a intrat în producție un PR pe care toți agenții îl trecuseră. Teste verzi, zero constatări de securitate, diff curat. Mai aplica și o regulă de discount pe segmentul greșit de clienți - o eroare de corectitudine de business, exact categoria pe care agenții de review n-o evaluează și exact categoria pe care pattern-ul ăsta o rezervă oamenilor. A rulat în producție săptămâni întregi până a scos-o la iveală un tichet de suport.

Post-mortem-ul a fost cinstit: toolkit-ul funcționase exact cum fusese proiectat. Eliminase constatările mecanice din review-ul uman, iar oamenii lăsaseră munca de judecată să se ducă odată cu munca mecanică. Capitolul 10 numește un arhetip - delegatorul necalibrat; aici, o echipă întreagă devenise unul, cu tooling bun pe post de alibi.

Soluția n-a fost scoaterea agenților de review. Soluția a fost un prag uman făcut explicit: un review minim pe corectitudinea de business și pe potrivirea arhitecturală pentru fiecare PR atins de agent, urmărit ca o cifră, lângă rata de defecte; ordinea de citire pentru diff-urile de agent din Capitolul 5 e pragul ăsta făcut concret. Agenții de review sunt un filtru pus în fața judecății umane. Din clipa în care devin un substitut pentru ea, pattern-ul ăsta îți face review-urile mai proaste exact în timp ce le face să arate mai bine.

---

Patru pattern-uri. Worktree-uri. Championi. Hook-uri. PR review toolkit. Niciunul nu cere să inventezi un proces nou. Toate se așază peste felul în care echipele de inginerie livrează deja cod, cu micile completări pe care lucrul cu agenți le cere.

---

**Sidebar: guvernanța pentru companiile care vând AI clienților lor.**

Ăsta nu e un pattern de operare brownfield - e un sfat pentru un anumit segment de public, ținut separat de pattern-urile numerotate tocmai din motivul ăsta. Dacă firma ta vinde capabilități AI propriilor clienți - nu doar consumă AI intern, ci revinde AI ca parte din produs - atunci pattern-ul de guvernanță e diferit față de cel al unui simplu consumator de AI. Demo-urile tale, call-urile de vânzări, proiectele cu clienții sunt toate situații în care disciplina echipei tale e la vedere. Clientul evaluează dacă știi să faci AI responsabil, nu doar dacă AI-ul funcționează.

Asta cere câteva pattern-uri suplimentare, peste cele generale.

Unu: demo-urile n-au voie să sară peste rigoare. Dacă îi arăți unui client cum folosești un agent ca să livrezi cod, îi arăți faza de Research, faza de Plan, faza de Review, faza de Verify. Nu-i arăți doar agentul generând cod și livrându-l, pentru că ăla e demo-ul care creează la client așteptări pe care nu le vei onora în producție.

Doi: AGENTS.md-ul tău e un instrument de vânzare. Clienții vor vrea să vadă ce a codificat echipa ta. Un AGENTS.md bine întreținut, de o sută de linii, cu un jurnal de greșeli care arată lecții reale, e mai credibil decât un AGENTS.md de o mie de linii care pare scris de un consultant. Arată disciplina, nu volumul.

Trei: framework-ul de kill signals e ceva ce îi înveți pe clienți. Grila valorează pentru client mai mult decât orice recomandare punctuală ai face tu, pentru că lentila asta îi permite clientului să-și evalueze singur codebase-urile, fără să depindă de tine. Când dai framework-ul mai departe, întărești relația de încredere. Echipele care țin framework-urile doar pentru ele pierd în fața echipelor care le împărtășesc.

Pattern-urile de mai sus se aplică oricărei echipe. Se aplică însă cu forță dublă echipelor ai căror clienți stau cu ochii pe ele - companiilor la care calitatea ingineriei e o suprafață vizibilă de produs, nu un centru intern de cost. Maturitatea guvernanței face parte din oferta acelor companii, iar disciplina descrisă în manualul ăsta e ceea ce face maturitatea apărabilă.

---

Încă patru pattern-uri. Trei sunt scurte, pentru că apar în echipele funcționale cu care am lucrat chiar dacă se vorbește mai rar despre ele. Al patrulea e materialul cel mai nou din capitolul ăsta și primește spațiul de care are nevoie.

---

**Pattern-ul cinci: review-ul jurnalului de greșeli.**

Jurnalul de greșeli din AGENTS.md e viu. Fiecare intrare e un eșec real prin care a trecut echipa. Dar jurnalul crește în timp, și nu orice intrare rămâne esențială la nesfârșit. Unele eșecuri se rezolvă structural - cauza de fond a fost eliminată printr-un refactoring, dependența a fost înlocuită, convenția a fost internalizată până în punctul în care nimeni n-ar mai face greșeala aia. Intrările astea pot fi retrase fără să pierzi nimic din siguranță, iar retragerea lor ține jurnalul suplu.

Championul rulează un review trimestrial al jurnalului. Pentru fiecare intrare, întrebarea e: a salvat regula asta pe cineva în ultimele trei luni? Dacă da, o păstrezi. Dacă nu, dar regula încă se aplică pe codebase, o păstrezi (regulile care previn eșecuri rare rămân valoroase chiar dacă eșecul nu s-a mai repetat recent). Dacă nu, și regula nu se mai aplică pentru că problema de fond a dispărut, o retragi, cu o notă în mesajul de commit care explică de ce.

Obiceiul ăsta împiedică jurnalul să devină un cimitir. Un cimitir de reguli e aproape la fel de inutil ca lipsa oricărei reguli, pentru că echipa nu mai are încredere în nicio regulă luată individual atunci când sunt prea multe, iar context window-ul agentului se aglomerează cu instrucțiuni perimate.

---

**Pattern-ul șase: plasa de siguranță pentru demo (demo-day backstop).**

Când echipa pregătește un demo de lucru cu agenți - pentru leadership, pentru clienți, pentru un showcase intern - apare tentația de a face demo-ul live, cu agentul lucrând pe bune în fața publicului. Uneori merge. Alteori agentul are o zi proastă, rețeaua sughite, modelul decide să fie neobișnuit de vorbăreț. Demo-urile live cu sisteme probabilistice vin cu un risc real de eșec.

Pattern-ul pe care îl recomand: pregătește o înregistrare de rezervă a aceluiași demo, făcută cu succes dinainte. Dacă demo-ul live intră în probleme, comuți pe înregistrare la secunda treizeci. Publicul nu trebuie să simtă diferența. Lecția ajunge la destinație oricum.

Plasa de siguranță nu e trișare. Plasa de siguranță e execuție profesionistă. Orice vorbitor cu experiență, din orice domeniu, are un plan de rezervă pentru momentul în care partea live cedează. Echivalentul în lumea agenților e o versiune înregistrată a aceleiași munci, ținută la îndemână.

---

**Pattern-ul șapte: watchlist-ul de eșecuri.**

După câteva luni de lucru cu agenți, începi să observi moduri de eșec care se repetă. Anumite tipuri de greșeli pe care agentul le face și pe care trebuie să le corectezi iar și iar. Anumite situații în care workflow-ul se împotmolește. Anumite comportamente ale utilizatorilor care duc la probleme previzibile.

Pattern-ul e să întreții un watchlist de eșecuri - un document care cataloghează aceste moduri de eșec recurente, condițiile în care apar și răspunsul standard al echipei când se întâmplă. Lista crește. Echipa o parcurge împreună cam o dată pe lună. Intrările noi se adaugă; intrările vechi, rezolvate structural, se retrag.

Watchlist-ul e pentru operațiuni ceea ce e jurnalul de greșeli pentru development. Jurnalul de greșeli previne greșelile de cod; watchlist-ul previne greșelile de proces. Amândouă sunt ținute în repository, versionate. Amândouă sunt revizuite regulat. Amândouă sunt felul în care experiența acumulată a echipei devine infrastructură.

---

**Pattern-ul opt: bucla exterioară (outer loop).**

Cele șapte pattern-uri de mai sus presupun un om în cameră. Al optulea e cel la care echipele ajung după câteva luni, când cineva pune întrebarea evidentă: dacă agentul poate rula o buclă disciplinată cât timp mă uit eu la el, de ce mă mai uit? Răspunsul industriei e bucla exterioară - reinvocarea automată a agentului, iterație după iterație, până când o condiție e îndeplinită. Bucla în șase faze din Capitolul 5 e bucla interioară (inner loop): o unitate de lucru, șase funcții, cu tine pe post de gate. Bucla exterioară o învelește. Când o iterație se termină, începe următoarea, și nimeni nu mai stă între ele.

Ideea are o preistorie, iar diferența dintre cele două epoci e toată lecția. În 2023, AutoGPT și BabyAGI învârteau un model în buclă pe baza propriei lui păreri despre progres. Nimic din exterior nu nota o iterație - modelul își corecta singur tema -, așa că fiecare tură amplifica deriva, iar abordarea s-a prăbușit în câteva luni ca mod de a livra software. Renașterea e structural diferită. La mijlocul lui 2025, Geoff Huntley a legat un coding agent într-un while-loop de bash - îi dai un singur fișier de prompt, îl lași să ruleze, repeți la nesfârșit - iar tehnica s-a răspândit sub numele Ralph Wiggum. Fiecare iterație pornește cu un context window proaspăt, face o unitate de lucru și se termină în fața unor evaluatori pe care modelul nu-i controlează: compilatorul, suita de teste, diff-ul. Starea trăiește în repository, nu în conversație. Tot ce face bucla să conveargă stă în afara modelului.

Între sfârșitul lui 2025 și primăvara lui 2026, pattern-ul a încetat să mai fie un truc de bash și a devenit o suprafață de produs. Copilot coding agent de la GitHub a devenit general disponibil în septembrie 2025: deleghi un task, un agent lucrează într-un mediu izolat, iar rezultatul se întoarce ca draft de pull request. Cursor a lansat Cloud Agents în octombrie 2025 - mulți agenți rulând detașat, cu laptopul tău închis. Jules de la Google a adăugat Scheduled Tasks în decembrie, pentru lucrările de mentenanță recurente. Un plugin ralph-wiggum aterizase deja în repository-ul oficial Claude Code în noiembrie, iar până în primăvara lui 2026 bucla ajunsese acolo funcționalitate de prim rang: /loop re-rulează un prompt la un interval dat sau își alege singur ritmul când nu specifici unul, Routines pornesc agenți cloud după un program sau după un eveniment GitHub, /goal ține agentul la lucru până când o condiție de finalizare e îndeplinită, /autofix-pr urmărește CI-ul și împinge fix-uri până când pull request-ul trece pe verde. O singură formă, multe grafii. După testul convergenței din Capitolul 1, capabilitatea a ajuns peste tot - deși ceea ce a ajuns la convergență e un workflow înfășurat în jurul componentelor principale, nu o componentă principală nouă.

Trendul e real, și tot aici disciplina e testată cel mai dur, pentru că bucla exterioară adaugă încercări, nu judecată. Multiplică orice îi permite bucla ta interioară. Dacă fiecare iterație se termină într-un gate strict, bucla acumulează progres: un queue de unități mici și verificate se scurtează peste noapte. Dacă gate-ul e slab, aceeași răbdare acumulează rebut. Numele dat de Huntley acestui mod de eșec e overbaking - ai lăsat-o prea mult „în cuptor”: lași bucla să ruleze după ce și-a terminat treaba și continuă să inventeze muncă pe care n-a cerut-o nimeni. Agentul nu obosește. Ăsta e avantajul - și, nesupravegheat, tot ăsta e pericolul.

Așa că pattern-ul nu e bucla; pattern-ul e contractul sub care o rulezi. Cinci linii, scrise înainte de prima iterație nesupravegheată. **O condiție de oprire pe care o poate evalua o mașină** - queue-ul e gol, suita e verde, bugetul s-a consumat. O buclă fără așa ceva nu e autonomie; e abandon. **Un buget** - tokeni, bani, iterații sau ore, oricare se atinge primul; o buclă nesupravegheată e clientul ideal al modelului de tarifare per token, iar calculele din Anexa A rulează și ele peste noapte. **Un gate pe care agentul nu-l poate edita** - testele, configurația de lint, workflow-ul de CI și regulile hookify stau în spatele unei reguli de deny (pattern-ul trei). Avertismentul din Capitolul 5 - o suită verde scrisă de agent e un indiciu, nu o dovadă - se aplică de două ori atunci când nimeni nu citește indiciile până dimineața. Cel mai ieftin mod în care o buclă ajunge pe verde e să negocieze cu propriul evaluator. **Context proaspăt la fiecare iterație, stare durabilă în repository** - un fișier de queue și un jurnal, ținute în repo prin commit-uri, astfel încât fiecare iterație pornește curată și citește istoria buclei din git, în loc să târască după ea un context care se degradează. Capitolul 5 numea contaminarea contextului drept cel mai mare motiv pentru care sesiunile lungi o iau razna; bucla exterioară făcută corect e un instrument de igienă a contextului - patruzeci de sesiuni scurte și curate în loc de una lungă, în degradare. **Izolare dimensionată pentru absență** - worktree-ul ei propriu (pattern-ul unu), sandbox-ul pornit, fără credențiale de producție, rețea constrânsă. O sesiune nesupravegheată e singurul loc în care prompt injection nu mai întâlnește niciun sceptic uman; straturile din Capitolul 3 nu sunt opționale aici - pe ele se sprijină toată greutatea. Anexa B.6 e contractul ăsta într-o singură pagină.

Ce pui în queue contează la fel de mult ca contractul. Munca eligibilă pentru buclă are multe unități similare, fiecare verificabilă de o mașină, fiecare reversibilă: migrări, curățenii de lint și de typing, dependency bump-uri, completarea testelor de caracterizare, refactorizări mecanice. Munca de design, cu un singur artefact, nu e eligibilă; mai multe încercări nu adaugă judecată, iar bucla îți va cheltui bugetul demonstrându-ți asta. Semaforul din Capitolul 8 se aplică aici cu forță dublă, pentru că bucla exterioară e munca autonomă a agentului în forma ei cea mai concentrată: doar codebase-uri pe VERDE. GALBEN înseamnă condus de om, iar bucla exterioară n-are, prin definiție, niciun om în ea.

Pragul uman nu dispare; se mută dimineața. Producția de peste noapte sosește sub formă de pull request-uri și primește review ca orice pull request - pragul explicit din pattern-ul patru, corectitudine de business și potrivire arhitecturală, nu o privire aruncată pe bife, pentru că tot ce produce o buclă sosește gata îmbrăcat în bife verzi. Iar bucla însăși primește kill signals, aceeași disciplină pe care Capitolul 8 o aplică pe codebase-uri. Patru sunt de ajuns: același diff aplicat și apoi revertat de la o iterație la alta; buget care arde în timp ce queue-ul nu scade; același eșec apărut a treia oară; orice iterație care a atins gate-ul. Oricare dintre ele înseamnă stop - citești jurnalul, repari cauza, abia apoi relansezi. O buclă repornită pe speranță e o buclă pe care ai încetat s-o mai controlezi.

Două extreme arată cât de departe duc echipele chestia asta. Huntley rulează bucla în forma ei brută și o tarifează ca pe un serviciu de utilități - în jur de 10 dolari pe oră. La capătul industrial, fabrica de software de la StrongDM rulează livrare complet non-interactivă, cu oameni care nici nu scriu, nici nu fac review la cod, și cu scenarii end-to-end ținute în afara codebase-ului, ca un holdout set pe care bucla nu-l poate slăbi - la un consum de tokeni pe care Simon Willison l-a estimat la aproape 20.000 de dolari pe lună per inginer. Pattern-ul ăsta stă deliberat între cele două extreme: contract, queue, gate-uri în afara razei de acțiune a agentului și un om care citește pull request-urile dimineața. Nimic din cele nouăzeci de zile ale Capitolului 10 nu cere bucla exterioară; ea e cum poate arăta luna a patra, dacă primele nouăzeci de zile au fost oneste. Supravegheat, plasa de siguranță ești tu. Nesupravegheat, plasa de siguranță e contractul - ceea ce face din bucla exterioară primul consumator al fiecărui control pe care îl instalează manualul ăsta, și testul cel mai curat dacă au fost vreodată instalate cu adevărat.

---

Opt pattern-uri în total. Nu se vor aplica toate fiecărei echipe. Primele patru - worktree-uri, championi, hook-uri, PR review toolkit - se aplică pe scară largă. Următoarele trei - review-ul jurnalului de greșeli, plasa de siguranță pentru demo, watchlist-ul de eșecuri - sunt pentru echipele care au trecut de primele luni. Ultimul - bucla exterioară - e pentru echipele care au trecut de celelalte șapte.

Capitolul următor: framework-ul de adopție - cum începe o echipă care a citit manualul ăsta. Trei roluri, nouăzeci de zile, angajamente concrete.

---

**Artefact: pattern-ul worktree + hook + review.** Cele trei pattern-uri pe care capitolul ăsta le instalează pe orice codebase brownfield: un worktree izolat pentru munca agentului, o pereche de hook-uri - o regulă pre-tool-use pentru acțiunile periculoase și un gate de git la commit/push pentru cele mecanice - și un checklist de review de PR calibrat pe diff-urile generate de agent.

---

**De pus în practică săptămâna asta.**

Configurează un git worktree pe un proiect pe care urmează să trimiți agentul. Folosește worktree-ul pentru munca agentului. Observă izolarea. Prima oară când nu-ți distrugi „din greșeală” starea locală, pattern-ul se fixează.

---

## Capitolul 10
## Adopția: 90 de zile, trei roluri

### Cum faci rollout-ul agenților AI de cod într-o echipă? {#how-to-roll-out}

Închei manualul cu întrebarea practică: de unde începi?

Cele mai multe adopții reușite ale livrării cu agenți din 2025 și 2026 n-au început cu trei roluri. Au început cu un singur inginer care a refuzat să renunțe. Championul care și-a instalat agentul în propriile ore de lucru, care a scris primul [AGENTS.md](https://agents.md/) împotriva scepticismului tăcut al echipei, care a rulat primul architecture review pe un codebase despre care echipa susținuse că nu se pretează, și care s-a întors luna următoare cu un PR funcțional pe care nimeni altcineva nu reușise să-l scrie. Framework-ul cu trei roluri pe care îl descriu mai târziu în acest capitol e versiunea disponibilă atunci când echipa are buget, buy-in din partea managementului și bandwidth-ul să acopere Championul, Lead-ul și Managerul cu oameni diferiți. Majoritatea echipelor cu care am lucrat nu au luxul ăsta la început. Au un singur om, care joacă toate cele trei roluri pe rând, supraviețuind din inerție până când practica devine suficient de reală încât celelalte roluri să poată fi acoperite. Așa că de aici începe capitolul: cu inginerul singur. Versiunea cu trei roluri e cum arată binele după ce ai demonstrat că practica merită investiția.

---

### Majoritatea adopțiilor încep aici: arcul grassroots

Prima dată când am predat grila celor trei roluri, un inginer din ultimul rând a ridicat mâna și a zis: „Compania mea nu arată așa. Managerul meu n-a auzit de AI agentic. Lead-ul meu n-are timp. Sunt singurul om din echipă căruia îi pasă. Eu ce fac?”

Răspunsul cinstit e că arcul ideal cu trei roluri nu funcționează pentru el. Nu are toate cele trei roluri. Modelul s-ar împotmoli în luna a doua, când conversația de procurement n-ar avea cu cine să se întâmple.

Dar există un al doilea arc care funcționează pentru el - și pentru mulții ingineri ca el. L-am văzut reușind de două ori. Îl numesc arcul grassroots: adopția de jos în sus. Arcul grassroots e cum arată de fapt majoritatea adopțiilor în viața reală, nu predarea ordonată a ștafetei între trei oameni diferiți.

Arcul grassroots are altă formă. Championul e inginerul cu curiozitatea. Lead-ul și managerul sunt recrutați mai târziu, după ce championul a strâns dovezile cu care să-i recruteze. Un singur om joacă toate cele trei roluri pe rând - champion în luna unu, lead de facto în luna trei, când i se alătură un coleg, avocat de facto pe lângă management în luna șase, când conversația de procurement se leagă în sfârșit - în loc de trei oameni cu câte un rol fiecare.

Luna unu: championul folosește agentul pentru propria productivitate. Architecture review-uri pe codebase-urile pe care le deține. Schițe de AGENTS.md pentru proiectele unde e autorul principal. Bucla în șase faze pe propriile story-uri. Championul pornește în interiorul politicilor existente, pe muncă pe care o deține deja, pe cât posibil pe căi de cod nesensibile. Nu anunță nicio „transformare AI”. Strânge dovezi, în liniște.

Luna doi: championul pune rezultatele pe hârtie. Story-uri concrete livrate cu agentul. Timp concret economisit. Îmbunătățiri concrete de calitate (sau recunoașterea onestă a locurilor unde agentul n-a ajutat). Materialul e intern - un memo de o pagină sau o prezentare într-un meeting de echipă. Championul nu face pitch de adopție; povestește ce a făcut.

Luna trei: un coleg întreabă cum poate face la fel. Championul îl învață. Cei doi produc împreună un material mai consistent. Își invită tech lead-ul la un walkthrough. Lead-ul, care acum are dovezi și doi ingineri care cer același workflow, pledează mult mai ușor pentru angajamentele la nivel de echipă pe care le cere arcul ideal.

Lunile patru-șase: lead-ul recrutează managerul cu același tipar - dovezi plus cerere venită din echipă. Managerul, care vede acum doi ingineri livrând vizibil mai repede, poartă o conversație de procurement care nu mai presupune să vândă conceptul de la zero.

Până în luna șase, arcul grassroots arată cum arăta arcul ideal în luna trei. A durat de două ori mai mult pentru că championul a trebuit să construiască singur condițiile pentru rolurile de lead și de manager, în loc să le primească de-a gata din prima zi.

Arcul grassroots cere un champion dispus să facă munca lipsită de glorie a productivității personale timp de două luni fără să-l observe nimeni, și apoi munca mai grea de a converti cu răbdare colegi și manageri în următoarele patru. Nu e pentru oricine. Dar pentru inginerii din companiile care nu sunt încă pregătite pentru arcul ideal, arcul grassroots e calea care funcționează - și, din experiența mea, e calea pe care o iau mai multe echipe decât oricare alta.

---

### Compromisul, numit onest

Arcul grassroots pornește mai repede și e fragil la plecarea championului. Dacă singurul inginer care duce practica în spate schimbă echipa sau face burnout înainte ca colegii și managementul să fi fost recrutați, practica moare odată cu el. Arcul ideal cu trei roluri pornește mai încet și rezistă mai bine la schimbările de rol. Dacă championul pleacă în luna a doua a arcului cu trei roluri, lead-ul și managerul continuă munca și recrutează un champion nou; practica supraviețuiește. Dacă championul pleacă în luna a doua a arcului grassroots, nu există nicio practică ce ar putea supraviețui.

Alege arcul care se potrivește situației tale. Dacă managerul tău a auzit de AI agentic, tech lead-ul tău e implicat și există buget pe masă, fă arcul cu trei roluri - plătești startul mai lent cu o practică mai durabilă. Dacă ești singur în povestea asta și singurele resurse pe care le ai sunt propriile ore de lucru și propria disponibilitate de a scrie un memo pe care nu ți l-a cerut nimeni, fă arcul grassroots. E ceea ce funcționează când n-ai ceea ce presupune versiunea ideală.

---

### Versiunea ideală: trei roluri în paralel

Framework-ul pe care îl recomand atunci când echipa are buget și buy-in din partea managementului are trei roluri și un arc de nouăzeci de zile. Rolurile sunt champion, lead, manager. Fiecare vine cu angajamente concrete. Fiecare angajament e suficient de mic încât să încapă pe lângă munca normală; efectul cumulat e suficient cât să mute echipa într-un regim susținut de livrare cu agenți.

Arcul e asimetric, ceea ce surprinde lumea prima dată când îl descriu. Primele treizeci de zile nu produc aproape nicio productivitate măsurabilă. Championul învață, lead-ul clasifică, managerul ține la distanță întrebările premature despre metrici. Echipa investește. Metricile nu vor arăta încă beneficii, iar cei care așteaptă ROI imediat vor fi dezamăgiți.

Următoarele treizeci de zile produc productivitate vizibilă pe proiectul verde. Echipa începe să livreze așa cum am descris în Partea a II-a - Research, Plan, Execute, Review, Verify, Ship. Timpii de ciclu se îmbunătățesc. Calitatea se menține. Reviewerii încep să observe că PR-urile produse de agent sunt mai ușor de citit la review decât erau PR-urile dinainte de agent, pentru că descrierea e mai structurată.

Ultimele treizeci de zile produc efecte care se compun la nivelul întregii echipe. Alți ingineri intră în workflow. AGENTS.md crește. Jurnalul de greșeli acumulează intrări reale. Proiectele galbene încep să se miște spre verde pe măsură ce investițiile structurale dau roade. Conversația de la finalul trimestrului nu mai e „am economisit timp?”, ci „cum scalăm asta?”.

Forma curbei e aproximativ exponențială - mică la început, mai mare la mijloc, consistentă la final. Companiile care măsoară productivitatea la treizeci de zile vor fi dezamăgite. Companiile care măsoară la nouăzeci vor vedea tabloul întreg. Spune-le stakeholderilor despre asimetrie din capul locului; gestionează așteptările în consecință. Framework-ul funcționează; nu funcționează rapid în primele treizeci de zile, și asta prin design.

Cele trei roluri intră în joc la momente diferite, pentru că arcul asimetric o cere. Championul intră primul, pentru că investiția timpurie e tehnică. Lead-ul intră când munca devine vizibilă și are nevoie de decizii la nivel de portofoliu. Managerul închide bucla în luna a treia, când rezultatele trebuie traduse în termeni strategici. Angajamentele fiecărui rol, descrise mai jos, reflectă acest calendar. (În arcul grassroots de mai sus se aplică același arc, doar că un singur om joacă rolurile pe rând - citește angajamentele de mai jos ca munca ce trebuie făcută, nu ca munca pe care trebuie s-o facă trei oameni diferiți.)

```
  Zilele 1-30: Fundația             Zilele 31-60: Extinderea        Zilele 61-90: Operaționalizarea
  -------------------------         -------------------------       -------------------------
  Championul instalează             Lead-ul aduce încă 2-3          Managerul integrează
  AGENTS.md schițat                 ingineri                        metricile în tracking-ul
  Primul proiect pe verde           AGENTS.md consolidat            normal de velocity
  Workflow-ul de architecture       Hooks configurate               Guvernanța de vendor semnată
  review demonstrat                 Skills scrise                   Politica de plugin
                                    Kill signals aplicate           marketplace stabilită
                                    pe portofoliu
  ====================              ====================            ====================
  Champion                          Lead                            Manager
```

*Figura: arcul de adopție de 90 de zile. Fiecare fază are un rol principal și un set principal de artefacte.*

---

**Championul.**

Championul e inginerul care învață primul workflow-ul cu agenți, în profunzime, și îl aduce înapoi în echipă. Championul e de obicei un senior sau staff engineer care are timpul și apetitul să învețe tooling nou cu atenție. Championul nu trebuie să fie cel mai senior om din echipă; trebuie să fie cel mai dispus să investească primele șaizeci de ore.

Angajamentele championului în primele nouăzeci de zile:

Săptămâna unu: instalează agentul. Treci prin workflow-ul de architecture review pe un codebase familiar. Citește ce produce agentul. Corectează ce e greșit. Dă commit artefactului. (Timp: vreo trei ore în total, pe parcursul săptămânii.)

Săptămâna doi: scrie primul AGENTS.md al echipei, în formă de schelet. Sub cincizeci de linii. Pattern-uri interzise, jurnal de greșeli (gol deocamdată), convenții, comenzi de build, unde-găsești-ce. Dă-i commit. Invită echipa să contribuie la el prin pull request-uri. (Timp: vreo cinci ore.)

Săptămânile trei și patru: rulează bucla în șase faze pe trei feature-uri mici. Story-uri care ar lua în mod normal o jumătate de zi. Folosește agentul pe toată bucla. Observă ce merge și ce nu. Documentează fricțiunile în jurnalul de greșeli pe măsură ce dai de ele. (Timp: cam cât ți-ar lua să faci feature-urile de mână; valoarea stă în experiență, nu în timpul economisit la început.)

Luna doi: rulează bucla în șase faze pe trei feature-uri medii. Story-uri care ar lua în mod normal o zi sau două. Continuă să documentezi fricțiunile. Trage și alți ingineri în workflow, pe faze individuale - lasă pe altcineva să facă review-ul planului, lasă pe altcineva verificarea conformității cu specificația. Distribuie experiența. (Timp: din nou, comparabil cu munca manuală, dar echipa construiește cunoaștere comună.)

Luna trei: predă rolul de champion. La finalul celor nouăzeci de zile, cel puțin încă un inginer din echipă ar trebui să poată rula workflow-ul la același nivel de fluență. Championul se rotește; workflow-ul nu mai depinde de championul inițial.

Valoarea championului pentru companie în nouăzeci de zile: echipa are un workflow funcțional de livrare cu agenți, un AGENTS.md întreținut, trei-patru feature-uri livrate care validează abordarea și un succesor desemnat. E un rezultat consistent. Costul: atenția parțială a unui singur inginer, timp de un trimestru.

---

**Lead-ul.**

Lead-ul e tech lead-ul, staff engineer-ul sau engineering managerul care decide ce proiecte primesc agentul și în ce ordine. Lead-ul e paznicul semaforului. Lead-ul e omul care îi spune echipei „proiectul ăsta e verde, trimite agentul; proiectul ăsta e galben, lucrează în pereche cu agentul; proiectul ăsta e roșu, nu-l atinge”.

Angajamentele lead-ului în primele nouăzeci de zile:

Săptămâna unu: clasifică primele cinci proiecte active ale echipei după cele opt kill signals. Dă fiecăruia o culoare. Pune clasificarea pe hârtie. Împărtășește-o echipei. (Timp: vreo două ore.)

Săptămânile doi-patru: pentru câte un proiect de fiecare culoare, documentează ce ar trebui să se schimbe ca să treacă la culoarea următoare. Pentru proiectul verde, documentează de ce rămâne verde (ca echipa să protejeze condițiile). Pentru proiectul galben, documentează cele două-trei reparații structurale care l-ar duce la verde într-un trimestru. Pentru proiectul roșu, documentează dacă răspunsul corect e investiție, înlocuire sau scoatere din uz. (Timp: vreo cinci ore în total.)

Luna doi: urmărește metricile. Cycle time-ul pe munca făcută cu agentul pe proiectul verde. Rata de defecte. Timpul reviewerilor. Orice măsoară deja echipa, plus întrebarea dacă workflow-ul cu agenți mișcă cifrele în direcția așteptată. Cifrele vor fi zgomotoase la început; obiceiul e să măsori oricum, ca să poți avea o discuție reală despre rezultate în luna trei. (Timp: vreo trei ore.)

Luna trei: prezintă rezultatele. Echipei, propriului management, oricui altcuiva trebuie să știe. Rezultate oneste. Dacă agentul livrează conform așteptărilor, spune-o cu date. Dacă nu, spune-o tot cu date și propune ajustări. (Timp: vreo cinci ore, cu tot cu pregătire.)

Valoarea lead-ului pentru companie în nouăzeci de zile: un portofoliu de proiecte clasificat onest, un roadmap pentru mutarea proiectelor galbene spre verde, o grilă de măsurare care desparte hype-ul de realitate și un raport onest despre rezultate, pe baza căruia restul organizației de inginerie poate acționa.

---

**Managerul.**

Managerul e engineering managerul, directorul sau liderul senior care deține bugetul, angajările și procurement-ul. Managerul e rolul pe care cei mai mulți îl uită când planifică adopția de AI agentic. Managerul e omul care decide dacă echipa poate angaja criptograful potrivit pentru problema de la kill signal-ul șase, dacă echipa poate investi un trimestru în mutarea unui proiect galben la verde, dacă echipa poate cheltui pe tooling sau servicii suplimentare.

Faza managerului acoperă zilele șaizeci și unu - nouăzeci, după ce Championul a pus practica pe picioare și Lead-ul a consolidat-o. Munca are trei centre de greutate: procurement (închide decizia de licențiere, ca echipa să nu rămână pe veci pe seat-uri individuale), guvernanță (semnează postura de securitate pe care o redactează Championul) și raportare (traduce rezultatele operaționale în termeni pe care leadership-ul îi va finanța). Niciuna dintre ele nu cere ca managerul să scrie cod sau să ruleze agenți. Toate cer ca managerul să apere granițe: între datele operaționale și promisiunile de ROI, între potrivirea tooling-ului cu utilizarea reală și uniformitatea impusă, între protejarea echipei de metrici premature și pretenția legitimă de dovezi că munca dă roade.

Ce NU face managerul e cel puțin la fel de important. Managerul nu vânează metrici de productivitate per inginer în luna a doua. Managerul nu se angajează la calcule de ROI pe trei ani înainte ca dashboard-ul să aibă măcar un trimestru de date. Managerul nu autorizează benchmark-uri comparative cu alți vendori înainte ca echipa să fi livrat suficient cât să definească ce anume compară. Astea sunt întrebările care omoară adopția când primesc răspuns prea devreme. Treaba managerului e să protejeze echipa de ele în lunile unu-trei, să apere cifra operațională când e solidă și să lase argumentul de venituri în seama celui care deține veniturile.

Până în ziua nouăzeci, rolul managerului s-a mutat de la „pune practica pe picioare” la „urmărește metricile în cadență trimestrială”. Dashboard-ul rămâne. Championul și Lead-ul rămân în rolurile lor. Managerul are capacitate pentru munca trimestrului următor, iar leadership-ul are un plan credibil, ancorat în date operaționale reale din primele nouăzeci de zile, nu în ROI promis pentru următoarele patru trimestre.

---

**Sidebar: un proiect cu 20 de ingineri în servicii financiare, săptămână cu săptămână.**

Un caz concret, ca faza managerului să devină palpabilă. Douăzeci de ingineri software într-o firmă reglementată de servicii financiare. Managerul conduce funcția de inginerie și raportează unui CTO care susține inițiativa, dar e atent la costuri. Board-ul a cerut un update de o pagină, la finalul trimestrului trei, despre investiția echipei în AI. Championul a dus primele treizeci de zile; Lead-ul a consolidat practica în zilele treizeci și unu - șaizeci. Managerul preia sarcina în zilele șaizeci și unu - nouăzeci.

Săptămâna unu a fazei managerului, zilele șaizeci și unu - șaizeci și șapte. Championul și Lead-ul predau un dashboard cu trei metrici: procentul de PR-uri merged care au atins cod generat de agent, cycle time-ul pe acel set de PR-uri față de trimestrul anterior și rata de defecte pe același set față de trimestrul anterior. Cifrele din acest proiect: 41% dintre PR-uri erau atinse de agent în luna a doua. Cycle time-ul pe acele PR-uri a fost cu 28% mai mic decât baseline-ul echipei dinainte de agent; rata de defecte a rămas în marja de zgomot a baseline-ului. Treaba managerului în săptămâna unu e să verifice că metricile sunt reale, nu să le crească.

Săptămâna doi, zilele șaizeci și opt - șaptezeci și patru. Procurement-ul ridică întrebarea seat-uri individuale versus contract enterprise. Echipa e momentan pe seat-uri Pro individuale; managerul trebuie să decidă dacă le consolidează într-un contract Team sau Enterprise înainte de finalul trimestrului. Matematica seat versus enterprise e în Anexa A. Decizia în acest caz a fost nivelul Team pentru 13 din cei 20 de ingineri și seat-uri Pro pentru cei 7 care folosesc agentul rar. Managerul apără împărțirea asta în fața procurement-ului cu argumentul că uniformitatea tooling-ului nu e scopul; scopul e o cheltuială ținută în frâu, potrivită cu utilizarea reală.

Săptămâna trei, zilele șaptezeci și cinci - optzeci și unu. Apare comitetul de securitate. Comitetul a citit despre clasa de injecție prin fișiere de configurare din Claude Code, dezvăluită de Check Point Research la începutul lui 2026 (citarea e în Anexa C), și vrea o postură de guvernanță scrisă. Managerul produce un document de o pagină care numește cele patru puncte de control: hooks, sandbox, vault de secrete, telemetrie. Managerul nu scrie documentul; îl scrie Championul. Managerul îl editează și îl semnează.

Săptămâna patru, zilele optzeci și doi - optzeci și opt. Sosește cererea board-ului. Update-ul managerului are două fraze și un singur număr. „Avem douăzeci de ingineri pe livrare asistată de agenți. Cycle time-ul pe PR-urile atinse de agent e cu 28% sub baseline, fără nicio schimbare măsurabilă în rata de defecte. Continuăm să evaluăm extinderea pe parcursul trimestrului următor.” Managerul nu promite o cifră de venituri; managerul apără cifra operațională și lasă argumentul de venituri în seama CTO-ului.

Ziua nouăzeci. Predarea înapoi către operațiunile curente. Dashboard-ul rămâne. Championul și Lead-ul rămân în rolurile lor.

---

---

### Două arhetipuri de ingineri care omoară rollout-urile dacă nu le numești

Cele trei roluri descriu ce se întâmplă când arcul funcționează. Există însă două arhetipuri de ingineri pe care le vei vedea în orice echipă în timpul adopției și care vor omorî rollout-ul pe tăcute dacă nu le numești cu voce tare.

Arhetipul unu: scepticul de principiu. Seniorul care a mai văzut cicluri de hype AI și nu e convins că ăsta e diferit. Nu va folosi agentul. Nu va scrie AGENTS.md pentru modulele pe care le deține. Va face review la PR-urile conduse de agent cu o ostilitate în plus, căutând dovezi că abordarea e greșită. Două feluri în care iese prost. Echipa începe să lucreze pe lângă el - review-urile lui întârzie PR-urile, modulele lui devin o insulă pe care agentul n-o atinge, codebase-ul se bifurcă în teritorii prietenoase cu agentul și teritorii ostile. Sau scepticul de principiu câștigă disputa politică din interiorul echipei și rollout-ul se blochează. Soluția nu e să-l convertești pe scepticul de principiu. Inginerii seniori și-au câștigat dreptul de a nu fi de acord. Soluția e să-i dai o graniță clară: „modulele tale, regulile tale, agentul nu se atinge de ele; peste tot în rest se aplică standardul echipei”. Și ai grijă ca sarcina lui de review să nu devină bottleneck-ul velocity-ului echipei - dacă fiecare PR condus de agent stă în queue-ul lui, echipa i-a dat scepticului de principiu un drept de veto pe care nu intenționa să i-l acorde.

Arhetipul doi: delegatorul necalibrat. Inginerul (deseori mai junior, alteori mai senior decât te-ai aștepta) care sare peste citirea atentă a output-ului agentului pentru că „agentul o nimerește mereu”. Problema nu e delegarea în sine; problema e calibrarea proastă a momentelor în care să ai încredere și a celor în care să inspectezi. Livrează PR-uri conduse de agent fără să le parcurgă. Defectele se adună, pentru că agentul face greșeli pe care omul le-ar fi prins dacă omul ar fi fost atent. Două feluri în care iese prost. Rata de defecte urcă încet, iar echipa dă vina pe agent, nu pe pasul de review care lipsește. Sau cunoștințele de domeniu ale delegatorului necalibrat se atrofiază, și după șase luni nu mai poate depana sistemul pe care agentul l-a ajutat să-l construiască. Soluția e disciplina de review deja numită: fiecare PR condus de agent primește același review uman ca fiecare PR condus de om, fără excepții. În prima lună, pune-l pe delegatorul necalibrat în pereche cu un reviewer senior care citește output-ul agentului linie cu linie. Calibrează.

Ambele arhetipuri sunt previzibile. Numește-le cu voce tare în rollout. Tratează-le pe fiecare ca pe o problemă structurală cu o soluție structurală, nu ca pe un defect de caracter. Echipele care fac asta țin ambele arhetipuri în joc, productive. Echipele care n-o fac îl pierd pe scepticul de principiu într-o rebeliune tăcută și pe delegatorul necalibrat într-o erodare lentă a judecății.

---

### Vendorul va avea o săptămână proastă

O realitate operațională pentru care rollout-ul trebuie să aibă un plan: agentul nu va fi mereu disponibil. Căderile la vendor se întâmplă. Limitările de capacitate se întâmplă. Modelul pe care îl folosești azi e scos din uz, iar înlocuitorul nu e încă stabil. Am văzut velocity-ul unei echipe înjumătățindu-se timp de o săptămână pentru că modelul lor principal era rate-limited în timpul unui incident regional de capacitate, și nu se gândiseră deloc ce fac atunci când bottleneck-ul e chiar agentul. Și căderile nu sunt plafonul: în iunie 2026, cel mai nou tier flagship al celui mai mare vendor a fost retras la nivel mondial la câteva zile după lansare și a rămas indisponibil aproape trei săptămâni. Echipele care își mutaseră deja workflow-urile pe el și-au rulat planurile de fallback pe bune; echipele fără fallback și-au redescoperit setup-ul anterior pe deadline.

Ce pui la punct. Un fallback non-agentic pentru munca cea mai sensibilă la timp. Seniorul care încă poate livra un hotfix la trei dimineața, când modelul e rate-limited. Runbook-ul pentru „ce facem când Claude Code e throttled și clientul așteaptă”. Acceptarea faptului că în unele săptămâni velocity-ul echipei scade pentru că vendorul a avut un incident, la fel cum în unele săptămâni scade pentru că o bază de date a avut un incident.

Nu construi o echipă care nu poate funcționa fără agent. Construiește o echipă al cărei velocity în regim normal presupune agentul și al cărei velocity în regim de fallback presupune că o săptămână doar-cu-oameni e de supraviețuit. Agentul e infrastructură. Ca orice infrastructură, are uptime, iar planul de continuitate al echipei trebuie să țină cont de downtime.

---

Trei roluri. Champion. Lead. Manager. Fiecare cu angajamente concrete. Niciunul full-time. Toate indispensabile. Niciunul complet fără celelalte.

Cel mai frecvent eșec de adopție pe care îl văd e echipa care are champion, dar n-are lead. Championul învață workflow-ul, îl rulează pe câteva proiecte, dar nu poate convinge echipa să-l aplice consecvent, pentru că nimeni nu ia deciziile la nivel de proiect despre unde merge agentul. Championul ajunge să facă singur toată munca cu agentul, ceea ce nu scalează, iar agentul rămâne catalogat drept „interesant, dar limitat”.

Al doilea cel mai frecvent eșec e echipa care are champion și lead, dar fără implicarea managerului. Munca tehnică merge bine. Procurement-ul stă blocat două luni așteptând avizul de la legal. Bugetul pentru inițiativa de documentare nu se alocă. Proiectele galbene rămân galbene pentru că nu există investiție. Clasificarea făcută de lead era corectă; n-a avut cumpărător.

Al treilea eșec, mai rar dar real, e echipa care are lead și manager, dar n-are champion. Lead-ul înțelege modelul. Managerul a alocat buget. Nimeni de pe partea de inginerie n-are experiența hands-on ca să ruleze workflow-ul. Echipa e angajată teoretic în livrarea cu agenți și blocată practic.

Toate cele trei roluri. Toate cele trei seturi de angajamente. Nouăzeci de zile. Arcul e real, munca e delimitată, rezultatele sunt măsurabile.

---

Aplică framework-ul ăsta. Pornește cronometrul. Întoarce-te peste nouăzeci de zile și spune-mi cum a mers.

Echipele care urmează arcul ăsta vor fi, peste doi ani, echipele al căror avans s-a compus timp de doi ani. Echipele care au ales un tool, l-au integrat neglijent și au așteptat să apară productivitatea vor fi echipele care spun „am încercat AI și n-a mers”.

Tu alegi în ce fel de echipă ești.

---

**Artefact: board-ul de rollout pe 90 de zile.** Un whiteboard sau un document partajat cu câte un lane pentru fiecare rol (Champion, Lead, Manager) și cele patru familii de artefacte (CLAUDE.md / AGENTS.md, hooks, skills, dashboard de metrici). Folosește-l ca board de lucru pentru rollout, nu ca slide de prezentare.

---

**De pus în practică săptămâna asta.**

Alege-ți rolul - champion, lead, manager. Fă săptămâna asta primul angajament din checklist-ul rolului respectiv. Pune acțiunea în calendar. Arcul începe în momentul în care evenimentul există în calendarul cuiva.

---

# Încheiere - Un mod de a gândi care supraviețuiește tool-urilor

Închei manualul acolo unde a început: cu o afirmație despre durabilitate.

Tool-urile concrete pe care le-am numit pe parcurs - Claude Code, Codex CLI, opencode, Superpowers, hookify, Understand Anything, diversele plugin-uri și marketplace-uri - vor arăta cu totul altfel până când i-ar veni rândul următoarei ediții a manualului. Unele vor fi fost scoase din uz. Altele vor fi fost rebranduite. Altele vor fi fost absorbite în produse mai mari. Marketplace-ul însuși va fi trecut prin sute de oferte concurente. Vor apărea jucători noi. Liderii de azi vor cădea.

Ce ai învățat din manualul ăsta nu sunt tool-urile. Ce ai învățat e un mod de a gândi care supraviețuiește tool-urilor.

Arhitectura pe care ai învățat-o în Partea I e invariantă - controlul capabilității. Componentele principale - context window, tool-uri, Permisiuni / Sandbox, skill-uri, plugin-uri, MCP, Memory, subagenți - plus harness-ul care le organizează. Majoritatea agenților de cod de nivel de producție converg spre anatomia asta. Agenții de cod care vor apărea în următorul deceniu vor lua, în cele mai multe cazuri, o formă similară, pentru că anatomia e dictată de natura muncii, nu de vendor. Când evaluezi un agent nou, parcurgi lista, pui întrebarea pentru fiecare componentă principală și ai răspunsul. Lista e deschisă; vor apărea componente principale noi pe măsură ce agenții mari converg spre mecanisme noi.

Metoda pe care ai învățat-o în Partea a II-a e invariantă - controlul workflow-ului. Trecerea de la a genera cod la a formula munca limpede e intuiția fundamentală. Bucla în șase faze e o implementare a disciplinei formulării; vor apărea și alte implementări. Pattern-ul AGENTS.md - cod versionat în repo, care codifică convențiile echipei ca agentul să le citească - va exista sub alte nume în alte tool-uri, dar principiul e permanent: disciplină sub formă de cod, nu de tradiție orală.

Realitatea pe care ai învățat-o în Partea a III-a e invariantă - controlul adopției. Kill signals sunt proprietăți ale codebase-urilor și ale echipelor, nu ale tool-urilor care lucrează pe ele. Semaforul e o regulă de decizie valabilă indiferent ce agent se întâmplă să folosești trimestrul ăsta. Arcul adopției - champion, lead, manager, nouăzeci de zile - e același arc pentru orice tranziție de tooling care atinge serios practica de inginerie. Tooling-ul concret se schimbă; framework-ul de change management nu.

Trei invariante, trei controale. Cuvântul înainte numea livrarea de software cu agenți o problemă de control, nu de tooling. Zece capitole mai târziu, ăsta e în continuare tot argumentul.

Dacă lași manualul din mână, instalezi agentul momentului și rulezi workflow-ul exact cum l-am descris, vei obține valoare. Instrucțiunile sunt suficient de concrete cât să le urmezi literal.

Dacă lași manualul din mână, îți însușești framework-ul arhitectură-metodă-realitate și îl aplici oricăror tool-uri îți ies în cale în următorul deceniu, vei obține mult mai mult. Framework-ul e activul. Instrucțiunile concrete sunt doar exemplul lucrat.

---

O singură reflecție, ușor pe lângă subiectul restului manualului.

Echipele pe care le-am văzut reușind cu livrarea cu agenți au în comun o proprietate pe care niciun framework din manualul ăsta nu ți-o poate instala. Iau munca în serios. Investesc în agent așa cum ar investi într-un coleg junior - onboarding, infrastructură comună, bucle de feedback, răbdare cu greșelile. Echipa care tratează agentul ca pe un tool petrece șase luni evaluând tool-uri și nu se angajează niciodată. Echipa care adoptă postura de investiție petrece șase luni construind infrastructură comună și ajunge la o relație de lucru care supraviețuiește hopurilor inevitabile.

Asta e postura pe care Cuvântul înainte o numea o convenție de încadrare, și aici se vede ce aduce ea concret. Agentul e software; încadrarea drept coleg de echipă n-a fost niciodată o afirmație despre natura lui. Fă investiția și rezultatele operaționale se compun în timp. Sari peste ea și agentul rămâne un tool, cu randamente de tool.

---

Înapoi la cele nouă secunde. PocketOS a pierdut o bază de date de producție în timpul cât îți ia să citești propoziția asta. Fiecare strat al metodologiei din manual exista în 2026 și ar fi putut fi pus în funcțiune la PocketOS în lunile dinaintea incidentului. Niciunul nu era. Ăsta e golul pe care manualul încearcă să-l închidă: golul dintre metodologia care există și metodologia care chiar se aplică.

Echipele pe care le-am văzut parcurgând arcul adopției descriu toate aceeași schimbare. Înainte să existe practica, discuția era „ar trebui să adoptăm AI agentic?”. După, discuția era „care codebase-uri sunt pregătite, care nu, ce ar trebui să se schimbe ca să mutăm galbenele pe verde, cine e championul, cine e lead-ul, cine e managerul”. Nivelul discuției urcă un etaj. Echipa nu mai evaluează tool-uri și începe să se evalueze pe sine.

Asta e schimbarea pe care am încercat s-o construiesc pentru tine cu manualul ăsta. Nu tool-ul anume. Nici măcar modelele anume, deși metodele sunt utile. Schimbarea în felul în care gândești munca.

Dacă manualul și-a făcut treaba, n-o să ai nevoie de o ediție revizuită peste doi ani. Vei ști cum să absorbi orice aduc următorii doi ani fără să-ți pierzi echilibrul. Asta e durabilitatea pe care metodele au fost menite s-o producă de la bun început.

---

Dacă iei o singură practică din manualul ăsta, ia workflow-ul de review de arhitectură și framework-ul lui de diagnostic din Capitolul 7. E testul cu cel mai mic cost pentru a afla dacă munca cu agenți va reuși pe codebase-urile tale. Rulează-l o dată și câștigul rămâne al tău.

Dacă iei un singur framework, ia kill signals și semaforul din Capitolul 8. Ele sunt regula care îți permite să spui da acolo unde agentul ajută și nu acolo unde nu ajută. „Nu”-ul contează la fel de mult ca „da”-ul.

Dacă iei o singură orientare filozofică, ia postura „framework-ul supraviețuiește tool-ului”. Tool-urile se vor schimba. Felul în care gândești munca se compune în timp. Investește în modul de a gândi.

---

Fraza la care mă întorc ori de câte ori explic munca asta e una pe care o tot împrumut de la mine însumi de ani buni, pornită dintr-un gând pe care l-am avut prima dată acum vreo zece ani.

Să înțelegi problema devine mai important decât să scrii codul.

Era adevărat când a programa însemna să perforezi cartele. Era adevărat când IDE-ul a înlocuit editorul de text. Era adevărat când coding-ul asistat de AI a trecut pragul de la autocomplete la redactarea de cod. E adevărat și acum, când scrisul a rămas în seama agenților.

Ăsta e lucrul durabil. Modelele pe care le-am așezat în manualul ăsta sunt schelăria din jurul lucrului durabil. Te vor ajuta să ajungi de unde ești acum până acolo unde poți livra software cu agenți într-un mod pe care îl poți apăra. Că folosești exact tool-urile pe care le-am numit, sau altele, sau tool-uri care încă nu s-au construit - nu contează. Tu acoperi partea care durează.

Tool-urile se vor schimba. Harness-urile se vor îmbunătăți. Numele modelelor din ediția asta vor îmbătrâni. Dar munca durabilă rămâne aceeași: înțelege problema, formulează munca, constrânge execuția, verifică rezultatul. Secvența asta e întreaga problemă de control - și n-a aparținut niciodată tool-urilor. Îți aparține ție.

Agenții scriu codul. Tu înțelegi problema. Asta e competența pe care n-o automatizează nimeni.

---

## Mulțumiri

Mulțumesc că ai citit.

Dacă ai întrebări, comentarii sau povești din propria adopție - reușite sau eșecuri - aș vrea să le aud. Următoarea ediție a manualului, peste doi-trei ani, va reflecta ce au învățat echipele între timp. Experiența ta e input-ul de care am cea mai mare nevoie.

-- Mihai Cvasnievschi

București, 2026

---

## Despre autor {#about-the-author}

Forma unui manual depinde de forma celui care îl scrie, iar tu meriți să știi dacă experiența autorului e genul de experiență care se potrivește cu situația ta.

Am dat prima oară de un calculator în biroul părinților mei, prin 1984, pe la șase ani - o sală de mainframe cu podea înălțată, Space Invaders rulând pe un terminal și o inițiere în BASIC. Primele programe le-am scris în BASIC, în 1989. A urmat Borland Pascal sub DOS, în 1993, cu assembly pe lângă, pentru bucățile la care limbajul nu ajungea, apoi Visual Basic - primul IDE adevărat pe care l-am folosit și primul limbaj în care am vândut software, încă adolescent. Cariera profesională mi-a început în 2000, ca IT Manager într-o companie de producție industrială. În 2001 am trecut la inginerie software propriu-zisă, într-un startup care construia software de multicasting pentru operatori de satelit pe DVB. Când startup-ul și-a pierdut investitorii și a pivotat spre outsourcing, am trecut de la C++ la .NET și mi-am petrecut următoarele două decenii, până în 2023, livrând pentru clienți din industrii diverse pe Visual Studio.NET și pe urmașii lui. În paralel cu munca pe .NET am livrat cod de producție în C, Java, JavaScript, Go și Python, în echipe și pe linii de produs diferite, inclusiv pe target-uri embedded - expunerea poliglotă care a făcut, mai târziu, ca paralela despre anatomia agenților din Capitolul 2 să-mi vină natural la scris. Sunt, prin formație și prin înclinație, întâi inginer și abia apoi consultant; consultanța a crescut firesc din faptul că fac inginerie alături de echipe care vor ajutor.

Interesul pentru machine learning mi-a apărut prin 2013. Primul deep dive serios a venit la finalul lui 2015, când am portat DarkNet și YOLO pe un headset XR; de atunci construiesc aplicații AI profesionist. În 2023 m-am alăturat unei companii care construia primul SoC neuromorfic, lucrând pe zona de nano-ML a domeniului. Pe partea de coding asistat, am folosit fiecare generație: Visual Assist de la Whole Tomato (primul asistent de cod inteligent pe care l-am instalat vreodată), tooling-ul timpuriu de la JetBrains în lumea .NET, primele versiuni de Copilot și LLM-uri pentru cod din ziua în care a apărut ChatGPT. Nu mi-am construit propriul coding agent. I-am folosit însă pe majoritatea celor care există acum și am văzut multe echipe folosindu-i.

Manualul se sprijină pe traiectoria asta. Metodologia pe care o descriu a fost rafinată de-a lungul a două decenii de proiecte de inginerie - și, mai recent, cu echipe care adoptă concret livrarea de software cu agenți. Framework-urile pe care le împărtășesc sunt cele care au rezistat în ambele contexte; cele care n-au rezistat au fost scoase la pensie. Nu e primul set de framework-uri pe care îl scriu despre livrarea cu agenți. E a treia sau a patra iterație. Iterațiile de dinainte au greșit în feluri interesante. Asta e, sper, mai puțin greșită.

Nu sunt neutru pe subiectul ăsta. Cred că livrarea de software cu agenți e schimbarea cu cele mai mari consecințe din domeniul nostru de la apariția limbajelor de programare de nivel înalt încoace. Mai cred și că felul în care o adoptă acum majoritatea echipelor le face mai mult rău decât bine. Ambele pot fi adevărate în același timp. Rostul manualului e să te ajute să adopți într-un fel care păstrează câștigul fără pagube. Framework-urile sunt mijlocul.

Traiectoria asta - patru decenii de scris cod, douăzeci și cinci dintre ele profesionist, mai bine de un deceniu de construit sisteme AI, fiecare generație de asistent de cod între ele - e traiectoria din care e scris manualul. Calibrează-ți așteptările în consecință.

<a id="contact"></a>
*Contact: [info@ship-it-with.ai](mailto:info@ship-it-with.ai) pentru discuții tehnice sau workshopuri personalizate, în persoană sau online, croite pe codebase-ul și pe constrângerile echipei tale. Mă găsești pe [LinkedIn](https://www.linkedin.com/in/mihaicvasnievschi/). Pentru audiențe executive și de leadership non-tehnic, practica-soră de la [ai-leaders.ro](https://ai-leaders.ro) acoperă partea de adopție fără profunzimea inginerească.*

---

## Changelog {#changelog}

Pagina asta urmărește actualizările semnificative ale manualului. Corecturile mărunte și ajustările de SEO nu sunt listate; footer-ul arată data ultimei actualizări.

### 2026-07-17 - Pasul de actualitate și corecturi din iulie

Un fact-check în profunzime al fiecărei afirmații datate, față de ce arată public în iulie 2026, cu verificare adversarială pe fiecare constatare. Corecturi: povestea post-mortem-ului din 23 aprilie e re-sursată - regresiile recunoscute de Anthropic sunt 4 martie (effort), 26 martie (caching) și 16 aprilie (plafonul de verbozitate), în timp ce atribuirea către adaptive thinking din februarie și auditul pe 6.852 de sesiuni îi aparțin Stellei Laurenzo de la AMD, publicate pe 6 aprilie, înaintea post-mortem-ului; jumătatea scrisă de agent a componentei principale Memory urcă de la semnal de pionierat la convergență deplină (GitHub Copilot Memory a precedat Auto Memory; Codex CLI a urmat în aprilie); Dreaming e corectat ca feature la nivel de platformă, nu o comandă de CLI livrată; subagenții paraleli din Codex, corectați de la opt la cei șase documentați; sistemul de subagenți din Cursor, re-datat la 2.4; repository-ul opencode, actualizat la anomalyco/opencode; adoptarea ralph-wiggum, re-datată în noiembrie 2025; corecturi mai mici de date (patch-ul Adversa, /loop). Actualitate: ferestrele de context (un milion de tokeni e acum gama medie), avertismentul propriu al METR din februarie 2026, telemetria care converge ca OpenTelemetry, tranziția Gemini CLI către Antigravity CLI. Adăugiri: soft-delete-ul de 48 de ore și accesul de agent cu scop limitat introduse de Railway după PocketOS (Capitolul 3), suspendarea tier-ului flagship din iunie 2026 ca exemplu de săptămână proastă a vendorului (Capitolul 10), CVE-urile de sandbox-escape DuneSlide ca mențiune onestă pe stratul doi (Capitolul 3), vectorul de injecție cu payload împărțit prin DNS TXT și mitigarea `sandbox.credentials`. Nota despre afirmațiile datate, actualizată la iulie 2026.

### 2026-07-06 - Diagrame SVG și corpuri de figuri localizate

Trei figuri trec de la layout-uri cu carduri la SVG adaptat temei: bucla în șase faze își desenează acum topologia reală (șase noduri, săgeți și cele două rute de eșec înapoi la Plan), cele cinci straturi de guvernanță se afișează ca un zid de apărare în adâncime, iar arcul de 90 de zile devine o cronologie cu etichete de rol. Toate cele cinci figuri au acum corpuri localizate în ediția română (înainte se traduceau doar legendele), iar etichetele învechite CLAUDE.md din figura arcului au fost corectate în AGENTS.md, ca să corespundă textului. Doar prezentare; conținutul figurilor rămâne neschimbat.

### 2026-07-05 - Cum faci review pe un diff de agent (Capitolul 5 + Anexa B.8)

Faza de Review din Capitolul 5 capătă jumătatea ei umană, inserată după cei doi revieweri-agent și înainte de Verify - citirea pe care doar un om o poate face, pe care cartea o invocase drept pragul uman fără s-o predea vreodată. Pornește de la de ce un diff de agent eșuează diferit ca natură, nu ca grad: un diff de om eșuează la execuție și vânezi greșeala linie cu linie, în timp ce un diff de agent compilează, trece de lint și se citește idiomatic, eșuând în schimb la intenție și context. Așa că ordinea de citire se inversează în cinci pași - diff-stat-ul raportat la plan înainte de orice cod, testele citite pentru ce afirmă, granițele despre care echipa are reguli, un grep pe fiecare nume nou pe care diff-ul îl introduce, și abia apoi linie cu linie, unde minutele merg către corectitudinea de business și potrivirea arhitecturală. Linia de calibrare o ancorează: fluența nu e corectitudine, iar un bug de agent arată ca acel cod pe care un inginer bun l-ar scrie pentru un task ușor diferit. Anexă nouă: B.8, one-pager-ul cu ordinea de citire a unui diff de agent (numărul de template-uri ajunge acum la opt). Pattern-ul patru din Capitolul 9 capătă o trimitere înapoi de încheiere, care numește ordinea asta de citire drept pragul uman făcut concret.

### 2026-07-05 - Igiena contextului (Capitolul 5 + Anexa B.7)

Capitolul 5 capătă o secțiune de igienă a contextului, inserată după paragraful de vocabular inner/outer loop, care predă meșteșugul zilnic pe care cartea îl numise, dar nu-l predase niciodată - fereastra e memoria de lucru a agentului, iar tot ce e încărcat în ea concurează cu raționamentul. Numește cele patru semne ale contaminării (agentul răspunde din nou la o întrebare deja rezolvată, citează o versiune învechită a unui fișier pe care l-a editat, uită o constrângere pe care o respecta sau scade în calitatea editărilor târziu într-o sesiune lungă), disciplina graniței dintre sesiuni - o unitate de muncă per sesiune, cu stare durabilă recitită din repository - și compactarea ca predare, nu continuare, unde tot ce nu e scris într-un fișier până atunci s-a pierdut. Anexă nouă: B.7, one-pager-ul igienei contextului (numărul de template-uri ajunge acum la șapte). Secțiunea despre context window din Capitolul 1 capătă o trimitere înainte, de o frază, către noua secțiune.

### 2026-07-05 - Exemplul lucrat din Anexa A

Anexa A capătă o trecere lucrată prin propria ei grilă, închizând singurul gol dintr-o carte construită pe exemple lucrate: secțiunea de costuri nu avea niciun număr. Noua subsecțiune ia proiectul de 20 de ingineri din servicii financiare din sidebar-ul managerului (Capitolul 10) și îl trece prin anexă - 13 seat-uri Team plus 7 seat-uri Pro, lista TCO cu patru categorii și euristica de încadrare - folosind cifrele operaționale publicate ale proiectului (41% dintre PR-urile merged atinse de agent, cycle time cu 28% sub baseline, defecte plate) drept ancoră de valoare. Tarifele de pe partea de cost sunt marcate ca numere rotunde ilustrative, nu cotații, în acord cu poziția anexei că prețurile concrete se învechesc trimestrial. Concluzia cinstită încape într-un tabel mic: prețul de listă e cea mai mică linie, iar categoriile de timp uman o pun în umbră. Încheierea ține granița din Capitolul 10: managerul apără cifra operațională, nu un ROI proiectat.

### 2026-07-05 - Două feluri de hook-uri (Capitolul 9, pattern-ul trei)

Pattern-ul trei din Capitolul 9 se extinde de la regulile hookify la două feluri de hook-uri: hook-ul pre-tool-use al agentului (hookify) și hook-ul de git pre-commit/pre-push. Materialul nou leagă gate-ul de git de faptul că agentul e doar încă un autor cu acces de scriere: un gate determinist de commit/push i se aplică gratis, iar portița `--no-verify` e închisă cu o regulă hookify de deny. Trage și linia cinstită - hook-urile locale sunt feedback rapid, în timp ce aceleași verificări în CI sunt gate-ul pe care nu-l poți sări de pe laptop, adică gate-ul din pattern-ul opt pe care agentul nu-l poate edita. Recap-ul, încheierea și caseta de artefact actualizate; numărul de pattern-uri rămâne opt.

### 2026-06-11 - Orchestrare scriptată a subagenților (`/workflows`)

Secțiunea despre subagenți din Capitolul 1 capătă un paragraf despre orchestrarea programatică: /workflows din Claude Code, care pune agentul să scrie un script determinist ce trimite subagenți pe faze, cu fan-out în paralel sau prin pipeline și predări validate prin schemă, cu un gate de verificare. Încadrat pe linia tezei cărții - nu o componentă principală nouă, ci o comoditate la nivel de harness peste componenta principală subagent, unde determinismul e singura diferență reală față de dispatch-ul condus de model (de pildă, un plugin în stil Superpowers). Datat la mijlocul lui 2026.

### 2026-06-10 - Bucla exterioară (pattern-ul opt)

Capitolul 9 capătă un al optulea pattern, care acoperă trendul outer-loop - re-invocarea agentului la interval, după un program sau dintr-un queue, până când o condiție e îndeplinită. Pattern-ul trasează filiația (buclele cu auto-evaluare din 2023; Ralph Wiggum la mijlocul lui 2025; valul de agenți de background și programați lansați de vendori la finalul lui 2025; bucla ca suprafață de prim rang până în primăvara lui 2026) și instalează controalele: un contract de buclă în cinci linii, testul de eligibilitate pentru buclă, patru kill signals de buclă și pragul minim al review-ului de dimineață. Capitolul 5 primește paragraful de vocabular inner/outer loop. Anexă nouă: B.6, one-pager-ul cu contractul outer-loop (numărul de template-uri ajunge la șase). Cinci intrări noi în Anexa C, sub un grup nou de surse despre outer loop și autonomie. Nota despre afirmațiile datate, actualizată la iunie 2026.

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

## Anexa A - Economia costurilor

### Cât costă programarea cu agenți? {#how-much-does-it-cost}

A doua cea mai frecventă întrebare a managerilor de inginerie, după „merge?”, e „cât costă?”. Prețurile concrete se schimbă în fiecare trimestru; grila de calcul nu. Pune numerele echipei tale în structura de mai jos.

### Nivelurile de preț

Trei modele de preț domină piața, cam în această ordine a complexității:

**Per-seat.** Tarif fix per inginer pe lună, indiferent de utilizare. Predictibil. Ieftin pentru utilizatorii ocazionali, scump pentru power user-ii care rulează agentul toată ziua.

**Per-token (consum măsurat).** Plătești pentru tokenii de input pe care îi citește agentul și pentru tokenii de output pe care îi produce, însumați pe toate sesiunile. Corect pentru utilizatorii ocazionali; nimicitor pentru inginerul care rulează trei sesiuni de agent în paralel, zece ore în șir.

**Enterprise.** Angajament anual negociat, care împachetează seat-uri plus o alocare de tokeni plus suprafața de conformitate (Zero Data Retention, acces la log-urile de audit, capacitate dedicată, SSO, BAA-uri semnate). Amortizează ambele extreme și adaugă ce cer industriile reglementate.

### Euristica de încadrare

Costul per inginer pe lună al unui tool de programare cu agenți ar trebui să se încadreze în ce ar fi cheltuit oricum echipa ta pe tooling similar: licențe de IDE, platforme de code intelligence, abonamente de coding asistat de AI, plus o fracțiune din valoarea orelor economisite pe săptămână de un inginer senior. Dacă costul lunar total per inginer al agentului depășește cu mult intervalul ăsta de referință, calculul are șanse mici să iasă, indiferent de vendor. Dacă se încadrează confortabil în interval, calculul are șanse mici să nu iasă.

Fă calculul pentru echipa ta. Ia stack-ul actual de tooling, costul orar complet al inginerilor tăi, o estimare onestă a numărului de ore pe săptămână pe care li le va economisi agentul și oferta per-seat sau per-token a vendorului. Pragul de break-even vine repede de îndată ce agentul economisește chiar și câteva ore pe lună per inginer.

### Ce nu intră în prețul de listă

Oferta vendorului e partea ușoară. Patru categorii nu apar în ea și domină TCO-ul real.

**Integrarea.** Scrierea skill-urilor custom, configurarea hook-urilor, instalarea serverelor MCP pentru sistemele interne. Investiție unică de câteva săptămâni de engineering; se amortizează pe toată durata folosirii agentului.

**Timpul de scris skill-uri.** Întreținerea [AGENTS.md](https://agents.md/), scrierea și actualizarea skill-urilor pe măsură ce codebase-ul evoluează. Continuu; de regulă câteva ore per inginer pe lună, plus timp concentrat din partea championului echipei (Capitolul 10).

**Timpul de review.** Review-ul output-ului agentului. Mai puțin per schimbare decât review-ul codului scris de mână, în majoritatea cazurilor, dar nu zero - și concentrat pe umerii reviewerilor seniori.

**Overhead-ul de guvernanță.** Evaluarea de securitate prin CISO. Negocierea addendum-ului de Zero Data Retention. Durata ciclului de achiziții. Infrastructura de audit logging. Monitorizarea riscului de vendor. Variază de la companie la companie; de la o săptămână la un trimestru.

### Un exemplu lucrat {#a-worked-example}

Sidebar-ul managerului din Capitolul 10 a lăsat o echipă de 20 de ingineri din servicii financiare la mijlocul arcului: 41% dintre PR-urile merged atinse de agent în luna a doua, cycle time pe acel set cu 28% sub baseline-ul dinainte de agent, defecte în marja de zgomot. Trece aceeași echipă prin grila din anexa asta. Cifrele de cost de mai jos sunt numere rotunde pentru aritmetică, nu cotații - pune-le pe ale tale; tot rostul anexei e că cele concrete se învechesc până la trimestrul următor.

Începe cu prețul de listă, partea ușoară. Proiectul a pus 13 ingineri pe nivelul Team și 7 pe seat-uri Pro, pentru că acei 7 folosesc agentul rar, iar nivelul s-a potrivit cu utilizarea (ideea din Capitolul 10: cheltuială ținută în frâu, nu tooling uniform). La un preț ilustrativ de $30 per seat Team și $20 per seat Pro, adică 13 seat-uri a câte $30 plus 7 a câte $20, iese $530 pe lună, să zicem $6.400 pe an. Notează cifra asta. E cea mai mică de pe pagină.

Acum cele patru categorii care nu sunt în prețul de listă, la magnitudinile pe care cartea le folosește deja:

| Linie | Magnitudine ilustrativă | Cadență |
|---|---|---|
| Seat-uri (13 Team + 7 Pro) | ~$530/lună (~$6.400/an) | recurent |
| Integrare | câteva săptămâni de engineering | o singură dată |
| Scrierea skill-urilor | câteva ore per inginer pe lună, plus trimestrul part-time al championului | continuu + o singură dată |
| Review | concentrat pe reviewerii seniori | continuu |
| Guvernanță | o săptămână până la un trimestru, concentrat la început într-o firmă reglementată | o singură dată |

Pune un preț pe liniile umane cu aceeași onestitate. Câteva săptămâni de engineering pentru integrare, la orice cost complet realist, acoperă singure prețul de listă pe primul an, o dată. Scrierea skill-urilor - câteva ore per inginer pe lună pe 20 de ingineri, plus trimestrul part-time al championului - e o linie recurentă care poate ajunge mai mare decât seat-urile însele. Timpul de review cade pe reviewerii seniori, cele mai scumpe ore ale tale. Guvernanța într-o firmă reglementată înseamnă o săptămână până la un trimestru de muncă de securitate, achiziții și audit logging înainte să fie facturat vreun seat. Prețul de listă e real, dar nu acolo sunt banii.

Partea de valoare folosește euristica de încadrare în sens invers. Ia un inginer la un cost complet ilustrativ de $100 pe oră. Un seat Team de $30 e acoperit când agentul îi economisește inginerului cam douăzeci de minute pe toată luna; câteva ore economisite pe lună nici nu se pun. Seat-ul își trece propriul prag devreme și ușor. Dar calculul ăsta pe dosul plicului nu e ce a justificat cheltuiala. Ce a justificat-o a fost cifra operațională pe care managerul o avea deja: 41% dintre PR-urile merged atinse de agent, cycle time pe ele cu 28% sub baseline, rata de defecte plată. Ore măsurate la ieșire, nu dolari proiectați.

Asta e disciplina. Prețul de listă e cea mai mică linie și cea despre care întreabă toată lumea prima dată. Cele patru categorii de TCO domină totalul real, iar cele umane pun în umbră toată matematica seat-urilor. Iar cifra pe care managerul o apără în fața board-ului e cea operațională - cycle time cu 28% mai mic, fără nicio schimbare măsurabilă în defecte - nu un ROI proiectat pe care dashboard-ul încă nu-l poate susține (Capitolul 10). Prețurile se schimbă; aritmetica asta, nu.

### Prețurile se schimbă; matematica nu

Prețurile concrete din orice trimestru vor fi greșite în trimestrul următor. Forma calculului, nu. Per-seat scalează cu mărimea echipei; per-token scalează cu intensitatea utilizării; planurile enterprise le împachetează pe amândouă, plus conformitatea. Euristica de încadrare și lista TCO cu patru categorii supraviețuiesc oricărei schimbări de preț. Intră în discuția de achiziții din secțiunea managerului din Capitolul 10 cu propriile numere puse în grila asta.

---

## Anexa B - Template-uri

Opt template-uri de copiat și lipit, la care se face referire pe tot parcursul manualului. Toate sunt puncte de plecare; adaptează-le pentru echipa ta.

Template-urile B.1 și B.2 rămân integral în engleză: sunt artefacte pe care le consumă agentul, iar prompturile se scriu în engleză.

### B.1 Promptul de architecture review

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

### B.2 Scheletul AGENTS.md

Template-ul funcționează fie ca [AGENTS.md](https://agents.md/) (standardul neutru față de vendor), fie ca CLAUDE.md (varianta Claude Code). Numele fișierului diferă de la agent la agent; formatul markdown, nu.

```
# AGENTS.md

## Forbidden patterns
- Never construct SQL by string concatenation. Use bound parameters. (Reason: SQL injection.)
- Never log PII fields. (Reason: data minimization compliance.)
- Never roll your own cryptography. Use the team's approved crypto wrapper. (Reason: AES-CBC with hardcoded IV shipped to production in 2024; we are not doing that again.)
- Never modify migration history. Migrations are append-only.

## Mistake journal
- 2026-03-03: agent generated JPQL query that bypassed the multi-tenant filter. Fix: queries extend MultiTenantQueryBuilder base class which enforces tenant filtering. Rule added.

## Conventions
- Constructor injection only, not field injection.
- @Transactional only on service methods that mutate state.
- Repositories extend BaseRepository<Entity>.
- DTOs at controller boundary use Bean Validation.

## Build and test
- Build: mvn clean verify
- Run tests: mvn test
- Run linting: mvn spotless:check
- Run security scan: mvn dependency-check:check

## Where things live
- Services: src/main/java/com/team/service/
- Repositories: src/main/java/com/team/repository/
- DTOs: src/main/java/com/team/dto/
- Tests: src/test/java/com/team/ (parallel package structure)
- Migrations: src/main/resources/db/migration/ (Flyway)

## Domain glossary
- "Customer" = end user. "Counterparty" = corporate client.
- "Transfer" = intra-bank or inter-bank. "Wire" = inter-bank only.
- "Hold" = short-term reservation. "Block" = long-term legal restriction.
```

### B.3 Checklist-ul buclei în șase faze (one-pager)

```
RESEARCH
- Agentul produce nota de research (2-4 pagini)
- Nota numește: fișierele de atins, convențiile de urmat, riscurile, întrebările deschise
- Review uman: se potrivește cu modelul meu mental despre munca asta?

PLAN
- Agentul produce un plan la nivel de fișier, fiecare task de 2-5 minute
- Planul numește schimbările de teste pentru orice schimbare de cod
- Planul spune ce înseamnă „gata” pentru întreaga modificare, nu doar per task
- Review uman: vreun task prea vag, prea mare, ordonat greșit? Ridică obiecții. Aprobă.

EXECUTE
- Agentul trimite subagenți per task, în context izolat
- Fiecare subagent: citește, implementează, verifică, raportează
- Orchestratorul integrează rezultatele
- Dacă un task eșuează: orchestratorul decide retry / ocolire / escaladare

REVIEW (doi revieweri, în ordine)
- Reviewerul de conformitate cu specificația: implementarea respectă spec-ul?
- Reviewerul de calitate a codului: e cod bun, după standardele echipei?

VERIFY
- Testele noi rulează. Testele existente rulează (ca parte din execute).
- Pentru UI: Playwright cu accessibility tree, nu pixeli.
- Niciun „done” fără dovezi din teste.

SHIP
- Mesaj de commit structurat + push + PR cu descriere structurată
- Revieweri etichetați conform CODEOWNERS
- Tichetul Jira legat e actualizat; Slack e notificat
- Pull request-ul trece prin review-ul normal al echipei
```

### B.4 Fișa de punctare a kill signals

```
Pentru fiecare codebase, punctează fiecare semnal: 0 (semnal absent) / 0.5 (parțial) / 1 (semnal prezent).

Semnalul 1 - Fără teste
- 0: > 70% line coverage ȘI testele rulează la fiecare commit
- 0.5: 30-70% coverage SAU testele există, dar nu rulează de rutină
- 1: < 30% coverage SAU nicio suită de teste automate

Semnalul 2 - Fără documentație
- 0: document de arhitectură la zi + comentarii în cod + decision records
- 0.5: documentație parțială, posibil învechită
- 1: nicio privire de ansamblu arhitecturală; doar autorul original știe

Semnalul 3 - Cuplare strânsă
- 0: granițe clare între module; modulele pot fi schimbate izolat
- 0.5: ceva cuplare; developerii cu experiență se descurcă, dar noii veniți se chinuie
- 1: ghem; editezi un fișier, se sparg alte trei

Semnalul 4 - Reguli de business împrăștiate
- 0: o singură sursă de adevăr pentru fiecare regulă de business
- 0.5: ceva duplicare, dar documentată
- 1: aceeași regulă exprimată în 3+ locuri, adesea inconsistent

Semnalul 5 - Constrângeri de reglementare
- 0: controale standard; mecanismul de audit existent acoperă schimbările
- 0.5: domeniu reglementat, dar echipa are workflow-ul pus la punct
- 1: controale stricte + echipa nu are un workflow integrat; matricele de sign-off lipsesc

Semnalul 6 - Echipa nu poate evalua output-ul
- 0: echipa are expertiză senior pentru fiecare domeniu din codebase
- 0.5: expertiza senior există, dar e fragilă (o singură persoană, posibil indisponibilă)
- 1: echipa nu poate evalua fiabil output-ul agentului într-un anumit domeniu

Semnalul 7 - Potrivirea model-context
- 0: codebase-ul e într-un limbaj/framework popular, cu amprentă publică substanțială
- 0.5: nișă, dar suficient de documentată cât agentul să aibă ceva context
- 1: DSL proprietar, framework intern sau limbaj rar, fără corpus public

Semnalul 8 - Viteza schimbării
- 0: framework-ul și dependențele sunt stabile; nicio migrare majoră în desfășurare
- 0.5: churn de versiuni minore în curs, dar echipa ține situația sub control
- 1: migrare majoră la jumătate; codebase-ul stă călare pe versiunea veche și pe cea nouă

Rotunjește la cel mai apropiat întreg.

Semaforul:
- 0-1: VERDE (lucrul condus de agent e potrivit)
- 2-3: GALBEN (condus de om, cu sprijinul agentului)
- 4+: ROȘU (repară întâi codebase-ul)

Semnalul 6 cântărește mai greu: orice codebase cu 1 la semnalul 6 e ROȘU pentru munca afectată, indiferent de restul semnalelor. Ține agentul departe de munca aceea până când golul de competență e închis.
```

### B.5 Calendarul de adopție în 90 de zile (one-pager)

```
CHAMPION (inginerul cu curiozitate)

Luna 1
- Săptămâna 1: instalează agentul. Architecture review pe un codebase familiar. Dă commit artefactului.
- Săptămâna 2: schițează primul AGENTS.md al echipei, < 50 de linii.
- Săptămânile 3-4: rulează bucla în șase faze pe trei feature-uri mici.

Luna 2: rulează bucla în șase faze pe trei feature-uri medii. Atrage alți ingineri în faze individuale.

Luna 3: predă rolul de champion unui succesor. AGENTS.md e acum al echipei, nu al championului.

---

LEAD (decide ce proiecte primesc agentul)

Săptămâna 1: clasifică top 5 proiecte după cele 8 kill signals. Pune clasificările pe hârtie. Împărtășește-le echipei.

Săptămânile 2-4: pentru câte un proiect din fiecare culoare, documentează ce ar trebui să se schimbe ca să-l muți.

Luna 2: urmărește metricile. Cycle time, rată de defecte, timp de reviewer.

Luna 3: prezintă rezultatele. Date oneste. Recomandă ajustări.

---

MANAGER (deține bugetul, achizițiile, angajările)

Lunile 1-2: protejează echipa. Fără metrici de productivitate per inginer, fără
proiecții de ROI, fără benchmark-uri de vendor deocamdată. Practica abia se construiește.

Zilele 61-67: preia handoff-ul de la Champion/Lead. Verifică dacă metricile din
dashboard sunt reale (ponderea PR-urilor atinse de agent, cycle time vs baseline, rata defectelor vs baseline).

Zilele 68-74: închide decizia de achiziție seat-vs-enterprise cu grila din
Anexa A. Potrivește nivelul cu utilizarea, nu cu uniformitatea.

Zilele 75-81: one-pager-ul de guvernanță (hook-uri, sandbox, secrete, telemetrie).
Championul schițează; managerul editează și semnează.

Zilele 82-90: update către leadership - două fraze și un număr. Apără
metrica operațională; lasă veniturile în seama cui deține veniturile. Treci la
o cadență trimestrială.

---

ARCUL GRASSROOTS (pentru echipe care nu au toate cele trei roluri)

Luna 1: championul folosește agentul doar pentru productivitatea personală. Fără anunțuri.
Luna 2: championul își pune rezultatele pe hârtie. Le prezintă în ședința de echipă.
Luna 3: un coleg întreabă cum. Championul îl învață. Demo-ul în doi ingineri invită lead-ul.
Lunile 4-6: lead-ul recrutează managerul cu baza de dovezi a celor doi ingineri.

De două ori mai lung decât arcul ideal; merge în companii care nu sunt încă pregătite pentru cel ideal.
```

### B.6 Contractul outer-loop (one-pager)

```
Înainte de orice rulare nesupravegheată, completează fiecare linie. O linie goală înseamnă că bucla nu e gata.

MUNCA
- Queue: ______ (fișier sau listă de issue-uri în repo; câte o unitate mică, similară, reversibilă per element)
- Eligibilitate: codebase VERDE (scor B.4 0-1) / fiecare unitate verificabilă de mașină / fiecare unitate revertibilă

CONDIȚIA DE OPRIRE (evaluabilă de mașină; bucla se oprește singură)
- Done când: ______ (queue gol / suita verde / N unități gata de review)
- Buget: max ______ tokeni sau $______ sau ______ iterații sau ______ ore - ce se atinge primul
- Regula de eșec: aceeași unitate eșuează de două ori -> sari peste ea și marcheaz-o; trei unități sărite -> oprește tot

FIECARE ITERAȚIE
- Context proaspăt; starea se citește din queue + jurnalul din repo, nu din istoricul sesiunii
- O unitate per iterație; termin-o sau notează în jurnal de ce nu - nimic lăsat aplicat pe jumătate
- Gate: ______ (teste / lint / typecheck / build) rulează în afara razei agentului (CI sau hook)
- Reguli de deny: agentul nu poate edita configurația de teste, configurația de lint, workflow-ul de CI, regulile de hook sau marker-ele de done din jurnal

IZOLARE
- Worktree și branch propriu; niciodată branch-ul default
- Sandbox pornit; fără credențiale de producție în environment; rețea oprită sau pe allowlist

REVIEW-UL DE DIMINEAȚĂ (pragul uman minim)
- Fiecare PR e citit pentru corectitudine de business și potrivire arhitecturală - nu bifat din ochi
- Verificarea de kill înainte de relansare: diff-uri care oscilează? buget consumat, dar queue-ul nu e mai scurt?
  același eșec a treia oară? gate-ul a fost atins?
  Orice „da” -> nu relansa. Citește jurnalul, repară întâi cauza.
```

### B.7 Igiena contextului (one-pager)

```
ÎNCĂRCARE
- Doar context relevant pentru task; tot ce e încărcat concurează cu raționamentul
- Pointere, nu payload-uri: linkuiește documentul de arhitectură, numește fișierele, nu le lipi
- AGENTS.md sub 200 de linii - stratul mereu-încărcat e spațiul cel mai scump

SESIUNE
- O unitate de muncă per sesiune
- Pornește curat la fiecare unitate; nu duce istoricul unui task terminat în următorul
- Starea durabilă trăiește în fișiere - nota de research, planul, jurnalul - ținute în repo prin commit-uri

DE URMĂRIT (semne de contaminare)
- Agentul răspunde din nou la o întrebare rezolvată deja în sesiune
- Agentul citează o versiune învechită a unui fișier pe care l-a editat mai devreme
- Agentul uită o constrângere pe care o respecta mai devreme
- Calitatea editărilor scade târziu într-o sesiune lungă

CÂND E CONTAMINAT
- Nu te certa cu sesiunea - nu poți readuce o fereastră la coerență prin dispută
- Dă commit la starea durabilă -> încheie sesiunea -> pornește de la zero
- Sesiunea proaspătă recitește progresul din repo, fără zgomot

COMPACTARE
- O predare, nu o continuare - rezumarea pierde detalii
- Tratează-o ca pe predarea muncii unui inginer nou
- Tot ce contează și nu e într-un fișier până atunci s-a pierdut

SUBAGENȚI
- Izolează fiecare task în propriul context; confuzia unui task nu ajunge niciodată la următorul
- Citește rezumatele de predare cu scepticismul cu care ai citi standup-ul unui junior
```

### B.8 Ordinea de citire a unui diff de agent (one-pager)

```
ÎNAINTE DE COD
- Diff-stat-ul raportat la plan, întâi - citește forma înainte de o linie de cod
- Schimbarea atinge ce a numit cererea, și doar atât?
- Fișierele pe care planul nu le-a numit niciodată sunt primul semnal - un diff care depășește scopul a decis ceva în locul tău

ÎNTÂI TESTELE
- Citește ce afirmă, nu dacă trec - verdele e semnalul pe care îl ai deja
- Aserțiunea trebuie să vină din intenție, nu din implementare
- Un test scris pornind de la cod va fi de acord cu codul

GRANIȚE
- Verifică regulile pe care echipa le-a scris - pattern-urile interzise din AGENTS.md, convențiile de strat
- Agentul încalcă o convenție sigur pe el și în stil fluent
- O trecere de graniță arată curat pe pagină - stilul fluent o ascunde de cititul pe stil

NUME NOI
- Dă grep pe fiecare API, funcție sau cheie de config pe care diff-ul o introduce și pe care n-o recunoști
- Zero rezultate în codebase sau în dependențe -> numele s-ar putea să nu existe
- Apelul inventat se citește la fel de plauzibil ca cel real

ABIA APOI LINIE CU LINIE
- Stratul mecanic pe care agenții de review l-au măturat deja - conformitatea cu spec-ul, calitatea codului
- Nu le repeta trecerea - cheltuiește minutele pe care ți le-au cumpărat
- Minutele merg unde agenții nu pot: corectitudinea de business și potrivirea arhitecturală

CALIBRARE
- Fluența nu e corectitudine
- Un bug de agent arată ca acel cod pe care un inginer bun l-ar scrie pentru un task ușor diferit
- Citirea umană devine mai scurtă și mai ascuțită pe măsură ce tooling-ul se îmbunătățește - niciodată sărită
```

---

## Anexa C - Surse și lecturi suplimentare

Anexa asta există pentru că fiecare afirmație din manual merită o sursă verificabilă, dacă vrei să mergi pe fir până la capăt. Am organizat intrările după afirmație, nu după sursă, ca să poți porni de la un pasaj din corpul cărții și să ajungi la dovezile din spatele lui. Intrările sunt grupate pe categorii (studii, incidente cunoscute, vulnerabilități cu versiuni de patch, documentația tool-urilor, marketplace-uri, surse pentru componenta principală Memory, surse pentru componenta principală Permisiuni / Sandbox, surse despre bucla exterioară și autonomie), iar fiecare intrare are aceeași formă: afirmația, sursa, unde anume e folosită în manual și orice avertisment care merită știut.

### Studii și cercetare

**Afirmația:** Dezvoltatorii open-source experimentați care au folosit asistență AI pe repo-uri pe care le cunoșteau bine au fost cu 19% mai lenți decât aceiași dezvoltatori fără ea, deși estimaseră în prealabil că vor fi cu 24% mai rapizi - un decalaj de 43 de puncte între accelerarea așteptată și încetinirea măsurată, care a persistat în auto-evaluările lor chiar și după ce datele i-au contrazis.
**Sursa:** Becker et al., METR, "Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity," July 10, 2025. arXiv: [arxiv.org/abs/2507.09089](https://arxiv.org/abs/2507.09089). Articol: [metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/). Schimbarea de design a follow-up-ului: [metr.org/blog/2026-02-24-uplift-update/](https://metr.org/blog/2026-02-24-uplift-update/).
**Unde e folosită:** Capitolul 4 (De la cod generat la software livrat).
**Atenție:** Studiul a testat asistența AI brută (Cursor + Claude), fără o variabilă pentru disciplina formulării. Interpretarea că disciplina de workflow e variabila lipsă îmi aparține mie, nu studiului. Follow-up-ul METR de la sfârșitul lui 2025 a suferit un selection bias sever (dezvoltatorii refuzau tot mai des randomizarea fără AI) și a produs doar estimări slabe; METR a anunțat un experiment reproiectat pe 24 februarie 2026 și avertizează împotriva extrapolării cifrei de 19% la tool-urile actuale.

---

### Incidente cunoscute

**Afirmația:** Pe 24 aprilie 2026, PocketOS și-a pierdut baza de date de producție în nouă secunde, când un agent Cursor bazat pe Claude Opus 4.6 a invocat Volume Delete de la Railway printr-un API token găsit pe parcurs, în timpul unei încercări de recuperare după o nepotrivire de credențiale. Backup-urile, stocate pe același volum, au fost distruse odată cu datele primare.
**Sursa:** Reported by DevOps.com ("When AI Goes Really, Really Wrong"), Business Insider (Jer Crane statement), and others. Anthropic's Claude Opus 4.6 system card (February 2026) describes the model that powered the agent.
**Unde e folosită:** Prolog (Nouă secunde) și Capitolul 3 (Guvernanța în straturi).
**Atenție:** Cronologia recuperării diferă între relatările publice - restore-ul făcut de Railway ar fi durat ~30 de minute după ce Crane i-a contactat, în timp ce alte relatări vorbesc de ~30 de ore sau două zile până la restaurarea operațională completă. Folosesc incidentul pentru pattern-ul de guvernanță, nu ca reconstituire criminalistică exactă. Urmarea: pe 29 aprilie 2026, Railway a anunțat că toate ștergerile de volume și resurse - până atunci instantanee când erau invocate prin API - fac acum soft-delete cu o fereastră de recuperare de 48 de ore, alături de guardrails la nivel de workspace și acces de agent cu scop limitat ([blog.railway.com/p/your-ai-wants-to-nuke-your-database](https://blog.railway.com/p/your-ai-wants-to-nuke-your-database)).

---

**Afirmația:** La sfârșitul lui februarie 2026, Alexey Grigorev de la DataTalks.Club a pierdut doi ani și jumătate de infrastructură de cursuri, când Claude Code a lucrat pe un state file Terraform rămas în urmă și a rulat `terraform destroy` peste ce a interpretat el drept resurse orfane.
**Sursa:** Public account by Alexey Grigorev (DataTalks.Club), late February 2026.
**Unde e folosită:** Capitolul 3 (Guvernanța în straturi).
**Atenție:** Pierderea de date a fost parțială; AWS a restaurat aproximativ 1,94 milioane de rânduri dintr-un snapshot, în circa o zi. Incidentul e documentat public, dar cu mai puțină acoperire decât PocketOS. Follow-up-ul lui Grigorev documentează întărirea adoptată după: delete protection și în Terraform, și în AWS, starea mutată în S3, review manual al fiecărui plan distructiv și un tier de suport AWS mai ridicat.

---

**Afirmația:** Post-mortem-ul tehnic al Anthropic din 23 aprilie 2026 („An update on recent Claude Code quality reports”) a recunoscut trei regresii: effort-ul implicit de reasoning coborât de la high la medium pe 4 martie (revenit pe 7 aprilie), un bug de caching din 26 martie care golea istoricul de raționament la fiecare tur în loc de o dată pe oră de inactivitate (reparat pe 10 aprilie, v2.1.101) și un plafon de verbozitate în system prompt din 16 aprilie, care a produs o scădere măsurată de ~3% a calității (revenit pe 20 aprilie). Separat și mai devreme, Stella Laurenzo, Senior Director la AMD, a publicat un audit independent (6 aprilie, depus ca issue GitHub anthropics/claude-code#42796) pe 6.852 de sesiuni Claude Code și 234.760 de tool call-uri, care arăta trecerea de la un comportament research-first la unul edit-first pe măsură ce ascunderea thinking-ului a crescut de la 1,5% la 100% dintre tururi, atribuind degradarea în parte rollout-ului din februarie al lui adaptive thinking activat implicit.
**Sursa:** Post-mortem-ul de engineering Anthropic, 23 aprilie 2026: [anthropic.com/engineering/april-23-postmortem](https://www.anthropic.com/engineering/april-23-postmortem). Auditul Laurenzo: issue-ul GitHub anthropics/claude-code#42796; acoperire în The Register, 6 aprilie 2026.
**Unde e folosită:** Capitolul 4 (De la cod generat la software livrat).
**Atenție:** Atribuirea către rollout-ul de adaptive thinking din februarie îi aparține lui Laurenzo, nu vendorului; cele trei cauze recunoscute de post-mortem încep în martie. Cele două relatări coincid pe regresii și diverg pe cauza cea mai timpurie.

---

### Vulnerabilități cu versiuni de patch

**Afirmația:** Claude Code era vulnerabil la remote code execution prin fișiere de proiect din surse nesigure: fișiere `.mcp.json` sau `.claude/settings.json` malițioase, din repo-uri în care nu aveai încredere, puteau executa hook-uri înainte de dialogul de trust, deschizând calea spre RCE.
**Sursa:** Check Point Research, February 2026. CVE-2025-59536. NVD: [nvd.nist.gov/vuln/detail/CVE-2025-59536](https://nvd.nist.gov/vuln/detail/CVE-2025-59536). Articol: [research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/).
**Unde e folosită:** Capitolul 3 (Guvernanța în straturi); menționată și în Capitolul 10 (Adopția, scena cu comitetul de securitate).
**Atenție:** Dezvăluită și patch-uită în Claude Code v1.0.111 (octombrie 2025); articolul Check Point a apărut în februarie 2026. Versiunile dinaintea patch-ului rămân vulnerabile; clasa de probleme supraviețuiește chiar și după patch-ul specific.

---

**Afirmația:** Claude Code era vulnerabil la exfiltrarea de API key-uri prin injecție de configurație: setări controlate de atacator, care suprascriau `ANTHROPIC_BASE_URL` înainte de promptul de trust, puteau scurge API key-urile.
**Sursa:** Check Point Research, February 2026. CVE-2026-21852.
**Unde e folosită:** Capitolul 3 (Guvernanța în straturi).
**Atenție:** Patch-uită în Claude Code v2.0.65. Aceeași clasă ca CVE-2025-59536: execuția configurației de proiect nesigure înainte de trust.

---

**Afirmația:** Claude Code încarcă automat fișierele `.env*` din directorul de lucru la începutul sesiunii, fără permisiunea explicită a utilizatorului, expunând secretele în contextul agentului.
**Sursa:** Knostic, December 2025. Blog: [knostic.ai/blog/claude-loads-secrets-without-permission](https://knostic.ai/blog/claude-loads-secrets-without-permission).
**Unde e folosită:** Capitolul 3 (Guvernanța în straturi), numită în clasa de vulnerabilități de auto-încărcare a fișierelor dot-env.
**Atenție:** Mitigarea e un `denyRead` în sandbox pe pattern-urile `.env*`, nu un patch de la vendor; în iunie 2026, Claude Code a adăugat o setare opt-in `sandbox.credentials`, care blochează comenzile din sandbox de la citirea fișierelor de credențiale și a variabilelor de mediu secrete - un control mai țintit pentru aceeași clasă, tot opt-in, nu implicit. Comportamentul se poate schimba în versiunile viitoare; clasa de probleme (agenți care încarcă config local la începutul sesiunii) rămâne valabilă.

---

**Afirmația:** Regulile de deny din Claude Code erau ocolite în tăcere atunci când o comandă de shell înlănțuia mai mult de 50 de subcomenzi (plafon dur MAX_SUBCOMMANDS_FOR_SECURITY_CHECK = 50), verificarea de securitate retrogradând la un prompt generic de "ask".
**Sursa:** Adversa AI Red Team, disclosed April 1, 2026. Articol: [adversa.ai/blog/claude-code-security-bypass-deny-rules-disabled/](https://adversa.ai/blog/claude-code-security-bypass-deny-rules-disabled/).
**Unde e folosită:** Capitolul 3 (Guvernanța în straturi), ca exemplul de bypass prin plafonul parserului pentru ideea că "orice strat luat individual poate avea un mod de eșec silențios".
**Atenție:** Patch-uită în Claude Code v2.1.90 în primele zile ale lui aprilie 2026 - writeup-ul Adversa consemnează fix-ul până pe 4 aprilie, la câteva zile de la dezvăluire. Clasa - straturi de guvernanță cu plafoane de parser care cedează în tăcere - e ce trebuie să-ți rămână în minte după ce plafonul specific dispare.

---

**Afirmația:** Parserele de permisiuni din coding agents recunosc doar un set cunoscut de comenzi de shell pentru citit fișiere; agenții care invocă `open()` din Python, `fs.readFile` din Node sau orice binar nerecunoscut ocolesc complet regulile de deny.
**Sursa:** Adam Kinney, April 2026. Articol: [Claude Code's Deny Rules Don't Protect You - Here's What Actually Does](https://adamkinney.com/aatt/claude-code/deny-rules-dont-protect-you-sandbox-does/).
**Unde e folosită:** Capitolul 3 (Guvernanța în straturi), ca o clasă de bypass al parserului de permisiuni.
**Atenție:** Problemă arhitecturală, nu un CVE punctual. Mitigarea e lista `denyRead` din sandbox-ul de la nivel de OS (la nivel de kernel), nu un patch de la vendor. Clasa persistă de la un patch la altul, pentru că parserul nu poate enumera fiecare binar existent.

---

**Afirmația:** Două vulnerabilități zero-click de prompt injection în sandbox-ul Cursor - CVE-2026-50548 și CVE-2026-50549 (CVSS 9.8, botezate „DuneSlide”) - abuzau allowlist-ul de scriere pe directorul de lucru și un fallback de rezolvare a symlink-urilor ca să evadeze din sandbox și să ajungă la remote code execution la nivel de OS. Toate versiunile dinainte de Cursor 3.0 (2 aprilie 2026) erau afectate; 3.0 le-a reparat pe ambele.
**Sursa:** Cato Networks (Cato AI Labs), dezvăluite la mijlocul lui 2026. Writeup: [catonetworks.com/blog/duneslide-two-critical-rce-vulnerabilities/](https://www.catonetworks.com/blog/duneslide-two-critical-rce-vulnerabilities/); acoperire: SecurityWeek, The Hacker News, iulie 2026.
**Unde e folosită:** Capitolul 3 (Guvernanța în straturi, stratul doi).
**Atenție:** Lecția e clasa, nu vendorul: și cel mai puternic strat poate avea bug-uri - exact de-asta straturile sunt cinci, nu unul.

---

**Afirmația:** Cercetătorii Mozilla 0Din au demonstrat (iunie 2026) un atac de prompt injection indirect în care un repository cu aspect inofensiv determină Claude Code să ruleze un script care își trage un payload codat base64 dintr-un DNS TXT record și deschide un reverse shell - atacul e împărțit între repository, DNS și mașina developerului, așa că nicio semnătură de reverse shell nu apare în clar pe disc sau pe fir.
**Sursa:** SecurityWeek, 29 iunie 2026: [securityweek.com/new-attack-abuses-claude-code-and-harmless-looking-repositories-to-hijack-developer-machines/](https://www.securityweek.com/new-attack-abuses-claude-code-and-harmless-looking-repositories-to-hijack-developer-machines/).
**Unde e folosită:** Capitolul 3 (Guvernanța în straturi, injecția prin munca în sine).
**Atenție:** Proof of concept; niciun patch de vendor raportat la momentul scrierii. Mitigarea e postura stratificată - un allowlist de rețea mărginește calea prin DNS indiferent de ce a fost convins agentul să ruleze.

---

### Documentația tool-urilor

**Afirmația:** Codex CLI a livrat Agent Skills ca componentă principală de primă clasă în decembrie 2025, cu fișiere SKILL.md cu frontmatter YAML și semantici de progressive disclosure comparabile cu Skills din Claude Code.
**Sursa:** OpenAI Codex CLI docs, [developers.openai.com/codex/skills](https://developers.openai.com/codex/skills).
**Unde e folosită:** Capitolul 1 (Componentele principale), ca partea Codex a convergenței pe componenta principală de skill.
**Atenție:** Documentație de vendor; datele de GA sunt corecte la mijlocul lui 2026, dar pot fi revizuite retroactiv.

---

**Afirmația:** Subagenții din Codex CLI au ajuns la GA pe 14 martie 2026 și rulează până la șase în paralel by default (`agents.max_threads`, implicit 6; adâncimea de nesting e implicit un singur nivel).
**Sursa:** OpenAI Codex CLI docs, [developers.openai.com/codex/subagents](https://developers.openai.com/codex/subagents).
**Unde e folosită:** Capitolul 1 (Componentele principale) și Capitolul 5 (Bucla în șase faze, faza de Execute).
**Atenție:** Documentație de vendor; default-ul de șase thread-uri e în practică un plafon la mijlocul lui 2026 (openai/codex#11965 urmărește configurabilitatea lui) și se poate schimba în versiunile următoare.

---

**Afirmația:** Codex CLI documentează [AGENTS.md](https://agents.md/) drept convenția pentru instrucțiuni de agent la nivel de proiect, încărcată la începutul sesiunii și echivalentă ca rol cu fișierele de instrucțiuni de echipă ale celorlalți vendori.
**Sursa:** OpenAI Codex CLI documentation, [developers.openai.com/codex/agents-md](https://developers.openai.com/codex/agents-md).
**Unde e folosită:** Capitolul 1 (Componentele principale, secțiunea despre skills) și Capitolul 6 (AGENTS.md ca infrastructură de echipă).
**Atenție:** Numele fișierului și semantica de încărcare sunt stabile; regulile specifice de frontmatter și de descoperire pot evolua de la o versiune la alta.

---

**Afirmația:** AGENTS.md, în calitate de convenție neutră față de vendor pentru fișierul de instrucțiuni al echipei, are suport nativ în Codex CLI, Cursor, GitHub Copilot, Gemini CLI, Aider, Zed și Windsurf. Formatul e markdown; semantica de încărcare e echivalentă între tool-uri.
**Sursa:** Cross-vendor documentation: Codex CLI ([developers.openai.com/codex/agents-md](https://developers.openai.com/codex/agents-md)), Cursor ([cursor.sh/docs](https://cursor.sh/docs)), GitHub Copilot ([docs.github.com/copilot](https://docs.github.com/copilot)), Gemini CLI ([cloud.google.com/gemini/docs/codeassist](https://cloud.google.com/gemini/docs/codeassist)), Aider ([aider.chat/docs](https://aider.chat/docs)), Zed ([zed.dev/docs/ai](https://zed.dev/docs/ai)), Windsurf ([codeium.com/windsurf/docs](https://codeium.com/windsurf/docs)).
**Unde e folosită:** Capitolul 1 (Componentele principale, secțiunea despre skills) și Capitolul 6 (Nume și convenții).
**Atenție:** Lista tool-urilor care îl suportă crește în timp; afirmația e că AGENTS.md e convenția de facto neutră față de vendor, nu că lista ar fi exhaustivă. Lista se și schimbă: Google a început la mijlocul lui 2026 tranziția utilizatorilor de Gemini CLI către Antigravity CLI (tier-urile gratuite și de consumator au încetat să fie servite în iunie) - iar succesorul citește același AGENTS.md, adică exact convenția care supraviețuiește tool-ului, adică exact poanta acestei intrări.

---

**Afirmația:** opencode e un coding agent open-source întreținut de o echipă independentă, scris în TypeScript și licențiat sub MIT. Codul sursă e organizat în jurul acelorași componente principale pe care manualul ăsta le identifică în Codex CLI și Claude Code.
**Sursa:** opencode repository ([github.com/anomalyco/opencode](https://github.com/anomalyco/opencode); fost sst/opencode - compania care îl întreține s-a redenumit Anomaly în ianuarie 2026); LICENSE and README.
**Unde e folosită:** Capitolul 1 (Componentele principale, trecerea în revistă a codului sursă) și Capitolul 2 (Anatomia invariantă, demo-ul cu doi agenți).
**Atenție:** Numele proiectului și componența echipei de mentenanță pot evolua; afirmația despre convergența arhitecturală supraviețuiește redenumirilor.

---

**Afirmația:** Playwright controlează un browser real prin interacțiuni scriptate; accessibility tree-ul e structura semantică pe care browserele o expun pentru tehnologiile asistive și rămâne stabil la restilizări vizuale sau la schimbarea bibliotecii de componente. Testele scrise pe accessibility tree verifică comportamentul, nu prezentarea.
**Sursa:** Playwright documentation ([playwright.dev/docs/accessibility-testing](https://playwright.dev/docs/accessibility-testing)); W3C ARIA Accessibility Object Model spec.
**Unde e folosită:** Capitolul 5 (faza de Verify), ca pattern recomandat de verificare a frontend-ului; checklist-ul din Anexa B.3.
**Atenție:** O parte din comportamentul UI-ului (animații, drag-and-drop, suprafețe canvas complexe) nu e surprinsă complet de accessibility tree și are nevoie de verificare suplimentară.

---

**Afirmația:** Claude Code suportă sandboxing la nivel de OS pe Linux (bubblewrap cu Landlock și seccomp), macOS (Seatbelt) și Windows (restricted tokens cu job objects), activabil opt-in prin configurare. Codex CLI impune sandbox-ul implicit pe Linux și macOS; trebuie să faci opt-out, nu opt-in.
**Sursa:** Claude Code docs ([code.claude.com/docs/en/sandboxing](https://code.claude.com/docs/en/sandboxing)) and Codex CLI agent approvals and security docs ([developers.openai.com/codex/agent-approvals-security](https://developers.openai.com/codex/agent-approvals-security)).
**Unde e folosită:** Capitolul 2 (Anatomia invariantă, constatarea despre divergența de sandbox) și Capitolul 3 (Guvernanța în straturi, stratul doi).
**Atenție:** "Activat implicit" versus "opt-in" e un detaliu de implementare care ține de versiune. Verifică default-ul curent pentru versiunea pe care o ai instalată înainte să te bazezi pe el.

---

**Afirmația:** Cursor 2.0 (octombrie 2025) a introdus agenți paraleli independenți și sandboxing activat implicit pe macOS; sistemul de subagenți propriu-zis - un agent părinte care deleagă către subagenți copii - a apărut în Cursor 2.4 (ianuarie 2026) și a devenit asincron în 2.5. Cline a livrat subagenți nativ. Claude Code a adăugat Agent Teams ca strat de coordonare de nivel mai înalt peste tool-ul Task.
**Sursa:** Changelog-urile Cursor (2.0, 2.4, 2.5); anunțurile și documentația vendorilor pentru Cline și Claude Code; colatate de-a lungul lui 2026.
**Unde e folosită:** Capitolul 1 (Componentele principale), ca dovadă pentru convergența pe componenta principală de subagent în aproximativ un an.
**Atenție:** Suprafețele de produs ale vendorilor evoluează; afirmația despre convergență rămâne în picioare chiar și când nume specifice de produs se rebranduiesc.

---

**Afirmația:** Claude Fable 5, lansat pe 9 iunie 2026 ca primul model din clasa Mythos, a avut accesul suspendat la nivel mondial între 12 și 30 iunie 2026, înainte de a fi redistribuit.
**Sursa:** Anthropic, „Claude Fable 5 and Mythos 5” (9 iunie 2026): [anthropic.com/news/claude-fable-5-mythos-5](https://www.anthropic.com/news/claude-fable-5-mythos-5); „Redeploying Fable 5” (30 iunie 2026): [anthropic.com/news/redeploying-fable-5](https://www.anthropic.com/news/redeploying-fable-5).
**Unde e folosită:** Capitolul 10 (Vendorul va avea o săptămână proastă).
**Atenție:** Motivul suspendării e relatarea vendorului; lecția operațională - planifică pentru indisponibilitatea vendorului - nu depinde de cauză.

---

### Marketplace-uri și ecosisteme de plugin-uri

**Afirmația:** Marketplace-ul `claude-plugins-official` al Anthropic vine inclus în Claude Code din mai 2026 și împachetează skill-uri, hook-uri, tool-uri și comenzi în spatele unei singure comenzi de instalare. Marketplace-ul avertizează utilizatorii să verifice dacă au încredere în plugin-uri înainte să le instaleze.
**Sursa:** Claude Code docs ([code.claude.com/docs/en/discover-plugins](https://code.claude.com/docs/en/discover-plugins)); the marketplace itself.
**Unde e folosită:** Capitolul 1 (Componentele principale, secțiunea despre plugin-uri).
**Atenție:** Numărul de plugin-uri și politicile marketplace-ului se vor schimba în timp; ce trebuie să iei cu tine e disciplina de supply chain descrisă în Capitolul 1, nu vreun număr anume.

---

### Surse pentru componenta principală Memory

**Afirmația:** AGENTS.md e citit la începutul sesiunii de Codex CLI, Cursor, GitHub Copilot, Gemini CLI, Aider și de ecosistemul mai larg de coding agents open-source (peste 20 de vendori listați pe agents.md la 2026-05). Claude Code citește CLAUDE.md, care poate importa AGENTS.md pentru a împărți același conținut cu ceilalți agenți. Convergența plasează AGENTS.md în stratul de memorie definită manual al componentei principale Memory numit în Capitolul 1.
**Sursa:** [agents.md](https://agents.md/) (the open standard's site), plus vendor documentation for each agent listed.
**Unde e folosită:** Capitolul 1 (Componentele principale, secțiunea Memory) și Capitolul 6 (AGENTS.md ca infrastructură de echipă).
**Atenție:** Numele exact al fișierului și semantica de încărcare diferă de la un vendor la altul - Claude Code citește CLAUDE.md (importabil din AGENTS.md prin `@AGENTS.md` sau symlink); Cursor citește AGENTS.md plus `.cursorrules`. Convergența e pe rolul structural - scris de utilizator, încărcat mereu, partajabil în echipă - nu pe un format de fișier identic la nivel de byte.

---

**Afirmația:** Claude Code întreține un strat de auto-memory în care Claude își scrie singur notițe de la o sesiune la alta - comenzi de build pe care le-a deslușit, concluzii de debugging pe care le-a confirmat, preferințe de stil de cod pe care le-a dedus - distinct de CLAUDE.md-ul scris de utilizator. Necesită Claude Code v2.1.59+; activat implicit; stocare per repo.
**Sursa:** [code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory).
**Unde e folosită:** Capitolul 1 (Componentele principale, secțiunea Memory).
**Atenție:** Intrarea documentează implementarea din Claude Code, dar jumătatea asta e o convergență, nu o exclusivitate: GitHub Copilot Memory a ajuns în public preview pe 15 ianuarie 2026 - înainte să apară Auto Memory - și era activat implicit pe tier-urile Pro până pe 4 martie; Codex CLI a adăugat memorie automată de fundal în aprilie 2026.

---

**Afirmația:** Anthropic a anunțat public Dreaming ca parte din Claude Managed Agents la Code with Claude SF pe 2026-05-06 - un proces de fundal programat, care trece în revistă sesiunile recente și memory store-ul, identifică greșelile recurente și workflow-urile convergente și scrie notițe consolidate înapoi în memoria pe termen lung. Se livrează ca feature la nivel de platformă, condiționat de un beta header; o suprafață în CLI-ul Claude Code (`/dream`) era doar sugerată în produs și nu apăruse ca o comandă funcțională până în iulie 2026.
**Sursa:** Code with Claude SF announcement, 2026-05-06; [code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory).
**Unde e folosită:** Capitolul 1 (Componentele principale, secțiunea Memory).
**Atenție:** Dreaming e specific Anthropic și la nivel de API la data publicării, nu încă un feature de CLI. Manualul ăsta indexează rolul structural, nu vendorul.

---

### Surse pentru componenta principală Permisiuni / Sandbox

**Afirmația:** Claude Code vine cu un model de permisiuni Allow/Ask/Deny, cu precedență deny-apoi-ask-apoi-allow, și cu un sandbox de OS opt-in - Seatbelt pe macOS, bubblewrap pe Linux - configurabil prin `/sandbox` și prin `.claude/settings.json` la nivel de proiect. Stratul de decizie e activ implicit; sandbox-ul de OS nu.
**Sursa:** [code.claude.com/docs/en/permissions](https://code.claude.com/docs/en/permissions); [code.claude.com/docs/en/sandboxing](https://code.claude.com/docs/en/sandboxing).
**Unde e folosită:** Capitolul 1 (secțiunea Permisiuni / Sandbox), Capitolul 3 (stratul unu și stratul doi).
**Atenție:** Postură opt-in pe jumătatea de enforcement la nivel de OS. O instalare standard de Claude Code are stratul de decizie, dar niciun sandbox la nivel de kernel; majoritatea instalărilor sar peste pasul de configurare a sandbox-ului.

---

**Afirmația:** Codex CLI impune implicit sandbox la nivel de OS pe Linux (Landlock + seccomp prin bwrap) și pe macOS (Seatbelt); pe Windows folosește restricted tokens plus izolare bazată pe ACL-uri. Stratul de decizie e livrat în paralel, ca gate de aprobare per tool.
**Sursa:** [developers.openai.com/codex/concepts/sandboxing](https://developers.openai.com/codex/concepts/sandboxing); [developers.openai.com/codex/agent-approvals-security](https://developers.openai.com/codex/agent-approvals-security).
**Unde e folosită:** Capitolul 1 (secțiunea Permisiuni / Sandbox), Capitolul 2 (constatarea din comparația arhitecturală cap la cap), Capitolul 3 (stratul doi).
**Atenție:** Postură opt-out - poți configura Codex să ruleze fără sandbox, dar default-ul inversează convenția, de la "oprit dacă nu-l configurezi" la "pornit dacă nu-l dezactivezi". Implementarea pe Windows e cea mai puțin uniformă dintre agenții majori.

---

**Afirmația:** opencode vine cu un model de prompt de permisiuni în interiorul agentului și cu validare de căi și permisiuni, dar nu oferă izolare prin sandbox la nivel de OS; pentru izolare, operatorul trebuie să împacheteze opencode în Docker, într-un microVM sau într-un alt harness de sandbox (KB-ul Vercel documentează explicit acest pattern de deployment). La testul de convergență din Capitolul 1, opencode trece jumătatea cu stratul de decizie și pică jumătatea cu enforcement-ul la nivel de OS.
**Sursa:** [vercel.com/kb/guide/running-opencode-securely-with-the-vercel-sandbox](https://vercel.com/kb/guide/running-opencode-securely-with-the-vercel-sandbox).
**Unde e folosită:** Capitolul 1 (secțiunea Permisiuni / Sandbox), Capitolul 2 (constatarea din comparația arhitecturală cap la cap).
**Atenție:** Eticheta de "îngrădire soft" îi aparține manualului, nu documentației opencode. opencode nu pretinde că livrează un sandbox - absența e asumată onest, nu ascunsă.

---

### Surse despre bucla exterioară și autonomie

**Afirmația:** Până în primăvara lui 2026, bucla exterioară devine o suprafață de primă clasă în Claude Code: /loop rerulează un prompt la un interval dat (martie 2026) sau își alege singur ritmul când intervalul lipsește (aprilie 2026), Routines declanșează cloud agents pe bază de template dintr-un program, dintr-un eveniment GitHub sau dintr-un apel de API (aprilie 2026), /goal ține agentul la lucru de la un tur la altul până când o condiție de finalizare e îndeplinită (mai 2026), iar /autofix-pr urmărește CI-ul și comentariile de review și împinge fix-uri până când pull request-ul e verde (aprilie 2026).
**Sursa:** Claude Code release notes, "What's new": [code.claude.com/docs/en/whats-new](https://code.claude.com/docs/en/whats-new), weekly digests for April-May 2026.
**Unde e folosită:** Capitolul 9 (pattern-ul opt).
**Atenție:** Numele de feature și săptămânile de release reflectă stadiul vendorului la iulie 2026; așteaptă-te la schimbări, conform notei despre afirmațiile datate.

---

**Afirmația:** Tehnica Ralph Wiggum - un while-loop de bash care tot trimite un fișier de prompt într-un coding agent, cu context proaspăt la fiecare iterație și starea ținută în repository - pornește de la Geoff Huntley la mijlocul lui 2025 ("In its purest form, Ralph is a Bash loop": `while :; do cat PROMPT.md | claude-code ; done`), devine virală la sfârșitul lui 2025 și e adoptată în repository-ul oficial Claude Code ca plugin-ul ralph-wiggum în noiembrie 2025 (commit-ul de migrare e datat 16 noiembrie). Huntley estimează costul rulării buclei brute la aproximativ 10 dolari pe oră, spune că multe startup-uri din Y Combinator rulează Ralph și numește modul de eșec central "overbaking".
**Sursa:** Geoff Huntley, [ghuntley.com/ralph](https://ghuntley.com/ralph/) (July 2025); HumanLayer, "A Brief History of Ralph," January 6, 2026: [humanlayer.dev/blog/brief-history-of-ralph](https://www.humanlayer.dev/blog/brief-history-of-ralph); The Register, January 27, 2026: [theregister.com/2026/01/27/ralph_wiggum_claude_loops/](https://www.theregister.com/2026/01/27/ralph_wiggum_claude_loops/).
**Unde e folosită:** Capitolul 9 (pattern-ul opt), paragrafele despre filiație și overbaking.
**Atenție:** Cifra de 10 dolari pe oră și afirmația despre adopția în Y Combinator îi aparțin lui Huntley, preluate de The Register - raportări de practician, nu cifre auditate.

---

**Afirmația:** Execuția de agenți în fundal și pe bază de program a fost livrată de mai mulți vendori pe parcursul sfârșitului lui 2025: GitHub Copilot coding agent disponibil general pe 25 septembrie 2025 (mediu izolat de GitHub Actions; rezultatul livrat ca draft de pull request; review cerut unui om la finalizare); Cursor Cloud Agents pe 30 octombrie 2025 (mulți agenți detașați, cu laptopul închis); Google Jules Scheduled Tasks pe 10 decembrie 2025 (cadențe recurente pentru muncă de mentenanță).
**Sursa:** GitHub changelog: [github.blog/changelog/2025-09-25-copilot-coding-agent-is-now-generally-available](https://github.blog/changelog/2025-09-25-copilot-coding-agent-is-now-generally-available/); Cursor blog: [cursor.com/blog/cloud-agents](https://cursor.com/blog/cloud-agents); Google blog: [blog.google/technology/developers/jules-proactive-updates](https://blog.google/technology/developers/jules-proactive-updates/).
**Unde e folosită:** Capitolul 9 (pattern-ul opt), paragraful despre convergență.
**Atenție:** Datele de livrare sunt cele din anunțurile vendorilor; suprafețele au continuat să evolueze de atunci.

---

**Afirmația:** Echipa "software factory" de la StrongDM rulează livrare cu agenți complet non-interactivă - oamenii nici nu scriu, nici nu fac review la cod - cu scenarii end-to-end de user story stocate în afara codebase-ului, ca un holdout set pe care agenții nu îl pot vedea sau slăbi, și tratează aproximativ 1.000 de dolari pe zi per inginer cheltuiți pe tokeni drept prag minim de sănătate al fabricii; Simon Willison rezumă economia la circa 20.000 de dolari pe lună per inginer și semnalează asta ca principala limitare a pattern-ului.
**Sursa:** Simon Willison, "How StrongDM's AI team build serious software without even looking at the code," February 7, 2026: [simonwillison.net/2026/Feb/7/software-factory/](https://simonwillison.net/2026/Feb/7/software-factory/).
**Unde e folosită:** Capitolul 9 (pattern-ul opt), polul industrial.
**Atenție:** Auto-descrierea unei singure companii; sumele în dolari sunt ale echipei și încadrarea lui Willison, nu un audit.

---

**Afirmația:** Era buclelor din 2023 - AutoGPT, BabyAGI - rula un model în buclă pe baza propriei lui evaluări a progresului, fără un verificator extern la fiecare iterație, și s-a prăbușit ca abordare de livrare de software în câteva luni. Revirimentul din 2025 diferă structural: fiecare iterație se încheie cu o confruntare cu compilatorul, cu testele și cu diff-ul.
**Sursa:** The AutoGPT and BabyAGI repositories document the 2023 design: [github.com/Significant-Gravitas/AutoGPT](https://github.com/Significant-Gravitas/AutoGPT), [github.com/yoheinakajima/babyagi](https://github.com/yoheinakajima/babyagi). The structural contrast is this manual's analysis, drawn from the Ralph-era sources above.
**Unde e folosită:** Capitolul 9 (pattern-ul opt), paragraful despre filiație.
**Atenție:** Verdictul de "prăbușire" e o interpretare; ambele proiecte au continuat în alte roluri.

---

### Note despre actualitate

Majoritatea surselor din anexa asta sunt datate. Documentația tool-urilor se actualizează frecvent; înregistrările de vulnerabilități se amendează pe măsură ce apar patch-uri și variante noi. Framework-urile din corpul manualului sunt gândite să supraviețuiască oricărui URL anume. Dacă un URL moare, afirmația din spatele lui ar trebui să rămână căutabilă după numele incidentului, al studiului sau al produsului.

---
