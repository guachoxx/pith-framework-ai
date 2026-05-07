---
name: pith-close-project
description: "Close a completed project/work unit. Uses methodology close_protocol when configured, otherwise only proposes moving to a completed state. Destructive action, only invoke when explicitly requested."
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

From `pith-framework/METHODOLOGY.yaml`, read `conventions.close_protocol` if it exists:
- `survives` — artifacts always preserved (typically TECHNICAL_REPORT)
- `survives_if_present` — artifacts preserved only when they exist with content (typically CHANGELOG)
- `discarded` — artifacts removed or archived according to the methodology
- `actions` — per-artifact instructions (move, rename, delete)
- How to rename/archive the project container
- How to update the project task/entry in the index

If `conventions.close_protocol` does not exist, do not infer preservation or deletion rules. In that case, the only allowed close action is to propose changing the work unit state to the first `completed` state from `states.values` after explicit user confirmation.

### 2. Confirm with user

Before any destructive action, show the user:
- Project name and current state
- If close_protocol exists: artifacts that will be **preserved** (list them)
- If close_protocol exists: artifacts that will be **discarded** (list them)
- If close_protocol is absent: state clearly that no artifacts will be deleted or archived automatically
- Ask for explicit confirmation: "This will archive [project]. Proceed? (yes/no)"

Do NOT proceed without confirmation.

### 3. Preserve surviving artifacts

For each artifact in `survives` (and each in `survives_if_present` that actually has content):
- Keep it in place, or move per the `actions` section of `close_protocol`
- Typical defaults: TECHNICAL_REPORT stays as deliverable; CHANGELOG moves to changelog root if it has content

Skip this step if `close_protocol` is absent.

### 4. Discard non-surviving artifacts

For each artifact in `discarded`:
- Apply the per-artifact action from `close_protocol.actions` (typically: rename with suffix like `_ARCHIVADO`, or delete)

Skip this step if `close_protocol` is absent.

### 5. Update project state

- Change the work unit state to the first state in `states.values` with `type: completed`
- If `close_protocol` defines container rename/archive actions, apply them after confirmation
- Update the work unit index entry

### 6. Clean cache

- If the provider uses `pith-framework/PROVIDER_CACHE.md`, remove project-specific entries and keep infrastructure/reference document entries
- For `markdown-files`, skip cache cleanup

### 7. Module context

- Do NOT delete or archive module context files, they describe code, not projects
- Module context persists across all projects (`module_context: maintain_always`)

### 8. Report

Tell the user: project closed (name, final state), preserved artifacts if any, discarded artifacts if any, whether cache cleanup applied, module contexts unchanged.
