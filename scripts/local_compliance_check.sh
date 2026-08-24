#!/usr/bin/env bash
set -euo pipefail

echo "============================================================"
echo " DaRT Automation [APM ID: AD00001234 | Track: HDX]"
echo " Running Local Compliance, Security & Quality Checks"
echo "============================================================"

echo "Step 1: Checking Code Formatting & Linting (Ruff)..."
ruff check src/ tests/
ruff format --check src/ tests/

echo "Step 2: Running SAST Security Audit (Bandit)..."
bandit -r src/ -c pyproject.toml

echo "Step 3: Running Test Suites with Coverage Threshold..."
pytest tests/ --cov=src --cov-fail-under=80

echo "============================================================"
echo " [SUCCESS] All local checks passed! Code is ready for CI PR."
echo "============================================================"

