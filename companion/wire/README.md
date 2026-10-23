# Wire: inspect the decision, then the test

**Synthetic worked companion, version 1.** Every request, code sample, review
conversation and deployment arrangement below was constructed for teaching.
This is not client code, a reconstruction of a recorded engagement, or evidence
for the banking case's delivery time or production results.

The book uses a Java/Spring banking illustration. This companion uses Python 3.8+
and its standard library so a reader can run the assertion experiment without
installing a framework, database, queue or dependencies. The decisions transfer;
the implementation is a small model, not a deployable banking service.

## Run it

From this directory:

```sh
python3 verify.py
```

The command runs three separate checks:

1. The inadequate audit assertion passes against the defective implementation.
2. The corrected assertion fails against that implementation with
   `AssertionError: None != 'URGENT'`. This is the expected educational result.
3. All **17 tests** pass against the repaired implementation.

The verifier exits successfully only when it observes that exact sequence. An
import error or an unrelated failure does not count as the expected red test.
It uses temporary process environments and does not edit the examples.

To inspect each result separately on a POSIX shell:

```sh
WIRE_IMPLEMENTATION=defective python3 -m unittest -v tests.LegacyAssertion
WIRE_IMPLEMENTATION=defective python3 -m unittest -v tests.AuditContract
python3 -m unittest -v tests
```

The middle command deliberately exits with status 1. On other shells, use
`python3 verify.py`, which sets the environment portably.

| File | What to inspect |
|---|---|
| [baseline.py](baseline.py) | Starting state: amount, unchanged response, idempotent creation, audit event |
| [tests.py](tests.py) | The inadequate assertion, corrected assertion, and acceptance checks |
| [defective.py](defective.py) | The small defective overlay: priority is dropped from the audit event |
| [wire.py](wire.py) | Repaired behavior, including defaults, queue failure and retries |
| [verify.py](verify.py) | The experiment, including verification of the expected failure |

For a judgment exercise, read the request and acceptance table below, then open
only `tests.LegacyAssertion`. Identify what it fails to establish before opening
`tests.AuditContract` or `defective.py`.

## Starting point and incomplete request

The baseline accepts an integer amount in cents and an idempotency key. It stores
a wire, emits `wire.created`, and returns the wire ID and amount. Retrying the
same key and amount returns the original wire without another event. Reusing
the key with a different amount is rejected. `BaselineContract` preserves an
example of that behavior.

The incomplete request is:

> Add priority to wires. Urgent wires need compliance review. Keep old clients
> working and make sure the audit log captures the change.

Before coding, someone responsible for the product must settle what "priority,"
"working," "review" and "captures" mean. In this synthetic exercise, the product
owner and compliance owner choose the following answers. They are decisions for
this example, not claims about a regulation or universal banking rules.

| Question | Accepted decision | Evidence in `tests.py` |
|---|---|---|
| What values are valid? | After defaulting, exactly `LOW`, `NORMAL`, `HIGH`, `URGENT`; case-sensitive | `test_four_priorities_round_trip`, `test_invalid_priority_is_rejected_without_side_effects` |
| What if priority is omitted or null? | New requests use `NORMAL` for both; null means unspecified in this example | `test_omitted_or_null_priority_defaults_to_normal` |
| What about old records? | A missing or NULL field reads as `NORMAL`; reading does not rewrite history | `test_missing_and_null_legacy_priority_read_as_normal` |
| What does an old client receive? | API v1 keeps exactly `wire_id` and `amount_cents`; v2 adds `priority` | `test_old_api_response_is_unchanged`, `test_new_api_response_includes_priority` |
| Which wires require review? | Only `URGENT`; this model queues a wire ID and does not execute a transfer | `test_only_urgent_wires_enter_the_review_queue` |
| What if that queue is unavailable? | Reject a new urgent request before accepting anything; normal creation continues | Both queue-outage tests |
| What is audited? | One `wire.created` event with wire ID, amount and chosen priority | `test_audit_records_the_chosen_priority`, `test_four_priorities_round_trip` |
| What happens on retry? | Same key and normalized input return the original result once; changed input conflicts | Retry and idempotency tests |
| Can a rejected urgent request be retried? | Yes, using the same key after recovery; no partial state was accepted | `test_queue_outage_rejects_urgent_without_partial_acceptance` |

The model raises `QueueUnavailable` rather than claiming acceptance. A real HTTP
adapter could map that to a documented retryable response such as 503. Invalid
inputs and idempotency conflicts need distinct API errors in a real adapter;
this exercise uses `ValueError` for both to keep the model small.

## Research note: facts, assumptions, decisions

**Observed facts about the supplied snapshot:** `baseline.py` has no priority
field or queue. Its response has two keys. Idempotency is an in-memory dictionary,
and its event contains a type and wire ID. There is no database migration runner,
HTTP server, authentication layer or external queue in this repository.

**Assumptions requiring confirmation in an actual system:** API versions are
selected outside the domain model; the deployment supports additive changes;
existing audit consumers tolerate documented added fields; the compliance owner
can verify an urgent wire's entry into review. None of these assumptions is
established by a green Python suite.

