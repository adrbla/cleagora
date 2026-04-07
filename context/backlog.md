# Backlog – CLEAgora

> Aligned with design doc (`context/references/design-doc.md`).
> Vision: **72h flash deployment** — brief → community → restructured output.

## Now — Phase 1: Foundation (target: 2 weeks)

- [x] **Design document** — Community architecture, respondent journey, animation model, technical architecture, implementation strategy. Flash deployment philosophy. Restructuration design.
- [ ] **Discourse instance setup** — Docker-based local Discourse. Configure: `login_required`, `invite_only`, `default_trust_level: 1`, French locale. Enable bundled plugins (polls, reactions, data-explorer, automation).
- [ ] **Discourse API client (Python)** — `discourse_client/` module: HTTP client with auth + rate limiting, CRUD for topics/posts/users/groups, invite management.
- [ ] **Study category structure** — Create the France Inter study categories, groups (`auditeurs`, `animateurs`, `chercheurs`), permissions matrix, sample topics with topic templates.
- [ ] **Basic extraction** — Pull all posts from a study category → JSON Lines output with full metadata (raw + cooked content, reply graph, user custom fields, reactions).
- [ ] **Test with fake data** — Populate Discourse with ~10 fake respondents, ~30 posts across categories. Extract and verify output structure.

## Next — Phase 2: Bot + Enrichment + Verbatim Pipeline

- [ ] **Bot service** — Python FastAPI: scheduler for posting topics on schedule, webhook listener for `post_created`, PM sender for engagement nudges.
- [ ] **Study YAML configuration** — Declarative study definition (phases, categories, topic templates, schedule, probe templates). Config-driven Discourse setup.
- [ ] **Verbatim segmentation** — LLM-powered: segment posts into verbatims (minimal units of meaning), tag boundaries, link to source.
- [ ] **Enrichment Layer 1 (descriptive)** — Per-verbatim: entities, sentiment, emotions, thematic tags.
- [ ] **Enrichment Layer 2 (interactions)** — Reply graph, agreement/disagreement detection, influence scoring.
- [ ] **Invitation workflow** — CSV bulk invite via API, auto-assign groups, branded email template, Discobot customization.
- [ ] **End-to-end integration test** — Full cycle: invite → participate → extract → segment → enrich.

## Later — Phase 3: Restructuration + Brief-to-Config

- [ ] **Write-up generation** — LLM-powered Markdown generation: by respondent, by theme, by profile, by study question, synthesis. Template-driven.
- [ ] **Brief → Config chain** — LLM parses free-text brief → generates structured YAML study config. Gap detection + structured supplement.
- [ ] **Config → Discourse setup** — Auto-apply YAML config: create categories, groups, permissions, schedule topics, configure bot.
- [ ] **Custom Discourse theme** — Study-branded, simplified UI.
- [ ] **AWS EC2 deployment** — Discourse + CLEAgora services on h2\ AWS, SSL, SMTP, backups.

## Backlog — Future Vision

- [ ] **Enrichment Layer 3 (analytical)** — Study-question alignment, signal strength, tension/convergence. Researcher review workflow.
- [ ] **LLM-powered animation probes** — Contextual follow-ups generated from discussion content + study objectives. Moderator approval queue.
- [ ] **Multimodality: stimuli** — Audio/video/image stimulus injection in topics (Discourse-native, low effort).
- [ ] **Multimodality: rich responses** — Enable image/video upload by respondents, integrate into extraction pipeline.
- [ ] **Multimodality: voice** — Voice note upload → transcription (Whisper) → verbatim pipeline.
- [ ] **Arcade integration** — Feed enriched JSON output into h2\ Arcade workspace.
- [ ] **Multi-study support** — Multiple isolated studies on one Discourse instance.
- [ ] **Longitudinal mode** — Diary studies / usage journals within the community.
- [ ] **AWS production deployment** — h2\ infrastructure, monitoring, security.
- [ ] **QORA bridge** — Mixed-methods: community quali + structured quanti.

***
*Last updated: 2026-04-07*
