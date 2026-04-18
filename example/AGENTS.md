# AGENTS.md — ShopFast

## System Overview
- **ShopFast** — E-commerce platform (Node.js 20 + Express + PostgreSQL 16)
- **Monorepo**: `apps/api` (REST API), `apps/web` (React 18 frontend), `packages/shared` (common types)
- **Stack**: Node.js 20 / TypeScript / Express / PostgreSQL 16
- **Active project**: `auth-refactor` — migrating from session-based auth (express-session + connect-pg-simple) to JWT

## Boot Sequence

**Mandatory Boot Rules**:
1. Every step and rule is **MANDATORY**.
2. The main agent executes ALL boot reads. Never delegate boot reads to subagents — the main agent needs this information first-hand to operate correctly.
3. Do not perform any other action until boot sequence is completed.

### Phase 1 — Load all config (single parallel read)

The list of boot files is static and known. Read ALL of them in a single parallel call:

- `pith-framework/CONFIG.md` — provider, user identity, connection settings.
- `pith-framework/METHODOLOGY.yaml` — active methodology rules (states, artifacts, distillation, conventions). Contains `resource_hints` that determine what to load before acting. If missing or malformed: inform the user which fields are missing. Do not assume defaults.
- `pith-framework/SYSTEM.yaml` — system documentation index (what docs exist and how to load them). Do NOT load document content here — only register what's available.

> **Note**: this example uses the `markdown-files` provider. Hybrid providers (ClickUp, Notion, etc.) additionally read `pith-framework/providers/{provider}/MAPPING_BOOT.md` and `pith-framework/PROVIDER_CACHE.md` at this phase.

### Phase 2 — Resource hints (at boot time)

When entering a project context (boot with argument), apply resource hints:
  a. Scan ALL `resource_hints` from METHODOLOGY.yaml against the project's current phase and area
  b. List every matching hint (document name) — do not skip any
  c. Load ALL matched documents in a single batch (parallel if possible)
  d. If a document fails to load, inform the user — do not silently continue without it

During the session, resource hints serve as a **reference for the agent**: when starting work on a new area (e.g., switching from DB work to API integration), consult `resource_hints` and load relevant docs before proceeding.

### Phase 3 — Ready

**Ready to work.** Read work unit entry points only when the user asks.

### Boot Checklist (verify before proceeding to Phase 2)

| # | File | Verify |
|---|------|--------|
| 1 | `AGENTS.md` | System overview, invariants, context budget present |
| 2 | `CONFIG.md` | `provider` and `current_user` identified |
| 3 | `METHODOLOGY.yaml` | `work_unit.label` exists, `resource_hints` registered |
| 4 | `SYSTEM.yaml` | `documents[]` registered (not loaded) |
| 5 | `MAPPING_BOOT.md` | Provider API limitations and query patterns loaded (hybrid providers only) |
| 6 | `PROVIDER_CACHE.md` | Workspace ID resolved, warm/cold start completed (hybrid providers only) |

If any row fails verification, stop and inform the user before proceeding.

## Invariants

These rules apply in every session, unconditionally:
- Never use past conversation transcripts as memory — distill to artifacts
- Never duplicate info between artifacts — cross-reference
- Distill before losing context (proactive when context fills up)
- User can always request distillation (non-negotiable trigger)
- Before accessing external sources (DB, APIs) directly, check if documented info exists in SYSTEM.yaml — load it first
- **Docs-before-code**: before exploring code (reading source files, using Glob/Grep, launching exploration agents), first load all REFERENCE documentation relevant to the area being explored — ARCHITECTURE, module context (`apps/{module}/CLAUDE.md`), or any matching resource hint. Code exploration must happen with the best available context, not before it.

## Context Budget

- **Lazy loading** by default — do not load what is not needed
- **Layer principle** — load from general (engine) to specific (work unit)
- Never load multiple log files, inactive modules, or unrequested documents
- The framework **complements** native agent memories — it does not replace them
- On conflict between native memory and framework, **framework prevails** (explicit, versioned, human-curated)

## On-disk Resources

| Need... | Read |
|---------|------|
| Framework engine + provider contract | `pith-framework/framework/ENGINE.md` (on-demand) |
| Methodology (states, artifacts, conventions) | `pith-framework/METHODOLOGY.yaml` |
| System documentation index | `pith-framework/SYSTEM.yaml` |
| Configuration (user, provider) | `pith-framework/CONFIG.md` (gitignored) |
| Reference architecture | `pith-framework/ARCHITECTURE.md` (on-demand) |
| Reusable lessons | `pith-framework/LESSONS_LEARNED.md` (on-demand) |
| Module-level code context | `apps/{module}/CLAUDE.md` (load only when working on that module) |
| Project documents | `pith-framework/projects/{project-name}/` (CURRENT_STATUS, PLAN, etc.) |
