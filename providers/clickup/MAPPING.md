# ClickUp Provider — Document Mapping

> How each framework concept maps to ClickUp entities.
> **Boot summary**: `MAPPING_BOOT.md` in this directory (loaded on every boot). This file is on-demand.

## ClickUp API Limitations

These constraints affect how the framework maps to ClickUp:

1. **No nested Folders** — ClickUp Folders cannot contain other Folders. Project containers cannot be sub-folders of a "Projects" folder.
2. **No custom field creation via API** — Custom fields must be created manually in the ClickUp UI. The framework uses native fields (Status, Assignee) instead of custom fields wherever possible.
3. **Docs support multiple Pages** — A single Doc can contain multiple Pages, each with independent content. This is the native way to group related documents.
4. **Search does not match underscores in Doc/Page names** — `clickup_search` cannot find Docs or Pages whose names contain underscores (e.g., `LESSONS_LEARNED`). Use spaces instead (e.g., `LESSONS LEARNED`). This affects cold start discovery and any search-based lookups.
5. **Search with keywords + location filter returns incomplete results** — `clickup_search` combining `keywords` with `location` filters (e.g., `location: {subcategories: [...]}`) may return 0 results even when items exist. To list all items in a location, use only the `location` filter without `keywords`.
6. **Editing existing Pages is not surgically safe by default** — `clickup_update_document_page` should not be treated as a block-level editor for long or historical Pages. In practice, `append` / `prepend` can behave destructively or semidestructively, so existing project Pages must be updated using a full-read / local-merge / full-replace workflow, followed by immediate verification.

## Entity Mapping Overview

| Framework concept | ClickUp entity |
|---|---|
| Reference document | Doc (single-page) in Reference folder |
| Project container | Doc (multi-page) in Projects folder |
| Project document (CURRENT STATUS, PLAN, etc.) | Page inside a project Doc |
| Project index | List with tasks (one task per project) |
| Project ownership | Native Assignee on Project Index task |
| Project status | Native Status on Project Index task/list |
| Cross-reference | Link between Docs or `@mention` |
| Module context | **On disk**: `{module}/CLAUDE.md` (not in ClickUp) |
| Entry point | **On disk**: `AGENTS.md` (with optional agent bridges like `CLAUDE.md`) |
| Framework files | **On disk**: `pith-framework/framework/ENGINE.md`, `pith-framework/METHODOLOGY.yaml`, `pith-framework/SYSTEM.yaml` |
| User configuration | **On disk**: `pith-framework/CONFIG.md` (gitignored) |

> **Hybrid provider**: Module context, configuration, and framework files always live on disk. Reference documents and project documents live in ClickUp. The entry point (`AGENTS.md`) lives on disk as the universal agent entry point.

### On-disk Files (ClickUp hybrid provider)

These files and directories persist on disk when using the ClickUp provider:

| Path | Git | Purpose |
|------|-----|---------|
| `AGENTS.md` | Committed | Universal entry point — the agent reads this on startup |
| `CLAUDE.md` | Committed | Bridge for Claude Code → redirects to `AGENTS.md` |
| `pith-framework/framework/ENGINE.md` | Committed | Framework kernel — primitive services and methodology contract |
| `pith-framework/METHODOLOGY.yaml` | Committed | Active methodology rules (states, artifacts, conventions) |
| `pith-framework/SYSTEM.yaml` | Committed | System documentation index |
| `pith-framework/CONFIG.md` | Gitignored | Provider config, user identity, connection |
| `pith-framework/PROVIDER_CACHE.md` | Gitignored | Cached ClickUp entity IDs (auto-generated) |
| `pith-framework/providers/` | Committed | Framework documentation (MAPPING, SETUP, README) |
| `pith-framework/scripts/permanent/` | Committed | Reusable scripts (extraction, testing, etc.) |
| `pith-framework/templates/` | Committed | Reusable templates (payloads, fixtures, etc.) |
| `pith-framework/logs/` | Gitignored | Working logs and debug output (temporary) |
| `pith-framework/temp/` | Gitignored | Temporary working files |
| `{module}/CLAUDE.md` | Committed | Module context (Tier 3) — one per code module |

