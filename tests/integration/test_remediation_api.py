"""Integration tests for DaRT Remediation API endpoints."""

from fastapi.testclient import TestClient


def test_root_endpoint(client: TestClient):
    """Test Root endpoint returns APM ID and Track info."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["apm_id"] == "AD00001234"
    assert data["track"] == "HDX"


def test_health_probes(client: TestClient):
    """Test Kubernetes Liveness and Readiness probes."""
    live_res = client.get("/api/v1/health/live")
    assert live_res.status_code == 200
    assert live_res.json()["status"] == "ALIVE"

    ready_res = client.get("/api/v1/health/ready")
    assert ready_res.status_code == 200
    assert ready_res.json()["status"] == "READY"
    assert ready_res.json()["apm_id"] == "AD00001234"


def test_metrics_endpoint(client: TestClient):
    """Test metrics endpoint returns telemetry metadata."""
    res = client.get("/api/v1/metrics")
    assert res.status_code == 200
    assert res.json()["apm_id"] == "AD00001234"
    assert res.json()["track"] == "HDX"
    assert res.json()["status"] == "UP"


def test_process_single_record_api(client: TestClient):
    """Test single record remediation endpoint."""
    payload = {
        "id": "REC-555",
        "account_id": "ACC99881122",
        "amount": 12500.00,
        "currency": "usd",
    }
    response = client.post("/api/v1/remediation/process", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["result"]["status"] == "REMEDIATED"
    assert data["result"]["amount"] == 12500.00
    assert data["result"]["currency"] == "USD"
    assert data["audit"]["compliance_verified"] is True


def test_process_batch_records_api(client: TestClient):
    """Test batch processing API."""
    payload = {
        "batch_id": "BATCH-TEST-01",
        "records": [
            {"id": "REC-1", "account_id": "ACC11112222", "amount": 100.0, "currency": "USD"},
            {"id": "REC-2", "account_id": "INVALID", "amount": -10.0, "currency": "USD"},
        ],
    }
    response = client.post("/api/v1/remediation/batch", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert data["remediated_count"] == 1
    assert data["batch_id"] == "BATCH-TEST-01"
