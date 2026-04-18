# Notion Provider — Document Mapping

> How each framework concept maps to Notion entities.

## Notion API Considerations

These characteristics affect how the framework maps to Notion:

1. **Block-based content model** — Notion stores content as blocks, not raw Markdown. The MCP server handles conversion, but complex Markdown (nested lists, tables inside toggles) may not round-trip perfectly.
2. **Databases as containers** — Notion Databases serve as both containers and indexes. Each row is a page with properties (Status, Assignee) and a page body for content.
3. **Sub-pages for grouping** — Project documents are sub-pages of a project page. This is Notion's native way to group related content under a single database row.
4. **Person property for ownership** — Unlike folder-based providers, ownership is tracked via the native Person property on database rows. No per-user namespaces or subdirectories needed.

## Entity Mapping Overview

| Framework concept | Notion entity |
|---|---|
| Document (reference) | Page (row in Reference Database), content in page body |
| Document (project) | Sub-page of a project page |
| Container | Database |
| Project container | Page (row) in Project Index Database |
| Project index | Database with Status + Assignee properties |
| Reference | Page links or `@mention` |
| Module context | **On disk**: `{module}/CLAUDE.md` (not in Notion) |
| Entry point | **On disk**: `AGENTS.md` (with optional agent bridges like `CLAUDE.md`) |
| Framework files | **On disk**: `pith-framework/framework/ENGINE.md`, `pith-framework/METHODOLOGY.yaml`, `pith-framework/SYSTEM.yaml` |

> **Hybrid provider**: Module context, configuration, and framework files always live on disk. Reference documents and project documents live in Notion. The entry point (`AGENTS.md`) lives on disk as the universal agent entry point.

### Consolidated View: On Disk vs. In Notion