> **Committed** = shared via git, part of the project. **Gitignored** = local to each machine, not shared.
> Implementations may add project-specific directories (e.g., additional log caches). Add them to `.gitignore` as needed.

### Consolidated View: On Disk vs. In ClickUp

```
ON DISK                                  IN CLICKUP
───────                                  ──────────
AGENTS.md (entry point)                  Space: "Pith Memory"
CLAUDE.md (bridge → AGENTS.md)           ├── Folder: "Reference"
pith-framework/                           │   ├── Doc: ARCHITECTURE
  ├── framework/ENGINE.md (committed)    │   ├── Doc: BUILD COMMANDS
  ├── METHODOLOGY.yaml (committed)       │   ├── Doc: TESTING METHODOLOGY
  ├── SYSTEM.yaml (committed)            │   ├── Doc: CREDENTIALS (restricted)
  ├── CONFIG.md (gitignored)             │   └── Doc: LESSONS LEARNED
  ├── PROVIDER_CACHE.md (gitignored)
  ├── providers/ (committed)
  ├── scripts/permanent/ (committed)
  ├── templates/ (committed)
  └── logs/, temp/ (gitignored)

{module}/CLAUDE.md (committed)
                                             ├── Doc: "{project-a}"
                                             │   ├── Page: CURRENT STATUS
                                             │   ├── Page: SPECIFICATIONS
                                             │   ├── Page: TECHNICAL ANALYSIS
                                             │   ├── Page: PLAN
                                             │   ├── Page: CHANGELOG
                                             │   ├── Page: TECHNICAL REPORT
                                             │   └── Page: TESTING
                                             └── Doc: "{project-b}"
                                                 └── Page: CURRENT STATUS
```

## Tier 1: Entry Point and Framework

| Component | Where | Purpose |
|---|---|---|
| `AGENTS.md` | **On disk**, project root | Universal entry point. Contains system overview, v2 boot sequence, and on-disk resources table. |
| `CLAUDE.md` | **On disk**, project root | Bridge for Claude Code → redirects to `AGENTS.md`. |
| `pith-framework/CONFIG.md` | **On disk**, gitignored | Provider type, connection settings, user identity. |
| `pith-framework/framework/ENGINE.md` | **On disk**, committed | Framework kernel — primitive services and methodology contract. |
| `pith-framework/METHODOLOGY.yaml` | **On disk**, committed | Active methodology rules (states, artifacts, distillation, conventions). |
| `pith-framework/SYSTEM.yaml` | **On disk**, committed | System documentation index (what docs exist and how to load them). |

The agent reads `AGENTS.md` → `CONFIG.md` → `METHODOLOGY.yaml` → `SYSTEM.yaml` → `PROVIDER_CACHE.md` on startup.

## Tier 2: Reference Documents

| Framework document | ClickUp entity | Location |
|---|---|---|
| Architecture | Doc: `ARCHITECTURE` | Reference folder |
| Build commands | Doc: `BUILD COMMANDS` | Reference folder |
| Testing methodology | Doc: `TESTING METHODOLOGY` | Reference folder |
| Credentials | Doc: `CREDENTIALS` | Reference folder (restricted) |
| Lessons learned | Doc: `LESSONS LEARNED` | Reference folder |

Each reference document is a single-page Doc (one Doc, one Page with the content).

## Tier 3: Module Context

| Framework document | Persisted as | Location |
|---|---|---|
| Module context | `{module}/CLAUDE.md` (~50 lines max) | **On disk**, alongside the code |

Module context **always lives on disk** regardless of provider. The agent reads these files natively when working on a module. They are code documentation, not project documentation — they belong with the code they describe.

## Project Containers

Each project is a **multi-page Doc** inside the Projects folder. All project documents (CURRENT STATUS, PLAN, etc.) are **Pages** within that Doc.

| Framework concept | ClickUp entity |
|---|---|
| Project container | Doc: `{project-name}` inside Projects folder |
| Project document | Page inside the project Doc |
| Project index entry | Task in "Project Index" List |

### Why Docs with Pages (not Folders with Docs)

