"""Telemetry & Compliance Metrics Endpoint."""

from fastapi import APIRouter

from src.config import get_settings

router = APIRouter(prefix="/metrics", tags=["Telemetry & Compliance"])


@router.get("", tags=["Metrics"])
def get_system_metrics() -> dict[str, str | int]:
    """Expose telemetry metadata for enterprise CMDB and APM tracking."""
    settings = get_settings()
    return {
        "service_name": settings.app_name,
        "version": settings.app_version,
        "apm_id": settings.apm_id,
        "track": settings.track,
        "environment": settings.environment,
        "status": "UP",
    }
