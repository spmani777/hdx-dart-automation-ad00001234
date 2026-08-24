"""Unit tests for AuditTrail compliance service."""

from src.services.audit_trail import AuditTrail


def test_create_audit_event():
    """Verify audit log event contains enterprise APM ID, Track, and ISO timestamp."""
    event = AuditTrail.create_event(
        event_type="TEST_EVENT",
        details={"key": "value"},
        user_id="CI_RUNNER",
    )
    assert event["apm_id"] == "AD00001234"
    assert event["track"] == "HDX"
    assert event["event_type"] == "TEST_EVENT"
    assert event["actor"] == "CI_RUNNER"
    assert "timestamp" in event
    assert event["compliance_verified"] is True
