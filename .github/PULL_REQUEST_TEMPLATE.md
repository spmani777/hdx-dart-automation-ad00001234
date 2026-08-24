## Enterprise Banking Change Request (PR)

### 📌 Governance & Metadata
- **Application Name**: DaRT Automation
- **APM ID**: `AD00001234`
- **Track**: `HDX`
- **Jira / ServiceNow Ticket #**: `HDX-`

---

### 📝 Summary of Changes
Provide a concise overview of the features, fixes, or refactors in this PR.

### 🛡️ Security & Compliance Checklist
- [ ] Code formatted and linted with Ruff (`make lint`)
- [ ] Unit & Integration tests passing with >80% coverage (`make test`)
- [ ] No hardcoded passwords, tokens, or private keys (Zero-Secret policy)
- [ ] SAST / Bandit scan clean (`make security`)
- [ ] Kubernetes health probes (`/health/live`, `/health/ready`) verified

### 🎯 Targeted Environments
- [ ] `dev` (Automatic deployment on merge)
- [ ] `staging` (Non-prod regression testing)
- [ ] `prod` (Requires change approval and tag)

