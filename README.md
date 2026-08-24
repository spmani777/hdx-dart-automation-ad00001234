# DaRT Automation (Data Remediation & Testing Engine)

[![PR Verification Gate](https://github.com/OWNER/hdx-dart-automation-ad00001234/actions/workflows/01-pr-gate.yml/badge.svg)](https://github.com/OWNER/hdx-dart-automation-ad00001234/actions/workflows/01-pr-gate.yml)
[![Security CodeQL](https://github.com/OWNER/hdx-dart-automation-ad00001234/actions/workflows/02-security-codeql.yml/badge.svg)](https://github.com/OWNER/hdx-dart-automation-ad00001234/actions/workflows/02-security-codeql.yml)
[![Container Security](https://github.com/OWNER/hdx-dart-automation-ad00001234/actions/workflows/03-security-trivy-harbor.yml/badge.svg)](https://github.com/OWNER/hdx-dart-automation-ad00001234/actions/workflows/03-security-trivy-harbor.yml)

---

## 🏛️ Enterprise Metadata & Governance
- **Application Name**: DaRT Automation Service
- **APM ID (Asset / Portfolio ID)**: `AD00001234`
- **Enterprise Track**: `HDX`
- **Architecture Standard**: 12-Factor Microservice, Zero-Trust Multi-Environment CI/CD

---

## 📁 Repository & Architecture Structure

```plaintext
hdx-dart-automation-ad00001234/
├── .github/
│   ├── workflows/                          # Complete CI/CD & Security Automation
│   │   ├── 01-pr-gate.yml                  # PR Gate: Ruff Lint, Unit Tests Matrix, Bandit SAST
│   │   ├── 02-security-codeql.yml          # GitHub CodeQL SAST Analysis
│   │   ├── 03-security-trivy-harbor.yml    # Container Security Scan & SBOM Generation
│   │   ├── 04-cd-dev.yml                   # Continuous Deployment to DEV Environment
│   │   ├── 05-cd-staging.yml               # Non-Prod / Staging (UAT) Deployment
│   │   ├── 06-cd-prod.yml                  # Production CD (Manual Approval Gate + Cosign Signing)
│   │   ├── 07-release-governance.yml       # Semantic Versioning & Compliance Audit Trail
│   │   └── ede-templates/                  # Enterprise Reusable Workflow Templates (EDE)
│   │       ├── ede-standard-ci-template.yml
│   │       └── ede-security-scan-template.yml
│   ├── actions/                            # Reusable Composite Actions
│   │   ├── setup-python-cache/
│   │   └── run-smoke-probes/
│   ├── ISSUE_TEMPLATE/                     # Standardized issue templates
│   ├── PULL_REQUEST_TEMPLATE.md            # Banking PR Checklist
│   └── dependabot.yml                      # Automated Weekly CVE Patching
│
├── src/                                    # Core Banking Application Source Code
│   ├── main.py                             # FastAPI Application Entrypoint
│   ├── config.py                           # 12-Factor Configuration Management
│   ├── api/v1/                             # Versioned REST APIs (Health, Remediation, Metrics)
│   └── services/                           # Banking Rules & Audit Trail Loggers
│
├── tests/                                  # Multi-Tier Automated Test Suites
│   ├── unit/                               # Fast Unit Tests (< 500ms)
│   ├── integration/                        # API & End-to-End Tests
│   └── smoke/                              # Post-Deployment Live Environment Probes
│
├── environments/                           # Config templates for dev, staging, prod
├── docker/                                 # Hardened Non-Root Multi-Stage Dockerfile
├── scripts/                                # Local DevOps & Smoke Probe Scripts
├── pyproject.toml / requirements.txt       # Tool Configurations & Pinned Dependencies
└── Makefile                                # Developer CLI Shortcuts
```

---

## 🚀 The 7 CI/CD Workflows Explained

| Workflow | Trigger | Jobs & Key Steps |
| :--- | :--- | :--- |
| **`ci.yml`** | Push to any branch + all PRs | **PRIMARY ENTRY POINT.** 5 jobs: Lint (Ruff), Security SAST (Bandit + pip-audit), Matrix Tests (Python 3.11 & 3.12 in parallel), Container Build Verification (no push), CI Gate (single branch protection check). |
| **`01-pr-gate.yml`** | Pull Requests to `main` or `develop` | Focused fast PR feedback: Ruff, Bandit, Matrix Tests with coverage upload artifact. |
| **`02-security-codeql.yml`** | Push / PR / Weekly Cron | GitHub CodeQL semantic AST scan for OWASP Top 10 vulnerabilities. Populates repository **Security** tab. |
| **`03-security-trivy-harbor.yml`** | Push to `main` / `develop` | Builds local container. Scans container OS & dependencies with Aqua Security Trivy. Generates SPDX SBOM and uploads SARIF report. |
| **`04-cd-dev.yml`** | Push / Merge to `develop` | Builds & pushes image tagged `AD00001234-${{ github.sha }}` to GHCR. Deploys container to `dev` environment. Executes automated post-deploy smoke probes. |
| **`05-cd-staging.yml`** | Push to `main` / `release/**` | Deploys container to `staging` environment. Executes full API regression test suite. |
| **`06-cd-prod.yml`** | Release Tag `v*.*.*` or Manual Dispatch | **Gate**: Enforces GitHub Environment Required Reviewer Approval. **Cosign/Venafi**: Cryptographically signs container digest with Sigstore. Deploys to `prod` and runs rollback safety probes. |
| **`07-release-governance.yml`** | Release Tag `v*.*.*` | Generates compliance release manifest and auto-publishes GitHub Release with changelog. |

---

## 🔐 Variables and Secrets Setup

### Repository Variables (`Settings -> Secrets and variables -> Actions -> Variables`)
- `APM_ID`: `AD00001234`
- `TRACK`: `HDX`

### GitHub Environments (`Settings -> Environments`)
Create three environments:
1. **`dev`**: No deployment branch restrictions (automatic deploy).
2. **`staging`**: Restricted to `main` and `release/**` branches.
3. **`prod`**:
   - Check **Required reviewers** (add your GitHub username as reviewer).
   - Restricted to `tags/v*.*.*` or `main`.

---

## 💻 Local Developer Commands

```bash
# Run code formatting and linting
make lint

# Run unit and integration tests with coverage
make test

# Run SAST security checks
make security

# Build Docker container image
make build
```

---

## 🛠️ Step-by-Step Hands-On Guide: Pushing to GitHub

1. **Create a new GitHub Repository**:
   - Go to [GitHub.com/new](https://github.com/new).
   - Name: `hdx-dart-automation-ad00001234` (or any name you prefer).
   - Visibility: **Public** (recommended to get free unlimited GitHub Actions & Security Tab) or Private.
   - Do NOT initialize with README/license (we already built everything!).

2. **Link Local Repository and Push**:
   ```bash
   cd C:\Users\91998\.gemini\antigravity\scratch\hdx-dart-automation-ad00001234
   git remote add origin https://github.com/<YOUR-USERNAME>/hdx-dart-automation-ad00001234.git
   git branch -M main
   git push -u origin main
   ```

3. **Observe the Actions Tab**:
   - Go to your repository on GitHub and click the **Actions** tab.
   - You will see the CI/CD pipelines trigger automatically!

