---
name: pith-close-project
description: "Close a completed project following the close protocol. Preserves surviving artifacts, discards the rest, updates state, cleans cache. Destructive action, only invoke when explicitly requested."
disable-model-invocation: true
---

# Pith Close Project - Close Work Unit

Close a completed project following the methodology close protocol.

## Prerequisites

- Boot must be completed this session
- The project must exist and be in an active state

## Arguments

- `$ARGUMENTS` must contain the project name
- If no name provided, ask the user which project to close

## Steps

### 1. Read close protocol

From `pith-framework/METHODOLOGY.yaml`, read `conventions.close_protocol`:
- `survives` — artifacts always preserved (typically TECHNICAL_REPORT)
- `survives_if_present` — artifacts preserved only when they exist with content (typically CHANGELOG)
- `discarded` — artifacts removed (typically CURRENT_STATUS, SPECIFICATIONS, TECHNICAL_ANALYSIS, PLAN, TESTING)
- `actions` — per-artifact instructions (move, rename, delete)
- How to rename/archive the project container
- How to update the project task/entry in the index

### 2. Confirm with user

Before any destructive action, show the user:
- Project name and current state
- Artifacts that will be **preserved** (list them)
- Artifacts that will be **discarded** (list them)
- Ask for explicit confirmation: "This will archive [project]. Proceed? (yes/no)"

Do NOT proceed without confirmation.

### 3. Preserve surviving artifacts

For each artifact in `survives` (and each in `survives_if_present` that actually has content):
- Keep it in place, or move per the `actions` section of `close_protocol`
- Typical defaults: TECHNICAL_REPORT stays as deliverable; CHANGELOG moves to changelog root if it has content

### 4. Discard non-surviving artifacts

For each artifact in `discarded`:
- Apply the per-artifact action from `close_protocol.actions` (typically: rename with suffix like `_ARCHIVADO`, or delete)
- Typical defaults: TECHNICAL_ANALYSIS, PLAN, TESTING, CURRENT_STATUS, SPECIFICATIONS

### 5. Update project state

- Change the work unit state to the `completed` state (typically RELEASED)
- Update the project container name per close_protocol (typically add suffix like `_DONE`)
- Update the Project Index entry

### 6. Clean cache

- Remove project-specific entries from `pith-framework/PROVIDER_CACHE.md`
- Keep infrastructure and reference document entries

### 7. Module context

- Do NOT delete or archive module context files, they describe code, not projects
- Module context persists across all projects (`module_context: maintain_always`)

### 8. Report

Tell the user: project closed (name, final state), preserved artifacts, discarded artifacts, cache cleaned, module contexts unchanged.
