# Example: Worked End-to-End Project

This directory shows what a project looks like in practice using the **markdown-files** provider with the **default** methodology.

## Scenario

A fictional e-commerce platform (`ShopFast`) needs to refactor its authentication system from session-based to JWT. The project spans 4 phases and several sessions.

## What's here

```
example/
├── AGENTS.md                                  ← Entry point (customized for ShopFast)
├── CLAUDE.md                                  ← Bridge for Claude Code → AGENTS.md
└── pith-framework/
    ├── METHODOLOGY.yaml                       ← Default methodology (active)
    ├── SYSTEM.yaml                            ← System documentation index
    ├── CONFIG.md                              ← User identity + provider (would be gitignored)
    ├── ARCHITECTURE.md                        ← System architecture overview
    ├── LESSONS_LEARNED.md                     ← Reusable lessons
    └── projects/
        ├── _INDEX.md                          ← Project index (one entry)
        └── auth-refactor/                     ← Project container
            ├── CURRENT_STATUS.md              ← Where we are now
            ├── SPECIFICATIONS.md              ← Requirements
            ├── TECHNICAL_ANALYSIS.md          ← What we found
            ├── PLAN.md                        ← What we're going to do
            ├── CHANGELOG.md                   ← What changed
            ├── TECHNICAL_REPORT.md            ← What we built
            └── TESTING.md                     ← How we verify it works
```

## How to read this

1. Start with `AGENTS.md` — this is what the agent reads first
2. Then `pith-framework/projects/auth-refactor/CURRENT_STATUS.md` — see where the project stands
3. Browse the other documents to see how they complement each other

Each document is filled with realistic content showing what it looks like mid-project (after Phase 2 of 4 is complete).

> **Note**: Some reference documents (BUILD_COMMANDS, TESTING_METHODOLOGY, CREDENTIALS) are omitted from this example for brevity — in a real project, they would contain your team's build commands and credentials. `ENGINE.md` would live at `pith-framework/framework/ENGINE.md` as a copy of the canonical `ENGINE.md` from this repo; it's also omitted here to avoid duplicating the source.
