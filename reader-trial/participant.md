# Ship It With AI reader exercises

Work through these three tasks in order and think aloud. We are observing how
you use the material. Tell the observer where you hesitate or need an
explanation. Before starting, say whether you have read the book or Wire example.

Use the material specified for each task. Please give your initial responses
without help from an AI assistant. The observer will discuss the answers with
you afterward.

## Task 1 Inspect the Wire test

Use only this excerpt until the observer records your first response.

This synthetic service creates a wire with an amount in cents and a selected
priority. The requirement is that each creation audit event records that chosen
priority. The test creates an urgent wire and checks the resulting audit event:

```python
service = WireService()
wire = service.create("audit-key", 12500, "URGENT")
self.assertEqual(len(service.audit_events), 1)
self.assertEqual(service.audit_events[0]["type"], "wire.created")
self.assertEqual(service.audit_events[0]["wire_id"], wire.wire_id)
```

Does this test provide enough evidence that the requirement holds? Explain
your reasoning and any change you would make. Exact Python syntax is optional.

Your first response:

>

## Task 2 Decide what work can proceed

Choose one real proposed change you understand. Open the
[B.4 readiness worksheet](https://ship-it-with.ai/appendix-b-templates/#template-b4)
or its [Romanian version](https://ship-it-with.ai/ro/appendix-b-templates/#template-b4).

Use the worksheet to decide what work can proceed next, what must wait, and
which evidence could change that decision. Explain what you know and what you
do not know. Point to the evidence and the parts of the worksheet you used.

Proposed change:

>

Decision and supporting evidence:

>

Unresolved questions and next step:

>

## Task 3 Interpret the economics

Open [Appendix A's worked example](https://ship-it-with.ai/appendix-a-for-managers/#a-worked-example)
or its [Romanian version](https://ship-it-with.ai/ro/appendix-a-for-managers/#a-worked-example).

Draft a brief update to an engineering manager about delivery time, human
effort and financial value. State what the example's figures support, what
they do not establish, and the next evidence you would request. Show the
figures or passages behind your interpretation.

Manager update:

>

## Debrief

After all three responses are recorded, discuss where the material helped or
needed explanation. Which term or passage would you change? If you already
knew an answer, say where you learned it.