ClickUp does not support nested Folders. The previous approach of "1 Folder per project inside a Projects folder" is impossible. Multi-page Docs are the native ClickUp solution:
- A project is self-contained in a single Doc
- Each document type is a Page within that Doc
- Navigation is natural in the ClickUp UI (sidebar shows Pages)
- API supports full CRUD on Pages: `clickup_create_document_page`, `clickup_update_document_page`, `clickup_get_document_pages`

### Project Index

Each project has a corresponding task in the "Project Index" List. This task uses **native ClickUp fields only** (custom fields cannot be created via API):

| Field | Type | Purpose |
|---|---|---|
| Status | **Native status** (configured on List/Space) | Project lifecycle status |
| Assignee | **Native assignee** | Project owner |
| Updated | **Native updated timestamp** (`dateUpdated`) | Fast-path `Last updated` metadata for listing/sorting |
| Description | **Native text** | Structured metadata (see format below) |

**Required statuses** (must be configured manually on the Project Index List or Space):

| Status | Framework phase | ClickUp status type |
|---|---|---|
| `PLANNING` | Analysis + Planning | Open |
| `IN_PROGRESS` | Development | Open |
| `TESTING` | QA validation | Open |
| `READY` | Pre-release | Open |
| `RELEASED` | Completed | Closed |
| `ON_HOLD` | Paused | Open |

**Task description format** for metadata that has no native field:

```
**Branch**: spike/feature-name
**Started**: YYYY-MM
**Summary**: One-line project description
```

