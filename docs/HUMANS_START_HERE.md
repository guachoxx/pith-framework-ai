# Pith Framework — Guide for Humans

This guide explains the framework from a human perspective: what it does, how your daily workflow changes, and the rules that make it work.

> **Haven't installed Pith Framework yet?** See [BOOTSTRAP.md](../BOOTSTRAP.md) for an agent-driven setup walkthrough (your agent asks a few questions and creates the files). For the manual alternative, see the "Quick Start" section of [README.md](../README.md).

## The Problem It Solves

AI coding agents are powerful but have two fundamental limitations:

1. **Finite context window** — In long sessions, the context fills up and the agent loses track or starts hallucinating.
2. **Amnesia between sessions** — Every new session starts from scratch. The agent doesn't remember what you did yesterday.

The usual outcome: repeating context, losing technical decisions, and the agent suggesting things that were already discarded.

## The Solution

A structured set of documents that the agent reads on startup and updates before the context fills up. Each session starts by reading clean documents and ends by distilling work into them.

```
Session 1                    Session 2                    Session 3
─────────                    ─────────                    ─────────
Read docs → Work →           Read docs → Work →           Read docs → Work →
Update docs                  Update docs                  Update docs
```

**Where** those documents live depends on your chosen **provider**: local `.md` files, ClickUp, Notion, or any other platform. The methodology stays the same.

---

## Three Layers

| Layer | What it contains | When it's read |
|-------|-----------------|----------------|
| **Engine** | Framework kernel — boot protocol, primitive services, methodology contract | On demand (reference) |
| **Methodology** | How work is organized — states, artifacts, distillation rules, conventions | On every startup |
| **System Knowledge** | Your project's documentation — architecture, module context, reference docs | On demand |

The engine never changes. The methodology is chosen per team. System knowledge is defined per project or across the entire codebase.

---

## Daily Workflow

### Starting a session

You don't need to do anything special. The agent reads `AGENTS.md` on startup, then follows the 3-phase boot sequence:

1. **Read** `AGENTS.md` — system overview, invariants, context budget.
2. **Phase 1** — Parallel read of all config: `CONFIG.md` (provider, your identity), `METHODOLOGY.yaml` (how work is organized), `SYSTEM.yaml` (documentation index). For hybrid providers (ClickUp, Notion, etc.) the agent also reads `providers/{provider}/MAPPING_BOOT.md` and `PROVIDER_CACHE.md` in the same batch.
3. **Phase 2** — Apply `resource_hints` from METHODOLOGY.yaml: load any reference docs that match the task area before acting.
4. **Phase 3** — Ready. The agent reads a project's CURRENT STATUS only when you ask to work on it — not all projects upfront.

In seconds it knows what's going on.

If you want to be explicit:

> "Read AGENTS.md and tell me the current status of the auth-refactor project."

If you haven't worked with the agent for a while (more than 48h), it will ask if the status is still valid before assuming anything.

### During the session

Work as usual. If the agent needs context from a specific module:

> "Read the module context for src/api."

If you notice the agent starting to lose track:

> "You're losing context. Read CURRENT STATUS to reorient."

### Closing the session (distillation)

This is the most important part of the framework. Before closing, tell the agent:

> "Consolidate the session: update CURRENT STATUS with what we've done and define the Next Step."

These also work: **"Consolidate"** / **"Distill"** / **"Save progress"**

If you forget, the agent should propose it when it detects the context is filling up.

What the agent updates depends on the project phase:

| Phase | Primary document updated |
|-------|-------------------------|
| Analysis | TECHNICAL ANALYSIS — findings, constraints, structure |
| Planning | PLAN — phases, files, order |
| Development | TECHNICAL REPORT — what was built, technical decisions |
| Testing | TESTING — test scenarios, results, verification |
| Always | CURRENT STATUS — concrete next step |

---

## The 7 Project Documents

For structured projects, the framework uses 7 documents with differentiated roles:

```
SPECIFICATIONS → TECHNICAL ANALYSIS → PLAN          → TECHNICAL REPORT → TESTING
──────────────   ──────────────────   ──────          ──────────────────   ───────
What is asked?   What exists?         What to do?     What was built?      Does it work?

For team         For the agent        For the agent   For team             For team
```

- **CURRENT STATUS** — Always present. Current state, what was done, what's left, concrete next step and verification condition.
- **SPECIFICATIONS** — Requirements: what the feature/change must do, acceptance criteria, constraints, out-of-scope. Created early, approved before planning starts.
- **TECHNICAL ANALYSIS** — Research: existing code involved, constraints, data structures, prior design decisions. The agent consults it to avoid repeating analysis.
- **PLAN** — Strategy: ordered phases, files to create/modify, dependencies. The agent consults it to know what to do next.
- **CHANGELOG** — Chronological record of code changes.
- **TECHNICAL REPORT** — Result: technical documentation of what was built. Aimed at the engineering team.
- **TESTING** — Test plan, test cases, and results.

