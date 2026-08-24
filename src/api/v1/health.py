"""Enterprise Health Probes (Liveness & Readiness for Kubernetes / Cloud)."""

from fastapi import APIRouter, status
from src.config import get_settings

router = APIRouter(prefix="/health", tags=["Health & Diagnostics"])


@router.get("/live", status_code=status.HTTP_200_OK)
def liveness_probe() -> dict[str, str]:
    """Kubernetes liveness probe: indicates whether the container process is alive."""
    return {"status": "ALIVE"}


@router.get("/ready", status_code=status.HTTP_200_OK)
def readiness_probe() -> dict[str, str]:
    """Kubernetes readiness probe: indicates whether the app is ready to accept traffic."""
    settings = get_settings()
    return {
        "status": "READY",
        "app_name": settings.app_name,
        "environment": settings.environment,
        "apm_id": settings.apm_id,
        "track": settings.track,
    }
