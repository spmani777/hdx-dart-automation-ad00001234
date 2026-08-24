"""Pytest Fixtures for Unit and Integration Test Suites."""

import pytest
from fastapi.testclient import TestClient
from src.main import create_app
from src.config import Settings, get_settings


@pytest.fixture
def mock_settings() -> Settings:
    """Fixture providing testing settings."""
    return Settings(
        app_name="DaRT Automation Test Engine",
        environment="test",
        apm_id="AD00001234",
        track="HDX",
    )


@pytest.fixture
def client(mock_settings: Settings) -> TestClient:
    """FastAPI TestClient fixture with dependency injection override."""
    app = create_app()
    # Override BEFORE wrapping in TestClient
    app.dependency_overrides[get_settings] = lambda: mock_settings
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
