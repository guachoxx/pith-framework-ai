---
name: pith-consolidate
description: "Distill current session into framework memory artifacts. Ensures knowledge survives between sessions. Use this skill whenever the user says consolidate, distill, save, save progress, guarda, consolida, destila; when switching topics or projects; after completing a significant block of work; when context is getting full; or before ending a session. If in doubt about whether to consolidate, do it — it is the most important operation in the Pith Framework."
---

# Pith Consolidate - Session Distillation

Distill the current session work into persistent framework artifacts. Nothing is lost between sessions.

## Prerequisites

- Boot must be completed (config, methodology, system loaded)
- An active project must be in context

If no project is in context, ask the user which project to consolidate for.

## Step 1 - Identify phase and targets

1. Read `pith-framework/METHODOLOGY.yaml` if not already in context
2. Identify the **active project** and its **current state** (from the Project Index or entry point)
3. Read the entry point artifact named in `work_unit.entry_point`
4. **Staleness check**: If `conventions.staleness.threshold_hours` exists and `last_updated` in the entry point exceeds it, warn the user: the entry point may not reflect reality. Ask whether to proceed with consolidation or re-read the entry point first. If no staleness convention exists, skip this check.
5. Determine artifact targets:
   - Always include everything in `distillation.always_update` (must include the entry point)
   - If `conventions.distillation_checklist` exists and contains a target set for the current state or a clearly mapped phase, use those targets too
   - Else if `distillation.targets_by_phase` exists and contains a target set for the current state or phase, use those targets too
   - Else update only `distillation.always_update`
6. Do not assume default state names such as PLANNING, IN_PROGRESS, or TESTING. Do not assume a specific entry point artifact name.

## Step 2 - Prepare content for each target

For each artifact in the target list, determine what to write based on the session work.

**Priority levels** may appear in `conventions.distillation_checklist`:
- `always`: MUST update regardless of what happened
- `primary`: Main artifact for this phase, update with core work
- `if_applies`: Update only if relevant work was done
- `if_changes`: Update only if code changes were made
- `mandatory_if_modified`: MUST update if the module code was changed

If the methodology does not define priorities, use this fallback:
- Update every artifact in `distillation.always_update`
- Update additional targets only when the methodology explicitly declares them or the user explicitly asks

## Step 3 - Update the entry point artifact (always)

Update the artifact named in `work_unit.entry_point`.

If `conventions.entry_point_format.template` exists, use it. Otherwise, generate a minimal entry point containing every field declared in `work_unit.entry_point_fields`. At minimum it must include:

```
**Last updated**: [today YYYY-MM-DD]
**Next step**: [concrete action to resume, NOT "continue development"]
```

Add any additional declared fields with concrete values. Keep the field names and format consistent with the existing entry point when one exists.

**Quality check** before writing:
- `next_step` must be concrete enough to resume without asking questions
- If the methodology declares a verification field such as `done_when`, it must be verifiable: a command that succeeds, a result that appears, a test that passes
- If any required field is vague, rewrite it to be specific

### Quality examples

**next_step bad**: "Continue with phase 3" / "Keep working on the project"
**next_step good**: "Implement UserAuth.validate_token(): add JWT verification with RS256, endpoint POST /auth/refresh"

**verification field bad**: "When it's ready" / "When it works"
**verification field good**: "Build succeeds + checkout flow in staging returns order confirmation with correct total"

## Step 4 - Write artifacts

Use the `pith-writer` subagent for parallel writes when updating multiple artifacts:

1. Prepare the content for each artifact (main agent does this, it has the context)
2. For each artifact, delegate the write to a pith-writer subagent with: artifact name, prepared content, provider write instructions. Use MAPPING_BOOT.md for hybrid providers when available; use the provider's full MAPPING.md for `markdown-files` or when MAPPING_BOOT is absent.
3. Wait for all writers to confirm success
4. If any write fails, report the failure

If pith-writer is not available, or if the provider requires external MCP tools that are not available to the writer subagent, write artifacts sequentially from the main agent.

## Step 5 - Supplementary updates

1. **Work unit index metadata**: If the entry point artifact was updated, update the work unit index's `Last updated` metadata too. For `markdown-files`, update the `_INDEX.md` row. For hybrid providers, update the Project Index task/database row metadata according to the provider mapping. This keeps no-argument boot/status fast without reading every entry point.
2. **Module context**: If any module code was modified, update its context file. This is MANDATORY.
3. **LESSONS_LEARNED**: If any reusable technical finding was discovered (not project-specific), add it.
4. **PROVIDER_CACHE**: If any new entities were created and the provider uses `pith-framework/PROVIDER_CACHE.md`, update the cache file. Skip for `markdown-files`.

## Step 6 - Report

Tell the user:
- Which artifacts were updated (list them)
- Which artifacts were created (if any were new)
- The `next_step` and any verification field from the entry point artifact
- Any module contexts that were updated
- Any warnings (staleness, failed writes, etc.)

## Information routing

| Information type | Goes to |
|-----------------|---------|
| What a module does, patterns, traps | Module context file |
| Prior analysis, mappings, constraints | TECHNICAL_ANALYSIS |
| Phase plan, files, order | PLAN |
| Deliverable technical docs | TECHNICAL_REPORT |
| Project state, next step | Entry point artifact (`work_unit.entry_point`) |
| Project change history | CHANGELOG |
| Requirements, acceptance criteria | SPECIFICATIONS |
| Test plan, results | TESTING |
| Reusable technical lessons | LESSONS_LEARNED |
