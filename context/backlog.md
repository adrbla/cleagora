# Backlog – CLEAgora

> Aligned with design doc (`context/references/design-doc.md`).
> Vision: **72h flash deployment** — brief → community → restructured output.

## Now — Phase 1: Foundation (target: 2 weeks)

- [x] **Design document** — Community architecture, respondent journey, animation model, technical architecture, implementation strategy. Flash deployment philosophy. Restructuration design.
- [x] **Discourse instance setup** — EC2 deployment (t3.small, eu-west-3). HTTPS via Let's Encrypt at cleagora.h2ai.app. Admin account + API key.
- [x] **Discourse API client (Python)** — `discourse_client/` module: HTTP client with auth + rate limiting, CRUD for topics/posts/users/groups, invite management, site settings.
- [x] **Discourse UX customization** — Site settings applied (42+), translation overrides (42+ strings catégorie→module), h2\ color palette, light theme. CSS theme component created (sidebar cleanup, topic footer, tags hidden). **Partial**: theme JS (welcome banner, header title, footer hide) crashes — needs migration to Discourse 2026 JS module format.
- [x] **Demo respondent account** — `marie_dupont` (Marie Dupont) in auditeurs group.
- [x] **Study category structure** — 3 groups, 6 categories (Bienvenue, Module 1/2/3, Le café, Coulisses), 12 topics with prompts. Categories renamed from "Semaine N" to "Module N" with intro descriptions.
- [x] **Branding** — CLEAgora logo, Clea bot account with h2\ avatar, community title set.
- [x] **Category description banners** — CSS-only `::after` pseudo-elements on `.category-breadcrumb` scoped via `body.category-{slug}`. Replaces "À propos" topics (unlisted).
- [x] **FAQ rewritten** — Adapted for quali respondents (vs. generic Discourse).
- [x] **Splash/welcome page** — `assets/welcome.html`, standalone, demo-ready.
- [x] **Fake data populated** — 10 respondents, ~42 posts across all topics. Realistic content with varied styles.
- [x] **Site icon/favicon** — Clea h2\ avatar as logo_small, favicon, large_icon.
- [ ] **Fix theme JS** — Welcome banner with personalized greeting. `<script>` in head_tag doesn't execute. Try Discourse 2026 `apiInitializer` gjs format via `extra_js` theme field.
- [ ] **SMTP setup** — SES domain identity created for `cleagora.com`, DNS records added, verification pending. Next: configure Discourse app.yml once verified, request SES production access.
- [ ] **Basic extraction** — Pull all posts from a study category → JSON Lines output with full metadata (raw + cooked content, reply graph, user custom fields, reactions).

## Next — Phase 2: Bot + Enrichment + Verbatim Pipeline

- [ ] **Bot service** — Python FastAPI: scheduler for posting topics on schedule, webhook listener for `post_created`, PM sender for engagement nudges.
- [ ] **Study YAML configuration** — Declarative study definition (phases, categories, topic templates, schedule, probe templates). Config-driven Discourse setup.
- [ ] **Verbatim segmentation** — LLM-powered: segment posts into verbatims (minimal units of meaning), tag boundaries, link to source.
- [ ] **Enrichment Layer 1 (descriptive)** — Per-verbatim: entities, sentiment, emotions, thematic tags.
- [ ] **Enrichment Layer 2 (interactions)** — Reply graph, agreement/disagreement detection, influence scoring.
- [ ] **Invitation workflow** — CSV bulk invite via API, auto-assign groups, branded email template.
- [ ] **End-to-end integration test** — Full cycle: invite → participate → extract → segment → enrich.

## Later — Phase 3: Restructuration + Brief-to-Config

- [ ] **Write-up generation** — LLM-powered Markdown generation: by respondent, by theme, by profile, by study question, synthesis. Template-driven.
- [ ] **Brief → Config chain** — LLM parses free-text brief → generates structured YAML study config. Gap detection + structured supplement.
- [ ] **Config → Discourse setup** — Auto-apply YAML config: create categories, groups, permissions, schedule topics, configure bot.

## Backlog — Future Vision

- [ ] **Enrichment Layer 3 (analytical)** — Study-question alignment, signal strength, tension/convergence. Researcher review workflow.
- [ ] **LLM-powered animation probes** — Contextual follow-ups generated from discussion content + study objectives. Moderator approval queue.
- [ ] **Multimodality: stimuli** — Audio/video/image stimulus injection in topics (Discourse-native, low effort).
- [ ] **Multimodality: rich responses** — Enable image/video upload by respondents, integrate into extraction pipeline.
- [ ] **Multimodality: voice** — Voice note upload → transcription (Whisper) → verbatim pipeline.
- [ ] **Arcade integration** — Feed enriched JSON output into h2\ Arcade workspace.
- [ ] **Multi-study support** — Multiple isolated studies on one Discourse instance.
- [ ] **Longitudinal mode** — Diary studies / usage journals within the community.
- [ ] **QORA bridge** — Mixed-methods: community quali + structured quanti.

***
*Last updated: 2026-04-08 (session #4)*