### Ad-hoc Work (Small Tasks)

For fixes, scoped refactors, or tasks completable in 1-2 sessions: only CURRENT STATUS + CHANGELOG. Specs can be a section inside CURRENT STATUS. If the task reveals complexity, it gets promoted to a full project.

---

## Module Context

Each code module can have its own context document (`{module}/CLAUDE.md`, ~50 lines max) with: what it does, dependencies, key patterns, files, and pitfalls. Direct, imperative language. Only what the agent needs to avoid mistakes when touching that code.

These always live on disk alongside the code, regardless of provider.

---

## Key Phrases the Agent Understands

| You say | The agent does |
|---------|---------------|
| "Consolidate" / "Distill" / "Save progress" | Updates all memory documents according to the current phase |
| "Create a project called X" | Creates the project container and initial documents |
| "Where are we with X?" | Reads the project's CURRENT STATUS |
| "Show me bob's projects" | Reads bob's projects from the project index (read-only) |
| "Close project X" | Archives deliverables, cleans up the project container, updates the index |

---

## Key Rules

1. **No duplication** — Each piece of data lives in one place only. Other documents point to it with references.
2. **No transcripts** — Never save conversations to "remember." Everything is distilled to structured documents.
3. **Lazy loading** — The agent only loads what it needs, when it needs it. No bulk loading.
4. **Cross-referencing** — Before creating something new, the agent reads the existing equivalent first.
5. **Staleness** — If a CURRENT STATUS is more than 48h old, the agent asks before assuming it's valid.
6. **Module context is mandatory** — If the core logic of a module is modified, updating its context document is mandatory.
7. **Distill before losing context** — The agent may proactively propose distillation when it senses context filling up (best-effort — LLMs self-estimate their context usage unreliably). More reliable: say "Consolidate" when you finish a block of work or switch topics.
8. **User can always request distillation** — Saying "Consolidate" is always available, non-negotiable. This is the primary mechanism; treat agent-initiated proposals as a nice-to-have nudge.

---

## Multi-User Setup

If multiple people use the agent on the same codebase, the framework supports per-user project ownership.

### How to enable it

Each user sets their identity in `pith-framework/CONFIG.md` (gitignored):

```
## User
current_user: Alice
```

### What's shared vs. owned

| Concept | Scope |
|---|---|
| Projects, project index entries | **Owned** per user (freely accessible to all) |
| Reference documents (ARCHITECTURE, etc.) | **Shared** across team |
| Module context | **Shared** (code-level) |
| LESSONS LEARNED | **Shared** across team |

### How it works

When `current_user` is set, the agent assigns ownership to new projects and can filter by owner:
- **Create**: `"Create a project called auth-refactor"` → creates with ownership = current user
- **Read**: The agent can read any project regardless of owner
- **Distill**: Only your project documents are updated (shared docs like LESSONS LEARNED update normally)
- **Cross-user read**: `"Show me bob's projects"` → reads bob's projects from the project index

---

## Adapting to Your Project

1. **Choose a provider** — See [`providers/`](../providers/) for available options. If yours isn't there, create one following the guide in [`providers/README.md`](../providers/README.md).
2. **Entry point** (`AGENTS.md`) — Rewrite the System Overview section with your system's description.
3. **Methodology** — The default methodology works for most projects. If you need something different, see [`methodologies/`](../methodologies/) for alternatives (OpenSpec for spec-driven work, Kanban-Lite for minimal tracking).
4. **System knowledge** (`SYSTEM.yaml`) — Uncomment the reference documents that apply to your project.
5. **Module context** — Create `{module}/CLAUDE.md` for each code module. The "Dependencies" section is especially valuable in legacy stacks.
6. **Credentials** — Fill in with your environments and credentials. Ensure restricted access.

---

## Quick Document Reference

| Document | For whom | Purpose |
|----------|----------|---------|
| AGENTS.md | Agent | Entry point, boot sequence, invariants |
| METHODOLOGY.yaml | Agent | How work is organized (states, artifacts, conventions) |
| SYSTEM.yaml | Agent | What documentation exists |
| CONFIG.md | Agent | Provider and user identity |
| ENGINE.md | Agent (on demand) | Framework kernel (services, contract) |
| CURRENT STATUS | Agent | Where we are, what's next |
| SPECIFICATIONS | Team + Agent | Requirements and acceptance criteria |
| TECHNICAL ANALYSIS | Agent | Prior research |
| PLAN | Agent | Implementation plan |
| CHANGELOG | Agent + Team | Change history |
| TECHNICAL REPORT | Team | Deliverable technical documentation |
| TESTING | Team + Agent | Test plan, cases, and results |
| LESSONS LEARNED | Agent | Mistakes not to repeat |
| Module context | Agent | Local module context |
| CREDENTIALS | Agent | Credentials (restricted access) |
