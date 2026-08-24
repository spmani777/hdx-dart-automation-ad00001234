# ==============================================================================
# Enterprise Banking Hardened Multi-Stage Dockerfile
# Application: DaRT Automation
# APM ID: AD00001234 | Track: HDX
# ==============================================================================

# Stage 1: Build & Dependency Wheel Stage
FROM python:3.11-slim-bullseye AS builder

WORKDIR /build

# Security: Install updates and build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# ==============================================================================
# Stage 2: Hardened Non-Root Production Runtime
# ==============================================================================
FROM python:3.11-slim-bullseye AS runtime

# Enterprise Compliance Labels (CMDB & Security Scanners: Harbor, Trivy, Prisma)
LABEL maintainer="HDX Engineering Team" \
      enterprise.apm_id="AD00001234" \
      enterprise.track="HDX" \
      enterprise.application="DaRT Automation" \
      org.opencontainers.image.title="hdx-dart-automation" \
      org.opencontainers.image.description="DaRT Automation Microservice" \
      org.opencontainers.image.vendor="Enterprise Banking Group"

WORKDIR /app

# Hardening: Create non-root system user & group (UID 10001)
RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup -s /sbin/nologin -d /app appuser

# Copy installed wheels from builder stage
COPY --from=builder --chown=appuser:appgroup /root/.local /app/.local
COPY --chown=appuser:appgroup src/ /app/src/
COPY --chown=appuser:appgroup pyproject.toml /app/

# Environment configurations
ENV PATH=/app/.local/bin:$PATH \
    PYTHONUSERBASE=/app/.local \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8080 \
    ENVIRONMENT=prod \
    APM_ID=AD00001234 \
    TRACK=HDX

# Security: Switch to non-root user
USER 10001:10001

EXPOSE 8080

# Healthcheck for container orchestrators (Kubernetes / ECS / Docker Swarm)
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/api/v1/health/live')" || exit 1

ENTRYPOINT ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]

