# CLEAgora — Design Document

> Practical design and implementation strategy for a community-based qualitative research platform on Discourse.
> Illustrated with a fictional study: **"La Matinale de France Inter — Usages, perceptions et attentes des auditeurs"**.

---

## Table of Contents

0. [Design Philosophy: Flash Deployment](#0-design-philosophy-flash-deployment)
1. [Study Design](#1-study-design)
2. [Community Architecture on Discourse](#2-community-architecture-on-discourse)
3. [Respondent Journey](#3-respondent-journey)
4. [Animation Model](#4-animation-model)
5. [Technical Architecture](#5-technical-architecture)
6. [Extraction & Enrichment Pipeline](#6-extraction--enrichment-pipeline)
7. [Restructured Output: Write-ups & Flat Views](#7-restructured-output-write-ups--flat-views)
8. [Multimodality Roadmap](#8-multimodality-roadmap)
9. [Implementation Strategy](#9-implementation-strategy)

---

## 0. Design Philosophy: Flash Deployment

### The Core Idea

CLEAgora's defining characteristic is **flash deployment**: the ability to go from a study brief to a fully configured, operational research community **in 72 hours**. This is not just a nice-to-have — it's the product thesis. Speed and agility are the core differentiators.

The 72h window covers the entire chain: brief intake → community configuration → field open → data collection → extraction → enrichment → restructured write-ups. Not a week of setup followed by fieldwork — the setup IS almost instant, and the 72h is mostly field time.

The sequence:

```
Study Brief (free text)
    → LLM parsing + structured extraction
        → Study Configuration (YAML)
            → Discourse setup (categories, groups, permissions, topics)
            → Animation guide (schedule, probes, stimuli)
            → Extraction pipeline config (what to capture, how to enrich)
            → Restructuration templates (output structure aligned with brief)
```

**Input**: a researcher writes a brief in natural language — objectives, target audience, themes to explore, duration, stimuli ideas. Essentially the same brief they'd write for a traditional study. Optionally supplemented by a structured form or conversation to fill gaps.

**Output**: a ready-to-launch community with everything configured — Discourse structure, bot schedule, extraction pipeline, and output templates — all aligned with the study's research questions.

### Why This Matters

In traditional online qualitative communities, setup takes days to weeks: platform configuration, discussion guide drafting, moderator briefing, analysis framework design. Each step involves manual translation from the study's intent to operational artifacts.

CLEAgora compresses this. The brief IS the configuration source. The LLM interprets the research intent and generates all downstream artifacts. The researcher reviews and adjusts, but doesn't build from scratch.

### The Brief → Config Chain

```
┌──────────────────────────────────────────────────────────┐
│                    STUDY BRIEF                           │
│  (free text: objectives, audience, themes, duration...)  │
└──────────────────────┬───────────────────────────────────┘
                       │
                       ▼  LLM parsing
┌──────────────────────────────────────────────────────────┐
│              STRUCTURED STUDY CONFIG                     │
│                                                          │
│  study:                                                  │
│    objectives: [...]       ← extracted from brief        │
│    audience: [...]         ← extracted from brief        │
│    duration: 3 weeks       ← extracted from brief        │
│    phases: [...]           ← generated from objectives   │
│                                                          │
│  discourse:                                              │
│    categories: [...]       ← generated from phases       │
│    topics: [...]           ← generated from themes       │
│    topic_templates: [...]  ← generated from objectives   │
│                                                          │
│  animation:                                              │
│    schedule: [...]         ← generated from phases       │
│    probe_templates: [...]  ← generated from objectives   │
│    engagement_rules: [...] ← default + brief hints       │
│                                                          │
│  restructuration:                                        │
│    axes: [...]             ← derived from objectives     │
│    write_up_templates: []  ← generated from brief        │
│    verbatim_tagging: [...] ← aligned with themes         │
└──────────────────────────────────────────────────────────┘
                       │
                       ▼  Apply
         ┌─────────────┼─────────────┐
         ▼             ▼             ▼
    Discourse     Bot Service    Pipeline
    (configured)  (scheduled)    (ready)
```

### The Verbatim as Minimal Unit

Following CLEA methodology, the **verbatim** is the atomic unit of analysis. In CLEAgora's community context, a verbatim is:

- A **meaningful segment** within a post (a post may contain multiple verbatims).
- Extracted from its conversational context but **linked back** to: the post, the topic, the thread, the author, the study phase.
- **Enriched** with metadata: descriptive (entities, sentiment, emotions), interactional (who they were responding to, agreement/disagreement), and analytical (aligned with study questions).
- **Recomposable**: verbatims can be reassembled into write-ups by respondent, by theme, by profile, by question — any axis the study requires.

The extraction pipeline segments posts into verbatims. The restructuration layer recomposes them.

### Brief Input: Practical Approach

For the prototype:
1. **Primary input**: free text brief (the researcher writes naturally).
2. **LLM parsing**: extracts objectives, audience, themes, duration, study design.
3. **Gap detection**: the LLM identifies what's missing or ambiguous.
4. **Structured supplement**: a short follow-up form or conversation to fill the gaps.
5. **Config generation**: the complete YAML config is generated.
6. **Researcher review**: the researcher validates the generated structure, adjusts topics/probes, confirms.

This mirrors the CLEA pattern: structured → unstructured → restructured, applied to study design itself.

---

## 1. Study Design

### 1.1 The Fictional Study

**Title**: La Matinale de France Inter — Usages, perceptions et attentes des auditeurs

**Client** (fictional): Radio France — Direction des études et de la stratégie

**Objectives**:
- Understand the listening habits and rituals around the morning show (when, where, how, with whom).
- Explore the emotional and intellectual relationship listeners have with the show (attachment, irritation, expectations).
- Capture reactions to specific editorial choices (chroniqueurs, rubriques, ton, sujets).
- Co-construct ideas for evolution of the format with engaged listeners.

**Panel**: 40 recruited listeners of France Inter's morning show.
- Mix of loyal daily listeners and occasional listeners.
- Age range 25–65, gender balanced, geographic spread (urban/periurban/rural).
- Recruited via an external panel provider; screened for France Inter listening habits.

**Duration**: 3 weeks (active community).

**Study phases**:
- **Week 1 — Exploration**: listening habits, relationship to the show, spontaneous perceptions.
- **Week 2 — Deep Dive**: reactions to specific stimuli (clips, chroniques, sujets), debates on editorial choices.
- **Week 3 — Co-construction**: ideas for the future, ideal matinale, priorities and trade-offs.

### 1.2 What This Illustrates

This fictional study demonstrates CLEAgora's design patterns. Every element below is **generalizable** — the category structure, animation model, and pipeline work for any community-based qualitative study. The France Inter case just makes it concrete.

---

## 2. Community Architecture on Discourse

### 2.1 Instance Configuration

| Setting | Value | Why |
|---------|-------|-----|
| `login_required` | `true` | No anonymous access — all content is private |
| `invite_only` | `true` | Only recruited respondents can join |
| `default_trust_level` | `1` (Basic) | Respondents can post freely from day one |
| `allow_new_registrations` | `false` | Redundant safety net — invites only |
| `title` | "La Matinale — Espace Auditeurs" | Clean, study-branded name |
| `site_description` | "Bienvenue dans votre espace d'échange sur la matinale de France Inter" | Welcoming, not "forum" jargon |
| `default_locale` | `fr` | French UI |

### 2.2 Category Structure

```
La Matinale — Espace Auditeurs
│
├── 📌 Bienvenue                          [read-only for respondents]
│   └── Topic: "Comment ça marche" (pinned, explains the rules and what's expected)
│
├── 🎙️ Semaine 1 — Votre matinale
│   ├── Topic: "Racontez-nous votre rituel du matin avec la radio"
│   ├── Topic: "Ce qui vous fait rester / ce qui vous fait décrocher"
│   └── Topic: "Si vous deviez décrire France Inter le matin en 3 mots..."
│
├── 🔍 Semaine 2 — Réactions & débats
│   ├── Topic: "Écoutez cet extrait et réagissez" (with audio/video stimulus)
│   ├── Topic: "Les chroniques : lesquelles vous parlent, lesquelles vous agacent ?"
│   ├── Topic: "Le traitement de l'actu : trop / pas assez / juste ce qu'il faut ?"
│   └── Topic: "Débat : humour le matin, pour ou contre ?"
│
├── 💡 Semaine 3 — Et si on imaginait...
│   ├── Topic: "Votre matinale idéale : décrivez-la"
│   ├── Topic: "Si vous étiez directeur des programmes, que changez-vous ?"
│   └── Topic: "Ce qu'il ne faut surtout pas changer"
│
├── ☕ Le café                             [open: respondents can create topics]
│   └── (Free discussion space — off-topic welcome, community bonding)
│
└── 🔒 Coulisses (Staff Only)             [invisible to respondents]
    ├── Topic: "Guide d'animation — semaine par semaine"
    ├── Topic: "Signaux intéressants à creuser"
    └── Topic: "Notes d'analyse en cours"
```

### 2.3 Groups & Permissions

| Group | Members | Permissions |
|-------|---------|-------------|
| `auditeurs` | All 40 respondents | See + Reply + Create in study categories; See + Reply + Create in "Le café" |
| `animateurs` | Moderator(s) + bot user | Full access everywhere |
| `chercheurs` | Research team (observation only) | See all categories including "Coulisses"; Reply in "Coulisses" only |
| `everyone` | (default) | No access to anything (overridden by `login_required`) |

**Category permission matrix**:

| Category | `auditeurs` | `animateurs` | `chercheurs` |
|----------|-------------|--------------|---------------|
| Bienvenue | See | See + Reply + Create | See |
| Semaine 1–3 | See + Reply | See + Reply + Create | See |
| Le café | See + Reply + Create | See + Reply + Create | See |
| Coulisses | — | See + Reply + Create | See + Reply + Create |

**Key design choice**: respondents can only **reply** in study categories (not create new topics) — this keeps the discussion structured around the research questions. They can freely create topics in "Le café" for social interaction.

### 2.4 Tags

Cross-cutting tags for the research team to use (not visible to respondents in topic lists, but applied by moderators/bot):

- `ritual`, `habit`, `emotion`, `irritant`, `attachment`
- `chronique`, `humour`, `actu`, `music`, `tone`
- `idea`, `wish`, `red-line`
- `strong-signal`, `weak-signal`, `unexpected`

Tags are used by the extraction pipeline for pre-structuring the analysis.

---

## 3. Respondent Journey

### 3.1 Phase 0 — Invitation & Onboarding (Day -3 to Day 0)

```
Recruitment panel
    → CSV with emails + demographics
        → Bulk invite via Discourse API (auto-assign to `auditeurs` group)
            → Respondent receives branded email invitation
                → Clicks link → sets password → lands on "Bienvenue"
                    → Discobot tutorial (customized: "Bienvenue [prénom] !
                       Je suis votre guide...")
                        → First pinned topic: "Comment ça marche"
                            → Ready to participate
```

**Email invitation** (customized template):
> Bonjour [Prénom],
>
> Vous avez été sélectionné(e) pour participer à un échange entre auditeurs de la matinale de France Inter. Pendant 3 semaines, vous retrouverez d'autres auditeurs dans un espace dédié pour partager vos impressions, débattre et imaginer ensemble.
>
> → [Rejoindre l'espace auditeurs]
>
> À très vite !

**Discobot customization**: replace generic tutorial with study-specific welcome:
- "Voici comment répondre à une discussion" (reply demo).
- "Voici comment réagir à un message" (like/reaction demo).
- "Voici comment partager une image ou un lien" (media demo).
- Skip advanced features (bookmarks, search, etc.).

**Custom user fields** (populated from recruitment CSV or filled at signup):
- `age_range`: 25-34 / 35-44 / 45-54 / 55-65
- `listening_frequency`: daily / several_times_week / occasional
- `listening_context`: home / car / commute / office
- `city_size`: urban / periurban / rural

### 3.2 Phase 1 — Active Participation (Weeks 1-3)

**Week 1: Exploration** (categories unlocked progressively or all at once)
- 3 topics posted by the moderator/bot on Day 1.
- Respondents reply at their own pace.
- Bot/moderator posts follow-up probes in threads ("Intéressant, est-ce que d'autres partagent cette impression ?", "Vous dites que vous décrochez à 8h — qu'est-ce qui se passe à ce moment-là ?").
- Goal: 5-10 contributions per respondent over the week.

**Week 2: Deep Dive** (new category unlocked)
- Stimulus-based discussions (audio clips, screenshots of programming grids, quotes from chroniqueurs).
- More structured prompts, including polls ("Notez cette chronique de 1 à 5").
- Debates encouraged ("Qui est d'accord avec [respondent] ? Qui voit les choses différemment ?").
- Goal: deeper engagement, more inter-respondent interaction.

**Week 3: Co-construction** (new category unlocked)
- Creative prompts ("Décrivez votre matinale idéale", "Si vous étiez directeur des programmes...").
- Building on insights from weeks 1-2.
- Synthesis topic: moderator posts a summary of emerging themes and asks respondents to react.
- Goal: forward-looking, constructive, collaborative.

### 3.3 Phase 2 — Closing (Day 22-23)

- Thank-you topic posted by moderator.
- Summary of key themes shared with respondents (optional — depends on client preference).
- Community remains accessible in read-only mode for a period.
- Respondents receive incentive/compensation via the recruitment panel.

### 3.4 Engagement Mechanics

| Mechanism | How | Purpose |
|-----------|-----|---------|
| **Email notifications** | "Someone replied to your post" (immediate) + weekly digest | Bring respondents back |
| **@mentions** | Moderator @mentions specific respondents to draw them into discussions | Targeted re-engagement |
| **Reactions** | Emoji reactions (👍 🤔 😮 ❤️) on posts | Low-effort feedback, shows engagement |
| **Polls** | Inline polls in stimulus topics | Quick structured input, breaks up text-heavy discussions |
| **Progressive unlocking** | New categories become visible each week | Sense of progression, anticipation |
| **Le café** | Unstructured social space | Community bonding, retention |
| **Slow mode** | Optional: 1 post per 15 min in debate topics | Prevents flooding, encourages thoughtful responses |

---

## 4. Animation Model

### 4.1 Recommended Approach: Human Moderator + Bot Assistant

After analyzing the options (see `discourse-platform-guide.md`), the recommended model for the prototype is:

**Human moderator** (a researcher from h2\) handles:
- Creating and sequencing study topics (or validating bot-generated ones).
- Reading discussions, identifying interesting threads to deepen.
- Writing substantive follow-up probes ("Vous dites X — c'est intéressant car [respondent Y] disait plutôt Z. Qu'en pensez-vous ?").
- Deciding when to unlock new categories / phases.
- Tagging topics and posts with research-relevant tags.
- Flagging strong/weak signals in "Coulisses".

**Bot assistant** (API bot, Python) handles:
- Scheduled posting: stimulus topics at planned times (e.g., Monday 9am).
- Reminders: "@auditeurs Nouvelle discussion ouverte dans Semaine 2 !"
- Lightweight probes: auto-generated follow-ups for posts that haven't received replies ("Merci [prénom] ! Quelqu'un d'autre a vécu la même chose ?").
- Engagement nudges: PM to inactive respondents ("Ça fait quelques jours qu'on ne vous a pas vu(e) — vos impressions nous intéressent !").
- Data tasks: trigger extraction pipeline, generate participation stats for "Coulisses".

**Why not full bot animation**: the collective dynamic requires human judgment — knowing when to let a debate breathe vs. when to redirect, sensing the group's mood, making connections between respondents' contributions that require understanding of the study's intent. AI-generated probes are useful for maintenance, but the moderator drives the quality of the discussion.

**Why not full human**: too much manual work for routine tasks (scheduling, reminders, engagement tracking). The bot handles the operational overhead so the moderator can focus on intellectual work.

### 4.2 Bot Implementation

The bot is a **Python service** that interacts with Discourse via its REST API:

```
┌──────────────────────────────────────┐
│         CLEAgora Bot Service         │
│              (Python)                │
│                                      │
│  ┌──────────┐  ┌──────────────────┐  │
│  │ Scheduler │  │ Webhook Listener │  │
│  │ (cron)    │  │ (FastAPI)        │  │
│  └─────┬─────┘  └────────┬─────────┘  │
│        │                 │            │
│        ▼                 ▼            │
│  ┌────────────────────────────────┐   │
│  │      Action Engine             │   │
│  │  - post_topic()                │   │
│  │  - post_reply()                │   │
│  │  - send_pm()                   │   │
│  │  - mention_group()             │   │
│  │  - generate_probe() [LLM]     │   │
│  │  - check_engagement()          │   │
│  └─────────────┬──────────────────┘   │
│                │                      │
│                ▼                      │
│  ┌────────────────────────────────┐   │
│  │    Discourse API Client        │   │
│  │    (requests + rate limiter)   │   │
│  └────────────────────────────────┘   │
└──────────────────────────────────────┘
         │                    ▲
         ▼                    │
    Discourse Instance ───────┘
    (webhooks: post_created, user_activated)
```

**Key bot behaviors**:

| Trigger | Action | Example |
|---------|--------|---------|
| Cron (scheduled) | Post stimulus topic | Monday 9am: "Écoutez cet extrait et réagissez" with embedded audio |
| Cron (daily) | Check engagement stats | Identify respondents with 0 posts in last 48h |
| Low engagement detected | Send PM | "Bonjour [prénom], vos impressions nous intéressent..." |
| Webhook: `post_created` | Log for pipeline | Store post metadata for extraction |
| Webhook: `post_created` + no replies after 6h | Post follow-up probe | "Merci [prénom] ! D'autres auditeurs partagent-ils cette impression ?" |
| Webhook: `user_activated` | Welcome PM | Send onboarding message with first task |
| Moderator command (in Coulisses) | Execute action | "Bot: crée un poll dans Semaine 2 sur les chroniqueurs préférés" |

### 4.3 LLM-Powered Probes (Optional, Later)

For the prototype, probes can be template-based ("Merci [prénom] ! Quelqu'un d'autre...?"). Later, integrate an LLM (Claude API) to generate contextual follow-ups:

- Input: the post content + topic context + study objectives.
- Output: a natural, moderator-style follow-up question.
- Constraint: always reviewed by the human moderator before posting (queue in "Coulisses"), unless confidence is high and the study is in a low-risk phase.

---

## 5. Technical Architecture

### 5.1 System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLEAgora System                          │
│                                                                 │
│  ┌─────────────────────┐     ┌──────────────────────────────┐  │
│  │   Discourse          │     │   CLEAgora Services          │  │
│  │   (Docker)           │     │   (Python)                   │  │
│  │                      │     │                              │  │
│  │  - Forum UI          │◄───►│  - Bot Service (FastAPI)     │  │
│  │  - User management   │     │  - Extraction Pipeline       │  │
│  │  - Content storage   │     │  - Enrichment Engine         │  │
│  │  - Notifications     │     │  - Study Configuration       │  │
│  │  - Webhooks ─────────┼────►│                              │  │
│  │                      │     │                              │  │
│  │  Plugins:            │     │  Integrations:               │  │
│  │  - Data Explorer     │     │  - Discourse REST API        │  │
│  │  - Reactions         │     │  - LLM API (Claude)          │  │
│  │  - Polls             │     │  - SMTP (notifications)      │  │
│  │  - Automation        │     │                              │  │
│  └─────────────────────┘     └──────────────┬───────────────┘  │
│                                              │                  │
│                                              ▼                  │
│                               ┌──────────────────────┐         │
│                               │  Output Store         │         │
│                               │  (JSON / SQLite)      │         │
│                               │                       │         │
│                               │  - Structured posts   │         │
│                               │  - Enriched verbatims │         │
│                               │  - Interaction graphs  │         │
│                               │  - Study metadata     │         │
│                               └──────────────────────┘         │
│                                              │                  │
│                                              ▼                  │
│                               ┌──────────────────────┐         │
│                               │  Arcade / Analysis    │         │
│                               │  (future integration) │         │
│                               └──────────────────────┘         │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 Discourse Instance

**Deployment**: Docker (official `discourse_docker` setup).

**Required plugins** (bundled with Discourse, just need enabling):
- `poll` — inline polls in posts.
- `discourse-reactions` — emoji reactions beyond Like.
- `discourse-data-explorer` — SQL queries for data extraction.
- `discourse-automation` — rule-based automation (scheduled posts, auto-actions).

**Optional plugins** (install separately):
- `discourse-custom-wizard` — structured onboarding forms (if we want richer intake).
- `discourse-ai` — AI-powered features (consider for later phases; adds complexity).

**Theme**: custom theme with:
- Study branding (logo, colors, neutral/professional palette).
- Simplified UI (hide badges, trust level indicators, gamification elements).
- Custom header with study name.
- Clean category layout.

### 5.3 CLEAgora Services (Python)

A single Python project with modular components:

```
cleagora/
├── src/
│   ├── discourse_client/       # Discourse API wrapper
│   │   ├── client.py           # HTTP client with auth, rate limiting
│   │   ├── topics.py           # Topic/post CRUD
│   │   ├── users.py            # User/group management
│   │   └── webhooks.py         # Webhook payload parsing
│   │
│   ├── bot/                    # Animation bot
│   │   ├── scheduler.py        # Cron-based task scheduling
│   │   ├── actions.py          # Post, reply, PM, poll creation
│   │   ├── probes.py           # Follow-up question generation
│   │   └── engagement.py       # Activity tracking, nudge logic
│   │
│   ├── extraction/             # Data extraction from Discourse
│   │   ├── extractor.py        # Pull topics, posts, users, metadata
│   │   ├── models.py           # Data models (Post, Topic, Respondent, Thread)
│   │   └── export.py           # JSON/CSV output
│   │
│   ├── enrichment/             # Metadata generation (DECODia-style)
│   │   ├── pipeline.py         # Orchestration of enrichment steps
│   │   ├── entities.py         # Entity extraction (people, brands, concepts)
│   │   ├── sentiment.py        # Sentiment / emotion analysis
│   │   ├── thematic.py         # Thematic tagging aligned with study questions
│   │   └── interactions.py     # Interaction pattern analysis (reply graphs, agreement)
│   │
│   ├── config/                 # Study configuration
│   │   ├── study.py            # Study definition (phases, categories, schedule)
│   │   └── discourse.py        # Discourse connection settings
│   │
│   └── api/                    # FastAPI app (webhook receiver + admin endpoints)
│       ├── app.py
│       ├── webhooks.py         # Webhook handlers
│       └── admin.py            # Study management endpoints
│
├── studies/                    # Study-specific configurations
│   └── france-inter-matinale/
│       ├── study.yaml          # Study definition
│       ├── topics.yaml         # Topic templates with schedule
│       ├── probes.yaml         # Follow-up probe templates
│       └── stimuli/            # Media files for stimulus topics
│
├── tests/
├── docker-compose.yml          # Discourse + CLEAgora services
├── pyproject.toml
└── README.md
```

### 5.4 Study Configuration (YAML)

A study is defined declaratively:

```yaml
# studies/france-inter-matinale/study.yaml
study:
  name: "La Matinale de France Inter"
  slug: "france-inter-matinale"
  duration_weeks: 3
  discourse:
    instance_url: "https://matinale.cleagora.h2.fr"
    bot_username: "animateur"
    group: "auditeurs"

phases:
  - name: "Semaine 1 — Votre matinale"
    category_slug: "semaine-1-votre-matinale"
    starts_at: "2026-05-05"
    topics:
      - title: "Racontez-nous votre rituel du matin avec la radio"
        body_template: "topics/rituel-matin.md"
        post_at: "2026-05-05T09:00:00"
      - title: "Ce qui vous fait rester / ce qui vous fait décrocher"
        body_template: "topics/rester-decrocher.md"
        post_at: "2026-05-06T09:00:00"
      - title: "Si vous deviez décrire France Inter le matin en 3 mots..."
        body_template: "topics/trois-mots.md"
        post_at: "2026-05-07T09:00:00"

  - name: "Semaine 2 — Réactions & débats"
    category_slug: "semaine-2-reactions-debats"
    starts_at: "2026-05-12"
    topics:
      - title: "Écoutez cet extrait et réagissez"
        body_template: "topics/stimulus-extrait.md"
        stimuli: ["stimuli/extrait-chronique.mp3"]
        post_at: "2026-05-12T09:00:00"
      # ... etc.

engagement:
  inactive_threshold_hours: 48
  nudge_pm_template: "probes/nudge-inactive.md"
  auto_probe_delay_hours: 6
  auto_probe_templates:
    - "Merci {author} ! Quelqu'un d'autre a vécu la même chose ?"
    - "Intéressant, {author}. Qu'en pensent les autres ?"
    - "{author} soulève un point important. D'accord ? Pas d'accord ?"
```

---

## 6. Extraction & Enrichment Pipeline

### 6.1 Extraction

The extraction layer pulls data from Discourse and normalizes it into a structured format.

**Data model**:

```
Study
  └── Phase[]
       └── Topic[]
            ├── metadata (title, category, tags, created_at, stimulus_type)
            └── Post[]
                 ├── content_raw (Markdown)
                 ├── content_html (rendered HTML)
                 ├── author (username, custom_fields, group)
                 ├── reply_to (post_id → builds interaction graph)
                 ├── reactions[] (emoji, count)
                 ├── quotes[] (quoted post references)
                 ├── created_at
                 └── poll_responses[] (if poll topic)
```

**Extraction modes**:
1. **Batch**: full extraction of a study (all categories/topics/posts). Triggered manually or on study close.
2. **Incremental**: webhook-driven. Each new post is extracted and stored immediately.
3. **Snapshot**: periodic full extraction for consistency checks.

**Output format**: JSON Lines (one JSON object per post), plus a study-level metadata file. Optionally CSV for tabular analysis.

### 6.2 Enrichment

Following DECODia principles, each post is enriched with metadata:

**Layer 1 — Descriptive metadata** (automated):
- **Entities**: people mentioned (chroniqueurs, invités), brands, media, concepts.
- **Sentiment**: positive / negative / mixed / neutral, with intensity.
- **Emotions**: specific emotions detected (surprise, irritation, nostalgia, amusement, etc.).
- **Topics**: thematic tags aligned with the study grid (listening habits, editorial choices, format, etc.).
- **Language markers**: spontaneity level, register (formal/informal), use of humor/irony.

**Layer 2 — Interaction metadata** (computed):
- **Reply graph**: who replied to whom, thread depth.
- **Agreement/disagreement**: explicit markers ("je suis d'accord", "pas du tout", "justement...").
- **Co-construction**: posts that build on others (quotes, references, "+1" patterns).
- **Influence**: posts that generate the most replies/reactions/quotes.
- **Topic evolution**: how the discussion topic shifts within a thread.

**Layer 3 — Analytical metadata** (semi-automated, researcher-supervised):
- **Alignment with study questions**: which research objective does this verbatim address?
- **Signal strength**: strong signal (repeated, emotional, detailed) vs. weak signal (single mention, tentative).
- **Tension/convergence**: where do respondents agree vs. disagree?

**Implementation**: Layers 1-2 are automated (LLM-powered for descriptive, graph algorithms for interaction). Layer 3 is generated as suggestions for researcher review.

### 6.3 Enriched Output Model

```json
{
  "post_id": 1234,
  "study": "france-inter-matinale",
  "phase": "exploration",
  "topic": {
    "id": 56,
    "title": "Ce qui vous fait rester / ce qui vous fait décrocher",
    "category": "Semaine 1 — Votre matinale",
    "tags": ["attachment", "irritant"]
  },
  "author": {
    "username": "auditeur_17",
    "age_range": "35-44",
    "listening_frequency": "daily",
    "listening_context": "car",
    "city_size": "periurban"
  },
  "content": {
    "raw": "Honnêtement, ce qui me fait décrocher c'est quand ils passent 15 minutes sur un sujet politique qui tourne en rond. J'ai l'impression qu'ils oublient qu'on est dans la voiture, qu'on a besoin de variété. Par contre le jour où Charline a fait son billet sur les JO, j'ai failli rater ma sortie d'autoroute tellement je riais.",
    "html": "<p>Honnêtement, ce qui me fait décrocher c'est quand...</p>"
  },
  "interaction": {
    "reply_to_post_id": 1230,
    "reply_to_author": "auditeur_03",
    "thread_depth": 2,
    "topic_position": 5,
    "reactions_received": {"😂": 4, "👍": 2},
    "quotes_received": 1,
    "replies_received": 3
  },
  "enrichment": {
    "entities": ["Charline (Vanhoenacker)", "JO"],
    "sentiment": {"polarity": "mixed", "intensity": 0.7},
    "emotions": ["irritation", "amusement", "nostalgia"],
    "topics": ["format_variety", "political_coverage", "humor", "listening_context_car"],
    "language": {"register": "informal", "spontaneity": "high", "humor": true},
    "study_alignment": ["what_makes_you_stay", "editorial_choices"],
    "signal_strength": "strong",
    "interaction_type": "agreement_with_nuance"
  }
}
```

### 6.4 Pipeline Architecture

```
Discourse Webhooks / API Polling
         │
         ▼
┌─────────────────┐
│   Extraction     │  → Raw posts (JSON Lines)
│   (Python)       │
└────────┬─────────┘
         │
         ▼
┌─────────────────┐
│  Enrichment L1   │  → Descriptive metadata (LLM-powered)
│  (Python + LLM)  │     Entities, sentiment, emotions, topics
└────────┬─────────┘
         │
         ▼
┌─────────────────┐
│  Enrichment L2   │  → Interaction metadata (graph analysis)
│  (Python)        │     Reply graph, agreement, influence
└────────┬─────────┘
         │
         ▼
┌─────────────────┐
│  Enrichment L3   │  → Analytical metadata (LLM + researcher)
│  (Python + LLM)  │     Study alignment, signals, tensions
└────────┬─────────┘
         │
         ▼
┌─────────────────┐
│  Output Store    │  → Enriched JSON Lines + SQLite DB
│                  │     + CSV exports + (future) Arcade feed
└──────────────────┘
```

---

## 7. Restructured Output: Write-ups & Flat Views

### 7.1 The CLEA Restructuration Principle

In CLEA, the sequence is **structured → unstructured → restructured**:
1. The study brief structures the intent (themes, questions, axes).
2. The community discussion unstructures it (organic, free-flowing, unpredictable).
3. The pipeline restructures the collected material into analysis-ready artifacts.

CLEAgora's restructuration produces **generated Markdown documents** — immediately readable, shareable, and exploitable. Not raw data, not dashboards: **written analysis material** that a researcher can pick up and work with.

### 7.2 Verbatim Segmentation

Before restructuration, posts are segmented into **verbatims** — the minimal unit of meaning:

```
Post by auditeur_17:
"Honnêtement, ce qui me fait décrocher c'est quand ils passent 15 minutes
sur un sujet politique qui tourne en rond. [VERBATIM 1: irritant/political_coverage]
J'ai l'impression qu'ils oublient qu'on est dans la voiture, qu'on a besoin
de variété. [VERBATIM 2: expectation/format_variety/listening_context]
Par contre le jour où Charline a fait son billet sur les JO, j'ai failli
rater ma sortie d'autoroute tellement je riais. [VERBATIM 3: attachment/humor/chroniqueur]"
```

Each verbatim is:
- Extracted with its boundaries.
- Tagged with enrichment metadata (from Layer 1–3).
- Linked to its source (post, topic, author, thread position).
- Recomposable along any axis.

Segmentation is LLM-powered: the model identifies distinct units of meaning within a post, based on thematic shifts, argumentative moves, or distinct experiences.

### 7.3 Output Axes

The restructuration engine generates write-ups along multiple axes, all from the same enriched verbatim corpus:

**By Respondent** (`output/respondents/auditeur_17.md`):
> Portrait of a single respondent — all their contributions across the study, organized by theme. Shows their journey, evolution of opinions, key quotes.

**By Topic/Theme** (`output/themes/humor-le-matin.md`):
> All verbatims related to a theme (e.g., "humor in the morning show"), across all respondents. Shows the range of perspectives, convergences, tensions, strong signals.

**By Profile** (`output/profiles/daily-car-listeners.md`):
> Aggregated view for a respondent segment (e.g., daily listeners in their car). Cross-cuts themes to show how this profile experiences the subject differently from others.

**By Study Question** (`output/questions/what-makes-you-stay.md`):
> Directly aligned with the brief's research objectives. Synthesizes all relevant verbatims that address a specific study question, organized by sub-themes.

**Synthesis** (`output/synthesis.md`):
> Executive summary: key findings, strong signals, tensions, unexpected insights, recommendations for further exploration.

### 7.4 Write-up Generation

Each write-up is generated by an LLM operating on the enriched verbatim corpus:

```
Enriched Verbatims (JSON)
    + Write-up Template (from study config, aligned with brief)
    + Restructuration Prompt (axis-specific: "by respondent", "by theme", etc.)
        → LLM generates Markdown write-up
            → Researcher reviews and edits
```

**Template structure** (example: by-theme write-up):

```markdown
# [Theme Name]

## Synthesis
[2-3 paragraph summary of findings on this theme]

## Key Signals
- **Strong**: [repeated, emotional, detailed verbatims]
- **Weak**: [single mentions, tentative, worth exploring]

## Convergence
[Where respondents agree]

## Tensions
[Where respondents disagree or express opposing views]

## Verbatim Selection
### [Sub-theme 1]
> "[verbatim]" — [respondent], [profile], [context]
> "[verbatim]" — [respondent], [profile], [context]

### [Sub-theme 2]
> "[verbatim]" — ...

## Interaction Dynamics
[Notable exchanges: debates, co-construction, influence patterns]
```

### 7.5 The 72h Promise

The restructuration layer is what closes the "brief to intelligence" loop. Within the 72h flash deployment window:

- **Hours 0–4**: Brief → config → Discourse live.
- **Hours 4–72**: Community active, respondents interacting.
- **Hour 72+**: Pipeline extracts, enriches, and restructures → write-ups available.

The researcher gets **analysis-ready material** within hours of field closure — not raw data to process manually. This is the CLEA acceleration applied to community research.

---

## 8. Multimodality Roadmap

> Not in scope for the initial prototype. Documented here as a design direction.

### 8.1 Three Dimensions

**Stimuli injection** (input to respondents):
- Audio clips (radio extracts, jingles) → embed in topics via upload or external link.
- Video clips → Discourse supports video upload with transcoding.
- Images (screenshots, program grids, visuals) → standard image upload.
- Discourse handles all these natively. The study YAML config already has a `stimuli` field per topic.

**Rich responses** (output from respondents):
- Image uploads (photos, screenshots of their listening setup) → supported natively.
- Video responses (selfie reactions, screen recordings) → supported, requires enabling video upload.
- Voice notes → not natively supported in Discourse. Options:
  - Third-party voice note plugin (if one exists).
  - External voice recording tool → upload as audio file.
  - Discourse chat supports voice messages (but chat ≠ forum topics).
- **Pipeline impact**: images and videos need multimodal analysis (description, emotion, context). Voice notes need transcription before entering the verbatim pipeline.

**Voice responses & transcription**:
- Respondent records audio → uploaded to Discourse as attachment.
- Pipeline downloads, sends to transcription service (Whisper, Deepgram, etc.).
- Transcript becomes a "post equivalent" — enters the verbatim pipeline like text.
- Original audio preserved as source, transcript as working material.
- **Metadata addition**: transcription confidence, speaker emotion (from audio analysis), spoken vs. written register.

### 8.2 Implementation Priorities

| Capability | Effort | Value | When |
|-----------|--------|-------|------|
| Stimulus injection (audio/video/image in topics) | Low | High | Phase 1 (Discourse-native) |
| Image responses from respondents | Low | Medium | Phase 1 (Discourse-native) |
| Video responses from respondents | Medium | Medium | Phase 2 (enable + pipeline handling) |
| Voice note responses | High | High | Phase 3 (custom upload + transcription) |
| Multimodal analysis (image/video description) | High | Medium | Phase 4 (LLM vision integration) |

---

## 9. Implementation Strategy

### 9.1 Phase 1 — Foundation (Weeks 1-2)

**Goal**: a working Discourse instance + basic extraction.

| Task | Effort | Output |
|------|--------|--------|
| Set up Discourse Docker locally | 0.5 day | Running instance |
| Configure closed community settings | 0.5 day | `login_required`, `invite_only`, groups, permissions |
| Create study category structure | 0.5 day | Categories + sample topics matching the France Inter case |
| Build Discourse API client (Python) | 1 day | `discourse_client/` module with auth, topics, posts, users |
| Build basic extraction script | 1 day | Extract all posts from a study → JSON Lines output |
| Test with fake data | 0.5 day | Populate instance, extract, verify structure |

**Milestone**: can configure a study on Discourse, populate it with test content, and extract it cleanly.

### 9.2 Phase 2 — Bot + Enrichment (Weeks 3-4)

**Goal**: animated community + enriched output.

| Task | Effort | Output |
|------|--------|--------|
| Build bot service (scheduler + actions) | 1.5 days | Bot posts topics on schedule, sends PMs |
| Build webhook listener | 1 day | FastAPI app receives Discourse events |
| Build enrichment Layer 1 (descriptive) | 1.5 days | LLM-powered entity/sentiment/emotion extraction |
| Build enrichment Layer 2 (interactions) | 1 day | Reply graph, agreement detection |
| Study YAML configuration | 0.5 day | Declarative study definition |
| Integration test: full cycle | 1 day | Invite → participate → extract → enrich → output |

**Milestone**: can run a simulated study end-to-end.

### 9.3 Phase 3 — Branding + Deployment (Week 5)

**Goal**: deployable, branded prototype.

| Task | Effort | Output |
|------|--------|--------|
| Custom Discourse theme | 1 day | Clean, study-branded UI |
| Email template customization | 0.5 day | Branded invitations and notifications |
| Deploy to Hetzner VPS | 1 day | Live instance with SSL, SMTP, backups |
| Deploy CLEAgora services | 0.5 day | Bot + pipeline running alongside Discourse |
| Documentation | 0.5 day | Setup guide, study configuration guide |

**Milestone**: ready for a pilot study with real respondents.

### 9.4 Total Effort Estimate

**~12 working days** (vibe-coding pace: one dev + AI assistants).

This assumes exploration stage — no tests, minimal error handling, functional but not production-hardened. A real pilot study would require additional time for:
- Content preparation (study topics, stimuli, probes).
- Respondent recruitment and invitation.
- Moderation during the study.
- Analysis and reporting.

### 9.5 Key Technical Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Discourse Docker setup complexity | Medium | Blocks everything | Use official setup guide; fallback to Discourse-managed hosting for proto |
| API rate limits during extraction | Low | Slows pipeline | Use Data Explorer SQL for bulk; webhook for incremental |
| LLM enrichment quality | Medium | Garbage metadata | Start with simple prompts; iterate; researcher validation on Layer 3 |
| Respondent engagement | Medium | Empty community | Strong onboarding + moderator animation + notification strategy |
| Discourse version updates | Low (short study) | Plugin breakage | Pin version during study |

---

*Document generated during CLEAgora Cowork framing session — 2026-04-07*
