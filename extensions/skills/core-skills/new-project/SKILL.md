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
- `work_unit.entry_point`: which artifact resumes the work unit
- `work_unit.entry_point_fields`: fields that must exist in the entry point
- `states.values`: identify the first `active` state (initial state for new projects)
- `artifacts.standard`: if present, identify which artifacts have `required: true` (only these are created now)
- `conventions.entry_point_format.template`: if present, template for the entry point

### 2. Read config

From `pith-framework/CONFIG.md`:
- `current_user`: ownership assignment (if multi-user)

### 3. Read provider instructions

From the provider documentation loaded or available during boot:
- How to create a work unit in this provider
- How to create artifacts (pages, files, etc.)
- Where work units are stored

For hybrid providers, use MAPPING_BOOT.md plus the full MAPPING.md when needed. For `markdown-files`, use `providers/markdown-files/MAPPING.md`; there is no provider cache or MAPPING_BOOT file.

### 4. Create in provider

1. Create the work unit container (Doc, directory, etc. depending on provider)
2. Create the entry point artifact named in `work_unit.entry_point`.
3. If `conventions.entry_point_format.template` exists, use it to shape the initial content. If not, generate minimal content containing every field declared in `work_unit.entry_point_fields`. At minimum:
   ```
   **Last updated**: [today]
   **Next step**: [from user description, or "Define scope and requirements"]
   ```
   Add any additional declared fields with sensible initial values.
4. If `artifacts.standard` exists, create required artifacts (`required: true`) that are not already the entry point. If `artifacts.standard` is absent, create only the entry point.
5. Register in the work unit index: name, state (first active), owner (current_user if configured), `Last updated` (today), and any provider-specific summary/branch metadata.

### 5. Update cache

If the provider uses `pith-framework/PROVIDER_CACHE.md`, add the new work unit provider IDs. For `markdown-files`, skip this step.

### 6. Report

Tell the user: project created (name, state, owner), entry point created, where to find it, suggested next action.

## Do NOT

- Do NOT assume the entry point is named CURRENT_STATUS; use `work_unit.entry_point`
- Do NOT create all artifacts upfront, only the required ones (often just the entry point)
- Do NOT create artifacts marked `required: false`, they are created on demand when needed
- Do NOT guess the project name, if `$ARGUMENTS` is empty, ask the user