**Decisions:** the table above is the acceptance contract. Omission and explicit
null both mean unspecified priority, so they default to NORMAL; this is an API
decision rather than a rule inferred from the programming language. The implementation
must preserve baseline amount validation and retry semantics. Priority is
immutable after creation in this example; editing an existing wire is out of
scope. Historical events are not rewritten. The new event schema is additive.

**Unavailable evidence:** production schemas, real consumer contracts, latency,
queue durability, concurrent-request behavior, service credentials, deployment
logs and regulatory interpretation. The exercise cannot establish those claims.

## Dependency-aware plan

Do not equate six task names with six independent workers.

| Wave | Work and ownership | Dependency and check |
|---|---|---|
| 0 | Product/compliance owners settle the table; implementer records contracts | Complete before dependent implementation; review unresolved questions |
| 1 | One implementer adds priority parsing, record reads and creation signature | All consumers share these names and default semantics; default/legacy/invalid-input tests |
| 2 | API projection, routing behavior and audit behavior may be designed independently | Each uses the settled Wave 1 contract; API, queue and event assertions |
| 3 | One writer integrates creation, queue acceptance, audit and idempotency | These share state and failure behavior; outage/retry/conflict tests |
| 4 | Reviewer compares assertions to acceptance; implementer repairs supported findings | Corrected assertion must expose the audit defect before the repair passes |
| 5 | Owner evaluates evidence and completes the production handoff | Passing model tests are insufficient to authorize a real deployment |

In this tiny implementation, the three Wave 2 concerns all touch `wire.py`.
Use one writer, even if someone else reviews a contract independently. In a
larger service they could have separate files and owners; they still depend on
the same agreed contract. No parallel execution time or speedup is claimed here.

## The green test that misses the change

`LegacyAssertion` checks that an event exists and names the created wire:

```python
self.assertEqual(len(service.audit_events), 1)
self.assertEqual(service.audit_events[0]["type"], "wire.created")
self.assertEqual(service.audit_events[0]["wire_id"], wire.wire_id)
```

Those assertions are useful for the old behavior. They do not ask whether the
event contains priority. The deliberately defective implementation drops that
field and still satisfies every assertion above.

Before reading further: what observation would distinguish an event that meets
the new requirement from one that merely exists?

The corrected assertion compares the recorded value with the chosen input:

```python
self.assertEqual(event.get("priority"), "URGENT")
```

It fails against `defective.py`, where the observed value is `None`. The repaired
`wire.py` includes `"priority": wire.priority` in `_audit_event`. The same assertion
then passes. The four-value test also checks that a hard-coded `URGENT` value
cannot satisfy the complete contract. The evidence links request → assertion →
observed failure → repair; a pass alone would show less.

## Review finding and response

**Finding — important, intent:** The new acceptance table requires priority in
each creation event, but the implementation emits no priority. The current audit
test only checks event presence and wire ID. An urgent wire can reach the review
queue while leaving an incomplete audit event. Add an assertion for the chosen
value, demonstrate it failing on this implementation, and fix event construction.

**Implementer's response:** Accepted. The corrected test fails because priority
is absent. The repair includes the normalized value in the event. All four
priority values now round-trip through storage, the v2 response and the event.
The full model suite passes; no production consumer contract has been verified.

**Recovery review — project-specific:** This model has no migration engine. In
the hypothetical deployment below, the project requires an additive expansion,
compatibility checks and a rehearsed roll-forward/restore procedure. A missing
`down` migration is not universally a defect: an undo script cannot necessarily
reverse externally consumed events or completed business actions.

## Completion evidence and example PR

Running `python3 verify.py` produces one weak-green test, one expected assertion
failure on the defective snapshot, and 17 passing tests on the repaired snapshot.
These counts describe this supplied experiment, not the book's original banking
engagement. The command must be rerun after relevant changes.

> **Add explicit priority to the synthetic Wire model**
>
> New wires accept four priorities; omitted or null input defaults to NORMAL. Missing/NULL legacy
> data reads as NORMAL; v1 responses remain unchanged, while v2 responses expose
> priority. Urgent wires require review-queue acceptance. Retries preserve the
> original outcome without duplicate audit or review entries.
>
> Verified: `python3 verify.py` demonstrates the inadequate assertion, observes
> the corrected assertion failing on the defect, and passes all 17 repaired
> checks. The audit omission was fixed after review against the acceptance table.
>
> Remaining risks: this in-memory model does not establish durable transactions,
> concurrent idempotency, authorization, real queue delivery or API compatibility
> with actual clients. Production integration and deployment are not performed.

## Production handoff: a filled hypothetical example

This is a proposed handoff for a real implementation, not a report that a release
occurred. Named roles must be replaced with accountable people before use.

