from datetime import date, timedelta

from legal_report.models import MatterIntake, follow_up_due


def test_pending_signed_document_near_deadline_needs_follow_up():
    matter = MatterIntake("M-1", "Acme", False, date(2026, 9, 10), "user@example.com")
    assert follow_up_due(matter, date(2026, 9, 5)) is True
    assert follow_up_due(matter, date(2026, 9, 1)) is False
    assert follow_up_due(MatterIntake("M-2", "Acme", True, date(2026, 9, 6), "user@example.com"), date(2026, 9, 5)) is False
