# Decisions – CLEAgora

## 2026-04-07 – Deployment path: local Docker → AWS EC2

**Context**: The original plan had three stages: local Docker (dev) → Hetzner VPS (prototype) → AWS h2\ (production). Hetzner added a migration step for a small cost benefit.

**Decision**: Skip Hetzner. Go local Docker for development, then deploy directly on EC2 within h2\'s AWS infrastructure.

**Rejected alternatives**:
- Hetzner VPS as intermediate (extra migration, one more environment to manage for marginal savings).
- Local-only (can't test invitations, SMTP, or share with stakeholders).

**Consequences**: Need AWS access and a domain/subdomain when ready to deploy. No intermediate hosting cost. Local Docker is the only dev environment.

***

## 2026-04-07 – Discourse as the research terrain

**Context**: CLEAgora needs a platform for closed community-based qualitative research. The original CLEA uses a custom 1:1 conversational interface. For the community variant, we need a forum/community platform that supports structured discussions, user management, and content extraction.

**Decision**: Use Discourse as the community platform. Discourse replaces CLEA's conversational interface — it IS the research terrain where respondents interact.

**Rejected alternatives**:
- Custom-built forum (too much effort for a prototype, reinventing solved problems).
- Existing community platforms like Circle, Mighty Networks (SaaS dependency, limited API/extensibility, sovereignty concerns).
- Adapting CLEA's 1:1 interface to support group conversations (loses the organic community dynamics).

**Consequences**: We inherit Discourse's strengths (mature forum software, rich API, plugin ecosystem, self-hostable) and constraints (Ruby on Rails stack, opinionated architecture, plugin API boundaries). The extraction pipeline must work through Discourse's API rather than direct database access.

***

## 2026-04-07 – Collective-first interaction model

**Context**: CLEA's original model is 1:1 (respondent ↔ AI assistant). A community platform naturally supports group interaction. We needed to decide whether to preserve 1:1 dynamics within Discourse or lean into the collective dimension.

**Decision**: Collective-first. The primary value of CLEAgora comes from respondents interacting with each other — debate, co-construction, mutual stimulation. This differentiates it from standard CLEA.

**Rejected alternatives**:
- 1:1 via Discourse private messages (loses the community value, might as well use standard CLEA).
- Hybrid with equal weight on 1:1 and collective (added complexity for a prototype, dilutes the differentiating concept).

**Consequences**: The study design, animation model, and analysis pipeline must be built around group dynamics. The enrichment layer needs to capture interaction patterns (who responds to whom, agreement/disagreement, topic evolution) not just individual verbatims.

***

## 2026-04-07 – Flash deployment as core product thesis

**Context**: CLEAgora needs to define its operational model. Traditional online communities take days/weeks to set up and configure for each study.

**Decision**: Flash deployment — the entire chain from study brief to live community to restructured output should fit within a **72h window**. Speed and agility are the primary differentiators. The system is designed around a `brief → auto-config → field → restructured output` pipeline where most of the setup is automated via LLM parsing of the brief.

**Rejected alternatives**:
- Manual per-study configuration (traditional approach — too slow, defeats the purpose).
- Fully templated studies with no brief parsing (too rigid, doesn't adapt to each study's questions).

**Consequences**: The study configuration system (YAML) becomes the central artifact. The `brief → config` LLM chain is a first-class component, not an afterthought. Everything downstream (Discourse setup, bot schedule, extraction, restructuration) must be drivable from config. This implies a declarative, automatable architecture end to end.

***

## 2026-04-07 – Restructured output as generated Markdown write-ups

**Context**: CLEAgora needs to define how the extracted and enriched material is delivered to researchers. Options: raw JSON for Arcade, generated documents, interactive dashboards.

**Decision**: Generate **Markdown write-ups** as the primary output — by respondent, by theme, by profile, by study question, plus a synthesis. The verbatim is the atomic unit; write-ups recompose verbatims along different axes. Documents are immediately readable and shareable, with no dependency on another tool.

**Rejected alternatives**:
- JSON-only output to Arcade (adds dependency, not self-contained for the prototype).
- Interactive dashboard (higher dev effort, less aligned with researcher workflows).

**Consequences**: Need a write-up generation layer (LLM-powered, template-driven) on top of the enrichment pipeline. Write-up templates must be derived from the study brief (another reason the brief → config chain matters). Arcade integration remains a future goal — the JSON enriched data is the pivot format that can feed both write-ups and Arcade.

***

## 2026-04-07 – Hybrid animation model (human moderator + API bot)

**Context**: Community animation can be fully human, fully automated (AI bot), or hybrid. Need to decide for the prototype.

**Decision**: Hybrid — human moderator handles intellectual work (substantive probes, connecting respondent contributions, sensing group dynamics), Python API bot handles operations (scheduled topic posting, engagement nudges, activity tracking, pipeline triggers). LLM-powered probes as a later addition with moderator approval.

**Rejected alternatives**:
- Full bot (risks mechanical, shallow interactions; misses the subtlety of group dynamics).
- Full human (too much manual work for routine tasks; doesn't scale).
- Discourse AI plugin as primary bot (Ruby/Ember stack, less control than external Python service).

**Consequences**: Bot is a Python FastAPI service, not a Discourse plugin. This keeps the AI logic in the familiar Python stack, close to the enrichment pipeline. Discourse is the UI layer; intelligence lives outside.

***
