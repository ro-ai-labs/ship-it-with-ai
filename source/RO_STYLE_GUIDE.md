# Ghid de stil - versiunea în limba română a manualului "Ship It With AI"

## Misiunea

NU facem o traducere literală. Facem o ADAPTARE în limba română, în registrul folosit
în mediul corporate tech românesc: română naturală, fluentă, de carte tehnică / de
business bine scrisă, în care terminologia tehnică și de business rămâne în engleză,
exact cum vorbesc inginerii români între ei pe Slack/Teams și în ședințe.

Testul suprem: un senior engineer român citește paragraful și NU simte că e tradus
din engleză. Sună ca și cum autorul l-ar fi scris direct în română.

## Registru și voce

- Persoana a II-a singular ("tu") pentru cititor, ca în cărțile tehnice românești moderne. Nu "dumneavoastră".
- Persoana I pentru vocea autorului (manualul e scris la persoana I, păstrăm asta).
- Ton: direct, ferm, colocvial-profesionist. Fraze care respiră. Fără limbă de lemn.
- Diacritice corecte peste tot: ș, ț (cu virgulă), ă, â, î. Obligatoriu.

## Regula de aur anti-calc

Dacă o formulare sună bine în engleză dar prost în română, RESCRIE ideea de la zero
în română. Tradu sensul, nu structura frazei. Exemple de capcane INTERZISE:

