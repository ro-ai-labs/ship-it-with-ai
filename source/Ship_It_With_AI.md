# Ship It With AI

### A Field Manual for Agentic Software Delivery

**Mihai Cvasnievschi**

---

> The agents write the code.
> You understand the problem.
> You remain accountable for the judgment.

---

## Contents

**Prologue** - Ten thousand dollars a week

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

## Ten thousand dollars a week {#nine-seconds}

In July 2026 a team of three senior engineers called Slopfix reached the front page of Hacker News with an unusual offer: "One week. Three senior engineers. $10,000." The job is not to write code. It is to delete it. They take codebases built with coding agents and cut them back to something a team can maintain, paid in proportion to how much of an agreed line-count reduction they deliver.

Their diagnosis fits in one sentence: "This happens to every vibecoded project past a certain size: the agent stops seeing the whole picture and starts duplicating code instead of finding it." Nobody deleted a database and nothing went rogue. The agent did what it was asked, one task at a time, until "adding a feature now takes days and breaks two other things." Their example of the cleanup: "the fourteen date formatters become one."

The twist is in their own FAQ: "Yes, we use Claude Code too. On a very short leash." The same kind of agent that produced the mess is the one removing it. What differs is the structure around it: a written list of what the app does, screen by screen, before anything is cut; senior engineers who decide what stays; and, among the deliverables, a CLAUDE.md, lint rules and CI checks. In their words, "the agent doesn't get a vote."

*I use Slopfix as a public illustration of a failure pattern, not as an audited case study. The source and its limits are in Appendix C.*

---

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
- **Process has a cost.** Start with the native agent and the team's existing controls. Add planning, skills and reviewers where the task needs them; Chapter 4's six phases name functions, not six compulsory documents or approval stops.

Workflow advice was reviewed on October 23, 2026; other tool-specific claims retain their stated dates. The load-bearing claims and their limits are in Appendix C. Meaningful updates are in the [changelog](/changelog/).

**How to read it.** It is written for the senior engineer, staff, principal or tech lead who will run this practice on a real team and defend it upward; anyone who ships software with AI can follow. Read sequentially for the full argument, or choose a route that ends in an inspectable result. Appendix D holds extended evidence and its limits.

| Immediate goal | Route | Output |
|---|---|---|
| Understand the approach | Prologue → Chapters 1-3 | A capability comparison and the controls/workflow your tasks need |
| Prepare an unfamiliar repository | Chapters 2 → 7 → 6 → 8 | A reviewed map, useful instructions and task prerequisites |
| Deliver one change | Chapters 3 → 4 → 5, with the [Wire pack](/companion/wire-v1.zip) | Accepted behavior, verification evidence and production handoff |
| Run a team pilot | Chapters 8 → 9 → Appendix A | A bounded pilot, measurement card and expansion/stop decision |

---

# Part I - Architecture

> *The control of capability: what the agent can know and do.*

---

## Chapter 1
## What an agent is

*By the end you can inspect a contemporary coding agent through nine recurring capabilities and compare how two systems implement or supply them.*

**TL;DR**

- A coding agent is a model inside a harness. The nine primitives below are a practical inspection framework, not a universal anatomy theorem.
- A capability can be built in, external, absent or implemented differently. Those differences, the sandbox above all, affect the controls you need.
- Inspect the harness and the model's fit for your tasks. For any new agent, ask one question per primitive, then test the combination.

---

### What is a coding-agent primitive? {#what-is-a-primitive}

**An agent is a model plus a harness, and the harness is a small, recurring set of parts.**

Contemporary coding agents repeatedly expose the capabilities below, though their packaging and availability differ. Here, "primitive" means a useful capability to inspect, not a requirement that every product ship it as a separate configurable bundle. Each card ends with a question; "absent" and "provided externally" are valid answers.

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

*Figure: The primitives and the harness as an inspection framework. Compare the agent-level decision layer with actual OS-level enforcement and its covered routes. Inspect team-written and agent-written memory separately, and check effort settings and retained reasoning in the selected model/client. A capability can be absent or supplied externally; a subagent is another constrained agent instance when the harness provides it.*

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

**What it is: two controls shipped as a pair - the agent's own rules and the operating system's enforcement.**

The agent-level decision layer checks the tool requests it covers against allow / ask / deny rules. Some modes add a model classifier for eligible actions after explicit rules are resolved. Injection can mislead that classifier or exploit permitted actions and gaps in coverage; it cannot simply persuade a correctly enforced deny rule to disappear. The OS layer refuses prohibited system calls from the processes it actually isolates, regardless of the agent's reasoning. Check which tools and subprocesses sit inside that boundary. Neither half is enough alone.

*Ask: What permission model does it ship, and what OS sandbox does it default to?*

---

### Skills

**What it is: packaged instructions the agent loads only when a task needs them.**

A skill is a chunk of markdown - the team's way of writing a Spring Boot service, say - loaded when a task needs it. Descriptions can occupy context before invocation; the full instructions load when used, and may remain for the session. Keep triggers specific. Specialized knowledge can help; a general procedure the agent already follows can add cost without improving the result.

*Ask: Are skills loaded on detection, or always?*

---

### Plugins

**What it is: a bundle of skills, tools, hooks and commands, installed with one command.**

The plugin is the unit of distribution: one team's PR-review workflow becomes another team's one-line install. Start with the native agent; add a plugin for a capability or a measured improvement you need. The marketplace is also a supply-chain surface, the npm of agentic coding. Appendix B.10 checks both trust and value.

*Ask: Is there a plugin marketplace, and how do you vet what is in it?*

---

### What is MCP? {#what-is-mcp}

**What it is: the Model Context Protocol, a specification for how agents talk to external systems** - Jira, Postgres, GitHub, your data warehouse.

An MCP integration can be reused across compatible clients. Check the negotiated protocol version, capabilities, transport and authentication: saying that two products support MCP does not establish that every server works unchanged with both.

*Ask: Does it speak MCP, and how good is the integration?*

---

### Memory {#memory}

**What it is: what carries over from one session to the next, in two halves.**

The team writes the first: project instruction files such as AGENTS.md. Discovery, scope and precedence depend on the client; some require configuration or explicit loading (Chapter 6). The agent writes the second for itself: preferences, corrections and decisions it cannot re-derive from the code.

*Ask: Does it read a team memory file at session start, and keep memory of its own?*

---

### Effort {#effort}

**What it is: how hard the model thinks before it acts - the newest primitive, and it earns its place on leverage.**

Where the model and client expose effort controls, compare the available settings on representative tasks. Effort can affect cost and quality: a lower setting may miss needed investigation, while a higher one may add reasoning the task does not need. Names do not transfer between models. Compare settings by task or phase rather than assuming one level suits the whole session (Appendix B.9).

*Ask: What effort levels does it expose, and does the reasoning survive between turns?*

---

### Subagents

**What it is: constrained child instances of the agent itself.**

The orchestrator hands a subagent a bounded task with scoped tools and gets a result back. A fresh context isolates the work; a fork can share the parent's history. Each worker adds usage, startup and coordination costs, partly affected by caching. Delegate sizeable, self-contained work when the expected gain exceeds those costs; keep quick or tightly dependent work in the main agent. Chapters 4, 5 and 7 show where it can pay.

*Ask: How does it expose subagents - is parallel dispatch first-class?*

---

### The harness

**The model sets the ceiling; the harness decides whether you reach it.**

The harness is the runtime around the model: it formats your request, manages the window, dispatches tool calls, feeds results back and decides when the work is done. The loop itself is simple; the surrounding controls matter. Inspect language fit, license, plugin ecosystem, sandbox enforcement and audit posture, then evaluate the model and harness together on your own work.

---

### Compare the implementations

**The framework makes differences visible; two implementations do not prove a universal architecture.**

> **Demonstration: one prompt, two agents.** While preparing this manual I pointed Claude Code at the source of two other coding agents in two terminal panes: Codex CLI (Rust, maintained by OpenAI) and opencode (TypeScript, an independent team). Both are open source and share no code. Same prompt in each: map the agent loop, tools, permission gates, sandbox and plugin model, citing files and line numbers.
>
> About four minutes later, with no human correction, both returned the same shape: an agent loop, a tool registry, a permission gate, a sandbox, a plugin model, MCP support, a subagent dispatch path. Different languages, files and names. The clearest divergence was the sandbox: Codex implements real OS-level isolation, so the kernel itself refuses what the agent is not authorized to do; opencode implements soft confinement, path validation and permission prompts with no kernel-enforced boundary.
>
> *Limits: an author-run comparison of two repositories illustrates the framework. It does not establish that every agent has all nine capabilities or that the implementations are equally effective.*

---

### Sandbox posture is a governance choice

**A vendor's choices about primitives are governance choices.**

Source and runtime probes can show what a sandbox actually covers. Codex CLI enforces an OS sandbox by default on Linux and macOS; Claude Code ships an opt-in shell sandbox; opencode needs external OS isolation. Defaults are versioned, so check yours.

What the sandbox actually covers matters more than what the vendor intended. You are the one choosing, and Chapter 2 turns the choice into five layers.

---

### When it breaks

- **A rule the agent consults is not a wall.** Injection can mislead model judgments and exploit permitted actions or coverage gaps. Enforced deny rules and the OS boundary protect the operations they cover (Chapter 2).
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

*By the end you can document and test a repository's intended control boundaries, identify uncovered routes and assign the next fix.*

**TL;DR**

- A prompt is a request, not a control. Destructive actions need layers the agent cannot talk its way past: permissions, sandbox, secrets, hooks and telemetry.
- Least privilege is the spine and redundancy is the control. A sandbox bounds the processes it actually covers; other tools need their own controls, and every layer can have bugs.
- Keep production credentials out of the session, and send the agent's pull requests through the same gates as everyone else's.

---

### What are the five layers?

**A prompt is a request. A control is something the agent cannot talk its way past.**

On April 24, 2026, PocketOS, a small car rental SaaS, lost its production database to a coding agent (Cursor powered by Claude Opus 4.6). During a routine task the agent hit a credentials mismatch, found an API token for Railway, the company's infrastructure platform, and invoked Volume Delete. The call took nine seconds. Afterward the agent wrote: "I guessed instead of verifying. I ran a destructive action without being asked." Railway says the legacy API path cascaded the delete so the backups looked gone, and that offsite disaster backups let it recover the data; accounts differ on how long that took. Appendix C has the sources.

PocketOS had a natural-language instruction, which is weaker than layer one. Three lessons get quoted from it, and all three are wrong:

- "The agent ignored its instructions." It did, as agents sometimes do; a prompt is never a hard control for a destructive action.
- "AI agents are unsafe." So is any automation that can reach production without enforced controls.
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
| 1. Permissions | Covered actions the rules or classifier deny | A path is permitted, missed or misclassified | Could have, if a rule gated destructive calls |
| 2. Sandbox | Prohibited access by isolated processes | Off, bypassed through an uncovered tool, or defective | Could have, if it covered the destructive call |
| 3. Secrets | The agent holding a credential | A secret sits within reach | Could have: no production token in the session |
| 4. Hooks | Covered actions a blocking policy rejects | A rule is missing, editable or fails open | Could have: forced human approval |
| 5. Telemetry | Nothing; it detects afterwards | Nobody is alerted or responds | No; a tested alert and response could shorten detection and recovery |

A preventive control could have broken the chain only if it covered the destructive operation. Telemetry serves detection and response, not prevention. The public record does not establish a complete configuration audit. A second 2026 incident, at DataTalks.Club, involved Claude Code running `terraform destroy` against a stale state file. Both accounts motivate testing destructive-operation approval, credential scope, state and recovery rather than assuming those protections exist.

---

### Layer 1: Permissions

**Permissions answer one question: is this agent allowed to do this, right now?**

Choose a permission mode for the work's risk, with explicit deny or approval rules for consequential actions. A classifier can reduce prompts for eligible actions; it supplements the runtime's rule checks. Cover each available route, including native file tools, shell commands and connected services. The policy needs as many clear, tested rules as that coverage requires; a shorter list is not inherently safer.

AGENTS.md explains the team's intent; it does not replace enforced permissions. Test an allowed and a prohibited action through the relevant tools, and recheck after configuration or version changes.

---

### Layer 2: Sandbox

**The kernel does not listen to the agent's reasoning, so injection cannot talk its way past it.**

For routine repository work, start by permitting needed reads, limiting writes to the assigned workspace and temporary files, and restricting network access to what the task requires. Verify coverage: Claude Code's built-in sandbox wraps shell commands, while its native file tools, MCP servers and hooks run outside it. Native Windows commands are unsandboxed; WSL2 is a supported sandbox route. Whole-agent isolation may be needed when a tool-level boundary is insufficient.

Investigate legitimate failures before widening access. Grant the smallest justified exception and check it; do not turn repeated denials into a blanket allow. Defaults and supported platforms vary by agent and version (Chapter 1).

---

### Layer 3: Secrets

**The safest credential is the one the session never held.**

Do not commit `.env` files or expose production credentials to the agent process. Keep runtime secrets in a vault with access scoped to the application or task. A shell sandbox's deny-read list protects only the reads it covers: in Claude Code it does not block the native Read tool. Apply file-tool permissions too, and account for inherited environment variables, MCP servers and hooks. Where secrets must be inaccessible to every route, keep them outside the agent's environment or isolate the whole process.

---

### Layer 4: Hooks

**Hooks are the precision instrument: a programmable gate for the categories your team cares about.**

A hook is code that runs before the agent executes a given kind of action (pre-tool-use) and, against your rules, allows it, asks for confirmation or blocks it. Off-the-shelf plugins ship a baseline: secret leaks in diffs, SQL injection patterns, hardcoded credentials.

A policy hook needs protected configuration, an explicit blocking response and failure behavior that blocks the action. Test a missing, crashing or timed-out hook. Claude Code command and HTTP hooks can otherwise fail open; current versions support `onFailure: "block"` from v2.1.295 (Appendix C).

Your own rules go on top: any change to currency-conversion logic needs explicit approval; any commit touching the customer table needs a security reviewer. Reach for a hook when permissions are too coarse and the sandbox too blunt.

---

### Layer 5: Telemetry

**The first four layers aim to prevent; telemetry supports detection and response. Test the alert and the response, not just the log.**

Record tool-call metadata and policy outcomes in a central store the security team owns. Capture arguments or results only where needed, with secrets and sensitive payloads redacted, access controlled and retention defined. Check what the harness actually exports; metrics alone are not a complete action log. Then "which sessions touched the payments service in the last thirty days" can be a query rather than a grep through local histories. Watch for:

- an edit outside the assigned task
- calls to hosts off the allowlist
- repeated permission denials: a bug in the rules or an injection attempt
- production credentials in context

---

### Injection arrives through the work itself

**Treat everything the agent reads as untrusted text, and do not count on the agent to spot the attack.**

Anywhere the agent reads natural language is a surface: a Jira ticket whose acceptance criteria say "ignore all previous instructions"; an outside contributor's PR comment with an instruction hidden in a review note; an error message from a flaky third-party test; a harmless-looking repository whose planted error nudges the agent to run a "fix" that pulls in its real payload. I have watched an agent follow an instruction buried in a pasted log file because the operator did not think of a log file as untrusted input.

Constrain what the agent can do regardless of what it has read. An enforced sandbox blocks prohibited access on covered paths; a protected, blocking hook can gate the categories it recognizes. Check the routes neither covers. A poisoned AGENTS.md can change the agent on every session start, one more reason it is reviewed like code (Chapter 6).

Repository configuration is code that runs. Before trusting a cloned repository, read its agent settings, hooks, MCP servers and editor tasks. Microsoft's August 2026 analysis of the ChainDrop worm found it writing `.claude/settings.json` and `.vscode/tasks.json` into repositories so that later agent or editor activity would restart the payload. If you find such a change, stop running sessions and background jobs, revoke the credentials they could reach, preserve the evidence and involve whoever owns incidents before cleaning up. In CI, never run an agent with secrets or write access over untrusted pull-request content.

---

### Beyond the five

**Two ordinary practices catch what the layers do not.**

- **Environment separation.** The agent does not hold production credentials by default. Production actions go through a separate gate - a human approval, a CI pipeline, a deploy script - that the agent triggers but does not execute end to end.
- **Protected branches, CODEOWNERS and CI policy.** The agent opens pull requests like any contributor; make sure its PRs flow through these rules, not around them.

---

### In the loop

**The rigor lives in the layers below execute; execute just runs the work.**

Before Chapter 4's execute phase, establish which permission rules, hooks and sandbox restrictions cover each tool. Do not assume one sandbox protects all file writes or connected services. A blocked action needs diagnosis and, where justified, an authorized policy change; asking the agent to try another route is not the fix.

---

### When it breaks

- **Every layer is code, and code has bugs.** In mid-2026 a red team disclosed two critical zero-click escapes of one vendor's kernel-backed sandbox (patched), and a permission check once skipped its deny rules on very long command chains. That is the argument for five layers.
- **A log alone does not ensure a response.** The PocketOS accounts describe a recorded deletion. They do not establish a tested alert-and-response path that could have prevented the loss.

---

### Do this Monday

*Create a control record for each intended boundary. Monitoring is evidence of detection, not evidence that a prohibited action is blocked. A separate subagent context is not a separate authority, and blocking one route does not block another: OpenAI's managed configuration notes that disabling Browser Use alone does not stop Computer Use driving the browser as a desktop app.*

| Record | What to write |
|---|---|
| Intended boundary | The operation that must be prohibited or explicitly approved |
| Covered routes | Shell, native file tools, MCP and other connected services, signed-in browser sessions, desktop control and subprocesses; name exclusions |
| Enforcement | Configuration location, protection against unilateral edits, installed version |
| Verification | A benign probe, expected denial or approval, actual result and evidence |
| Failure behavior | What happens when the control is absent, cannot start, crashes or times out |
| Detection and response | Alert recipient, expected response and a tested alert; separate from blocking |
| Owner and date | Who checked it, when, and when it must be rechecked |

- [ ] Choose one consequential boundary in a repository and fill the record for every available route.
- [ ] Use harmless fixtures and a test environment to confirm an allowed action and the intended denial; do not probe destructive production actions.
- [ ] Test control failure and alert delivery. Record uncovered routes as gaps, with an owner and next action.
- [ ] Finish when another engineer can reproduce the probe and interpret its result. Recheck after version, policy or tool changes.

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

- Agents make plausible code cheaper to produce. Domain clarity, useful decomposition and evidence before "done" help turn that output into useful changes.
- Match the workflow to uncertainty and risk: direct work for clear changes, a short plan for dependencies, explicit outcomes and review for consequential work.
- Setup and review have a cost; measure whether the work improves. Start with a useful constraint, not a perfect setup.

---

### The constraint moved

**Cheaper code generation makes the surrounding engineering decisions more visible.**

Agents make producing plausible code much cheaper. That exposes the constraints around it: deciding what should change, supplying missing context, integrating the result and establishing that it works. Different teams have different bottlenecks; typing speed was never a complete account of software delivery.

Teams that treat the agent as a code generator let it type, handle everything else as before, and spend more time fixing output than the typing saved. Teams that ship well formulate the work so the agent can execute it correctly. Vague specifications produce guessing, and guessing produces output that looks right and is not.

The people building the models agree. In July 2026 an Anthropic engineer opened a field guide to Claude Fable 5 by calling it "the first model where I find the quality of the work is bottlenecked by my ability to clarify its unknowns."

---

### Three habits

**All three are formulation, not generation.**

- **Domain clarity before code.** The agent does not know your business, your conventions or why the codebase looks the way it does. Load that context first: AGENTS.md, skills, the research phase.
- **Decomposition where it helps.** Split a large change into coherent steps with clear dependencies. A quick, well-understood edit can stay one task.
- **Evidence before "done".** The agent can say the change is complete and be wrong. Choose checks that exercise the intended result: a regression test, build, lint, rendered page or a direct content check. The check should fit the change.

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

**Use the least process that makes the outcome clear and the risk reviewable.**

Start with the native agent and your normal repository checks. Size the work before adding a workflow:

- **Clear and contained:** ask for the change directly, with a focused check. A typo or familiar rename rarely needs a separate plan.
- **Unclear or dependent:** inspect the relevant code, settle material questions and write a short plan. Keep coupled steps together; record decisions the next step needs.
- **Risky or unfamiliar:** define the expected behavior, failure cases, permissions and human decisions explicitly. Add deeper investigation and independent review where a mistake would matter.

File count is a clue, not a threshold. A one-line authorization change can deserve more scrutiny than a mechanical rename across fifty files. Reversibility helps recovery; it does not make a behavioral bug harmless. The six functions in Chapter 4 give you a checklist of what must be covered, not paperwork to generate for every task.

---

### Two teams, one quarter

**One team's investment paid back over a quarter; your timeline needs measurement.**

The clearest case I have seen: two teams at the same company, in adjacent areas of the same product, using the same agent.

Team A turned the agent loose immediately and celebrated the early velocity. By month three they were shipping at roughly the pre-agent baseline, with higher defect rates and visibly drained senior reviewers.

Team B spent month one on the practice: AGENTS.md drafted and iterated, skills written for the team's patterns, hooks configured. They shipped no agent-led work that month. By month two they were back at baseline velocity. By month three they shipped at noticeably better quality and velocity than before the agent.

The observation motivates measuring setup, delivery, review and defects together. It does not establish that every team should lose its first month or that this workflow caused the difference.

| Case note | What this account establishes |
|---|---|
| Provenance | Author-reported, anonymized engagement |
| Evidence | The qualitative account above; no underlying task counts or time series are published here |
| Comparison | Adjacent teams before and after adoption, without controlled task selection |
| Limitations | Team differences and the combined interventions prevent causal attribution to one agent or method |
| Transfer | Measure your own baseline and costs; expand when the observed outcomes justify it |

---

### Start small

**The practice does not need to be perfect to pay.**

A few useful lines in AGENTS.md can prevent a repeated mistake. A short note can settle an unfamiliar task. Teams that build the perfect workflow before running it get stuck, because there is always one more rule, skill or hook to add.

Write the few useful constraints the first task needs, run bounded work through the agent, and add rules justified by observed failures or a specific risk.

---

### When it breaks

- **One workflow for every task.** Ceremony can slow a clear edit; missing investigation can sink an unfamiliar one. Run the loop test first.
- **Waiting for a promised quarter-end payoff.** Track outcomes from the start; change or stop a pilot whose costs and failures are not justified.

---

### Do this Monday

