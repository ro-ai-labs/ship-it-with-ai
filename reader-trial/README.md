# Ship It With AI reader trial

Use three short tasks to observe whether engineers can apply the stable edition
without the author explaining it. Run individual sessions with two or three
engineers. Allow about 40 minutes per person as a planning estimate; record the
time actually used.

**Status:** prepared; reader sessions have not started.

**Edition:** `1c4a9e3c965c62caf944dfb4afb00b7c9f87049e`.
Record any different edition used during a session. The maintained book and the
Wire companion are unchanged by this trial pack.

## Assign readers and an observer

Choose engineers who resemble the intended audience, with experience reviewing
changes or leading delivery. Include different levels of familiarity with agents
where practical. This is a small qualitative trial, not a representative sample.

| Reader label | Role and relevant experience | Language | Prior book or Wire exposure | Observer | Session date |
|---|---|---|---|---|---|
| | | | | | |

Each reader should bring one actual proposed change they understand for the
readiness task. No implementation or production access is required. If they
cannot bring a real change, mark that task as not assessed rather than inventing
an engagement.

## Send the participant sheet

Send only [participant.md](participant.md) or
[participant.RO.md](participant.RO.md). Keep [facilitator.md](facilitator.md)
and its answer criteria with the observer.

For the first task, use the supplied excerpt. The book's Chapter 5, B.11,
companion README and full `tests.py` reveal the explanation. Release those
resources after recording the first Wire response. Record previous exposure;
a remembered answer cannot establish first-time discovery.

Readers may use the specified book pages for the readiness and economics tasks.
Ask them to work without an AI assistant during the initial responses so the
observation concerns their use of the book. Discuss the answers afterward.

Invitation draft for the organizer to send:

> Could you try three short exercises from Ship It With AI in an individual
> session of about 40 minutes? We want to see where the book needs explanation.
> Please bring a real proposed change you understand. You will inspect a test,
> use the readiness worksheet, and interpret a cost example. Think aloud as you
> work; we will record where you look, your first interpretation and any help
> you need. Please tell us whether you have already read the book or Wire example.

## Run and record

1. Read the observer instructions before the session. Fill the reader record
   above and note the edition and prior exposure.
2. Give the participant sheet. Observe the three tasks in order. Save the first
   response before hints, corrections or the verifier.
3. Use [observations.csv](observations.csv) for one row per reader and task.
   Distinguish independent completion, assisted completion, incomplete work
   and tasks that could not be assessed.
4. Debrief after the tasks. The observer may then explain the Wire experiment
   or run `python3 companion/wire/verify.py` from the repository root.
5. Fill [findings.md](findings.md) from the observations. Link every proposed
   edit to an actual misunderstanding or difficulty and the passage involved.

Do not convert two or three readers into success percentages or a claim that
the method improves delivery. A single consequential misunderstanding can
justify an edit; a recurring hesitation can identify a confusing explanation.
Correctly supported restrictions are successful readiness decisions.
