# Decisions – CLEAgora

## 2026-04-08 – cleagora.com as email sending domain

**Context**: Discourse needs outbound SMTP for invitations, notifications, and password resets. The existing `h2ai.app` domain had no MX records and DNS access was unclear.

**Decision**: Register `cleagora.com` as a dedicated domain. Use AWS SES in eu-west-3 for sending. Domain verified via DKIM (3 CNAME), SPF (TXT), DMARC (TXT). No MX record needed (outbound only).

**Rejected alternatives**:
- `h2ai.app` or `cleagora.h2ai.app` (less control over DNS, mixing concerns).
- External SMTP provider like Mailgun/Sendgrid (additional vendor, SES is already in AWS).

**Consequences**: `cleagora.com` DNS records to maintain. SES starts in sandbox mode — need production access request before real study. Emails come from `@cleagora.com` (clean, professional).

***

## 2026-04-08 – Clea bot account replaces system user for community posts

**Context**: All study topics and moderation posts were created by the Discourse `system` account, which shows a generic black "C" avatar and "system" username — impersonal for respondents.

**Decision**: Create a dedicated `clea` admin account with the h2\ icon as avatar. All API posts go through `clea`. Existing system posts reassigned. The `system` account is still used for admin API operations (theme management, site settings).

**Rejected alternatives**:
- Rename the `system` account (protected by Discourse, cannot be renamed).
- Use Adrien's admin account for bot posts (mixes human and automated activity).

**Consequences**: Two API usernames: `clea` for content creation (`.env` default), `system` for admin operations. The Clea persona gives the community a branded, approachable "host" identity.

***

## 2026-04-08 – Dedicated EC2 instance for Discourse (not cohosting on h2-apps-1)

**Context**: The plan was to deploy Discourse on h2-apps-1 (t3.small, 15.224.11.232) alongside existing services. Assessment revealed: only 1.9GB RAM total (~1GB free), 9.7GB disk free, ports 80/443 taken by nginx, Docker not installed, 3 apps already running (bse, pyra, tria).

**Decision**: Create a dedicated t3.small EC2 instance (`cleagora-discourse`, i-014b79d534f31b382, 13.38.105.2) for Discourse. Avoids resource contention and port conflicts.

**Rejected alternatives**:
- Cohosting on h2-apps-1 (insufficient RAM — Discourse needs 2GB minimum, port conflicts, risk to existing services).
- t3.medium (4GB RAM, ~$30/mo) — comfortable but unnecessary for prototype with 2GB swap.

**Consequences**: ~$15/mo additional AWS cost. Clean single-purpose instance. Discourse has full access to 2GB RAM + 2GB swap + 30GB disk. Independent lifecycle from other h2 services.

***

## 2026-04-08 – Information architecture: one category per study day/phase

**Context**: Need to structure a 4-5 day qualitative research sprint. Options: flat topics in one category, topics tagged by day, or one category per day.

**Decision**: One category per study day/phase. Categories provide permission control (hide future days), visual grouping on the homepage, and natural progressive disclosure. Tags are secondary (for research team thematic tagging, not respondent navigation).

**Rejected alternatives**:
- Single category + tags (flatter but tags are less visible, no permission control per day).
- Flat topics with no categorization (every Discourse topic must belong to a category anyway, and no progressive disclosure).

**Consequences**: The homepage categories view becomes the day-by-day agenda. Progressive disclosure via category permissions or topic timers. France Inter study structure: 3-5 day categories + Le café (free space) + Coulisses (staff-only).

***

## 2026-04-08 – Aggressive UX simplification for respondent experience

**Context**: Discourse is designed for tech-savvy community users. CLEAgora respondents are regular people invited to share opinions over 4-5 days. Most forum features (badges, gamification, likes, trust levels, user directory, suggested topics) add noise and confusion.

**Decision**: Strip Discourse to its essentials. Disable badges, likes, Discobot, user directory, suggested topics. Simplify navigation to categories-only. Lower posting thresholds. Install Trendy Login for branded login page, Tab Bar for mobile. Use CSS overrides to hide remaining visual noise (trust levels, stats, footer).

**Rejected alternatives**:
- Keep Discourse mostly vanilla (too much cognitive overhead for respondents, feels like "a tech forum").
- Build a custom frontend (way too much work for exploration stage).

**Consequences**: Respondent experience is clean and focused. Maintenance overhead from CSS overrides (fragile across Discourse updates, acceptable for short study sprints). Need to test the full respondent journey before each study.

***

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
