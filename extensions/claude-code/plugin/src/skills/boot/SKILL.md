---
name: pith-boot
description: "Initialize a Pith Framework session. Executes the full boot sequence: loads config, methodology, system index, provider cache, verifies boot checklist, applies resource hints. Without arguments shows active projects. With a project name enters that project context immediately, loads entry point, checks staleness, applies resource hints, ready to resume. Use this skill at the start of every session, when the user mentions a Pith project by name, asks to start working, says boot, arranca, inicia sesión, or when Pith config files (CONFIG.md, METHODOLOGY.yaml) are present but have not been loaded yet."
---

# Pith Boot - Session Initialization

Execute the full Pith Framework boot sequence. This ensures every session starts with complete, verified context.

## Phase 1 - Load all config (single parallel read)

Read ALL of these files in a single parallel call. The list is static and known:

1. `AGENTS.md` - system overview, invariants, context budget, on-disk resource map
   - If missing: STOP. The project is not configured for Pith.
2. `pith-framework/CONFIG.md` - provider type, user identity, connection settings
   - If missing: STOP. Ask user to create it. See `pith-framework/providers/` for setup.
3. `pith-framework/METHODOLOGY.yaml` - active methodology (states, artifacts, distillation, conventions, resource_hints)
   - If missing or malformed: STOP. Inform user which fields are missing. Do NOT assume defaults.
   - **Required fields** (malformed = any of these missing):
     - `work_unit.label` and `work_unit.entry_point`
     - `states.values` (at least one state)
     - `artifacts.standard` (at least CURRENT_STATUS)
     - `distillation.always_update`
     - `distillation.triggers`
     - `conventions.staleness.threshold_hours`
4. `pith-framework/SYSTEM.yaml` - system documentation index. Register what docs exist. Do NOT load content.
5. `pith-framework/providers/{provider}/MAPPING_BOOT.md` - build path from `provider` field in CONFIG.md. Contains API limitations, entity mapping summary, query patterns.
6. `pith-framework/PROVIDER_CACHE.md` - cached entity IDs for direct access
   - **Warm start** (file exists): read cache, ready to proceed
   - **Cold start** (no file): read full MAPPING.md of the provider, build cache from provider

**IMPORTANT - Cache has two types of data**:
- `## Infrastructure` and `## Reference Documents` = **stable IDs**, safe to use directly
- `## Projects` = **ID reference only** for known projects. NOT an exhaustive list. Always query the provider live for project discovery.

## Phase 1b - Boot Checklist

Verify ALL of these before proceeding. If any fails, STOP and inform the user:

| # | File | Verify |
|---|------|--------|
| 1 | AGENTS.md | System overview, invariants, context budget present |
| 2 | CONFIG.md | `provider` and `current_user` identified |
| 3 | METHODOLOGY.yaml | `work_unit.label` exists, `resource_hints` registered |
| 4 | SYSTEM.yaml | `documents[]` registered (names known, content NOT loaded) |
| 5 | MAPPING_BOOT.md | Provider API limitations and query patterns loaded |
| 6 | PROVIDER_CACHE.md | Workspace ID resolved, warm or cold start completed |

## Phase 2 - Resource hints

**Before acting on any request**, apply resource hints from METHODOLOGY.yaml:

1. Scan ALL `resource_hints` against the user's request (or project context if argument provided)
2. List every matching hint (document name) — do not skip any
3. Load ALL matched documents in a single batch (parallel if possible)
4. If a document fails to load, inform the user — do not silently continue without it
5. Only after ALL matched documents are loaded, proceed to Phase 3

## Phase 3 - Depends on arguments

### If NO argument provided:

1. Query the Project Index **live from the provider** (use query pattern from MAPPING_BOOT.md). Do NOT rely on cache as project list.
2. Display summary:
   - System: project name, stack (from SYSTEM.yaml identity)
   - Methodology: name, version (from METHODOLOGY.yaml identity)
   - Active projects grouped by state, ordered by their position in `states.values` from METHODOLOGY.yaml (first defined = first shown). Within each group, sort by last_updated ascending (oldest first). Show: name, owner, last_updated for each.
3. **Ready to work.** Read work unit entry points only when the user asks.

### If argument provided (`$ARGUMENTS`):

1. Locate the project by name in the provider (try cache first for ID, fall back to search)
2. Read the project entry point (the artifact named in `work_unit.entry_point`, typically CURRENT_STATUS)
3. Check staleness: if `last_updated` exceeds `conventions.staleness.threshold_hours`, warn the user
4. Display:
   - System + methodology summary
   - **Project context**: last_session_summary, next_step, done_when
   - **Pre-loaded docs**: list what was loaded via resource hints (Phase 2)
5. **Ready to continue.** The agent can execute `next_step` without asking questions.

## Rules

- The **main agent** executes ALL boot reads. Never delegate boot reads to subagents.
- Do not perform any other action until boot is complete.
- This skill is the canonical boot sequence — aligned with AGENTS.md.
