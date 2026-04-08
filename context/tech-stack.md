# Tech Stack – CLEAgora

> Updated 2026-04-08 — after first deployment.

## Platform

- **Community platform**: [Discourse](https://www.discourse.org/) (Ruby on Rails backend, Ember.js frontend)
  - Self-hosted via Docker (`discourse_docker` launcher)
  - Plugins (all bundled since late 2025): polls, reactions, data-explorer, automation
  - Live at: **https://cleagora.h2ai.app**
- **Interaction mode**: API-first — Discourse is the UI layer, intelligence lives outside

## Pipeline & Services (Python)

- **Language**: Python 3.11+
- **API client**: `src/discourse_client/` — httpx-based HTTP client with auth, rate limiting, retry. Modules: client, categories, topics, users.
- **Dependencies**: httpx, pydantic, python-dotenv
- **Dev tools**: ruff (linting), pytest
- **Bot service** (planned): FastAPI (scheduled topic posting, webhook listener, nudges)
- **Enrichment** (planned): LLM-powered (segmentation, tagging, write-up generation)
- **Output format**: JSON Lines (extraction), Markdown (write-ups)

## Infrastructure

- **Discourse instance**: AWS EC2 t3.small (i-014b79d534f31b382), Ubuntu 24.04, eu-west-3 (Paris)
  - IP: 13.38.105.2
  - Domain: cleagora.h2ai.app (Let's Encrypt SSL)
  - SSH: `ssh -i ~/.ssh/id_ed25519 ubuntu@13.38.105.2`
  - 2GB RAM + 2GB swap, 30GB disk
  - Security group: cleagora-sg (sg-0d22b0182609e4158)
  - Config: `/var/discourse/containers/app.yml` (local copy: `infra/app.yml`)
- **Other h2 services** (h2-apps-1, i-068957687f162210f, 15.224.11.232): bse, pyra, tria — NOT used for CLEAgora
- **Local dev**: Python venv (`.venv/`)
- **SMTP**: Not configured yet — needs SES setup or alternative

## Project tooling

- **Version control**: Git + GitHub
- **AI workflow**: Claude Code (terminal) + IDE assistant (Cursor/Kiro)
- **Context management**: Nexus pattern (`CLAUDE.md`, `context/*.md`)
- **No CI/CD yet** — to be set up when there's code to test/deploy

## Conventions

- Python: ruff for linting (line-length 100), type hints
- Modular architecture: extraction / enrichment / output as separate concerns
- `.env` for secrets (not committed), `.env.example` as template

***
*Last updated: 2026-04-08*
