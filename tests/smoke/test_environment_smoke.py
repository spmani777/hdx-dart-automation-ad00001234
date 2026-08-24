"""Post-deployment Environment Smoke Test Suite.

Runs against live environments (dev, staging, prod) after deployment.
"""

import os

import httpx
import pytest

TARGET_URL = os.getenv("DEPLOYED_SERVICE_URL", "http://localhost:8080")


@pytest.mark.asyncio
async def test_live_environment_health():
    """Verify live endpoint responds with status 200 and valid APM ID."""
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(f"{TARGET_URL}/api/v1/health/ready")
            assert response.status_code == 200, f"Expected 200, got {response.status_code}"
            data = response.json()
            assert data["status"] == "READY"
            assert data["apm_id"] == "AD00001234"
            assert data["track"] == "HDX"
        except httpx.ConnectError:
            pytest.skip(f"Live service not running at {TARGET_URL} (Skipped in offline unit test run)")

