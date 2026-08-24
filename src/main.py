"""DaRT Automation Service - Main Application Entrypoint."""

import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.v1.health import router as health_router
from src.api.v1.metrics import router as metrics_router
from src.api.v1.remediation import router as remediation_router
from src.config import get_settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("dart-automation")


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """Application startup and shutdown lifecycle management."""
    settings = get_settings()
    logger.info(
        "Starting %s v%s [APM ID: %s | Track: %s | Env: %s]",
        settings.app_name,
        settings.app_version,
        settings.apm_id,
        settings.track,
        settings.environment,
    )
    yield
    logger.info("Shutting down %s cleanly.", settings.app_name)


def create_app() -> FastAPI:
    """Application Factory for Enterprise FastAPI Service."""
    settings = get_settings()

    app = FastAPI(
        title=f"{settings.app_name} [{settings.track}]",
        description="Enterprise Data Remediation & Testing Engine for Banking Records",
        version=settings.app_version,
        lifespan=lifespan,
        docs_url="/docs" if settings.environment != "prod" else None,
        redoc_url="/redoc" if settings.environment != "prod" else None,
    )

    # Security Middleware: Restrict CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"] if settings.environment == "dev" else ["https://internal.bank.corp"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
    )

    # Include Versioned Routers
    app.include_router(health_router, prefix=settings.api_prefix)
    app.include_router(remediation_router, prefix=settings.api_prefix)
    app.include_router(metrics_router, prefix=settings.api_prefix)

    @app.get("/", tags=["Root"])
    def root():
        return {
            "message": "DaRT Automation Service Online",
            "apm_id": settings.apm_id,
            "track": settings.track,
            "docs": f"{settings.api_prefix}/health/ready",
        }

    return app


app = create_app()