- [ ] Size the next task with the loop test: direct work, a short plan, or deeper investigation and review.
- [ ] Write one sentence saying what "done" means and which check will show it. Add only the context the agent is missing.
- [ ] Run it with the native agent first. Add a rule, skill or plugin for a documented need, missing capability or repeated failure, then check whether it helped.

---

### Go deeper

- **Templates:** [Appendix B.2](#template-b2), the AGENTS.md skeleton; [B.3](#template-b3), the six-phase loop checklist.
- **Deep dive:** [Appendix D, Chapter 3](#deep-dive-chapter-3) - the Fable 5 unknowns frame, the METR trial and its caveat, and the February to April 2026 regression.
- **Sources:** Appendix C.

---

## Chapter 4
## The six-phase loop

*By the end you can cover the six functions of a sound change, choose how much process each needs, and name the gates that remain yours.*

**TL;DR**

- Six functions: research, plan, execute, review, verify, ship. They can share a step or an artifact; the task determines which need an explicit gate.
- When the approach is uncertain, review the plan before execution. A few minutes reading it can save an afternoon of unwinding the wrong change.
- Ship is a normal pull request with the evidence attached. There is no AI lane.

---

### What is the six-phase loop? {#what-is-the-six-phase-loop}

**Cover the functions; size the ceremony to the work.**

The six phases are research, plan, execute, review, verify, ship. On a clear edit, one native-agent turn and the normal PR can cover them. On an unfamiliar banking feature, a note, a reviewed plan and separate checks make the work legible. A phase can be packaged as a skill; it need not be a separate skill, document or approval stop.

Superpowers, GitHub Spec Kit, BMAD and team-built collections package parts of this discipline differently. Superpowers is optional. Compare the installed version with the native agent on your tasks before adopting its extra process; old-version benchmarks do not establish the value of today's version on your model. Appendix B.10 gives the comparison, and Appendix D the evidence reviewed for this edition.

```
   +--------+    +------+    +---------+    +--------+    +--------+    +------+
   |Research|--->| Plan |--->| Execute |--->| Review |--->| Verify |--->| Ship |
   +--------+    +------+    +---------+    +--------+    +--------+    +------+
       ^             ^            ^
       |             |            |
   missing facts   changed     failed check?
                  approach    repair Execute
```

*Figure: The six-phase loop. An implementation defect returns to Execute and the affected checks; a changed approach returns to Plan; missing evidence returns to Research.*

| Phase | Evidence when needed | Human decision | Failure caught |
|---|---|---|---|
| Research | Relevant facts and open questions | Resolve material unknowns | Missing context |
| Plan | Approach, dependencies and checks | Review uncertain or consequential choices | Bad decomposition |
| Execute | Diff and relevant check results | None or light | Implementation drift |
| Review | Findings against intent and standards | Normal owner or senior review | Wrong or weak code |
| Verify | Relevant test, build or behavior evidence | Confirm enough evidence for the risk | Behavioral failure |
| Ship | PR with evidence trail | Normal PR process | Process violation |

**The loop stands on a well-defined expected outcome.** The agent can build almost anything you describe, but it cannot know which thing you meant. Research surfaces what is undecided, you settle it, the plan turns it into checks, and verify measures the result against it. Skip that and "done" is whatever the agent decided.

---

### The feature

Here is one feature, followed through every phase: add a `priority` field to a `Wire` record in a banking service. The narrative below is an author-reported example; its original code and run logs are not published. The [Wire companion source](https://github.com/ro-ai-labs/ship-it-with-ai/tree/main/companion/wire) and [versioned runnable pack](/companion/wire-v1.zip) are a clearly labeled synthetic worked example for practice, not evidence of the original engagement. The small Python model makes the decisions inspectable without claiming to implement production banking infrastructure.

Priority is one of low / normal / high / urgent and defaults to normal. The urgent flag triggers a separate compliance-review queue. The companion settles missing and null priority, older clients, unavailable queues, audit contents and retry behavior in an acceptance table before code. Those are explicit teaching decisions, not claims about an undisclosed client's policy.

---

### Research

**Research produces a note, not code - and its open questions are yours to settle.**

I asked the agent to read the codebase and write a research note. It named four files I would not have found in an hour of grepping:

- the `Wire` record itself
- the migration directory
- the compliance-review-queue service
- the audit-log emitter

It also raised an open question: should priority be an enum or free text? The regulator's spec uses free text in some documents and an enum in others. I picked enum. That was not a detail - it defined the target every later phase was checked against.

A research note is as short as the task allows. For unfamiliar work it covers:

- the files that will be touched
- the conventions those files follow
- the existing tests that cover the area
- related concepts elsewhere in the codebase
- open questions where a human has to decide

Research grounds the approach in the real code instead of the agent's first guess. For a familiar edit, reading the relevant function may be enough; the banking example needed a durable note because the domain decisions had to survive hand-offs.

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

- **Every task names the area, the change, its dependencies and the check that will assess it.** Keep steps small enough to review and recover when one fails.
- **It names the relevant checks and tests to add or update.** A behavioral fix usually needs a regression test where feasible; a prose correction may need only a content or rendering check.
- **It states what "done" means for the whole change**, not only per task. That is the outcome verify will check.

Where the task needs plan approval, read it before execute: challenge vague, oversized or wrongly ordered tasks, add what it missed and remove what is out of scope. Clear work already authorized by the request need not stop for a second permission ceremony.

The review takes a few minutes. It saves an afternoon when the plan was wrong and you would have found out during execute, where it is much harder to unwind.

---

### Execute

**Delegate independent work when the gain exceeds the coordination cost.**

The original account reported six concurrent workers, despite the dependency between tasks four and five. Without a preserved handoff record, that account does not establish that the dependency was satisfied; it describes a coordination risk, not a schedule to copy. The companion makes the safe schedule visible: settle the priority/API/audit contracts first; implement independent areas against those contracts; integrate dependent routing and verify the whole behavior afterward. One implementer can follow the same waves without subagents.

The sixth, the audit-log emitter, also had a passing test - but the test was wrong. It asserted the old log format. Green, and wrong. Chapter 5 picks up how that got caught.

Each worker receives the context it needs, makes its scoped change, runs the relevant check and reports back. Fresh workers isolate exploration; forks can reuse established context. Neither removes the need to communicate shared contracts accurately.

Isolation is not a silver bullet. The rules that keep it working:

- **Keep one writer per overlapping area.** Run dependent changes in order. Different files can still depend on the same schema, contract or decision.
- **Make delegation earn its cost.** A sizeable, self-contained investigation or implementation can benefit from another context. A few tool calls or tightly coupled steps usually belong in the main agent; startup and coordination can exceed the time saved.
- **Read the orchestrator's hand-offs with skepticism.** It still holds a summary of every task, and an imprecise summary of task one can lead task four to contradict it. I have watched six subagents produce mutually inconsistent edits for exactly this reason.
- **Record material deviations where the next reader will find them.** A note, task report or PR can carry changed assumptions, uncovered edge cases and decisions. Use a separate implementation-notes file when the work and hand-offs justify it.

When a check fails, diagnose it before retrying. Repair a local implementation defect and rerun the affected checks; revise the plan if the approach or a dependency changed, and research again if evidence is missing. Ask the owner when a material domain decision or new authorization is needed. Repeating the same attempt without new evidence is not recovery.

---

### Review and verify

**Review checks the diff against the spec; verify checks the behavior against the outcome.**

On the wire, review challenged the audit-log assertion and the migration's recovery plan. An absent down migration is a defect only if the project's recovery policy requires one; backward-compatible deployment, roll-forward repair or tested restoration can be valid alternatives. Verify then assesses the chosen behavior and recovery approach. Chapter 5 shows the inadequate assertion directly, and the companion lets you run the red and green stages.

---

### Ship

**Ship is a normal pull request. There is no AI lane.**

The agent commits with a structured message, pushes the branch and opens a pull request whose description says what changed, why, how it was verified, what risks remain and who is tagged to review.

On the wire, the PR carried the research note, the plan, the per-task reports, both reviews and the test evidence. A senior reviewer spent eleven minutes on it and asked one question: should the urgent flag be observable in the metrics dashboard? I had not thought about it. Approved, merged.

That PR is an artifact the team knows how to review, but merge is not the end of delivery. Complete the production handoff through the existing release process:

| Question | Required handoff |
|---|---|
| How does it reach production? | Deployment order, compatibility with existing data and clients, responsible release owner |
| What confirms success? | Observable behavior or operational signal, including urgent routing and audit priority |
| What triggers intervention? | A named failure condition and the person who receives it |
| How is recovery handled? | The tested rollback, roll-forward or restore approach appropriate to this change |
| What follows release? | A bounded observation window, its owner and the decision to close it |

The companion fills these fields and distinguishes simulated checks from staging and production evidence. The agent feeds your delivery process; it does not replace its accountable owners.

---

### What it costs in time

**Budget agent time, investigation and human review separately.**

In my experience with bounded tasks, a small feature can take twenty to thirty minutes through the loop, a medium one around an hour and a large one a few hours. These are planning examples, not delivery promises or a measured comparison with manual work. Unknowns, environment failures, test duration and review availability can dominate the time; measure them on your own tasks.

The wire feature took ninety minutes from "let's add a priority field" to merged code. The difference is the regulated context: a 3,400-test suite, a staging smoke test and a contract diff for the regulator. Small in scope is not small in ceremony.

If a small feature takes three hours, inspect where the time went and whether each step changed a decision or reduced a material risk. Some checks are necessary; others may be ceremony that no longer earns its cost.

---

### When to run less of it

**A function needs coverage, not necessarily a separate phase.**

Chapter 3's test tells you when the loop pays at all; inside the loop the same accounting applies.

One team I watched ran for most of a year on what looked like half the loop: research was a comment thread, the plan was three bullets in the PR. It worked because the functions had moved into the team's walls - a small senior team that built the codebase, a strict CI suite and a serious PR culture. The lesson is to name what covers the function. Do not produce another document or agent review when the existing step already does the job.

For a contrasting small change, the companion illustrates a proportionate workflow for a help-text typo: find the string, confirm its scope, edit it, inspect the diff and displayed text, then use the normal PR and release process. Research, planning, execution, review, verification and shipping are covered in a brief interaction. No additional agent or plan file is needed to make that work inspectable.

---

### When it breaks

- **The gates are requests, not walls.** Skill instructions request discipline. Required controls belong in protected runtime policy or server gates; a hook helps only on the routes it covers (Chapter 2).
- **Parallel subagents on overlapping files** produce inconsistent edits. Re-scope by file or module, or run the tasks in sequence.
- **Long sessions drift.** Repeated questions or forgotten constraints can signal stale context, conflicting requirements or missing information. Diagnose the cause, then use Chapter 6's handoff practices where appropriate.

---

### Do this Monday

- [ ] Pick an unfamiliar or consequential task and settle its material unknowns before implementation. Keep a note if the decisions need to survive hand-offs.
- [ ] Read the approach and checks: dependencies are clear, scope is bounded and there is a "done when" line.
- [ ] Execute directly unless sizeable independent work justifies delegation. Record material deviations.
- [ ] Ship through the normal PR process with the evidence the reviewer needs.
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

- Review intent and code quality. Your normal human review remains; add agent reviewers where the risk and measured benefit justify them.
- A clean agent diff can still fail at intent, so read it from the outside in: the shape of the change, then the tests, then the lines.
- A green suite the agent wrote is evidence, not proof. Check its assertions against intent and protect the gates from being weakened to pass.

---

### Who checks what

**Cover both review lenses and the behavior; the number of reviewers can vary.**

| Check | Reads | Asks |
|---|---|---|
| Intent and spec lens | Request, relevant decisions, diff | Does this match the required business behavior? |
| Code-quality lens | Diff and relevant surrounding code | Is this correct and maintainable by the team's standards? |
| Human read | Diff-stat, tests, boundaries, new names | Is the business rule right? Does it fit the architecture? |
| Verify | Checks suited to the change and its risk | Does the behavior meet the agreed outcome? |

One human review can cover both lenses. For risky or unattended work, a fresh agent can find gaps before that review. Separate reviewers need distinct questions and enough context to judge the change; two sequential agents are an option, not a requirement.

---

### The wire, continued

**A suite that is happy can still be wrong.**

Chapter 4 left the audit-log emitter with a test that was green and incomplete. Review found that the assertion omitted the newly required priority, and asked for a documented migration recovery approach. The latter is a project decision, not a universal requirement for a down migration. The implementer addressed the findings and reran the relevant checks.

In the synthetic companion, the old test checks that one `wire.created` event exists and names the wire:

```python
self.assertEqual(len(service.audit_events), 1)
self.assertEqual(service.audit_events[0]["type"], "wire.created")
self.assertEqual(service.audit_events[0]["wire_id"], wire.wire_id)
```

Before reading on, ask: which new acceptance criterion could still fail while these checks pass?

The event can omit priority entirely. The stronger assertion observes the chosen value:

```python
self.assertEqual(event.get("priority"), "URGENT")
```

It fails on the defective implementation with `None != 'URGENT'`; including the normalized priority repairs it. Testing all four values also excludes a hard-coded URGENT fix. Run `python3 verify.py` from the [companion pack](/companion/wire-v1.zip) to observe weak-green, corrected-red and repaired-green. That model experiment does not establish the original banking system's behavior.

Back in the original banking engagement described here, verification included the full suite of 3,400 tests, a smoke test against the staging compliance-routing service and a diff of the API contract change for the regulator's review. The checks passed, and that evidence went into the pull request at Chapter 4's ship step.

---

### Review: choose the depth {#review-two-agents-then-you}

**That was the banking case's design, not the default for every change.**

Start with the team's normal review and relevant automated checks. Add an independent agent where the change's consequences, unfamiliarity or unattended execution warrant it. Use two distinct reviewers only when their different lenses find useful defects worth the extra time. Model behavior matters: Anthropic recommends fresh verifiers for Fable 5 long tasks, but warns that extra verifier scaffolding makes Opus 5 over-verify (Appendix D).

- **Scope findings to the task and real defects.** Broad requests to improve everything can turn review into repeated polishing and new abstractions.
- **Keep separate judgments independent.** Give a fresh reviewer the requirements, diff and relevant code, without the implementer's defense or an earlier reviewer's verdict.
- **Accept or rebut findings with evidence.** Track useful defects caught, false positives, review time and rework. A high rate of responding to comments does not show that the review improved the change.
- **Bound repair by value.** Fix supported findings, then run the affected checks. Stop when no material issue remains; another round needs a new concern, changed code or other evidence.

Findings carry a severity: critical blocks ship, important is fixed before ship, suggestions go in the PR description for the human reviewer.

---

### How do you review an agent-written diff? {#reviewing-agent-diffs}

**Read from the outside in: intent first, lines last.**

Any diff can contain a typo, an off-by-one or a forgotten edge case. An agent diff can also compile, pass lint and read like code your team would merge while failing at intent and context: a business rule that is plausible and wrong, the right code in the wrong layer, the code a good engineer would write for a slightly different task. Fluency is not correctness.

Start above the code, with time proportionate to the change:

1. **Diff-stat against the request or plan.** Does the shape of the change match the ask? An unexpected file deserves an explanation; it can be a necessary discovery or scope drift.
2. **Read the tests for what they assert,** not whether they pass. Green is the cheapest signal, and the one you already have.
3. **Check the boundaries your team wrote down:** forbidden patterns in AGENTS.md, layer conventions, dangerous modules. The agent crosses them confidently, in fluent style, so a violation looks clean.
4. **Grep every new name the diff introduces** that you do not recognize. The call that does not exist reads as plausibly as the one that does (Chapter 6 has the cross-check). For a new dependency, confirm the exact package and publisher, its license and advisories and what it runs at install, and read the manifest and lockfile together; an existing approved dependency may already do the job.
5. **Only now, line by line,** for business correctness and architectural fit.

For consequential or unfamiliar changes, an optional comprehension check can help: ask the agent to quiz you on edge cases, ownership and what breaks if an assumption is wrong. An unanswered question identifies something to resolve before approval. Use it when normal review has not already established that understanding. Appendix B.8 carries the read order and this optional check.

---

### Verify

**Verify measures the behavior against the outcome the plan defined.**

Verify asks whether the intended behavior works and what evidence supports that conclusion. Run the relevant tests, build, lint, behavior or visual checks. Add a regression test for a behavioral fix where feasible, using the failure case rather than copying the implementation into the assertion. Existing valid test output can carry forward when no relevant code or assumptions changed; a new phase name is not a reason to repeat a suite.

A reversible prose or configuration edit does not automatically need a permanent test file. Check the changed content, parser, build or rendered result as appropriate. A reversible change to permissions or money handling can still need substantial behavioral testing: reversibility is not a measure of bug risk.

For frontend behavior, prefer user-facing roles and labels over brittle CSS selectors, assert the resulting behavior and inspect rendered visual changes; semantic locators do not assess layout. Appendix D covers control-specific interactions.

---

### Can you trust the tests the agent writes? {#trusting-agent-tests}

**Green tests are evidence, not proof.**

They are evidence the change does what the test says, not that the test says the right thing, as the audit-log test showed. Coverage does not close the gap: it measures which lines ran, not whether anything meaningful was checked, and an agent optimizing a coverage gate writes tests that call the code and assert nothing of consequence. Characterization tests, Chapter 8's first fix for an untested codebase, lock in current behavior, not correctness, and preserve a bug as faithfully as a feature: a regression net while you migrate, never proof.

So review the agent's tests like its code, checking the assertions against the spec. A test written from the implementation agrees with the implementation; the assertion has to come from the intent.

The agent also optimizes the evidence it can see. On SpecBench, frontier agents saturated the visible tests while held-out scores stayed far lower; for Claude Code the gap was roughly 43 to 48 points across three search strategies. That is a warning about what the gate rewards, not a requirement to turn every PR into a benchmark. Apply the controls at the right boundary:

- **For ordinary changes:** review assertions against intent and diagnose failures before changing code or checks. A wrong test can need a legitimate, reviewed update; changing the assertion just to get green needs rejection.
- **Protect the team's gates:** keep required CI and security checks outside the agent's unilateral control. Hooks can block bypasses and require review for test or lint configuration changes while allowing authorized maintenance.
- **For evaluations or high-assurance work:** independently written held-out tests can detect overfitting. Sealing answer-bearing git history and network access can prevent benchmark leakage. Ordinary development often needs both history and documentation; restrict them only when that boundary serves the task.

---

### When the toolkit does the looking

**Review agents are a filter in front of human judgment, never a substitute for it.**

A team I worked with installed a full review toolkit: agents for swallowed exceptions, weak tests, security issues and stale docs. It caught real bugs week after week, the senior reviewers learned to trust the green checkmarks, and within a quarter their fifteen-minute reviews had become three-minute scans. Nobody decided that; attention drifts away from work that appears to be done.

Then a PR that every agent had passed - tests green, no security findings, clean diff - applied a discount rule to the wrong customer tier and ran in production for weeks until a support ticket surfaced it. The toolkit had worked as designed: it removed the mechanical findings from human review, and the judgment drifted away with them. That is Chapter 9's uncalibrated delegator, at team scale.

The fix was a judgment floor, not a duration quota. Before approval, the reviewer should be able to explain the business rule, the consequential edge case, why the change belongs at this architectural boundary, and which evidence would reveal the most damaging plausible mistake. Review time and escaped defects are useful diagnostics. A short review can answer these questions well; a long review can still miss them.

---

### When it breaks

- **The read decays into a glance at checkmarks.** Review time and escaped defects can expose the drift; an optional comprehension check can reveal gaps before approval.

---

### Do this Monday

- [ ] Read your next agent diff in the order above. For an unfamiliar or consequential change, try the optional quiz and resolve what you could not answer.
- [ ] Open the last three tests the agent wrote. Do the assertions come from the spec or from the code?
- [ ] Check both intent and code quality. Try a fresh reviewer on a consequential change, then record useful findings, false positives and time before making it a default.
- [ ] Diagnose a failing check before changing it. Confirm required CI cannot be bypassed, and that legitimate check updates have a review path.
- [ ] Confirm the review answers the business-rule, consequential-edge, architectural-boundary and damaging-mistake questions. Track time as a diagnostic alongside escaped defects, not a quality quota.

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

- AGENTS.md is team infrastructure: short rules for documented needs and failures, reviewed like code and owned by one champion.
- Keep it concise and scoped: commands, key conventions, pitfalls and pointers. About 200 lines is a useful guideline, not a proven cutoff. The agent reads before it cites; you grep what it names.
- Context is working memory. One unit of work per session, durable state in files; when drift appears, diagnose the cause before compacting or restarting.

---

### What is AGENTS.md? {#what-is-agents-md}

**AGENTS.md is the team's agreement with the agent, committed in git.**

It is a Markdown file for project instructions. A compatible client loads it according to its own discovery and configuration rules; some clients need explicit loading. The text records what the team wants the agent to follow, reviewable in a pull request. It is the manually owned layer of Memory from Chapter 1, not an enforced permission policy.

### AGENTS.md vs CLAUDE.md: what's the difference? {#agents-md-vs-claude-md}

**The discipline is shared; loading depends on the agent and version.**

The shared filename does not imply identical loading. This compatibility summary was checked October 23, 2026; verify the installed version and effective context.

| Client | Filename and configuration | Scope and precedence | Inspect what loaded |
|---|---|---|---|
| Codex CLI | `AGENTS.md`; `AGENTS.override.md` takes precedence in a directory; fallback names configurable | Global guidance, then repository root toward working directory; closer instructions override earlier ones; combined size limit configurable | Ask for active sources and inspect session/TUI logs when auditing |
| Claude Code | `CLAUDE.md` default; direct `AGENTS.md` from v2.1.277 | Default AGENTS fallback only when the working-directory/ancestor path contains no `CLAUDE.md`, `.claude/CLAUDE.md` or `CLAUDE.local.md`; a CLAUDE file can import `@AGENTS.md`; AGENTS override/local filenames are not Codex equivalents | `/memory`; direct AGENTS listings require v2.1.280+, with early exceptions fixed in v2.1.281 |
| Gemini CLI | `GEMINI.md` default; configure `context.fileName` to include `AGENTS.md` | Global, workspace/ancestor and relevant directory context, subject to trusted-root rules; not Codex's precedence model | `/memory show`, then `/memory reload` after changes |
| Aider | Explicit `aider --read AGENTS.md`; persist `read: AGENTS.md` in `.aider.conf.yml` | Included read-only chat context; no implied AGENTS ancestor-discovery hierarchy | Startup confirmation and `/ls` |

Primary documentation and version limits are in Appendix C. Test one distinctive instruction in a fresh session rather than assuming the file was discovered or has identical authority in every client.

---

### The story: one convention, three supports

A team I worked with had used a coding agent for six months when a senior engineer brought me a complaint. "Every time we generate an API endpoint, I have to fix the validation. Always the same fix. The agent puts it in the wrong layer."

"Why isn't the rule written down?"

"We never wrote it down. We just keep fixing it."

The senior repeatedly corrected the same validation placement during endpoint reviews. The original account included endpoint counts and a time estimate, but the underlying review records are not available here, so this edition makes no precise monthly saving claim.

We documented the convention in AGENTS.md, added a PR-template reminder and identified correct endpoints as reference examples. Subsequent reviews reportedly needed fewer corrections of that kind. The intervention was that combination; the account does not isolate the instruction's contribution.

| Case note | What this account establishes |
|---|---|
| Provenance | Author-reported, anonymized engagement |
| Evidence | A recurring review problem and a reported improvement; underlying review/time records are not published |
| Comparison | Before/after observations of a combined instruction, reminder and reference-example change |
| Limitations | No isolated instruction effect, controlled task mix or defensible monthly time saving |
| Transfer | Write a scoped convention, support reviewers and examples, then measure recurring corrections |

---

### Six rules for the file

**Six rules, each with a test you can apply to any line.**

| # | Rule | You met it when |
|---|---|---|
| 1 | One line, one checkable constraint | It names the layer, the mechanism and an example |
| 2 | A documented need or failure | You can explain the risk, missing convention or repeated correction |
| 3 | Task-relevant contents | Key conventions, commands, pitfalls, glossary and pointers |
| 4 | Concise and scoped | Every always-loaded line earns its cost; start well below 200 lines |
| 5 | Treat it as code | Git, PR review, one rotating champion |
| 6 | Read before cite | Every name was read this session or found by grep |

---

### Rule 1: write rules the agent can check

**A rule the agent cannot check is decoration.**

| | The rule |
|---|---|
| Bad | "Always follow our coding standards. Be careful with validation. Use the right architecture." |
| Good, for this project's HTTP entry path | "Controller DTOs establish request-shape guarantees through Bean Validation before service calls; follow UserCreateController. Other entry points establish the same guarantees. Service/domain code still enforces business invariants; use service method validation where required by that boundary." |

The bad version leaves the architecture unspecified. The scoped version identifies an entry boundary, its guarantee, a mechanism and an example without declaring services universally safe to trust arbitrary input. Spring supports service method validation too. A portable pattern is: "Within [scope], [entry boundary] establishes [input guarantee] using [mechanism]; follow [reference]. Other entries establish the same guarantee; [owner] maintains domain invariants." Appendix B.2 is a project-specific starting point.

### Rules 2 and 5: justified by need, owned like code {#rules-2-and-5-earned-by-failure-owned-like-code}

**A rule earns its place through a concrete need, and a champion keeps the file honest.**

- **Review it like code.** The agent works against these instructions. Ask which non-obvious convention, preventive constraint or repeated failure justifies each line, and keep the rationale. A documented access restriction need not wait for an incident; vague speculative best practices still pile up into bloat.
- **Keep a mistake journal.** One entry per real incident, with the rule that prevents a repeat and an evidence pointer, the commit or the incident; B.2 has a sample entry.
- **Name a champion.** One person owns the file and the journal; everyone edits through pull requests and the champion curates. Each quarter the champion asks of every entry whether it saved anyone in the last three months, and retires those whose underlying problem is gone, with the reason in the commit message; a rule that still prevents a rare failure stays. Then the role rotates.

### Rules 3 and 4: scoped contents, a size guideline {#rules-3-and-4-fixed-contents-hard-cap}

**Keep the instructions the agent needs; link to the detail.**

- **Forbidden patterns, conventions and journal entries**, one line each.
- **Exact build and test commands.** Without them the agent guesses, and guesses are sometimes wrong.
- **A domain glossary.** In pretraining "transfer" means many things; in your bank it means one, and a "wire" is only the inter-bank kind.
- **One pointer line:** "Repository layout and module map: `docs/architecture.md`. Read it before touching a module you have not seen this session."

Avoid a repository dump. The revised context-file study found no general success improvement from generated files and over 20% more inference cost in its tested settings; developer-written files helped slightly, without a statistically significant average gain. That does not establish that all instructions harm or all maps are useless. Keep non-obvious conventions and useful pointers here; put a long architecture map in `docs/architecture.md`, read on demand (Chapter 7).

**Aim short; treat 200 lines as a guideline.** The file loads at session start, so every line spends context. There is no universal line count at which a model stops following rules. Remove duplication and stale instructions, and scope conventions to the paths or skills that need them. Keep rare but important constraints while their underlying risk remains.

A banking team's file grew to about nine hundred lines in six months and the agent began ignoring the newest rules. We cut it to ninety, moving conventions into skills that load on detection and past-mistake history into the architecture document, and compliance jumped within a week. That is one team's observation, not a measured threshold; the useful habit is deciding what belongs in every session.

### Rule 6: when the agent confidently lies

**The agent invents files, functions and options, so make it prove what it cites.**

It will cite a file that does not exist, a function the library never exposed, an option deprecated three versions ago. The output looks plausible and is wrong; the agent pattern-matches against similar code and does not know it is guessing. Three mechanical tactics:

- **Read before cite.** Anything the agent references must have been read this session. AGENTS.md can say so: "Before referencing any function, read the file that defines it. Citations without preceding reads are drafts to verify."
- **Grep every new name.** No hits means the function probably does not exist, or lives in a vendored dependency the agent cannot see. It takes seconds and catches the most common fabrications.
- **Hook the citations.** If the agent cites a file and line, a few lines of bash in a hook can verify the line exists (Chapter 2).

---

### Context hygiene {#context-hygiene}

**The window is the agent's working memory, so load what the task needs and nothing else.**

Everything in the window competes for the same bounded attention. Stale or conflicting context is one way a long session can lose track of the task. Four habits help manage that risk.

- **Pointers over payloads.** Link the architecture document from AGENTS.md, do not paste it. Keep the always-loaded layer small and load scoped detail when it matters.
- **One coherent unit of work per session.** Stay in the session while the shared context remains useful. Before a handoff or restart, save the decisions, constraints, changed files and useful evidence the next session needs in a task note, PR or other suitable place; commit when repository practice calls for it.
- **Watch for signs of drift.** The agent re-answers a settled question, cites a stale file version, forgets a constraint or makes poorer edits late in the session. These symptoms prompt diagnosis: conflicting requirements, stale source material or missing access can also explain them. Resolve the cause; preserve the needed state before restarting or compacting.
- **Treat compaction as a handoff.** Summarization can retain conversational decisions but omit or distort details, so save indispensable decisions, constraints and evidence durably. Give the compactor a keep-list: the plan, open questions, implementation deviations and exact commands that worked. Then check that the resulting context contains what the next step needs.

The client determines what it summarizes, retains and reloads; [Claude Code's compaction documentation](https://code.claude.com/docs/en/context-window#what-survives-compaction) describes those distinctions. Check the behavior of the client and version you use.

---

### When it breaks

- **The file is a request, not a wall.** The agent can still violate AGENTS.md. Required restrictions need enforced permissions, isolation or protected review gates; a hook helps only on the paths it covers (Chapter 2).
- **Old entries turn into folklore.** An entry with no evidence pointer is hard to retire, and a graveyard of rules is almost as useless as none: the team stops trusting any of them.

---

### Do this Monday

- [ ] Inspect the repository's current instructions. Add a documented missing convention, justified constraint or recurring correction; include commands and pointers where they save guessing. There is no quota of lines or rules to fill.
- [ ] Find your own validation story: a correction you keep making in review. Write it as one checkable line and add it to the PR template as a reviewer prompt.
- [ ] Check unfamiliar names against their definitions and sources. Add a read-before-cite rule if it corrects an observed problem, and name an owner for instruction maintenance.
- [ ] In your next long session, watch for drift. Preserve the state needed for a handoff, then recover, compact or restart as appropriate; commit according to repository practice.

---

### Go deeper

- **Templates:** [Appendix B.2](#template-b2), the AGENTS.md skeleton (it carries the precedence line); [B.7](#template-b7), context hygiene on one page; [B.11](#template-b11), bootstrapping the file on a repository.
- **Deep dive:** [Appendix D, Chapter 6](#deep-dive-chapter-6) - the context-files study, the rule-count cliff, mistake-journal mechanics, and the compaction and cache measurements.
- **Sources:** Appendix C.

---

## Chapter 7
## Map it first: architecture review

*By the end you can produce a corrected architecture map of a codebase nobody remembers, and use the run as an initial diagnostic before choosing a bounded next task.*

**TL;DR**

- Use a scoped investigation to draft `docs/architecture.md`, then review it against the code and business reality.
- In the case below, agent work took 18 minutes and expert correction about 45. Accuracy and review time depend on access, scope and domain knowledge.
- The same run is an initial diagnostic. An incoherent map means pause autonomous changes and investigate the model, access, context and codebase (Chapter 8).

---

### The workflow

**Make the agent read the code first, then correct what it wrote and commit the result.**

Many teams own a codebase that fits one description: the author left, the README describes a build that no longer works, the code earns money and nobody wants to touch it. An agent can shorten the first investigation, but producing a map is not the same as becoming productive or understanding the business. The case below took minutes of agent work and a domain expert's review; other repositories take longer.

The prompt asks for nine sections, from purpose and data model to risks and unknowns, with file-and-line citations throughout; the full text is Appendix B.1. Choose the sections and depth the investigation needs. A document can look complete while its central business interpretation is wrong. If the codebase outgrows one context window, independent module investigations can justify subagents, with the orchestrator assembling the parts and checking their shared boundaries.

---

### The case

**The agent did not decide the rewrite was unnecessary. It gave the domain experts enough structure to decide faster.**

A banking team owned a customer onboarding system: about sixty thousand lines of Java, written between 2018 and 2024 by a rotating cast of contractors. The team had been assembled in 2024 from three acquisitions, and nobody had been there for the original build. The README described a 2020 architecture, and the documentation listed two of the build's three steps. They were weighing a complete rewrite, estimated at eighteen months, because "nobody understands it well enough to maintain it confidently."

I asked for fifteen minutes and a terminal. I pasted the review prompt with two additions: the domain (customer onboarding, regulated banking) and a request to flag anything that looked compliance-sensitive. Eighteen minutes later there was a thirteen-page document, wrong in three places:

- It called the deduplication service a "search service" because the implementation used the search infrastructure. Its business purpose was preventing double-creation of customer records.
- It described a scheduled job in confident detail. On inspection it was commented-out code that had not run in production for three years.
- It missed that a third-party dependency was deprecated and carried a security advisory. The agent had no access to the advisory database, so I added that myself.

The corrected document went into the repository, and the team chose targeted work instead of the broad rewrite proposal. They replaced two modules the following quarter, including the deprecated dependency. The eighteen-month proposal and three-month replacement describe elapsed schedules, not comparable labor totals. Without the original staffing assumptions and a credible counterfactual, this account does not establish person-months saved or isolate the agent's effect from the experts' judgment.

| Case note | What this account establishes |
|---|---|
| Provenance | Author-reported, anonymized banking engagement |
| Evidence | The account, its three corrected mistakes and reported investigation times; original artifacts are not published |
| Comparison | An estimated broad rewrite schedule versus the targeted work the team chose; staffing is unspecified |
| Limitations | Avoided effort is an unmeasured counterfactual; experts corrected the map and chose the alternative |
| Transfer | Use a reviewed map to challenge scope, then estimate the alternatives explicitly |

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

### Delete with evidence {#delete-with-evidence}

**A removal is a claim; prove it before the agent deletes anything.**

The map also makes cleanup safer, the work the Prologue's Slopfix sells. For each candidate, gather static references, runtime use (logs, metrics, flags, scheduled jobs), any fallback kept for incidents, and the owner's confirmation. Then open one small pull request per removal with the evidence linked, reviewed by the team that owns the code. OpenAI's account of its own cleanup with GPT-6 models, over 1,400 merged pull requests deleting more than 800,000 lines, names the traps: reflection that defeats static analysis, an unused path kept to mitigate future incidents, and proposals that added more complexity than they removed.

---

### Review as diagnostic

**An incoherent map is a reason to pause autonomous changes and investigate the cause.** The run is an initial diagnostic, not a verdict on the codebase.

- **Coherent map, reasonable correction:** useful evidence for a bounded next task. It does not establish behavioral understanding or production readiness.
- **Incoherent map:** check missing access, incomplete context, investigation scope and model fit before attributing the failure to tangled code. If the team still cannot evaluate the result, keep the relevant work human-led and use Chapter 8's rubric.

Time-box the first investigation, then decide whether another pass is likely to resolve a specific gap. Chapter 8's kill signals are the systematic rubric; a single map does not replace it.

---

### When it breaks

- **Unreviewed output.** Citations and a polished structure do not make a draft correct documentation.
- **A reviewer with no domain knowledge** cannot tell which plausible mistakes to flag. Budget hours.
- **The map goes stale.** Re-run the review whenever the codebase changes substantially.

---

### Do this Monday

- [ ] On a poorly understood codebase, choose the relevant parts of Appendix B.1, name the domain and time-box the first pass.
- [ ] Correct the output against the five checks above.
- [ ] Save it as `docs/architecture.md`, commit it, and add one pointer line to AGENTS.md. Do not paste the layout in.
- [ ] Judge the evidence: choose a bounded next task, or investigate why the map failed. Use Chapter 8 before expanding scope.
- [ ] Record investigation and correction time before repeating the exercise elsewhere.

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

*By the end you can establish a task's prerequisites, identify preparation gaps and decide what work can proceed within tested boundaries.*

**TL;DR**

- Before scoring, define the task, its qualified reviewer, evidence that would expose a consequential mistake, and appropriate permissions and recovery.
- Missing or unknown prerequisites restrict the affected task to investigation or supervised preparation. A green repository score does not authorize every task in it.
- Use the eight signals as a heuristic preparation guide. Record unknowns explicitly; coverage percentage alone does not establish verification.

---

### When should you not use AI coding agents? {#when-not-to-use-agents}

**Some codebases should not get an agent yet, and saying no there is what lets you say yes everywhere else.**

The reason is not that the agent or the team is bad: a proposed change can exceed the team's ability to evaluate it, verify it or contain its consequences. Establish those prerequisites first. The eight signals then help prioritize preparation; they are a discussion aid drawn from practice, not a validated risk model.

### Before scoring: define the task

| Prerequisite | Evidence needed |
|---|---|
| Scope | Named behavior, affected module and environment; permitted actions |
| Evaluability | A qualified person who can recognize a plausible but incorrect result |
| Verification | Checks that expose consequential mistakes in this change, with meaningful assertions and interpretable failures |
| Boundaries and recovery | Appropriate access, approval, deployment and recovery arrangements for the consequences |

If any answer is missing or unknown, restrict that work until the gap is addressed. An agent can still investigate an untested module or draft characterization tests under supervision. That does not authorize it to change the module's business behavior. The restriction follows the affected task, not every activity in the repository.

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

**Establish relevant verification before behavioral changes; let the agent help prepare it.**

Ask the agent to draft characterization tests of current behavior, then have a qualified reviewer distinguish intended behavior from existing bugs. Check important outcomes, failure cases, reliability and whether the team can interpret failures. If no available evidence would expose a consequential mistake, restrict the affected work to investigation or supervised preparation until that evidence exists. The tests are a regression net, not proof of correctness (Chapter 5).

---

### Signal 6: the team cannot evaluate the output

**This is the most important signal, and the one teams misread most often.**

A junior is assigned a story to add a cryptographic verification step to the payment flow and dispatches the agent. It produces a module using AES-256 in CBC mode with a hardcoded initialization vector. To someone new to cryptography it looks right: it compiles, the unit tests pass, and the senior cryptographer is on parental leave for three months. The junior ships it, and the vulnerability sits in production for six months until a penetration test finds it.

The agent did exactly what was asked. Its output looked right and was wrong, and nobody was placed to see it.

Teams read this as "we need more senior engineers", which does not scale on a six-month timeline. Make qualified approval a required server-side review for the sensitive paths, with agent credentials unable to bypass it. Enforced tool policy can also keep the agent from editing those modules. AGENTS.md can explain the restriction and agent reviewers can assist, but neither substitutes for the missing expertise or makes approval unavoidable.

This signal fails the evaluability prerequisite regardless of the total. Several other signals can also block a particular task, including absent verification or an unavailable approval path. Build the missing capability, bring in someone who has it, or restrict the affected work. A low total never overrides a missing prerequisite.

---

### Are AI coding agents production-ready? {#are-agents-production-ready}

**Readiness belongs to a task and its controls; a repository color only helps prioritize preparation.**

```
  Check task prerequisites first. Unknown is not zero.
  With no unknowns, sum and round halves upward before choosing a color.

  Signal count       Color       Preparation guide
  ============       =====       ====

  0 - 1              GREEN       Few preparation gaps
  2 - 3              YELLOW      Substantial preparation
  4 +                RED         Broader preparation first

  Signals (score each known gap):
   1. No tests          5. Regulatory constraints
   2. No documentation  6. Team cannot evaluate output
   3. Tight coupling    7. Model-context fit
   4. Scattered rules   8. Velocity-of-change
```

*Figure: The kill signals and the traffic light preparation guide. Missing task prerequisites override the color; unknown answers require investigation.*

- **Green:** a candidate starting point, once the proposed task meets all prerequisites.
- **Yellow:** prioritize the specific gaps and use closely supervised work where the prerequisites hold.
- **Red:** broader preparation is likely needed. Investigation and bounded repair can still be useful; do not treat the color as permission for behavioral changes.

Apply the guide to the relevant area of a project. A green repository score supports choosing a starting point. It does not authorize every task in that repository.

---

### Count by intensity, not presence

**Score the evidence for the affected area; leave uninvestigated properties unknown.**

Use 0 for an absent preparation gap, 0.5 for a partial gap and 1 for a substantial gap, with a short evidence note. Use `?` when uninvestigated; do not calculate a reassuring total by counting it as zero. With no unknowns, sum and round halves upward before applying the 0-1 / 2-3 / 4+ bands. These are author heuristics, not measured safety thresholds. Appendix B.4 gives behavioral anchors; a line-coverage percentage is supporting information only.

---

### What the colors look like

**Each color changes how you use the agent.**

| Project and evidence | Count | Preparation | What to do |
|---|---|---|---|
| Customer-profile service: relevant outcomes and failure cases tested reliably, current overview, canonical rules, qualified reviewer | 0 | Green | Choose a bounded task and establish its remaining prerequisites |
| Legacy payments: relevant failure cases absent (1), stale docs (0.5), costly coupling (1), scattered rules (0.5); approval and expertise available | 3 | Yellow | Prepare verification first; supervise bounded investigation and refactoring |
| Custom encryption library: undocumented, no qualified cryptographic reviewer | Not decisive | Prerequisite failed | Restrict cryptographic changes; obtain expertise or evaluate a vetted replacement |
| Greenfield API: clear request, verification and deployment not investigated | ? | Unknown | Define behavior, checks, reviewer and recovery before choosing a mode |
| Internal tool: relevant checks established, some documentation and coupling gaps (0.5 each), low exposure | 1 | Green | A possible pilot, subject to task prerequisites and spending limits |

---

### When it breaks

- **Counting test coverage instead of assertions** hides missing verification. Check the affected behavior and consequential failure cases.
- **A green total masks an unknown.** Investigate the unknown and task prerequisites before expanding scope.
- **Leadership mandates a mode despite a missing prerequisite.** Restrict the affected task and name the preparation needed.
- **A green codebase starts giving yellow results after a model upgrade.** Suspect instructions written for the previous model before you blame the code: run the migration checklist in Appendix B.9.

---

### Do this Monday

- [ ] Name one proposed task, the affected behavior and environment.
- [ ] Fill the four prerequisites in B.4; restrict the affected work wherever an answer is missing or unknown.
- [ ] Record evidence for the eight preparation signals. Use `?` for unknowns and meaningful checks rather than coverage thresholds.
- [ ] Give the lead a bounded next action, owner and completion criterion. Finish when another engineer can reproduce the decision from the worksheet.
- [ ] Recheck when the task, model, controls or surrounding system changes.

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

- Isolate concurrent or conflicting work, use local checks for feedback and protected server gates for enforcement, and retain normal human review.
- One engineer can start a rollout: use it yourself, record outcomes, teach a peer, then recruit the lead and manager. Measure the pace rather than assuming a fixed productivity curve.
- Give skepticism a constructive role, make review accountable and plan for vendor outages.

---

### Guardrails for a real repo

**The agent is one more author with write access, so give it the boundaries every author gets.**

These repo-level habits sit on top of Chapter 2's five layers and matter most on yellow codebases (Chapter 8). The human review floor that no review bot replaces is Chapter 5's.

---

### Worktrees

**Isolate concurrent agent work from unfinished local changes.**

A worktree is a separate checked-out copy of the repository on its own branch. It is useful for concurrent tasks or when an agent would otherwise touch unfinished local work. A clean dedicated checkout or an already isolated environment can satisfy the same purpose. Worktrees prevent working-copy collisions; they are not a security sandbox, and all work still goes through normal review.

---

### Two kinds of hooks

**Hook the agent, hook the repository, and run the same checks in CI.**

- **The agent hook** (hookify, or your agent's equivalent) checks covered actions and allows them, requests approval or blocks them. Use it for sensitive areas such as cryptography, payments or migrations. Its configuration and failure behavior need protection (Chapter 2); a repository file the agent can rewrite is not a firm boundary.
- **The git hook** runs for whoever is committing - you, a teammate or the agent - so one check covers every author. Fast checks (format, lint, typecheck, secret scan) run at commit, tests and the build at push, and a hook manager with versioned config makes sure the hooks are installed on every clone.
- **Local bypasses** include `--no-verify` and changing Git's hook configuration. A deny rule can catch some attempts; it does not make local hooks mandatory.

Local hooks are fast feedback: skippable and not guaranteed on every machine. Enforce acceptance with required server checks, protected workflow changes and required owner approval. Verify that the agent's credentials cannot change or bypass those rules; moving an editable check into CI does not by itself protect it.

---

### Keeping it alive

**Rules rot, so someone owns pruning them.**

The mistake journal and its champion are Chapter 6. For process mistakes, keep a failure watchlist: recurring failures, what triggers them and the team's standard response. Review it every month or so and retire what is fixed.

---

### The outer loop

**Run the agent unattended only under a written contract.**

The outer loop re-invokes the agent until a condition holds. It adds attempts, not judgment, so it multiplies whatever your inner loop permits (Chapter 4). Use it only when every unit meets Chapter 8's task prerequisites and can be independently verified and recovered, with controls suited to unattended work. A green preparation score alone is insufficient. Review the resulting pull requests before release.

Before the first unattended run, record a machine-evaluable stop condition, budget, protected acceptance gate, durable state and context handoff, and isolation sized for absence. Use a dedicated branch and working copy, verify each tool's sandbox coverage, keep production credentials out and test network restrictions. Appendix B.6 is the form, with the four signs that mean stop before relaunch.

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

**The 90-day arc is one workable schedule, not a productivity law.**

Before starting, establish an approved service and account, permitted repositories and data, a responsible owner, initial tested controls and a spending limit. Existing policy applies to a grassroots pilot too. The example then gives setup and a bounded pilot the first month, expansion the second, and operational ownership the third. Later governance work reviews expansion and recurring ownership; it is not the first approval. Track elapsed and human touch time, quality, review/rework and total cost from the start. Add instructions, skills and hooks for a demonstrated need or justified risk. The reusable calendar and measurement card are Appendix B.5.

```
  BEFORE STARTING: approved service/account; permitted repositories/data;
  responsible owner; initial tested controls; spending limit and baseline.

  Days 1-30: Foundation             Days 31-60: Expansion           Days 61-90: Productionization
  -------------------------         -------------------------       -------------------------
  Champion installs                 Lead onboards 2-3 more          Manager folds metrics
  AGENTS.md drafted                 engineers                       into normal velocity
  First green-light project         AGENTS.md hardened              tracking
  Architecture review               Hooks configured                Expansion governance reviewed
  workflow proven                   Skills if useful                Ongoing marketplace
                                    Kill signals applied            policy and ownership
                                    to portfolio
  ====================              ====================            ====================
  Champion                          Lead                            Manager
```

*Figure: The 90-day adoption arc as one possible schedule. Each phase assigns responsibility; milestones depend on the pilot's needs and results.*

---

### Role commitments

**Agree an explicit time budget and adjust these example commitments to the team.**

**The champion** learns the workflow first. They need protected time and willingness to investigate failures; seniority alone does not select them. They run the architecture review (Chapter 7) on a familiar codebase, tighten the instruction file, and use Chapter 4's loop on a few features sized to each, logging friction in the mistake journal. By day 90 another engineer runs the workflow as fluently. Appendix B.5 has the week-by-week calendar.

**The lead** decides which work gets the agent.

- [ ] Week 1: select proposed tasks, establish their prerequisites and record preparation gaps (Chapter 8).
- [ ] Months 2-3: track cycle time, defect rate and reviewer time (noisy; measure anyway), then present honest results, including where the agent did not deliver.

**The manager** owns pilot eligibility and budget before work begins, then procurement, expansion decisions and recurring governance. Appendix A provides an illustrative twenty-engineer scenario and a complete hypothetical cost calculation; it does not supply measured adoption or cycle-time outcomes.

---

### Dissent and overconfidence

**Separate justified dissent from unexamined delegation, using evidence and the normal engineering process.**

**The principled skeptic** may be identifying a real failure mode. Invite them to define representative tasks, consequential mistakes, evidence needed to expand scope and stop conditions. A demanding reviewer can improve the pilot without choosing to use the agent personally. Distinguish evidence-based dissent from obstruction through the normal engineering process. Resolve ownership and conduct disputes there; do not route around required expertise or approvals to preserve adoption momentum.

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
| Local hooks treated as enforcement | Skipped, edited or never installed | Protected required server checks and reviewed policy changes |

---

### Do this Monday

- [ ] Check that the agent's workspace is isolated from concurrent work and unfinished local changes; use a worktree or dedicated checkout where needed.
- [ ] Pick your role - champion, lead or manager - make the first commitment from its checklist this week, and put it on a calendar.
- [ ] Check required server checks and sensitive-path approval, including who can bypass them. Test any policy hook's blocking response and failure behavior; local hooks are additional feedback.
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

**Architecture is the control of capability.** Inspect context, tools, permissions / sandbox, skills, plugins, MCP, memory, effort and subagents, and the harness that supplies them. The list helps compare contemporary systems; absent or externally supplied capabilities are legitimate findings.

**Method is the control of workflow.** Formulating work clearly is the foundational shift. The six-phase loop is one implementation; AGENTS.md will exist under other names, but the principle is permanent: discipline as code, not oral tradition.

**Reality is the control of adoption.** Kill signals are properties of codebases and teams, not of tools. The traffic light applies whichever agent you use this quarter, and champion, lead, manager is the arc for any tooling transition.

If you take one practice away, take the architecture review from Chapter 7 as an initial diagnostic: useful evidence to inspect, not a verdict from one run. If you take one framework, take the task prerequisites and preparation signals from Chapter 8; the "no" matters as much as the "yes." If you take one orientation, invest in the way of thinking, not the tool.

Back to Slopfix: the agent that wrote fourteen date formatters and the agent that collapses them into one are the same kind of agent. What changed was the context it was given, the checks it could not argue with and the people who decided what stayed. That is the whole manual in one example. It asks you to make your own controls and decisions inspectable.

Understanding the problem becomes more important than writing the code. That was true when programming meant punching holes in cards, when the IDE replaced the text editor, and when AI-assisted coding crossed from autocomplete to drafting; it is true now that agents do the writing. The model names will age out of this edition, and the durable work stays: understand the problem, formulate the work, constrain the execution, verify the result. That sequence is the whole control problem, and it never belonged to the tools: it belongs to you.

Agents can help you understand the system. You remain accountable for understanding enough to choose the work, evaluate the evidence and accept the consequences.

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

I started on machine learning around 2013. In late 2015 I ported DarkNet and YOLO onto an XR headset and began building AI applications professionally; in 2023 I joined a company developing neuromorphic SoCs. I have used every generation of coding assistant, from Visual Assist to the first Copilot to LLMs for coding since ChatGPT shipped. I have not built my own coding agent; I have used most of the ones that ship now and watched many teams use them.

I am not neutral. I think agentic software delivery is the most consequential shift in our field since high-level languages, and that the way most teams adopt it is doing them more harm than good. This is the third or fourth iteration of these frames; the earlier ones were wrong in interesting ways.

<a id="contact"></a>
*Contact: [info@ship-it-with.ai](mailto:info@ship-it-with.ai) for technical conversations or tailored workshops, in-person or online, shaped to your team's codebase and constraints. Find me on [LinkedIn](https://www.linkedin.com/in/mihaicvasnievschi/).*

---

## Changelog {#changelog}

This page tracks meaningful updates to the manual. Smaller copy-edits and SEO tweaks are not listed; the footer shows the last updated date.

### 2026-10-30 - October currency pass: trust, routes, cleanup and recovery

Chapter 2 adds repository configuration as an attack surface (the ChainDrop worm), a short compromise response and the CI boundary, and the control record now covers browser sessions, desktop control and connected services. Chapter 5 adds a dependency check to diff review. Chapter 7 adds deleting with evidence. B.6 adds reconciliation before a retry and an enforced budget; B.9 records routed models, sign-in surface and memory state. Corrections: Railway's account of the PocketOS backups and token scopes, the separate Claude Code trust-dialog advisories, Knostic's finding, SpecBench's Claude Code attribution, `/workflows` budgets and current auto-memory policy. The reader-observation protocol moved to the reader-trial materials.

### 2026-10-23 - Evidence, task prerequisites and reproducible delivery

The maintained editions start with the native agent and task-sized process; Superpowers remains optional. Task prerequisites now precede the heuristic readiness score, with unknowns explicit and behavior-based verification anchors. Control records distinguish prevention, detection, failure behavior and tested coverage. Case notes separate author reports, unavailable measurement records and counterfactual savings; unsupported rollout percentages and labor-saving precision were removed. The economics include all attempts, amortized setup, maintenance and recurring governance, separating capacity from cash. A synthetic runnable Wire companion demonstrates inadequate-green, corrected-red and repaired-green, dependency-aware planning and production handoff. Technical corrections cover instruction discovery, concurrency, context-study baselines, DNS routes, Playwright actions, RULER, MCP and Spring. Templates, summaries, sources and Romanian recommendations align; reader routes, template labels and archive dates are clearer. New or rechecked sources identify their scope and date; this is not a claim that every historical fact was revalidated. The September manuscripts remain frozen.

A final edit removes the remaining certainty about PocketOS controls, qualifies effort availability and compaction, and marks the return from the synthetic Wire experiment to the original engagement. B.9 now covers model, harness and skill evaluation in both languages, retaining migration checks. B.11 adds a reader-observation protocol; it records no trial results.

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

Chapter 5 gains a Context hygiene section, inserted after the inner/outer loop vocabulary paragraph, that teaches the daily craft the book had named but never taught - the window is the agent's working memory, and everything loaded into it competes with reasoning. It names four signs of drift (the agent re-answers a settled question, cites a stale version of a file it edited, forgets a constraint it honored, or degrades in edit quality late in a long session), the session-boundary discipline of one unit of work per session with durable state read back from the repository, and compaction as a handoff. The current guidance qualifies that early wording: summaries can retain details, but indispensable state needs durable preservation and a checked handoff. New Appendix B.7 context-hygiene one-pager (the template count is now seven). Chapter 1's context-window section gains a one-sentence forward pointer to the new section.

### 2026-07-05 - Appendix A worked example

Appendix A gained a worked cost example using illustrative rates and the then-reported rollout figures. **Superseded October 23:** the underlying measurement definitions and records are not available here; those figures are no longer presented as measured pilot evidence. The maintained appendix now contains an explicitly hypothetical full-cost comparison and a reusable measurement card.

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

*For the engineering manager, director or CTO who owns budget, staffing and procurement, and for the champion who has to hand them a case. Read Chapters 2, 8 and 9 for controls, task readiness and rollout. This appendix covers your decisions, an illustrative team, and a cost comparison you can replace with your own numbers. It can be forwarded on its own.*

---

### Your job in the 90 days

**The manager owns the conditions for starting, the decision to expand, and the ongoing cost.** Those responsibilities begin before the first pilot. The sample 90-day arc in Chapter 9 gives more attention to the manager later; it does not postpone procurement or governance until day 61.

Before starting, name the responsible owner and agree:

- The approved service and account, permitted repositories and data, and any required contractual terms.
- Initial permissions, secrets controls, isolation and recovery arrangements appropriate to the pilot. Verify the covered routes rather than assuming the configuration works.
- A spending limit, comparable work to observe, success criteria, and conditions for stopping or restricting the pilot.
- Who can judge the affected behavior, review consequential changes, and make the expansion decision.

During the pilot, protect time for investigation, review and maintenance. Help the lead resolve access, documentation and expertise gaps. A team unable to evaluate a payment algorithm needs qualified help or a narrower task; a subscription does not supply that expertise.

Later, decide whether the evidence supports expansion, a different workflow or stopping. Assign continuing ownership for instructions, integrations, vendor risk, controls and evaluation. These are operating responsibilities, even when the initial setup is complete.

Track outcomes from the start. Resist individual rankings based on PR counts, early promises of revenue, and a calendar that expands scope regardless of results. A small, well-understood pilot is easier to evaluate than a company-wide adoption target.

---

### Which codebases now, later, never

**Decide for the proposed task before sorting the portfolio.** Define the affected behavior and environment. Establish a qualified evaluator, evidence that would expose a consequential mistake, and suitable permissions and recovery. If a prerequisite is missing or unknown, restrict that task to investigation or supervised preparation until the gap is addressed.

Chapter 8's eight signals then help prioritize preparation. The colors are a heuristic, not a delegation policy. With no unknowns, sum and round halves upward before applying a color:

| Rounded repository score | Preparation guide | Manager's decision |
|---|---|---|
| Green, 0-1 known gaps | Few preparation gaps | Consider bounded work whose task prerequisites are established. |
| Yellow, 2-3 known gaps | Substantial preparation | Fund the most consequential gaps and select work the team can evaluate now. |
| Red, 4+ known gaps | Broader preparation | Restrict the affected work while deciding what to investigate, improve, replace or retire. |
| Unknown, `?` | Evidence is missing | Investigate it; do not silently count it as zero. |

A green repository score does not authorize every task. A high score does not prohibit useful read-only investigation. Missing qualified evaluation is a task prerequisite failure regardless of the total. Test coverage can inform the discussion, but relevant assertions, failure cases, reliable execution and the team's ability to interpret results matter more than a percentage.

Ask the lead for a short portfolio record: proposed task, prerequisites, known and unknown gaps, permitted scope, required preparation and owner. For each investment, ask what decision or verification capability it buys. "Never" should describe work the team cannot responsibly authorize under its present constraints, not a permanent label attached to a company or repository.

---

### One team, week by week

**Illustrative planning scenario:** twenty engineers in a regulated financial-services firm, with an engineering manager and a cost-conscious CTO. This is not a measured pilot or a report of a client engagement. The schedule illustrates decisions and responsibilities; it supplies no observed adoption, cycle-time or defect-rate result. Use the sequence where it fits, and change the dates to match the evidence.

| Stage | What the team brings | What the manager does |
|---|---|---|
| Before the pilot | A bounded proposal, an accountable owner, approved account/data scope, initial controls, and an evaluation plan | Confirms eligibility, expertise, spending limit and stopping conditions before work begins. |
| First month | A small sample of accepted and failed attempts, review findings, billed usage and unresolved gaps | Protects evaluation time; addresses missing access or expertise; does not demand an adoption percentage. |
| Second month | A comparison of similar work, with human effort, delivery time, quality observations and costs recorded separately | Checks how tasks were selected and whether the results justify another bounded group of users or tasks. |
| Later manager phase | A recommendation to expand, change or stop, with limitations and operating responsibilities | Resolves licensing for the approved scope, assigns ongoing governance and maintenance, and reports supported outcomes. |

A useful board update names what was compared, what was observed and what remains uncertain. For example: *"We compared [counts and task types] during [dates], using [selection method]. Human touch time was [result], elapsed delivery time was [result], and [defect observations] cover [window]. The incremental cost was [amount]. We recommend [decision], subject to [remaining uncertainty]."* Fill the fields from records; leave unsupported claims out.

Keep one measurement card with the report:

| Field | What to record |
|---|---|
| Provenance and period | Observed pilot or illustrative example; dates, service/model versions, workflow and owner. |
| Work and comparison | Raw counts of attempted, completed and accepted tasks; task types, selection method, baseline/comparison group, exclusions and material differences. |
| Delivery time | Elapsed start-to-acceptance time, with the start/end definition and waiting time stated. Record human touch time separately. |
| Human effort | Investigation, implementation, review and rework for both groups; include failed or abandoned attempts. State how time was captured. |
| Quality | Escaped defects by severity, denominator and observation window. Record acceptance criteria and relevant checks; disclose missing follow-up. |
| Review | Reviewer effort, useful findings, resulting rework and required domain expertise. |
| Cost | Seats, all billed usage including failures, infrastructure, setup, ongoing maintenance and recurring governance/evaluation. State allocation and amortization assumptions. |
| Independence | Whether another engineer can operate the workflow and interpret its evidence without the champion. |
| Decision and limits | What supports expanding, changing or stopping; uncertainty, confounders and the next observation needed. |

Agent-touched PR share describes adoption. It is not an outcome target. A change in cycle time does not establish effort released, cash saved or unchanged quality. With a small sample or a short defect window, say what you observed; do not replace missing evidence with "within noise."

---

### How much does agentic coding cost? {#how-much-does-it-cost}

**Count the full delivery cost, then compare useful accepted work.** A seat quote is easy to find; investigation, review, failed attempts and maintenance are easier to miss. Prices and contract terms change. Use the structure below with your own agreement and records.

- **Fixed seats.** A genuinely fixed monthly fee stays the same when usage rises. Effective cost per useful task falls as useful usage increases. That does not make more generated output valuable. Usage caps, overages and tier changes are separate conditions to check.
- **Metered usage.** Count what is billed across all attempts, including retries, discarded work and additional agents. Use actual bills or usage records, not the final response's token count.
- **Enterprise terms.** Commitments, allowances, access controls, retention, audit facilities and contractual protections vary. Verify what the agreement provides and what the pilot requires; the label does not establish the terms.

Separate initial setup from continuing work:

| Cost | Include |
|---|---|
| Task delivery | Human investigation, implementation, review and rework, including failed attempts, on both sides of the comparison. |
| Tooling and infrastructure | Incremental seats, metered usage, environments and connected services. |
| Initial setup | Initial instruction, integration and control work; state the period over which it is amortized. |
| Ongoing maintenance | Updating instructions, skills, integrations and controls as the system changes. |
| Recurring governance and evaluation | Vendor-risk review, access review, measurement, control checks and procurement work that continues after setup. |

Keep three outcomes separate: shorter elapsed delivery time, useful engineering capacity released, and actual cash savings. A loaded hourly rate values capacity for comparison; it does not mean payroll falls when a task takes fewer hours. Record how any released time is used.

---

### The structural levers {#cost-levers}

**Change a cost lever only while checking the outcomes it must preserve.** A cheaper run that misses the requirement is a failed attempt, not a saving.

- **Effort and model choice.** Compare settings on representative tasks. Use more reasoning or a stronger model where it changes the result enough to justify its cost; use a cheaper setting where the evidence supports it.
- **Stable prefixes and caching.** Where the provider supports prefix caching, stable instructions before changing task content can reduce repeated input cost. Check cache eligibility, actual hits and billed rates.
- **Tool loading.** Load the capabilities the task needs. Deferred schemas can reduce initial context where the client supports them; confirm that required tools remain discoverable.
- **Context management.** The cited JetBrains study compared observation masking and summarization with unmanaged history across five configurations. Both substantially reduced cost in most settings; masking was cheaper than summarization in four of five. The Qwen3-Coder 480B configuration saved 52.7% and 50.4% respectively against unmanaged history. This is not a universal 50% saving from replacing summarization with masking.
- **Workflow and routing.** Compare the native workflow with optional skills, reviewers or advisor arrangements on matched tasks. Include their startup, review and coordination costs. The right arrangement depends on the task and model.

Appendix C records the sources and their scope. Recheck the relevant result before treating it as a budget assumption.

---

### A worked example {#a-worked-example}

**Hypothetical monthly comparison, not a measured result or vendor quote.** A twenty-engineer team accepts twenty comparable pilot changes. The calculation assumes comparable useful outcomes for the arithmetic; it does not establish equal quality or prove that agents caused the effort difference.

Across those changes, the baseline uses **200 human task hours** and the agent-assisted workflow uses **160**. Both include investigation, implementation, review, rework and failed or abandoned attempts. Value human time at an illustrative loaded **$100 per hour**. Costs shared unchanged by both workflows are omitted from both sides.

| Monthly cost for 20 accepted changes | Baseline | Agent-assisted |
|---|---:|---:|
| Human task time: 200h / 160h at $100/h | $20,000 | $16,000 |
| Incremental seats | $0 | $530 |
| Metered usage, including failed attempts | $0 | $270 |
| Incremental infrastructure | $0 | $100 |
| Initial setup: 120h × $100 = $12,000, amortized over 12 months | $0 | $1,000 |
| Ongoing instruction/integration maintenance: 10h × $100 | $0 | $1,000 |
| Recurring governance/evaluation: 4h × $100 | $0 | $400 |
| **Modeled monthly total** | **$20,000** | **$19,300** |
| **Modeled cost per comparable accepted change** | **$1,000** | **$965** |

The maintenance and governance hours are additional operating work, separate from the 160 task hours. Task review and rework appear only in task time. Initial setup appears only in its amortized line. All attempts contribute their effort and usage costs, even though only accepted changes form the denominator.

The value calculation is:

**$4,000 released task-capacity value − $900 tooling/infrastructure − $1,000 amortized setup − $1,000 ongoing maintenance − $400 recurring governance = $700 modeled net capacity value per month.**

That $700 is not cash savings or a forecast. The initial setup consumes 120 hours upfront; amortization spreads its value for this comparison rather than changing when the work occurs. A different useful life, more review, fewer accepted tasks, worse quality or unused released capacity can change the result. Elapsed delivery time is not specified by these human-hour totals.

For an actual pilot, replace each assumption with a record or label it as an estimate. Compare the measurement card as well as the arithmetic. Cost per accepted task is useful only when the work and its accepted outcomes are comparable; twenty easy fixes and twenty consequential changes do not become equivalent because both sets contain twenty items.

---

**Related:** [Appendix B.4](#template-b4) (task prerequisites and preparation worksheet), [Appendix B.5](#template-b5) (example rollout calendar), [Appendix B.10](#template-b10) (matched workflow comparison), Appendix C (sources).

---

## Appendix B. Templates

Eleven copy-paste templates and exercises. All are starting points; customize for your team.

### B.1 Architecture review prompt {#template-b1}

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

### B.2 AGENTS.md skeleton {#template-b2}

This is an illustrative Java/Spring project skeleton. Replace example names, incident dates, commands and restrictions with verified project facts; the sample incidents are not reports about your repository.

Works as [AGENTS.md](https://agents.md/) or CLAUDE.md; check your agent's loading rules. Start short and use roughly 200 lines as a trimming guideline, not a target or universal limit. The precedence line goes first: it clarifies how these local instructions relate to the task and skills, within the agent's higher-priority rules.

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

### B.3 Six-phase loop checklist (one-pager) {#template-b3}

```
SIZE THE WORK
  Clear and contained: native agent, direct change, focused check.
  Unclear or dependent: inspect, settle material questions, make a short plan.
  Risky or unfamiliar: explicit outcomes, failure cases, human decisions and review.
RESEARCH AND PLAN
  Gather missing context; record decisions and dependencies when needed.
  Define "done" and the checks that assess it. Gate consequential choices.
EXECUTE
  Work directly unless sizeable independent work earns delegation's cost.
  Keep one writer per overlapping area; run dependencies in order.
  Finish the authorized scope; record material deviations. Ask only when a new
  decision or action actually needs the user's authorization.
REVIEW
  Cover intent and code quality in the normal review. Add independent reviewers
  where risk, model behavior and measured usefulness justify them.
  Keep separate judgments fresh and blind to earlier verdicts.
  Accept or rebut findings with evidence; track useful defects and false positives.
  Stop repair when no material issue remains; another round needs new evidence.
VERIFY
  Run relevant tests, build, lint, behavior or visual checks; report the evidence.
  For a behavioral fix, add a regression test where feasible. Permanent test files
  are not required for every prose or config edit; assess risk separately.
  Diagnose failures before changing checks. Protect gates from bypass; review
  legitimate test/config updates. Reuse valid results until relevant code changes.
  Held-out tests and sealed history/network are evaluation or high-assurance tools.
SHIP
  Structured commit and PR; reviewers per CODEOWNERS; normal team review.
  Record release owner/order, compatibility, success signal, intervention trigger,
  recovery approach and observation window before the production handoff.
```

### B.4 Kill signal scoring worksheet {#template-b4}

```
TASK PREREQUISITES - complete before scoring
  Proposed behavior/module/environment: ______
  Qualified evaluation owner: ______
  Consequential mistake and evidence that would expose it: ______
  Permitted actions, required approval, deployment and recovery: ______
Missing or unknown? Restrict the affected work to investigation or supervised
preparation until resolved. A green repository score authorizes no task by itself.

PREPARATION SIGNALS - 0 absent gap / 0.5 partial / 1 substantial / ? unknown
For each, record evidence, owner and next action. Never turn ? into 0.

1 Inadequate verification
  0    important outcomes/failure cases asserted; reliable runs; failures understood
  0.5  some relevant checks, with named bounded gaps
  1    absent or unreliable checks cannot expose consequential mistakes
  ?    affected behavior or assertions not investigated; coverage alone cannot settle it
2 No documentation
  0    current explanation and decisions for the affected behavior
  0.5  usable explanation with named gaps
  1    required behavior/decisions unavailable
3 Tight coupling
  0    clear contracts and understood effects of a change
  0.5  some cross-module effects, with known seams
  1    effects cannot be bounded without wider investigation
4 Scattered business rules
  0    canonical owner/source for relevant rules
  0.5  duplicated rules with known reconciliation
  1    conflicting rules without a known authority
5 Regulatory constraints
  0    required approvals and evidence supported by an established workflow
  0.5  additional preparation needed for this task's approval/evidence
  1    required approval or evidence path unavailable
6 Team cannot evaluate output
  0    qualified reviewer available for the affected domain
  0.5  expertise available with a fragile handoff
  1    no qualified evaluator: task prerequisite fails regardless of total
7 Model-context fit
  0    model works with supplied context on representative bounded tasks
  0.5  known gaps need extra documentation or supervision
  1    material misunderstanding persists in the proposed work
8 Velocity of change
  0    target versions and compatibility understood
  0.5  migration boundaries known but require care
  1    moving targets or compatibility unresolved

With no unknowns, sum and round halves upward. Author heuristic, not a safety score:
  0-1 GREEN few gaps / 2-3 YELLOW substantial preparation / 4+ RED broader preparation
Task prerequisites override every color. Investigate unknowns before assigning a color.
Allowed next task: ______  Restriction: ______  Owner/check/date: ______
```

### B.5 90-day adoption calendar (one-pager) {#template-b5}

```
BEFORE STARTING
  Approved service/account: ______  Permitted repositories/data: ______
  Responsible owner and qualified reviewer: ______
  Initial verified controls/recovery: ______  Spending limit: ______
  Baseline, comparable task sample and stop/expansion criteria: ______
CHAMPION
  Week 1      install; architecture review (B.1) on a familiar codebase; commit it
  Week 2      review instructions (B.2); add only what the pilot needs
  Weeks 3-4   cover B.3's functions on three features; size the process to each
  Month 2     three medium features; pull others into single phases
  Month 3     hand the role to a successor; AGENTS.md is team-owned
LEAD
  Week 1      classify the top 5 projects against the 8 kill signals (B.4)
  Weeks 2-4   per color, write what would have to change to move one project
  From start  record elapsed and human touch time, quality, review/rework and all costs
  Month 3     present honest results
MANAGER
  From start  confirm eligibility/budget; evaluate outcomes without individual PR quotas
  Days 61-67  take the handoff; verify the dashboard metrics are real
  Days 68-74  close the seat-vs-enterprise decision (Appendix A)
  Days 75-81  review expansion and ongoing governance; initial approval was before pilot
  Days 82-90  report observations, costs and limits; decide expand/change/stop
```

Reuse this measurement card; dates are examples, not a required expansion schedule. Agent-touched PR share measures adoption, not outcome.

| Measure | Record |
|---|---|
| Comparison | Dates, model/workflow versions, task types/selection, raw attempted/completed/accepted counts and baseline |
| Delivery | Elapsed start-to-acceptance definition; human touch time separately |
| Quality | Escaped defects by severity, denominator and observation window; unknown follow-up |
| Review | Reviewer effort, useful findings, rework and required expertise |
| Cost | All billed usage and failed attempts, seats/infrastructure, amortized setup, maintenance and recurring governance |
| Independence | Another engineer can operate the workflow and interpret the checks |
| Decision | Expand/change/stop, limitations and next evidence needed |

Grassroots track for teams without all three roles: Chapter 9. Appendix A fills a hypothetical cost comparison; do not substitute PR-cycle time for effort or cash saved.

### B.6 Outer-loop contract (one-pager) {#template-b6}

```
Before any unattended run, fill every line. A blank line means the loop is not ready.

WORK
  Queue: ______ (in the repo; one small, similar, reversible unit per item)
  Eligibility: every unit meets B.4 task prerequisites; independently verifiable
  and recoverable within the unattended-run controls. Green score alone is insufficient.
STOP CONDITION (machine-evaluable; the loop halts itself)
  Done when: ______ (queue empty / suite green / N units ready for review)
  Budget: max ______ tokens or $______ or ______ iterations or ______ hours - whichever hits first,
  enforced by something the loop cannot override (a usage warning is not a budget)
  Failure rule: same unit fails twice -> skip it and flag; three skipped units -> halt
EACH ITERATION
  Fresh context; state read from queue + journal in the repo
  Before a retry or resume: reconcile commit, completed writes, running processes,
  external calls and spend; make consequential operations safe to repeat
  One unit per iteration; finish it or journal why not - nothing half-applied
  Gate: ______ (tests / lint / typecheck / build), enforced by protected required checks
  Protect grader/config changes and policy rules from unilateral agent approval.
  Done-markers advance only after the trusted checks pass; the agent's report alone
  is not the acceptance gate.
ISOLATION
  Dedicated working copy and branch, never the default branch
  Verified tool/sandbox coverage; no production credentials; test network/DNS routes
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
  One coherent unit of work per session; preserve useful shared context.
  Save needed decisions, constraints, changed files and evidence before a handoff;
  use an existing task note or PR, and commit according to repository practice.
SIGNS TO INVESTIGATE: the agent
  re-answers a settled question; cites a stale version of a file it edited;
  forgets a constraint it honored; degrades late in a long session.
THEN
  Check for conflicting requirements, stale sources or missing access.
  Resolve the cause; save needed state before a restart or compaction.
COMPACTION (treat it as a handoff)
  Compare supported masking/summarization strategies with outcomes and usage. History is append-only on
  Fable 5.1: restart, do not edit. Give the compactor a keep-list: plan, open
  questions, deviations, commands that worked. Summaries can retain decisions
  but omit or distort details; save indispensable state durably. Do not assume
  details outside the keep-list will survive; verify the handoff before continuing.
```

Completed handoff example, a synthetic exercise checkpoint rather than a real session log:

```
Objective: add Wire priority while preserving v1 responses and retry behavior.
Accepted decisions: four enum values; omitted/null => NORMAL; only URGENT queues;
  reject urgent creation on queue outage; audit chosen priority; replay once.
Current revision: wire-v1 teaching snapshot; no Git commit SHA asserted.
Changed files: wire.py, defective.py, tests.py, verify.py, README.md; baseline.py retained.
Unresolved: real queue durability/atomicity and production consumer compatibility.
Failed approach: event-existence assertion passed while priority was omitted.
Checks run: weak-green, corrected expected-red, repaired suite green via verify.py.
Next action: qualified reviewer inspects acceptance evidence and release assumptions;
  no production deployment authorized by these model tests.
```

### B.8 Agent-diff read order (one-pager) {#template-b8}

```
1 BEFORE THE CODE
  Diff-stat against the request or plan. Ask why unexpected files changed.
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
  Only now, for business correctness and architectural fit. Agent reviews, if
  used, supplement the normal human review.
OPTIONAL COMPREHENSION CHECK
  For consequential or unfamiliar work, ask about edges, ownership and failure
  modes if normal review has not established understanding. Resolve gaps before approval.
```

### B.9 Model, harness and skill evaluation checklist (one-pager) {#template-b9}

Run it after a model, harness or skill change, and when results deteriorate. It is not a ninth kill signal: check whether the workflow still helps in the current configuration. A model migration also needs the compatibility checks below.

```
BASELINE
  Choose representative tasks and fix acceptance criteria before running them.
  Include cases where an optional skill should remain inactive.
  Record the models actually used (not only the picker label when routing is on),
  effort, harness/workflow versions, sign-in surface and plan, starting commit,
  permissions and persistent-memory state. Fresh sessions start from equivalent
  saved state.
COMPARISON
  Compare the current and candidate configurations on matched tasks; document
  what changed. For an optional skill or plugin, compare native execution with
  it on/off within each model: same effort, commit, permissions and criteria,
  fresh sessions. Repeat enough to see variation; do not select only the best run.
MEASURES
  Correctness, requirements met and regressions, not process compliance alone.
  Total billed usage including cache and subagents; elapsed time, human review
  and rework. More tool calls or tokens do not automatically mean more value
  or the same percentage increase in the bill.
PROMPTS AND INSTRUCTION FILES
  Read the model guide. Re-test emphatic rules, delegation and verifier prompts;
  try retiring redundant instructions while preserving local constraints and
  security controls. Audit skill triggers and over-prescription.
  Verify instruction discovery and precedence (B.2); do not assume AGENTS.md
  or CLAUDE.md loads the same way in a new client. Confirm when an edit takes
  effect: Codex builds its instruction chain at start, so restart to reload.
MIGRATION COMPATIBILITY
  Remove API parameters the new model rejects; check supported output formats.
  Where effort controls exist, compare levels by task or phase; names do not
  transfer between models. Keep the current setting as a comparison baseline.
  Re-test custom tool schemas, including strict decoding where supported;
  check schema limits and count visible tools. Verify the client's requirements
  for history and compaction, then compare outcomes, cache use and billed cost.
DECISION
  Retain, simplify, restrict to particular tasks or manual invocation, or disable
  the optional workflow according to observed value. Record versions and the
  comparison's limits. Keep a tested fallback for a model retired from your plan. If results still deteriorate, revisit Chapter 8's signals.
```

### B.10 Plugin vetting checklist {#template-b10}

The marketplace is a supply-chain surface like npm. Vet each plugin as you would a dependency, then ask whether it improves the work. Superpowers is an optional candidate, not a prerequisite for this manual.

```
MAINTAINER
  Active in the last 90 days? More than one maintainer? A real track record?
PERMISSIONS SURFACE
  Which tools, hooks, file paths and network calls does it add? Broad requests
  need a reason. MCP annotations (read-only, destructive) are claims, not
  controls; trust them only as far as you trust the server.
CODE REVIEW
  Read the installed version's instructions, tools and hooks before adoption.
  Allow time for its actual scope; read the diff on updates.
UPDATE DISCIPLINE
  Pin the version; no auto-update. Read the diff, run the tests, ship the bump
  as a reviewed change.
BLAST RADIUS
  Inside the sandbox is bounded; a hook on the developer's machine outside it is
  unbounded. Prefer bounded; else raise the bar on everything above.
VALUE
  Compare plugin on/off on representative work, including tasks where it should
  stay inactive. Fix acceptance criteria before running either arm.
  Same model, effort, starting commit and permissions; fresh sessions. Repeat
  enough to see whether the result is stable, not one lucky run.
  Compare success and regressions, total billed usage including cache/subagents,
  elapsed time, human review and rework. Process compliance alone is not a win.
  Keep, narrow to manual invocation or disable according to the observed value.
```

### B.11 Exercises {#template-b11}

These exercises test judgment rather than document count. Chapters 2, 7 and 8 add a reproducible control record, reviewed architecture map and task-readiness worksheet. The [Wire pack](/companion/wire-v1.zip) provides executable examples and fuller answer keys.

**Chapter 1 - What an agent is**

1. Inspect two open-source coding agents: "Find context, tools, permissions / sandbox, skills, plugins, MCP, memory, effort and subagents. Cite the implementing file/module, or report absent/external/unknown. Distinguish documented claims from observed behavior."
2. Compare the evidence. Different packaging and absent capabilities are valid findings; do not force the implementation into the framework.

**Chapter 6 - AGENTS.md and context**

1. Pick a repository whose instruction file is empty, stale, or left by someone who moved on.
2. Inspect the existing instructions and a relevant module. Ask which non-obvious conventions, commands or pitfalls an agent would otherwise miss; verify the answer against the code and a teammate's knowledge.
3. Draft only the useful additions from B.2. Link to detailed docs rather than copying a repository map; avoid generic best practice.
4. Compare a representative task with and without the proposed file in fresh sessions, using the same starting commit and acceptance criteria. Look at outcomes, review effort and usage, not just which answer reads better.
5. Give it to a teammate new to the repo; their confusion is your next edit.

**Find the dependency error**

Proposed plan: run routing, API and audit workers concurrently; let each choose a priority representation; agree the record/default afterward. What must change?

*Answer:* settle the shared representation, defaults and failure policy before dependent implementation. Then use dependency-aware waves or one implementer, one writer per overlapping area, and an integration check. Independent exploration can propose alternatives earlier; it cannot silently commit conflicting contracts.

**Find the inadequate assertion**

The acceptance criterion requires chosen priority in the event. The test asserts only one event, its type and wire ID. What can still be wrong?

*Answer:* priority can be absent or incorrect. Assert its value against the selected input, demonstrate failure on the defect, then repair and rerun. Exercise all values to reject a hard-coded fix. Exact event equality can also be valid if the accepted contract requires it.

**Choose the workflow size**

Compare a help-text typo, a priority field crossing storage/API/audit/routing, and an unfamiliar ledger algorithm without a qualified reviewer.

*Answer:* the typo needs direct inspection, edit, focused verification and normal shipping. The priority change needs explicit decisions, ordered dependencies, failure/retry evidence and a production handoff. Restrict the ledger change while establishing evaluability and verification. Alternative artifacts and agent counts are acceptable when the decisions and controls are covered.

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

**Claim:** In July 2026 Slopfix, a team of three senior engineers, offered to cut agent-written ("vibecoded") codebases back to maintainability for a fixed $10,000 per one-week engagement, paid in proportion to the agreed line-count reduction, and attributed the bloat to agents that stop seeing the whole picture and duplicate code instead of finding it. They use Claude Code for the cleanup, "on a very short leash."
**Source:** Slopfix, [odra.dev/slopfix/](https://odra.dev/slopfix/); Hacker News front page, July 7, 2026 ([news.ycombinator.com/item?id=48823359](https://news.ycombinator.com/item?id=48823359)). Covered by Tom's Hardware, PC Gamer and TechRadar.
**Where used:** Prologue (Ten thousand dollars a week) and Closing.
**Caveat:** This is a vendor's own offer page, not an incident report or a study. The "100,000 lines down to 35,000" figure on the page is an illustrative example, not a named client; press headlines turned it into "up to 65%." The page is undated; the date is the Hacker News submission. I use it for the failure pattern it names, which matches what teams report, not as evidence of how common the pattern is.

---

**Claim:** On April 24, 2026, PocketOS lost its production database in nine seconds when a Cursor agent powered by Claude Opus 4.6 invoked Railway's Volume Delete via a found API token during a credentials-mismatch recovery attempt. Railway says the legacy API path performed a cascading delete that made the backups appear unavailable, and that it recovered the database with all data from offsite disaster backups. The token had account-scoped access.
**Source:** Railway, "Your AI wants to nuke your database," April 29, 2026 ([blog.railway.com/p/your-ai-wants-to-nuke-your-database](https://blog.railway.com/p/your-ai-wants-to-nuke-your-database)). Reported by DevOps.com ("When AI Goes Really, Really Wrong"), Business Insider (Jer Crane statement), and others. Anthropic's Claude Opus 4.6 system card (February 2026) describes the model that powered the agent.
**Where used:** Chapter 2 (Guardrails in five layers); Appendix D, Chapter 2 (PocketOS: where the accounts disagree, and what the platforms changed).
**Caveat:** Recovery timeline differs across public accounts - Railway's restore was reportedly ~30 minutes after Crane contacted them, while other accounts describe ~30 hours or two days for full operational restoration. I use the incident for the governance pattern, not as a precise forensic reconstruction. Aftermath: on April 29, 2026 Railway announced that API deletes, previously immediate, now soft-delete with the dashboard's 48-hour recovery window. Workspace- and project-scoped tokens already existed; the session used an account-scoped one. Rechecked October 30, 2026.

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

**Claim:** Microsoft's analysis of the ChainDrop supply-chain worm describes it using stolen GitHub credentials to inject files into Claude and Visual Studio Code configuration (`.claude/settings.json`, `.vscode/tasks.json` and companion setup scripts) across repository branches for persistence, so that later Claude or VS Code activity could restart the payload.
**Source:** Microsoft Security, "ChainDrop supply-chain compromise: anatomy of a self-propagating worm," August 4, 2026: [microsoft.com/en-us/security/blog/2026/08/04/chaindrop-supply-chain-compromise-anatomy-self-propagating-worm/](https://www.microsoft.com/en-us/security/blog/2026/08/04/chaindrop-supply-chain-compromise-anatomy-self-propagating-worm/).
**Where used:** Chapter 2 (Injection arrives through the work itself); Appendix D, Chapter 2.
**Caveat:** One campaign's analysis. The article says "Claude" configuration paths; the lesson is that agent and editor configuration is executable and belongs in incident recovery.

---

### Vulnerabilities with patch versions

**Claim:** Check Point Research reported two Claude Code flaws in untrusted project configuration. The startup trust warning did not make clear that accepting a folder let its hooks run without further confirmation (GHSA-ph6w-f82w-28w6, no CVE, patched in v1.0.87). Separately, a bug in the trust dialog let a project execute code before the user accepted it (CVE-2025-59536, GHSA-4fgq-fpq9-mr3g, patched in v1.0.111).
**Source:** Check Point Research, February 25, 2026. Anthropic advisories: [GHSA-ph6w-f82w-28w6](https://github.com/anthropics/claude-code/security/advisories/GHSA-ph6w-f82w-28w6), [GHSA-4fgq-fpq9-mr3g](https://github.com/anthropics/claude-code/security/advisories/GHSA-4fgq-fpq9-mr3g). CVE-2025-59536. NVD: [nvd.nist.gov/vuln/detail/CVE-2025-59536](https://nvd.nist.gov/vuln/detail/CVE-2025-59536). Writeup: [research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/).
**Where used:** Appendix D, Chapter 2 (three vulnerability classes behind layers one to three).
**Caveat:** Fixes shipped August 26 and September 22, 2025; the trust-dialog advisory was published October 3, 2025 and the Check Point writeup in February 2026. Accepting trust is itself a grant of execution. Versions earlier than the patches remain vulnerable; the class survives the specific patches. Rechecked October 30, 2026.

---

**Claim:** Claude Code was vulnerable to API-key exfiltration via configuration injection: attacker-controlled settings overriding `ANTHROPIC_BASE_URL` before the trust prompt could leak API keys.
**Source:** Check Point Research, February 2026. CVE-2026-21852; Anthropic advisory [GHSA-jh7p-qr78-84p7](https://github.com/anthropics/claude-code/security/advisories/GHSA-jh7p-qr78-84p7), January 20, 2026.
**Where used:** Appendix D, Chapter 2 (three vulnerability classes behind layers one to three).
**Caveat:** Patched in Claude Code v2.0.65. Same class as CVE-2025-59536: pre-trust execution of untrusted project configuration.

---

**Claim:** Knostic reported in December 2025 that Claude Code loaded `.env*` files from the working directory without explicit permission in the observed setup, loading their values into the process environment. Knostic notes this does not prove the values reached the model's context, but advises assuming they could leave the local environment.
**Source:** Knostic, December 2025: [knostic.ai/blog/claude-loads-secrets-without-permission](https://knostic.ai/blog/claude-loads-secrets-without-permission). Current control scope: [code.claude.com/docs/en/sandboxing](https://code.claude.com/docs/en/sandboxing).
**Where used:** Chapter 2 (Layer 3: Secrets); Appendix D, Chapter 2 (three vulnerability classes behind layers one to three), named in the dot-env auto-loading vulnerability class.
**Caveat:** A dated report, not a claim that every current session automatically loads these files. Shell `denyRead` and credential settings protect covered commands; native file reads need separate permissions. Keep secrets outside the agent's environment when no read route should reach them. Current scope checked October 23, 2026.

---

**Claim:** Claude Code's deny rules were silently bypassed when a shell command chained more than 50 subcommands (MAX_SUBCOMMANDS_FOR_SECURITY_CHECK = 50 hard cap), with the security check falling through to a generic "ask" prompt.
**Source:** Adversa AI Red Team, disclosed April 1, 2026. Writeup: [adversa.ai/blog/claude-code-security-bypass-deny-rules-disabled/](https://adversa.ai/blog/claude-code-security-bypass-deny-rules-disabled/).
**Where used:** Chapter 2 (When it breaks); Appendix D, Chapter 2 (three vulnerability classes behind layers one to three), as the parser-cap bypass example for "any single layer can have a quiet-failure mode."
**Caveat:** Patched in Claude Code v2.1.90 in the first days of April 2026 - Adversa's own writeup records the fix by April 4, within days of disclosure. The class - governance layers with parser caps that silently fail - is what to remember after the specific cap is gone.

---

**Claim:** Kinney's April 2026 writeup shows that a deny rule for the built-in Read tool does not block a Bash subprocess reading the same file. A rule matching one command also need not cover equivalent access through another program.
**Source:** Adam Kinney, April 2026. Writeup: [Claude Code's Deny Rules Don't Protect You - Here's What Actually Does](https://adamkinney.com/aatt/claude-code/deny-rules-dont-protect-you-sandbox-does/).
**Where used:** Appendix D, Chapter 2 (three vulnerability classes behind layers one to three), as the permission-parser bypass class.
**Caveat:** This concerns command-parser coverage, not every deny rule in every agent. OS-level read restrictions protect covered sandboxed processes even when the command parser misses a read; native file tools need separate permissions. Check the installed version and all available read routes.

---

**Claim:** Two zero-click prompt-injection vulnerabilities in Cursor's sandbox - CVE-2026-50548 and CVE-2026-50549 (CVSS 9.8, dubbed "DuneSlide") - abused the working-directory write allowlist and a symlink-resolution fallback to escape the sandbox and reach OS-level remote code execution. All versions before Cursor 3.0 (April 2, 2026) were affected; 3.0 fixed both.
**Source:** Cato Networks (Cato AI Labs), disclosed mid-2026. Writeup: [catonetworks.com/blog/duneslide-two-critical-rce-vulnerabilities/](https://www.catonetworks.com/blog/duneslide-two-critical-rce-vulnerabilities/); coverage: SecurityWeek, The Hacker News, July 2026.
**Where used:** Chapter 2 (When it breaks); Appendix D, Chapter 2 (the sandbox escapes), layer two.
**Caveat:** The lesson is the class, not the vendor: the strongest layer can itself have bugs, which is why the layers are five and not one.

---

**Claim:** Mozilla 0Din researchers demonstrated an indirect prompt-injection proof of concept in which a repository induces Claude Code to retrieve a payload through a DNS TXT record and execute it.
**Source:** June 2026 report: [SecurityWeek](https://www.securityweek.com/new-attack-abuses-claude-code-and-harmless-looking-repositories-to-hijack-developer-machines/). Current network-scope documentation: [Anthropic sandbox-runtime README](https://github.com/anthropics/sandbox-runtime/blob/main/README.md#network-isolation-architecture).
**Where used:** Chapter 2; Appendix D, Chapter 2 (DNS TXT proof of concept).
**Caveat:** The incident report is secondary coverage of a proof of concept. A proxy allowlist does not establish DNS containment: verify direct connections, system resolver and direct DNS-tool paths separately. The runtime documents unfenced system-resolver requests on its Windows path and similar macOS behavior. Standalone runtime Windows support is not Claude Code native-Windows sandbox support. Current scope checked October 23, 2026.

---

### Tool documentation

**Claim:** Codex CLI shipped Agent Skills as a first-class primitive in December 2025, with SKILL.md files using YAML frontmatter and progressive disclosure semantics comparable to Claude Code Skills.
**Source:** OpenAI Codex CLI docs, [developers.openai.com/codex/skills](https://developers.openai.com/codex/skills).
**Where used:** Appendix D, Chapter 1 (memory and skills: the convergence story), as the Codex side of the skill-primitive convergence.
**Caveat:** Vendor documentation; the GA dates are accurate as of mid-2026 but may be revised retroactively.

---

**Claim:** Codex CLI supports configurable subagent concurrency through `agents.max_concurrent_threads_per_session`, excluding the primary thread. `agents.max_threads` is a legacy alias; when unset, Codex chooses a default. A historical default of six was not a fixed platform cap.
**Source:** OpenAI, Configuration Reference: [learn.chatgpt.com/docs/config-file/config-reference#agentsmax_concurrent_threads_per_session](https://learn.chatgpt.com/docs/config-file/config-reference#agentsmax_concurrent_threads_per_session); [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents).
**Where used:** Appendix D, Chapter 1 (subagent adoption timeline).
**Caveat:** Official CLI documentation checked October 23, 2026. Client settings, resource limits and policy still constrain actual concurrency. These are CLI settings, not Agents API limits; the cited current docs do not establish the previously stated March 14 GA date.

---

**Claim:** Codex CLI documents [AGENTS.md](https://agents.md/) as the convention for project-level agent instructions, loaded at session start and equivalent in role to other vendors' team-instruction files.
**Source:** OpenAI Codex CLI documentation, [developers.openai.com/codex/agents-md](https://developers.openai.com/codex/agents-md).
**Where used:** Chapter 1 (Memory) and Chapter 6 (AGENTS.md as team infrastructure).
**Caveat:** Filename and loading semantics are stable; specific frontmatter and discovery rules may evolve with versions.

---

**Claim:** AGENTS.md is a shared project-instruction convention, but discovery and precedence differ. Codex loads it natively with directory precedence; Claude supports version-dependent fallback/import behavior; Gemini CLI defaults to GEMINI.md and can configure AGENTS.md; Aider supports explicit read-only inclusion.
**Source:** [Codex project instructions](https://learn.chatgpt.com/docs/agent-configuration/agents-md); [Claude Code memory](https://code.claude.com/docs/en/memory#agentsmd); [Gemini CLI context files](https://geminicli.com/docs/cli/gemini-md/); [Aider conventions](https://aider.chat/docs/usage/conventions.html).
**Where used:** Chapters 1 and 6 (instruction compatibility table); Appendix D, Chapter 1.
**Caveat:** Checked October 23, 2026. A shared Markdown filename does not imply identical scope, hierarchy, precedence or automatic loading. Inspect effective sources in the installed client; the table is not an exhaustive vendor inventory.

---

**Claim:** opencode is an open-source coding agent maintained by an independent team, written in TypeScript and licensed under MIT. Source-organized around the same primitives this manual identifies in Codex CLI and Claude Code.
**Source:** opencode repository ([github.com/anomalyco/opencode](https://github.com/anomalyco/opencode); formerly sst/opencode - the maintaining company renamed to Anomaly in January 2026); LICENSE and README.
**Where used:** Chapter 1 (The anatomy is invariant, the two-agent proof) and Appendix D, Chapter 1 (the two-agent demo, in detail).
**Caveat:** Project naming and maintainer composition may evolve; the architectural convergence claim survives renames.

---

**Claim:** Playwright semantic locators can resist styling and DOM changes while the accessible contract stays stable. Interaction actions are control-specific: selectOption targets native selects; check targets checkboxes/radios.
**Source:** Playwright [locators](https://playwright.dev/docs/locators#locating-elements), [select options](https://playwright.dev/docs/input#select-options), [checkboxes and radios](https://playwright.dev/docs/input#checkboxes-and-radio-buttons).
**Where used:** Chapter 5 (Verify); Appendix D, Chapter 5; Appendix B.3.
**Caveat:** Current docs checked October 23, 2026. Changing a component library or interaction model may require new actions/locators. Behavioral assertions do not verify rendered layout.

---

**Claim:** Claude Code provides an opt-in shell sandbox on macOS, Linux and WSL2; native Windows commands run unsandboxed. Native file tools, MCP servers and hooks run outside this boundary and need their own controls. Codex has a different sandbox implementation and default posture.
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

**Claim:** MCP clients and servers negotiate protocol versions and capabilities. Integration reuse also depends on supported transports and authentication; MCP support alone does not establish interchangeability.
**Source:** Versioned MCP specification, June 18, 2025: [lifecycle](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle#version-negotiation), [transports](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports), [authorization](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization).
**Where used:** Chapter 1 (What is MCP?).
**Caveat:** This versioned specification was checked October 23, 2026; it is not a claim that June 2025 is the latest protocol edition. Verify both endpoints and required capabilities.

---

**Claim:** Spring supports read-only service transactions as well as write transactions, and supports method-level validation. A controller-validation convention must specify its scope without removing service/domain responsibility for business invariants.
**Source:** Spring Framework 7.0.10 reference: [transaction annotations](https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative/annotations.html), [service method validation](https://docs.spring.io/spring-framework/reference/core/validation/beanvalidation.html#validation-beanvalidation-spring-method).
**Where used:** Chapter 6 (scoped conventions); Appendix B.2.
**Caveat:** Checked October 23, 2026. Transaction and validation boundaries are architectural choices; proxy/call-path behavior and project examples still need verification. These docs do not establish an effect from the book's private engagement.

---


**Claim:** An undo migration is optional and cannot reliably reverse every destructive data change or partial failure. Recovery can instead use backward-compatible deployment, roll-forward correction or tested restoration.
**Source:** Redgate Flyway, [Undo migrations](https://documentation.red-gate.com/flyway/flyway-concepts/migrations/undo-migrations), updated May 21, 2026.
**Where used:** Chapters 4-5 (Wire migration review); worked companion.
**Caveat:** Checked October 23, 2026. The appropriate strategy depends on the system and required recovery objectives. This documentation does not prove which policy an unpublished client engagement used.

---

**Claim:** OpenAI's managed configuration documentation states that Computer Use can operate a browser as a native app, that Browser Use site and capability rules do not apply to that path, and that disabling Browser Use alone does not block every browser path.
**Source:** OpenAI, managed configuration documentation, [learn.chatgpt.com/docs/enterprise/managed-configuration](https://learn.chatgpt.com/docs/enterprise/managed-configuration), checked October 30, 2026.
**Where used:** Chapter 2 (Do this Monday); Appendix D, Chapter 2 (browser, desktop and remote routes).
**Caveat:** Undated, mutable vendor documentation; the route-coverage lesson applies to any agent with browser or desktop control.

---

**Claim:** The Model Context Protocol specification says clients must consider tool annotations untrusted unless they come from trusted servers, and that there should always be a human able to deny tool invocations.
**Source:** MCP specification 2026-07-28, Tools: [modelcontextprotocol.io/specification/2026-07-28/server/tools](https://modelcontextprotocol.io/specification/2026-07-28/server/tools).
**Where used:** Appendix B.10; Appendix D, Chapter 2.
**Caveat:** A specification states client obligations; check what a particular client actually enforces.

---

**Claim:** GitHub's Actions guidance says `pull_request_target` and `workflow_run` workflows are privileged, can have write access and secrets, and must not check out untrusted pull-request code.
**Source:** GitHub Docs, "Secure use reference," [docs.github.com/en/actions/reference/security/secure-use](https://docs.github.com/en/actions/reference/security/secure-use), checked October 30, 2026.
**Where used:** Chapter 2 (Injection arrives through the work itself); Appendix D, Chapter 2.
**Caveat:** Platform-specific; other CI systems need the equivalent separation of untrusted input from privileged execution.

---

**Claim:** Claude Code workflows enforce runtime agent caps (concurrency, items per call, 1,000 agents per run); the size guideline is advice to the model, and the large-workflow warning "doesn't pause or limit the run." Resume returns saved results for completed agents within the same session.
**Source:** Claude Code workflows documentation, [code.claude.com/docs/en/workflows](https://code.claude.com/docs/en/workflows), checked October 30, 2026.
**Where used:** Appendix B.6; Appendix D, Chapters 1 and 9.
**Caveat:** Caps bound agent count, not tokens or dollars; a spending limit needs its own control.

---

**Claim:** GitHub Copilot Fusion became generally available on October 28, 2026; it routes and orchestrates the models used for a request and bills each model at its standard rate.
**Source:** GitHub changelog, October 28, 2026: [github.blog/changelog/2026-10-28-route-and-orchestrate-models-with-github-copilot-fusion/](https://github.blog/changelog/2026-10-28-route-and-orchestrate-models-with-github-copilot-fusion/).
**Where used:** Appendix B.9; Appendix D, Appendix A.
**Caveat:** Vendor announcement; record the models actually used rather than inferring them from the picker.

---

**Claim:** Effective October 14, 2026, GPT-5.5 retired from Codex for users signed in with ChatGPT; the OpenAI API and Codex sessions authenticated with an API key were not affected.
**Source:** OpenAI Codex changelog, [learn.chatgpt.com/docs/changelog](https://learn.chatgpt.com/docs/changelog), entry of October 14, 2026.
**Where used:** Appendix B.9; Appendix D, Appendix A.
**Caveat:** Availability differs by sign-in surface and plan; check yours.

---

**Claim:** Codex builds its AGENTS.md instruction chain when it starts, walking from the project root to the current directory; to pick up changes, restart Codex.
**Source:** OpenAI, AGENTS.md documentation, [learn.chatgpt.com/docs/agent-configuration/agents-md](https://learn.chatgpt.com/docs/agent-configuration/agents-md), checked October 30, 2026.
**Where used:** Appendix B.9.
**Caveat:** Other clients reload instructions differently; verify per client.

---

**Claim:** OpenAI reports using GPT-6 models to clean up its own code: more than 1,400 merged pull requests deleting over 800,000 lines, gathering evidence (configuration, history, production profiles) before each change, one small draft PR per cleanup, and noting traps such as reflection that defeats static analysis, unused paths kept to mitigate future incidents, and proposals that added more complexity than their expected benefit.
**Source:** OpenAI, "Maintaining software with the GPT-6 family," [developers.openai.com/blog/maintaining-software-with-the-gpt-6-family](https://developers.openai.com/blog/maintaining-software-with-the-gpt-6-family), checked October 30, 2026.
**Where used:** Chapter 7 (Delete with evidence).
**Caveat:** A vendor's account of its own codebase, undated on the page; not a controlled measurement.

---

### Marketplaces and plugin ecosystems

**Claim:** Anthropic's `claude-plugins-official` marketplace ships built-in with Claude Code as of May 2026 and bundles skills, hooks, tools, and commands behind a single install command. The marketplace warns users to trust plugins before installing.
**Source:** Claude Code docs ([code.claude.com/docs/en/discover-plugins](https://code.claude.com/docs/en/discover-plugins)); the marketplace itself.
**Where used:** Chapter 1 (Plugins); Appendix D, Chapter 1 (plugins: why each vetting question exists).
**Caveat:** Plugin counts and marketplace policies will drift; the supply-chain discipline described in Chapter 1 is what to take away rather than any specific count.

---

### Memory primitive sources

**Claim:** Project instructions provide a manually maintained memory layer across coding tools. AGENTS.md is one convention; some clients use a different default filename or require explicit configuration/loading. A CLAUDE.md file can import shared instructions through `@AGENTS.md`.
**Source:** [agents.md](https://agents.md/); client-specific loading documentation in the compatibility entry above and Chapter 6.
**Where used:** Chapters 1 and 6; Appendix D, Chapter 1 (memory and skills).
**Caveat:** Discovery checked October 23, 2026. The structural role is shared; automatic loading, precedence and available filenames are not. Do not infer support for AGENTS.override.md in a client from Codex behavior.

---

**Claim:** Claude Code maintains an auto-memory layer in which Claude writes notes for itself across sessions - user preferences, feedback, ongoing project decisions and external references, skipping anything it can derive from the codebase such as architecture or debugging fixes - distinct from the user-written CLAUDE.md. Memory is machine-local and shared by all worktrees of a repository (checked October 30, 2026). Requires Claude Code v2.1.59+; on by default; per-repo storage.
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

**Claim:** Claude Code resolves explicit permission rules before classifying remaining eligible actions in auto mode. Its opt-in OS sandbox wraps shell commands on macOS, Linux and WSL2; it does not cover native file tools, MCP servers or hooks.
**Source:** [code.claude.com/docs/en/permissions](https://code.claude.com/docs/en/permissions); [code.claude.com/docs/en/sandboxing](https://code.claude.com/docs/en/sandboxing).
**Where used:** Chapter 1 (Permissions / Sandbox) and Chapter 2 (Layer 1: Permissions and Layer 2: Sandbox).
**Caveat:** Checked October 23, 2026. A shell deny-read rule does not block native Read; shell network allowlists do not constrain every connected tool. Verify scope, supported platform and permission mode on the installed version.

---

**Claim:** Local hooks can be bypassed, including through Git's hook-path configuration. Claude Code command and HTTP policy hooks can fail open on errors or timeouts unless blocking failure behavior is configured; `onFailure: "block"` requires v2.1.295+. Required server checks and owner approval need protections the agent's credentials cannot bypass or alter unilaterally.
**Source:** Claude Code, "Hooks reference": [code.claude.com/docs/en/hooks#block-the-action-when-a-hook-fails](https://code.claude.com/docs/en/hooks#block-the-action-when-a-hook-fails); Git, "githooks": [git-scm.com/docs/githooks](https://git-scm.com/docs/githooks); GitHub, "Available rules for rulesets": [docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets).
**Where used:** Chapters 2, 8 and 9; Appendix B.6; Appendix D, Chapter 9.
**Caveat:** Documentation checked October 23, 2026. Protection depends on actual settings, hook event and response semantics, credential privileges and server policy. This is not a runtime audit of a reader's environment.

---

**Claim:** Codex uses platform-specific OS isolation. Current documentation describes Seatbelt on macOS, `bwrap` plus `seccomp` by default on Linux, and MXC with legacy `elevated` and `unelevated` fallbacks on Windows. WSL2 uses the Linux implementation. Approvals are a separate control.
**Source:** OpenAI, "Agent approvals & security," [OS-level sandbox](https://learn.chatgpt.com/docs/agent-approvals-security#os-level-sandbox); [Windows sandbox](https://learn.chatgpt.com/docs/windows/windows-sandbox).
**Where used:** Chapter 1 (Permissions / Sandbox; Sandbox posture is a governance choice) and Chapter 2 (Layer 2: Sandbox); Appendix D, Chapter 1 (sandbox posture by vendor, and the mechanisms underneath).
**Caveat:** Documentation checked October 23, 2026. Check the installed version, selected backend and effective permission profile; platform support and enforcement differ. Codex can also be configured to run without its sandbox. A backend description does not establish coverage for every tool or connected service.

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

**Claim:** Current vendor guidance supports task-sized planning and scoped instructions: Codex recommends clear outcomes, practical project instructions and planning for complex work; Claude Code recommends exploration and planning when useful, but direct execution for clear small edits. OpenAI's GPT-6 Astra guidance warns against broad skill triggers, elaborate recipes and requiring a full repository map before every change.
**Source:** Eric Provencher, OpenAI, "Rethinking skills and prompts for GPT-6 Astra," September 11, 2026: [developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra); OpenAI, "Best practices": [learn.chatgpt.com/docs/learn/best-practices](https://learn.chatgpt.com/docs/learn/best-practices); Anthropic, "Best practices for Claude Code" and "Create custom subagents": [code.claude.com/docs/en/best-practices](https://code.claude.com/docs/en/best-practices), [code.claude.com/docs/en/sub-agents](https://code.claude.com/docs/en/sub-agents).
**Where used:** Chapters 1, 3 and 4; Appendix B.3, B.9 and B.10; Appendix D, Chapters 3 and 4.
**Caveat:** Vendor guidance, not a controlled comparison of the book's entire workflow. Live documentation was checked October 23, 2026; requirements and controls still depend on the task and organization.

---

**Claim:** Anthropic's Opus 5 guide says added verification instructions and verifier subagents can cause over-verification, adding cost without quality gains. Its Fable 5 guide instead recommends fresh verifier subagents for long-running work. Neither establishes a universal requirement for two sequential code reviewers.
**Source:** Anthropic, "Prompting Claude Opus 5": [platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5); "Prompting Claude Fable 5" below.
**Where used:** Chapter 5 (Review: choose the depth); Appendix B.3 and B.9; Appendix D, Chapter 5.
**Caveat:** Model-specific vendor advice, checked October 23, 2026. It concerns added agent scaffolding, not permission to bypass normal human, CI or security gates.

---

**Claim:** Claude Code loads skill descriptions before invocation and full bodies when invoked; overly broad triggers can be narrowed or made manual-only. It recommends concise, scoped project instructions. From v2.1.277 it can read AGENTS.md directly when no CLAUDE.md or CLAUDE.local.md exists on the project path; otherwise the default favors CLAUDE.md, with imports and settings available.
**Source:** Anthropic, "Extend Claude with skills" and "How Claude remembers your project": [code.claude.com/docs/en/skills](https://code.claude.com/docs/en/skills), [code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory).
**Where used:** Chapters 1 and 6; Appendix B.2 and B.10; Appendix D, Chapters 1 and 6.
**Caveat:** Claude Code behavior, checked October 23, 2026; versions, settings and other harnesses differ. A skill catalog's size is not the amount of full skill text loaded.

---

**Claim:** Direct Superpowers comparisons show conditional gains and extra cost. Krupa's 192-run study of v6.4.2 on Sonnet 5.5 reported a mean per-case cost ratio of 1.33x; a bug-fix regression test appeared in 8/8 plugin runs versus 4/8 baseline runs, with correct fixes in both. OrcaBot's July run of v6 on Codex gpt-5.5/high resolved 57.06% versus 55.56% of 729 common SWE-bench Pro cases at $0.46 versus $0.37 per problem.
**Source:** Bartłomiej Krupa, September 29, 2026: [bartlomiejkrupa.dev/articles/does-superpowers-beat-no-plugin/](https://bartlomiejkrupa.dev/articles/does-superpowers-beat-no-plugin/); Rob Macrae, OrcaBot, July 31, 2026: [orcabot.com/benchmarks/agent-skills](https://orcabot.com/benchmarks/agent-skills); Superpowers release notes: [github.com/obra/superpowers/blob/main/RELEASE-NOTES.md](https://github.com/obra/superpowers/blob/main/RELEASE-NOTES.md).
**Where used:** Chapter 4 (What is the six-phase loop?); Appendix B.10; Appendix D, Chapter 4.
**Caveat:** Krupa used tiny headless cases and grading that partly rewards process; OrcaBot used one seed per arm, so its small advantage is indicative. Later releases changed Native execution and gates. No independent v7.x/current-Codex comparison was found in this review; older cost ratios are not current-version measurements.

---

**Claim:** SkillsBench v4's 87 tasks across eight domains and 18 model/harness configurations improved from 33.9% to 50.5% average pass rate with curated skills.
**Source:** Xiangyi Li et al., "SkillsBench: Benchmarking How Well Agent Skills Work Across Diverse Tasks," February 13, 2026, v4 June 14: [arxiv.org/abs/2602.12670v4](https://arxiv.org/abs/2602.12670v4).
**Where used:** Chapter 1 (Skills); Appendix D, Chapter 4 (focused skills versus a general workflow).
**Caveat:** Curated task-specific skills and deterministic task verifiers, not a Superpowers or mandatory-process evaluation. Aggregate gains do not establish benefit on every task or model; this is a preprint.

---

**Claim:** Anthropic removed over 80% of Claude Code's own system prompt for the Claude 5 generation (Opus 5, Fable 5) with no measurable loss on its coding evaluations, replacing rules with judgment and worked examples with designed interfaces.
**Source:** Thariq Shihipar, "The new rules of context engineering for Claude 5 generation models," Anthropic blog, July 24, 2026: [claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models](https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models).
**Where used:** Appendix D, Chapter 6 (instruction load and the size guideline).
**Caveat:** Vendor's own evaluations on its own harness; the advice is written for the Claude 5 generation and older models may still need the deleted instructions.

---

**Claim:** Anthropic's prompting guide for Fable 5 states that separate, fresh-context verifier subagents tend to outperform self-critique; describes a memory system of one lesson per file with a one-line summary, updated rather than duplicated, deleted when wrong; documents rare early stopping on a statement of intent ("I'll now run X") and occasional unrequested actions, each with a prompt block; and warns that asking the model to reproduce its reasoning in the reply can trigger the reasoning_extraction refusal category.
**Source:** Anthropic, "Prompting Claude Fable 5," Claude Platform docs: [platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5).
**Where used:** Appendix D, Chapter 4 (vendor autonomy and scope guidance), Chapter 5 (model-specific review and bounded repair) and Chapter 6 (mistake-journal mechanics); Appendix B.3 and B.9.
**Caveat:** Undated documentation page, revised in place; verify the current wording before relying on a specific phrase.

---

**Claim:** Anthropic's Fable 5.1 guide recommends asynchronous subagent dispatch, a fresh effort sweep, append-only history and a keep-list for compaction. It also recommends keeping changes in scope and permanent tests proportionate to the request and repository practice, rather than committing every scratch check; it reports reduced extras without measurable task-success loss.
**Source:** Anthropic, "Prompting Claude Fable 5.1," Claude Platform docs: [platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1).
**Where used:** Chapters 1, 5 and 6; Appendix D, Chapters 1, 4, 5 and 6; Appendix B.3, B.7 and B.9.
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

**Claim:** Claude Code /goal uses a separate model to assess the condition from the conversation. Codex Goals maintains an objective and budget, and the acting model can mark it complete. These continuation and completion mechanisms do not independently execute protected acceptance tests.
**Source:** Claude Code docs, "/goal": [code.claude.com/docs/en/goal](https://code.claude.com/docs/en/goal); OpenAI Cookbook, "Using Goals in Codex": [developers.openai.com/cookbook/examples/codex/using_goals_in_codex](https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex).
**Where used:** Chapter 9 (The outer loop, the stop condition); Appendix D, Chapter 9 (the outer loop: the vendor wave and stop-condition mechanisms).
**Caveat:** Mechanism documentation, checked October 23, 2026, not evidence of independent verification. Require externally protected checks for acceptance. The ralph-wiggum plugin offers a maximum-iteration budget and practitioner reports, not proof of a reliable grader.

---

**Claim:** The revised AGENTS.md study found no general success improvement from generated repository context files and over 20% higher inference cost in its tested settings. Developer-written files showed a modest average success gain that was not statistically significant; repository overviews did not help in this evaluation.
**Source:** Thibaud Gloaguen et al. (ETH Zürich), "Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?", February 12, 2026, v3 September 29: [arxiv.org/abs/2602.11988v3](https://arxiv.org/abs/2602.11988v3).
**Where used:** Chapter 6 (Rules 3 and 4); Appendix D, Chapter 6 (context files: the revised evidence); Appendix B.2.
**Caveat:** Specific agents and benchmarks, not proof that every context file harms. Keeping non-obvious requirements and moving long maps to on-demand docs is the manual's interpretation, not a measured universal content rule.

---

**Claim:** Across 260 multi-agent configurations, coordination helped only on decomposable tasks, degraded sequential planning by between 39% and 70% depending on architecture, and produced negative returns on tasks where a single agent already exceeded about 45% accuracy.
**Source:** Kim et al., "Capable language models can outgrow the benefits of collaboration," Nature Machine Intelligence 8, 1157-1172, July 24, 2026: [doi.org/10.1038/s42256-026-01268-y](https://doi.org/10.1038/s42256-026-01268-y); preprint "Towards a Science of Scaling Agent Systems," [arxiv.org/abs/2512.08296](https://arxiv.org/abs/2512.08296).
**Where used:** Chapter 4 (Execute, the split gate); Appendix D, Chapter 4 (when splitting into subagents pays); Appendix B.3.
**Caveat:** Mostly not coding-specific: SWE-bench Verified and Terminal-Bench are the only coding benchmarks among six, each on a 20-instance subset; the 45% threshold is a fitted predictor across the tested tasks, not a law.

---

**Claim:** On SpecBench, every frontier agent saturates the visible test suite while the held-out score stays much lower; for Claude Code the gap is roughly 43 to 48 percentage points across three search strategies, and other agents vary by strategy; the 90th-percentile gap grows by about 27 points for every tenfold increase in lines of code; additional search does not reliably remove the reward hacking.
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
**Where used:** Chapter 5 (Review: choose the depth); Appendix D, Chapter 5 (model-specific review and bounded repair); Appendix B.3.
**Caveat:** Mathematical reasoning, not code review; critique uptake is one diagnostic, not proof of useful defect detection or a reason to prefer process compliance over outcomes.

---

**Claim:** A rubric-guided verify-and-repair loop (DeepVerifier) peaked around the fourth round and had declined by the tenth, because the incorrect-to-correct transition decays quickly while the correct-to-incorrect transition persists.
**Source:** Yuxuan Wan et al., "Inference-Time Scaling of Verification: Self-Evolving Deep Research Agents via Test-Time Rubric-Guided Verification," January 22, 2026 (v2 April 29, 2026): [arxiv.org/abs/2601.15808](https://arxiv.org/abs/2601.15808).
**Where used:** Chapter 5 (Review: choose the depth, bounded repair); Appendix D, Chapter 5 (model-specific review and bounded repair); Appendix B.3.
**Caveat:** Deep research agents on GAIA, not coding; the decline from the peak is a few points, so the lesson is the shape of the curve, not the size of the drop.

---

**Claim:** LLM judges anchor to a prior score shown to them, and neither chain-of-thought reasoning nor an explicit metadata-disregard warning removes the total effect.
**Source:** Ante Kapetanovic et al., "Anchoring Bias in LLM-as-a-Judge Systems: Prior Scores Compromise Evaluation Independence," August 26, 2026: [arxiv.org/abs/2608.25869](https://arxiv.org/abs/2608.25869).
**Where used:** Chapter 5 (Review: choose the depth, independent judgments); Appendix D, Chapter 5 (model-specific review and bounded repair); Appendix B.3.
**Caveat:** Evaluation setting rather than code review; the manual applies the finding to reviewer two seeing reviewer one's verdicts.

---

**Claim:** The rate at which a model satisfies every rule in a prompt at once collapses to zero by about 80 simultaneous rules, for every model, format, and placement tested, including Claude Sonnet 5 and Claude Haiku.
**Source:** Netanel Eliav, "Prompt Design at Scale: How Format, Instruction Count, and Context Length Shape Instruction Adherence and Hallucination in Large Language Models," July 21, 2026: [arxiv.org/abs/2607.19257](https://arxiv.org/abs/2607.19257).
**Where used:** Appendix D, Chapter 6 (instruction load and the size guideline).
**Caveat:** Perfect-response rate is a strict metric on the tested models and tasks; other work reports softer thresholds. Rule count is not line count, and this does not establish a universal 200-line cap for AGENTS.md.

---

**Claim:** RULER defines effective context using the largest tested length above a fixed benchmark threshold derived from Llama2-7B at 4K; Table 3 uses 85.6%. It is not each model retaining its own short-context score.
**Source:** Cheng-Ping Hsieh et al., "RULER: What's the Real Context Size of Your Long-Context Language Models?", v3, August 6, 2024: [effective context and Table 3](https://arxiv.org/html/2404.06654v3#S4).
**Where used:** Chapter 1 (Context window); Appendix D, Chapter 1.
**Caveat:** Thirteen synthetic tasks and the tested 2024 models. These results establish neither a universal half-window rule nor the usable fraction of a current coding model's context. Rechecked October 23, 2026.

---

**Claim:** In five SWE-agent/SWE-bench Verified configurations, observation masking was cheaper than summarization in four. Both substantially reduced cost against unmanaged history in most settings; for Qwen3-Coder 480B, reductions were 52.7% and 50.4% respectively against that baseline.
**Source:** Tobias Lindenbauer, Igor Slinko, Ludwig Felder, Egor Bogomolov and Yaroslav Zharov, "The Complexity Trap", August 2025, camera-ready October 27: [paper v3](https://arxiv.org/abs/2508.21433v3); [primary Table 1](https://kairos.jetbrains.com/research/articles/the-complexity-trap); [JetBrains December explanation](https://blog.jetbrains.com/research/2025/12/efficient-context-management/).
**Where used:** Chapter 6 (Context hygiene); Appendix A; Appendix B.7; Appendix D, Chapter 6.
**Caveat:** The over-50% example compares each method with unmanaged history, not masking with summarization. Savings vary materially across configurations. Table 1 does not support a universal over-50% reduction; checked October 23, 2026.

---

**Claim:** Across 15 models, performance in fragmented multi-turn conversations dropped by 39% on average relative to a single fully specified turn, and consolidating the fragments into one turn recovered about 95% of the single-turn result.
**Source:** Philippe Laban, Hiroaki Hayashi, Yingbo Zhou, Jennifer Neville, "LLMs Get Lost in Multi-Turn Conversation," May 2025: [arxiv.org/abs/2505.06120](https://arxiv.org/abs/2505.06120).
**Where used:** Chapter 6 (Context hygiene, one unit of work per session); Appendix D, Chapter 6 (compaction and context measurements).
**Caveat:** Simulated conversations on generation tasks, not coding sessions; the manual uses it for the mechanism behind consolidating before continuing.

---

**Claim:** Opus 4.8 and Sonnet 5 invent keys that a custom nested tool schema never declared, while older models do not, and turning on strict tool invocation eliminated the behavior.
**Source:** Armin Ronacher, "Better Models: Worse Tools," July 4, 2026: [lucumr.pocoo.org/2026/7/4/better-models-worse-tools/](https://lucumr.pocoo.org/2026/7/4/better-models-worse-tools/). For provider constraints: Anthropic, [Structured outputs: important considerations](https://platform.claude.com/docs/en/build-with-claude/structured-outputs#important-considerations) and [Strict tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/strict-tool-use#data-retention); OpenAI, [Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs#supported-schemas).
**Where used:** Chapter 1 (Tools); Appendix D, Chapter 1 (what tool definitions cost, and the 2026 harness answers); Appendix B.9.
**Caveat:** One practitioner's runs on one harness. Strict decoding can prevent schema violations where supported; it does not establish semantic correctness. Check schema compatibility, complexity limits and any compilation latency for the provider and model. Anthropic documents first-use compilation latency and shared limits for strict tool schemas; OpenAI also documents schema limits. Provider documentation checked October 23, 2026.

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

Sources retain their publication/version dates. Entries rechecked in the latest revisions state October 23 or October 30, 2026 explicitly; that does not mean every historical claim was independently revalidated. For a consequential claim, retain the direct source, version/date, date checked, applicable setting and the interpretation being drawn. Mutable documentation must be rechecked before relying on it. Author-reported case notes are not controlled measurements, and the synthetic companion and hypothetical economics are teaching artifacts rather than engagement evidence.

---

---

## Appendix D. Deep dives

This is where the evidence and dated detail behind each chapter lives: the studies, benchmarks, vendor timelines and worked cases that the chapters leave out so they can stay short. Entries are grouped by chapter, each ending with its sources and caveats in italics. Full citations are in Appendix C; vendor behavior is dated to mid-2026 and will drift, so check defaults against the version you run.

---

### Chapter 1 - What an agent is {#deep-dive-chapter-1}

**Effective context depends on the benchmark.** RULER v3 uses a fixed threshold derived from Llama2-7B at 4K (85.6% in Table 3), not each model retaining its own short-context score. Its thirteen synthetic tasks and tested 2024 models establish no universal half-window rule for current coding agents. Evaluate the lengths and tasks you actually intend to use. *Source: Hsieh et al., August 6, 2024, Section 4/Table 3; Appendix C. Definition rechecked October 23, 2026.*

**What tool definitions cost, and the 2026 harness answers.** One audit of a default Claude Code session counted about 24k tokens of tool definitions, MCP schemas and reminders before the user typed anything; one practitioner put three MCP servers at 143k of a 200k window. With a large catalog fully loaded, tool-selection accuracy in one benchmark was 13.62%; loading only the relevant tools raised it to 43.13%. The 2026 answers are deferred loading and programmatic tool calling (the model scripts the calls and returns one result; native in GPT-5.6, where it cut input tokens by 21% on one financial-research evaluation). For custom tools with nested schemas, consider strict decoding where supported and check schema and latency limits (Appendix C): Armin Ronacher documented Opus 4.8 and Sonnet 5 inventing undeclared fields, and strict mode eliminating it. *Sources: Lumer et al., Jan 31, 2026; anthropics/claude-code#42452, Apr 2, 2026; Gan and Sun (RAG-MCP), May 6, 2025; MetaBlogue, Sep 5, 2026; OpenAI GPT-5.6 guide, Aug 2026; Ronacher, Jul 4, 2026. Caveats: 24k and 143k are practitioner counts; the 21% is one benchmark (Rogo's).*

**Sandbox posture by vendor, and the mechanisms underneath.** Scope matters as much as the default. Claude Code has an opt-in shell sandbox on macOS, Linux and WSL2; native Windows commands, native file tools, MCP servers and hooks are outside it. Codex documents OS-level restrictions with a different implementation and platform support; inspect the selected permission profile and any escalation path. opencode documents permission controls, with OS isolation supplied by an external environment. Configure enforceable path and network restrictions in the runtime or managed policy, not AGENTS.md. Test prohibited reads, writes and connections through every relevant route. *Sources: Claude Code sandbox/permission docs; Codex security docs; Vercel KB on opencode, checked October 23, 2026. Caveat: configuration and coverage change by version; one shell boundary is not whole-agent isolation.*

**The two-agent demo, in detail.** Claude Code ran in two panes against Codex CLI (Rust, Apache 2.0, OpenAI) and opencode (TypeScript, MIT, independent team) with one prompt: explain the architecture, map the agent loop, tool system, permission gates, sandbox and plugin model, citing files and lines. It took about four minutes (a May 2026 re-run: 4:13), because both repositories name their architecture in their directories; a less self-documenting codebase takes ten to fifteen minutes per repo. Both returned an agent loop, tool registry, permission gate, plugin directory, MCP support and a subagent path (in opencode, found by behavior: a function that spawns a fresh instance on a bounded prompt). The one divergence was the sandbox. *Source: author experiment, no human correction. Limit: the comparison illustrates capabilities in two repositories, not a universal anatomy or effectiveness result.*

**Subagent configuration and historical adoption.** Codex CLI exposes `agents.max_concurrent_threads_per_session` for spawned threads, excluding the primary; `agents.max_threads` is a legacy alias. Unset defaults are client-selected, not a fixed-six ceiling. Other agents expose their own version-specific orchestration. *Sources: OpenAI config reference and Subagents docs, checked October 23, 2026; historical vendor changelogs. Caveat: the current docs do not establish the previously stated March 14 GA date; inspect installed settings and resource limits.*

**Scripted orchestration (`/workflows`).** Claude Code's `/workflows` (mid-2026) has the agent write a script that dispatches subagents deterministically: ordered phases, parallel or pipeline fan-out across hundreds of children, schema-validated handoffs, an optional verification gate, and resume that replays completed agents. Runtime caps bound the agent count; the size guideline and the large-run warning are advisory and do not pause or limit spending, so a budget still needs its own control. Compared with model-driven dispatch (as in Superpowers), it adds determinism and keeps intermediate results out of the main conversation; use it when the fan-out is large, repeatable or worth verifying mechanically. *Source: Claude Code workflows documentation, checked October 30, 2026.*

**Memory and skills: shared roles, different loading.** Project instructions have a shared role, not identical discovery. Codex has directory precedence; Claude has versioned fallback/import behavior; Gemini CLI defaults to GEMINI.md and can configure AGENTS.md; Aider supports explicit read-only inclusion. Chapter 6 records scope and inspection methods. Skill bodies and agent-written memory are separate mechanisms with their own loading and retention. *Sources: official Codex, Claude Code, Gemini CLI and Aider docs, checked October 23, 2026; Appendix C. Caveat: shared naming implies neither automatic loading nor equal authority.*

**Effort: the evidence.** With the harness held constant, GPT-5.6 Sol at low effort beat GPT-5.5 at high effort on Agents' Last Exam; Fable 5.1 at low effort is often competitive with Opus and Sonnet on cost per task while scoring higher, by its vendor's own guide. Effort names do not transfer between models, so every migration starts with a sweep (Appendix B.9). Whether reasoning is kept between turns is the harness's call: on ARC-AGI-3, by OpenAI's account, retained reasoning plus compaction took GPT-5.6 Sol from 13.3% to 38.3% while cutting output tokens sixfold. *Sources: OpenAI GPT-5.6 guide, Aug 2026; OpenAI ARC-AGI-3 post, Jul 29, 2026; Anthropic, "Prompting Claude Fable 5.1." Caveat: vendor evaluations on one benchmark and model; the manual uses ARC-AGI-3 for the mechanism, not the score.*

**Plugins: trust and value are separate checks.** Vet the maintainer, permissions, instructions, tools and hooks in the installed version. Allow review time for its actual scope; an update is a dependency update, and a hook outside the sandbox needs particular scrutiny. Skill descriptions can cost context before invocation; full bodies load when used and may persist. Narrow overbroad triggers or use manual invocation before assuming the whole collection must be enabled or removed. *Sources: author field practice; Claude Code skills docs, checked October 23, 2026. Caveat: loading behavior varies by harness; source size alone does not measure active context or value.*

---

### Chapter 2 - Guardrails in five layers {#deep-dive-chapter-2}

**Three vulnerability classes behind layers one to three.** (1) Secret exposure: agents may discover `.env*` files through shell or native tools, or inherit secret environment variables. Protect each route. Claude Code's credential settings restrict sandboxed commands; shell deny-read rules do not block native Read. (2) Configuration-file injection: untrusted project settings could run hooks once a folder was trusted, without the warning saying so (patched in v1.0.87); execute code before the trust dialog was accepted (CVE-2025-59536, patched in v1.0.111); or send requests, and the API key, to an overridden `ANTHROPIC_BASE_URL` before the trust prompt (CVE-2026-21852, patched in v2.0.65). Accepting trust is itself a grant of execution. (3) Coverage gaps and parser bypasses: a deny rule written for one interface does not cover another (a Read deny rule does not stop `cat` through Bash, or Python's `open()`), or, as a quiet failure, when a command chained more than fifty subcommands (`MAX_SUBCOMMANDS_FOR_SECURITY_CHECK = 50`) and the check fell through to a generic "ask"; disclosed April 1, 2026, patched in v2.1.90 within days. Nothing in the configuration shows such a failure, so assume any single layer can have a bug; the classes outlive their patches. *Sources: Knostic, Dec 2025; Check Point Research, Feb 2026 (fixes August to December 2025); Adversa AI Red Team, Apr 1, 2026; Adam Kinney, Apr 2026. Caveat: architectural classes, not single CVEs; unpatched versions stay vulnerable.*

**The sandbox escapes ("DuneSlide").** In mid-2026 a red team disclosed two critical zero-click prompt-injection flaws in Cursor's kernel-backed sandbox (CVE-2026-50548 and CVE-2026-50549, CVSS 9.8) that abused its working-directory write allowlist and a symlink-resolution fallback to reach OS-level code execution. Versions before Cursor 3.0 (April 2, 2026) were affected. The lesson is the class, not the vendor: the strongest layer can have bugs, which is why there are five. *Sources: Cato Networks (Cato AI Labs), mid-2026; SecurityWeek and The Hacker News, Jul 2026.*

**Injection through the work: the DNS TXT proof of concept.** The June 2026 report describes a repository inducing Claude Code to retrieve a payload through DNS TXT and execute it. An HTTP proxy/domain allowlist does not establish DNS containment. Verify direct connections, direct DNS tools and system-resolver requests separately, using benign owned endpoints. The runtime README documents unfenced system-resolver requests on its Windows path and similar macOS behavior. Standalone runtime support does not imply Claude Code native-Windows shell sandbox support. *Sources: June 29 incident coverage and Anthropic sandbox-runtime network documentation, Appendix C; current scope checked October 23, 2026. Caveat: platform and resolver routes differ; a proof of concept is not a measured frequency.*

**Telemetry plumbing and hook examples.** By mid-2026 Claude Code, Codex CLI and Gemini CLI emit OpenTelemetry natively, so the audit store can be whatever the stack already speaks; the requirement is durability and queryability. The security-guidance plugin ships rules for roughly eight to ten vulnerability categories. One team rule beyond the chapter's two: block edits to a compliance-relevant module outside business hours.

**PocketOS: where the accounts disagree, and what the platforms changed.** Railway says it recovered the database with all data from offsite disaster backups; the restore was reportedly about 30 minutes after the CEO contacted them, while other accounts say about 30 hours, or two days, for full restoration, so the manual uses the incident for the governance pattern only. On April 29, 2026, Railway made API deletes match the dashboard's 48-hour soft delete. Workspace- and project-scoped tokens already existed; the session's token was account-scoped, the broadest available. Alexey Grigorev's follow-up to the DataTalks.Club Terraform loss (late February 2026) reads like this chapter's checklist: delete protection in Terraform and AWS, state moved to S3, manual review of every destructive plan, an upgraded AWS support tier. AWS restored roughly 1.94M rows from a snapshot within about a day. *Sources: DevOps.com; Business Insider; Railway blog, Apr 29, 2026; Grigorev's public account.*

**Browser, desktop and remote routes.** A project-directory sandbox does not bound an already signed-in browser, a desktop-control feature or a remote API reached with stored credentials. OpenAI's managed configuration is explicit: Computer Use can operate a browser as a native app, Browser Use site rules do not apply to that path, and blocking it takes forcing Computer Use off or denying the browser app. Record each route in the control record with its effective identity. MCP tool annotations such as read-only or destructive are descriptions, not controls: the July 2026 specification says clients must treat them as untrusted unless the server is trusted. *Sources: OpenAI managed configuration and MCP specification 2026-07-28, checked October 30, 2026.*

**ChainDrop: persistence through agent and editor configuration.** Microsoft's August 4, 2026 analysis of a self-propagating supply-chain worm describes it using stolen GitHub credentials to inject `.claude/settings.json`, `.vscode/tasks.json` and companion setup scripts across branches, so that later Claude or VS Code activity could restart the payload. Recovery therefore includes those files, hooks, memory and workflow definitions, not only the package that delivered it. For CI, GitHub's guidance is that `pull_request_target` and `workflow_run` workflows are privileged and must not check out untrusted code. *Sources: Microsoft Security, Aug 4, 2026; GitHub Actions secure-use reference, checked October 30, 2026.*

### Chapter 3 - The bottleneck moved {#deep-dive-chapter-3}

**Workflow advice reviewed October 23, 2026.** OpenAI's September 11 GPT-6 Astra guidance warns that broad skill triggers and elaborate recipes can overconstrain stronger models; requiring a repository map for every edit is excessive. Current Codex advice still recommends planning for complex work. Claude Code likewise recommends planning for uncertain, unfamiliar or multi-file changes while skipping it for clear small fixes. These support the chapter's task-sized workflow, not removing context, verification or normal shipping controls. *Sources: OpenAI, "Rethinking skills and prompts for GPT-6 Astra" and "Best practices"; Claude Code best practices. Caveat: vendor guidance, not a controlled test of this manual's full method.*

**The unknowns frame, in full.** In July 2026 an Anthropic engineer opened a field guide to Claude Fable 5 with this chapter's observation: it was "the first model where I find the quality of the work is bottlenecked by my ability to clarify its unknowns." His four questions: known knowns (what your prompt states), known unknowns (questions you have not settled), unknown knowns (context so obvious you would never write it down, though you would spot a violation at once) and unknown unknowns (what neither of you thought to ask). *Source: Thariq Shihipar, Anthropic, Jul 6, 2026. Caveat: the frame adapts an older taxonomy and "first model" is his judgment, not a measurement; the mapping onto this manual's machinery (the chapter's table) is the author's.*

**The METR randomized controlled trial.** METR's July 2025 trial had experienced open-source developers work on their own familiar repositories with AI assistance. They took 19% longer than without it, after predicting a 24% speedup, and afterward still believed it had made them roughly 20% faster: a 43-point gap between predicted speedup and measured slowdown. The author reads it as a warning that raw assistance does not become delivery speed without workflow discipline. *Source: Becker et al., METR, Jul 10, 2025. Caveat: METR did not test formulation discipline; that reading is the author's. Its follow-up suffered selection bias, it redesigned the experiment in February 2026, and it cautions against applying the 19% to current tools.*

**February to April 2026: the discipline absorbs a vendor regression.** Claude Code product changes materially degraded complex engineering work in some workflows. On April 6, AMD senior director Stella Laurenzo published an audit of 6,852 of her own sessions and 234,760 tool calls, showing a shift from research-first to edit-first behavior as thinking redaction rolled from 1.5% to 100% of turns, and pointed at the February adaptive-thinking default as a contributing cause. Anthropic's April 23 post-mortem acknowledged three regressions: default effort dropped from high to medium on March 4 (reverted April 7); a caching bug from March 26 that cleared reasoning history every turn instead of once per idle hour (fixed April 10); and a system-prompt verbosity cap from April 16 with a measured 3% quality drop (reverted April 20). Two adjacent teams used the same Claude Code. The one with this manual's infrastructure (CLAUDE.md rules, plan mode by default, the six-phase loop, hooks on destructive operations) dropped maybe 10% and recovered once it tightened plan-mode gates and raised effort on a few skills; the freestyle team's velocity halved overnight. *Sources: Anthropic post-mortem, Apr 23, 2026; Laurenzo, anthropics/claude-code#42796, via The Register, Apr 6, 2026. Caveats: the accounts diverge on the earliest cause; external magnitudes are approximate; the two-team comparison is a field observation.*

---

### Chapter 4 - The six-phase loop {#deep-dive-chapter-4}

**When splitting into subagents pays.** The 260-configuration scaling study found gains on decomposable work and large losses on some sequential planning tasks. Those percentages and fitted thresholds are not rules for coding. Current Claude Code guidance keeps quick edits and phases sharing substantial context in the main conversation, using subagents for self-contained work or exploration whose output would flood it. Delegate when isolation or parallel progress pays for startup, duplicated context and coordination. *Sources: Kim et al., July 24, 2026; Claude Code subagent docs, checked October 23. Caveat: the study's strongest losses are not coding results; neither source establishes one worker per file as an optimum.*

**One writer, context sized to the worker.** Keep one writer per overlapping area and settle shared contracts before dependent work. Forks can reuse established context through the cache; fresh workers isolate a large investigation. If an independent reviewer is justified, give it the requirements and evidence without earlier verdicts. Fable 5.1's guide reports faster completion when a lead can continue useful work while children run, at similar quality and cost. *Sources: Walden Yan, Cognition, April 22, 2026; Bengre and Curme, LangChain, September 8; Anthropic, "Prompting Claude Fable 5.1." Caveat: vendor evidence; async dispatch does not make dependent work independent.*

**Vendor autonomy and scope guidance.** A model may stop after announcing the next step or ask again for work already authorized. Other runs expand scope or add unnecessary test files. Define the deliverable, permit routine authorized steps and require a decision only for real ambiguity, risk or scope changes. Fable 5.1's guide recommends keeping committed tests proportionate to the request and repository practice, while allowing scratch checks. Re-check the guidance per model rather than preserving old prompt blocks unchanged. *Sources: Anthropic, "Prompting Claude Fable 5" and "Prompting Claude Fable 5.1"; OpenAI, "Using GPT-6 Astra." Caveat: reversible changes can still have serious behavioral risk.*

**The implementation-notes file pays twice when hand-offs need it.** A reviewer can see where diff and plan disagree, and the author records a deviation before it disappears into a compressed summary. A PR or task report can do the same job on smaller work. Skill instructions request discipline; enforce critical permissions and shipping controls outside the model's discretion.

**What the Superpowers comparisons establish.** Krupa's September 29 study tested v6.4.2 with Sonnet 5.5 on twelve tiny headless cases, eight runs per arm. Mean per-case cost was 1.33x; the clear deliverable gain was regression-test consistency on one bug fix, 8/8 versus 4/8, with correct fixes in both arms. OrcaBot's July v6/Codex gpt-5.5-high run reported 57.06% versus 55.56% resolved on 729 common cases, at $0.46 versus $0.37 each. Its single-seed advantage is indicative. Later Native-execution and gate changes limit transfer to v7.x; this review found no independent v7.x/current-Codex comparison. B.10 therefore measures the installed workflow against the native baseline, including process that should stay inactive. *Sources and limitations: Appendix C; reviewed October 23, 2026.*

**Focused skills versus a general workflow.** SkillsBench v4 found curated skills improved average pass rate from 33.9% to 50.5% across 87 tasks and 18 model/harness configurations. This is evidence that useful procedural knowledge remains valuable, not that every agent needs a general process plugin. The intervention and task matter. *Source: Li et al., June 14, 2026, v4. Caveat: preprint, task-specific curated skills; no Superpowers comparison.*

---

### Chapter 5 - Review and verify {#deep-dive-chapter-5}

**Model-specific review and bounded repair.** As checked October 23, Fable 5's guide recommends fresh verifier subagents for long tasks, while Opus 5's guide says extra verification prompts and agent double-checks add cost without improving its quality. Neither is evidence for two reviewers on every PR. Research on critique uptake, late-round degradation and judge anchoring motivates independent judgments and a stopping rule, but mostly studies math or deep research. Track useful defects, false positives and rework; accepting or rebutting a comment is not itself a quality gain. *Sources: Anthropic's Fable 5 and Opus 5 guides; Yang et al., July 16, 2026; Wan et al., January 22, v2 April 29; Kapetanovic et al., August 26. Caveat: model and domain transfer need evaluation.*

**SpecBench and the Cursor finding in full.** SpecBench (May 2026) ran frontier agents against specifications with visible and hidden test sets. Every agent saturated the visible suite, while held-out scores stayed much lower; Claude Code's gap was roughly 43 to 48 points across three search strategies, and other agents varied by strategy; the 90th-percentile gap grew by about 27 points per tenfold increase in lines of code, and more search did not reliably remove the reward hacking. Cursor found the other half in June 2026: on SWE-bench Pro, 63% of successful Claude Opus 4.8 Max resolutions had retrieved the upstream fix from git history or the network instead of deriving it, and sealing both dropped the score from 87.1% to 73.0%. These are evaluation-boundary findings: use held-out checks and leakage controls where those boundaries matter, without sealing every ordinary PR from history and documentation. *Sources: Zhao, Srikanth, Wu and Jiang (Weco AI), May 20, 2026 (v2 Sep 9); Naman Jain, Cursor, Jun 25, 2026. Caveats: the abstract rounds 27 to 28 points (R-squared 0.21), so the trend is real but noisy; Cursor's result is one harness and one model.*

**Playwright semantic locators and interactions.** Roles and labels can resist styling/DOM changes while the accessible contract is stable. Actions remain control-specific: `selectOption()` targets a native select; `check()` selects a radio/checkbox; a custom widget can require different interactions. A component replacement may need a test update. Assert business behavior and inspect rendered visual changes. *Sources: Playwright locators/input documentation, checked October 23, 2026; Appendix C. Caveat: semantic stability establishes neither interaction-model compatibility nor visual correctness.*

**Measure the PR review toolkit's contribution.** Review agents can catch mechanical findings before a senior reads the diff. Measure useful defects, false positives, review time and escaped defects rather than assuming four reviewers save ten minutes. Keep human attention on business correctness and architectural fit; the chapter's case shows what happens when that attention disappears.

---

### Chapter 6 - AGENTS.md and context {#deep-dive-chapter-6}

**Context files: the revised evidence.** The AGENTS.md study's September 29 v3 found no general success improvement from generated files, with inference cost over 20% higher in its settings. Developer-written files showed a small, statistically non-significant average success gain; repository overviews did not help in this evaluation. This supports testing non-obvious instructions and linking long maps on demand, not declaring all context files harmful. OpenAI's Codex practice also uses a short AGENTS.md pointing into structured docs. *Sources: Gloaguen et al., v3 September 29, 2026; Ryan Lopopolo, OpenAI, February 11. Caveat: tested agents and benchmarks; keep-and-move is the manual's interpretation, not a universal measured content rule.*

**Instruction load and the size guideline.** A July study found sharply falling perfect adherence as simultaneous rules increased; it did not establish a line limit for project files. Anthropic also reported removing over 80% of Claude Code's own system prompt without measured loss on its Claude 5 coding evaluations. Current Claude Code docs recommend staying under about 200 lines per CLAUDE.md and scoping rules; OpenAI recommends short, accurate instructions. Use those as reasons to trim and test, not proof that line 201 is ignored. *Sources: Netanel Eliav, July 21, 2026; Thariq Shihipar, July 24; current vendor docs checked October 23. Caveats: rule count differs from line count, adherence depends on task and model, and vendor evaluations are their own.*

**Claude Code's native AGENTS.md support.** Direct loading begins at v2.1.277 under the Project instructions setting. Default fallback checks for CLAUDE.md, .claude/CLAUDE.md and CLAUDE.local.md on the working-directory/ancestor path. A CLAUDE file can import @AGENTS.md. These are not Codex override semantics; Chapter 6 includes inspection/version caveats. *Source: current memory documentation, checked October 23, 2026. Caveat: earlier releases and settings differ.*

**Mistake-journal mechanics.** Anthropic's Fable 5 guide describes a memory system with three rules that keep a journal honest at a hundred entries: one lesson per file with a one-line summary, update rather than duplicate when a lesson recurs, delete notes that turn out wrong. Add an evidence pointer so the next champion can check whether the failure is still possible. OpenWiki's claims runtime, which attaches evidence pointers to stored claims and re-checks them, cut stale claims from 3.5% to 0.5% across 2,000 evaluated claims. The quarterly review asks of each entry, "has anyone been saved by this rule in the last three months?" If yes, keep it; if no but the rule still applies, keep it, since rare failures still matter; if no and the cause is gone, retire it with a commit-message note. *Sources: Anthropic, "Prompting Claude Fable 5"; Colin Francis, LangChain, Aug 25, 2026. Caveat: OpenWiki is a knowledge-base system, not a journal; the manual borrows the mechanism.*

**Why the precedence line exists.** GPT-6 Astra follows longer instructions better and is more sensitive to context: conflicting guidance in a skill file can make it pause and block early, and OpenAI's guide says the user's instructions take precedence over a skill's. One top line ("In a conflict, the task prompt wins over this file; this file wins over any skill", in the B.2 skeleton) removes a class of stalls. *Source: OpenAI, "Using GPT-6 Astra," Sep 2026 (GPT-6 released September 3-4, 2026; guide revised in place).*

**Compaction and context measurements.** JetBrains compared unmanaged history, masking and summarization across five SWE-agent/SWE-bench Verified configurations. Masking was cheaper than summarization in four; Qwen3-Coder 480B saved 52.7% with masking and 50.4% with summarization against unmanaged history. Other configurations saved less; neither a universal over-50% reduction nor that ratio between methods follows. Anthropic separately reported a 29% gain from tool-result clearing on its internal search evaluation. The multi-turn study found average degradation against a fully specified turn and recovery through consolidation. *Sources: Lindenbauer et al., The Complexity Trap, Table 1; Anthropic, September 29, 2025; Laban et al., May 2025; Appendix C. Caveat: different interventions and settings, not a controlled coding-handoff comparison. Cost baseline rechecked October 23, 2026.*

**Append-only history and cache pricing (Fable 5.1).** Thinking blocks are bound to the exact prefix that produced them, so editing or reordering earlier turns invalidates them and discards the retained reasoning that Chapter 1 counts as half of Effort. The guide's answer is to keep history append-only and let server-side compaction or context editing do the trimming; if you compact on the client, replace the whole history with one summary plus the new turn. With cache reads at 0.025x the base input price, the guide says compacting early to save cost may no longer be the right trade; when you do compact, give the compactor a keep-list (the plan, open questions, deviations in the implementation notes, the exact commands that worked). *Source: Anthropic, "Prompting Claude Fable 5.1." Caveats: undated page, written for API harness builders; 0.025x is the manual's arithmetic from published prices; append-only applies to accounts created on or after August 31, 2026.*

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

**Signal 7, model-context fit: the in-house workflow engine.** A proprietary workflow engine can be unfamiliar to the model even when domain experts understand it. Check representative state transitions and edge cases against documented behavior; investigate missing context or choose a better-fit model. Thin public documentation creates model-fit uncertainty, not automatically a missing qualified evaluator. If the team also cannot judge the behavior, evaluability separately fails. *Author-reported case pattern, not a measured rule about language popularity.*

**Signal 8, velocity-of-change: the React 18/19 bug.** On a codebase mid-migration the agent is confidently right about the old version and wrong about the new, and you cannot always tell which. The author's own bug: Claude used React 18 idioms where React 19 was needed; it worked locally on a transitive React 18 dependency and broke when production pulled 19. Fix: a version rule in AGENTS.md ("we are migrating from React 18 to React 19 this quarter; new code uses 19 idioms; old code may still use 18 but should be updated when touched").

**The model-migration soft signal, with its evidence.** Instructions written for the previous model (AGENTS.md rules, skill prompts, effort levels) do not retire themselves. For between 37% and 63% of the software-engineering papers surveyed, a newer model given a single prompt natively outperformed the heavily engineered tooling proposed about a year earlier. It is not a ninth kill signal; it is what to check when a green codebase turns yellow after a model upgrade (Appendix B.9). *Source: Salsabil et al., Aug 31, 2026 (arXiv 2609.00468). Caveat: preprint, not peer-reviewed; use it for the direction, not the fraction.*

**Worked preparation examples and task restrictions.** (1) Customer-profile service: relevant assertions/failure cases run reliably, current overview, canonical rules and qualified reviewer. Zero known gaps, green candidate; still establish task scope and recovery. (2) Legacy payments: missing failure-case checks (1), stale docs (0.5), costly coupling (1), scattered rules (0.5), with expertise and approval machinery available. Total 3, yellow preparation; establish verification before behavior changes. (3) Custom cryptography without a qualified reviewer fails evaluability regardless of count. (4) Greenfield API with uninvestigated checks/deployment is unknown, not automatically green. (5) Internal tool with relevant checks and bounded documentation/coupling gaps (0.5 each) totals 1, a possible pilot subject to task prerequisites. (6) A vendor-customized fork with unknown upstream effects needs investigation and a decision whether to retain the custom layer. These are illustrative worksheet applications, not validated safety classifications; coverage percentages alone determine none of them.

---

### Chapter 9 - Rolling it out {#deep-dive-chapter-9}

**The two kinds of hooks in full: pre-commit versus pre-push.** Use quick checks at commit and costlier tests or builds at push for fast feedback. A hook manager helps install them but cannot make local hooks unavoidable: Git permits bypasses and alternative hook directories. Policy hooks also need protected configuration and blocking failure behavior. Acceptance belongs in required server checks and protected workflow review, with credentials unable to bypass them. *Sources: Git githooks reference, GitHub rulesets and Claude Code hooks reference, checked October 23, 2026. Caveat: a particular repository must configure and verify these protections; running CI alone is not enforcement.*

**The outer loop: from AutoGPT to Ralph Wiggum.** The inner loop is the six-phase loop (Chapter 4); the outer loop wraps it and re-invokes the agent until a condition holds. In 2023 AutoGPT and BabyAGI looped a model against its own opinion of its progress; nothing external graded an iteration, laps compounded drift, and the approach collapsed as a way of shipping software within months. The revival differs structurally: in mid-2025 Geoff Huntley wired an agent into a bash while-loop (one prompt file, repeat), which spread as "Ralph Wiggum". Each iteration starts with a fresh context, does one unit of work and ends against graders the model does not control (compiler, tests, diff), with state in the repository. His name for the failure mode is overbaking: a loop left running past its job invents work nobody asked for. *Sources: ghuntley.com/ralph (Jul 2025); HumanLayer, Jan 6, 2026; The Register, Jan 27, 2026; AutoGPT and BabyAGI repositories. Caveat: the collapse judgment and structural contrast are the manual's interpretation.*

**The outer loop: the vendor wave and stop-condition mechanisms.** Between September and December 2025 GitHub, Cursor and Google shipped cloud or scheduled agents, and a ralph-wiggum plugin landed in the official Claude Code repository. By spring 2026 Claude Code had `/loop` (re-run on an interval or self-paced), Routines (cloud agents from a schedule or GitHub event), `/goal` (work until a completion condition holds) and `/autofix-pr` (push fixes until CI is green). By Chapter 1's test the capability converged, though what converged is a workflow around the primitives, not a primitive. `/goal` uses a separate model to assess the condition from the conversation; Codex Goals lets the acting model mark a persistent objective complete. These control continuation and budgets. Neither replaces independently protected acceptance checks. The ralph-wiggum plugin has no controlled evidence, and its README names max iterations as its primary safeguard, a budget, not a stop condition. *Sources: GitHub changelog, 2025-09-25; Cursor and Google blogs; Claude Code release notes, Apr-May 2026; Claude Code "/goal" docs; OpenAI Cookbook, "Using Goals in Codex." Caveat: vendor dates drift; the goal docs describe mechanism, not outcomes.*

**The outer loop: why each contract line exists, and the two poles.** A machine-evaluable stop condition, because a loop without one is abandonment. A budget, because an unattended loop is the per-token model's best customer (Appendix A). An acceptance gate enforced by protected required checks and reviewed policy changes, because the cheapest way to go green is to negotiate with your own grader, and a green suite the agent wrote is evidence, not proof (Chapter 5). A durable queue and decision record, with fresh context when the handoff or observed drift justifies it. Fresh context does not mean a fresh world: before a retry or resume, reconcile the current commit, completed writes, running processes, external calls and spend, and make consequential operations safe to repeat. Isolation sized for absence, since an unattended session is where prompt injection meets no human skeptic (Chapter 2). Queue similar, independently verifiable and recoverable units only after each meets the task prerequisites and unattended-run controls; green alone is insufficient. Huntley runs the loop raw at roughly $10 an hour; StrongDM's software factory runs fully non-interactive delivery, humans neither writing nor reviewing code, with end-to-end scenarios held outside the codebase as a holdout the loop cannot weaken, at a spend Simon Willison pegged near $20,000 a month per engineer. *Sources: Willison, Feb 7, 2026; Huntley and The Register as above. Caveat: the $10 figure is Huntley's own and the StrongDM figures are one company's self-description and Willison's framing, not audits.*

**Example time budgets for the role commitments.** In this schedule, the champion reserves about three hours in week one and five in week two; later weeks depend on the pilot features. The intended outputs are a tested workflow, useful maintained instructions, delivered features and a designated successor. The lead reserves roughly two hours in week one and three to five in later phases. These are planning examples from practice; adjust them to measured effort and the team's starting point.

**Why the 90-day example is shaped that way.** The schedule reserves time for learning, a bounded pilot, expansion and operational ownership. It is an organizing example drawn from practice, not a measured exponential curve. Baseline cycle time, defects, review effort and usage before the pilot; inspect outcomes throughout it. Expand or change the approach when those outcomes justify it rather than waiting for a promised month-three payoff.

---

**The outer loop's own kill signals.** The loop gets kill signals the way Chapter 8 gives them to codebases. Four are enough: the same diff applied and then reverted across iterations; budget burning while the queue does not shrink; the same failure surfacing a third time; any iteration that touched the gate. Any one means stop: read the journal, fix the cause, then relaunch. A loop restarted on hope is a loop you have stopped controlling. Appendix B.6's morning-review block carries the same four checks.

### Appendix A - For managers {#deep-dive-appendix-a}

**Tier routing, the two measured points.** Anthropic's advisor pattern pairs a cheaper executor with a stronger model on call. Sonnet with Opus as advisor scored 2.7 points higher on SWE-bench Multilingual than Sonnet alone, at 11.9% lower cost per task. Haiku with an Opus advisor scored 41.2% on BrowseComp against 19.7% solo, trailing Sonnet solo by 29% in score at 85% lower cost per task. These vendor benchmarks suggest a candidate to compare on representative tasks, not a universal routing rule for implementation or research. Routing can also be the vendor's: GitHub Copilot Fusion, generally available on October 28, 2026, chooses the models per request and bills each at its standard rate, so record the models actually used. Availability depends on how you sign in: GPT-5.5 left Codex for ChatGPT sign-ins on October 14, 2026, while API-key sessions were unaffected. Keep a tested fallback. *Sources: Anthropic, "The advisor strategy," Apr 9, 2026; GitHub changelog, Oct 28, 2026; Codex changelog, Oct 14, 2026. Caveat: vendor benchmarks on the vendor's own models; per-task figures, not a general ratio.*

**Cache-first layout, tool tax and masking.** Cache-first layout cut API cost by 41% to 80% on more than 500 agent sessions across three providers (Lumer et al., Jan 31, 2026). The tool-definition figures are under Chapter 1, the masking result under Chapter 6.

**The full-cost comparison.** Compare useful accepted work and human effort on both sides, including investigation, implementation, review, rework and failed attempts. Add incremental tooling/infrastructure, amortized setup, ongoing maintenance and recurring governance/evaluation. The hypothetical calculation in Appendix A values released capacity; it establishes neither cash savings nor faster elapsed delivery. Replace assumptions with records before making an investment claim.
