.PHONY: install lint format test security scan build run help

help:
	@echo "Enterprise DaRT Automation (APM ID: AD00001234, Track: HDX)"
	@echo "Available commands:"
	@echo "  make install    - Install production and development dependencies"
	@echo "  make lint       - Run Ruff code formatting and linting checks"
	@echo "  make format     - Automatically format code with Ruff"
	@echo "  make test       - Run all unit and integration test suites with coverage"
	@echo "  make security   - Run Bandit SAST and pip-audit vulnerability checks"
	@echo "  make build      - Build the hardened multi-stage Docker container"
	@echo "  make run        - Run the application locally with uvicorn"

install:
	pip install -r requirements-dev.txt

lint:
	ruff check src/ tests/
	ruff format --check src/ tests/

format:
	ruff format src/ tests/
	ruff check --fix src/ tests/

test:
	pytest tests/ --cov=src --cov-report=term-missing --cov-report=xml

security:
	bandit -r src/ -c pyproject.toml
	pip-audit

build:
	docker build -f docker/Dockerfile -t hdx-dart-automation:latest .

run:
	uvicorn src.main:app --host 0.0.0.0 --port 8080 --reload

