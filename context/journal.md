# Journal – CLEAgora

<!-- Reverse chronological order: newest entries first. Always prepend below this line. -->

## Dev session #4 – 2026-04-08 (Adrien B.)

**Goal**: UI tweaks, fake data population, splash page, branding polish.

**What we did**:
- **Category description banners** (CSS-only): added per-category `::after` pseudo-elements on `.category-breadcrumb`, scoped via `body.category-{slug}`. Shows 1-2 sentence intro above topic list for each module. No JS needed.
- **"À propos" topics hidden**: Discourse protects category definition topics from deletion. Solution: unpinned + unlisted all 8 "About" topics — invisible to regular users.
- **FAQ rewritten**: replaced generic Discourse FAQ with content adapted for quali respondents (bienvenue, comment participer, échanges sereins, confidentialité, aide).
- **Splash/welcome page** (`assets/welcome.html`): standalone HTML page for respondent onboarding. Warm, human tone. Hero + 3 steps + 4 reassurance blocks + CTA to cleagora.h2ai.app. Can be shown independently for demos.
- **Fake data populated**: 10 respondent accounts created (Sophie, Thomas, Nathalie, Julien, Claire, Patrick, Amina, François, Lucie, Marc), all in `auditeurs` group, trust level 2. ~42 realistic posts across all 9 study topics + 1 free topic in Le café. Varied writing styles, @mentions, debates.
- **Site icon/favicon**: uploaded Clea's h2\ avatar as `logo_small`, `favicon`, and `large_icon`.
- **Theme component re-attached** to Foundation (was detached since session #3 due to JS crash). CSS works fine; JS welcome banner attempted but not rendering (deferred).
- **CSS fixes**: removed overly aggressive wildcard selectors (`[class*="welcome-banner"]`, `.search-container`) that were hiding homepage content.
- **Le café permissions fixed**: category had lost group permissions; restored auditeurs=create, animateurs=create, chercheurs=see.

**Known issues**:
- **Welcome banner JS** (`theme-head.html`): `<script>` tag with `Discourse.User.current()` doesn't execute — possibly blocked by Discourse CSP or the global isn't available at that point. Debug logging added but untested. Needs investigation with browser console.
- **Le café posts**: users couldn't post to Le café despite correct permissions — had to fall back to `system` user. Possibly Discourse permission cache issue after update. Needs testing.
- **Category description `description_text`** may have been cleared on some categories when About topics were unlisted (they're linked in Discourse). CSS banners replace the visual, but API `description_text` may be empty. Not blocking for now.

**Not done (next session)**:
- Fix welcome banner JS (try `apiInitializer` gjs format instead of head_tag script)
- SMTP: SES domain verification still pending, configure Discourse app.yml
- SES production access request
- Test full respondent journey (invitation → login → participate)
- Basic extraction pipeline (posts → JSON Lines)

**Open questions**:

**For PO**:
- Welcome page (`assets/welcome.html`): validated? Want any content/tone changes?
- SES cleagora.com: DNS verification status?
- Ready to show the demo to stakeholders?

***

## Dev session #3 – 2026-04-08 (Adrien B.)

**Goal**: UX customization, France Inter study structure, demo respondent, SMTP setup, branding.

**What we did**:
- **SMTP/SES**: Registered `cleagora.com` domain. Created SES domain identity in eu-west-3. Generated DKIM tokens, SPF, DMARC records. DNS records added by PO — verification still pending (propagation).
- **Discourse UX customization** (42+ site settings via API): closed community (login_required + invite_only), badges/likes/gamification disabled, Discobot disabled, navigation simplified, posting thresholds lowered, trust level gates zeroed, user directory hidden, suggested topics disabled, tags disabled.
- **France Inter study structure**: created 3 groups (auditeurs, animateurs, chercheurs), 6 categories with permissions (Bienvenue, Module 1/2/3, Le café, Coulisses), 12 discussion topics with prompts, 2 pinned topics.
- **Demo respondent**: `marie_dupont` (Marie Dupont) created, added to auditeurs group.
- **Branding**: uploaded CLEAgora logo (PNG from PO), set community title "Communauté La Matinale de France Inter", created h2\ color palette (#425779/#E8622C/#0E131B/#86898D), switched to light theme, logo resized 25% smaller.
- **Clea bot account**: created `clea` user with h2\ icon avatar, admin + animateurs + chercheurs. Reassigned 18 system posts to clea. `.env` updated to post as clea by default.
- **Category renames**: "Semaine N" → "Module N". Updated descriptions with intro text for each module.
- **Translation overrides**: 42+ Discourse UI strings changed "catégorie" → "module" (sidebar, breadcrumbs, topic titles, search, etc.).
- **Theme component** (CLEAgora Customizations): CSS for hiding sidebar items (Inviter, Filtre, Sujets, Toutes les catégories, Mes messages), renaming "Catégories" → "MODULES" in sidebar, hiding "Créer un sujet" for non-staff, hiding topic footer buttons except Répondre, hiding tags, category description banner styling.
- **Default categories** (Général, Responsables, Commentaires): restricted to staff-only or deleted.
- **Scripts created**: `customize_discourse.py` (site settings), `apply_customizations.py` (text overrides + category renames), `apply_theme.py` (theme component CSS/JS).
- **New client module**: `src/discourse_client/settings.py` (get/update site settings).

**Known issue — theme JS crashes page render**:
- The theme component's JS (welcome banner, community title in header, "Catégories"→"Modules" rename, category description banner) causes blank page. Root cause: Discourse 2026 deprecated `<script type="text/discourse-plugin">` and removed `controller:discovery/topics`. Standard `<script>` in `head_tag` also failed. Component is currently **detached** from Foundation theme to keep the site functional.
- CSS-only customizations work fine. JS needs to be migrated to Discourse's new theme JS module format.

**Not done (next session)**:
- Fix theme JS (use Discourse 2026 theme JS module format instead of deprecated script tags)
- Welcome banner with personalized greeting
- Community title text in header bar
- Hide welcome banner + search bar on homepage
- Hide "Alimenté par Discourse" footer
- Category description banners on module pages
- SMTP: wait for SES domain verification, then configure Discourse app.yml + rebuild
- SES production access request (currently sandbox — can only send to verified emails)
- Test full respondent journey (invitation → login → participate)
- Populate with fake respondent data (~10 users, ~30 posts)

**Open questions**:

**For PO**:
- SES `cleagora.com` verification still pending — check DNS propagation. If still pending tomorrow, verify records at registrar.
- Branding: the current logo works well. Do we want a favicon / mobile icon too?
- Welcome text: "Bonjour [prénom] ! Ravis de t'avoir à bord..." — validate the tone/content before we re-implement the JS.

***

## Dev session #2 – 2026-04-08 (Adrien B.)

**Goal**: Deploy Discourse on AWS + build Python API client.

**What we did**:
- Explored h2-apps-1 (i-068957687f162210f, 15.224.11.232): too loaded for Discourse (1.9GB RAM, 3 apps running, nginx on 80/443, no Docker). Decision: create dedicated instance.
- Created dedicated EC2 instance `cleagora-discourse` (i-014b79d534f31b382, t3.small, Ubuntu 24.04, eu-west-3, IP 13.38.105.2). Security group `cleagora-sg` (ports 22/80/443). Added 2GB swap.
- Deployed Discourse via `discourse_docker`. Bootstrap issues resolved: (1) `LC_ALL`/`LANG` locale env vars break bootstrap — use `DISCOURSE_DEFAULT_LOCALE: fr` only; (2) data-explorer, automation, reactions plugins are now bundled — do NOT add them to `after_code` hooks.
- Enabled Let's Encrypt SSL after DNS propagation. Discourse live at **https://cleagora.h2ai.app**.
- Created admin account (`adrien` / ab@ubyx.com) via Rails console. Generated global API key.
- Built Python project structure: `src/discourse_client/` (client.py, categories.py, topics.py, users.py), `scripts/setup_france_inter.py`, `pyproject.toml`. Dependencies: httpx, pydantic, python-dotenv. All installs and lints clean.
- Tested Python client against live Discourse API — works.
- Researched Discourse customization for private qualitative research communities: branding, feature removal, information architecture, respondent experience flow. Comprehensive settings list ready for next session.

**Decisions**:
- **Dedicated EC2 for Discourse** (not h2-apps-1): h2-apps-1 too loaded (RAM, disk, port conflicts). See decisions.md.
- **Information architecture**: one category per study day/phase (not flat topics, not tags-only). Categories provide permission control and progressive disclosure.
- **UX strategy**: strip Discourse down aggressively (disable badges, likes, gamification, Discobot, user directory, suggested topics), install Trendy Login for branded login page, Tab Bar for mobile.

**Not done (next session)**:
- Apply all Discourse site settings (badges off, likes off, navigation simplification, etc.)
- Install theme components (Trendy Login, Tab Bar for Mobile) + CSS overrides
- Create demo respondent account for UX testing
- Create France Inter mockup categories and topics
- Customize branding, email templates, welcome PM
- SMTP setup (no email sending yet — admin activated via Rails console)

**Open questions**:

**For PO**:
- SMTP: need to set up SES for `h2ai.app` domain (DKIM/SPF/DMARC verification). Or use another provider?
- Branding: do we have a logo/visual identity for CLEAgora or for the France Inter study?
- Demo: how many days for the mockup study sprint? 4 or 5? (affects category structure)

***

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