```
ON DISK                                  IN NOTION
───────                                  ─────────
AGENTS.md (entry point)                  Teamspace: "Pith Memory"
CLAUDE.md (bridge → AGENTS.md)          ├── Database: "Reference"
pith-framework/                           │   ├── Page (row): ARCHITECTURE
  ├── framework/ENGINE.md (committed)    │   ├── Page (row): BUILD_COMMANDS
  ├── METHODOLOGY.yaml (committed)      │   ├── Page (row): TESTING_METHODOLOGY
  ├── SYSTEM.yaml (committed)           │   ├── Page (row): CREDENTIALS (restricted)
  ├── CONFIG.md (gitignored)            │   └── Page (row): LESSONS_LEARNED
  ├── PROVIDER_CACHE.md (gitignored)

{module}/CLAUDE.md (committed)
                                       └── Database: "Project Index"
                                           ├── Page (row): "{project-name}"
                                           │   ├── Sub-page: CURRENT_STATUS
                                           │   ├── Sub-page: SPECIFICATIONS
                                           │   ├── Sub-page: TECHNICAL_ANALYSIS
                                           │   ├── Sub-page: PLAN
                                           │   ├── Sub-page: CHANGELOG
                                           │   ├── Sub-page: TECHNICAL_REPORT
                                           │   └── Sub-page: TESTING
                                           └── ...
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

| Framework document | Notion entity | Location |
|---|---|---|
| Architecture | Page (row): `ARCHITECTURE` | Reference database |
| Build commands | Page (row): `BUILD_COMMANDS` | Reference database |
| Testing methodology | Page (row): `TESTING_METHODOLOGY` | Reference database |
| Credentials | Page (row): `CREDENTIALS` | Reference database (restricted) |
| Lessons learned | Page (row): `LESSONS_LEARNED` | Reference database |

Each reference document is a row in the Reference database. The document name is the title property. The document content lives in the page body of the row.

## Tier 3: Module Context

| Framework document | Persisted as | Location |
|---|---|---|
| Module context | `{module}/CLAUDE.md` (~50 lines max) | **On disk**, alongside the code |

Module context **always lives on disk** regardless of provider. The agent reads these files natively when working on a module. They are code documentation, not project documentation — they belong with the code they describe.

## Project Containers

| Framework concept | Notion entity | Details |
|---|---|---|
| Project container | Page (row) in Project Index Database | Properties: Name, Status, Assignee |
| Project documents | Sub-pages of the project page | CURRENT_STATUS, PLAN, etc. |
| Project index | Project Index Database | Filterable by Status and Assignee |

### Project Index properties

| Property | Type | Maps to |
|---|---|---|
| Name | Title | Project name (kebab-case) |
| Status | Select: PLANNING, IN_PROGRESS, TESTING, READY, RELEASED, ON_HOLD | Project status |
| Assignee | Person | Project owner (multi-user mode) |

Each project is a page (row) in this database. This replaces `_INDEX.md`. Additional properties (Branch, Started, Summary) can be added as needed using Notion's native property types (Text, Date, Text).

## Project Documents

| Framework document | Notion entity | Location |
|---|---|---|
| Current Status | Sub-page: `CURRENT_STATUS` | Inside project page |
| Specifications | Sub-page: `SPECIFICATIONS` | Inside project page |
| Technical Analysis | Sub-page: `TECHNICAL_ANALYSIS` | Inside project page |
| Plan | Sub-page: `PLAN` | Inside project page |
| Changelog | Sub-page: `CHANGELOG` | Inside project page |
| Technical Report | Sub-page: `TECHNICAL_REPORT` | Inside project page |
| Testing | Sub-page: `TESTING` | Inside project page |

Project documents are **sub-pages** of the project row page. When the agent fetches the project page, sub-pages are listed in the page content as linked child pages, allowing the agent to discover and navigate to each document.

## Lite Mode

For small projects (fix, scoped refactor, <3 phases), create only:
- Sub-page: `CURRENT_STATUS` (with Analysis and Plan sections inline)
- Sub-page: `CHANGELOG`

Both inside the project page (row in Project Index). Promote to full structure if the project grows.

## Cross-references

Notion supports several mechanisms for cross-referencing:
- **Page mentions**: Reference other pages inline with `@page-name`
- **Page links**: Embed links to other pages using Notion's native linking
- **Inline references**: Text references pointing to document names

Example in a page:
```
See @ARCHITECTURE → "System Overview"
```

## Version Control

- Notion pages maintain edit history natively (page history feature)
- For formal versioning, note the date and author at the top of each page update
- CREDENTIALS page should have restricted sharing permissions instead of `.gitignore`

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

**In Notion (MCP tools):**
- Fetching page content (reference and project documents)
- Updating page content
- Creating new pages (when creating a project or document)
- Searching for pages and databases
- Querying database properties (for Project Index — reading statuses, assignees)
- Updating page properties (for Project Index — changing status)

> **Performance note**: With a populated Provider Cache, the agent skips the MCP search calls that would otherwise be needed to resolve entity IDs. See "Provider Cache" section below.

## Archiving Completed Projects

When a project reaches RELEASED status:
1. Update the Status property to `RELEASED` on the Project Index row
2. Optionally move `TECHNICAL_REPORT` sub-page to a documentation area
3. Archive the project page in Notion (or leave it in place with RELEASED status for reference)

## Provider Cache

### What Is Cached

Every Notion entity that the agent needs to access by ID is cached in `pith-framework/PROVIDER_CACHE.md`:

| Cached entity | Notion type | Why cached |
|---|---|---|
| Teamspace | Teamspace ID | Scoping for searches |
| Reference Database | Database ID + data source ID | Container for reference documents |
| Each reference page | Page ID | Direct access without searching |
| Project Index Database | Database ID + data source ID | Container for project entries |
| Each project page | Page ID | Direct navigation to project |
| Each project sub-page | Page ID | Direct read/write of project documents |

### Notion Cache Template

Use key-value format for token efficiency (no markdown tables):

```markdown
# Provider Cache (auto-generated)
> Do NOT edit manually. Regenerated on cold start.
> Provider: notion | Last generated: YYYY-MM-DD

## Infrastructure
teamspace: ts-xxxxx (Pith Memory)
reference_database: db-xxxxx
reference_datasource: collection://xxxxx
project_index_database: db-yyyyy
project_index_datasource: collection://yyyyy

