# Vision – CLEAgora

## Purpose

CLEAgora is a community-based qualitative research platform built on Discourse. It adapts the CLEA (Consumer-Level Elicitation Architecture) methodology — originally designed for 1:1 AI-guided conversations — into a **collective, forum-based format** where respondents interact with each other, not just with a moderator.

The core insight: in a community setting, the richness comes from **debate, co-construction, and organic interaction** between participants. CLEAgora captures this collective intelligence while maintaining CLEA's rigorous approach to structuring, enriching, and analyzing qualitative material.

CLEAgora is a module within the DECODia ecosystem. It inherits DECODia's foundational principles: sovereign infrastructure, systematic metadata generation, calibrated orchestration, and continuous expert supervision.

## Users / Audience

**Respondents**: recruited externally and invited via email into a closed Discourse instance. They participate in structured discussions, react to stimuli, and interact with each other in a guided but natural forum environment.

**Researchers / Study leads** (h2\ team): design the study architecture (categories, topics, discussion guides), configure the community, supervise the field, and interpret results. They are the Human In The Loop.

**Clients**: consume the structured intelligence produced — dashboards, verbatim exploration, synthesis reports — via Arcade or dedicated deliverables.

## Expected outcomes

- A functional prototype demonstrating the CLEAgora concept: Discourse as a qualitative research terrain with a downstream analysis pipeline.
- Invitation-only community management (email-based onboarding, closed registration).
- A moderation/animation model (bot, human, or hybrid — to be defined during Foundation).
- Extraction pipeline: Discourse content → structured, enriched data → analysis-ready material.
- Integration point with the broader DECODia/Arcade ecosystem.

## Objectives

- Validate that Discourse can serve as a qualitative research platform for closed communities.
- Demonstrate the collective dimension as a differentiator vs. CLEA 1:1.
- Build a working extraction + enrichment pipeline from Discourse data.
- Define the animation model (how topics are created, how discussions are guided, how respondents are engaged).
- Produce a prototype deployable for a real pilot study.

## Non-objectives

- Building a public community or social network.
- Replacing CLEA's 1:1 conversational capabilities (CLEAgora complements, it doesn't replace).
- Building a full production-grade SaaS platform (this is a prototype).
- Deep Discourse core modifications (prefer API, plugins, and themes over core forks).

## Constraints

- **Closed community**: no public registration; email invitation only.
- **Discourse ecosystem**: work within Discourse's plugin/theme/API architecture — avoid core forks.
- **Infra**: AWS EC2 (h2\ infrastructure) for both prototype and production.
- **Sovereignty**: data must remain on controlled infrastructure (no third-party SaaS for Discourse hosting in production).
- **Team**: small team, vibe-coding workflow with AI assistance.
- **Timeline**: prototype-first, iterate from real usage.

## Stage

**Exploration**

We are testing the core idea: can Discourse serve as a collective qualitative research terrain, and can we build a viable extraction/enrichment pipeline from it? Throwaway code is acceptable, the priority is validating the concept and identifying the key technical and methodological challenges.

Stage definitions:
- **Exploration** – Testing an idea. Throwaway code, minimal overhead, no tests required.
- **Foundation** – Setting up the real architecture. Structural decisions matter, discuss before acting.
- **MVP** – Building toward a first usable deliverable. Balance speed and quality. May include first deployment.
- **Growth** – Product in service, adding features. Stability, tests, and robustness become priorities.
- **Maintenance** – Stable product. Focus on fixes, refactors, dependency upgrades.
