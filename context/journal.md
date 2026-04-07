# Journal – CLEAgora

<!-- Reverse chronological order: newest entries first. Always prepend below this line. -->

## Dev session #1 – 2026-04-07 (Adrien B.)

**Goal**: First Claude Code session — project initialization.

**What we did**:
- Explored the repo (no code yet, only context files from Cowork sessions).
- Generated `context/tech-stack.md` from repo scan (planned stack, no code conventions yet).
- Created `README.md`.
- Validated `.gitignore` (macOS metadata already covered, no tracked `.DS_Store`).
- Validated the backlog against repo state — no gaps or surprises.
- Initial commit of all project files.

**Decisions**:
- **Deployment path**: local Docker for dev → EC2 on AWS h2\ for production. Skip Hetzner. Rationale: Hetzner was planned as a prototype host, but going straight to AWS h2\ avoids an intermediate migration step.

**Next steps**:
- Set up local Discourse via Docker.
- Build the Python API client (`discourse_client/`).
- Create the France Inter study structure via API.

***

## Cowork session #2 – 2026-04-07 (Adrien B.)

**Goal**: Deep design — from Discourse research to full design document, flash deployment philosophy, restructuration model.

**What we did**:
- Conducted extensive web research on Discourse capabilities: closed communities, UI/UX customization, API & data extraction, plugins & automation. Produced `context/references/discourse-platform-guide.md` (comprehensive technical reference).
- Produced the full design document (`context/references/design-doc.md`) illustrated with a fictional France Inter matinale study. Covers: community architecture (categories, groups, permissions), respondent journey (invitation → onboarding → participation → closing), animation model (human + bot hybrid), technical architecture, extraction pipeline, and implementation phases.
- Clarified the **flash deployment** philosophy: 72h brief-to-output is the core product thesis. Brief → LLM parsing → YAML config → auto-setup Discourse + bot + pipeline → restructured write-ups.
- Defined the **restructuration model**: verbatim as atomic unit, LLM-powered segmentation, generated Markdown write-ups by respondent / theme / profile / study question / synthesis.
- Defined the **animation model**: human moderator for intellectual work + Python API bot for operations. LLM probes as later addition.
- Documented **multimodality roadmap**: stimuli injection (Discourse-native), rich responses (image/video), voice notes (transcription pipeline). Not in scope for proto.
- Searched for MCP connectors and Cowork plugins — nothing Discourse-specific available.
- Updated backlog with phased implementation aligned to design doc.

**Important decisions**:
- Flash deployment (72h) as core product thesis — everything is designed around brief → auto-config → field → restructured output.
- Markdown write-ups as primary restructured output (vs. Arcade/dashboard).
- Hybrid animation: human moderator + Python API bot (vs. full bot or Discourse AI plugin).
- Verbatim as minimal analysis unit, with LLM-powered segmentation.
- Brief input: primarily free text, LLM-parsed, with optional structured supplement.

**Open questions**:

**For PO**:
- Animation model details: how much latitude does the bot get for auto-probes vs. everything goes through moderator approval?
- Write-up templates: what does a "good" mise à plat look like for h2\? Do we have examples from existing CLEA studies?
- Brief format: do we have example study briefs we can use to test the brief → config parsing?
- Pilot timing: when would a first real pilot be realistic?

**Next steps**:
- First Claude Code session: set up Discourse Docker, build API client, create France Inter study structure.
- Validate design doc with PO — particularly the flash deployment chain and restructuration model.

***

## Cowork session #1 – 2026-04-07 (Adrien B.)

**Goal**: Initial framing of the CLEAgora project.

**What we did**:
- Clarified the vision: CLEAgora is a community-based CLEA variant where Discourse serves as the qualitative research terrain.
- Defined the core concept: collective-first (respondents interact with each other), closed community (email invitation), with a downstream extraction + enrichment pipeline.
- Positioned the project within the DECODia ecosystem (CLEA methodology adapted for community format).
- Created the full Nexus: CLAUDE.md, DEVS.md, and context files.
- Established the initial backlog with four immediate priorities: Discourse setup, API exploration, community architecture design, and animation model definition.

**Important decisions**:
- Discourse as the platform (vs. custom-built or SaaS alternatives).
- Collective-first interaction model (vs. 1:1 within Discourse).
- Exploration stage — prototype-first, validate the concept before investing in architecture.
- Infra: Hetzner for prototype, AWS h2\ for production.

**Open questions**:

**For PO**:
- Animation model: what's the initial intuition — full bot, human moderator, or hybrid? This drives the first technical choices.
- Do we have a pilot study in mind (client, topic, timeline) that could shape the prototype requirements?
- Naming convention for categories/topics in Discourse — should we define a standard structure (e.g., "Phase 1 — Exploration", "Stimulus — [name]") or keep it flexible for now?

**Next steps**:
- Start the first Claude Code session with this context.
- Set up a local Discourse instance (Docker).
- Explore the Discourse API and plugin ecosystem.

***
