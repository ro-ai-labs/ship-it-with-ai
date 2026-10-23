"""Repaired teaching model. In-memory, single-process, and single-threaded."""

from dataclasses import dataclass


PRIORITIES = frozenset({"LOW", "NORMAL", "HIGH", "URGENT"})


class QueueUnavailable(RuntimeError):
    pass


def parse_priority(value):
    # Missing/NULL legacy values have the same meaning as an omitted new field.
    if value is None:
        return "NORMAL"
    if not isinstance(value, str) or value not in PRIORITIES:
        raise ValueError("priority must be LOW, NORMAL, HIGH, or URGENT")
    return value


@dataclass(frozen=True)
class Wire:
    wire_id: str
    amount_cents: int
    priority: str


class WireService:
    def __init__(self, existing_rows=()):
        self.records = {row["wire_id"]: dict(row) for row in existing_rows}
        self.audit_events = []
        self.review_queue = []
        self.completed_requests = {}
        self.queue_available = True

    def read(self, wire_id):
        row = self.records[wire_id]
        return Wire(row["wire_id"], row["amount_cents"],
                    parse_priority(row.get("priority")))

    def create(self, key, amount_cents, priority=None):
        if not isinstance(key, str) or not key.strip():
            raise ValueError("a nonempty idempotency key is required")
        if type(amount_cents) is not int or amount_cents <= 0:
            raise ValueError("amount_cents must be a positive integer")
        priority = parse_priority(priority)
        signature = (amount_cents, priority)
        if key in self.completed_requests:
            previous_signature, wire_id = self.completed_requests[key]
            if signature != previous_signature:
                raise ValueError("idempotency key reused with different input")
            return self.read(wire_id)

        # Reject before mutating anything; a retry with this key may then succeed.
        if priority == "URGENT" and not self.queue_available:
            raise QueueUnavailable("urgent review queue unavailable; nothing accepted")

        number = len(self.records) + 1
        while f"wire-{number}" in self.records:
            number += 1
        wire = Wire(f"wire-{number}", amount_cents, priority)
        event = self._audit_event(wire)
        self.records[wire.wire_id] = {
            "wire_id": wire.wire_id, "amount_cents": amount_cents,
            "priority": priority,
        }
        if priority == "URGENT":
            self.review_queue.append(wire.wire_id)
        self.audit_events.append(event)
        self.completed_requests[key] = (signature, wire.wire_id)
        return wire

    def _audit_event(self, wire):
        return {
            "type": "wire.created", "wire_id": wire.wire_id,
            "amount_cents": wire.amount_cents, "priority": wire.priority,
        }


def api_response(wire, version=1):
    if type(version) is not int or version not in (1, 2):
        raise ValueError("supported API versions: 1 and 2")
    response = {"wire_id": wire.wire_id, "amount_cents": wire.amount_cents}
    if version == 2:
        response["priority"] = wire.priority
    return response
