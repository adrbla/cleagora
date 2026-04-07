# CLEAgora

Community-based qualitative research platform built on [Discourse](https://www.discourse.org/).

CLEAgora adapts the **CLEA methodology** (Consumer-Level Elicitation Architecture) — originally designed for 1:1 AI-guided conversations — into a **collective, forum-based format** where recruited respondents interact with each other in closed communities.

Part of the [DECODia](https://decodia.ai) ecosystem by [h2\](https://h2.fr).

## Concept

- **Closed communities**: respondents are invited by email into a private Discourse instance configured for a specific study.
- **Collective-first**: the value comes from debate, co-construction, and organic interaction between participants.
- **Flash deployment**: brief → auto-config → live community → restructured output in 72h.
- **Structured output**: an extraction + enrichment pipeline transforms forum content into analysis-ready material (segmented verbatims, thematic tags, interaction graphs, Markdown write-ups).

## Status

**Exploration stage** — validating the concept. No application code yet. Design documents and reference material are in `context/`.

## Project structure

```
CLAUDE.md              # AI assistant instructions
DEVS.md                # Developer workflow guide
context/
  vision.md            # Purpose, users, constraints, stage
  journal.md           # Session log (reverse chronological)
  decisions.md         # Architectural/product decisions
  backlog.md           # Now / Next / Later tasks
  tech-stack.md        # Technologies and conventions
  references/          # Design docs, research, meeting notes
```

## Getting started

_Setup instructions will be added once the Discourse instance and Python pipeline are in place._

See `DEVS.md` for the developer workflow and `context/backlog.md` for current priorities.

## License

Proprietary — h2\ / Ubyx.
