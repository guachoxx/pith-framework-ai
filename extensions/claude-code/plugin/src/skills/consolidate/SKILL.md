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
3. **Staleness check**: If `last_updated` in the entry point exceeds `conventions.staleness.threshold_hours`, warn the user: the entry point may not reflect reality. Ask whether to proceed with consolidation or re-read the entry point first.
4. Map the state to a distillation phase:
   - PLANNING state = `analysis` or `planning` phase
   - IN_PROGRESS state = `development` phase
   - TESTING state = `testing` phase
5. **If the state has no matching phase** in `distillation_checklist` (e.g., ON_HOLD, READY, or a custom state): warn the user, then consolidate `distillation.always_update` only (typically CURRENT_STATUS). Do not guess which artifacts to update.
6. Look up `distillation_checklist` for the identified phase
7. Include everything in `distillation.always_update` (always includes the entry point)

## Step 2 - Prepare content for each target

For each artifact in the target list, determine what to write based on the session work.

**Priority levels** (from the distillation checklist):
- `always`: MUST update regardless of what happened
- `primary`: Main artifact for this phase, update with core work
- `if_applies`: Update only if relevant work was done
- `if_changes`: Update only if code changes were made
- `mandatory_if_modified`: MUST update if the module code was changed

### Distillation checklist by phase

**Analysis**: TECHNICAL_ANALYSIS (primary: findings, code, constraints), SPECIFICATIONS (if_applies: requirements), CURRENT_STATUS (always)

**Planning**: PLAN (primary: phases, files, order, dependencies), TECHNICAL_ANALYSIS (if_applies: enrich), CURRENT_STATUS (always)

**Development**: CURRENT_STATUS (always), TECHNICAL_REPORT (primary: classes, methods, decisions), CHANGELOG (if_changes), LESSONS_LEARNED (if_applies: reusable only), module context (mandatory_if_modified)

**Testing**: TESTING (primary: results, environment comparison), TECHNICAL_REPORT (if_applies: corrections), CURRENT_STATUS (always)

## Step 3 - Update CURRENT_STATUS (always)

Update the entry point using `conventions.entry_point_format.template`:

```
**Last updated**: [today YYYY-MM-DD]
**Last session summary**: [1-2 sentences of what was done]
**Next step**: [concrete action to resume, NOT "continue development"]
**Done when**: [verifiable condition: a command, a result, a test]

## Done
- Completed items (cumulative)

## In Progress
- Partially done + exact state

## Next Steps
- [ ] Pending, ordered by priority

## Blockers
- (if any)
```

**Quality check** before writing:
- `next_step` must be concrete enough to resume without asking questions
- `done_when` must be verifiable: a command that succeeds, a result that appears, a test that passes
- If either is vague, rewrite it to be specific

### Quality examples

**next_step bad**: "Continue with phase 3" / "Keep working on the project"
**next_step good**: "Implement UserAuth.validate_token(): add JWT verification with RS256, endpoint POST /auth/refresh"

**done_when bad**: "When it's ready" / "When it works"
**done_when good**: "Build succeeds + checkout flow in staging returns order confirmation with correct total"

## Step 4 - Write artifacts

Use the `pith-writer` subagent for parallel writes when updating multiple artifacts:

1. Prepare the content for each artifact (main agent does this, it has the context)
2. For each artifact, delegate the write to a pith-writer subagent with: artifact name, prepared content, provider write instructions (from MAPPING_BOOT.md)
3. Wait for all writers to confirm success
4. If any write fails, report the failure

If pith-writer is not available, write artifacts sequentially.

## Step 5 - Supplementary updates

1. **Module context**: If any module code was modified, update its context file. This is MANDATORY.
2. **LESSONS_LEARNED**: If any reusable technical finding was discovered (not project-specific), add it.
3. **PROVIDER_CACHE**: If any new entities were created in the provider, update the cache file.

## Step 6 - Report

Tell the user:
- Which artifacts were updated (list them)
- Which artifacts were created (if any were new)
- The next_step and done_when from CURRENT_STATUS
- Any module contexts that were updated
- Any warnings (staleness, failed writes, etc.)

## Information routing

| Information type | Goes to |
|-----------------|---------|
| What a module does, patterns, traps | Module context file |
| Prior analysis, mappings, constraints | TECHNICAL_ANALYSIS |
| Phase plan, files, order | PLAN |
| Deliverable technical docs | TECHNICAL_REPORT |
| Project state, next step | CURRENT_STATUS |
| Project change history | CHANGELOG |
| Requirements, acceptance criteria | SPECIFICATIONS |
| Test plan, results | TESTING |
| Reusable technical lessons | LESSONS_LEARNED |
