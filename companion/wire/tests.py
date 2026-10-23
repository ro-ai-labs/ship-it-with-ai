"""Assertions derived from the acceptance table, plus the inadequate specimen."""

import importlib
import os
import unittest

import baseline
from wire import QueueUnavailable, api_response


implementation = os.environ.get("WIRE_IMPLEMENTATION", "wire")
if implementation not in ("wire", "defective"):
    raise ValueError("WIRE_IMPLEMENTATION must be wire or defective")
WireService = importlib.import_module(implementation).WireService


class BaselineContract(unittest.TestCase):
    def test_original_response_and_retry(self):
        service = baseline.WireService()
        wire = service.create("baseline-key", 12500)
        self.assertEqual(baseline.api_response(wire),
                         {"wire_id": "wire-1", "amount_cents": 12500})
        self.assertEqual(service.create("baseline-key", 12500), wire)
        self.assertEqual(len(service.audit_events), 1)


class LegacyAssertion(unittest.TestCase):
    def test_audit_event_was_emitted(self):
        """GREEN on the defect: this does not test the new requirement."""
        service = WireService()
        wire = service.create("audit-key", 12500, "URGENT")
        self.assertEqual(len(service.audit_events), 1)
        self.assertEqual(service.audit_events[0]["type"], "wire.created")
        self.assertEqual(service.audit_events[0]["wire_id"], wire.wire_id)


class AuditContract(unittest.TestCase):
    def test_audit_records_the_chosen_priority(self):
        service = WireService()
        wire = service.create("audit-key", 12500, "URGENT")
        event = service.audit_events[0]
        self.assertEqual(event["wire_id"], wire.wire_id)
        self.assertEqual(event["amount_cents"], 12500)
        self.assertEqual(event.get("priority"), "URGENT")


class AcceptanceContract(unittest.TestCase):
    def test_omitted_or_null_priority_defaults_to_normal(self):
        for supplied in ({}, {"priority": None}):
            with self.subTest(supplied=supplied):
                service = WireService()
                wire = service.create("default-key", 12500, **supplied)
                self.assertEqual(wire.priority, "NORMAL")
                self.assertEqual(service.records[wire.wire_id]["priority"], "NORMAL")

    def test_missing_and_null_legacy_priority_read_as_normal(self):
        service = WireService([
            {"wire_id": "legacy-1", "amount_cents": 100},
            {"wire_id": "legacy-2", "amount_cents": 200, "priority": None},
        ])
        original_rows = {key: dict(row) for key, row in service.records.items()}
        self.assertEqual(service.read("legacy-1").priority, "NORMAL")
        self.assertEqual(service.read("legacy-2").priority, "NORMAL")
        self.assertEqual(service.records, original_rows)

    def test_four_priorities_round_trip(self):
        for priority in ("LOW", "NORMAL", "HIGH", "URGENT"):
            with self.subTest(priority=priority):
                service = WireService()
                wire = service.create("key", 100, priority)
                self.assertEqual(service.read(wire.wire_id).priority, priority)
                self.assertEqual(api_response(wire, 2)["priority"], priority)
                self.assertEqual(service.audit_events[0]["priority"], priority)

    def test_invalid_priority_is_rejected_without_side_effects(self):
        for priority in ("urgent", "EXPRESS", "", 1, [], {}):
            with self.subTest(priority=priority):
                service = WireService()
                with self.assertRaises(ValueError):
                    service.create("key", 100, priority)
                self.assertEqual(service.records, {})
                self.assertEqual(service.audit_events, [])
                self.assertEqual(service.review_queue, [])
                self.assertEqual(service.completed_requests, {})

    def test_amount_and_key_validation_remain_in_force(self):
        for amount in (0, -1, 1.5, True):
            with self.subTest(amount=amount):
                with self.assertRaises(ValueError):
                    WireService().create("key", amount)
        for key in (None, "", " ", 123):
            with self.subTest(key=key):
                with self.assertRaises(ValueError):
                    WireService().create(key, 100)

    def test_only_urgent_wires_enter_the_review_queue(self):
        service = WireService()
        for priority in ("LOW", "NORMAL", "HIGH"):
            service.create(priority, 100, priority)
        urgent = service.create("URGENT", 100, "URGENT")
        self.assertEqual(service.review_queue, [urgent.wire_id])

    def test_queue_outage_rejects_urgent_without_partial_acceptance(self):
        service = WireService()
        service.queue_available = False
        with self.assertRaises(QueueUnavailable):
            service.create("retry-key", 100, "URGENT")
        self.assertEqual(service.records, {})
        self.assertEqual(service.audit_events, [])
        self.assertEqual(service.review_queue, [])
        self.assertEqual(service.completed_requests, {})
        service.queue_available = True
        accepted = service.create("retry-key", 100, "URGENT")
        self.assertEqual(service.create("retry-key", 100, "URGENT"), accepted)
        self.assertEqual(len(service.records), 1)
        self.assertEqual(len(service.audit_events), 1)
        self.assertEqual(service.review_queue, [accepted.wire_id])

    def test_queue_outage_does_not_block_normal_creation(self):
        service = WireService()
        service.queue_available = False
        self.assertEqual(service.create("key", 100).priority, "NORMAL")

    def test_retry_replays_once_even_if_queue_later_fails(self):
        service = WireService()
        accepted = service.create("key", 100, "URGENT")
        service.queue_available = False
        self.assertEqual(service.create("key", 100, "URGENT"), accepted)
        self.assertEqual(len(service.records), 1)
        self.assertEqual(len(service.audit_events), 1)
        self.assertEqual(service.review_queue, [accepted.wire_id])

    def test_omitted_and_explicit_normal_share_an_idempotent_request(self):
        service = WireService()
        first = service.create("key", 100)
        self.assertEqual(service.create("key", 100, "NORMAL"), first)
        self.assertEqual(len(service.audit_events), 1)

    def test_reusing_key_with_changed_input_is_a_conflict(self):
        service = WireService()
        service.create("key", 100)
        for amount, priority in ((101, "NORMAL"), (100, "URGENT")):
            with self.subTest(amount=amount, priority=priority):
                with self.assertRaises(ValueError):
                    service.create("key", amount, priority)
        self.assertEqual(len(service.records), 1)
        self.assertEqual(len(service.audit_events), 1)
        self.assertEqual(service.review_queue, [])

    def test_old_api_response_is_unchanged(self):
        wire = WireService().create("key", 100, "URGENT")
        self.assertEqual(api_response(wire, 1),
                         {"wire_id": "wire-1", "amount_cents": 100})

    def test_new_api_response_includes_priority(self):
        wire = WireService().create("key", 100, "URGENT")
        self.assertEqual(api_response(wire, 2), {
            "wire_id": "wire-1", "amount_cents": 100, "priority": "URGENT"
        })

    def test_unsupported_api_version_is_rejected(self):
        wire = WireService().create("key", 100)
        for version in (0, 3, "2", True):
            with self.subTest(version=version):
                with self.assertRaises(ValueError):
                    api_response(wire, version)


if __name__ == "__main__":
    unittest.main()
