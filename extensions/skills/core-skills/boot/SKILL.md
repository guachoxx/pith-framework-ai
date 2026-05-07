---
name: pith-boot
description: "Use when starting a Pith Framework session, listing active work units, entering a work unit by name, or when Pith config files are present but not loaded yet."
---

# Pith Boot - Session Initialization

Execute the Pith Framework boot sequence with the fast path first. A warm no-argument boot should load only the boot contract and the live work-unit index; provider deep docs, reference docs, and work-unit entry points stay lazy.

## Fast Path Rules

- Prefer the warm path. Do not read full `MAPPING.md`, reference document content, or work-unit entry points unless a fallback below requires it.
- Do not load resource hints for no-argument boot. Only register that resource hints exist.
- For hybrid providers, use `MAPPING_BOOT.md` for the live Project Index query pattern; use cache only to resolve known IDs.
- For `markdown-files`, compute the project index path directly:
  - If `current_user` is set: `pith-framework/projects/{current_user}/_INDEX.md`
  - Otherwise: `pith-framework/projects/_INDEX.md`
- Read full provider `MAPPING.md` only on cold start, missing boot mapping, or genuinely unknown provider behavior.

## Phase 1 - Load boot context (two parallel batches)

Provider-specific files depend on the `provider` value in CONFIG.md, so boot uses two ordered batches. Within each batch, read files in parallel when possible.

### Phase 1a - Static boot batch

Read ALL of these files in a single parallel call:

1. `AGENTS.md` - system overview, invariants, context budget, on-disk resource map
   - If missing: STOP. The project is not configured for Pith.
2. `pith-framework/CONFIG.md` - provider type, user identity, connection settings
   - If missing: STOP. Ask user to create it. See `pith-framework/providers/` for setup.
3. `pith-framework/METHODOLOGY.yaml` - active methodology (states, artifacts, distillation, optional conventions)
   - If missing or malformed: STOP. Inform user which fields are missing. Do NOT assume defaults.
   - **Required fields** (engine contract; malformed = any of these missing):
     - `identity.name` and `identity.version`
     - `work_unit.label` and `work_unit.entry_point`
     - `work_unit.entry_point_fields` including `last_updated` and `next_step`
     - `states.values` with at least one `active` state and one `completed` state
     - `distillation.always_update` including `work_unit.entry_point`
4. `pith-framework/SYSTEM.yaml` - system documentation index. Register what docs exist. Do NOT load content.

After Phase 1a, identify `provider` from CONFIG.md.

### Phase 1b - Provider boot batch

For hybrid providers only:

5. `pith-framework/providers/{provider}/MAPPING_BOOT.md` - build path from `provider` field in CONFIG.md. Contains API limitations, entity mapping summary, query patterns.
6. `pith-framework/PROVIDER_CACHE.md` - cached entity IDs for direct access.
   - **Warm start** (file exists): read cache, ready to proceed
   - **Cold start** (no file): read full MAPPING.md of the provider, build cache from provider

For the `markdown-files` provider, skip `MAPPING_BOOT.md` and `PROVIDER_CACHE.md`; do not read `providers/markdown-files/MAPPING.md` during normal boot.

**IMPORTANT - Cache has two types of data**:
- `## Infrastructure` and `## Reference Documents` = **stable IDs**, safe to use directly
- `## Projects` = **ID reference only** for known projects. NOT an exhaustive list. Always query the provider live for project discovery.

## Phase 1c - Boot Checklist

Verify ALL of these before proceeding. If any fails, STOP and inform the user:

| # | File | Verify |
|---|------|--------|
| 1 | AGENTS.md | System overview, invariants, context budget present |
| 2 | CONFIG.md | `provider` and `current_user` identified |
| 3 | METHODOLOGY.yaml | Engine contract valid: identity, work_unit entry point, states, always_update |
| 4 | SYSTEM.yaml | `documents[]` registered (names known, content NOT loaded) |
| 5 | Work unit index | `_INDEX.md` exists with Project/State/Owner/Last updated columns (markdown-files only) |
| 6 | MAPPING_BOOT.md | Provider API limitations and query patterns loaded (hybrid providers only) |
| 7 | PROVIDER_CACHE.md | Workspace ID resolved, warm or cold start completed (hybrid providers only) |

## Phase 2 - Resource hints (conditional)

Do not run this phase for plain no-argument boot used to list active work units.

Apply resource hints only when entering a work unit context or starting a concrete task area:

1. If `conventions.resource_hints` does not exist, continue without preloading hint-based documents.
2. If boot has `$ARGUMENTS`, first read the work unit entry point in Phase 3, then scan ALL hints against that work unit's current phase and area.
3. If the user starts a concrete task area after boot, scan ALL hints against that task area before acting.
4. List every matching hint (document name) — do not skip any.
5. Load ALL matched documents in a single batch (parallel if possible).
6. If a document fails to load, inform the user — do not silently continue without it.

## Phase 3 - Depends on arguments

### If NO argument provided:

1. Query the work unit index **live from the provider**. For hybrid providers, use the query pattern from `MAPPING_BOOT.md`. For `markdown-files`, read only the computed `_INDEX.md` path from the Fast Path Rules. Do NOT rely on cache as a complete work unit list.
2. Display summary:
   - System: project name, stack (from SYSTEM.yaml identity)
   - Methodology: name, version (from METHODOLOGY.yaml identity)
   - Active projects grouped by state, ordered by their position in `states.values` from METHODOLOGY.yaml (first defined = first shown). Within each group, sort by `Last updated` from the work unit index metadata ascending (oldest first). Show: name, owner, Last updated for each. Do not read entry point artifacts just to sort or list.
3. **Ready to work.** Read work unit entry points only when the user asks.

### If argument provided (`$ARGUMENTS`):

1. Locate the work unit by name in the provider (try cache first for hybrid providers, fall back to provider search/index)
2. Read the work unit entry point: the artifact named in `work_unit.entry_point`. Do not assume a specific artifact name.
3. Apply Phase 2 resource hints if configured, using the loaded entry point's current phase and area.
4. If `conventions.staleness.threshold_hours` exists, check staleness: if `last_updated` exceeds the threshold, warn the user. If no staleness convention exists, skip this check.
5. Display:
   - System + methodology summary
   - **Work unit context**: the fields declared in `work_unit.entry_point_fields`, including `next_step`
   - **Pre-loaded docs**: list what was loaded via resource hints (Phase 2)
6. **Ready to continue.** The agent can execute `next_step` without asking questions.

## Rules

- The **main agent** executes ALL boot reads. Never delegate boot reads to subagents.
- Do not perform any other action until boot is complete.
- This skill is the canonical boot sequence — aligned with AGENTS.md.
