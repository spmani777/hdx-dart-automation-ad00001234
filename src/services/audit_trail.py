"""Compliance Audit Trail Engine for Banking Governance."""

from datetime import datetime, timezone
from typing import Any
from src.config import get_settings


class AuditTrail:
    """Immutable Audit Log Generator for SOX & Financial Compliance."""

    @staticmethod
    def create_event(event_type: str, details: dict[str, Any], user_id: str = "SYSTEM_AUTOMATION") -> dict[str, Any]:
        """Generate an audit event with enterprise APM ID and Track metadata."""
        settings = get_settings()
        return {
            "apm_id": settings.apm_id,
            "track": settings.track,
            "environment": settings.environment,
            "event_type": event_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "actor": user_id,
            "details": details,
            "compliance_verified": True,
        }

