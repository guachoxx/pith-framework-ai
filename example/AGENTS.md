# AGENTS.md — ShopFast

## System Overview
- **ShopFast** — E-commerce platform (Node.js 20 + Express + PostgreSQL 16)
- **Monorepo**: `apps/api` (REST API), `apps/web` (React 18 frontend), `packages/shared` (common types)
- **Stack**: Node.js 20 / TypeScript / Express / PostgreSQL 16
- **Active project**: `auth-refactor` — migrating from session-based auth (express-session + connect-pg-simple) to JWT

## Boot Sequence

If the `pith-boot` skill is available, it is the procedural source of truth for executing boot. This section is a repo-local summary/fallback and must not override the skill.

> 📌 **Contract source**: `ENGINE.md` defines the framework boot invariants and methodology contract. **Execution source**: `pith-boot` defines the procedural boot flow when available. Keep this summary aligned with both.

**Mandatory Boot Rules**:
1. Every step and rule is **MANDATORY**.
2. The main agent executes ALL boot reads. Never delegate boot reads to subagents — the main agent needs this information first-hand to operate correctly.
3. Do not perform any other action until boot sequence is completed.

### Phase 1 — Load boot context (two parallel batches)

Provider-specific files depend on the `provider` field in `CONFIG.md`, so boot uses two ordered batches. Within each batch, read files in parallel when possible.

#### Phase 1a — Static boot batch

Read ALL of these files in a single parallel call:

- `AGENTS.md` — system overview, invariants, context budget, on-disk resource map.
- `pith-framework/CONFIG.md` — provider, user identity, connection settings.
- `pith-framework/METHODOLOGY.yaml` — active methodology rules (states, artifacts, distillation, optional conventions). If missing or malformed: inform the user which engine-contract fields are missing. Do not assume defaults.
- `pith-framework/SYSTEM.yaml` — system documentation index (what docs exist and how to load them). Do NOT load document content here — only register what's available.

#### Phase 1b — Provider boot batch

> **ShopFast provider**: this example uses `markdown-files`, so skip `pith-framework/providers/{provider}/MAPPING_BOOT.md` and `pith-framework/PROVIDER_CACHE.md`. Do not read `providers/markdown-files/MAPPING.md` during normal boot.

> **Plain no-argument boot**: use the fast path. Read the project index directly: if `current_user` is set, use `pith-framework/projects/{current_user}/_INDEX.md`; otherwise use `pith-framework/projects/_INDEX.md`. Do not load resource hints, reference document content, provider mapping, or project entry points just to list active projects.

### Phase 2 — Resource hints (conditional)

Do not run this phase for plain no-argument boot used to list active projects.

Apply resource hints only when entering a work unit context or starting a concrete task area:
  a. If `conventions.resource_hints` does not exist, continue without preloading hint-based documents.
  b. If boot has an argument, first read the project entry point in Phase 3, then scan ALL hints against the project's current phase and area.
  c. If the user starts a concrete task area after boot, scan ALL hints against that task area before acting.
  d. List every matching hint (document name) — do not skip any.
  e. Load ALL matched documents in a single batch (parallel if possible).
  f. If a document fails to load, inform the user — do not silently continue without it.

During the session, resource hints serve as a **reference for the agent** when present: when starting work on a new area (e.g., switching from DB work to API integration), consult `resource_hints` and load relevant docs before proceeding.

### Phase 3 — Ready

**Ready to work.** Read work unit entry points only when the user asks.

### Boot Checklist (verify before proceeding to Phase 2)

| # | File | Verify |
|---|------|--------|
| 1 | `AGENTS.md` | System overview, invariants, context budget present |
| 2 | `CONFIG.md` | `provider` and `current_user` identified |
| 3 | `METHODOLOGY.yaml` | Engine contract valid: identity, work_unit entry point, states, always_update |
| 4 | `SYSTEM.yaml` | `documents[]` registered (not loaded) |
| 5 | Work unit index | `_INDEX.md` exists with Project/State/Owner/Last updated columns (markdown-files only) |
| 6 | `MAPPING_BOOT.md` | Provider API limitations and query patterns loaded (hybrid providers only) |
| 7 | `PROVIDER_CACHE.md` | Workspace ID resolved, warm/cold start completed (hybrid providers only) |

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