- "face sens" → corect: "are sens"
- "a adresa o problemă" → corect: "a rezolva / a aborda o problemă"
- "la sfârșitul zilei" (calc după "at the end of the day") → corect: "până la urmă", "în final"
- "cel mai bun din clasă" (best-in-class) → reformulează
- "a livra valoare" e acceptat în corporate RO, dar nu abuza
- "împuternicește echipa" (empower) → "dă echipei autonomie / pârghii"
- "robust" e ok, "a îmbrățișa schimbarea" (embrace) → "a adopta / a accepta"
- structuri pasive englezești lungi → reformulează activ, românește
- "Iată chestia:" (here's the thing) → reformulează natural
- NU traduce idiomuri mot-à-mot. Găsește echivalentul românesc sau reformulează.
- Atenție la topica românească: nu copia ordinea cuvintelor din engleză.
- "framework" / "the frame" în sensul de cadru de evaluare/de referință/metodologie
  (ex. "a frame for evaluating tools", "the frame survives", "the architecture-method-reality
  frame") → "framework" (NU "cadru" - sună prost; articulat: framework-ul / framework-uri /
  framework-ului).
- DAR "the frame of this manual" (titlul din Cuvânt înainte, sensul de structură/organizare
  a manualului - "trei părți...") → "Structura manualului" (NU "Framework", NU "Cadrul";
  e despre cum e împărțit manualul, nu despre metodologie).
- Excepție generală: "cadru" în sensul ramei unei diagrame ("încap în cadru") rămâne;
  "încadrare" e alt cuvânt, se păstrează.
- "primitive" (conceptul de arhitectură - building block) → "componentă principală"
  (feminin: o componentă principală / două componente principale / componentele principale).
  NU "primitiv" și NU "primitivă" - ambele sună prost. Atenție la acord (feminin) la articole,
  demonstrative și adjective. NU atinge ancorele/slug-urile (ex. {#what-is-a-primitive}) și
  nici prompturile păstrate în engleză ("name the primitives...").
- "queue" → "queue" (NU "coadă"; masculin în romgleză: un queue / queue-ul / queue-uri /
  queue-ului). EXCEPȚIE: idiomul "cap-coadă" (= cover-to-cover / end-to-end) NU se atinge.
- "gate" → "gate" (NU "poartă"; masculin: un gate / gate-ul / gate-uri). EXCEPȚIE: verbul
  "a purta" ("poartă semnătura", "poartă o conversație", "Poartă conversația...") NU se atinge.
- "embedded targets" → "target-uri embedded" (NU "ținte embedded" - "ținte" sună prost
  pentru termenul tehnic; păstrează "target" în engleză, articulat: target-uri).

## Ce rămâne în ENGLEZĂ (neapărat, ca în vorbirea corporate RO)

Termeni tehnici și de produs - se păstrează în engleză, articulați românește cu
cratimă unde e natural (codebase-ul, hook-urile, pipeline-ul, PR-ul):

agent (e și românesc, perfect), coding agent, harness, context window (la prima
apariție poți glosa: "context window - fereastra de context"), tool / tool call,
sandbox, skill / skills, plugin, MCP, memory ("memorie" în proza generală e ok, dar
primitive-ul se numește Memory), subagent / subagenți, prompt, prompt injection,
token, model, benchmark, codebase, repo / repository, branch, commit, push, merge,
pull request / PR, code review (sau "review de cod"), review, diff, build, deploy /
deployment, pipeline, CI / CI/CD, lint / linting, refactor / refactoring, bug,
debugging, feature, backlog, sprint, task, deadline, feedback, stakeholder, rollout,
onboarding, business, enterprise, greenfield, brownfield, legacy, hook / hooks,
worktree, workflow, framework, marketplace, vendor, post-mortem, supply chain,
champion (rolul), lead (rolul), manager, kill signal / kill signals (termen-marcă al
cărții, rămâne în engleză: "cele opt kill signals"), inner loop / outer loop (vezi
glosar), staging, production / producție (ambele ok; "producție" e natural în RO),
unit test / integration test ("teste unitare / de integrare" sunt și ele naturale -
alege ce curge mai bine în frază), happy-path, edge case, blast radius (glosează la
prima apariție: "blast radius - raza de impact"), bus factor, two-person rule.

Nume proprii și de produse rămân neatinse: Claude Code, Codex CLI, opencode, Cursor,
Gemini CLI, Copilot, Aider, Zed, Windsurf, Superpowers, hookify, Understand Anything,
Ralph Wiggum, AGENTS.md, CLAUDE.md, SKILL.md, Playwright, Terraform, Railway, Jira,
Confluence, Slack, Spring Boot, React, Flyway, METR, PocketOS, DataTalks.Club,
StrongDM, /loop, /goal, /dream, /autofix-pr, Routines, Auto Memory, Auto Dream,
Agent Teams, Cloud Agents, Scheduled Tasks, Spec Kit, BMAD, Seatbelt, bubblewrap,
Landlock, seccomp, Bean Validation, JPQL, DTO, PII, GDPR, SOX, PCI, RCE, CVE, SIEM,
Zero Data Retention, SSO, BAA, CODEOWNERS, ROI, TCO, AES-CBC, IV, SaaS, LLM, IDE,
API, REST, COBOL, DSL.

Reguli de articulare Romgleză (consecvent!):
- codebase-ul, codebase-uri / harness-ul / hook-ul, hook-uri / plugin-ul, plugin-uri
- PR-ul, PR-uri / tool-ul, tool-urile / token-i? NU: "tokeni" e uzual → "tokeni"
- skill-ul, skill-uri / sprint-ul / task-ul, task-uri / worktree-ul, worktree-uri
- "pattern-ul, pattern-uri" (NU "tipare" pentru sensul tehnic)
- "subagent → subagentul, subagenții" (fără cratimă, s-a românizat natural)

## Ce se TRADUCE natural (nu lăsa în engleză)

- proza narativă, argumentația, povestirile
- "team" → echipa; "tooling" → tooling-ul e ok în corporate RO, dar și "unelte/sculărie" NU - folosește "tooling" sau "instrumentele"
- "shipping software" → "a livra software" (verbul "a livra" e standard corporate);
  titlul "Ship It With AI" și sloganul rămân în engleză
- "governance" → "guvernanță" (uzual în corporate RO)
- "permissions" → "permisiuni" (natural; primitive-ul se numește "Permisiuni / Sandbox")
- "traffic light" → "semaforul" (verde / galben / roșu)
- "mistake journal" → "jurnalul de greșeli"
- "forbidden patterns" → "pattern-uri interzise"
- "research note" → "nota de research" (corporate RO zice "research")
- "characterization tests" → "teste de caracterizare"
- "telemetry" → "telemetrie"
- "secrets" → "secrete" (credențiale: "credențiale")
- "least privilege" → "principiul privilegiului minim" la prima mențiune, apoi "privilegiu minim"
- "defense in depth" → "apărare în adâncime" la prima mențiune cu glosă "(defense in depth)", apoi alege una și fii consecvent

## Glosar canonic (FOLOSEȘTE EXACT ACESTE FORME - consecvență totală)

Structura cărții:
- Foreword → "Cuvânt înainte - De ce există manualul ăsta"
- How to read this manual → "Cum se citește manualul"
- A note on dated claims → "O notă despre afirmațiile datate"
- Scope and limits → "Aria de acoperire și limitele"
- Cases used in this manual → "Cazurile folosite în manual"
- Prologue → "Prolog"; Nine seconds → "Nouă secunde"
- Part I - Architecture → "Partea I - Arhitectura"
- Part II - Method → "Partea a II-a - Metoda"
- Part III - Reality → "Partea a III-a - Realitatea"
- Closing → "Încheiere - Un mod de a gândi care supraviețuiește tool-urilor"
- Acknowledgments → "Mulțumiri"
- About the author → "Despre autor"
- Changelog → "Changelog" (rămâne)
- Appendix A - Cost Economics → "Anexa A - Economia costurilor"
- Appendix B - Templates → "Anexa B - Template-uri"
- Appendix C - Sources and Further Reading → "Anexa C - Surse și lecturi suplimentare"

Titluri de capitole (canonice):
1. "Componentele principale"
2. "Anatomia invariantă"
3. "Guvernanța în straturi"
4. "De la cod generat la software livrat"
5. "Bucla în șase faze"
6. "AGENTS.md ca infrastructură de echipă"
7. "Review-ul de arhitectură: documentare și diagnostic"
8. "Pregătirea: kill signals și semaforul"
9. "Pattern-uri pentru codebase-uri brownfield"
10. "Adopția: 90 de zile, trei roluri"

Termeni recurenți:
- "the primitives" → "componentele principale" (vezi regula din secțiunea anti-calc: o componentă principală / componentele principale; ex. "componenta principală Memory"). NU "primitivele".
- "the harness" → "harness-ul"
- "the agent loop" → "bucla agentului"
- "the six-phase loop" → "bucla în șase faze"
- fazele: Research, Plan, Execute, Review, Verify, Ship - RĂMÂN ÎN ENGLEZĂ ca nume
  de faze (ex: "faza de Research", "faza de Plan"), pentru că așa le folosește
  tooling-ul; în proză poți spune natural "cercetezi / planifici / execuți"
- "inner loop / outer loop" → "bucla interioară / bucla exterioară", cu "(inner
  loop / outer loop)" glosate la prima apariție în fiecare capitol unde contează
- "kill signals" → rămâne "kill signals" ("cele opt kill signals", "un kill signal")
- "the traffic light" → "semaforul"; culorile: VERDE / GALBEN / ROȘU
- "readiness" → "pregătirea" / "gradul de pregătire"
- "the anatomy invariant" → "anatomia invariantă" / "invarianța anatomiei" în proză
- "formulation discipline" → "disciplina formulării"
- "context contamination" → "contaminarea contextului"
- "the champion / the lead / the manager" → "championul / lead-ul / managerul"
- "grassroots arc" → "arcul grassroots" (glosează la prima apariție: "de jos în sus")
- "the principled skeptic" → "scepticul de principiu"
- "the uncalibrated delegator" → "delegatorul necalibrat"
- "overbaking" → rămâne "overbaking" (termenul lui Huntley), glosat la prima apariție
- "Ship this week." (rubrică recurentă) → "**De pus în practică săptămâna asta.**"
- "Try it yourself." (rubrică recurentă) → "**Încearcă și tu.**"
- "Artifact:" (rubrică recurentă) → "**Artefact:**"
- "Case note:" → "**Fișă de caz:**"
- "Source note." → "*Notă despre surse.*"
- "Ship It With AI" (titlul) → rămâne; subtitlul "A Field Manual for Agentic
  Software Delivery" → "Un manual practic pentru livrarea de software cu agenți AI"
- motto-ul de pe copertă: "The agents write the code. / You understand the problem. /
  That is the skill no one is automating." → "Agenții scriu codul. / Tu înțelegi
  problema. / Asta e competența pe care n-o automatizează nimeni."
- "agentic software delivery" → "livrarea de software cu agenți" (NU "livrare agentică" - sună rău; ocazional "delivery agentic" e tolerat în citate, dar evită)
- "agentic AI" → "AI agentic" (acesta DA, e încetățenit)
- "agentic coding" → "coding agentic" e urât; folosește "programarea cu agenți" / "lucrul cu agenți de cod"
- "production-ready / production-grade" → "gata de producție" / "de nivel de producție" - sau reformulează
- "field manual" → "manual practic" (NU "manual de teren")

## Elemente care NU se modifică

1. TOATE ancorele de heading rămân identice: `{#what-is-a-primitive}` etc. NU le traduce.
2. TOATE URL-urile și linkurile rămân identice.
3. Blocurile de cod (```) cu diagrame ASCII: păstrează structura și etichetele
   tehnice; etichetele care sunt nume de primitive / faze rămân în engleză.
   Liniile de proză explicativă DIN diagramă (ex: "the agent loop binds them
   together") se pot traduce dacă încap în cadru; dacă nu, lasă-le în engleză.
4. În Anexa B: template-urile B.1 (promptul de architecture review) și B.2
   (scheletul AGENTS.md) RĂMÂN ÎN ENGLEZĂ integral (sunt artefacte pe care le
   consumă agentul; inginerii români promptează în engleză). Adaugă o singură frază
   introductivă în română care spune exact asta. B.3-B.6 (checklist-uri pentru
   oameni) se adaptează în română cu termenii tehnici în engleză.
5. Tabelele: structura rămâne; conținutul se adaptează după aceleași reguli.
6. Citatele directe documentate (confesiunea agentului PocketOS, citatul lui
   Huntley "In its purest form...", comenzile bash) rămân în engleză; poți adăuga
   parafrază scurtă în română dacă fluxul o cere.
7. Numerele, datele, procentele rămân identice. "90 de zile", "19%", "43 de puncte".
8. Separatoarele `---` și nivelurile de heading rămân exact ca în original.
9. În Anexa C: "Claim/Source/Where used/Caveat" devin "**Afirmația** / **Sursa** /
   **Unde e folosită** / **Atenție**"; afirmațiile și caveat-urile se traduc,
   sursele (titluri de articole, nume, URL-uri) rămân în engleză.

## Verificare finală per fragment

Înainte să predai fragmentul, recitește-l și întreabă-te la fiecare paragraf:
1. Ar scrie un autor român fraza asta exact așa? Dacă nu - rescrie.
2. Am păstrat TOATE informațiile și nuanțele din original? (adaptare ≠ rezumare;
   nu ai voie să tai conținut)
3. Termenii din glosar sunt EXACT în forma canonică?
4. Ancorele, linkurile, structura markdown - intacte?
