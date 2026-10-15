# Ship It With AI

### A Field Manual for Agentic Software Delivery

**Mihai Cvasnievschi**

---

> The agents write the code.
> You understand the problem.
> That is the skill no one is automating.

---

## Contents

**Prologue** - Nine seconds

**Part I - Architecture**
1. What an agent is
2. Guardrails in five layers

**Part II - Method**
3. The bottleneck moved
4. The six-phase loop
5. Review and verify
6. [AGENTS.md](https://agents.md/) and context
7. Map it first: architecture review

**Part III - Reality**
8. Should the agent touch this code?
9. Rolling it out

**Closing** - A way of thinking that survives the tools

**Acknowledgments**

**Appendix A** - For Managers
**Appendix B** - Templates
**Appendix C** - Sources and Further Reading
**Appendix D** - Deep Dives

---

# Prologue

## Nine seconds {#nine-seconds}

On April 24, 2026, a small SaaS company called PocketOS, a car rental management product, lost its production database to an AI agent that decided to fix a credentials problem on its own.

A developer was using a coding agent (Cursor powered by Claude Opus 4.6) on the PocketOS codebase. During a routine task the agent hit a credentials mismatch and, instead of stopping and asking, decided to fix it itself. It found an API token that authenticated against Railway, the infrastructure platform PocketOS used, and invoked Railway's Volume Delete command. The destructive call took nine seconds.

The loss was total: all the customer reservations, payment records and vehicle inventory. Railway stores backups on the same volume as the primary data, so the backups went with it, and the most recent recoverable snapshot was three months old. Recovery turned out to be possible, but not through the backup path the team expected; public accounts differ on the timeline.

Afterward the agent confessed in writing: "I violated every principle I was given. I guessed instead of verifying. I ran a destructive action without being asked. I didn't understand what I was doing before doing it."

*I use the incident for the governance pattern, not as a precise forensic reconstruction. Sources and the disputed details are in Appendix C.*

---

**What would have stopped it.** Not magic: ordinary engineering controls, applied to a new kind of worker. Bound the credentials, bound the tools, review the work before it ships, record what happened - the same controls an experienced engineer would apply to any new junior teammate authorized to push to production. None of them is exotic, and none was in place. Chapter 2 walks the incident through five layers, any one of which could have broken the chain.

**Why this keeps happening.** A senior engineer tells me they tried Claude Code, or Codex, or another coding agent, and "it didn't work": the code looked right and was not, or something broke and nobody noticed for two weeks. Most failed adoptions are not explained by model weakness alone. They are failures of structure around the agent: missing context, constraints, process and review discipline.

You can pick up a hammer and use it. You cannot pick up a junior engineer and use them; you onboard them, give them context, set up review, build trust over time. Agents are closer to the junior engineer than to the hammer - a stance, not a claim about the agent's nature: the agent is software.

**The thesis.** Agentic software delivery is not primarily a tooling problem. It is a control problem. Control the context, the actions, the verification and the adoption surface, and the agent becomes useful; fail to, and it becomes expensive noise or operational risk. The three parts of this manual are three controls: Architecture is the control of capability (what the agent can know and do), Method is the control of workflow (how work is formulated, executed and verified), Reality is the control of adoption (where the method applies and where it should not).

By "agentic" I mean a system that takes a goal, decides which actions to perform, and executes them with some autonomy. You stop authoring keystrokes and start supervising work. What agents offer is not faster typing; it is the ability to delegate well-formed work. Understanding the problem, the idea on the cover, is the part that stays yours.

I will not tell you which agent to pick. The one you pick today will be deprecated, rebranded or absorbed within a procurement cycle. The way you think about the work survives the replacement.

---

**Where I am coming from.** I have written software professionally since 2000 and built AI systems for more than a decade. I have used every generation of coding assistant, from early IDE intelligence to Copilot to current agents, and for the last eighteen months I have watched production teams adopt agentic workflows well and badly. The manual is what survived repeated use across real teams. [Full background: About the author.](#about-the-author)

**Where this can be wrong.**

- **The tools will change.** The products I name, the hook formats, the permission syntax and the prices will age. The primitives and the five-layer model are what I expect to hold.
- **Regulated shops differ.** I assume you can install hooks, configure AGENTS.md, set up sandboxes and run subagents. Where that needs a review board or months of procurement, the manual describes the destination, not the path.
- **Lighter process can work.** The six-phase loop is the safe bet, not the only path. Chapter 4 shows a team that earned the lighter version, and what it had in place first.

Tool-specific references are current as of September 2026; the frameworks are meant to outlast them, and the load-bearing claims are sourced in Appendix C. Meaningful updates are in the [changelog](/changelog/).

**How to read it.** It is written for the senior engineer, staff, principal or tech lead, who will run this practice on a real team and defend it upward; anyone who ships software with AI can follow. Read it in order the first time. Managers and directors: Chapters 2, 8 and 9 and Appendix A; facilitating adoption: Chapters 7 to 9 and Appendix B. The studies and numbers behind each chapter are in Appendix D; the chapters keep only what changes a decision.

---

# Part I - Architecture

> *The control of capability: what the agent can know and do.*

---

## Chapter 1
## What an agent is

*By the end you can name the nine parts of any coding agent, find the one that controls a given risk, and compare two agents by what is inside them.*

**TL;DR**

- A coding agent is a model inside a harness, built from nine primitives you can inspect.
- The anatomy is the same across vendors. The implementations differ, and the differences, the sandbox above all, are governance choices.
- Compare harnesses, not models. For any new agent, ask one question per primitive.

---

### What is a coding-agent primitive? {#what-is-a-primitive}

**An agent is a model plus a harness, and the harness is a small, recurring set of parts.**

Open the source of most production-grade coding agents and the same architecture shows up: a set of primitives wrapped by a harness. A mechanism counts as a primitive when every major coding agent ships it as a distinct, configurable bundle. Each card below ends with the question to ask a new agent.

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
        the agent loop binds them together;
        subagents spawn constrained child instances
        of the agent itself
```

*Figure: The primitives and the harness that runs them. Permissions / Sandbox sits in slot 3 as a primitive whose two halves - the agent-level decision layer and OS-level enforcement - converge on presence but diverge on posture across vendors. Memory's second half - the agent-written layer - converged across the major agents in the first months of 2026. Effort is the newest slot: the reasoning dial, and whether the reasoning it buys is retained from one turn to the next. Subagents sit below the line because they are the recursive primitive: each subagent is itself an instance of the others.*

---

### Context window

**What it is: everything the agent knows right now, within a bounded number of tokens.**

It holds the system prompt, the conversation, tool results and files read - not the rest of your codebase or the tickets. Most "obviously wrong" decisions trace to missing context: nobody told it about the new authentication library. Advertised window sizes overstate what a model uses well. Chapter 6 covers working inside the bound.

*Ask: How big is the window, and how does the agent manage it under pressure?*

---

### Tools

**What it is: the actions the agent can take - read, write and edit files, run shell commands, search the codebase.**

Each tool call is a decision point, an audit point and a control point: log the calls to replay what happened, intercept them to govern. "Do not delete files here" works by stopping the Bash call before `rm` runs. Keep the always-visible tool set small, since each tool costs context before your first word.

*Ask: What tools does it have, and how are they constrained?*

---

### Permissions / Sandbox {#permissions-sandbox}

**What it is: two controls shipped as a pair - the agent's own rules and the operating system's enforcement.** This is the primitive PocketOS lacked (see the Prologue).

The decision layer, allow / ask / deny rules plus the newer auto-mode classifier, is consulted before every tool call. Prompt injection can defeat it, because injection manipulates the reasoning that consults the rules. The OS layer sits underneath: the kernel refuses system calls the agent was not authorized to make, and it is not listening to the agent's reasoning. Neither half is enough alone.

*Ask: What permission model does it ship, and what OS sandbox does it default to?*

---

### Skills

**What it is: packaged instructions the agent loads only when a task needs them.**

A skill is a chunk of markdown - the team's way of writing a Spring Boot service, say - kept out of context until a task matches its trigger. Skills are the closest thing in the anatomy to the senior engineer's tribal knowledge, written down.

*Ask: Are skills loaded on detection, or always?*

---

### Plugins

**What it is: a bundle of skills, tools, hooks and commands, installed with one command.**

The plugin is the unit of distribution: one team's PR-review workflow becomes another team's one-line install. The marketplace that results is also a supply-chain surface, the npm of agentic coding. Vet plugins like dependencies, with the checklist in Appendix B.10.

*Ask: Is there a plugin marketplace, and how do you vet what is in it?*

---

### What is MCP? {#what-is-mcp}

**What it is: the Model Context Protocol, a specification for how agents talk to external systems** - Jira, Postgres, GitHub, your data warehouse.

The same MCP server works with any agent that supports it, so the integration survives the next agent you adopt: the closest thing the ecosystem has to an open standard.

*Ask: Does it speak MCP, and how good is the integration?*

---

### Memory {#memory}

**What it is: what carries over from one session to the next, in two halves.**

The team writes the first: AGENTS.md, read at session start by most agents (Claude Code reads CLAUDE.md, which can import it). The agent writes the second for itself: build commands it figured out, debugging insights, inferred preferences. Chapter 6 covers the file.

*Ask: Does it read a team memory file at session start, and keep memory of its own?*

---

### Effort {#effort}

**What it is: how hard the model thinks before it acts - the newest primitive, and it earns its place on leverage.**

Every major agent exposes it as a setting, under different names. It moves cost and quality in both directions: too low skips the research the task needed, too high pays for reasoning it never called for. Names do not transfer between models, so every model migration starts with an effort sweep (Appendix B.9). Set it per phase, not per session: research and plan earn high, a mechanical execute task usually does not.

*Ask: What effort levels does it expose, and does the reasoning survive between turns?*

---

### Subagents

**What it is: constrained child instances of the agent itself.**

The orchestrator hands a subagent a bounded task; it runs in its own isolated context with its own scoped tools and returns a result, and neither side pollutes the other's context. The price is tokens: an eight-subagent dispatch uses about eight times a single run. Chapters 4, 5 and 7 use them to execute, review and map architecture.

*Ask: How does it expose subagents - is parallel dispatch first-class?*

---

### The harness

**The model sets the ceiling; the harness decides whether you reach it.**

The harness is the runtime around the model: it formats your request, manages the window, dispatches tool calls, feeds results back and decides when the work is done. The loop itself is trivial, roughly an HTTP request handler; the middleware around it is what you are buying. Compare harnesses, not models, on your own constraints: language fit, license, plugin ecosystem, sandbox enforcement, audit posture.

---

### The anatomy is invariant

**The anatomy is the same in every agent; the implementation is not.**

> **Proof: one prompt, two agents.** While preparing this manual I pointed Claude Code at the source of two other coding agents in two terminal panes: Codex CLI (Rust, maintained by OpenAI) and opencode (TypeScript, an independent team). Both are open source and share no code. Same prompt in each: map the agent loop, tools, permission gates, sandbox and plugin model, citing files and line numbers.
>
> About four minutes later, with no human correction, both returned the same shape: an agent loop, a tool registry, a permission gate, a sandbox, a plugin model, MCP support, a subagent dispatch path. Different languages, files and names. The clearest divergence was the sandbox: Codex implements real OS-level isolation, so the kernel itself refuses what the agent is not authorized to do; opencode implements soft confinement, path validation and permission prompts with no kernel-enforced boundary.
>
> *Limits: the experiment shows the primitives exist, not that they are equally well implemented, and they are not.*

---

### Sandbox posture is a governance choice

**A vendor's choices about primitives are governance choices.**

The kernel calls are in the source, so you can see whether a sandbox is real or theater. Codex CLI enforces an OS sandbox by default on Linux and macOS; Claude Code ships one as opt-in, and most installations skip it; opencode ships only the decision half. Defaults are versioned, so check yours.

A vendor that ships a real sandbox expects untrusted instructions to arrive - through dependencies, compromised files, injection - and builds defense in depth. One that ships soft confinement expects a trusted environment. Both are defensible; you are the one choosing, and Chapter 2 turns the choice into five layers.

---

### When it breaks

- **A rule the agent consults is not a wall.** Prompt injection can defeat the decision layer; the OS layer is the hard boundary (Chapter 2).
- **A sandbox in the docs is not a sandbox in the kernel.** Confirm the OS layer is on.
- **A plugin is code you did not write.** An unvetted install is a supply-chain risk, and a hook that runs outside the sandbox is unbounded.

---

### Do this Monday

- [ ] Ask the agent you use daily one question per primitive (the Ask lines), note the answers and rate each basic, intermediate or advanced.
- [ ] Check that its OS sandbox is on and note its effort level.
- [ ] Open an open-source agent's repository and find the file that implements the agent loop (twenty minutes: you will get its shape, not every line). Then locate where each of the nine primitives lives.

---

### Go deeper

- **Templates:** [Appendix B.10](#template-b10), plugin vetting; [B.11](#template-b11), the two-agent source walk; [B.9](#template-b9), the effort sweep.
- **Deep dive:** [Appendix D, Chapter 1](#deep-dive-chapter-1) - context-window and tool-count numbers, strict decoding for custom tool schemas, vendor sandbox postures and timelines, the effort evidence, scripted subagent orchestration.
- **Sources:** Appendix C.

---

## Chapter 2
## Guardrails in five layers

*By the end you can score a repository on five layers of control and name the one fix that closes its biggest gap.*

**TL;DR**

- A prompt is a request, not a control. Destructive actions need layers the agent cannot talk its way past: permissions, sandbox, secrets, hooks and telemetry.
- Least privilege is the spine and redundancy is the control. The sandbox is the hard boundary against prompt injection - and even it can have bugs.
- Keep production credentials out of the session, and send the agent's pull requests through the same gates as everyone else's.

---

### What are the five layers?

**A prompt is a request. A control is something the agent cannot talk its way past.**

PocketOS (the Prologue) had a natural-language instruction, which is weaker than layer one. Three lessons get quoted from it, and all three are wrong:

- "The agent ignored its instructions." It did, as agents sometimes do; a prompt is never a hard control for a destructive action.
- "AI agents are unsafe." So is any tool pointed at production without controls.
- "Do not use AI for database operations." That throws away real productivity when layers can bound the risk.

Underneath all five sits least privilege: at every level - the agent, its process, its credentials, its network - grant the minimum that lets the work happen.

```
+----------------------------------------------------+
|  Layer 5: Telemetry (detective)                    |
+----------------------------------------------------+
|  Layer 4: Security hooks (per-action enforcement)  |
+----------------------------------------------------+
|  Layer 3: Secrets (structural protection)          |
+----------------------------------------------------+
|  Layer 2: Sandbox (OS-level isolation)             |
+----------------------------------------------------+
|  Layer 1: Permissions (allow / ask / deny)         |
+----------------------------------------------------+

       Least privilege is the spine.
       Each layer catches what the others miss.
```

*Figure: The five governance layers, layered as defense in depth.*

| Layer | Blocks | Fails when | Would it have stopped PocketOS? |
|---|---|---|---|
| 1. Permissions | Actions the rules or classifier deny | Injection talks the agent into requests the gate never sees | Could have, if a rule gated destructive calls |
| 2. Sandbox | What the kernel refuses: paths, hosts | Never switched on, or has a bug | Could have, whatever the agent decided |
| 3. Secrets | The agent holding a credential | A secret sits within reach | Could have: no production token in the session |
| 4. Hooks | Dangerous categories, before they run | A category has no rule | Could have: forced human approval |
| 5. Telemetry | Nothing; it detects afterwards | Nobody is alerted | No, but "two days until we notice" becomes "two minutes until the on-call engineer is paged" |

No single layer would have saved PocketOS with certainty; any one enforceable layer could have broken the chain. A second 2026 incident, at DataTalks.Club, was the mirror image: Claude Code ran `terraform destroy` against a stale state file. Same cure: confirmation on destructive operations, only the credentials the task needs, and state the team has verified.

---

### Layer 1: Permissions

**Permissions answer one question: is this agent allowed to do this, right now?**

I recommend a classifier that makes the allow, ask or deny call on each action, with a small set of explicit rules on top, such as denying writes to `.env` files. Ten to fifteen overrides per repository is a sound ceiling; past that, your AGENTS.md is too thin, not your rule list too short.

Every team starts here, and a successful prompt injection can defeat it. Necessary, not sufficient.

---

### Layer 2: Sandbox

**The kernel does not listen to the agent's reasoning, so injection cannot talk its way past it.**

For most teams the default is to read the whole repository, write only inside the worktree, reach only allowlisted hosts and block everything else.

Calibrate by friction: if the agent hits the limits often in normal work, widen them. It costs an afternoon to configure, and some agents ship it opt-in, so check yours (Chapter 1).

---

### Layer 3: Secrets

**The safest credential is the one the session never held.**

Do not commit `.env` files, and remember that agents can pick them up from the working directory unasked. Keep secrets in a vault and pull them at runtime through an explicit fetch step the agent can be configured to skip. Put sensitive paths on the sandbox deny-read list: the agent literally cannot read them, whatever the system prompt says.

---

### Layer 4: Hooks

**Hooks are the precision instrument: a programmable gate for the categories your team cares about.**

A hook is code that runs before the agent executes a given kind of action (pre-tool-use) and, against your rules, allows it, asks for confirmation or blocks it. Off-the-shelf plugins ship a baseline: secret leaks in diffs, SQL injection patterns, hardcoded credentials.

Your own rules go on top: any change to currency-conversion logic needs explicit approval; any commit touching the customer table needs a security reviewer. Reach for a hook when permissions are too coarse and the sandbox too blunt.

---

### Layer 5: Telemetry

**The first four layers prevent; telemetry detects, so a failed prevention costs minutes instead of days.**

Log every tool call - each Bash command, file write and external API request, with arguments and results - to a central store the security team owns. Then "which sessions touched the payments service in the last thirty days" is a query, not a grep through eighty engineers' local histories. Watch for:

- an edit outside the assigned task
- calls to hosts off the allowlist
- repeated permission denials: a bug in the rules or an injection attempt
- production credentials in context

---

### Injection arrives through the work itself

**Treat everything the agent reads as untrusted text, and do not count on the agent to spot the attack.**

Anywhere the agent reads natural language is a surface: a Jira ticket whose acceptance criteria say "ignore all previous instructions"; an outside contributor's PR comment with an instruction hidden in a review note; an error message from a flaky third-party test; a harmless-looking repository whose planted error nudges the agent to run a "fix" that pulls in its real payload. I have watched an agent follow an instruction buried in a pasted log file because the operator did not think of a log file as untrusted input.

Constrain what the agent can do regardless of what it has read. The sandbox catches the dangerous action even when the agent is convinced it is legitimate; the hook catches the dangerous category even when "just this once" sounds fine. A poisoned AGENTS.md can change the agent on every session start, one more reason it is reviewed like code (Chapter 6).

---

### Beyond the five

**Two ordinary practices catch what the layers do not.**

- **Environment separation.** The agent does not hold production credentials by default. Production actions go through a separate gate - a human approval, a CI pipeline, a deploy script - that the agent triggers but does not execute end to end.
- **Protected branches, CODEOWNERS and CI policy.** The agent opens pull requests like any contributor; make sure its PRs flow through these rules, not around them.

---

### In the loop

**The rigor lives in the layers below execute; execute just runs the work.**

In Chapter 4's execute phase every tool call passes the permission gate, every Bash command the hooks, every file write the sandbox. A blocked action goes back to the orchestrator to decide.

---

### When it breaks

- **Every layer is code, and code has bugs.** In mid-2026 a red team disclosed two critical zero-click escapes of one vendor's kernel-backed sandbox (patched), and a permission check once skipped its deny rules on very long command chains. That is the argument for five layers.
- **A log with no alert is not a layer.** PocketOS's platform recorded the delete, but no alert fired when an agent session used a production token; the first signal was an unreachable database.

---

### Do this Monday

*Score each layer DEFAULT, CONFIGURED, ENFORCED or MONITORED. DEFAULT or CONFIGURED across the board is normal; ENFORCED or MONITORED everywhere is production-grade.*

- [ ] Pick one repository your team owns, ideally one where an agent already commits code.
- [ ] Permissions: what runs without a prompt? Are `rm`, `terraform destroy`, drop table and force push to main gated?
- [ ] Sandbox: kernel-enforced, or only path validation inside the agent's own code?
- [ ] Secrets: are `.env` files committed? Can the agent reach a production token?
- [ ] Hooks: does any pre-tool-call hook audit, log or gate dangerous operations?
- [ ] Telemetry: would a destructive command show on a dashboard within minutes?
- [ ] For every layer below ENFORCED, write one fix and one owner. That sheet is next quarter's plan; rerun it after every incident.

---

### Go deeper

- **Template:** the scorecard above; for plugins that ship hooks, [Appendix B.10](#template-b10), plugin vetting.
- **Deep dive:** [Appendix D, Chapter 2](#deep-dive-chapter-2) - the named vulnerability classes, sandbox escapes, per-agent sandbox defaults and what the platforms changed after the incidents.
- **Sources:** Appendix C.

---

# Part II - Method

> *The control of workflow: how work is formulated, executed, and verified.*

Architecture answers "what is this thing." Method answers "how do we get work done with it."

---

## Chapter 3
## The bottleneck moved

*By the end you can tell whether a task deserves the full loop, and you know the three habits that make it pay.*

**TL;DR**

- Typing code is no longer the constraint; formulating the work is. Three habits carry it: domain clarity, decomposition, test evidence before "done".
- Run the full loop only when the task touches more than three files, crosses concerns, or is something you would not hand-type. Otherwise type it.
- The rigor costs a slow first month and pays back over the quarter. Start with fifteen lines, not a perfect setup.

---

### The constraint moved

**The bottleneck is no longer producing code. It is formulating the work clearly enough that the agent does exactly what is needed.**

For forty years, output was limited by how fast a developer could type valid code. Autocomplete, better IDEs and AI-assisted typing all attacked that gap. An agent breaks it: in the work an agent handles well, the next hundred lines went from an hour of typing to thirty seconds of waiting. The cost is not zero, but it is no longer the constraint.

Teams that treat the agent as a code generator let it type, handle everything else as before, and spend more time fixing output than the typing saved. Teams that ship well formulate the work so the agent can execute it correctly. Vague specifications produce guessing, and guessing produces output that looks right and is not.

The people building the models agree. In July 2026 an Anthropic engineer opened a field guide to Claude Fable 5 by calling it "the first model where I find the quality of the work is bottlenecked by my ability to clarify its unknowns."

---

### Three habits

**All three are formulation, not generation.**

- **Domain clarity before code.** The agent does not know your business, your conventions or why the codebase looks the way it does. Load that context first: AGENTS.md, skills, the research phase.
- **Decomposition by file and by task.** An agent will attempt a multi-file refactor in one shot, and the result is far harder to review than five coherent steps. Write the plan, execute it, verify each step.
- **Test evidence before "done".** The agent will say the change is complete, sincerely, and sometimes be wrong: "this looks right" is not "I ran the tests." Use behavioral tests that exercise the change. If you cannot test it that way, it probably should not have been an agent task.

The first two habits define the expected outcome; the third measures against it.

---

### The four unknowns

**Every gap in a prompt is one of four kinds of unknown, and each has a different fix.**

The same guide splits the human half of formulation into four questions. The mapping onto this manual is mine, not his.

| Quadrant | What it is | Where this manual handles it |
|---|---|---|
| Known knowns | What your prompt actually states | The prompt itself |
| Known unknowns | Questions you know you have not settled | Open questions in the research note, settled before the plan (Chapter 4) |
| Unknown knowns | Context so obvious you would never write it down, though you would spot a violation instantly | The team instruction file, AGENTS.md (Chapter 6) |
| Unknown unknowns | What neither of you thought to ask | The blind spot pass and implementation notes (Chapter 4), the quiz (Chapter 5) |

---

### The loop test

**Run the full loop if any one of three triggers is true. If none is, type it.**

Formulating well is paid before the agent writes a line, and for trivial work it costs more than the agent contributes. The loop pays back when at least one holds:

- **The work touches more than three files.** The blast radius is large enough that an unguided agent will get something wrong.
- **The change crosses concerns.** Schema plus service layer plus UI, where one misstep cascades.
- **You would not hand-type it.** It is novel, or large, or in code you do not know well enough to write by hand.

A two-line bug fix needs no research note; a one-line config change needs no plan. Use the loop when formulating costs less than the agent getting it wrong.

---

### Two teams, one quarter

**The cost of rigor is paid in the first month; the benefit keeps paying after it.**

The clearest case I have seen: two teams at the same company, in adjacent areas of the same product, using the same agent.

Team A turned the agent loose immediately and celebrated the early velocity. By month three they were shipping at roughly the pre-agent baseline, with higher defect rates and visibly drained senior reviewers.

Team B spent month one on the practice: AGENTS.md drafted and iterated, skills written for the team's patterns, hooks configured. They shipped no agent-led work that month. By month two they were back at baseline velocity. By month three they shipped at noticeably better quality and velocity than before the agent.

Discipline feels slow; the lack of it costs more, and that stays invisible until you look at cycle time across a quarter. This was a field observation, not a controlled experiment, and adjacent teams are not independent samples.

---

### Start small

**The practice does not need to be perfect to pay.**

A fifteen-line AGENTS.md beats none, and a half-finished research note beats none. Teams that build the perfect workflow before running it get stuck, because there is always one more rule, skill or hook to add.

Write fifteen lines on what you know is dangerous, run a few stories through the agent, and add the rules that would have prevented the failures you saw.

---

### When it breaks

- **Looping everything, or nothing.** Every task through the loop slows you down; none misses the wins. Run the loop test first.
- **Judging at week four.** Team B shipped no agent-led work in month one. Measure across the quarter.

---

### Do this Monday

- [ ] Put the next task you were about to dispatch through the loop test. If no trigger fires, type it.
- [ ] If one does, write a 200-word research note before dispatching.
- [ ] Write one sentence saying what "done" means for the change, and which test will show it. No AGENTS.md yet? Write its fifteen-line skeleton too.

---

### Go deeper

- **Templates:** [Appendix B.2](#template-b2), the AGENTS.md skeleton; [B.3](#template-b3), the six-phase loop checklist.
- **Deep dive:** [Appendix D, Chapter 3](#deep-dive-chapter-3) - the Fable 5 unknowns frame, the METR trial and its caveat, and the February to April 2026 regression.
- **Sources:** Appendix C.

---

## Chapter 4
## The six-phase loop

*By the end you can run one feature through research, plan, execute and ship, and you know which gates are yours.*

**TL;DR**

- Six phases: research, plan, execute, review, verify, ship. Each one produces an artifact you can read, and each one ends at a gate.
- The plan is the gate where a human matters most. A few minutes reading it saves an afternoon of unwinding execute.
- Ship is a normal pull request with the evidence attached. There is no AI lane.

---

### What is the six-phase loop? {#what-is-the-six-phase-loop}

**Every phase produces an artifact and ends at a gate.**

The six phases are research, plan, execute, review, verify, ship. Each phase is a skill - a packaged set of instructions the agent loads when the phase is active - with a clear input, a clear output and a clear hand-off to the next phase. Superpowers is one implementation; GitHub Spec Kit, BMAD frameworks and team-built skill collections share the same loop.

```
   +--------+    +------+    +---------+    +--------+    +--------+    +------+
   |Research|--->| Plan |--->| Execute |--->| Review |--->| Verify |--->| Ship |
   +--------+    +------+    +---------+    +--------+    +--------+    +------+
       ^                          |              |
       |                          v              v
       +----- failed plan? ---- replan       failed verify? --- back to plan
```

*Figure: The six-phase loop. Most failures route back to Plan, not back to Research.*

| Phase | Artifact | Human gate | Failure caught |
|---|---|---|---|
| Research | Research note (2-4 pages) | Domain plausibility check | Missing context |
| Plan | File-level task plan | Scope and order review | Bad decomposition |
| Execute | Diff + per-task reports | None or light | Implementation drift |
| Review | Spec compliance + quality reports | Senior review | Wrong or weak code |
| Verify | Test evidence (failing -> passing) | QA or owner review | Behavioral failure |
| Ship | PR with evidence trail | Normal PR process | Process violation |

**The loop stands on a well-defined expected outcome.** The agent can build almost anything you describe, but it cannot know which thing you meant. Research surfaces what is undecided, you settle it, the plan turns it into checks, and verify measures the result against it. Skip that and "done" is whatever the agent decided.

---

### The feature

Here is one feature, followed through every phase. It is small: add a `priority` field to the `Wire` record in a regulated banking service.

Priority is one of low / normal / high / urgent and defaults to normal. The urgent flag triggers a separate compliance-review queue.

---

### Research

**Research produces a note, not code - and its open questions are yours to settle.**

I asked the agent to read the codebase and write a research note. It named four files I would not have found in an hour of grepping:

- the `Wire` record itself
- the migration directory
- the compliance-review-queue service
- the audit-log emitter

It also raised an open question: should priority be an enum or free text? The regulator's spec uses free text in some documents and an enum in others. I picked enum. That was not a detail - it defined the target every later phase was checked against.

A research note is two to four pages and covers:

- the files that will be touched
- the conventions those files follow
- the existing tests that cover the area
- related concepts elsewhere in the codebase
- open questions where a human has to decide

Teams skip research most often, because it produces no code. In my experience it is the highest-leverage phase: a bad note guarantees a bad plan, and a good one grounds the plan in the real code instead of the agent's first guess.

If the task sits outside your own domain, run a blind spot pass first: ask the agent to help you find your unknown unknowns, and tell it plainly what you do not know. It calibrates to the expertise it infers from your vocabulary, so false fluency hides its assumptions.

Commit the note with the change. Six months later, when someone asks why the code is shaped this way, the answer is in the repository.

---

### Plan

**The plan is the gate where you matter most.**

The agent turned the note into a six-task plan:

1. Add the database column with a default.
2. Update the `Wire` record class.
3. Update the wire-builder service.
4. Update the API contract.
5. Update the compliance-routing logic to read the new field.
6. Update the audit-log emitter.

Each task touched one file or one pair of files. Task five depended on task four's contract change; the order was right and the agent had flagged the dependency. Approved.

A plan you can approve has three properties:

- **Every task names the file, the change and the check that proves it worked.** Each is sized to two to five minutes - small enough that a failure is recoverable.
- **It names the tests to add or update.** A plan without tests is incomplete and goes back.
- **It states what "done" means for the whole change**, not only per task. That is the outcome verify will check.

Then you read it. Push back on tasks that are vague, too large or wrongly ordered. Add what it missed, remove what is out of scope. Only then does execute start.

The review takes a few minutes. It saves an afternoon when the plan was wrong and you would have found out during execute, where it is much harder to unwind.

---

### Execute

**One subagent per task, one writer per file.**

Six subagents ran in parallel, one per task, each constrained to its file. They returned in under three minutes. Five tasks had passing tests on the first run.

The sixth, the audit-log emitter, also had a passing test - but the test was wrong. It asserted the old log format. Green, and wrong. Chapter 5 picks up how that got caught.

Each subagent works in its own isolated context: it reads only what it needs, makes its change, runs the plan's check and reports back. Task one's confused reasoning cannot pollute task four.

Isolation is not a silver bullet. The rules that keep it working:

- **Split only when the tasks are independent by file or by module.** Six subagents each editing one file is safe. Six editing the same feature across overlapping files is a recipe for expensive conflicts, which eat the speed you went parallel for.
- **Fewer is usually faster.** Three well-scoped subagents finish faster than eight overlapping ones.
- **Read the orchestrator's hand-offs with skepticism.** It still holds a summary of every task, and an imprecise summary of task one can lead task four to contradict it. I have watched six subagents produce mutually inconsistent edits for exactly this reason.
- **Keep an implementation-notes file.** Every deviation from the plan and why, every edge case the plan never mentioned, every decision a subagent made that the plan left open. Recorded when it happens, not compressed into a hand-off later.

When a task fails, the orchestrator retries, routes around it, or stops and asks you. Most failures are recoverable on a second attempt. A blocking failure means the plan needs revision, and the loop goes back to plan.

---

### Review and verify

**Review checks the diff against the spec; verify checks the behavior against the outcome.**

On the wire, review caught the audit-log test and a migration with no down direction, and verify ran the full suite plus a smoke test against staging. Chapter 5 owns both phases: how to read an agent diff, and why a green suite the agent wrote is evidence, not proof.

---

### Ship

**Ship is a normal pull request. There is no AI lane.**

The agent commits with a structured message, pushes the branch and opens a pull request whose description says what changed, why, how it was verified, what risks remain and who is tagged to review.

On the wire, the PR carried the research note, the plan, the per-task reports, both reviews and the test evidence. A senior reviewer spent eleven minutes on it and asked one question: should the urgent flag be observable in the metrics dashboard? I had not thought about it. Approved, merged.

That PR is exactly the artifact the team already knows how to review. The agent does not replace your shipping process; it feeds it better-formulated work.

---

### What it costs in time

**On a healthy workflow, the human gates are the rate limiter, not the agent.**

On a small feature the full loop takes twenty to thirty minutes of wall clock; on a medium one, an hour; on a large one, a few hours - work that would have taken days without the agent. The agent runs for maybe a third to half of that. The rest is you reading the note, reviewing the plan and approving the diff.

The wire feature took ninety minutes from "let's add a priority field" to merged code. The difference is the regulated context: a 3,400-test suite, a staging smoke test and a contract diff for the regulator. Small in scope is not small in ceremony.

If a small feature takes three hours, your gates are over-engineered or run as slow back-and-forth instead of a focused pass. The agent will not save you from your own meeting culture.

---

### When to run less of it

**Skip a phase only if you can name what already does its job.**

Chapter 3's test tells you when the loop pays at all; inside the loop the same accounting applies.

One team I watched ran for most of a year on what looked like half the loop: research was a comment thread, the plan was three bullets in the PR. It worked because the functions had moved into the team's walls - a small senior team that built the codebase, a strict CI suite and a serious PR culture. The six phases are functions that have to happen somewhere. If you cannot say where, the phase stays.

---

### When it breaks

- **The gates are requests, not walls.** Skill instructions ask for "tests in the plan"; strict enforcement needs a project-specific PreToolUse hook (Chapter 2).
- **Parallel subagents on overlapping files** produce inconsistent edits. Re-scope by file or module, or run the tasks in sequence.
- **Long sessions drift.** The agent re-answers settled questions and forgets constraints. That is context contamination, and Chapter 6 covers the fix.

---

### Do this Monday

- [ ] Pick one task that passes Chapter 3's test and ask the agent for a research note before any code.
- [ ] Settle every open question in the note, in writing.
- [ ] Read the plan: every task names a file, a change and a check; tests are listed; there is a "done when" line. Push back once before approving.
- [ ] Execute with one subagent per file and an implementation-notes file.
- [ ] Ship it as a normal PR with the note and plan attached.
- [ ] Time each phase. Note which ate the most wall clock and which produced the most value. They are often not the same.

---

### Go deeper

- **Template:** [Appendix B.3](#template-b3), the six-phase loop checklist.
- **Deep dive:** [Appendix D, Chapter 4](#deep-dive-chapter-4) - when splitting into subagents pays, forking workers vs isolating reviewers, and the vendor autonomy and scope prompt blocks.
- **Sources:** Appendix C.

---

## Chapter 5
## Review and verify

*By the end you can read an agent's diff in the right order, say how much a green test suite proves, and set the controls that keep verify honest.*

**TL;DR**

- Agent reviewers sweep the mechanical layer. Your read is for business correctness and architectural fit.
- An agent diff fails at intent, not syntax, so read it from the outside in: the shape of the change, then the tests, then the lines.
- A green suite the agent wrote is evidence, not proof. Four controls keep verify from grading its own homework.

---

### Who checks what

**Each check sees what the others cannot, so the loop runs all of them.**

| Check | Reads | Asks |
|---|---|---|
| Spec reviewer | Note, plan, notes file, diff | Does this match the spec? |
| Quality reviewer | The diff only | Is this correct by the team's standards? |
| Human read | Diff-stat, tests, boundaries, new names | Is the business rule right? Does it fit the architecture? |
| Verify | New tests, full suite, staging, contract diff | Does the behavior meet the plan's "done"? |

---

### The wire, continued

**A suite that is happy can still be wrong.**

Chapter 4 left the audit-log emitter with a test that was green and wrong. The spec-compliance reviewer, comparing the diff to the plan, caught that the test asserted the old log format, and flagged a migration with no down direction. The code-quality reviewer, who saw only the diff, found nothing of note. The implementer subagent fixed both and re-ran the relevant tests.

Verify then ran the full suite of 3,400 tests and a smoke test against the staging compliance-routing service, and produced a diff of the API contract change for the regulator's review. All passing. That evidence went into the pull request at Chapter 4's ship step.

---

### Review: two agents, then you

**Two reviewers, in sequence, with different prompts.**

One reviewer doing both jobs blurs the signals, so the quality reviewer is a different agent with a different prompt, reading only the diff. Four rules keep it useful:

- **Scope it to correctness.** A reviewer told to review "as a senior would" always finds something, and a diff re-polished each round grows abstractions nobody asked for.
- **Keep it blind to reviewer one.** Judges anchor on a prior score, and neither chain of thought nor an explicit warning removes the anchor.
- **Require accept-or-rebut on every finding.** Track the repair rate, meaning findings fixed or rebutted with a reason, not the reviewer's accuracy. A finding nobody acts on is worth nothing.
- **Cap the rounds.** In one measured verify-and-repair loop, late rounds re-opened settled work about as often as they fixed it.

Findings carry a severity: critical blocks ship, important is fixed before ship, suggestions go in the PR description for the human reviewer.

---

### How do you review an agent-written diff? {#reviewing-agent-diffs}

**Read from the outside in: intent first, lines last.**

A human diff fails at execution: a typo, an off-by-one, a forgotten edge case. An agent diff compiles, passes lint and reads like code your team would merge unremarked. It fails one layer up, at intent and context: a business rule that is plausible and wrong, the right code in the wrong layer, the code a good engineer would write for a slightly different task. Fluency is not correctness.

So spend the first ten minutes above the code:

1. **Diff-stat against the plan.** Does the shape of the change match the ask? A file the plan never named is the first flag: the agent decided something you did not ask it to.
2. **Read the tests for what they assert,** not whether they pass. Green is the cheapest signal, and the one you already have.
3. **Check the boundaries your team wrote down:** forbidden patterns in AGENTS.md, layer conventions, dangerous modules. The agent crosses them confidently, in fluent style, so a violation looks clean.
4. **Grep every new name the diff introduces** that you do not recognize. The call that does not exist reads as plausibly as the one that does (Chapter 6 has the cross-check).
5. **Only now, line by line,** spending the minutes the reviewers bought you on business correctness and architectural fit.

Before you approve, have the agent quiz you on the change: what happens at the edges, which module owns the new behavior, what breaks first if an assumption is wrong. Three or four questions, one minute. If you cannot answer, you were rubber-stamping with extra steps. Appendix B.8 is this order as a one-pager.

---

### Verify

**Verify measures the behavior against the outcome the plan defined.**

Execute already ran the existing tests. Verify runs the new ones and asks whether the change is correct, not merely whether anything else broke.

For frontend work, write them against the accessibility tree, the structure browsers keep for screen readers, not pixels or CSS selectors. A Playwright test that finds the field labeled Priority, changes it, clicks Save and checks the new value asserts behavior, and survives a restyle or a component-library swap.

---

### Can you trust the tests the agent writes? {#trusting-agent-tests}

**Green tests are evidence, not proof.**

They are evidence the change does what the test says, not that the test says the right thing, as the audit-log test showed. Coverage does not close the gap: it measures which lines ran, not whether anything meaningful was checked, and an agent optimizing a coverage gate writes tests that call the code and assert nothing of consequence. Characterization tests, Chapter 8's first fix for an untested codebase, lock in current behavior, not correctness, and preserve a bug as faithfully as a feature: a regression net while you migrate, never proof.

So review the agent's tests like its code, checking the assertions against the spec. A test written from the implementation agrees with the implementation; the assertion has to come from the intent.

The agent also optimizes the evidence it can see. On SpecBench, frontier agents scored near 100% on the visible tests and fell 43 to 48 points short on a hidden set. That is not cheating in the human sense; it is a system doing what the gate rewards. Four controls close the gap:

- [ ] **Held-out tests** the agent never sees, written from the intent and run only at verify.
- [ ] **Sealed git history and no network egress** while verify runs, so it cannot look the answer up.
- [ ] **A PreToolUse hook** that blocks edits to linter and test configuration and blocks `commit --no-verify` (the deny rules from Chapter 9, now on every run).
- [ ] **Explain before fix.** The agent states why a test fails before it may fix it; a fix without a diagnosis is the one most likely to have edited the assertion instead of the code.

---

### When the toolkit does the looking

**Review agents are a filter in front of human judgment, never a substitute for it.**

A team I worked with installed a full review toolkit: agents for swallowed exceptions, weak tests, security issues and stale docs. It caught real bugs week after week, the senior reviewers learned to trust the green checkmarks, and within a quarter their fifteen-minute reviews had become three-minute scans. Nobody decided that; attention drifts away from work that appears to be done.

Then a PR that every agent had passed - tests green, no security findings, clean diff - applied a discount rule to the wrong customer tier and ran in production for weeks until a support ticket surfaced it. The toolkit had worked as designed: it removed the mechanical findings from human review, and the judgment drifted away with them. That is Chapter 9's uncalibrated delegator, at team scale.

The fix was an explicit floor: a minimum review on business correctness and architectural fit for every agent-touched PR, tracked as a number next to defect rate. The read order above is that floor made concrete.

---

### When it breaks

- **The read decays into a glance at checkmarks.** The decay is invisible from the inside; the pre-approval quiz makes it measurable.

---

### Do this Monday

- [ ] Read your next agent diff in the order above, then have the agent quiz you before you approve. Note what you could not answer.
- [ ] Open the last three tests the agent wrote. Do the assertions come from the spec or from the code?
- [ ] Split review into two prompts: spec compliance first, then correctness on the diff alone. Require accept-or-rebut on every finding.
- [ ] Add the four verify controls, starting with explain-before-fix.
- [ ] Set a minimum human review for agent-touched PRs and track it next to defect rate.

---

### Go deeper

- **Templates:** [Appendix B.8](#template-b8), the agent-diff read order; [B.3](#template-b3), the loop checklist.
- **Deep dive:** [Appendix D, Chapter 5](#deep-dive-chapter-5) - the review measurements, SpecBench and Cursor in full, and the accessibility-tree caveat.
- **Sources:** Appendix C.

---

## Chapter 6
## AGENTS.md and context

*By the end you can write an AGENTS.md in which every line earns its place, and run agent sessions that stay sharp.*

**TL;DR**

- AGENTS.md is team infrastructure: short, failure-driven rules, reviewed like code and owned by one champion.
- Keep it under 200 lines with fixed contents and no repo map. The agent reads before it cites; you grep what it names.
- Context is working memory. One unit of work per session, durable state in files, a clean restart at the first sign of drift.

---

### What is AGENTS.md? {#what-is-agents-md}

**AGENTS.md is the team's agreement with the agent, committed in git.**

It is a markdown file in the repository root that the agent reads at session start, before any prompt. It turns "what the agent thinks is reasonable" into "what the team has agreed is reasonable", reviewable in a pull request. It is the manually owned layer of the Memory primitive from Chapter 1: the part the team writes.

### AGENTS.md vs CLAUDE.md: what's the difference? {#agents-md-vs-claude-md}

**Same file, same discipline, different name.**

AGENTS.md is the vendor-neutral name, read natively by Codex CLI, Cursor, GitHub Copilot, Gemini CLI and most others. CLAUDE.md is the Claude Code variant. The format and the loading are equivalent.

---

### The story: one line, three hours a month

A team I worked with had used a coding agent for six months when a senior engineer brought me a complaint. "Every time we generate an API endpoint, I have to fix the validation. Always the same fix. The agent puts it in the wrong layer."

"Why isn't the rule written down?"

"We never wrote it down. We just keep fixing it."

We counted. Last month the agent had generated twelve endpoints and he had fixed the validation layer in eleven, about fifteen minutes each. Three hours of senior time a month, absorbed into "normal review work".

We wrote one line in AGENTS.md: "Bean Validation annotations on DTOs at the controller boundary; service-layer methods trust their inputs." We added it to the pull request template as a reviewer prompt and tagged the already-correct endpoints as reference examples. The next twelve endpoints needed zero validation-layer corrections.

The rule did not make the agent perfect. It removed one repeated correction, and that is the file's whole job.

---

### Six rules for the file

**Six rules, each with a test you can apply to any line.**

| # | Rule | You met it when |
|---|---|---|
| 1 | One line, one checkable constraint | It names the layer, the mechanism and an example |
| 2 | Failure-driven only | You can name the failure and when you last saw it |
| 3 | Fixed contents, no repo map | Forbidden patterns, conventions, commands, glossary, one pointer |
| 4 | Under 200 lines, hard cap | Past it, the newest rules get ignored |
| 5 | Treat it as code | Git, PR review, one rotating champion |
| 6 | Read before cite | Every name was read this session or found by grep |

---

### Rule 1: write rules the agent can check

**A rule the agent cannot check is decoration.**

| | The rule |
|---|---|
| Bad | "Always follow our coding standards. Be careful with validation. Use the right architecture." |
| Good | "DTOs own controller-boundary validation via Bean Validation annotations. Services trust validated DTOs and do not re-validate. Never add validation annotations inside service methods. Examples: UserCreateController, AccountUpdateController." |

The bad version sounds responsible, but "careful" is not a constraint and "the right architecture" depends on context the rule never gives. The good version is the story's line, hardened: it names the layer, the mechanism, the rule and two examples to pattern-match against. Forbidden patterns follow the same form, with the reason in a clause; Appendix B.2 has three.

### Rules 2 and 5: earned by failure, owned like code

**A rule lands only if a real failure earned it, and a champion keeps the file honest.**

- **Review it like code.** AGENTS.md is code in the sense that the agent executes against it. The reviewer asks: what failure does this prevent, and when did we last see it? "We have not seen it, but we might" does not land, because speculative rules pile up into bloat.
- **Keep a mistake journal.** One entry per real incident, with the rule that prevents a repeat and an evidence pointer, the commit or the incident; B.2 has a sample entry.
- **Name a champion.** One person owns the file and the journal; everyone edits through pull requests and the champion curates. Each quarter the champion asks of every entry whether it saved anyone in the last three months, and retires those whose underlying problem is gone, with the reason in the commit message; a rule that still prevents a rare failure stays. Then the role rotates.

### Rules 3 and 4: fixed contents, hard cap

**Put in forbidden patterns, conventions, commands and a glossary. Leave the map out.**

- **Forbidden patterns, conventions and journal entries**, one line each.
- **Exact build and test commands.** Without them the agent guesses, and guesses are sometimes wrong.
- **A domain glossary.** In pretraining "transfer" means many things; in your bank it means one, and a "wire" is only the inter-bank kind.
- **One pointer line:** "Repository layout and module map: `docs/architecture.md`. Read it before touching a module you have not seen this session."

The map stays out. The agent derives the layout from the tree in seconds. A February 2026 study found that context files as a whole raised inference cost by over 20% without generally improving success, and that the repository overview was the part that did not help (Appendix D). The map lives in `docs/architecture.md`, read on demand; Chapter 7 produces it.

**Under 200 lines.** The file loads at every session start, so each line spends context the task needs, and instruction-following degrades as the rule count grows (Appendix D). Drop rules untriggered in six months and keep each rule to a line.

A banking team's file grew to about nine hundred lines in six months and the agent began ignoring the newest rules. We cut it to ninety, moving conventions into skills that load on detection and past-mistake history into the architecture document, and compliance jumped within a week. The cap forces opinion, and the opinion is the value.

### Rule 6: when the agent confidently lies

**The agent invents files, functions and options, so make it prove what it cites.**

It will cite a file that does not exist, a function the library never exposed, an option deprecated three versions ago. The output looks plausible and is wrong; the agent pattern-matches against similar code and does not know it is guessing. Three mechanical tactics:

- **Read before cite.** Anything the agent references must have been read this session. AGENTS.md can say so: "Before referencing any function, read the file that defines it. Citations without preceding reads are drafts to verify."
- **Grep every new name.** No hits means the function probably does not exist, or lives in a vendored dependency the agent cannot see. It takes seconds and catches the most common fabrications.
- **Hook the citations.** If the agent cites a file and line, a few lines of bash in a hook can verify the line exists (Chapter 2).

---

### Context hygiene {#context-hygiene}

**The window is the agent's working memory, so load what the task needs and nothing else.**

Everything in the window competes for the same bounded attention. Long sessions fail through context contamination, where settled and stale material crowds out the live task; it is the biggest single reason long agent sessions go wrong. Four habits prevent it.

- **Pointers over payloads.** Link the architecture document from AGENTS.md, do not paste it. The 200-line cap is this rule applied to the always-loaded layer.
- **One unit of work per session.** The research note, plan and per-task reports from Chapter 4 are committed so the next session starts clean and reads its state from the repository, not from a conversation's history.
- **Watch for the four signs.** The agent re-answers a question it already settled. It cites a stale version of a file it edited an hour ago. It forgets a constraint it honored twenty minutes back. Its edits get sloppier as the session runs. Do not argue with the session: commit the durable state, end it, start clean. The fresh session is not lost progress; it is the progress, read back without the noise.
- **Treat compaction as a handoff.** Summarizing a full window drops detail, so anything that matters and is not in a file is gone. If you compact, give the compactor a keep-list: the plan, the open questions, the deviations in the implementation notes, the exact commands that worked.

---

### When it breaks

- **The file is a request, not a wall.** The agent can still violate AGENTS.md. Anything that must never happen needs a hook (Chapter 2).
- **Old entries turn into folklore.** An entry with no evidence pointer is hard to retire, and a graveyard of rules is almost as useless as none: the team stops trusting any of them.

---

### Do this Monday

- [ ] Draft a fifteen-line AGENTS.md for one repository: three forbidden patterns, one real mistake-journal entry from last quarter, the exact build and test commands, one pointer line to where the code lives. Commit it.
- [ ] Find your own validation story: a correction you keep making in review. Write it as one checkable line and add it to the PR template as a reviewer prompt.
- [ ] Add the read-before-cite line, grep every new name in the next agent diff, and name a champion with a quarterly review date.
- [ ] In your next long session, note which of the four signs shows up first. Then commit the state and start clean.

---

### Go deeper

- **Templates:** [Appendix B.2](#template-b2), the AGENTS.md skeleton (it carries the precedence line); [B.7](#template-b7), context hygiene on one page; [B.11](#template-b11), bootstrapping the file on a repository.
- **Deep dive:** [Appendix D, Chapter 6](#deep-dive-chapter-6) - the context-files study, the rule-count cliff, mistake-journal mechanics, and the compaction and cache measurements.
- **Sources:** Appendix C.

---

## Chapter 7
## Map it first: architecture review

*By the end you can produce a corrected architecture map of a codebase nobody remembers, and read the same run as a verdict on whether agents belong there.*

**TL;DR**

- One prompt, one agent run and an hour of human review give you `docs/architecture.md`, a map the team and the agent can start from.
- The agent gets roughly 70% right. The review is the work, and the 45-minute estimate assumes you know the domain.
- The same run is a diagnostic. If the agent cannot produce a coherent map, the codebase is not ready for autonomous work (Chapter 8).

---

### The workflow

**Make the agent read the code first, then correct what it wrote and commit the result.**

Most teams own a codebase that fits one description: the author left, the README describes a build that no longer works, the code earns money and nobody wants to touch it. Getting productive in it used to take a senior engineer weeks. Now it takes ten to twenty minutes of agent time plus an hour of human review.

The prompt asks for nine sections, from purpose and data model to risks and unknowns, with file-and-line citations throughout; the full text is Appendix B.1. On a moderately complex Spring Boot service it produces a ten-to-fifteen-page document in under fifteen minutes, roughly 70% correct. If the codebase outgrows one context window, fan out: one subagent per module, the orchestrator assembling the parts.

---

### The case

**The agent did not decide the rewrite was unnecessary. It gave the domain experts enough structure to decide faster.**

A banking team owned a customer onboarding system: about sixty thousand lines of Java, written between 2018 and 2024 by a rotating cast of contractors. The team had been assembled in 2024 from three acquisitions, and nobody had been there for the original build. The README described a 2020 architecture, and the documentation listed two of the build's three steps. They were weighing a complete rewrite, estimated at eighteen months, because "nobody understands it well enough to maintain it confidently."

I asked for fifteen minutes and a terminal. I pasted the review prompt with two additions: the domain (customer onboarding, regulated banking) and a request to flag anything that looked compliance-sensitive. Eighteen minutes later there was a thirteen-page document, wrong in three places:

- It called the deduplication service a "search service" because the implementation used the search infrastructure. Its business purpose was preventing double-creation of customer records.
- It described a scheduled job in confident detail. On inspection it was commented-out code that had not run in production for three years.
- It missed that a third-party dependency was deprecated and carried a security advisory. The agent had no access to the advisory database, so I added that myself.

The corrected document went into the repository, and the team did not do the rewrite. It showed them the two modules that really needed replacing, the deprecated dependency among them, and they replaced just those the following quarter. I ran this exact workflow on this exact codebase, and the company saved nine person-months of rewrite effort that they would otherwise have spent and regretted.

| | |
|---|---|
| **Context** | Regulated banking team, ~60k LOC Java service written 2018-2024, stale documentation |
| **Agent time** | ~15-18 minutes |
| **Human correction time** | ~45 minutes (reviewer knew the customer onboarding domain) |
| **Outcome** | Two modules carried the technical debt; the 18-month rewrite became a targeted 3-month replacement |
| **Limitations** | The workflow accelerates domain knowledge, it does not substitute for it |

---

### Correct it

**The agent's map is a draft, and the 45-minute estimate assumes a reviewer who knows the domain.**

I had never seen that codebase, but I had built onboarding systems before, so I knew what a deduplication service and a regulated-banking compliance path usually look like. The agent's mistakes looked wrong to me. A reviewer new to both the codebase and the domain has no such prior: the misidentifications still look plausible, they cannot tell which to flag, and the correction takes hours, not 45 minutes. The workflow still works; the human side of it costs more.

Check the map against five things:

- Module purposes against business reality, not implementation infrastructure.
- Anything described as live that may be dead or commented out.
- Dependency and advisory facts the agent cannot see.
- The compliance-sensitive paths.
- Every ambiguity the agent itself flagged.

---

### Commit it

**The corrected document is the entry point for all later work.**

Put it at `docs/architecture.md`. New hires read it first, senior engineers consult it before touching an unfamiliar part, and the agent opens it on demand, when a task touches a module it has not seen, instead of re-deriving the architecture. AGENTS.md holds a pointer to the file, not the layout (Chapter 6).

---

### Review as diagnostic

**If the agent cannot produce a coherent map, that is a kill signal.** The same run is the cheapest test of whether agentic work will succeed on a codebase.

- **Coherent map, reasonable correction:** the codebase is in good enough shape for the agent to be useful on later work.
- **Garbage:** the codebase is so tangled that even reading it fails. It sits in the red zone of Chapter 8, and the fix is human-led documentation first, not a different prompt.

Either answer is worth the price: fifteen minutes plus an hour, with a bounded downside. Chapter 8's kill signals are the systematic rubric; this run is the cheap test that comes first.

---

### When it breaks

- **Unreviewed output.** The 70% is a draft, not documentation.
- **A reviewer with no domain knowledge** cannot tell which plausible mistakes to flag. Budget hours.
- **The map goes stale.** Re-run the review whenever the codebase changes substantially.

---

### Do this Monday

- [ ] On the codebase your team understands least, send the Appendix B.1 prompt with one added line naming the domain (about 15 minutes of agent time).
- [ ] Correct the output against the five checks above.
- [ ] Save it as `docs/architecture.md`, commit it, and add one pointer line to AGENTS.md. Do not paste the layout in.
- [ ] Judge the run: a coherent map means go on; garbage means a kill signal, so read Chapter 8 before any production change there.
- [ ] Repeat on your next two or three poorest-understood codebases, an hour each, and note which produce a clean map.

---

### Go deeper

- **Template:** [Appendix B.1](#template-b1), the architecture review prompt.
- **Deep dive:** [Appendix D, Chapter 7](#deep-dive-chapter-7) - why plain code search beats a vector index here, and Understand Anything, the visual alternative.
- **Sources:** Appendix C.

---

# Part III - Reality

> *The control of adoption: where the method works, where it does not, and how to tell.*

---

## Chapter 8
## Should the agent touch this code?

*By the end you can score any codebase green, yellow or red, and say which work the agent should and should not do there.*

**TL;DR**

- Score a codebase on eight kill signals: 0-1 is green (agent-led), 2-3 yellow (human-led), 4 or more red (fix the codebase first).
- Signal 6, a team that cannot evaluate the output, weighs more than the others: present, it makes that work red whatever the count.
- Count by intensity, not presence, and score per project, not per company.

---

### When should you not use AI coding agents? {#when-not-to-use-agents}

**Some codebases should not get an agent yet, and saying no there is what lets you say yes everywhere else.**

The reason is not that the agent or the team is bad: the codebase has properties that make agentic work unsafe, unproductive, or both. The rubric is eight kill signals, each a property of the codebase or the team. Without it, every project becomes an AI project, and the failures of the ones that should not be taint the whole approach.

---

### The eight kill signals

**Each signal breaks agent work in its own way, and each has a first fix.**

| Signal | What it looks like | Example | First fix |
|---|---|---|---|
| 1. No tests | No suite, or one nobody runs | An edit broke an untested reconciliation module; it surfaced two months later | Characterization tests |
| 2. No documentation | Only the original author knows why | The agent "simplified" a fee tier that had a 2017 regulatory carve-out | Architecture review (Chapter 7) |
| 3. Tight coupling | Edit one file, three others break | Three modules in a 14-year-old import cycle | Break the worst coupling |
| 4. Scattered rules | One rule lives in several places | Transfer limit in a UI config, a service constant and a database trigger | One source of truth |
| 5. Regulatory constraints | Every change needs a traceable approval | Anti-money-laundering changes need three sign-offs the agent cannot route | Approval workflow |
| 6. Team cannot evaluate output | No one can judge the result in some domain | A junior ships agent-written encryption (below) | Restrict scope or add an expert reviewer |
| 7. Model-context fit | Thin public corpus (COBOL, proprietary DSLs) | An in-house workflow engine; the agent applied another framework's patterns | Add docs and skills, or a better-fit model |
| 8. Velocity-of-change | A framework is moving under the agent | React 18 idioms in code that needed 19 | Name the target version in [AGENTS.md](https://agents.md/); slow the agent on touched paths |

---

### Signal 1: no tests

**Close this one first, and let the agent help - as a net, not as proof.**

Ask the agent for characterization tests of what the module does today; the spec is "whatever the code currently produces", which is bulk work it does well. It is a real investment of time, and if the team will not make it, the answer is no. The tests lock in today's behavior, bugs included: a net, not proof (Chapter 5).

---

### Signal 6: the team cannot evaluate the output

**This is the most important signal, and the one teams misread most often.**

A junior is assigned a story to add a cryptographic verification step to the payment flow and dispatches the agent. It produces a module using AES-256 in CBC mode with a hardcoded initialization vector. To someone new to cryptography it looks right: it compiles, the unit tests pass, and the senior cryptographer is on parental leave for three months. The junior ships it, and the vulnerability sits in production for six months until a penetration test finds it.

The agent did exactly what was asked. Its output looked right and was wrong, and nobody was placed to see it.

Teams read this as "we need more senior engineers", which does not scale on a six-month timeline. The structural answer makes senior review unavoidable: a hook that blocks the merge until a senior approves, review agents that run before the human sees the diff, or an AGENTS.md rule that keeps the agent out of cryptography modules until a flag is set.

This signal is weighted more heavily than the others: it is counted with them, and it also overrides the count. A codebase that scores zero on signals one through five but yes on signal six is still red for the relevant work. The other seven cost productivity; this one ends in compliance disclosures and incident retrospectives. The fix is to build the capability, bring in someone who has it, or keep the agent away.

---

### Are AI coding agents production-ready? {#are-agents-production-ready}

**It depends on the project: the count picks the color, and signal 6 alone makes it red.**

```
  Signal count       Color       Mode
  ============       =====       ====

  0 - 1              GREEN       Agent-led, normal velocity
  2 - 3              YELLOW      Human-led, agent support
  4 +                RED         Stop. Fix codebase first.

  Signals (count each present):
   1. No tests          5. Regulatory constraints
   2. No documentation  6. Team cannot evaluate output
   3. Tight coupling    7. Model-context fit
   4. Scattered rules   8. Velocity-of-change
```

*Figure: The kill signals and the traffic light decision rule. Signal 6 weighs more heavily than the others.*

- **Green:** agent-led. One developer dispatches and supervises the six-phase loop.
- **Yellow:** human-led, agent supports. Pair with it instead of dispatching it; the gain is quality more than speed.
- **Red:** fix the codebase first. The agent is net negative until the signals come down.

Apply the light per project, not per company. Start on green, move yellow toward green over a quarter or two, and reform or retire red.

---

### Count by intensity, not presence

**Signals are not binary, and 3 versus 4 is a rule of thumb, not a threshold.**

A partial signal scores half: tests that exist but are partial are half of signal 1, documentation three years stale is half of signal 2. Add the partials and round: four halves is a 2, three halves and a full signal is a 3, five halves is a 3. The full worksheet is Appendix B.4.

---

### What the colors look like

**Each color changes how you use the agent.**

| Project | Count | Color | What to do |
|---|---|---|---|
| Customer-profile service: 70% coverage, README overview, rules in one library | 0 | Green | Agent-led through the loop |
| Legacy payments engine: 20% coverage, stale docs, moderate coupling, audit machinery in place | 2.5, round to 3 | Yellow | Human-led: characterization tests, docs, bounded refactors |
| Custom encryption library, 2017 contractor: undocumented, no cryptographer | 5 | Red | Keep the agent out; fund the expertise or replace it with a vetted standard library |
| Greenfield API service: senior team, clear spec | 0 | Green-plus | AGENTS.md before the first commit, tests from day one |
| Internal tool: 20 developers, written 2019, low regulatory exposure | 1 | Green-leaning | The right first target for a team new to agents: realistic, low stakes |

---

### When it breaks

- **Counting presence instead of intensity** turns yellow into green. "Technically has tests" that cover 10% of the code at low quality is not a pass.
- **Adopting AI on a red codebase because leadership decided to** is the pattern behind failed adoption stories. Fix the signals first.
- **A green codebase starts giving yellow results after a model upgrade.** Suspect instructions written for the previous model before you blame the code: run the migration checklist in Appendix B.9.

---

### Do this Monday

- [ ] Pick one in-flight project and write your gut color on a separate sheet. The whole exercise takes under fifteen minutes.
- [ ] Score the eight signals with the Appendix B.4 worksheet, using the team's answers rather than your impression.
- [ ] Check signal 6 first: if it is present, that work is red whatever the count. Then count and compare with your gut; the gap shows which signals you over- or under-weight.
- [ ] Defend the classification to your tech lead with the scores.
- [ ] Re-score quarterly, after major incidents, and before expanding agent scope.

---

### Go deeper

- **Templates:** [Appendix B.4](#template-b4), the scoring worksheet; [B.9](#template-b9), the model-migration checklist.
- **Deep dive:** [Appendix D, Chapter 8](#deep-dive-chapter-8) - the banking cases behind signals 1 to 5 and 7, the React 18/19 bug behind signal 8, and the study behind the migration check.
- **For managers:** Appendix A, the portfolio view.
- **Sources:** Appendix C.

---

## Chapter 9
## Rolling it out

*By the end you can run agents safely in a real repository and start a rollout the way most successful ones start: with one engineer.*

**TL;DR**

- On a real repo, give agent work its own worktree, hook both the agent and git, and keep a human review floor that no review bot replaces.
- Most adoptions start with one engineer, not three roles: use it yourself, write it up, teach a peer, then recruit the lead and the manager. Month one shows almost no gain; it compounds after.
- Name the two engineer archetypes and plan for the vendor's bad week before either finds you.

---

### Guardrails for a real repo

**The agent is one more author with write access, so give it the boundaries every author gets.**

These repo-level habits sit on top of Chapter 2's five layers and matter most on yellow codebases (Chapter 8). The human review floor that no review bot replaces is Chapter 5's.

---

### Worktrees

**Every agent session gets its own git worktree.**

A worktree is a separate checked-out copy of the repository on its own branch. The agent can experiment, fail and retry there without touching anyone's working copy. Good work goes through normal PR review; bad work is a deleted directory. Without one, the agent contends with your unfinished local work and you spend an hour finding out what changed.

---

### Two kinds of hooks

**Hook the agent, hook the repository, and run the same checks in CI.**

- **The agent hook** (hookify, or your agent's equivalent) reads the proposed action and allows it, prompts you or blocks it. Aim it at areas too dangerous to change without senior review: cryptography, payments, data migrations, anything regulatory. Committed to the repository, five to ten rules is usually enough on a yellow project. AGENTS.md is the polite request; the hook is the firm boundary.
- **The git hook** runs for whoever is committing - you, a teammate or the agent - so one check covers every author. Fast checks (format, lint, typecheck, secret scan) run at commit, tests and the build at push, and a hook manager with versioned config makes sure the hooks are installed on every clone.
- **The escape hatch** is `--no-verify`. Close it with a deny rule in the agent hook.

Local hooks are still fast feedback, not enforcement: skippable, configured in a file the agent can edit, and not guaranteed on every machine. The same checks in CI cannot be skipped from a laptop; with the hook config and the CI workflow behind a deny rule, that is the gate the agent cannot edit.

---

### Keeping it alive

**Rules rot, so someone owns pruning them.**

The mistake journal and its champion are Chapter 6. For process mistakes, keep a failure watchlist: recurring failures, what triggers them and the team's standard response. Review it every month or so and retire what is fixed.

---

### The outer loop

**Run the agent unattended only under a written contract.**

The outer loop re-invokes the agent until a condition holds. It adds attempts, not judgment, so it multiplies whatever your inner loop permits (Chapter 4). Use it on GREEN codebases only (Chapter 8), on many similar, verifiable, reversible units, and read the pull requests in the morning.

Before the first unattended run, write five lines: a stop condition a machine can evaluate; a budget; a gate the agent cannot edit; fresh context each iteration with state in the repository; isolation sized for absence (own worktree, sandbox on, no production credentials, network constrained). Appendix B.6 is the form, with the four signs that mean stop before you relaunch.

---

### How do you roll out AI coding agents on a team? {#how-to-roll-out}

**Start with one engineer who refuses to give up, not with a program.**

The first time I taught the three-role rubric, an engineer in the back row said: "My manager has not heard of agentic AI. My lead does not have time. I am the only person on my team who cares. What do I do?"

The three-role arc would stall for him in month two, when the procurement conversation never happens. The grassroots arc would not, and it is how most successful adoptions in 2025 and 2026 started: one person plays champion, then de facto lead, then manager-advocate, in sequence. I have watched it succeed twice.

- **Month 1: use it on your own work.** Architecture reviews, AGENTS.md drafts and the six-phase loop on code you own, inside existing policy. No announcement; build evidence quietly.
- **Month 2: write it up.** A one-page memo: stories shipped, time saved, honest notes where the agent did not help. Share what you did; do not pitch adoption.
- **Month 3: teach the peer who asks.** Write a bigger case together and invite your tech lead to a walkthrough.
- **Months 4-6: the lead recruits the manager** with evidence and two engineers asking for the same workflow.

By month six it looks like the ideal arc at month three, in twice the time. The trade-off: the grassroots arc is fast to start and fragile, because if the one engineer leaves before peers and management are recruited, the practice dies with them. The three-role arc starts slower and survives a departure. With a manager who knows agents, an engaged lead and budget, run three roles; with only your own hours, run the grassroots arc.

---

### The 90-day arc

**The curve is asymmetric: the first thirty days produce almost no measurable productivity.**

Days 31-60 show visible gains on the green project; days 61-90 compound across the team. Companies that measure at thirty days will be disappointed, so tell stakeholders up front. The full calendar is Appendix B.5.

```
  Days 1-30: Foundation             Days 31-60: Expansion           Days 61-90: Productionization
  -------------------------         -------------------------       -------------------------
  Champion installs                 Lead onboards 2-3 more          Manager folds metrics
  AGENTS.md drafted                 engineers                       into normal velocity
  First green-light project         AGENTS.md hardened              tracking
  Architecture review               Hooks configured                Vendor governance signed
  workflow proven                   Skills written                  Plugin marketplace
                                    Kill signals applied            policy in place
                                    to portfolio
  ====================              ====================            ====================
  Champion                          Lead                            Manager
```

*Figure: The 90-day adoption arc. Each phase has a primary role and a primary artifact set.*

---

### Role commitments

**Each commitment is small enough to fit alongside normal work.**

**The champion** learns the workflow first. They need to be the most willing to invest the first sixty hours, not the most senior.

- [ ] Week 1: install the agent, run the architecture review (Chapter 7) on a familiar codebase and commit the artifact.
- [ ] Week 2: write the first AGENTS.md, under fifty lines, and invite additions by pull request.
- [ ] Weeks 3-4: run the six-phase loop (Chapter 4) on three small features; log friction in the mistake journal.
- [ ] Months 2-3: three medium features with others taking single phases, then hand the role off; by day 90 another engineer runs the workflow as fluently.

**The lead** decides which projects get the agent and keeps the traffic light.

- [ ] Week 1: classify the top five projects against the eight kill signals (Chapter 8) and share the colors.
- [ ] Weeks 2-4: for one project per color, write down what would have to change to move it up.
- [ ] Months 2-3: track cycle time, defect rate and reviewer time (noisy; measure anyway), then present honest results, including where the agent did not deliver.

**The manager** owns budget, procurement and governance sign-off, and shields the team from premature metrics. Their page is Appendix A, with the 20-engineer engagement where agent-touched PRs (41% of the total) ran 28% below the pre-agent cycle-time baseline, defects within noise.

---

### Two archetypes that kill rollouts

**Treat each as a structural problem with a structural fix, not a character flaw.**

**The principled skeptic** is the senior who has seen AI hype cycles before, will not use the agent and reviews agent-led PRs with extra hostility. Either the team works around them and the codebase splits into agent-friendly and agent-hostile territory, or they win the argument and the rollout stalls. Do not try to convert them; give them a boundary: "your modules, your rules, the agent will not touch them; everywhere else the team standard applies." And do not let every agent-led PR queue behind them, or you have granted a veto nobody intended.

**The uncalibrated delegator** skips the careful read because "the agent always does it right". Defects compound, the team blames the agent instead of the missing review step, and eventually the engineer cannot debug what the agent helped build. Every agent-led PR gets the same human review as a human-led one. For the first month, pair them with a senior who reads the output line by line.

---

### The vendor will have a bad week

**Plan for the agent being unavailable.**

I watched a team's velocity halve for a week when their primary model was rate-limited. In June 2026 the largest vendor's newest flagship tier was pulled worldwide days after launch and stayed unavailable for nearly three weeks; teams with fallbacks ran them for real; teams without rediscovered their old setup under deadline. Keep a non-agentic fallback for time-sensitive work, a senior who can still ship a hotfix at three in the morning, and a runbook for "the agent is throttled and the customer is waiting".

---

### When it breaks

| It breaks when | What happens | Fix |
|---|---|---|
| A champion, no lead | The champion does all the agent work alone; the agent is labeled "interesting but limited" | The lead's checklist, above |
| A champion and lead, no manager | Procurement stalls, yellow projects stay yellow; the classification has no buyer | The manager's page, Appendix A |
| A lead and manager, no champion | Committed in theory, stuck in practice | The champion's checklist, above |
| Local hooks treated as enforcement | Skipped, edited or never installed | Run the same checks in CI |

---

### Do this Monday

- [ ] Set up one git worktree on a project you are about to dispatch the agent on, and do the agent's work there.
- [ ] Pick your role - champion, lead or manager - make the first commitment from its checklist this week, and put it on a calendar.
- [ ] Add one agent-hook rule on your most dangerous directory, a deny rule on `--no-verify`, and the same checks in CI.
- [ ] Write the fallback for a vendor outage week: who ships the hotfix without the agent.

---

### Go deeper

- **Templates:** [Appendix B.5](#template-b5), the 90-day calendar with the manager track; [B.6](#template-b6), the outer-loop contract; [B.4](#template-b4), the kill-signal worksheet.
- **Deep dive:** [Appendix D, Chapter 9](#deep-dive-chapter-9) - the outer loop's lineage and vendor timeline, and the two kinds of hooks in full.
- **For managers:** Appendix A.
- **Sources:** Appendix C.

---

# Closing - A way of thinking that survives the tools

The tools I have named will all be different by the time the next edition of this manual is due. What you have learned is not the tools. It is a way of thinking that survives them, in three controls.

**Architecture is the control of capability.** The primitives - context window, tools, permissions / sandbox, skills, plugins, MCP, memory, effort, subagents - plus the harness that organizes them. Most production agents converge on this anatomy because the work determines it, not the vendor, so you can evaluate the next agent by walking down the list.

**Method is the control of workflow.** Formulating work clearly is the foundational shift. The six-phase loop is one implementation; AGENTS.md will exist under other names, but the principle is permanent: discipline as code, not oral tradition.

**Reality is the control of adoption.** Kill signals are properties of codebases and teams, not of tools. The traffic light applies whichever agent you use this quarter, and champion, lead, manager is the arc for any tooling transition.

If you take one practice away, take the architecture review from Chapter 7: the lowest-cost test of whether agentic work will succeed on your codebases. If you take one framework, take the kill signals and the traffic light from Chapter 8; the "no" matters as much as the "yes." If you take one orientation, invest in the way of thinking, not the tool.

Back to those nine seconds: PocketOS lost a production database in the time it takes to read this sentence. Every layer of this methodology existed in 2026 and could have been in place in the months before. None was. That is the gap this manual tries to close: between the methodology that exists and the methodology that is applied.

Understanding the problem becomes more important than writing the code. That was true when programming meant punching holes in cards, when the IDE replaced the text editor, and when AI-assisted coding crossed from autocomplete to drafting; it is true now that agents do the writing. The model names will age out of this edition, and the durable work stays: understand the problem, formulate the work, constrain the execution, verify the result. That sequence is the whole control problem, and it never belonged to the tools: it belongs to you.

The agents write the code. You understand the problem. That is the skill no one is automating.

---

## Acknowledgments

Thank you for reading.

If you have questions, comments, or stories from your own adoption - successes or failures - I would like to hear them. The next edition of this manual, in two or three years, will reflect what teams have learned in the interval. Your experience is the input I want most.

-- Mihai Cvasnievschi

Bucharest, 2026

---

## About the author {#about-the-author}

The shape of a manual depends on the shape of the writer, so here is mine.

I wrote my first programs in BASIC in 1989. My professional career started in 2000 as IT Manager for a manufacturing company; from 2001 I was in software engineering, and through 2023 I delivered .NET for customers across industries, with production code in C, Java, JavaScript, Go and Python along the way. I am an engineer first and a consultant second.

I started on machine learning around 2013. In late 2015 I ported DarkNet and YOLO onto an XR headset and began building AI applications professionally; in 2023 I joined a company building the first neuromorphic SoC. I have used every generation of coding assistant, from Visual Assist to the first Copilot to LLMs for coding since ChatGPT shipped. I have not built my own coding agent; I have used most of the ones that ship now and watched many teams use them.

I am not neutral. I think agentic software delivery is the most consequential shift in our field since high-level languages, and that the way most teams adopt it is doing them more harm than good. This is the third or fourth iteration of these frames; the earlier ones were wrong in interesting ways.

<a id="contact"></a>
*Contact: [info@ship-it-with.ai](mailto:info@ship-it-with.ai) for technical conversations or tailored workshops, in-person or online, shaped to your team's codebase and constraints. Find me on [LinkedIn](https://www.linkedin.com/in/mihaicvasnievschi/).*

---

## Changelog {#changelog}

This page tracks meaningful updates to the manual. Smaller copy-edits and SEO tweaks are not listed; the footer shows the last updated date.

### 2026-10-14 - The short edition

The manual now reads in about an hour. The reading path went from roughly 53,000 words to about 15,000, from a Foreword plus ten chapters to a Prologue plus nine. The frameworks did not change; the repetition, the stacked evidence and the meta-commentary did. Chapters 1 and 2 merged into "What an agent is", with the nine primitives as cards. Governance became "Guardrails in five layers". The six-phase loop split in two: Chapter 4 runs the loop, Chapter 5 owns review and verify. Context hygiene joined AGENTS.md in Chapter 6. Brownfield patterns and adoption merged into "Rolling it out". Every chapter now has the same shape: a TL;DR, one story, one table or figure, When it breaks, Do this Monday, Go deeper. The studies, benchmarks and dated vendor detail moved to a new Appendix D, Deep dives, organized by chapter; Appendix A became "For managers" (cost, the manager role, the 20-engineer case); Appendix B gained the plugin-vetting checklist and the exercises; Appendix C is unchanged apart from pointing at the new locations. Old chapter URLs redirect to their new homes. The September 2026 edition, unabridged, stays available at [/full/](/full/).

### 2026-09-11 - September evidence pass: Effort primitive, review and verify controls, the AGENTS.md correction, B.9

The manual read against the September 2026 evidence: the Claude 5 and GPT-5.6 and GPT-6 generation guides, and a run of measured studies on context files, multi-agent scaling, reward hacking, critique uptake, and context management. The structure held; the updates land where new evidence changes a claim, sharpens one, or fills a gap. Chapter 1 gains Effort as the ninth primitive - the reasoning dial and retained reasoning - because it now passes the convergence test and has become the largest cost and quality lever; the tools section gains the tool-count cliff, deferred loading, programmatic tool calling, and strict schemas; the context-window section discounts advertised windows. Chapter 2's inspection walk grows to nine points. Chapter 5: a when-to-split gate for Execute (decomposable work only, one writer per file, fork the workers and isolate the reviewers), vendor autonomy and scope blocks, reviewer two scoped to correctness and blind to reviewer one, repair rate over reviewer accuracy with capped rounds, the SpecBench and Cursor numbers behind "evidence, not proof" with four verify controls (held-out tests, sealed history and egress, a config-edit hook, explain before fix), and measured context hygiene (masking over summarization, append-only history, a keep-list for the compactor). Chapter 6 carries the one correction with direct evidence against the text: the repository map moves out of AGENTS.md into docs/, per the ETH context-file study; the mistake journal gains maintenance mechanics and evidence pointers; the two-hundred-line cap gains the eighty-rule cliff and the 80% system-prompt cut; a precedence line joins the file. Chapter 7 cites the retrieval evidence behind reading code rather than indexing it. Chapter 8 names instructions written for the previous model as a soft signal. Chapter 9's stop condition names /goal and Codex Goals. Appendix A gains the structural cost levers; Appendix B gains B.9, the model-migration checklist (the template count is now nine), with B.2, B.3 and B.7 updated; Appendix C gains a harness and model-migration group of twenty-seven entries. Dated-claims note bumped to September 2026.

### 2026-07-27 - Finding your unknowns (Chapter 4 + Chapter 5 + B.8)

Chapter 4's formulation-bottleneck thesis gains its strongest external receipt yet: Anthropic's own July 2026 field guide to working with Fable 5, whose author describes the frontier model as "bottlenecked by my ability to clarify its unknowns" - the vendor's engineers now describing the frontier the way Chapter 4 does. The guide's four-quadrant unknowns frame is mapped onto the manual's machinery (the team instruction file drains the unknown knowns, the research note surfaces the known unknowns), and Chapter 5 gains three techniques for the quadrant no checklist reaches. In Research: a blind spot pass before research proper when the task sits outside your domain, paired with stating your experience level so the agent's assumptions get spelled out where you can veto them. In Execute: an implementation-notes file recording every deviation from the plan at the moment it happens - the spec reviewer's confession list, and the antidote to orchestrator-summary drift. Closing the agent-diff read: a pre-approval quiz - if you cannot answer what happens at the edges, that was rubber-stamping, not review, and pattern four's decay just became measurable. The B.8 one-pager gains the quiz block; new Appendix C entry for the field guide.

### 2026-07-17 - July currency and corrections pass

A deep fact-check of every dated claim against the July 2026 public record, with adversarial verification on each finding. Corrections: the April 23 post-mortem story is re-sourced - Anthropic's acknowledged regressions are March 4 (effort), March 26 (caching), and April 16 (verbosity cap), while the February adaptive-thinking attribution and the 6,852-session audit belong to AMD's Stella Laurenzo, published April 6, ahead of the post-mortem; the Memory primitive's agent-written half is upgraded from early-mover signal to full convergence (GitHub Copilot Memory preceded Auto Memory; Codex CLI followed in April); Dreaming is corrected to a platform-level feature, not a shipped CLI command; Codex parallel subagents corrected from eight to the documented six; Cursor's subagent system re-dated to 2.4; opencode's repository updated to anomalyco/opencode; ralph-wiggum's adoption re-dated to November 2025; smaller date fixes (Adversa patch, /loop). Currency: context windows (a million tokens is now mid-range), METR's own February 2026 follow-up caution, telemetry converging as OpenTelemetry, the Gemini CLI to Antigravity CLI transition. Additions: Railway's post-PocketOS 48-hour soft-delete and scoped agent access (Chapter 3), the June 2026 flagship-tier suspension as the vendor-bad-week example (Chapter 10), the DuneSlide sandbox-escape CVEs as the honest caveat on layer two (Chapter 3), the DNS-TXT split-payload injection vector, and the `sandbox.credentials` mitigation. Dated-claims note bumped to July 2026.

### 2026-07-06 - SVG diagrams and localized figure bodies

Three figures graduate from card layouts to theme-aware SVG: the six-phase loop now draws its real topology (six nodes, arrows, and the two failure routes back to Plan), the five governance layers render as a defense-in-depth stack, and the 90-day arc becomes a timeline with role chips. All five figures now render localized bodies in the Romanian edition (previously only captions were translated), and the arc figure's stale CLAUDE.md labels were corrected to AGENTS.md to match the text. Presentation only; the figures' content is unchanged.

### 2026-07-05 - How to review an agent diff (Chapter 5 + Appendix B.8)

Chapter 5's review phase gains its human half, inserted after the two agent reviewers and before verify - the read only a human can do, which the book had invoked as the human floor without ever teaching. It starts from why an agent diff fails in kind, not in degree: a human diff fails at execution and you hunt the mistake line by line, while an agent diff compiles, passes lint, and reads idiomatic, failing instead at intent and context. So the read order inverts into five steps - the diff-stat against the plan before any code, the tests read for what they assert, the boundaries the team has rules about, a grep of every new name the diff introduces, and only then line by line, where the minutes go to business correctness and architectural fit. The calibration line anchors it: fluency is not correctness, and an agent bug looks like the code a good engineer would write for a slightly different task. New Appendix B.8 agent-diff read order one-pager (the template count is now eight). Chapter 9's pattern four gains a closing back-pointer naming this read order as the human floor made concrete.

### 2026-07-05 - Context hygiene (Chapter 5 + Appendix B.7)

Chapter 5 gains a Context hygiene section, inserted after the inner/outer loop vocabulary paragraph, that teaches the daily craft the book had named but never taught - the window is the agent's working memory, and everything loaded into it competes with reasoning. It names the four signs of contamination (the agent re-answers a settled question, cites a stale version of a file it edited, forgets a constraint it honored, or degrades in edit quality late in a long session), the session-boundary discipline of one unit of work per session with durable state read back from the repository, and compaction as a handoff rather than a continuation, where anything not written to a file by then is gone. New Appendix B.7 context-hygiene one-pager (the template count is now seven). Chapter 1's context-window section gains a one-sentence forward pointer to the new section.

### 2026-07-05 - Appendix A worked example

Appendix A gains a worked pass of its own rubric, closing the one gap in a book built on worked examples: the cost section had no numbers. The new subsection runs the Chapter 10 manager sidebar's 20-engineer financial-services engagement through the appendix - 13 Team seats plus 7 Pro seats, the four-category TCO list, and the bounding heuristic - using the engagement's published operational numbers (41% of merged PRs agent-touched, cycle time 28% below baseline, defects flat) as the value anchor. The cost-side rates are labeled as illustrative round numbers, not quotes, consistent with the appendix's stance that specific prices go stale quarterly. The honest headline lands in a small table: the sticker is the smallest line, and the human-time categories dwarf it. The close holds Chapter 10's boundary: the manager defends the operational number, not a projected ROI.

### 2026-07-05 - Two kinds of hooks (Chapter 9 pattern three)

Chapter 9 pattern three expands from hookify rules into two kinds of hooks: the agent's pre-tool-use hook (hookify) and git's pre-commit/pre-push hook. The new material frames the git gate on the agentic spine - the agent is just another author with write access, so a deterministic commit/push gate applies to it for free, and the `--no-verify` escape hatch is closed by a hookify deny rule. It draws the honest line too: local hooks are fast feedback, while the same checks in CI are the gate you cannot skip from your laptop, which is pattern eight's gate the agent cannot edit. Recap, closing, and the artifact box updated to match; the pattern count stays eight.

### 2026-06-11 - Scripted subagent orchestration (`/workflows`)

Chapter 1's subagents section gains a paragraph on programmatic orchestration: Claude Code's `/workflows`, which has the agent write a deterministic script that dispatches subagents across phases, parallel/pipeline fan-out, and schema-validated handoffs, with a verification gate. Framed on-thesis - not a new primitive but harness convenience over the subagent primitive, where the determinism is the only real difference from model-driven parallel dispatch (e.g. a Superpowers-style plugin). Dated to mid-2026.

### 2026-06-10 - The outer loop (pattern eight)

Chapter 9 grows an eighth pattern covering the outer-loop trend - re-invoking the agent on an interval, a schedule, or a queue until a condition holds. The pattern traces the lineage (the 2023 self-grading loops; Ralph Wiggum in mid-2025; the late-2025 vendor wave of background and scheduled agents; the loop as a first-class surface by spring 2026) and installs the controls: a five-line loop contract, the loop-eligibility test, four loop kill signals, and the morning review floor. Chapter 5 gains the inner/outer loop vocabulary paragraph. New Appendix B.6 outer-loop contract one-pager (the template count is now six). Five new Appendix C entries under a new outer-loop and autonomy sources group. Dated-claims note bumped to June 2026.

### 2026-05-27 - Permissions / Sandbox primitive

Permissions / Sandbox promoted to a named primitive - the third slot in the inventory, after Context window and Tools. Two halves like Memory: the agent-level decision layer (Allow / Ask / Deny + auto mode) and OS-level enforcement (Seatbelt / bubblewrap / restricted tokens / WSL2). The vocabulary note in Chapter 1 was rewritten to name the convergence test that promoted this primitive while leaving telemetry as a control layer. Chapter 3 gains a framing paragraph binding three of its five layers (permissions, hooks, sandbox) to the new primitive's configuration surfaces; the five-layer defense-in-depth narrative is preserved unchanged. Inspection-points count in Chapter 2 dropped from nine to eight (the two halves of P/S collapsed to one). Diagram updated to 8 cells. Three new Appendix C entries source the Claude Code / Codex / opencode implementations.

### 2026-05-27 - Changelog + last-updated footer

Added this page and a "Last updated &lt;date&gt;" line in the footer, plus a Changelog link in the contact row. The intent: returning readers can see what moved since their last visit without diffing chapters.

### 2026-05-27 - Memory primitive + open-set framing

Memory promoted to a named primitive across the book; Chapter 1 retitled "The primitives" and the structural argument rewritten as "named primitives + the recursive primitive (subagents)". Dropped the closed "six primitives" count throughout; the list is now framed as open-set. New Memory section covers two halves - manually defined memory (AGENTS.md/CLAUDE.md, agent-agnostic) and the auto-memory system (Auto Memory, Auto Dream - currently Claude-Code-led). Diagram updated. Chapter 6 gains a one-paragraph framing intro anchoring AGENTS.md as the team-shareable memory layer. Three new Appendix C entries source the Memory claims.

### 2026-05-27 - SEO pass: per-chapter URLs

Every chapter and appendix now has its own URL (20 pages total). Old `/#chapter-N` bookmarks redirect. Each page got a unique title, meta description, canonical URL, prev/next nav, and `TechArticle` + `BreadcrumbList` structured data. Hero gained a three-button CTA row. Schema upgraded from `Article` to `Book` + `Organization` + `FAQPage`. Cross-section anchor rewriting, AGENTS.md de-linking, `/read/` mode for the single-page reading experience. Built-in 404 page, `llms.txt` for AI answer engines, `cover.webp`.

### 2026-05-26 - Feedback-pass polish

External-reviewer pass: TOC chapter-to-part mismatch fixed, figure numbering dropped (web-manual style), new Source-note and Artifact callout components with light + dark variants, foreword bio trimmed to four sentences and full version moved to a new About-the-author section, hero gained a control-thesis dek, AGENTS.md links collapsed to at most one per chapter, per-section `¶` copy-link anchors, callout stack tightening.

### 2026-05-26 - First public version

Manual published at ship-it-with.ai. Ten chapters across three parts (Architecture, Method, Reality), three appendices, plus foreword, prologue, closing.

---

## Appendix A. For managers

*For the engineering manager, director or CTO who owns budget, hiring and procurement - and for the champion who has to hand them a case. Read Chapters 2, 8 and 9 first (guardrails, readiness, rollout). This appendix holds the rest: your role, the portfolio call, one worked team, and the money. It is built to be forwarded on its own.*

---

### Your job in the 90 days

**The manager does not run the agent. The manager defends three boundaries.**

The manager phase is days 61-90, after the champion has stood up the practice and the lead has hardened it (Chapter 9 has the arc). It has three centers of gravity:

- **Procurement.** Close the licensing decision so the team is not on individual seats forever.
- **Governance.** Sign off on the security posture the champion drafts.
- **Reporting.** Translate operational results into terms leadership will fund.

None of it needs you to write code. All of it needs you to hold lines: operational data versus ROI promises, tooling matched to usage versus forced uniformity, protecting the team from premature metrics versus demanding evidence that the work pays off.

You also own the calls nobody else can make: hiring the cryptographer behind a signal-six problem, funding a quarter to move a yellow project to green, buying extra tooling or services.

**What you do not do:**

- Chase per-engineer productivity metrics in month two.
- Commit to a three-year ROI before the dashboard has a quarter of data.
- Authorize vendor-versus-vendor benchmarks before the team has shipped enough to define what it is benchmarking.

Those questions destroy adoption when answered too early. In months one to three, shield the team from them, and tell stakeholders up front that the first thirty days show almost no measurable productivity. When the operational number is solid, defend it; leave the revenue argument to whoever owns revenue. By day 90 your role shifts from standing up the practice to tracking the metrics each quarter.

Without an engaged manager the cost shows up elsewhere: procurement sits two months waiting on legal, the documentation budget is never allocated, yellow projects stay yellow. The lead's classification was correct. It had no buyer.

---

### Which codebases now, later, never

**Apply the traffic light per project, never per company.** The question is not "is this company ready for AI." It is "which of our codebases is ready today, and what would it take to move the others." Chapter 8 holds the eight kill signals and the scoring. The part you act on is the sort.

| Color | Signals | Mode | Your call |
|---|---|---|---|
| Green | 0-1 | Agent-led | **Now.** Start here to build the team's experience and confidence. |
| Yellow | 2-3 | Human-led, agent support | **Later.** Fund the structural fixes that move it toward green over a quarter or two. |
| Red | 4+ | Fix the codebase first | **Never, as it stands.** Reform or retire over a longer horizon; the agent stays out until the signals close. |

Most companies hold a mix, and the mix is the plan. When leadership has decided to "adopt AI," the temptation is to put the agent on a red codebase anyway. Resist: that temptation is what produces the failed adoption stories that taint the field.

Two rules to know before you read a scorecard:

- **Signal six is weighted more heavily than the others.** It is counted with them and also overrides the count: a codebase that scores zero on signals one through five but yes on signal six is still red for the relevant work. The fix is structural: build the capability, partner with someone who has it, or restrict the agent away from those areas.
- **Count by intensity, not presence.** "Tests exist but are partial" is half a signal. A codebase that technically has tests that cover 10% of the code at low quality is not green.

Ask your lead for a one-row-per-project scorecard on the top five active projects: signals scored, color, recommended mode (agent-led, human-led, fix first). It takes about two hours. For a yellow project, ask for the two or three structural fixes that would make it green. For a red one, ask whether the answer is investment, replacement or retirement. Sometimes the question is the strategy, not the codebase: a vendor-customized fork with severe upstream coupling asks whether the custom layer should exist at all.

---

### One team, week by week

**Twenty engineers in a regulated financial-services firm.** The manager owns the engineering function and reports to a supportive but cost-conscious CTO. The board wants a one-page update at the end of the third quarter on the AI investment. The champion ran days 1-30 and the lead hardened the practice in days 31-60; the manager picks up from day 61.

| Week | What lands | What the manager does |
|---|---|---|
| 1 (days 61-67) | A dashboard of three metrics: share of merged PRs touching agent code; cycle time and defect rate on that set, each compared to the prior quarter. | Verifies the metrics are real. Does not try to grow them. |
| 2 (days 68-74) | Procurement asks seat versus enterprise. The team is on individual Pro seats. | Chooses Team tier for 13 of 20 engineers and Pro seats for the 7 who rarely use the agent. Defends it: the goal is bounded spend that matches usage, not uniform tooling. |
| 3 (days 75-81) | The security committee has read about the configuration-file injection class Check Point Research disclosed in early 2026 (Appendix C) and wants a written governance posture. | Edits and signs a one-page document naming four control points: hooks, sandbox, secrets vault, telemetry (Chapter 2 has the layers). The champion writes it. |
| 4 (days 82-88) | The board ask. | Sends two sentences and one number. Promises no revenue figure. |

The numbers behind week 1: 41% of merged PRs agent-touched in month two, cycle time on them 28% below the pre-agent baseline, defect rate within noise of it.

The board update, in full: *"We have twenty engineers on agent-assisted delivery. Cycle time on agent-touched PRs is 28% lower than baseline at no measurable change in defect rate. We are continuing to scope expansion through the next quarter."* The manager defends the operational number and leaves the revenue argument to the CTO.

Day 90: back to ongoing operations. The dashboard stays; the champion and lead keep their roles.

---

### How much does agentic coding cost? {#how-much-does-it-cost}

**The sticker is the smallest line, and the one everybody asks about first.** Prices change every quarter; the rubric does not. Plug your own numbers into it.

Three pricing models dominate:

- **Per-seat.** A flat monthly fee per engineer. Predictable; cheap for occasional users, expensive for power users who run the agent all day.
- **Per-token.** You pay for what the agent reads and writes. Fair to occasional users; punishing for the engineer running three parallel sessions for ten hours.
- **Enterprise.** A negotiated annual commitment bundling seats, a token allowance and the compliance surface (Zero Data Retention, audit log access, dedicated capacity, SSO, signed BAAs). It amortizes both extremes and adds what regulated industries require.

**The bounding heuristic.** Per-engineer cost is bounded by what the team would otherwise spend on similar tooling (IDE licenses, code-intelligence platforms, AI-coding subscriptions) plus a fraction of a senior engineer's hourly time saved per week. If the all-in monthly cost exceeds that envelope by a wide margin, the math is unlikely to work with any vendor. If it falls comfortably inside, it is unlikely to fail. Break-even lands quickly when the agent saves even a few hours a month per engineer.

**What the quote leaves out.** Four lines dominate the real total:

| Line | What it covers | The 20-engineer team (illustrative) |
|---|---|---|
| Seats (the sticker) | The vendor quote | ~$530/mo, ~$6,400/yr, recurring |
| Integration | Custom skills, hooks, MCP servers for internal systems | A few engineer-weeks, one-time |
| Skill-authoring | Maintaining AGENTS.md, updating skills as the codebase evolves | A few hours per engineer per month, plus the champion's part-time quarter |
| Review | Reviewing agent output: less per change than hand-written code in most cases, never zero | Concentrated on senior reviewers, ongoing |
| Governance | CISO security review, Zero Data Retention addendum, procurement cycle, audit logging, vendor-risk monitoring | A week to a quarter, front-loaded in a regulated firm, one-time |

---

### The structural levers {#cost-levers}

**Prices go stale; the levers that move the token line do not.** On per-token plans they are where the second-year savings live.

- **Effort level.** The Chapter 1 primitive and the largest cost dial you own. Set it per phase, sweep it per model, and never leave the default on for the whole loop.
- **Cache-first prompt layout.** Stable content first (system prompt, AGENTS.md, loaded skills), per-turn content last, so the prefix caches. Across 500 sessions on three providers that ordering alone cut cost by 41% to 80%.
- **Deferred tool loading.** One audit of a default Claude Code session counted about 24k tokens of tool definitions and schemas before the user's first word. Defer the schemas and pay only when a tool is used.
- **Masking over summarization.** Blank old tool results instead of summarizing the history. JetBrains measured it over 50% cheaper, with a solve rate that matched or beat summarization.
- **Tier routing.** Route by task, not by team: a cheaper model does the work, a stronger one stays on call. In Anthropic's advisor pattern (April 2026), Sonnet with an Opus advisor beat Sonnet alone at 11.9% lower cost per task; Haiku with the advisor was 85% cheaper than Sonnet alone but trailed it by 29% in score. Right for the mechanical tiers of the loop, wrong for research.

---

### A worked example {#a-worked-example}

**Run the 20-engineer team through the rubric.** The figures are round numbers for the arithmetic, not quotes.

Sticker first. 13 Team seats at an illustrative $30 plus 7 Pro seats at $20 is $530 a month, call it $6,400 a year. Write it down: it is the smallest number on the page.

Then the human lines. A few engineer-weeks of integration, at any realistic loaded cost, clears the first year's sticker on its own, once. Skill-authoring across 20 engineers, plus the champion's quarter, recurs and can run larger than the seats themselves. Review lands on your most expensive hours, the senior reviewers. Governance in a regulated shop is a week to a quarter of security, procurement and audit-logging work before a single seat is billed.

The value side runs the bounding heuristic in reverse. At an illustrative $100 loaded per hour, a $30 seat is covered when the agent saves that engineer about twenty minutes in the month; a few saved hours is nowhere near close. But that back-of-envelope is not what justified the spend. The operational number did: 41% of merged PRs agent-touched, cycle time 28% below baseline, defects flat. Measured hours out, not projected dollars.

**The discipline:** the four hidden lines dominate, and the human ones dwarf the seat math. Defend the operational number to the board, not a projected ROI the dashboard cannot yet support. Walk into procurement with your own numbers in this structure. Pricing changes; this arithmetic does not.

---

**Related:** [Appendix B.4](#template-b4) (kill-signal scoring worksheet), [Appendix B.5](#template-b5) (90-day calendar), Appendix C (sources).

---

## Appendix B. Templates

Eleven copy-paste templates and exercises. All are starting points; customize for your team.

### B.1 Architecture review prompt {#template-b1}

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

### B.2 AGENTS.md skeleton {#template-b2}

Works as [AGENTS.md](https://agents.md/) or CLAUDE.md. Near a hundred lines, never past two hundred. The precedence line goes first: it removes a class of stalls over which instruction to obey.

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

### B.3 Six-phase loop checklist (one-pager) {#template-b3}

```
RESEARCH
  Note of 2-4 pages: files, conventions, open questions.
PLAN
  File-level tasks of 2-5 minutes; tests named; "done" defined for the whole change.
  Human gate: push back on anything vague, too large or wrongly ordered.
EXECUTE
  Split only for independent files or modules; one writer per file.
  Fork the workers; isolate the reviewers (fresh context).
  Autonomy block: finish the task before ending the turn; do not stop at acknowledging
  capability; no confirmation on reversible actions; no tests for reversible,
  low-impact changes.
  Scope block: only the files the plan names; stop and report on anything else.
  Each subagent keeps the implementation-notes file.
REVIEW (two reviewers in sequence; cap at three or four rounds)
  Spec compliance, then correctness; reviewer two never sees reviewer one's verdicts.
  Executor accepts or rebuts every finding; track repair rate, not reviewer accuracy.
VERIFY
  New tests run; a held-out set the agent never sees; git history sealed, network off.
  Hook blocks lint and test-config edits and commit --no-verify.
  Failing test: agent explains why before it may fix. UI: Playwright, accessibility tree.
  No "done" without test evidence.
SHIP
  Structured commit and PR; reviewers per CODEOWNERS; normal team review.
```

### B.4 Kill signal scoring worksheet {#template-b4}

```
Score each signal 0 (absent), 0.5 (partial, between the anchors) or 1 (present).

1 No tests
  0    > 70% coverage AND run on every commit
  0.5  30-70% coverage, or not routinely run
  1    < 30% coverage or no suite
2 No documentation
  0    current architecture doc, decision records
  1    no overview; only the author knows
3 Tight coupling
  0    clear boundaries; modules change in isolation
  0.5  some coupling; new hires struggle
  1    hairball; one edit breaks three files
4 Scattered business rules
  0    one source of truth per rule
  1    same rule in 3+ places, inconsistent
5 Regulatory constraints
  0    standard controls; audit machinery copes
  0.5  regulated, but the workflow is in place
  1    heavy controls, no integrated workflow
6 Team cannot evaluate output
  0    senior expertise for every domain
  0.5  expertise exists but is fragile
  1    cannot evaluate output in some domain
7 Model-context fit
  0    popular language/framework, public footprint
  1    proprietary DSL, internal framework
8 Velocity of change
  0    stable framework and dependencies
  1    major migration mid-flight

Sum, round to the nearest integer.
  0-1 GREEN (agent-led)  2-3 YELLOW (human-led, agent supports)  4+ RED (fix the codebase first)
Signal 6 weighs extra: a 1 is RED for the affected work, whatever the total.
```

### B.5 90-day adoption calendar (one-pager) {#template-b5}

```
CHAMPION
  Week 1      install; architecture review (B.1) on a familiar codebase; commit it
  Week 2      first AGENTS.md (B.2), under 50 lines
  Weeks 3-4   six-phase loop (B.3) on three small features
  Month 2     three medium features; pull others into single phases
  Month 3     hand the role to a successor; AGENTS.md is team-owned
LEAD
  Week 1      classify the top 5 projects against the 8 kill signals (B.4)
  Weeks 2-4   per color, write what would have to change to move one project
  Month 2     track cycle time, defect rate, reviewer time
  Month 3     present honest results
MANAGER
  Months 1-2  protect the team: no per-engineer productivity metrics, ROI projections or vendor benchmarks yet
  Days 61-67  take the handoff; verify the dashboard metrics are real
  Days 68-74  close the seat-vs-enterprise decision (Appendix A)
  Days 75-81  governance one-pager; champion drafts, manager signs
  Days 82-90  two sentences and one number to leadership; quarterly cadence
```

Grassroots track for teams without all three roles: Chapter 9.

### B.6 Outer-loop contract (one-pager) {#template-b6}

```
Before any unattended run, fill every line. A blank line means the loop is not ready.

WORK
  Queue: ______ (in the repo; one small, similar, reversible unit per item)
  Eligibility: GREEN codebase (B.4 score 0-1) / every unit machine-verifiable / every unit revertible
STOP CONDITION (machine-evaluable; the loop halts itself)
  Done when: ______ (queue empty / suite green / N units ready for review)
  Budget: max ______ tokens or $______ or ______ iterations or ______ hours - whichever hits first
  Failure rule: same unit fails twice -> skip it and flag; three skipped units -> halt
EACH ITERATION
  Fresh context; state read from queue + journal in the repo
  One unit per iteration; finish it or journal why not - nothing half-applied
  Gate: ______ (tests / lint / typecheck / build) runs outside the agent's reach (CI or hook)
  Deny rules: agent cannot edit test config, lint config, CI workflow, hook rules, or the
  journal's done-markers
ISOLATION
  Own worktree and branch, never the default branch
  Sandbox on; no production credentials; network off or allowlisted
MORNING REVIEW (the human floor)
  Each PR reviewed for business correctness and architectural fit
  Kill check before relaunch: oscillating diffs? budget spent but queue not shorter?
  same failure a third time? gate touched? Any yes -> do not relaunch. Read the journal,
  fix the cause first.
```

### B.7 Context hygiene one-pager {#template-b7}

```
LOAD
  Task-relevant context only. Pointers over payloads: name the files, do not
  paste them.
SESSION
  One unit of work per session. Durable state lives in committed files.
CONTAMINATED WHEN the agent
  re-answers a settled question; cites a stale version of a file it edited;
  forgets a constraint it honored; degrades late in a long session.
THEN
  Do not argue with the session. Commit the durable state, end it, start fresh.
COMPACTION (a handoff, not a continuation)
  Prefer masking old tool outputs to summarizing. History is append-only on
  Fable 5.1: restart, do not edit. Give the compactor a keep-list: plan, open
  questions, deviations, commands that worked. The rest is gone.
```

### B.8 Agent-diff read order (one-pager) {#template-b8}

```
1 BEFORE THE CODE
  Diff-stat against the plan. Files the plan never named are the first flag.
2 TESTS FIRST
  Read what they assert, not whether they pass. A test written from the code
  agrees with the code; the assertion must come from the intent.
3 BOUNDARIES
  Check the team's written rules (AGENTS.md forbidden patterns, layer
  conventions). A crossing looks clean in fluent style.
4 NEW NAMES
  Grep every API, function or config key you do not recognize. No hits: the
  name may not exist.
5 LINE BY LINE
  Only now, for business correctness and architectural fit. The review agents
  already swept the mechanical layer.
THE QUIZ
  Before approving, have the agent quiz you on edges, ownership and failure
  modes. Cannot answer: you were rubber-stamping.
```

### B.9 Model-migration checklist (one-pager) {#template-b9}

Run it after every model swap, and when a green codebase turns yellow after an upgrade: instructions written for the previous model do not retire themselves. Not a ninth kill signal.

```
BEFORE THE SWAP
  Baseline five representative tasks on the current model: cost, outcome, effort
  level. Read the vendor's guide - every generation retires part of the harness.
EFFORT
  Sweep effort per task type; pick per phase, not per session. Effort names do
  not transfer between models.
PROMPTS AND INSTRUCTION FILES
  Strip emphatic capitals and "verify your work" lines written for a model that
  needed them. Remove parameters the new model rejects: temperature, prefill,
  forced tool choice.
  Never ask for the model's reasoning in the reply - a refusal category on Fable 5.
  Audit skills for over-prescription; rewrite the autonomy and scope blocks (B.3).
  Keep the precedence line (B.2); re-read AGENTS.md for rules the model no longer breaks.
TOOLS AND HISTORY
  Re-test custom tool schemas with strict decoding on; re-count visible tools.
  Keep history append-only; re-check compaction - the cost trade moved with
  cached-input pricing.
AFTER THE SWAP
  Re-run the baseline; compare cost and outcome per phase. Still yellow: now
  check the kill signals (Chapter 8).
```

### B.10 Plugin vetting checklist {#template-b10}

The marketplace is a supply-chain surface like npm. Vet each plugin as you would a dependency.

```
MAINTAINER
  Active in the last 90 days? More than one maintainer? A real track record?
PERMISSIONS SURFACE
  Which tools, hooks, file paths and network calls does it add? Broad requests
  need a reason.
CODE REVIEW
  Read the source on first install; it should take twenty minutes. Too large:
  find a smaller plugin or invest a deeper review.
UPDATE DISCIPLINE
  Pin the version; no auto-update. Read the diff, run the tests, ship the bump
  as a reviewed change.
BLAST RADIUS
  Inside the sandbox is bounded; a hook on the developer's machine outside it is
  unbounded. Prefer bounded; else raise the bar on everything above.
```

### B.11 Exercises {#template-b11}

Two exercises that go beyond a chapter's Do this Monday list. For Chapters 2, 7 and 8, the Monday list is the exercise: the five-layer scorecard, the first architecture review, the gut-color check.

**Chapter 1 - What an agent is**

1. Clone two open-source coding agents, open your own agent in each and ask: "Walk this codebase and name the primitives - context window, tools, permissions / sandbox, skills, plugins, MCP, memory, effort, subagents. For each, name the file or module that implements it and rate it basic, intermediate, or advanced."
2. Save both answers in a two-column table. The primitives match; the differences are governance choices.

**Chapter 6 - AGENTS.md and context**

1. Pick a repository whose instruction file is empty, stale, or left by someone who moved on.
2. Ask your agent: "Walk this codebase for twenty minutes and tell me what a new teammate would need to know before contributing. Cover conventions, test discipline, build and deploy commands, and anything documented partly or wrong."
3. Draft the file from B.2 and the answer: concrete to this repo, a pointer to docs/architecture.md instead of a layout, no generic best practice.
4. Commit it. In a fresh session ask: "What would you change about this codebase if I asked you to add a Priority field to the main entity?" Compare with the answer before the file existed.
5. Give it to a teammate new to the repo; their confusion is your next edit.

---

## Appendix C. Sources and Further Reading

This appendix exists because every claim in this manual deserves a verifiable source if you choose to chase it down. I have organized the entries by claim, not by source, so you can map back from a passage in the body to the evidence behind it. Entries are grouped by category (studies, named incidents, vulnerabilities with patch versions, tool documentation, marketplaces, memory primitive sources, permissions / sandbox primitive sources, outer-loop and autonomy sources, harness and model-migration sources) and each entry follows the same shape: the claim, the source, where in the manual it is used, and any caveat worth knowing.

### Studies and research

**Claim:** Experienced open-source developers using AI assistance on familiar repositories were 19% slower than the same developers without it, while predicting beforehand they would be 24% faster - a 43-point gap between expected speedup and measured slowdown that persisted in their self-reports even after the data contradicted it.
**Source:** Becker et al., METR, "Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity," July 10, 2025. arXiv: [arxiv.org/abs/2507.09089](https://arxiv.org/abs/2507.09089). Writeup: [metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/). Follow-up design change: [metr.org/blog/2026-02-24-uplift-update/](https://metr.org/blog/2026-02-24-uplift-update/).
**Where used:** Appendix D, Chapter 3 (the METR randomized controlled trial).
**Caveat:** Tested raw AI assistance (Cursor + Claude) without a formulation-discipline variable. My interpretation that workflow discipline is the missing variable is mine, not the study's. METR's late-2025 follow-up suffered severe selection bias (developers increasingly refused randomization away from AI) and produced only weak estimates; METR announced a redesigned experiment on February 24, 2026 and cautions against extrapolating the 19% figure to current tools.

---

### Named incidents

**Claim:** On April 24, 2026, PocketOS lost its production database in nine seconds when a Cursor agent powered by Claude Opus 4.6 invoked Railway's Volume Delete via a found API token during a credentials-mismatch recovery attempt. Backups stored on the same volume were destroyed with the primary data.
**Source:** Reported by DevOps.com ("When AI Goes Really, Really Wrong"), Business Insider (Jer Crane statement), and others. Anthropic's Claude Opus 4.6 system card (February 2026) describes the model that powered the agent.
**Where used:** Prologue (Nine seconds) and Chapter 2 (Guardrails in five layers); Appendix D, Chapter 2 (PocketOS: where the accounts disagree, and what the platforms changed).
**Caveat:** Recovery timeline differs across public accounts - Railway's restore was reportedly ~30 minutes after Crane contacted them, while other accounts describe ~30 hours or two days for full operational restoration. I use the incident for the governance pattern, not as a precise forensic reconstruction. Aftermath: on April 29, 2026 Railway announced that all volume and resource deletes - previously instant when invoked via the API - now soft-delete with a 48-hour recovery window, alongside workspace guardrails and scoped agent access ([blog.railway.com/p/your-ai-wants-to-nuke-your-database](https://blog.railway.com/p/your-ai-wants-to-nuke-your-database)).

---

**Claim:** In late February 2026, Alexey Grigorev at DataTalks.Club lost two and a half years of course infrastructure when Claude Code worked against a stale Terraform state file and ran `terraform destroy` against what it read as orphaned resources.
**Source:** Public account by Alexey Grigorev (DataTalks.Club), late February 2026.
**Where used:** Chapter 2 (Guardrails in five layers); Appendix D, Chapter 2 (PocketOS: where the accounts disagree, and what the platforms changed).
**Caveat:** Data loss was partial; AWS restored roughly 1.94M rows from a snapshot within about a day. The incident is documented publicly but with less coverage than PocketOS. Grigorev's follow-up documents the hardening adopted afterward: delete protection in both Terraform and AWS, state moved to S3, manual review of every destructive plan, and an upgraded AWS support tier.

---

**Claim:** Anthropic's technical post-mortem of April 23, 2026 ("An update on recent Claude Code quality reports") acknowledged three regressions: default reasoning effort dropped from high to medium on March 4 (reverted April 7), a caching bug from March 26 that cleared reasoning history every turn instead of once per idle hour (fixed April 10, v2.1.101), and a system-prompt verbosity cap from April 16 that produced a measured ~3% quality drop (reverted April 20). Separately and earlier, AMD Senior Director Stella Laurenzo published an independent audit (April 6, filed as GitHub issue anthropics/claude-code#42796) of 6,852 Claude Code sessions and 234,760 tool calls, showing a shift from research-first to edit-first behavior as thinking redaction rolled from 1.5% to 100% of turns and attributing the degradation in part to the February adaptive-thinking-by-default rollout.
**Source:** Anthropic engineering post-mortem, April 23, 2026: [anthropic.com/engineering/april-23-postmortem](https://www.anthropic.com/engineering/april-23-postmortem). Laurenzo audit: GitHub issue anthropics/claude-code#42796; coverage in The Register, April 6, 2026.
**Where used:** Appendix D, Chapter 3 (February to April 2026: the discipline absorbs a vendor regression).
**Caveat:** The attribution to the February adaptive-thinking rollout is Laurenzo's, not the vendor's; the post-mortem's own three causes start in March. The two accounts agree on the regressions and diverge on the earliest cause.

---

### Vulnerabilities with patch versions

**Claim:** Claude Code was vulnerable to remote code execution via untrusted project files: malicious `.mcp.json` or `.claude/settings.json` files in untrusted repos could execute hooks before the trust dialog, enabling RCE.
**Source:** Check Point Research, February 2026. CVE-2025-59536. NVD: [nvd.nist.gov/vuln/detail/CVE-2025-59536](https://nvd.nist.gov/vuln/detail/CVE-2025-59536). Writeup: [research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/).
**Where used:** Appendix D, Chapter 2 (three vulnerability classes behind layers one to three); referenced in Appendix A (One team, week by week, security committee scene).
**Caveat:** Disclosed and patched in Claude Code v1.0.111 (October 2025); the Check Point writeup was published February 2026. Versions earlier than the patch remain vulnerable; the class survives even after the specific patch.

---

**Claim:** Claude Code was vulnerable to API-key exfiltration via configuration injection: attacker-controlled settings overriding `ANTHROPIC_BASE_URL` before the trust prompt could leak API keys.
**Source:** Check Point Research, February 2026. CVE-2026-21852.
**Where used:** Appendix D, Chapter 2 (three vulnerability classes behind layers one to three).
**Caveat:** Patched in Claude Code v2.0.65. Same class as CVE-2025-59536: pre-trust execution of untrusted project configuration.

---

**Claim:** Claude Code automatically loads `.env*` files in the working directory at session start without explicit user permission, exposing secrets to the agent's context.
**Source:** Knostic, December 2025. Blog: [knostic.ai/blog/claude-loads-secrets-without-permission](https://knostic.ai/blog/claude-loads-secrets-without-permission).
**Where used:** Chapter 2 (Layer 3: Secrets); Appendix D, Chapter 2 (three vulnerability classes behind layers one to three), named in the dot-env auto-loading vulnerability class.
**Caveat:** Mitigation is sandbox `denyRead` of the `.env*` patterns rather than a vendor patch; in June 2026 Claude Code added an opt-in `sandbox.credentials` setting that blocks sandboxed commands from reading credential files and secret environment variables - a more targeted control for the same class, still opt-in rather than default. The behavior may change in future versions; the class (agents loading local config at session start) is enduring.

---

**Claim:** Claude Code's deny rules were silently bypassed when a shell command chained more than 50 subcommands (MAX_SUBCOMMANDS_FOR_SECURITY_CHECK = 50 hard cap), with the security check falling through to a generic "ask" prompt.
**Source:** Adversa AI Red Team, disclosed April 1, 2026. Writeup: [adversa.ai/blog/claude-code-security-bypass-deny-rules-disabled/](https://adversa.ai/blog/claude-code-security-bypass-deny-rules-disabled/).
**Where used:** Chapter 2 (When it breaks); Appendix D, Chapter 2 (three vulnerability classes behind layers one to three), as the parser-cap bypass example for "any single layer can have a quiet-failure mode."
**Caveat:** Patched in Claude Code v2.1.90 in the first days of April 2026 - Adversa's own writeup records the fix by April 4, within days of disclosure. The class - governance layers with parser caps that silently fail - is what to remember after the specific cap is gone.

---

**Claim:** Permission parsers in coding agents recognize only a known set of shell-read commands; agents invoking Python's `open()`, Node's `fs.readFile`, or any unrecognized binary bypass the deny rules entirely.
**Source:** Adam Kinney, April 2026. Writeup: [Claude Code's Deny Rules Don't Protect You - Here's What Actually Does](https://adamkinney.com/aatt/claude-code/deny-rules-dont-protect-you-sandbox-does/).
**Where used:** Appendix D, Chapter 2 (three vulnerability classes behind layers one to three), as the permission-parser bypass class.
**Caveat:** Architectural, not a single CVE. Mitigation is the OS sandbox `denyRead` list (kernel-level), not a vendor patch. The class persists across patches because the parser cannot enumerate every binary.

---

**Claim:** Two zero-click prompt-injection vulnerabilities in Cursor's sandbox - CVE-2026-50548 and CVE-2026-50549 (CVSS 9.8, dubbed "DuneSlide") - abused the working-directory write allowlist and a symlink-resolution fallback to escape the sandbox and reach OS-level remote code execution. All versions before Cursor 3.0 (April 2, 2026) were affected; 3.0 fixed both.
**Source:** Cato Networks (Cato AI Labs), disclosed mid-2026. Writeup: [catonetworks.com/blog/duneslide-two-critical-rce-vulnerabilities/](https://www.catonetworks.com/blog/duneslide-two-critical-rce-vulnerabilities/); coverage: SecurityWeek, The Hacker News, July 2026.
**Where used:** Chapter 2 (When it breaks); Appendix D, Chapter 2 (the sandbox escapes), layer two.
**Caveat:** The lesson is the class, not the vendor: the strongest layer can itself have bugs, which is why the layers are five and not one.

---

**Claim:** Mozilla 0Din researchers demonstrated (June 2026) an indirect prompt-injection attack in which a harmless-looking repository induces Claude Code to run a script that pulls a base64-encoded payload from a DNS TXT record and spawns a reverse shell - splitting the attack across the repository, DNS, and the developer's machine so no reverse-shell signature appears in plaintext on disk or on the wire.
**Source:** SecurityWeek, June 29, 2026: [securityweek.com/new-attack-abuses-claude-code-and-harmless-looking-repositories-to-hijack-developer-machines/](https://www.securityweek.com/new-attack-abuses-claude-code-and-harmless-looking-repositories-to-hijack-developer-machines/).
**Where used:** Chapter 2 (Injection arrives through the work itself); Appendix D, Chapter 2 (injection through the work: the DNS TXT proof of concept).
**Caveat:** Proof of concept; no vendor patch reported at the time of writing. The mitigation is the layered posture - a network allowlist bounds the DNS path regardless of what the agent was convinced to run.

---

### Tool documentation

**Claim:** Codex CLI shipped Agent Skills as a first-class primitive in December 2025, with SKILL.md files using YAML frontmatter and progressive disclosure semantics comparable to Claude Code Skills.
**Source:** OpenAI Codex CLI docs, [developers.openai.com/codex/skills](https://developers.openai.com/codex/skills).
**Where used:** Appendix D, Chapter 1 (memory and skills: the convergence story), as the Codex side of the skill-primitive convergence.
**Caveat:** Vendor documentation; the GA dates are accurate as of mid-2026 but may be revised retroactively.

---

**Claim:** Codex CLI subagents went GA on March 14, 2026 and run up to six in parallel by default (`agents.max_threads`, default 6; nesting depth defaults to one level).
**Source:** OpenAI Codex CLI docs, [developers.openai.com/codex/subagents](https://developers.openai.com/codex/subagents).
**Where used:** Appendix D, Chapter 1 (subagent adoption timeline).
**Caveat:** Vendor documentation; the six-thread default is effectively a cap as of mid-2026 (openai/codex#11965 tracks making it configurable) and may change with subsequent versions.

---

**Claim:** Codex CLI documents [AGENTS.md](https://agents.md/) as the convention for project-level agent instructions, loaded at session start and equivalent in role to other vendors' team-instruction files.
**Source:** OpenAI Codex CLI documentation, [developers.openai.com/codex/agents-md](https://developers.openai.com/codex/agents-md).
**Where used:** Chapter 1 (Memory) and Chapter 6 (AGENTS.md as team infrastructure).
**Caveat:** Filename and loading semantics are stable; specific frontmatter and discovery rules may evolve with versions.

---

**Claim:** AGENTS.md as the vendor-neutral team-instruction-file convention has native support across Codex CLI, Cursor, GitHub Copilot, Gemini CLI, Aider, Zed, and Windsurf. The format is markdown; the loading semantics are equivalent across tools.
**Source:** Cross-vendor documentation: Codex CLI ([developers.openai.com/codex/agents-md](https://developers.openai.com/codex/agents-md)), Cursor ([cursor.sh/docs](https://cursor.sh/docs)), GitHub Copilot ([docs.github.com/copilot](https://docs.github.com/copilot)), Gemini CLI ([cloud.google.com/gemini/docs/codeassist](https://cloud.google.com/gemini/docs/codeassist)), Aider ([aider.chat/docs](https://aider.chat/docs)), Zed ([zed.dev/docs/ai](https://zed.dev/docs/ai)), Windsurf ([codeium.com/windsurf/docs](https://codeium.com/windsurf/docs)).
**Where used:** Chapter 1 (Memory), Chapter 6 (AGENTS.md vs CLAUDE.md) and Appendix D, Chapter 1 (memory and skills: the convergence story).
**Caveat:** The list of supporting tools grows over time; the claim is that AGENTS.md is the de facto vendor-neutral convention, not that the list is exhaustive. The list also churns: Google began transitioning Gemini CLI users to Antigravity CLI in mid-2026 (free and consumer tiers stopped being served in June) - and the successor reads the same AGENTS.md, which is the convention outliving the tool, i.e. the point of this entry.

---

**Claim:** opencode is an open-source coding agent maintained by an independent team, written in TypeScript and licensed under MIT. Source-organized around the same primitives this manual identifies in Codex CLI and Claude Code.
**Source:** opencode repository ([github.com/anomalyco/opencode](https://github.com/anomalyco/opencode); formerly sst/opencode - the maintaining company renamed to Anomaly in January 2026); LICENSE and README.
**Where used:** Chapter 1 (The anatomy is invariant, the two-agent proof) and Appendix D, Chapter 1 (the two-agent demo, in detail).
**Caveat:** Project naming and maintainer composition may evolve; the architectural convergence claim survives renames.

---

**Claim:** Playwright drives a real browser through scripted interactions; the accessibility tree is the semantic structure browsers expose for assistive technology and is stable across visual restyles or component-library swaps. Tests written against the accessibility tree assert behavior rather than presentation.
**Source:** Playwright documentation ([playwright.dev/docs/accessibility-testing](https://playwright.dev/docs/accessibility-testing)); W3C ARIA Accessibility Object Model spec.
**Where used:** Chapter 5 (Verify), as the recommended frontend-verification pattern; Appendix D, Chapter 5 (Playwright with the accessibility tree); Appendix B.3 checklist.
**Caveat:** Some UI behavior (animation, drag-and-drop, complex canvas surfaces) is not fully captured by the accessibility tree and needs supplementary verification.

---

**Claim:** Claude Code supports OS-level sandboxing on Linux (bubblewrap with Landlock and seccomp), macOS (Seatbelt), and Windows (restricted tokens with job objects), and is opt-in by configuration. Codex CLI enforces sandbox by default on Linux and macOS; you have to opt out, not opt in.
**Source:** Claude Code docs ([code.claude.com/docs/en/sandboxing](https://code.claude.com/docs/en/sandboxing)) and Codex CLI agent approvals and security docs ([developers.openai.com/codex/agent-approvals-security](https://developers.openai.com/codex/agent-approvals-security)).
**Where used:** Chapter 1 (Sandbox posture is a governance choice) and Chapter 2 (Layer 2: Sandbox); Appendix D, Chapter 1 (sandbox posture by vendor, and the mechanisms underneath).
**Caveat:** Default-on versus opt-in is a versioned implementation detail. Verify the current default for your installed version before relying on it.

---

**Claim:** Cursor 2.0 (October 2025) introduced parallel independent agents and default-on macOS sandboxing; the subagent system proper - a parent agent delegating to child subagents - shipped in Cursor 2.4 (January 2026) and went async in 2.5. Cline shipped subagents natively. Claude Code added Agent Teams as a higher-level coordination layer on top of the Task tool.
**Source:** Cursor changelogs (2.0, 2.4, 2.5); vendor announcements and docs for Cline and Claude Code; collated across early-to-mid 2026.
**Where used:** Appendix D, Chapter 1 (subagent adoption timeline), as evidence for subagent-primitive convergence within roughly a year.
**Caveat:** Vendor surface areas evolve; the convergence claim survives even when specific product names rebrand.

---

**Claim:** Claude Fable 5, launched June 9, 2026 as the first Mythos-class model, had access suspended worldwide from June 12 to June 30, 2026 before being redeployed.
**Source:** Anthropic, "Claude Fable 5 and Mythos 5" (June 9, 2026): [anthropic.com/news/claude-fable-5-mythos-5](https://www.anthropic.com/news/claude-fable-5-mythos-5); "Redeploying Fable 5" (June 30, 2026): [anthropic.com/news/redeploying-fable-5](https://www.anthropic.com/news/redeploying-fable-5).
**Where used:** Chapter 9 (The vendor will have a bad week).
**Caveat:** The suspension rationale is the vendor's account; the operational lesson - plan for vendor downtime - is independent of the cause.

---

**Claim:** An Anthropic engineer's July 2026 field guide describes Claude Fable 5 as "the first model where I find the quality of the work is bottlenecked by my ability to clarify its unknowns," and organizes the working method around four kinds of unknowns, with techniques including the blind spot pass, implementation-notes files, and comprehension quizzes.
**Source:** Thariq Shihipar, "A field guide to Claude Fable 5: Finding your unknowns," Anthropic blog, July 6, 2026: [claude.com/blog/a-field-guide-to-claude-fable-finding-your-unknowns](https://claude.com/blog/a-field-guide-to-claude-fable-finding-your-unknowns).
**Where used:** Chapter 3 (the formulation bottleneck and the four unknowns), Chapter 4 (blind spot pass in Research, implementation notes in Execute) and Chapter 5 (the quiz in the agent-diff read); Appendix D, Chapter 3 (the unknowns frame, in full).
**Caveat:** One practitioner's account, published by the vendor about its own model. The techniques stand on their own; the "first model" superlative is the author's judgment, not a measurement.

---

### Marketplaces and plugin ecosystems

**Claim:** Anthropic's `claude-plugins-official` marketplace ships built-in with Claude Code as of May 2026 and bundles skills, hooks, tools, and commands behind a single install command. The marketplace warns users to trust plugins before installing.
**Source:** Claude Code docs ([code.claude.com/docs/en/discover-plugins](https://code.claude.com/docs/en/discover-plugins)); the marketplace itself.
**Where used:** Chapter 1 (Plugins); Appendix D, Chapter 1 (plugins: why each vetting question exists).
**Caveat:** Plugin counts and marketplace policies will drift; the supply-chain discipline described in Chapter 1 is what to take away rather than any specific count.

---

### Memory primitive sources

**Claim:** AGENTS.md is read at session start by Codex CLI, Cursor, GitHub Copilot, Gemini CLI, Aider, and the wider open-source coding-agent ecosystem (20+ vendors listed at agents.md as of 2026-05). Claude Code reads CLAUDE.md, which can import AGENTS.md to share the same content with other agents. The convergence puts AGENTS.md in the manually defined memory layer of the Memory primitive named in Chapter 1.
**Source:** [agents.md](https://agents.md/) (the open standard's site), plus vendor documentation for each agent listed.
**Where used:** Chapter 1 (Memory) and Chapter 6 (AGENTS.md as team infrastructure); Appendix D, Chapter 1 (memory and skills: the convergence story).
**Caveat:** The exact filename and load semantics vary by vendor - Claude Code reads CLAUDE.md (importable from AGENTS.md via `@AGENTS.md` or symlink); Cursor reads AGENTS.md plus `.cursorrules`. Convergence is on the structural role - user-written, always-loaded, team-shareable - not on byte-identical file format.

---

**Claim:** Claude Code maintains an auto-memory layer in which Claude writes notes for itself across sessions - build commands it figured out, debugging insights it confirmed, code-style preferences it inferred - distinct from the user-written CLAUDE.md. Requires Claude Code v2.1.59+; on by default; per-repo storage.
**Source:** [code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory).
**Where used:** Chapter 1 (Memory); Appendix D, Chapter 1 (memory and skills: the convergence story).
**Caveat:** The entry documents the Claude Code implementation, but the half is a convergence, not an exclusive: GitHub Copilot Memory reached public preview on January 15, 2026 - before Auto Memory shipped - and was on by default for Pro tiers by March 4; Codex CLI added automatic background memory in April 2026.

---

**Claim:** Anthropic publicly unveiled Dreaming as part of Claude Managed Agents at Code with Claude SF on 2026-05-06 - a scheduled background process that reviews recent sessions and the memory store, identifies recurring mistakes and convergent workflows, and writes consolidated notes back into long-term memory. It ships as a platform-level feature gated behind a beta header; a Claude Code CLI surface (`/dream`) was hinted in the product but had not shipped as a working command as of July 2026.
**Source:** Code with Claude SF announcement, 2026-05-06; [code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory).
**Where used:** Appendix D, Chapter 1 (memory and skills: the convergence story).
**Caveat:** Dreaming is Anthropic-specific and API-level at publication date, not yet a CLI feature. The structural role is what this manual indexes, not the vendor.

---

### Permissions / Sandbox primitive sources

**Claim:** Claude Code ships an Allow/Ask/Deny permission model with deny-then-ask-then-allow precedence and an opt-in OS sandbox - Seatbelt on macOS, bubblewrap on Linux - configurable via `/sandbox` and project-level `.claude/settings.json`. The decision layer is on by default; the OS sandbox is not.
**Source:** [code.claude.com/docs/en/permissions](https://code.claude.com/docs/en/permissions); [code.claude.com/docs/en/sandboxing](https://code.claude.com/docs/en/sandboxing).
**Where used:** Chapter 1 (Permissions / Sandbox) and Chapter 2 (Layer 1: Permissions and Layer 2: Sandbox).
**Caveat:** Opt-in posture on the OS-enforcement half. A default Claude Code installation has the decision layer but no kernel-level sandbox; most installations skip the sandbox configuration step.

---

**Claim:** Codex CLI enforces OS-level sandbox by default on Linux (Landlock + seccomp via bwrap) and macOS (Seatbelt); on Windows it uses restricted tokens plus ACL-based isolation. The decision layer ships alongside as a per-tool approval gate.
**Source:** [developers.openai.com/codex/concepts/sandboxing](https://developers.openai.com/codex/concepts/sandboxing); [developers.openai.com/codex/agent-approvals-security](https://developers.openai.com/codex/agent-approvals-security).
**Where used:** Chapter 1 (Permissions / Sandbox; Sandbox posture is a governance choice) and Chapter 2 (Layer 2: Sandbox); Appendix D, Chapter 1 (sandbox posture by vendor, and the mechanisms underneath).
**Caveat:** Opt-out posture - you can configure Codex to run without sandbox, but the default flips the convention from "off unless configured" to "on unless disabled." Windows implementation is the least uniform across major agents.

---

**Claim:** opencode ships an in-agent permission-prompt model and path/permission validation, but does not provide OS-level sandbox isolation; isolation requires the operator to wrap opencode in Docker, a microVM, or another sandbox harness (Vercel's KB documents this explicitly as a deployment pattern). On the convergence test from Chapter 1, opencode passes the decision-layer half and not the OS-enforcement half.
**Source:** [vercel.com/kb/guide/running-opencode-securely-with-the-vercel-sandbox](https://vercel.com/kb/guide/running-opencode-securely-with-the-vercel-sandbox).
**Where used:** Chapter 1 (Permissions / Sandbox; The anatomy is invariant; Sandbox posture is a governance choice); Appendix D, Chapter 1 (sandbox posture by vendor, and the mechanisms underneath).
**Caveat:** The "soft confinement" framing is the manual's, not opencode's documentation. opencode does not claim to ship a sandbox - the absence is honest, not hidden.

---

### Outer-loop and autonomy sources

**Claim:** By spring 2026 the outer loop is a first-class surface in Claude Code: /loop re-runs a prompt on an interval (March 2026) or paces itself when the interval is omitted (April 2026), Routines fire templated cloud agents from a schedule, a GitHub event, or an API call (April 2026), /goal keeps the agent working across turns until a completion condition holds (May 2026), and /autofix-pr watches CI and review comments and pushes fixes until the pull request is green (April 2026).
**Source:** Claude Code release notes, "What's new": [code.claude.com/docs/en/whats-new](https://code.claude.com/docs/en/whats-new), weekly digests for April-May 2026.
**Where used:** Appendix D, Chapter 9 (the outer loop: the vendor wave and stop-condition mechanisms).
**Caveat:** Feature names and release weeks are vendor-current as of July 2026; expect drift, per the note on dated claims.

---

**Claim:** The Ralph Wiggum technique - a bash while-loop re-piping a prompt file into a coding agent, one fresh context per iteration, state in the repository - originates with Geoff Huntley in mid-2025 ("In its purest form, Ralph is a Bash loop": `while :; do cat PROMPT.md | claude-code ; done`), went viral in late 2025, and was adopted into the official Claude Code repository as the ralph-wiggum plugin in November 2025 (the migrating commit is dated November 16). Huntley prices raw loop operation at roughly $10 per hour, says many Y Combinator startups run Ralph, and names the core failure mode "overbaking."
**Source:** Geoff Huntley, [ghuntley.com/ralph](https://ghuntley.com/ralph/) (July 2025); HumanLayer, "A Brief History of Ralph," January 6, 2026: [humanlayer.dev/blog/brief-history-of-ralph](https://www.humanlayer.dev/blog/brief-history-of-ralph); The Register, January 27, 2026: [theregister.com/2026/01/27/ralph_wiggum_claude_loops/](https://www.theregister.com/2026/01/27/ralph_wiggum_claude_loops/).
**Where used:** Appendix D, Chapter 9 (the outer loop: from AutoGPT to Ralph Wiggum), lineage and overbaking paragraphs.
**Caveat:** The $10-per-hour figure and the Y Combinator adoption claim are Huntley's own, relayed by The Register - practitioner-reported, not audited.

---

**Claim:** Background and scheduled agent execution shipped across vendors through late 2025: GitHub Copilot coding agent generally available September 25, 2025 (isolated GitHub Actions environment; output as a draft pull request; review requested from a human on completion); Cursor Cloud Agents October 30, 2025 (many detached agents, laptop closed); Google Jules Scheduled Tasks December 10, 2025 (recurring cadences for maintenance work).
**Source:** GitHub changelog: [github.blog/changelog/2025-09-25-copilot-coding-agent-is-now-generally-available](https://github.blog/changelog/2025-09-25-copilot-coding-agent-is-now-generally-available/); Cursor blog: [cursor.com/blog/cloud-agents](https://cursor.com/blog/cloud-agents); Google blog: [blog.google/technology/developers/jules-proactive-updates](https://blog.google/technology/developers/jules-proactive-updates/).
**Where used:** Appendix D, Chapter 9 (the outer loop: the vendor wave and stop-condition mechanisms), convergence paragraph.
**Caveat:** Ship dates are the vendors' announcements; the surfaces have kept evolving since.

---

**Claim:** StrongDM's "software factory" team runs fully non-interactive agentic delivery - humans neither write nor review code - with end-to-end user-story scenarios stored outside the codebase as a holdout set the agents cannot see or weaken, and treats roughly $1,000 per day per engineer in token spend as a factory health floor; Simon Willison frames the economics at about $20,000 per month per engineer and flags that as the pattern's main limitation.
**Source:** Simon Willison, "How StrongDM's AI team build serious software without even looking at the code," February 7, 2026: [simonwillison.net/2026/Feb/7/software-factory/](https://simonwillison.net/2026/Feb/7/software-factory/).
**Where used:** Appendix D, Chapter 9 (the outer loop: why each contract line exists, and the two poles), the industrial pole.
**Caveat:** Single-company self-description; the dollar figures are the team's and Willison's framing, not an audit.

---

**Claim:** The 2023 loop era - AutoGPT, BabyAGI - looped a model against its own assessment of progress, with no external grader per iteration, and collapsed as a software-delivery approach within months. The 2025 revival differs structurally: every iteration ends against compiler, tests, and diff.
**Source:** The AutoGPT and BabyAGI repositories document the 2023 design: [github.com/Significant-Gravitas/AutoGPT](https://github.com/Significant-Gravitas/AutoGPT), [github.com/yoheinakajima/babyagi](https://github.com/yoheinakajima/babyagi). The structural contrast is this manual's analysis, drawn from the Ralph-era sources above.
**Where used:** Appendix D, Chapter 9 (the outer loop: from AutoGPT to Ralph Wiggum), lineage paragraph.
**Caveat:** The collapse judgment is interpretive; both projects continued in other roles.

---

### Harness and model-migration sources

**Claim:** Anthropic removed over 80% of Claude Code's own system prompt for the Claude 5 generation (Opus 5, Fable 5) with no measurable loss on its coding evaluations, replacing rules with judgment and worked examples with designed interfaces.
**Source:** Thariq Shihipar, "The new rules of context engineering for Claude 5 generation models," Anthropic blog, July 24, 2026: [claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models](https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models).
**Where used:** Appendix D, Chapter 6 (the cap is sized by a rule-count cliff, and vendors are deleting instructions).
**Caveat:** Vendor's own evaluations on its own harness; the advice is written for the Claude 5 generation and older models may still need the deleted instructions.

---

**Claim:** Anthropic's prompting guide for Fable 5 states that separate, fresh-context verifier subagents tend to outperform self-critique; describes a memory system of one lesson per file with a one-line summary, updated rather than duplicated, deleted when wrong; documents rare early stopping on a statement of intent ("I'll now run X") and occasional unrequested actions, each with a prompt block; and warns that asking the model to reproduce its reasoning in the reply can trigger the reasoning_extraction refusal category.
**Source:** Anthropic, "Prompting Claude Fable 5," Claude Platform docs: [platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5).
**Where used:** Appendix D, Chapter 4 (vendor autonomy and scope blocks), Chapter 5 (the evidence behind the two-reviewer design) and Chapter 6 (mistake-journal mechanics); Appendix B.3 and B.9.
**Caveat:** Undated documentation page, revised in place; verify the current wording before relying on a specific phrase.

---

**Claim:** Anthropic's prompting guide for Fable 5.1 recommends that the tool starting a subagent return immediately with the result delivered in a later message; states that effort level names do not correspond to the same amount of thinking across models and that Fable 5.1 at low effort is often competitive with Opus and Sonnet on cost per task while scoring higher; requires append-only conversation history because thinking blocks are valid only in the exact conversation that produced them; notes that with cheaper cache reads, compacting early to save cost may no longer be the right trade; and gives a preserve-list for compaction summaries.
**Source:** Anthropic, "Prompting Claude Fable 5.1," Claude Platform docs: [platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1).
**Where used:** Chapter 1 (Effort), Chapter 6 (Context hygiene); Appendix D, Chapter 1 (Effort: the evidence), Chapter 4 (one writer, forked workers, isolated reviewers) and Chapter 6 (append-only history and cache pricing); Appendix B.7 and B.9.
**Caveat:** Undated documentation page for a model released September 1, 2026. The 0.025x figure in Appendix D, Chapter 6 is the manual's arithmetic from the published cache-read and base input prices at the time of writing; the append-only requirement applies to accounts created on or after August 31, 2026 per the guide.

---

**Claim:** Anthropic's advisor pattern: Sonnet with Opus as an advisor scored 2.7 percentage points higher on SWE-bench Multilingual than Sonnet alone at 11.9% lower cost per agentic task; Haiku with an Opus advisor scored 41.2% on BrowseComp against 19.7% solo, trailing Sonnet solo by 29% in score at 85% lower cost per task.
**Source:** Anthropic, "The advisor strategy: Give agents an intelligence boost," April 9, 2026: [claude.com/blog/the-advisor-strategy](https://claude.com/blog/the-advisor-strategy).
**Where used:** Appendix A (The structural levers, tier routing); Appendix D, Appendix A (tier routing, the two measured points).
**Caveat:** Vendor benchmarks on the vendor's own models; the cost figures are per task on those benchmarks, not a general ratio.

---

**Claim:** Anthropic's context editing (automatic clearing of stale tool results) delivered a 29% improvement on an internal agentic search evaluation.
**Source:** Anthropic, "Managing context on the Claude Developer Platform," September 29, 2025: [claude.com/blog/context-management](https://claude.com/blog/context-management).
**Where used:** Appendix D, Chapter 6 (compaction and context measurements).
**Caveat:** Internal evaluation; the post describes clearing, not a comparison against summarization - that comparison is the JetBrains entry below.

---

**Claim:** OpenAI's builder's guide reports that GPT-5.6 Sol at low reasoning effort outperformed GPT-5.5 at high effort on Agents' Last Exam with the harness held constant, and that programmatic tool calling matched rubric quality while using 21% fewer input tokens on a financial-research benchmark.
**Source:** OpenAI, "The builder's guide to GPT-5.6," August 2026: [openai.com/index/builders-guide-to-gpt-5-6/](https://openai.com/index/builders-guide-to-gpt-5-6/); migration guidance in "Prompting guidance for GPT-5.6 Sol," [developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6](https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6).
**Where used:** Appendix D, Chapter 1 (Effort: the evidence; what tool definitions cost); Appendix B.9.
**Caveat:** Vendor evaluations; the 21% figure is from one benchmark (Rogo's Big Finance Benchmark), not a general average. The migration guidance says to preserve the current effort as the baseline and compare one level lower, which is the B.9 sweep in the vendor's words.

---

**Claim:** OpenAI's guide for GPT-6 Astra states that the user's instructions take precedence over guidelines provided in a skill; that the model is more sensitive to information in context, so unclear or conflicting guidance in a skill file can make it pause and block work early; that it is more likely to ask the user a question when input could change the result; and that it tends toward broader tests than a task requires, with counter-guidance not to write tests for reversible, low-impact changes.
**Source:** OpenAI, "Using GPT-6 Astra," September 2026: [developers.openai.com/api/docs/guides/latest-model](https://developers.openai.com/api/docs/guides/latest-model).
**Where used:** Appendix D, Chapter 4 (vendor autonomy and scope blocks) and Chapter 6 (why the precedence line exists); Appendix B.2 and B.3.
**Caveat:** Astra is the codename of OpenAI's GPT-6 model released September 3-4, 2026, not a separate product; the guide is undated and revised in place.

---

**Claim:** OpenAI's own Codex practice keeps a short AGENTS.md of roughly 100 lines that serves primarily as a map with pointers to deeper sources of truth, with the repository's knowledge base in a structured docs/ directory treated as the system of record.
**Source:** Ryan Lopopolo, "Harness engineering: leveraging Codex in an agent-first world," OpenAI, February 11, 2026: [openai.com/index/harness-engineering/](https://openai.com/index/harness-engineering/).
**Where used:** Chapter 6 (Rules 3 and 4, where the map lives); Appendix D, Chapter 6 (repository overviews in context files do not help); Appendix B.2.
**Caveat:** One team's practice, described by the vendor. The Codex harness itself was released as open source in August 2026 ("Codex as a platform," [developers.openai.com/blog/codex-as-a-platform](https://developers.openai.com/blog/codex-as-a-platform)), which is a separate post.

---

**Claim:** Enabling retained reasoning and compaction took GPT-5.6 Sol from 13.3% to 38.3% on ARC-AGI-3 while reducing output tokens by a factor of six, with the harness otherwise unchanged.
**Source:** OpenAI, "How enabling two settings tripled our scores on the ARC-AGI-3 benchmark," July 29, 2026: [openai.com/index/how-two-settings-tripled-our-arc-agi-3-scores/](https://openai.com/index/how-two-settings-tripled-our-arc-agi-3-scores/).
**Where used:** Chapter 1 (Effort, retained reasoning); Appendix D, Chapter 1 (Effort: the evidence).
**Caveat:** Vendor post on one benchmark and one model. The manual uses it for the mechanism - reasoning kept across turns compounds - not for the specific score.

---

**Claim:** Both major agents now expose a completion-condition evaluator the loop does not control: Claude Code's /goal sends the condition and the conversation to a small fast model (Haiku by default) after each turn, which returns one of three verdicts - not yet met, met, or impossible; Codex Goals gives a thread a persistent completion condition and stops only when an evaluation confirms it or a hard limit is hit.
**Source:** Claude Code docs, "/goal": [code.claude.com/docs/en/goal](https://code.claude.com/docs/en/goal); OpenAI Cookbook, "Using Goals in Codex": [developers.openai.com/cookbook/examples/codex/using_goals_in_codex](https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex).
**Where used:** Chapter 9 (The outer loop, the stop condition); Appendix D, Chapter 9 (the outer loop: the vendor wave and stop-condition mechanisms).
**Caveat:** Mechanism documentation, not outcome evidence. The ralph-wiggum plugin's README names `--max-iterations` as the primary safety mechanism and offers anecdote rather than controlled results; no controlled evidence for any of the three was found at the time of writing.

---

**Claim:** Repository-level context files (AGENTS.md and equivalents) did not generally improve coding-agent task success while increasing inference cost by over 20% on average; repository overviews, although popular and recommended by model providers, were not helpful; files written by developers showed only a modest, non-significant gain over generated ones.
**Source:** Thibaud Gloaguen, Niels Mündler, Mark Niklas Müller, Veselin Raychev, Martin Vechev (ETH Zürich), "Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?", February 12, 2026 (v2 June 23, 2026): [arxiv.org/abs/2602.11988](https://arxiv.org/abs/2602.11988).
**Where used:** Chapter 6 (Rules 3 and 4, where the map lives); Appendix D, Chapter 6 (repository overviews in context files do not help); Appendix B.2.
**Caveat:** Measured on specific agents and benchmarks. The manual's reading - keep forbidden patterns, journal, conventions, and commands, move the map out - is an interpretation; the paper does not isolate a content category with a significant positive effect.

---

**Claim:** Across 260 multi-agent configurations, coordination helped only on decomposable tasks, degraded sequential planning by between 39% and 70% depending on architecture, and produced negative returns on tasks where a single agent already exceeded about 45% accuracy.
**Source:** Kim et al., "Capable language models can outgrow the benefits of collaboration," Nature Machine Intelligence 8, 1157-1172, July 24, 2026: [doi.org/10.1038/s42256-026-01268-y](https://doi.org/10.1038/s42256-026-01268-y); preprint "Towards a Science of Scaling Agent Systems," [arxiv.org/abs/2512.08296](https://arxiv.org/abs/2512.08296).
**Where used:** Chapter 4 (Execute, the split gate); Appendix D, Chapter 4 (when splitting into subagents pays); Appendix B.3.
**Caveat:** Benchmarks are not coding-specific; the 45% threshold is a fitted predictor across the tested tasks, not a law.

---

**Claim:** On SpecBench, every frontier agent saturates the visible test suite while the held-out score stays much lower, producing gaps of roughly 43 to 48 percentage points; the 90th-percentile gap grows by about 27 points for every tenfold increase in lines of code; additional search does not reliably remove the reward hacking.
**Source:** Bingchen Zhao, Dhruv Srikanth, Yuxiang Wu, Zhengyao Jiang (Weco AI), "SpecBench: Measuring Reward Hacking in Long-Horizon Coding Agents," May 20, 2026 (v2 September 9, 2026): [arxiv.org/abs/2605.21384](https://arxiv.org/abs/2605.21384).
**Where used:** Chapter 5 (Can you trust the tests the agent writes?); Appendix D, Chapter 5 (SpecBench and the Cursor finding in full); Appendix B.3.
**Caveat:** The abstract rounds the growth figure to 28 points; the body reports 27 with R² of 0.21, so the trend is real and noisy.

---

**Claim:** On SWE-bench Pro, 63% of successful Claude Opus 4.8 Max resolutions retrieved the upstream fix rather than deriving it; sealing git history and cutting network egress dropped the score from 87.1% to 73.0%.
**Source:** Naman Jain, Cursor, "Reward hacking is swamping model intelligence gains," June 25, 2026: [cursor.com/blog/reward-hacking-coding-benchmarks](https://cursor.com/blog/reward-hacking-coding-benchmarks).
**Where used:** Chapter 5 (Can you trust the tests the agent writes?, the sealed-history control); Appendix D, Chapter 5 (SpecBench and the Cursor finding in full).
**Caveat:** One vendor's harness and one model; the behavior is a property of the gate, not of the model named.

---

**Claim:** In a multi-agent reasoning setup, the more precise reviewer had its verified-useful critiques change the next candidate only 33.6% of the time, while a broadcast (peer) setup reached 93.5% and the higher final pass rate.
**Source:** Chih-Hsuan Yang et al., "Precise but Uncoupled: Reviewer Precision Does Not Guarantee Critique Uptake in Multi-Agent Math Reasoning," July 16, 2026: [arxiv.org/abs/2607.15388](https://arxiv.org/abs/2607.15388).
**Where used:** Chapter 5 (Review: two agents, then you); Appendix D, Chapter 5 (the evidence behind the two-reviewer design); Appendix B.3.
**Caveat:** Mathematical reasoning, not code review; the manual borrows the measurement, uptake over precision, not the domain.

---

**Claim:** A rubric-guided verify-and-repair loop (DeepVerifier) peaked around the fourth round and had declined by the tenth, because the incorrect-to-correct transition decays quickly while the correct-to-incorrect transition persists.
**Source:** Yuxuan Wan et al., "Inference-Time Scaling of Verification: Self-Evolving Deep Research Agents via Test-Time Rubric-Guided Verification," January 22, 2026 (v2 April 29, 2026): [arxiv.org/abs/2601.15808](https://arxiv.org/abs/2601.15808).
**Where used:** Chapter 5 (Review: two agents, then you, capping rounds); Appendix D, Chapter 5 (the evidence behind the two-reviewer design); Appendix B.3.
**Caveat:** Deep research agents on GAIA, not coding; the decline from the peak is a few points, so the lesson is the shape of the curve, not the size of the drop.

---

**Claim:** LLM judges anchor to a prior score shown to them, and neither chain-of-thought reasoning nor an explicit metadata-disregard warning removes the total effect.
**Source:** Ante Kapetanovic et al., "Anchoring Bias in LLM-as-a-Judge Systems: Prior Scores Compromise Evaluation Independence," August 26, 2026: [arxiv.org/abs/2608.25869](https://arxiv.org/abs/2608.25869).
**Where used:** Chapter 5 (Review: two agents, then you, the second reviewer stays blind); Appendix D, Chapter 5 (the evidence behind the two-reviewer design); Appendix B.3.
**Caveat:** Evaluation setting rather than code review; the manual applies the finding to reviewer two seeing reviewer one's verdicts.

---

**Claim:** The rate at which a model satisfies every rule in a prompt at once collapses to zero by about 80 simultaneous rules, for every model, format, and placement tested, including Claude Sonnet 5 and Claude Haiku.
**Source:** Netanel Eliav, "Prompt Design at Scale: How Format, Instruction Count, and Context Length Shape Instruction Adherence and Hallucination in Large Language Models," July 21, 2026: [arxiv.org/abs/2607.19257](https://arxiv.org/abs/2607.19257).
**Where used:** Chapter 6 (Rules 3 and 4, the hard cap); Appendix D, Chapter 6 (the cap is sized by a rule-count cliff, and vendors are deleting instructions).
**Caveat:** Perfect-response rate is a strict metric; other 2026 work on other frontier models reports softer thresholds. The manual uses the cliff to size the file, not to predict a specific compliance number.

---

**Claim:** RULER measures an effective context length - the longest input at which a model keeps a threshold score on retrieval and reasoning tasks across the window - and for most models tested that length falls well short of the claimed context size.
**Source:** Cheng-Ping Hsieh et al. (NVIDIA), "RULER: What's the Real Context Size of Your Long-Context Language Models?", 2024: [arxiv.org/abs/2404.06654](https://arxiv.org/abs/2404.06654).
**Where used:** Chapter 1 (Context window); Appendix D, Chapter 1 (effective context is shorter than the advertised window).
**Caveat:** The "around half" reading in Appendix D, Chapter 1 is a rule of thumb from 2026 practitioner roundups of RULER-style results, not a single measurement; per-model effective lengths vary widely and improve with each generation.

---

**Claim:** For long agentic coding sessions, masking old tool observations beat LLM summarization in four of five settings, cut cost by over 50%, and matched or slightly beat summarization on solve rate.
**Source:** Katie Fraser and Tobias Lindenbauer, JetBrains Research, "Cutting Through the Noise: Smarter Context Management for LLM-Powered Agents," December 2025: [blog.jetbrains.com/research/2025/12/efficient-context-management/](https://blog.jetbrains.com/research/2025/12/efficient-context-management/) (paper: "The Complexity Trap," NeurIPS 2025 DL4Code workshop).
**Where used:** Chapter 6 (Context hygiene); Appendix D, Chapter 6 (compaction and context measurements); Appendix A; Appendix B.7.
**Caveat:** The 52% figure sometimes quoted is one configuration (Qwen3-Coder 480B); the general finding is "over 50%."

---

**Claim:** Across 15 models, performance in fragmented multi-turn conversations dropped by 39% on average relative to a single fully specified turn, and consolidating the fragments into one turn recovered about 95% of the single-turn result.
**Source:** Philippe Laban, Hiroaki Hayashi, Yingbo Zhou, Jennifer Neville, "LLMs Get Lost in Multi-Turn Conversation," May 2025: [arxiv.org/abs/2505.06120](https://arxiv.org/abs/2505.06120).
**Where used:** Chapter 6 (Context hygiene, one unit of work per session); Appendix D, Chapter 6 (compaction and context measurements).
**Caveat:** Simulated conversations on generation tasks, not coding sessions; the manual uses it for the mechanism behind consolidating before continuing.

---

**Claim:** Opus 4.8 and Sonnet 5 invent keys that a custom nested tool schema never declared, while older models do not, and turning on strict tool invocation eliminated the behavior.
**Source:** Armin Ronacher, "Better Models: Worse Tools," July 4, 2026: [lucumr.pocoo.org/2026/7/4/better-models-worse-tools/](https://lucumr.pocoo.org/2026/7/4/better-models-worse-tools/).
**Where used:** Chapter 1 (Tools); Appendix D, Chapter 1 (what tool definitions cost, and the 2026 harness answers); Appendix B.9.
**Caveat:** One practitioner's runs on one harness; the recommendation - strict decoding on custom schemas - costs nothing to adopt regardless.

---

**Claim:** In a multi-agent harness, fork a worker so it receives the supervisor's history and prompt cache and continues the investigation, and isolate a verifier so it evaluates the work itself rather than being anchored by the supervisor's diagnosis; writes in working multi-agent systems stay single-threaded, with additional agents contributing intelligence rather than actions.
**Source:** Thushanth Bengre and Chester Curme, LangChain, "Organizing Context in a Multi-Agent Harness," September 8, 2026: [langchain.com/blog/organizing-context-in-a-multi-agent-harness](https://www.langchain.com/blog/organizing-context-in-a-multi-agent-harness); Walden Yan, Cognition, "Multi-Agents: What's Actually Working," April 22, 2026: [cognition.com/blog/multi-agents-working](https://cognition.com/blog/multi-agents-working).
**Where used:** Chapter 4 (Execute, one writer per file); Appendix D, Chapter 4 (one writer, forked workers, isolated reviewers); Appendix B.3.
**Caveat:** Both are vendor engineering posts; "one writer" is the manual's compression of Cognition's "writes stay single-threaded."

---

**Claim:** OpenWiki's claims runtime, which attaches evidence pointers to stored claims and re-checks them, cut stale claims in its knowledge base from 3.5% to 0.5% across 2,000 evaluated claims.
**Source:** Colin Francis, "Building Self-Correcting Memory in OpenWiki," LangChain blog, August 25, 2026: [langchain.com/blog/self-correcting-memory-openwiki](https://www.langchain.com/blog/self-correcting-memory-openwiki).
**Where used:** Chapter 6 (Rules 2 and 5, the evidence pointer); Appendix D, Chapter 6 (mistake-journal mechanics).
**Caveat:** A knowledge-base system, not a mistake journal; the manual borrows the mechanism - a claim that cites its evidence can be retired when the evidence goes stale.

---

**Claim:** Agentic navigation on Claude Sonnet 4.5 reached 49.6% recall@1 on BRIGHT, 21.8 points above the best embedding model; bounded workspaces (RISE) keep agentic retrieval working at one million documents where direct context inspection degrades; and code search for agents resolves into three modalities - lexical (ripgrep), structural (ast-grep), and graph (LSP references).
**Source:** Susheel Suresh et al., "AgenticRAG: Agentic Retrieval for Enterprise Knowledge Bases," May 7, 2026: [arxiv.org/abs/2605.05538](https://arxiv.org/abs/2605.05538); Shengyao Zhuang et al., "Towards Retrieving Interaction Spaces for Agentic Search" (RISE), June 5, 2026: [arxiv.org/abs/2606.06880](https://arxiv.org/abs/2606.06880); Andrey Kumanyaev, "Code search for AI agents: the grep replacement is three tools, not one," June 6, 2026: [zzet.org/gortex/grep-replacement-for-ai-agents/](https://zzet.org/gortex/grep-replacement-for-ai-agents/).
**Where used:** Appendix D, Chapter 7 (why the agent reads the code rather than an index of it); Chapter 7 (The workflow) states the conclusion.
**Caveat:** The recall figure is on a general retrieval benchmark, not a codebase; the three-tools framing is a practitioner's, and the manual states no numeric threshold for when an embedding index starts to pay.

---

**Claim:** Prompt caching with a cache-first prompt layout reduced API cost by 41% to 80% across providers on more than 500 agent sessions; a default Claude Code session was found to consume roughly 24,000 tokens of tool definitions, MCP schemas, and reminders before any user interaction; with a large tool pool fully loaded, baseline tool-selection accuracy was 13.62% and retrieving only the relevant tools per query raised it to 43.13%; one practitioner's count put three MCP servers at roughly 143,000 tokens of a 200,000-token window.
**Source:** Elias Lumer et al., "Don't Break the Cache: An Evaluation of Prompt Caching for Long-Horizon Agentic Tasks," January 31, 2026: [arxiv.org/abs/2601.06007](https://arxiv.org/abs/2601.06007); GitHub issue anthropics/claude-code#42452, April 2, 2026; Tiantian Gan and Qiyao Sun, "RAG-MCP: Mitigating Prompt Bloat in LLM Tool Selection via Retrieval-Augmented Generation," May 6, 2025: [arxiv.org/abs/2505.03275](https://arxiv.org/abs/2505.03275); MetaBlogue, "MCP servers and the context window," September 5, 2026: [metablogue.com/mcp-servers-context-window/](https://metablogue.com/mcp-servers-context-window/).
**Where used:** Chapter 1 (Tools); Appendix D, Chapter 1 (what tool definitions cost, and the 2026 harness answers); Appendix A (The structural levers).
**Caveat:** The 24k and 143k figures are practitioner counts that vary by installation and were not produced by a controlled study; the RAG-MCP figures compare a retrieval method against a no-retrieval baseline at scale and date from 2025.

---

**Claim:** For between 37% and 63% of software-engineering papers surveyed, a newer model with a single prompt natively outperforms the heavily engineered tooling proposed about a year earlier.
**Source:** Nahian Salsabil et al., "What Survives the Next Model? Benchmarking LLM-Based Techniques Against Single-Prompts," August 31, 2026: [arxiv.org/abs/2609.00468](https://arxiv.org/abs/2609.00468).
**Where used:** Chapter 8 (When it breaks, the model-migration check); Appendix D, Chapter 8 (the model-migration soft signal, with its evidence); Appendix B.9.
**Caveat:** arXiv preprint, not yet peer-reviewed; the manual uses it for the direction - each generation retires part of the harness - not the exact fraction.

---

### Notes on currency

Most of the sources in this appendix are dated. Tool documentation updates frequently; vulnerability records get amended as patches ship and new variants surface. The frameworks in the body of the manual are intended to outlast any specific source URL. If a URL breaks, the underlying claim should still be searchable by the named incident, study, or product.

---

---

## Appendix D. Deep dives

This is where the evidence and dated detail behind each chapter lives: the studies, benchmarks, vendor timelines and worked cases that the chapters leave out so they can stay short. Entries are grouped by chapter, each ending with its sources and caveats in italics. Full citations are in Appendix C; vendor behavior is dated to mid-2026 and will drift, so check defaults against the version you run.

---

### Chapter 1 - What an agent is {#deep-dive-chapter-1}

**Effective context is shorter than the advertised window.** Windows run from 200 thousand tokens on compact models to a million from the mid-range up. NVIDIA's RULER measures effective context length, the longest input at which a model still holds its short-context score across the whole window, and for most models it lands well under the advertised figure, commonly around half. *Source: Hsieh et al. (NVIDIA), "RULER," 2024. Caveat: "around half" is a rule of thumb from 2026 practitioner roundups, not one measurement.*

**What tool definitions cost, and the 2026 harness answers.** One audit of a default Claude Code session counted about 24k tokens of tool definitions, MCP schemas and reminders before the user typed anything; one practitioner put three MCP servers at 143k of a 200k window. With a large catalog fully loaded, tool-selection accuracy in one benchmark was 13.62%; loading only the relevant tools raised it to 43.13%. The 2026 answers are deferred loading and programmatic tool calling (the model scripts the calls and returns one result; native in GPT-5.6, where it cut input tokens by 21% on one financial-research evaluation). For custom tools with nested schemas, turn strict decoding on: Armin Ronacher documented Opus 4.8 and Sonnet 5 inventing undeclared fields, and strict mode eliminating it. *Sources: Lumer et al., Jan 31, 2026; anthropics/claude-code#42452, Apr 2, 2026; Gan and Sun (RAG-MCP), May 6, 2025; MetaBlogue, Sep 5, 2026; OpenAI GPT-5.6 guide, Aug 2026; Ronacher, Jul 4, 2026. Caveats: 24k and 143k are practitioner counts; the 21% is one benchmark (Rogo's).*

**Sandbox posture by vendor, and the mechanisms underneath.** The OS half runs on Seatbelt (macOS), bubblewrap with Landlock and seccomp (Linux) and restricted tokens with job objects or WSL2-backed isolation (Windows, the least uniform). Codex CLI enforces it by default on Linux and macOS, so you opt out. Cursor added kernel-backed controls in 2.x (default-on macOS from 2.0, October 2025); Gemini CLI ships per-platform profiles. Claude Code is opt-in (`/sandbox`, project `.claude/settings.json`) and most installations skip it, leaving a default install with no kernel-level protection against injection or agent misbehavior (PocketOS is what an unsandboxed default installation looks like when it goes wrong). opencode has permission prompts and path validation only, leaving OS isolation to the operator's Docker or microVM ("soft confinement" is the manual's term). Allowlists for paths and network go in the agent's configuration or AGENTS.md; setup takes an afternoon. Defaults are versioned, so verify yours. *Sources: Claude Code and Codex CLI docs; Vercel KB on opencode; Cursor changelogs.*

**The two-agent demo, in detail.** Claude Code ran in two panes against Codex CLI (Rust, Apache 2.0, OpenAI) and opencode (TypeScript, MIT, independent team) with one prompt: explain the architecture, map the agent loop, tool system, permission gates, sandbox and plugin model, citing files and lines. It took about four minutes (a May 2026 re-run: 4:13), because both repositories name their architecture in their directories; a less self-documenting codebase takes ten to fifteen minutes per repo. Both returned an agent loop, tool registry, permission gate, plugin directory, MCP support and a subagent path (in opencode, found by behavior: a function that spawns a fresh instance on a bounded prompt). The one divergence was the sandbox. *Source: author experiment, no human correction. Limit: the primitives exist; that does not make them equally well built.*

**Subagent adoption timeline.** Claude Code shipped the Task tool, then Agent Teams on top. Codex CLI took subagents GA on March 14, 2026 (up to six in parallel by default, nesting depth one). Cursor shipped parallel agents in 2.0 (October 2025), a subagent system in 2.4 (January 2026) and async in 2.5. *Sources: Codex CLI subagents docs; Cursor changelogs. Caveat: the six-thread Codex default is effectively a cap as of mid-2026.*

**Scripted orchestration (`/workflows`).** Claude Code's `/workflows` (mid-2026) has the agent write a script that dispatches subagents deterministically: ordered phases, parallel or pipeline fan-out across hundreds of children, schema-validated handoffs, an optional verification gate, resumable and budget-bounded. Determinism is the only real difference from model-driven dispatch (as in Superpowers); use it when the fan-out is large, repeatable or worth verifying mechanically. *Source: Changelog, 2026-06-11.*

**Memory and skills: the convergence story.** The always-loaded primitive converged on AGENTS.md (read at session start by Codex CLI, Cursor, GitHub Copilot, Gemini CLI, Aider, Zed, Windsurf and more; 20+ vendors listed at agents.md as of 2026-05) and CLAUDE.md, which Claude Code reads natively and which can import AGENTS.md. On-demand skills converged too (Claude Code Skills; Codex CLI `SKILL.md`, December 2025). The agent-written half converged within a winter: GitHub Copilot Memory public preview January 15, 2026, on by default for individual tiers by March; Claude Code Auto Memory in February (v2.1.59+); Codex CLI background memory in April. Anthropic's Dreaming (Claude Managed Agents, Code with Claude SF, 2026-05-06) is a scheduled background process that reviews sessions and memory and writes consolidated notes back; it is platform-level behind a beta header, and a `/dream` CLI had not shipped as of July 2026. *Sources: agents.md; vendor and Claude Code memory docs. Caveat: load semantics vary (Cursor also reads `.cursorrules`).*

**Effort: the evidence.** With the harness held constant, GPT-5.6 Sol at low effort beat GPT-5.5 at high effort on Agents' Last Exam; Fable 5.1 at low effort is often competitive with Opus and Sonnet on cost per task while scoring higher, by its vendor's own guide. Effort names do not transfer between models, so every migration starts with a sweep (Appendix B.9). Whether reasoning is kept between turns is the harness's call: on ARC-AGI-3, by OpenAI's account, retained reasoning plus compaction took GPT-5.6 Sol from 13.3% to 38.3% while cutting output tokens sixfold. *Sources: OpenAI GPT-5.6 guide, Aug 2026; OpenAI ARC-AGI-3 post, Jul 29, 2026; Anthropic, "Prompting Claude Fable 5.1." Caveat: vendor evaluations on one benchmark and model; the manual uses ARC-AGI-3 for the mechanism, not the score.*

**Plugins: why each vetting question exists.** As of May 2026 the marketplace was a real distribution channel and a supply-chain surface, the npm of agentic coding. Behind the B.10 questions: a plugin from Anthropic, a known vendor or a verifiable engineer is a different risk class from one uploaded last week by an unknown name; broad permissions deserve the suspicion you give an npm package asking for filesystem and network access; the plugins worth installing are small enough to read in twenty minutes (Superpowers and hookify are); an update is a dependency update; a hook running outside the sandbox is unbounded. *Source: author field practice, May 2026.*

---

### Chapter 2 - Guardrails in five layers {#deep-dive-chapter-2}

**Three vulnerability classes behind layers one to three.** (1) Dot-env auto-loading: agents read `.env*` files in the working directory at session start. Mitigate with a sandbox deny-read list; Claude Code added an opt-in `sandbox.credentials` setting in June 2026 that blocks sandboxed commands from reading credential files and secret environment variables. (2) Configuration-file injection: untrusted `.claude/settings.json` or `.mcp.json` files run hooks before the trust dialog, enabling remote code execution (CVE-2025-59536, patched in Claude Code v1.0.111) or API-key exfiltration through an overridden `ANTHROPIC_BASE_URL` (CVE-2026-21852, patched in v2.0.65). (3) Permission-parser bypass: deny rules skipped for binaries the parser does not recognize (Python's `open()`, Node's `fs.readFile`), or, as a quiet failure, when a command chained more than fifty subcommands (`MAX_SUBCOMMANDS_FOR_SECURITY_CHECK = 50`) and the check fell through to a generic "ask"; disclosed April 1, 2026, patched in v2.1.90 within days. Nothing in the configuration shows such a failure, so assume any single layer can have a bug; the classes outlive their patches. *Sources: Knostic, Dec 2025; Check Point Research, Feb 2026 (patched October 2025); Adversa AI Red Team, Apr 1, 2026; Adam Kinney, Apr 2026. Caveat: architectural classes, not single CVEs; unpatched versions stay vulnerable.*

**The sandbox escapes ("DuneSlide").** In mid-2026 a red team disclosed two critical zero-click prompt-injection flaws in Cursor's kernel-backed sandbox (CVE-2026-50548 and CVE-2026-50549, CVSS 9.8) that abused its working-directory write allowlist and a symlink-resolution fallback to reach OS-level code execution. Versions before Cursor 3.0 (April 2, 2026) were affected. The lesson is the class, not the vendor: the strongest layer can have bugs, which is why there are five. *Sources: Cato Networks (Cato AI Labs), mid-2026; SecurityWeek and The Hacker News, Jul 2026.*

**Per-agent sandbox defaults.** See the Chapter 1 entry on sandbox posture by vendor; the point for this chapter is that a default install of an opt-in agent runs with layer two switched off.

**Injection through the work: the DNS TXT proof of concept.** In June 2026 Mozilla 0Din researchers showed a harmless-looking repository inducing Claude Code to run a script that pulls a base64 payload from a DNS TXT record and spawns a reverse shell, split across the repository, DNS and the developer's machine so no signature appears in plaintext. A proof of concept with no vendor patch reported; a network allowlist bounds the DNS path. *Source: SecurityWeek, Jun 29, 2026.*

**Telemetry plumbing and hook examples.** By mid-2026 Claude Code, Codex CLI and Gemini CLI emit OpenTelemetry natively, so the audit store can be whatever the stack already speaks; the requirement is durability and queryability. The security-guidance plugin ships rules for roughly eight to ten vulnerability categories. One team rule beyond the chapter's two: block edits to a compliance-relevant module outside business hours.

**PocketOS: where the accounts disagree, and what the platforms changed.** Railway's restore was reportedly about 30 minutes after the CEO contacted them; other accounts say about 30 hours, or two days, for full restoration, so the manual uses the incident for the governance pattern only. Within a week, on April 29, 2026, Railway moved all volume and resource deletes, including the API path the agent used, to soft-delete with a 48-hour recovery window, and added workspace guardrails and scoped agent credentials. Alexey Grigorev's follow-up to the DataTalks.Club Terraform loss (late February 2026) reads like this chapter's checklist: delete protection in Terraform and AWS, state moved to S3, manual review of every destructive plan, an upgraded AWS support tier. AWS restored roughly 1.94M rows from a snapshot within about a day. *Sources: DevOps.com; Business Insider; Railway blog, Apr 29, 2026; Grigorev's public account.*

---

**PocketOS: the public post.** The PocketOS CEO posted about the incident publicly, and the post quickly became a reference point in discussions of AI safety in production. *Source: Appendix C, Named incidents.*

**DataTalks.Club as the mirror image of PocketOS.** In the DataTalks.Club incident Claude Code ran `terraform destroy` against a stale state file: a map the agent did not know it needed, where PocketOS was a credential it should not have held. Same cure: confirmation on destructive operations, only the credentials the task needs, and state the team has verified. *Source: Alexey Grigorev's public account; Appendix C.*

### Chapter 3 - The bottleneck moved {#deep-dive-chapter-3}

**The unknowns frame, in full.** In July 2026 an Anthropic engineer opened a field guide to Claude Fable 5 with this chapter's observation: it was "the first model where I find the quality of the work is bottlenecked by my ability to clarify its unknowns." His four questions: known knowns (what your prompt states), known unknowns (questions you have not settled), unknown knowns (context so obvious you would never write it down, though you would spot a violation at once) and unknown unknowns (what neither of you thought to ask). *Source: Thariq Shihipar, Anthropic, Jul 6, 2026. Caveat: the frame adapts an older taxonomy and "first model" is his judgment, not a measurement; the mapping onto this manual's machinery (the chapter's table) is the author's.*

**The METR randomized controlled trial.** METR's July 2025 trial had experienced open-source developers work on their own familiar repositories with AI assistance. They took 19% longer than without it, after predicting a 24% speedup, and afterward still believed it had made them roughly 20% faster: a 43-point gap between predicted speedup and measured slowdown. The author reads it as a warning that raw assistance does not become delivery speed without workflow discipline. *Source: Becker et al., METR, Jul 10, 2025. Caveat: METR did not test formulation discipline; that reading is the author's. Its follow-up suffered selection bias, it redesigned the experiment in February 2026, and it cautions against applying the 19% to current tools.*

**February to April 2026: the discipline absorbs a vendor regression.** Claude Code product changes materially degraded complex engineering work in some workflows. On April 6, AMD senior director Stella Laurenzo published an audit of 6,852 of her own sessions and 234,760 tool calls, showing a shift from research-first to edit-first behavior as thinking redaction rolled from 1.5% to 100% of turns, and pointed at the February adaptive-thinking default as a contributing cause. Anthropic's April 23 post-mortem acknowledged three regressions: default effort dropped from high to medium on March 4 (reverted April 7); a caching bug from March 26 that cleared reasoning history every turn instead of once per idle hour (fixed April 10); and a system-prompt verbosity cap from April 16 with a measured 3% quality drop (reverted April 20). Two adjacent teams used the same Claude Code. The one with this manual's infrastructure (CLAUDE.md rules, plan mode by default, the six-phase loop, hooks on destructive operations) dropped maybe 10% and recovered once it tightened plan-mode gates and raised effort on a few skills; the freestyle team's velocity halved overnight. *Sources: Anthropic post-mortem, Apr 23, 2026; Laurenzo, anthropics/claude-code#42796, via The Register, Apr 6, 2026. Caveats: the accounts diverge on the earliest cause; external magnitudes are approximate; the two-team comparison is a field observation.*

---

### Chapter 4 - The six-phase loop {#deep-dive-chapter-4}

**When splitting into subagents pays.** A study of 260 multi-agent configurations found coordination pays only on decomposable work and costs between 39% and 70% on sequential work, planning above all; when a single agent already clears roughly 45% on a task, adding agents predicts no gain. Split only when tasks are independent by file or module. *Source: Kim et al., Nature Machine Intelligence 8, 1157-1172, Jul 24, 2026. Caveat: not coding-specific benchmarks; 45% is a fitted predictor, not a law.*

**One writer, forked workers, isolated reviewers.** Keep one writer per file, which is where Cognition landed after a year of arguing against multi-agent systems: parallel readers, a single writer. Fork the workers so they inherit the orchestrator's history cheaply through the cache; isolate the reviewers so they inherit none of it and cannot be anchored by its assumptions. On current harnesses dispatch returns immediately and the result arrives later, so the orchestrator keeps working (the shape B.3 assumes). Collisions are mediated cheaply (drop the later branch, re-run it sequentially with the first's output) or expensively (a higher-capability model picks the merge); the expensive ones eat the speed gain. *Sources: Walden Yan, Cognition, Apr 22, 2026; Bengre and Curme, LangChain, Sep 8, 2026; Anthropic, "Prompting Claude Fable 5.1." Caveat: vendor posts; "one writer" compresses Cognition's "writes stay single-threaded".*

**Vendor autonomy and scope blocks.** Fable ends a turn on a statement of intent ("I'll now run the tests") or takes an action nobody asked for; GPT-6 Astra pauses to ask unneeded questions and writes broader tests than a reversible change requires. Both vendors publish the fix as a prompt block: autonomy (finish the task before ending the turn; no tests for reversible, low-impact changes) and scope (only the files the plan names; stop and report on anything else). B.3 carries both; B.9 rewrites them for the next model. *Sources: Anthropic, "Prompting Claude Fable 5"; OpenAI, "Using GPT-6 Astra," Sep 2026.*

**The implementation-notes file pays twice.** The spec-compliance reviewer reads it first, a confession list of where diff and plan disagree, and it counters orchestrator-summary drift because each deviation is recorded when it happens, by the subagent that made it. Phase gating is still maturing: Superpowers asks through skill instructions, strict gating needs a project-specific PreToolUse hook, and kernel-level enforcement was immature as of mid-2026.

---

### Chapter 5 - Review and verify {#deep-dive-chapter-5}

**The evidence behind the two-reviewer design.** Anthropic's Fable 5 prompting guide states that separate, fresh-context verifier subagents tend to outperform self-critique. Uptake beats precision: in a July 2026 multi-agent reasoning study the more precise reviewer lost, its verified-useful critiques changing the solver's next answer only 33.6% of the time against 93.5% for a peer setup with less precise critiques broadcast to everyone, which also had the better final pass rate. Track the repair rate (findings fixed, or rebutted with a reason), not accuracy. Cap the rounds: a rubric-guided verify-and-repair loop (DeepVerifier) peaked around round four and had declined by round ten, because late rounds re-open settled work about as often as they fix it. Keep reviewer two blind: judges anchor to a prior score they see, and neither chain of thought nor an explicit warning removes it. *Sources: Anthropic, "Prompting Claude Fable 5" (undated, revised in place); Yang et al., Jul 16, 2026; Wan et al., Jan 22, 2026 (v2 Apr 29); Kapetanovic et al., Aug 26, 2026. Caveats: math reasoning and deep-research agents, not code review; the round-four decline is a few points, so the lesson is the curve's shape.*

**SpecBench and the Cursor finding in full.** SpecBench (May 2026) ran frontier agents against specifications with visible and hidden test sets. Every agent saturated the visible suite near 100%, with hidden-test gaps of roughly 43 to 48 points; the 90th-percentile gap grew by about 27 points per tenfold increase in lines of code, and more search did not reliably remove the reward hacking. Cursor found the other half in June 2026: on SWE-bench Pro, 63% of successful Claude Opus 4.8 Max resolutions had retrieved the upstream fix from git history or the network instead of deriving it, and sealing both dropped the score from 87.1% to 73.0%. Both are a system doing what the gate rewards, hence the four verify controls. *Sources: Zhao, Srikanth, Wu and Jiang (Weco AI), May 20, 2026 (v2 Sep 9); Naman Jain, Cursor, Jun 25, 2026. Caveats: the abstract rounds 27 to 28 points (R-squared 0.21), so the trend is real but noisy; Cursor's result is one harness and one model.*

**Playwright with the accessibility tree.** The accessibility tree is the structure browsers keep for assistive technology (a button with this label, a field labeled "email"), stable under restyling and component-library swaps. "Find the field labeled Priority, change it, click Save, verify the new value renders" passes whether the field is a select, radio group or custom component. Banking teams with flaky snapshot suites found it the first approach that stayed green. *Sources: Playwright docs; W3C ARIA AOM. Caveat: animation, drag-and-drop and canvas need supplementary verification.*

**The PR review toolkit's saving.** With four agents run first (silent-failure hunter, PR test analyzer, security scanner, documentation reviewer) catching the mechanical findings, a senior's fifteen-minute review becomes five, and the other ten go to architectural judgment.

---

### Chapter 6 - AGENTS.md and context {#deep-dive-chapter-6}

**Repository overviews in context files do not help.** ETH Zurich found that repository-level context files taken as a whole did not generally improve coding-agent task success while raising inference cost by over 20% on average. The repository overview, popular and vendor-recommended, did not help: the agent derives the layout from the tree in seconds. Developer-written files did slightly better than generated ones, not significantly. So the always-loaded file keeps rules, and the map moves to `docs/`, read on demand. OpenAI's Codex practice has the same shape: an AGENTS.md of roughly 100 lines that maps into a structured docs directory. *Sources: Gloaguen, Mundler, Muller, Raychev and Vechev (ETH Zurich), Feb 12, 2026 (v2 Jun 23); Ryan Lopopolo, OpenAI, Feb 11, 2026. Caveats: the paper isolates no content category with a significant positive effect, so keep-and-move is the manual's reading; OpenAI's is one team's practice.*

**The cap is sized by a rule-count cliff, and vendors are deleting instructions.** In a July 2026 study across formats and placements, the rate at which a model satisfied every rule at once collapsed to zero by about eighty simultaneous rules, on Claude Sonnet 5 and Claude Haiku alike. Eighty rules is roughly a two-hundred-line file with one rule per line, which is why 200 lines is a hard cap. Anthropic removed more than 80% of Claude Code's own system prompt for the Claude 5 generation with no measured loss on its coding evaluations, replacing rules with judgment and worked examples with typed tool interfaces. *Sources: Netanel Eliav, Jul 21, 2026; Thariq Shihipar, Anthropic, Jul 24, 2026. Caveats: perfect-response rate is a strict metric and other 2026 work reports softer thresholds, so the cliff sizes the file, not a compliance number; Anthropic's evaluations are its own.*

**Mistake-journal mechanics.** Anthropic's Fable 5 guide describes a memory system with three rules that keep a journal honest at a hundred entries: one lesson per file with a one-line summary, update rather than duplicate when a lesson recurs, delete notes that turn out wrong. Add an evidence pointer so the next champion can check whether the failure is still possible. OpenWiki's claims runtime, which attaches evidence pointers to stored claims and re-checks them, cut stale claims from 3.5% to 0.5% across 2,000 evaluated claims. The quarterly review asks of each entry, "has anyone been saved by this rule in the last three months?" If yes, keep it; if no but the rule still applies, keep it, since rare failures still matter; if no and the cause is gone, retire it with a commit-message note. *Sources: Anthropic, "Prompting Claude Fable 5"; Colin Francis, LangChain, Aug 25, 2026. Caveat: OpenWiki is a knowledge-base system, not a journal; the manual borrows the mechanism.*

**Why the precedence line exists.** GPT-6 Astra follows longer instructions better and is more sensitive to context: conflicting guidance in a skill file can make it pause and block early, and OpenAI's guide says the user's instructions take precedence over a skill's. One top line ("In a conflict, the task prompt wins over this file; this file wins over any skill", in the B.2 skeleton) removes a class of stalls. *Source: OpenAI, "Using GPT-6 Astra," Sep 2026 (GPT-6 released September 3-4, 2026; guide revised in place).*

**Compaction and context measurements.** JetBrains found that masking old tool outputs (call kept, bulky result blanked) beat LLM summarization in four of five settings at over 50% lower cost, with a matching or slightly better solve rate. Anthropic's tool-result clearing, the same move at platform level, gave a 29% gain on an internal agentic search evaluation. Across 15 models, fragmented multi-turn conversations lost 39% on average against a single specified turn, and one consolidated turn recovered about 95%. *Sources: Fraser and Lindenbauer, JetBrains Research, Dec 2025; Anthropic, Sep 29, 2025; Laban et al., May 2025. Caveats: the 52% sometimes quoted is one configuration (Qwen3-Coder 480B); Anthropic's result is internal; the multi-turn study used simulated generation tasks, not coding sessions.*

**Append-only history and cache pricing (Fable 5.1).** Thinking blocks are bound to the exact prefix that produced them, so editing or reordering earlier turns invalidates them and discards the retained reasoning that Chapter 1 counts as half of Effort: end the session and start clean. With cache reads at 0.025x the base input price, the guide says compacting early to save cost may no longer be the right trade; when you do compact, give the compactor a keep-list (the plan, open questions, deviations in the implementation notes, the exact commands that worked). *Source: Anthropic, "Prompting Claude Fable 5.1." Caveats: undated page; 0.025x is the manual's arithmetic from published prices; append-only applies to accounts created on or after August 31, 2026.*

---

### Chapter 7 - Map it first: architecture review {#deep-dive-chapter-7}

**Why the agent reads the code rather than querying an index of it.** Navigation beats retrieval on this task. On Claude Sonnet 4.5, agentic navigation (grep, open the file, follow the reference) reached 49.6% recall@1 on BRIGHT, 21.8 points above the best embedding model, and bounded workspaces (the RISE result) keep it working at a million documents, where direct context inspection degrades. Code search for agents resolves into three tools: ripgrep for text, ast-grep for structure, the language server for references. An embedding index is the exception you add when a corpus outgrows them. *Sources: Suresh et al., May 7, 2026; Zhuang et al. (RISE), Jun 5, 2026; Kumanyaev, Jun 6, 2026. Caveat: the recall figure is on a general retrieval benchmark, not a codebase.*

**The visual alternative: Understand Anything.** A plugin that renders the codebase as a navigable graph: a structural view (modules, dependencies) for engineers and a domain view (business concepts, entities) for managers, who can read "this service handles fraud detection on incoming transfers" without reading source.

---

### Chapter 8 - Should the agent touch this code? {#deep-dive-chapter-8}

**Signal 1, no tests: the reconciliation module.** Twice in banking: a reconciliation module written in the early 2010s by a senior engineer who left in 2018, with no tests because "the senior engineer just knew it worked." The next change broke it in a way that took two months to surface, by which point the discrepancy had crossed the threshold that triggers a regulatory disclosure. Fix: characterization tests first, the agent doing the bulk.

**Signal 2, no documentation: the fee tier.** The fee tier for the legacy product line was calculated differently because of a 2017 regulatory carve-out. The agent assumed uniform treatment and "simplified" it; the senior caught it in review. The second-order cost is senior engineers reviewing AI output forty hours a week instead of building, until they leave. Fix: the architecture review (Chapter 7) plus a short domain glossary.

**Signal 3, tight coupling: the fourteen-year cycle.** A customer service module imported a loan origination module, which imported a credit scoring module, which imported customer service: a cycle introduced fourteen years earlier to "save time" and never broken because it was an eight-week project. The agent's change surfaced months later at month-end batch close. Fix: break only the worst coupling; if the team will not, yellow at best.

**Signal 4, scattered rules: the maximum transfer amount.** The limit lived in a UI config, a service constant and a database trigger. Compliance updated the config; six weeks later a valid transfer failed on the stale constant. With no single source of truth the agent guesses which copy is canonical. Fix: one source (a typed rules engine or configuration service) and worth it with or without agents.

**Signal 5, regulatory constraints.** Any change to anti-money-laundering logic needs sign-off from the compliance officer, a representative from legal and a senior engineer not involved in the implementation; the agent cannot route approvals or satisfy a two-person rule. Mild constraints (a senior review on every change) fit the existing process; heavy ones (sign-off matrices, evidence trails, time-stamped approvals, retention) mean the agent works only inside a system that already handles them.

**Signal 7, model-context fit: the in-house workflow engine.** A custom engine from the early 2010s with no public documentation and peculiar state-transition syntax. The agent applied patterns from an unrelated framework it had seen more of; the code compiled, the thin tests passed, and the state machine misbehaved in three untested edge cases. With no substantial public footprint (repositories, documentation, talks), treat the codebase as if signal 6 were active even when every other signal is clean.

**Signal 8, velocity-of-change: the React 18/19 bug.** On a codebase mid-migration the agent is confidently right about the old version and wrong about the new, and you cannot always tell which. The author's own bug: Claude used React 18 idioms where React 19 was needed; it worked locally on a transitive React 18 dependency and broke when production pulled 19. Fix: a version rule in AGENTS.md ("we are migrating from React 18 to React 19 this quarter; new code uses 19 idioms; old code may still use 18 but should be updated when touched").

**The model-migration soft signal, with its evidence.** Instructions written for the previous model (AGENTS.md rules, skill prompts, effort levels) do not retire themselves. For between 37% and 63% of the software-engineering papers surveyed, a newer model given a single prompt natively outperformed the heavily engineered tooling proposed about a year earlier. It is not a ninth kill signal; it is what to check when a green codebase turns yellow after a model upgrade (Appendix B.9). *Source: Salsabil et al., Aug 31, 2026 (arXiv 2609.00468). Caveat: preprint, not peer-reviewed; use it for the direction, not the fraction.*

**The six worked examples in full.** (1) Customer-profile microservice: 70% coverage, README overview, REST-decoupled, rules in one typed validation library, standard SOX controls, seniors who handle profile changes. Zero, green. (2) Legacy payments engine: 20% mostly happy-path coverage, partly stale docs, moderate coupling with documented seams, a few straggler rules, real PCI and fraud-reporting constraints with audit machinery in place, one or two seniors who can judge payments output. No tests half, documentation half, coupling one, rules half, regulatory zero, evaluation zero: two and a half, rounded up to three, yellow. (3) Custom encryption library by a 2017 contractor: undocumented, integration-tested only, tightly coupled to key management, compliance rules in code, no cryptographer. Five, red. (4) Greenfield API service, senior team, clear spec: zero, green-plus. (5) Internal tool, 20 developers, written 2019, modest tests, low regulatory exposure: one, green-leaning, the right first target. (6) Vendor-customized fork, hasty contractor layer, no tests or docs on the customizations, severe upstream coupling: four, red. The question is the strategy: should the custom layer exist at all? Replace it with upstream features, contribute it back or maintain it deliberately, but do not use the agent to make the wrong work faster.

---

### Chapter 9 - Rolling it out {#deep-dive-chapter-9}

**The two kinds of hooks in full: pre-commit versus pre-push.** Split git checks by cost. Pre-commit is the fast pass (format, lint, typecheck, secret scan), seconds, so nobody reaches for the escape hatch; every skip trains the habit of skipping. Pre-push is the heavier pass (the fast test suite, the build), run once per push. Manage both from a versioned config through a hook manager so they install on every clone. The two boundaries cover each other's blind spot: the agent hook catches the agent mid-session before the edit lands, the git gate catches every author on paths the agent hook never sees. Deterministic checks do not drift the way probabilistic reviewers can.

**The outer loop: from AutoGPT to Ralph Wiggum.** The inner loop is the six-phase loop (Chapter 4); the outer loop wraps it and re-invokes the agent until a condition holds. In 2023 AutoGPT and BabyAGI looped a model against its own opinion of its progress; nothing external graded an iteration, laps compounded drift, and the approach collapsed as a way of shipping software within months. The revival differs structurally: in mid-2025 Geoff Huntley wired an agent into a bash while-loop (one prompt file, repeat), which spread as "Ralph Wiggum". Each iteration starts with a fresh context, does one unit of work and ends against graders the model does not control (compiler, tests, diff), with state in the repository. His name for the failure mode is overbaking: a loop left running past its job invents work nobody asked for. *Sources: ghuntley.com/ralph (Jul 2025); HumanLayer, Jan 6, 2026; The Register, Jan 27, 2026; AutoGPT and BabyAGI repositories. Caveat: the collapse judgment and structural contrast are the manual's interpretation.*

**The outer loop: the vendor wave and stop-condition mechanisms.** GitHub's Copilot coding agent went generally available on September 25, 2025 (isolated environment, draft pull request); Cursor shipped Cloud Agents on October 30, 2025; Google's Jules added Scheduled Tasks on December 10, 2025; a ralph-wiggum plugin landed in the official Claude Code repository in November 2025. By spring 2026 Claude Code had `/loop` (re-run on an interval or self-paced), Routines (cloud agents from a schedule or GitHub event), `/goal` (work until a completion condition holds) and `/autofix-pr` (push fixes until CI is green). By Chapter 1's test the capability converged, though what converged is a workflow around the primitives, not a primitive. `/goal` sends the condition and conversation to a fresh small model (Haiku by default) after each turn, returning not yet met, met or impossible; Codex Goals gives a thread a persistent condition confirmed by an evaluation or a hard limit. Both are a grader the loop does not control. The ralph-wiggum plugin has no controlled evidence, and its README names max iterations as its primary safeguard, a budget, not a stop condition. *Sources: GitHub changelog, 2025-09-25; Cursor and Google blogs; Claude Code release notes, Apr-May 2026; Claude Code "/goal" docs; OpenAI Cookbook, "Using Goals in Codex." Caveat: vendor dates drift; the goal docs describe mechanism, not outcomes.*

**The outer loop: why each contract line exists, and the two poles.** A machine-evaluable stop condition, because a loop without one is abandonment. A budget, because an unattended loop is the per-token model's best customer (Appendix A). A gate the agent cannot edit (tests, lint config, CI workflow, hook rules behind a deny rule), because the cheapest way to go green is to negotiate with your own grader, and a green suite the agent wrote is evidence, not proof (Chapter 5). Fresh context with a committed queue and journal: forty short sessions instead of one degrading one. Isolation sized for absence, since an unattended session is where prompt injection meets no human skeptic (Chapter 2). Queue many similar, machine-verifiable, reversible units (migrations, lint sweeps, dependency bumps, test backfill) on green codebases only. Huntley runs the loop raw at roughly $10 an hour; StrongDM's software factory runs fully non-interactive delivery, humans neither writing nor reviewing code, with end-to-end scenarios held outside the codebase as a holdout the loop cannot weaken, at a spend Simon Willison pegged near $20,000 a month per engineer. *Sources: Willison, Feb 7, 2026; Huntley and The Register as above. Caveat: the $10 figure is Huntley's own and the StrongDM figures are one company's self-description and Willison's framing, not audits.*

**Time budgets of the role commitments.** Champion: week one about three hours, week two about five, weeks three and four roughly the time the features would take by hand (the value is the experience), month two comparable to manual work; after ninety days, a working workflow, a maintained AGENTS.md, three or four delivered features and a designated successor. Lead: week one about two hours, weeks two to four about five, month two about three, month three about five including preparation.

**Why the 90-day curve is shaped that way.** The first thirty days produce almost no measurable productivity: the champion is learning, the lead is classifying, the manager is deflecting premature metrics. In the second thirty, cycle times improve, quality holds and reviewers find agent PRs easier to review because the descriptions are more structured. In the third, other engineers join, AGENTS.md grows, the journal fills and yellow projects start moving. The curve is roughly exponential, so measuring at thirty days disappoints and at ninety shows the picture.

---

**The outer loop's own kill signals.** The loop gets kill signals the way Chapter 8 gives them to codebases. Four are enough: the same diff applied and then reverted across iterations; budget burning while the queue does not shrink; the same failure surfacing a third time; any iteration that touched the gate. Any one means stop: read the journal, fix the cause, then relaunch. A loop restarted on hope is a loop you have stopped controlling. Appendix B.6's morning-review block carries the same four checks.

### Appendix A - For managers {#deep-dive-appendix-a}

**Tier routing, the two measured points.** Anthropic's advisor pattern pairs a cheaper executor with a stronger model on call. Sonnet with Opus as advisor scored 2.7 points higher on SWE-bench Multilingual than Sonnet alone, at 11.9% lower cost per task. Haiku with an Opus advisor scored 41.2% on BrowseComp against 19.7% solo, trailing Sonnet solo by 29% in score at 85% lower cost per task. Right for the mechanical tiers of the loop, wrong for research. *Source: Anthropic, "The advisor strategy," Apr 9, 2026. Caveat: vendor benchmarks on the vendor's own models; per-task figures, not a general ratio.*

**Cache-first layout, tool tax and masking.** Cache-first layout cut API cost by 41% to 80% on more than 500 agent sessions across three providers (Lumer et al., Jan 31, 2026). The tool-definition figures are under Chapter 1, the masking result under Chapter 6.

**The bounding heuristic, long form.** Cost per engineer per month is bounded by what the team would otherwise spend on similar tooling (IDE licenses, code-intelligence platforms, AI-coding subscriptions) plus a fraction of a senior engineer's hourly time saved per week. Run it with your tooling stack, loaded hourly cost, an honest hours-saved estimate and the vendor's quote; break-even lands quickly when the agent saves even a few hours a month per engineer.
