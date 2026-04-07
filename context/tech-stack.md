# Tech Stack – CLEAgora

> Auto-generated on 2026-04-07 — first Claude Code session.
> No application code exists yet. This documents the planned stack based on design decisions.

## Platform

- **Community platform**: [Discourse](https://www.discourse.org/) (Ruby on Rails backend, Ember.js frontend)
  - Self-hosted via Docker (`discourse_docker` launcher)
  - Target plugins: polls, reactions, data-explorer, automation (all bundled)
- **Interaction mode**: API-first — Discourse is the UI layer, intelligence lives outside

## Pipeline & Services (Python)

- **Language**: Python 3.11+
- **API client**: Custom `discourse_client/` module (HTTP client with auth, rate limiting, CRUD)
- **Bot service**: FastAPI (scheduled topic posting, webhook listener, nudges)
- **Enrichment**: LLM-powered (segmentation, tagging, write-up generation) — provider TBD
- **Output format**: JSON Lines (extraction), Markdown (write-ups)

## Infrastructure

- **Local dev**: Docker (Discourse) + Python venv
- **Prototype**: Hetzner VPS
- **Production** (future): AWS (h2\ infrastructure)

## Project tooling

- **Version control**: Git + GitHub
- **AI workflow**: Claude Code (terminal) + IDE assistant (Cursor/Kiro)
- **Context management**: Nexus pattern (`CLAUDE.md`, `context/*.md`)
- **No CI/CD yet** — to be set up when there's code to test/deploy

## Conventions

- No application code exists yet. Conventions will be established when the first code is written.
- Expected: Python (black/ruff formatting, type hints), modular architecture (extraction / enrichment / output as separate concerns).

***
*Last updated: 2026-04-07*
