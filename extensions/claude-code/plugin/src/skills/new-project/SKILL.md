---
name: pith-new-project
description: "Create a new project (work unit). Use when user says create project, new project, or wants to begin structured multi-session work. Destructive action, only invoke when explicitly requested."
disable-model-invocation: true
---

# Pith New Project - Create Work Unit

Create a new project following the active methodology and provider rules.

## Prerequisites

Boot must be completed this session. If not, run `/pith-boot` first.

## Arguments

- `$ARGUMENTS` should contain the project name (required) and optionally a description
- If no name provided, ask the user

## Steps

### 1. Read methodology

From `pith-framework/METHODOLOGY.yaml`:
- `work_unit.label`: what this work unit is called (project, spec, ticket)
- `states.values`: identify the first `active` state (initial state for new projects)
- `artifacts.standard`: identify which artifacts have `required: true` (only these are created now)
- `conventions.entry_point_format.template`: template for the entry point

### 2. Read config

From `pith-framework/CONFIG.md`:
- `current_user`: ownership assignment (if multi-user)

### 3. Read provider instructions

From the MAPPING_BOOT.md loaded during boot:
- How to create a work unit in this provider
- How to create artifacts (pages, files, etc.)
- Where work units are stored

### 4. Create in provider

1. Create the work unit container (Doc, directory, etc. depending on provider)
2. Create the entry point artifact (CURRENT_STATUS) with initial content:
   ```
   **Last updated**: [today]
   **Last session summary**: Project created
   **Next step**: [from user description, or "Define scope and requirements"]
   **Done when**: [from context, or "Scope documented in SPECIFICATIONS"]

   ## Done
   - Project created

   ## In Progress
   - (nothing yet)

   ## Next Steps
   - [ ] [appropriate first step based on project description]

   ## Blockers
   - None
   ```
3. Register in the Project Index: name, state (first active), owner (current_user)

### 5. Update cache

Add the new project provider IDs to `pith-framework/PROVIDER_CACHE.md`.

### 6. Report

Tell the user: project created (name, state, owner), entry point created, where to find it, suggested next action.

## Do NOT

- Do NOT create all artifacts upfront, only the required ones (typically just CURRENT_STATUS)
- Do NOT create artifacts marked `required: false`, they are created on demand when needed
- Do NOT guess the project name, if `$ARGUMENTS` is empty, ask the user
