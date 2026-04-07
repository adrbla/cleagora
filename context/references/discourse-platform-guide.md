# Discourse as a Qualitative Research Platform — Technical Reference

> Reference document for CLEAgora. Covers Discourse capabilities relevant to building a community-based qualitative research platform. Written for the PO (who doesn't know Discourse well) and for Claude Code (as implementation context).

---

## Table of Contents

1. [What Discourse Is](#1-what-discourse-is)
2. [Closed Community Setup](#2-closed-community-setup)
3. [Upstream Integration: User Accounts & Invitations](#3-upstream-integration-user-accounts--invitations)
4. [Community Architecture: Categories, Groups, Permissions](#4-community-architecture-categories-groups-permissions)
5. [UI/UX Customization & Branding](#5-uiux-customization--branding)
6. [Content Types & Respondent Experience](#6-content-types--respondent-experience)
7. [Animation & Moderation: Bots, AI, Automation](#7-animation--moderation-bots-ai-automation)
8. [Downstream Integration: API & Data Extraction](#8-downstream-integration-api--data-extraction)
9. [Plugin Ecosystem & Extensibility](#9-plugin-ecosystem--extensibility)
10. [Infrastructure & Deployment](#10-infrastructure--deployment)
11. [Key Risks & Limitations](#11-key-risks--limitations)
12. [Sources](#12-sources)

---

## 1. What Discourse Is

Discourse is an open-source forum platform (Ruby on Rails backend, Ember.js frontend). It's the most mature modern forum software — used by communities ranging from developer forums to brand communities. Self-hostable, with a rich plugin ecosystem and a comprehensive REST API.

**Why it fits CLEAgora**: it provides user management, structured discussions, notifications, moderation, and an API for data extraction — all out of the box. We configure and extend it rather than building from scratch.

**Key mental model**: Discourse organizes content as **Categories** (top-level spaces) containing **Topics** (discussion threads) containing **Posts** (individual messages). Users belong to **Groups** which control access via **Permissions**.

---

## 2. Closed Community Setup

CLEAgora requires a closed, invitation-only community. Discourse supports this natively via three site settings:

| Setting | What it does | Recommended for CLEAgora |
|---------|-------------|------------------------|
| `login_required` | Requires login to see any content | **Yes** — no anonymous browsing |
| `invite_only` | Disables public signup; users can only join via invitation | **Yes** — respondents are recruited externally |
| `must_approve_users` | Admin must approve each new account | Optional — belt-and-suspenders if needed |

**Recommended combination**: `login_required: true` + `invite_only: true`. This creates a fully closed instance where only invited respondents can access content.

Additional hardening options:
- `allowed_email_domains`: restrict registration to specific email domains.
- `invite_expiry_days`: control how long invitation links remain valid.
- Disable all social login providers (Google, GitHub, etc.) if you want email-only auth.

---

## 3. Upstream Integration: User Accounts & Invitations

### Email Invitations

Discourse has a robust invitation system:

- **Individual invites**: Admin or staff can invite users one by one via email. The invitation email is customizable (Admin → Customize → Email Templates).
- **Bulk CSV import**: Upload a CSV with columns `email,groups,topic_id` to invite many respondents at once. Each row can auto-assign the user to specific groups on signup.
- **API-based invitations**: `POST /invites` endpoint to create invitations programmatically. Supports specifying groups, custom message, and expiry.
- **Invite links**: Generate a reusable link (with optional max redemptions) for a group of respondents.

**Practical flow for a study**:
1. Prepare a CSV: `email,groups` (e.g., `respondent@email.com,study-wave-1`).
2. Upload via Admin → Users → Invite → Bulk Invite, or via API.
3. Respondents receive a branded email, click the link, set a password, and land in the community.
4. They're automatically added to the right group, which controls what categories they see.

### Discourse Connect (SSO)

If h2\ has a central identity system, Discourse Connect lets you delegate all authentication to an external provider:

- Enable via `enable_discourse_connect` setting.
- Set a `discourse_connect_url` (your auth endpoint) and `discourse_connect_secret`.
- All login/registration goes through your system; Discourse auto-provisions user accounts.
- Supports syncing user attributes (name, email, avatar, groups, custom fields).

**Use case**: if CLEAgora evolves to manage respondents across multiple studies with a central panel, SSO avoids duplicate accounts and gives you centralized identity control.

### Custom User Fields

You can add custom fields to user profiles (Admin → Customize → User Fields):
- Demographics (age range, location, profession).
- Study metadata (cohort, recruitment source, consent status).
- Fields can be required at signup, editable by user or admin-only.
- Accessible via API: `GET /users/{username}.json` returns custom field values.

---

## 4. Community Architecture: Categories, Groups, Permissions

### Categories & Subcategories

Categories are the primary organizational unit. For a qualitative study, a typical structure:

```
CLEAgora Instance
├── Welcome & Instructions       (pinned, read-only for respondents)
├── Phase 1 — Exploration
│   ├── Topic: "Your first impressions of [stimulus]"
│   ├── Topic: "Tell us about your habits with [product]"
│   └── Topic: "React to this image/video"
├── Phase 2 — Deep Dive
│   ├── Topic: "What matters most when choosing [product]?"
│   └── Topic: "Debate: [proposition A] vs [proposition B]"
├── Phase 3 — Co-construction
│   ├── Topic: "Design your ideal [product/service]"
│   └── Topic: "What would you change about [brand]?"
├── Free Discussion              (open-ended, respondent-initiated topics)
└── Staff / Researchers Only     (invisible to respondents)
```

- Subcategories are supported (one level deep).
- **Tags** complement categories for cross-cutting themes (e.g., `emotion`, `price`, `brand-perception`).
- **Topic templates**: each category can have a template that pre-fills the composer when a respondent creates a new topic. Useful for structured responses ("Describe your experience in 3 steps: 1. What happened, 2. How you felt, 3. What you'd change").

### Groups

Groups are the access control mechanism:
- Create study-specific groups (e.g., `study-wave-1`, `study-wave-2`, `moderators`).
- Groups can be auto-assigned during CSV bulk invite.
- Managed via API: `PUT /groups/{id}/members.json` to add/remove members.
- Groups also enable group @mentions and group messaging.

### Category Permissions

Each category has a permission matrix: which groups can **See**, **Reply**, **Create Topics**.

Example for a study category:
| Group | See | Reply | Create |
|-------|-----|-------|--------|
| study-wave-1 | ✓ | ✓ | ✓ |
| moderators | ✓ | ✓ | ✓ |
| everyone | ✗ | ✗ | ✗ |

This enables **multi-study isolation** on one instance: each study gets its own categories + group, and respondents from one study never see another study's content.

---

## 5. UI/UX Customization & Branding

### Theme System

Discourse theming works in two layers:

- **Full themes**: control the overall look (colors, fonts, layout). Only one active theme at a time.
- **Theme components**: modular add-ons that customize one aspect (e.g., a custom header, a sidebar tweak). Multiple components can be active simultaneously under any theme.

Both support CSS, HTML (Handlebars templates), JavaScript, and configurable settings. Themes can be managed via the admin UI or synced from a GitHub repo.

### What You Can Customize

**Colors & typography**: Full color scheme control (primary, secondary, accent, background). Custom web fonts. All via Admin → Appearance → Themes.

**Header & branding**: The "Brand Header" theme component adds a custom top bar with logo, navigation links, and social icons. Custom logos for desktop, mobile, and favicon via Admin → Settings → Branding.

**Homepage layout**: The "Homepage Blocks" component lets you arrange the landing page (featured topics, category highlights, custom HTML blocks). Useful for showing the current study phase or welcome message.

**Sidebar**: Customizable sidebar with category navigation. "Group Navigation Sidebar" component shows different menu sections to different user groups — useful for showing study-specific navigation.

**Hiding forum-like elements**: For a cleaner research-oriented interface, you can disable or hide via CSS/settings:
- Gamification badges and trust level indicators.
- Like counts (or replace with Reactions plugin for richer feedback).
- User titles and flair.
- "Suggested topics" at the bottom of threads.

### Email Branding

All Discourse emails (invitations, notifications, digests) are customizable:
- **Outer template**: Admin → Customize → Email Style (HTML wrapper + CSS).
- **Individual templates**: Admin → Customize → Email Templates (invitation text, welcome message, notification format).
- Custom `from` address and reply-to address.

### Mobile Experience

Discourse is mobile-first and works as a **PWA** (Progressive Web App):
- Respondents can "install" it on their phone's home screen — it looks and feels like a native app.
- Fully responsive design, touch-optimized.
- No separate mobile app needed for the prototype.

### Branding Strategy for CLEAgora

For a study, the goal is to make Discourse look like a **dedicated research space**, not a generic forum:
1. Custom theme with neutral/study-branded colors and clean typography.
2. Brand header with h2\ or study-specific logo.
3. Simplified UI: hide gamification, minimize forum jargon ("topic" → "discussion", etc.).
4. Custom welcome email and onboarding flow.
5. Pinned "Welcome & Instructions" topic with study context.

---

## 6. Content Types & Respondent Experience

### What Respondents Can Post

- **Text** (Markdown): the primary format. Rich formatting, quotes, @mentions.
- **Images**: upload directly or paste. Drag-and-drop supported.
- **Videos**: upload with server-side transcoding and thumbnail generation. Also embed from YouTube/Vimeo.
- **Files**: PDF, audio, documents — configurable upload types and size limits.
- **Polls**: built-in poll plugin. Inline polls in any post (single choice, multiple choice, number rating). Results visible to all or only after voting.
- **Reactions**: beyond "Like" — the Reactions plugin allows configurable emoji reactions (e.g., 👍 ❤️ 😮 🤔). Good for lightweight respondent feedback.

### Engagement & Notifications

Discourse has a sophisticated notification system:
- **In-app**: real-time notifications for replies, @mentions, likes.
- **Email**: configurable per-user or admin-set defaults:
  - Immediate email on reply to your post.
  - Daily/weekly email digest of activity.
  - "Mailing list mode" — every new post sent as email (for respondents who prefer email to forum).
- **@mentions**: mention a user or group to notify them.
- **Watching/Tracking**: users can watch a topic (notified of every reply) or track it (notified only of @mentions).

**Admin defaults for respondents**: you can set sensible defaults like "email on reply" + "weekly digest" so respondents stay engaged even if they don't check the forum daily.

### Onboarding

- **Discobot**: built-in interactive tutorial bot that teaches new users how to post, reply, format text, etc. via a private message conversation. Text is fully customizable (Admin → Customize → Text, search "narrative_bot").
- **Pinned topics**: a "Welcome" topic pinned in each category that explains the study and what's expected.
- **Custom Wizard plugin**: multi-step onboarding forms that collect structured data (demographics, consent) and can auto-create a personalized welcome topic or assign the user to groups.

### Trust Levels

Discourse has 5 trust levels (TL0 to TL4) that gate capabilities:
- **TL0 (New)**: can reply but limited in links, images, mentions.
- **TL1 (Basic)**: earned after minimal reading/participation. Unlocks full posting.
- **TL2–4**: progressively more capabilities (editing others' posts, moderation powers).

For CLEAgora, you'd want to **auto-promote all respondents to TL1** immediately (setting: `default_trust_level: 1`) so they can post freely from day one. Higher trust levels can be reserved for moderators.

---

## 7. Animation & Moderation: Bots, AI, Automation

This is one of the key open questions for CLEAgora. Discourse offers several building blocks:

### Option A: API Bot (Custom)

Build a Python bot that uses the Discourse API to:
- **Create topics** on a schedule (research stimuli, discussion prompts).
- **Post replies** in threads (follow-up questions, probes, summaries).
- **React to posts** (acknowledge contributions).
- **Send private messages** (individual prompts, reminders).

**How it works**: create a dedicated bot user in Discourse, generate an API key for it, and have your external service post via `POST /posts` with `api_key` and `api_username` headers.

**Pros**: full control, can integrate with your LLM pipeline (e.g., Claude for generating probes), no dependency on Discourse plugins.
**Cons**: you build and maintain it; no native UI in Discourse admin.

### Option B: Discourse AI Plugin

The official Discourse AI plugin is powerful and actively developed:
- **AI Bot**: a conversational bot available in topics and private messages. Can be configured with custom system prompts (personas), custom tools (JavaScript), and even MCP server integration.
- **Custom LLM backend**: supports OpenAI, Anthropic (Claude), Cohere, or your own endpoint. You can point it at h2\'s infrastructure.
- **Topic summarization**: auto-generate summaries of long discussions.
- **AI Triage**: automated content moderation (flag off-topic or low-quality posts).

**Pros**: deep integration with Discourse UI, admin-configurable, supports custom tools and personas.
**Cons**: Ruby/Ember ecosystem (less familiar than Python for h2\), still evolving, some features experimental.

### Option C: Discourse Automation Plugin

The built-in automation plugin handles rule-based workflows:
- **Recurring triggers**: post a new stimulus every Monday at 9am.
- **Event triggers**: when a user is added to a group, send a welcome message; when a post is created, auto-tag it.
- **Actions**: create posts, send PMs, add/remove from groups, close topics.

**Pros**: no code, admin UI configuration, bundled with Discourse.
**Cons**: rule-based only (no AI), limited to predefined trigger/action combinations.

### Recommended Approach for CLEAgora

**Hybrid**: use Discourse Automation for scheduling and rule-based workflows + a custom API bot (Python) for AI-powered animation (stimulus generation, intelligent probes, discussion facilitation). This keeps the AI logic in Python (familiar stack, close to the enrichment pipeline) while leveraging Discourse's native automation for routine tasks.

### Moderation Tools

- **Flagging**: users and staff can flag posts. Configurable auto-hide after N flags.
- **Review queue**: staff review flagged content in a dedicated queue.
- **Slow mode**: limit posting frequency in a topic (e.g., one post per 15 minutes — useful for structured discussion phases).
- **Topic timers**: auto-close or auto-open topics on a schedule (control discussion phases).
- **AI Triage** (Discourse AI): auto-flag posts based on content analysis.

---

## 8. Downstream Integration: API & Data Extraction

This is critical for CLEAgora's enrichment pipeline.

### REST API Overview

- **Documentation**: [docs.discourse.org](https://docs.discourse.org/) — auto-generated, comprehensive.
- **Principle**: Discourse consumes its own API, so anything the web UI does, the API can do.
- **Authentication**: Admin API key (header: `Api-Key` + `Api-Username`) for full access. Created in Admin → Settings → API.
- **Format**: JSON responses throughout.
- **Rate limits**: ~12 requests/second per IP (configurable). Manageable with simple throttling.

### Key Extraction Endpoints

| What | Endpoint | Notes |
|------|----------|-------|
| All categories | `GET /categories.json` | Includes subcategories, topic counts |
| Topics in a category | `GET /c/{slug}/{id}.json` | Paginated, includes topic metadata |
| Single topic + posts | `GET /t/{id}.json` | Returns first 20 posts; use `?page=N` for more |
| Raw post content | `GET /t/{id}.json?include_raw=true` | Adds Markdown source alongside HTML |
| Single post raw | `GET /raw/{post_id}` | Just the Markdown |
| User profile | `GET /users/{username}.json` | Includes custom fields, groups |
| Search | `GET /search/query.json?term=...` | Full-text, max 50 results per query |
| Latest topics | `GET /latest.json` | Paginated, site-wide |

### Post Content Formats

Discourse stores posts in two formats:

- **Raw** (Markdown): the original text as typed by the user. Best for NLP/analysis.
- **Cooked** (HTML): the rendered HTML after Discourse processing (links, embeds, formatting). Best for display.

**For the enrichment pipeline**: extract both. Use raw for text analysis and metadata generation; use cooked for preserving rich content (embedded images, polls, quotes).

### Conversation Structure

Each post has:
- `post_number`: sequential position in the topic.
- `reply_to_post_number`: which post this is a reply to (null if it's a top-level reply to the topic).
- `username`, `created_at`, `updated_at`.
- `like_count`, `reads`.
- `quote_count`: how many times this post was quoted by others.

This gives you a **reply graph** — who responded to whom — which is essential for analyzing collective dynamics (agreement/disagreement chains, topic evolution, key contributors).

### Webhooks (Real-Time)

For event-driven pipeline triggers instead of batch polling:

- **Configuration**: Admin → Settings → Webhooks. Specify a payload URL and select events.
- **Available events**: `post_created`, `post_edited`, `topic_created`, `topic_revised`, `user_created`, `user_activated`, etc.
- **Payload**: JSON with full object data (post content, user info, topic metadata).
- **Use case**: trigger enrichment immediately when a new post is created, rather than waiting for a batch extraction.

### Data Explorer Plugin

The Data Explorer plugin (bundled with Discourse) lets you run **SQL queries directly against the Discourse database** from the admin UI:
- Write custom queries (e.g., "all posts in category X with user custom fields").
- Export results as CSV.
- Schedule recurring queries.
- **API access**: queries can be triggered via API too.

**This is extremely powerful for CLEAgora**: you can write extraction queries that join posts, users, custom fields, likes, and categories in a single SQL query — much more efficient than chaining REST API calls.

### Bulk Extraction Strategy

For a complete study extraction:

1. **Option A — API-based** (recommended for prototype):
   - Fetch category → iterate topics → fetch posts per topic (with `include_raw=true`).
   - Throttle at ~10 req/sec. A study with 50 topics × 20 posts = ~100 API calls ≈ 10 seconds.
   - Enrich each post with user data (cached to avoid redundant calls).

2. **Option B — Data Explorer SQL** (recommended for production):
   - Write a SQL query that extracts everything in one shot.
   - Trigger via API, get CSV/JSON result.
   - More efficient for large studies.

3. **Option C — Webhooks + incremental** (recommended for live monitoring):
   - Webhook on `post_created` triggers enrichment in near-real-time.
   - Maintain a local store of extracted/enriched posts.
   - Complement with periodic full extraction for consistency.

### Extraction Output Model (Proposed)

For the enrichment pipeline, each extracted post should produce a structure like:

```json
{
  "post_id": 1234,
  "topic_id": 56,
  "topic_title": "Your first impressions of [stimulus]",
  "category": "Phase 1 — Exploration",
  "tags": ["first-impression", "stimulus-A"],
  "author": {
    "username": "respondent_42",
    "custom_fields": { "age_range": "25-34", "cohort": "wave-1" }
  },
  "content_raw": "I was really surprised by...",
  "content_html": "<p>I was really surprised by...</p>",
  "reply_to_post_id": 1230,
  "created_at": "2026-04-10T14:23:00Z",
  "likes": 3,
  "quotes_received": 1,
  "interaction_context": {
    "thread_depth": 2,
    "parent_author": "respondent_17",
    "topic_position": 5
  }
}
```

This structure is ready for CLEA-style enrichment: entity extraction, sentiment, thematic tagging, interaction pattern analysis.

---

## 9. Plugin Ecosystem & Extensibility

### Plugins vs. Theme Components

| | Theme Component | Plugin |
|---|---|---|
| **Scope** | Frontend only (CSS, JS, HTML templates) | Full stack (Ruby backend + Ember frontend) |
| **Install** | Admin UI, no restart needed | Requires server rebuild (`./launcher rebuild app`) |
| **Use for** | Visual changes, UI tweaks, lightweight JS | Database changes, API routes, background jobs, deep integration |
| **Maintenance** | Low | Medium-high (must track Discourse updates) |

### Plugins Relevant to CLEAgora

**Bundled with Discourse (no install needed):**

| Plugin | Use for CLEAgora |
|--------|-----------------|
| **Polls** | Inline polls in stimulus topics (quick reactions, ratings) |
| **Reactions** | Emoji reactions beyond "Like" (e.g., 🤔 😮 👎) for lightweight feedback |
| **Data Explorer** | SQL queries for data extraction and analysis |
| **Automation** | Scheduled posts, event-triggered actions, group management |
| **Discourse AI** | AI bot, topic summarization, AI triage moderation |
| **Calendar** | Schedule discussion phases, study events |
| **Solved** | Mark key insights or consensus points in discussions |
| **Assign** | Assign topics to researchers for analysis |
| **Post Voting / Topic Voting** | Let respondents vote on ideas, proposals, or insights |

**Community plugins (require install):**

| Plugin | Use for CLEAgora |
|--------|-----------------|
| **Custom Wizard** ([GitHub](https://github.com/paviliondev/discourse-custom-wizard)) | Multi-step onboarding forms, structured data collection |
| **Discourse Chatbot** ([GitHub](https://github.com/merefield/discourse-chatbot)) | AI-powered conversational bot with RAG (searches forum content) |

### Plugin Development

If needed, custom Discourse plugins are written in Ruby (server) + Ember.js (client). The plugin API provides:
- Model extensions (add fields to posts, topics, users).
- New API routes.
- Background jobs (scheduled or event-triggered).
- **Plugin outlets**: ~hundreds of injection points in the Discourse UI where you can insert custom components.

**For CLEAgora**: a custom plugin is likely needed eventually for deep pipeline integration (e.g., a "research dashboard" in the admin UI, or server-side hooks that trigger enrichment). But for the prototype, the API + external Python service approach is faster and more maintainable.

---

## 10. Infrastructure & Deployment

### Docker (Development & Prototype)

Discourse's official deployment is Docker-based:

```bash
# Clone the official Docker manager
git clone https://github.com/discourse/discourse_docker.git
cd discourse_docker

# Copy and edit the configuration
cp samples/standalone.yml containers/app.yml
# Edit app.yml: set domain, email, SMTP, etc.

# Build and launch
./launcher bootstrap app
./launcher start app
```

**For local development**: Discourse also supports a dev environment via `d/boot_dev` script or a `discourse/discourse_dev` Docker image. This is faster for iteration but not production-ready.

### Production Deployment

- **Minimum requirements**: 2GB RAM, 1 CPU core, 10GB disk (for a small community).
- **Recommended for CLEAgora prototype**: 4GB RAM VPS on Hetzner (~€7/month).
- **Production (AWS)**: EC2 instance or ECS container, with RDS for PostgreSQL and S3 for uploads.
- **SSL**: built-in Let's Encrypt support in the Docker setup.
- **Email**: requires SMTP configuration (e.g., Amazon SES, Mailgun, or h2\'s mail server) for invitations and notifications.

### Backup & Data

- Built-in backup system (Admin → Backups): full database + uploads.
- Configurable automatic backups (daily, weekly).
- Backups can be uploaded to S3.
- Easy restore for migration between instances.

---

## 11. Key Risks & Limitations

**For CLEAgora decision-making:**

| Risk | Impact | Mitigation |
|------|--------|-----------|
| **Forum UX ≠ research UX** | Respondents might find the forum interface unfamiliar or intimidating | Custom theme to simplify UI; good onboarding (Discobot + welcome topic); consider respondent demographics |
| **Engagement decay** | Forum participation drops after initial enthusiasm | Notification strategy; scheduled stimuli; moderator/bot probes; short study cycles |
| **Discourse updates breaking plugins** | Community plugins (Custom Wizard, Chatbot) may lag behind Discourse releases | Pin Discourse version during a study; prefer bundled plugins; test updates in staging |
| **Rate limits on API extraction** | 12 req/sec may slow large extractions | Use Data Explorer SQL for bulk; webhooks for real-time; cache aggressively |
| **Topic threading is flat** | Discourse threading is shallow (reply-to, not nested). Complex debate structures may be hard to follow | Use quotes liberally; consider the Solved plugin for synthesis; accept that this is a forum, not a threaded chat |
| **Ruby/Ember stack** | h2\ team is more familiar with Python. Plugin development requires Ruby/Ember knowledge | Prefer API + external Python services over custom plugins; use theme components (JS) for UI tweaks |
| **Sovereignty** | Self-hosted Discourse is sovereign, but plugins may phone home or depend on external services | Audit plugin dependencies; host Discourse AI models on h2\ infrastructure |

---

## 12. Sources

### Official Documentation
- [Discourse API Documentation](https://docs.discourse.org/)
- [Discourse Meta (community & support)](https://meta.discourse.org/)
- [Discourse Developer Documentation](https://github.com/discourse/discourse-developer-docs)

### Key Meta Topics
- [Configuring Discourse for a closed or private community](https://meta.discourse.org/t/configuring-discourse-for-a-closed-or-private-community/27014)
- [Understanding groups and category permissions](https://meta.discourse.org/t/understanding-groups-and-category-permissions/87678)
- [Creating and using invites](https://meta.discourse.org/t/creating-and-using-invites/263314)
- [Beginner's guide to Discourse themes](https://meta.discourse.org/t/beginners-guide-to-using-discourse-themes/91966)
- [Discourse AI plugin](https://meta.discourse.org/t/discourse-ai/259214)
- [Discourse Automation plugin](https://meta.discourse.org/t/discourse-automation/195773)
- [Setup DiscourseConnect (SSO)](https://meta.discourse.org/t/setup-discourseconnect-official-single-sign-on-for-discourse-sso/13045)
- [Customizing Discobot](https://meta.discourse.org/t/customizing-discobot-for-your-site/103633)
- [Configure webhooks](https://meta.discourse.org/t/configure-webhooks-that-trigger-on-discourse-events-to-integrate-with-external-services/49045)
- [Data Explorer plugin](https://meta.discourse.org/t/discourse-data-explorer/32566)
- [Fetch all posts from a topic](https://meta.discourse.org/t/fetch-all-posts-from-a-topic-using-the-api/260886)
- [Creating form templates](https://meta.discourse.org/t/creating-form-templates/397564)
- [Custom Wizard plugin](https://meta.discourse.org/t/custom-wizard-plugin/73345)
- [Discourse Reactions plugin](https://meta.discourse.org/t/discourse-reactions/183261)
- [Brand Header theme component](https://meta.discourse.org/t/brand-header/77977)

### GitHub Repositories
- [discourse/discourse](https://github.com/discourse/discourse) — Core platform + bundled plugins
- [discourse/discourse_docker](https://github.com/discourse/discourse_docker) — Official Docker deployment
- [discourse/discourse-ai](https://github.com/discourse/discourse-ai) — AI plugin
- [paviliondev/discourse-custom-wizard](https://github.com/paviliondev/discourse-custom-wizard) — Custom Wizard
- [merefield/discourse-chatbot](https://github.com/merefield/discourse-chatbot) — Community chatbot with RAG
- [lvoytek/discourse-data-exporter](https://github.com/lvoytek/discourse-data-exporter) — Bulk data export tool