| Question | Agreed arrangement for the example |
|---|---|
| Who releases it? | Payments release owner uses the existing reviewed deployment pipeline; compliance owner approves urgent-review behavior |
| Deployment order? | Expand storage and prepare tolerant audit/review consumers; deploy fallback-capable readers and the v2 adapter with urgent creation disabled; verify mixed-version behavior; backfill/validate legacy values; enable the feature only after queue checks pass |
| What happens to old data and clients? | Missing/NULL means NORMAL during expansion; retain API v1; do not rewrite historical events; enforce stricter storage constraints only after backfill and old-writer compatibility checks |
| What confirms success? | A staging synthetic urgent wire has the same priority in storage, v2 response, audit event and review entry; retry produces no duplicates; a v1 contract check remains unchanged |
| What production signal matters? | Compare accepted urgent IDs with durable review/audit records; monitor rejection rate and review age using the service's agreed operational targets |
| What triggers intervention? | Any accepted urgent wire missing its required audit or review record, or a breached agreed review-age target; page the payments on-call and stop new urgent acceptance |
| How is recovery handled? | Disable new urgent requests; preserve records and events; reconcile affected IDs; roll forward the defect where possible. Use a tested restore procedure only under the incident owner's decision, accounting for externally observed events |
| Who observes afterward? | Payments on-call owns the first 24-hour observation window and hands off to the service owner; compliance owner confirms review reconciliation before closing the release |

In a production service, independent database and queue writes cannot acquire
durable atomicity from the ordering used in this single-threaded model. Choose
and test a real transaction/outbox or equivalent delivery design; include crash
recovery, consumer idempotency and concurrent retries. If the accepted design
queues durably while delivery is unavailable, its acceptance decision differs
from this example's reject-before-acceptance policy and needs different tests.

## A proportionate maintenance interaction

Consider a separate request: "Correct a typo in the admin help text; no behavior
change." A reasonable short interaction is:

> Agent: I found the exact text and its rendered help page. I will correct the
> spelling, keep the link and surrounding meaning, then inspect the page.
>
> Owner: The requested wording is correct.
>
> Agent: The one-line diff is ready. The page renders the corrected text and its
> existing link still opens the intended destination. Normal PR review applies.

Research was locating the text; planning was one sentence; execution was the
edit; review checked meaning and scope; verification checked the rendered page
and link; shipping uses the ordinary PR. No extra permanent test, agent team or
separate planning document is justified merely by the six function names.

## Completed context handoff

> **Objective:** Add priority while preserving old clients and idempotent creation.
> **Accepted decisions:** Four uppercase values; omitted/null priority defaults to NORMAL; urgent requests
> rejected during queue outage; audit includes priority; same-key retries replay.
> **Current commit:** No companion commit is claimed; this is the supplied
> `wire-v1` file snapshot. In a repository handoff, replace this with the actual
> reviewed commit and describe any uncommitted changes.
> **Changed files:** `wire.py`, `defective.py`, `tests.py`, `verify.py`, plus this
> explanation; `baseline.py` is the starting snapshot.
> **Unresolved question:** Which durable transaction/outbox design will a real
> deployment use? No production implementation is authorized by this exercise.
> **Failed approach:** Checking only event existence left priority untested.
> **Checks already run:** Verifier observed weak-green, corrected-red, repaired-green
> (17 tests). Re-run it if relevant files change.
> **Next action:** Review the acceptance decisions and adapter/deployment evidence
> before considering integration into any actual service.

## Exercises and feedback

### 1. Find the dependency error

A proposed plan starts the API adapter, routing and audit implementation in
parallel. Each worker chooses its own representation for priority. The record
and default are agreed afterward. What should change?

**Answer:** Settle the shared representation, default and failure policy first.
Then run work against that contract, with one writer per overlapping area and
an integration check. Independent contract exploration can run earlier if its
output is explicitly a proposal, not an independently committed assumption.
Waves are one acceptable schedule; one implementer is another.

### 2. Find the inadequate assertion

Without opening `AuditContract`, explain why `LegacyAssertion` passes on the
defective implementation. Write an observation that would reject the defect.

**Answer:** Emitting an event does not establish its priority value. Assert that
the event's priority equals the selected input, show that assertion fail against
the defect, and rerun after repair. Checking only that the key exists is weaker:
it permits an incorrect or hard-coded value. Checking all four values adds a
useful distinction. Exact whole-event equality is also defensible if that is the
agreed schema contract, but it may unnecessarily constrain allowed future fields.

### 3. Choose three workflow sizes

Choose a workflow for (a) a help-text typo, (b) a priority field crossing API,
storage, audit and routing, and (c) changing an unfamiliar ledger algorithm with
no qualified reviewer or trustworthy oracle.

**Answer:** (a) Locate, make the small edit, inspect the affected output and use
normal review. (b) Settle business decisions, order dependencies, inspect tests
against intent, verify failure/retry behavior and fill the production handoff.
(c) Restrict behavior changes while establishing evaluability; investigate with
a domain expert, build relevant evidence and resolve authority/boundaries first.
A low repository score cannot supply the missing expertise. Different artifacts
or agent counts are acceptable if they cover these decisions and controls.
