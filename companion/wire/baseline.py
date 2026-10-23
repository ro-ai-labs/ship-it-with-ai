"""Synthetic starting snapshot: idempotent wire creation without priority."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Wire:
    wire_id: str
    amount_cents: int


class WireService:
    def __init__(self):
        self.records = {}
        self.audit_events = []
        self.completed_requests = {}

    def create(self, key, amount_cents):
        if not isinstance(key, str) or not key.strip():
            raise ValueError("a nonempty idempotency key is required")
        if type(amount_cents) is not int or amount_cents <= 0:
            raise ValueError("amount_cents must be a positive integer")
        if key in self.completed_requests:
            amount, wire = self.completed_requests[key]
            if amount != amount_cents:
                raise ValueError("idempotency key reused with different input")
            return wire
        wire = Wire(f"wire-{len(self.records) + 1}", amount_cents)
        self.records[wire.wire_id] = {
            "wire_id": wire.wire_id, "amount_cents": wire.amount_cents
        }
        self.audit_events.append({"type": "wire.created", "wire_id": wire.wire_id})
        self.completed_requests[key] = (amount_cents, wire)
        return wire


def api_response(wire):
    return {"wire_id": wire.wire_id, "amount_cents": wire.amount_cents}