## Reference Documents
ARCHITECTURE: page-xxxxx
BUILD_COMMANDS: page-xxxxx
TESTING_METHODOLOGY: page-xxxxx
CREDENTIALS: page-xxxxx
LESSONS_LEARNED: page-xxxxx

## Projects

### {project-name}
page: page-xxxxx
CURRENT_STATUS: page-xxxxx
PLAN: page-xxxxx
TECHNICAL_ANALYSIS: page-xxxxx
CHANGELOG: page-xxxxx
```

> **Format rationale**: Key-value pairs consume fewer tokens than markdown tables and are equally parseable by the agent.

### How the Agent Uses the Cache

**Session startup (warm — cache exists)**:
1. Agent reads `AGENTS.md` (on disk) — or bridge file (e.g., `CLAUDE.md` → `AGENTS.md`)
2. Agent reads `pith-framework/CONFIG.md` (on disk)
3. Agent reads framework files: `METHODOLOGY.yaml`, `SYSTEM.yaml` (on disk)
4. Agent reads `pith-framework/PROVIDER_CACHE.md` (on disk) — all Notion IDs available
5. Ready to work. Reads a project's CURRENT STATUS only when the user asks.

**Session startup (cold — no cache)**:
1. Agent reads `AGENTS.md` + `CONFIG.md` + framework files
2. Agent discovers Notion structure (see "Initial Generation" below)
3. Agent generates `PROVIDER_CACHE.md`
4. Ready to work

**During work**:
- When the agent creates a new project page or sub-page → appends the new ID to the cache
- When a cached ID returns a not-found error → the agent regenerates the entire cache

### Initial Generation Workflow (Cold Start)

When the cache file does not exist, the agent generates it by querying Notion:

1. `notion-search` for the Reference and Project Index databases → get Database IDs
2. `notion-fetch` each database → get data source IDs and schema
3. `notion-search` or fetch database pages → get all reference document Page IDs
4. For each project page in the Project Index → `notion-fetch` to discover sub-pages and their Page IDs
5. Optionally `notion-get-teams` → get Teamspace ID
6. Write the complete cache to `pith-framework/PROVIDER_CACHE.md`

### Update Triggers

| Action | Cache update |
|---|---|
| Create project (new page + sub-pages) | Append project section + Page IDs |
| Create new sub-page in existing project | Update the project's section |
| Archive/close project | Remove the project section |
| Rename a project or document | Update the affected entry |
| Cached ID returns error | Regenerate entire cache |

---

## Multi-User Mode

When `current_user` is set (via `pith-framework/CONFIG.md`), the Notion structure handles ownership through the **Assignee property** on the Project Index database:

```
Teamspace: "Pith Memory"
├── Database: "Reference"              ← Shared, team-level
└── Database: "Project Index"          ← Shared database with Assignee (Person) property
    ├── Page: "auth-refactor"          ← Assignee: Alice
    │   ├── Sub-page: CURRENT_STATUS
    │   └── ...
    └── Page: "checkout-fix"           ← Assignee: Bob
        └── ...
```

### No User Subdirectories Needed

Unlike folder-based providers, Notion's Person property handles ownership natively at the database level. There is no need for per-user folders or namespaces — the Assignee property on each project row provides filtering and ownership tracking.

### Shared Project Index with Assignee

The Project Index database is shared across all users. When `current_user` is set, the agent:
- **Creates** new projects with Assignee = `current_user`
- **Filters** the Project Index by Assignee when listing "my projects"
- **Can read** all projects (any Assignee) when asked to view another user's work
- **Must not write** to other users' projects (the agent enforces this)

### Per-User Views (recommended)

Create a filtered View on the Project Index database for each user:
- View name: `{username}'s Projects`
- Filter: Assignee = {username}

This keeps the Notion UI clean. It is optional — the agent filters programmatically regardless.

### Mapping current_user to Notion Identity

The `current_user` value must match the user's Notion display name or email so that the MCP server can resolve Person properties. The agent uses `notion-get-users` with the `current_user` value to verify the user exists in the workspace.

### Single-User Fallback

When `current_user` is NOT set:
- Projects are created without Assignee
- No filtering applied — all projects are listed
- Behaves identically to single-user mode
