# Methodologies

## What is a Methodology?

A **methodology** defines *how* work is organized and tracked within the framework. It determines:
- What a work unit is called (project, ticket, spec, etc.)
- What states a work unit goes through (PLANNING → IN_PROGRESS → RELEASED, etc.)
- What artifacts are produced (CURRENT_STATUS, PLAN, TECHNICAL_REPORT, etc.)
- When and how distillation happens (triggers, targets, checklists)
- Team conventions (naming, documentation language, formatting rules)

Methodologies are **pluggable** — the engine (ENGINE.md) defines the contract, and any methodology that satisfies the contract works.

## Included Methodologies

| Methodology | Description | Best for |
|-------------|-------------|----------|
| [default](default/) | Full-featured with 7 artifacts, 6 states, phase-based distillation | Most projects — features, integrations, refactors |
| [openspec](openspec/) | Spec Driven Development with acceptance criteria validation | Projects requiring formal specifications and validation |
| [kanban-lite](kanban-lite/) | Minimal — 3 states, 2 artifacts | Simple workflows, quick fixes, lightweight tracking |

## How to Use

1. Choose a methodology from the list above
2. Copy its `MANIFEST.yaml` to your project as `pith-framework/METHODOLOGY.yaml`
3. Customize the `conventions` section to match your team's preferences
4. The engine reads `METHODOLOGY.yaml` on every session startup (boot step 3)

## Engine Contract

Every methodology must satisfy the engine contract defined in `ENGINE.md` §6. Required fields:

| Field | Description |
|-------|-------------|
| `identity` | `name` and `version` |
| `work_unit` | `label`, `entry_point`, `entry_point_fields` (must include `last_updated` + `next_step`) |
| `states.values` | At least 1 `active` state + 1 `completed` state |
| `distillation.always_update` | Must include the entry point artifact |

Optional fields (with defaults): `boot_context`, `artifacts.standard`, `distillation.triggers` (default: `[user_request]`), `distillation.targets_by_phase`.

## Conventions Zone

Everything under the `conventions` key is a **free zone** — the engine ignores it but preserves it. This is where methodologies define:
- Documentation language
- Naming conventions
- Work modes (ad-hoc vs. project)
- Artifact content guides
- Entry point format templates
- Distillation checklists
- Anti-patterns

Artifact close-protocol behaviour (which artifacts survive when a work unit closes, which are discarded) is a methodology extension — declare it under `conventions.close_protocol` (lists like `survives`, `survives_if_present`, `discarded`). Do **not** mix it with the engine contract fields inside `artifacts.standard[]` — keep those lists to `name` and `required`.

### Resource Hints

The `resource_hints` section (under `conventions`) tells the agent **what to load before acting**, based on the type of task. This prevents the agent from guessing or inspecting external sources (databases, APIs) when documented information already exists.

```yaml
conventions:
  resource_hints:
    - when: "database query, SQL, table structure"
      load: "data_model/{relevant_category}"
      how: "Match keywords to categories in SYSTEM.yaml"
      note: "Always before executing any SELECT"
```

See `ENGINE.md` §5 for the lazy loading contract: documents marked `on_demand` without a trigger require the agent to ask the user before accessing external sources directly.

## Creating a Custom Methodology

1. Start from one of the included methodologies (or create from scratch)
2. Define at minimum the required contract fields (see above)
3. Add your conventions in the `conventions` zone
4. Save as `pith-framework/METHODOLOGY.yaml` in your project
5. The engine validates the contract on boot — if required fields are missing, the agent will inform you

**Tips:**
- Keep it simple — start with kanban-lite and add complexity only when needed
- The `conventions` zone is yours — add whatever your team needs
- `user_request` is always a distillation trigger (engine invariant) — you don't need to declare it, but you can
