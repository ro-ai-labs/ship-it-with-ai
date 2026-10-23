# Reader trial observer instructions

Keep this sheet with the observer. Send the participant sheet separately so
the Wire answer remains unseen until the first response is recorded.

## Before the session

Record the reader label, role, language, edition, previous exposure and date.
Confirm that the reader has a real proposed change for Task 2. An unavailable
task means that exercise cannot be assessed in this session.

Use the same prompts across readers. Say: “Please think aloud. We want to see
where the material needs explanation. I will discuss the answers after you have
given your initial responses.”

## Observe before explaining

Record the first interpretation as closely as possible, the source consulted,
hesitations and elapsed task time. Save that response before supplying hints,
corrections or additional resources. Normal source lookup is permitted for
Tasks 2 and 3; Task 1 initially uses the excerpt alone.

Neutral followups include “What led you to that?” and “Where did you look?”
Log the prompt and response. Content hints such as “Look at priority” change
the interpretation of the result: retain the original response and mark any
later completion as assisted. Never replace it with the corrected answer.

Prior familiarity is useful context. If the reader remembers the Wire answer,
record that; this session cannot establish how they first discovered the gap.

## Task 1 Evidence to look for

The test establishes event count, type and wire identity. A missing or incorrect
priority can still pass. An adequate response identifies that gap and proposes
comparing the recorded priority with the selected input. Accept plain language
or any assertion that checks the accepted contract; exact Python syntax is not
the objective.

Checking all priorities to rule out a hard-coded fix is useful extra reasoning,
not a requirement for understanding the basic gap. Merely asking for “more
tests” without identifying the missing observation is incomplete evidence.

After initial responses are recorded, the reader may inspect the companion
and run its verifier. The expected sequence is one inadequate green test,
one corrected assertion failing with `None != 'URGENT'`, then 17 repaired tests
passing. Record any run separately; a prior verified run is not a session result.

## Task 2 Evidence to look for

The reader bounds a real change by behavior, module and environment. They use
B.4's four prerequisites: qualified evaluation, meaningful verification and
permitted actions/recovery alongside the defined task. Known facts have
evidence; missing facts remain explicit.

If a prerequisite is missing or unknown, a supported decision to investigate
or prepare under supervision is successful application. The reader should
identify what would resolve the gap and who can judge it. Repository signals
guide preparation; they do not override prerequisites. Unknown signals remain
`?`, and no color is assigned until they are investigated. Green alone grants
no task authority.

Judge consistency with the stated facts, not whether the observer would pick
the same workflow. Record a justified alternative. The exercise does not
authorize implementation or deployment of the proposed change.

## Task 3 Evidence to look for

The hypothetical example has 200 baseline and 160 assisted task hours: 40 task
hours released, valued at $4,000 at the stated $100/hour assumption. That is
before additional operating and setup costs. The complete comparison is
$20,000 versus $19,300, or $700 modeled net capacity value; modeled cost per
accepted change is $1,000 versus $965.

Human task hours do not supply elapsed delivery time. Valuing released capacity
does not establish cash savings. The example assumes comparable accepted work;
it does not demonstrate equal quality or a causal agent effect. The reader
should request actual pilot records for any claim beyond the illustration.

The essential result is separating delivery time, human effort and modeled
financial value. Do not require every arithmetic detail or these exact words
when the explanation preserves the distinctions.

## Record and debrief

Use one row per reader and task in [observations.csv](observations.csv).
Choose an outcome:

- `independent`: the initial response supports the task's intended decision.
- `assisted`: completion follows a recorded content hint or explanation.
- `incomplete`: the task was attempted but the response remains insufficient.
- `not_assessed`: no suitable real task, skipped exercise or unavailable response.

Record prior exposure separately; `independent` means no assistance during the
task, not that the reader has never seen the answer. Keep disagreements and
uncertainty in the notes rather than forcing a favorable category.

After all tasks, ask which passage helped, which required explanation and what
the reader would change. Fill [findings.md](findings.md) using reader labels and
task evidence. Distinguish a book problem, unfamiliarity with the domain, a
trial-material problem and an unresolved interpretation. Record counts as
counts, not percentages. Plan edits from observed difficulties and check those
edits with readers before claiming the difficulty is resolved.
