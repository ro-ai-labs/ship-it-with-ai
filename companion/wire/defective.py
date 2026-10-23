"""The plausible defect: the new field never reaches the audit event.

This small overlay isolates the teaching difference from wire.py. It is an
intentionally defective synthetic snapshot, not an alternative to deploy.
"""

from wire import WireService as RepairedWireService


class WireService(RepairedWireService):
    def _audit_event(self, wire):
        event = super()._audit_event(wire)
        del event["priority"]
        return event