Fast-path boot/status uses the Project Index task metadata for `Last updated` (the task's `dateUpdated` value). Do not read project Pages just to sort or list projects. When an agent updates a project's entry point, it should also touch/update the Project Index task metadata when practical so the fast-path timestamp remains meaningful.

**Recommended query pattern** to list all projects from the Project Index:

```
clickup_search(filters: {
  asset_types: ["task"],
  location: { subcategories: ["<project_index_list ID from PROVIDER_CACHE>"] }
})
```

Do NOT add `keywords` — see API Limitation #5. The location filter alone returns all tasks in the list.

## Project Documents

Each project document is a **Page** inside the project's Doc:

| Framework document | ClickUp entity | Location |
|---|---|---|
| Current Status | Page: `CURRENT STATUS` | Doc: `{project-name}` |
| Specifications | Page: `SPECIFICATIONS` | Doc: `{project-name}` |
| Technical Analysis | Page: `TECHNICAL ANALYSIS` | Doc: `{project-name}` |
| Plan | Page: `PLAN` | Doc: `{project-name}` |
| Changelog | Page: `CHANGELOG` | Doc: `{project-name}` |
| Technical Report | Page: `TECHNICAL REPORT` | Doc: `{project-name}` |
| Testing | Page: `TESTING` | Doc: `{project-name}` |

## Cross-references

ClickUp supports two mechanisms:
- **Doc links**: Embed links to other Docs using ClickUp's native linking
- **@mentions**: Reference Docs or tasks inline with `@`

Example in a Page:
```
See @ARCHITECTURE → "System Overview"
```

## Version Control

- ClickUp Docs maintain edit history natively
- For formal versioning, note the date and author at the top of each Page update
- CREDENTIALS Doc should have restricted permissions

## Read/Write Operations

The agent uses **two access methods** in this hybrid provider:

**On disk (native file tools):**
- Entry point (`AGENTS.md`) — read on every session startup
- Bridge (`CLAUDE.md`) — redirects to `AGENTS.md` (agent-specific)
- Methodology (`pith-framework/METHODOLOGY.yaml`) — read on startup
- System index (`pith-framework/SYSTEM.yaml`) — read on startup
- Engine (`pith-framework/framework/ENGINE.md`) — on demand (reference)
- Configuration (`pith-framework/CONFIG.md`) — read on startup for provider settings
- Provider cache (`pith-framework/PROVIDER_CACHE.md`) — read on startup for cached entity IDs
- Module context (`{module}/CLAUDE.md`) — read when working on a module

**In ClickUp (MCP tools):**

| Operation | MCP tool | Parameters |
|---|---|---|
| Read reference Doc | `clickup_get_document_pages` | `(doc_id, [page_id])` |
| Read project Page | `clickup_get_document_pages` | `(doc_id, [page_id])` |
| Update project Page | `clickup_update_document_page` | `(doc_id, page_id, content, content_format="text/md")` |
| Create new Page | `clickup_create_document_page` | `(doc_id, name, content, content_format="text/md")` |
| List Pages in a Doc | `clickup_list_document_pages` | `(doc_id)` |
| Create project Doc | `clickup_create_document` | `(name, parent={id, type="5"}, visibility, create_page)` |
| Read Project Index task | `clickup_get_task` | `(task_id)` |
| Update task status | `clickup_update_task` | `(task_id, status)` |
| Create task | `clickup_create_task` | `(name, list_id, assignees, description)` |

> **Performance note**: With a populated Provider Cache, the agent uses Doc IDs and Page IDs directly — no search or list calls needed. See "Provider Cache" section below.

### Safe Update Protocol for Existing Pages

For Pages with historical content (`CURRENT STATUS`, `PLAN`, `TESTING`, `TECHNICAL ANALYSIS`, etc.), the safe workflow is:

1. Read the full current Page with `clickup_get_document_pages`
2. Merge the intended changes locally against that exact content
3. Rewrite the complete Page once with `clickup_update_document_page(..., content_edit_mode="replace")`
4. Read the Page back immediately and verify the result before touching any other Page

Rules:
- Do **not** use `append` / `prepend` on existing historical Pages unless content loss would be acceptable
- Do **not** treat `clickup_update_document_page` as a surgical patch/diff primitive
- For high-value Pages, update them one at a time and verify each write before continuing
- If the final merged content has not been reconstructed yet, create a new support Page instead of risking a partial in-place edit

## Lite Mode

For small projects (fix, scoped refactor, <3 phases), create only:
- Page: `CURRENT STATUS` (with Analysis and Plan sections inline)
- Page: `CHANGELOG`

Both as Pages inside the project Doc. Promote to full structure if the project grows.

## Archiving Completed Projects

When a project reaches RELEASED status:
1. Keep `TECHNICAL REPORT`, `SPECIFICATIONS`, and `TESTING` Pages for reference
2. Update the task in `Project Index` to RELEASED status (closed)
3. Optionally archive or move the project Doc

---

## Provider Cache

### What Is Cached

Every ClickUp entity that the agent needs to access by ID is cached in `pith-framework/PROVIDER_CACHE.md`:

| Cached entity | ClickUp type | Why cached |
|---|---|---|
| Workspace | Workspace ID | Root of all API calls |
| Space | Space ID + name | Container for all framework content |
| Reference Folder | Folder ID | Contains all reference Docs |
| Each reference Doc | Doc ID + Page ID | Direct access to content |
| Projects Folder | Folder ID | Contains all project Docs |
| Project Index List | List ID | Where project tasks live |
| Each project Doc | Doc ID | Parent container for project Pages |
| Each project Page | Page ID | Direct read/write access |
| Each project task | Task ID | Direct status/assignee access |

### Cache Template

Use key-value format for token efficiency (no markdown tables):

```markdown
# Provider Cache (auto-generated)
> Do NOT edit manually. Regenerated on cold start.
> Provider: clickup | Last generated: YYYY-MM-DD

## Infrastructure
workspace: 12345678
space: 90123456 (Pith Memory)
reference_folder: fol456
projects_folder: fol789
project_index_list: lst012

## Reference Documents
ARCHITECTURE: doc=abc123 page=page001
BUILD_COMMANDS: doc=ghi012 page=page003
TESTING_METHODOLOGY: doc=jkl345 page=page004
CREDENTIALS: doc=mno678 page=page005
LESSONS_LEARNED: doc=pqr901 page=page006

## Projects

### auth-refactor
doc: doc111
task: tsk001
CURRENT_STATUS: pg101
PLAN: pg102
TECHNICAL_ANALYSIS: pg103

### api-migration
doc: doc222
task: tsk002
CURRENT_STATUS: pg201
CHANGELOG: pg202
```

> **Format rationale**: Key-value pairs consume fewer tokens than markdown tables and are equally parseable by the agent. Reference documents use `KEY: doc=X page=Y` (both IDs on one line since each ref doc is a single-page Doc). Project pages use bare `KEY: page_id` because the parent doc ID is already declared in the project header.

### How the Agent Uses the Cache

**Session startup (warm — cache exists)**:
1. Agent reads `AGENTS.md` (on disk) — or bridge file (e.g., `CLAUDE.md` → `AGENTS.md`)
2. Agent reads `pith-framework/CONFIG.md` (on disk)
3. Agent reads framework files: `METHODOLOGY.yaml`, `SYSTEM.yaml` (on disk)
4. Agent reads `pith-framework/PROVIDER_CACHE.md` (on disk) — all ClickUp IDs available
5. Ready to work. Reads a project's CURRENT STATUS only when the user asks.

**Session startup (cold — no cache)**:
1. Agent reads `AGENTS.md` + `CONFIG.md` + framework files
2. Agent discovers ClickUp structure (see "Initial Generation" below)
3. Agent generates `PROVIDER_CACHE.md`
4. Ready to work

**During work**:
- When the agent creates a new project Doc or Page → appends the new ID to the cache
- When a cached ID returns a 404/not-found error → the agent regenerates the entire cache

### Initial Generation Workflow

When the cache file does not exist, the agent generates it by querying ClickUp using settings from `CONFIG.md`:

1. `clickup_get_workspace_hierarchy` → find the Space by name (from CONFIG.md), get Folder IDs, List IDs
2. For the Reference Folder: `clickup_search` with `asset_types: ["doc"]` scoped to the folder → get reference Doc IDs
3. For each reference Doc: `clickup_list_document_pages` → get Page IDs
4. For the Projects Folder: `clickup_search` with `asset_types: ["doc"]` → get project Doc IDs
5. For each project Doc: `clickup_list_document_pages` → get Page IDs
6. Write the complete cache to `pith-framework/PROVIDER_CACHE.md`

### Update Triggers

| Action | Cache update |
|---|---|
| Create project (new Doc + Pages + task) | Append project row with Doc ID, Task ID, Page IDs |
| Create new Page in existing project | Update the project's Pages cell |
| Archive/close project | Remove the project row |
| Rename a project or Page | Update the affected row |
| Cached ID returns error | Regenerate entire cache |

---

## Multi-User Mode

When `current_user` is set in `CONFIG.md`, the agent uses the native Assignee field on Project Index tasks for ownership.

### How It Works

All project Docs live **flat** inside the Projects folder (no per-user sub-folders — ClickUp does not support nested Folders). Ownership is tracked via the task assignee:

```
Space: "Pith Memory"
├── Folder: "Reference"
└── Folder: "Projects"
    ├── List: "Project Index"
    │   ├── Task: "auth-refactor"    → Assignee: alice
    │   ├── Task: "checkout-fix"     → Assignee: bob
    │   └── Task: "api-migration"    → Assignee: alice
    ├── Doc: "auth-refactor"
    ├── Doc: "checkout-fix"
    └── Doc: "api-migration"
```

### Ownership Operations

When `current_user` is set, the agent:
- **Creates** new project tasks with Assignee = `current_user` (resolved via `clickup_resolve_assignees`)
- **Filters** the Project Index by Assignee when listing "my projects"
- **Can read** all projects regardless of owner (freely accessible)
- **Creates** project Docs directly inside the Projects folder

### Per-User Views (recommended)

Create a filtered View on the Project Index List for each user:
- View name: `{username}'s Projects`
- Filter: Assignee = {username}

This keeps the ClickUp UI clean. It is optional — the agent filters programmatically regardless.

### Mapping current_user to ClickUp Identity

The `current_user` value in `CONFIG.md` must be resolvable by the ClickUp MCP server. Use one of:
- ClickUp display name (e.g., `Alice`)
- ClickUp email (e.g., `alice@company.com`)

The agent calls `clickup_resolve_assignees` with the `current_user` value to get the ClickUp user ID for assignee operations.

### Single-User Fallback

When `current_user` is NOT set:
- Project Docs are created inside "Projects" folder (same structure)
- Project Index tasks have no Assignee
- Behaves identically to single-user mode
