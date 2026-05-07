# Notion Provider — Setup

> Documents are stored as Notion Pages and Databases within a dedicated Teamspace. The agent accesses them via a Notion MCP server.

## Prerequisites

- A Notion workspace with permissions to create Teamspaces, Databases, and Pages
- A Notion integration (internal or public) with read/write access
- An AI agent that supports MCP (e.g., Claude Code)

## Notion Structure

Create the following structure in your Notion workspace:

```
Workspace
└── Teamspace: "Pith Memory" (or your project name)
    ├── Database: "Reference"                  ← Tier 2
    │   ├── Page (row): "ARCHITECTURE"
    │   ├── Page (row): "BUILD_COMMANDS"
    │   ├── Page (row): "TESTING_METHODOLOGY"
    │   ├── Page (row): "CREDENTIALS"          ← Restrict permissions
    │   └── Page (row): "LESSONS_LEARNED"
    └── Database: "Project Index"              ← Project containers
        ├── Page (row): "{project-name}"       ← Status + Assignee properties
        │   ├── Sub-page: "CURRENT_STATUS"
        │   ├── Sub-page: "SPECIFICATIONS"
        │   ├── Sub-page: "TECHNICAL_ANALYSIS"
        │   ├── Sub-page: "PLAN"
        │   ├── Sub-page: "CHANGELOG"
        │   ├── Sub-page: "TECHNICAL_REPORT"
        │   └── Sub-page: "TESTING"
        └── ...
```

> **Module Context** always lives on disk alongside the code as `{module}/CLAUDE.md`, regardless of provider. Agents read these files natively. They are NOT stored in Notion because they are code context, not project context.

## Step-by-step Setup

### 1. Create the Teamspace

Create a Teamspace named `Pith Memory` (or embed the structure within an existing Teamspace). This is the top-level container for all framework documents.

### 2. Create the Reference database

Inside the Teamspace, create a Database named `Reference` with:
- **Schema**: A single `title` property (e.g., `Name`)
- **Type**: Full-page database (not inline)

Create one page (row) for each reference document:
- ARCHITECTURE
- BUILD_COMMANDS
- TESTING_METHODOLOGY
- CREDENTIALS (restrict access — this is sensitive)
- LESSONS_LEARNED

Each document's content goes in the **page body** of its row.

> **Cross-provider naming note**: Notion preserves the canonical `UPPER_SNAKE_CASE` naming from the methodology. The ClickUp provider uses spaces instead (e.g., `BUILD COMMANDS`) because its search API doesn't match underscores — both map to the same abstract documents. See `providers/clickup/SETUP.md`.

### 3. Set up the Entry Point

**a) On disk — `AGENTS.md` (mandatory)**

Place `AGENTS.md` at your project root. This is the universal agent entry point. It must include:
- System overview
- Boot sequence (pointing to CONFIG.md, METHODOLOGY.yaml, SYSTEM.yaml, and PROVIDER_CACHE)
- On-disk resources table
- A note that reference and project documents live in Notion (with Teamspace name)

Optionally, create a bridge file for your agent (e.g., `CLAUDE.md` for Claude Code) that redirects to `AGENTS.md`.

**b) In Notion — team navigation (optional)**

You may optionally create a page within the Teamspace for humans to navigate the workspace. The agent's entry point is always the on-disk `AGENTS.md`.

### 4. Create the Project Index database

Inside the Teamspace, create a Database named `Project Index` with the following schema:

| Property | Type | Values |
|----------|------|--------|
| Name | Title | Project name (kebab-case) |
| Status | Select | `PLANNING`, `IN_PROGRESS`, `TESTING`, `READY`, `RELEASED`, `ON_HOLD` |
| Assignee | Person | Project owner |
| Last updated | Date | Fast-path listing/sorting metadata |

Each project is a **page (row)** in this database. Project documents (CURRENT_STATUS, PLAN, etc.) are created as **sub-pages** inside each project page.

Update `Last updated` whenever the project's entry point changes. This lets boot/status list and sort projects from the Project Index database without reading every project sub-page.

#### Database template (recommended)

Create a template in the Project Index database that pre-creates standard sub-pages:
- CURRENT_STATUS
- SPECIFICATIONS
- TECHNICAL_ANALYSIS
- PLAN
- CHANGELOG
- TECHNICAL_REPORT
- TESTING

When creating a new project, applying this template generates the complete document structure automatically.

### 5. Configure agent access

The agent needs a Notion MCP server to read/write pages and databases. Add a Notion MCP server to your agent's MCP configuration:

```json
{
  "mcpServers": {
    "notion": {
      "command": "npx",
      "args": ["-y", "<notion-mcp-server-package>"],
      "env": {
        "NOTION_API_KEY": "your-integration-token"
      }
    }
  }
}
```

> **Finding an MCP server**: Search the [MCP server registry](https://github.com/modelcontextprotocol/servers) or npm for a Notion MCP server. The configuration above is a template — replace `<notion-mcp-server-package>` with the actual package name.

### 6. Configure the framework

Create `pith-framework/CONFIG.md` at your project root (gitignored):

```markdown
# Memory Configuration
> Per-user, per-machine. This file is gitignored — do not commit.

## User
current_user: YourName

## Provider
provider: notion

## Connection
mcp_server: notion

## Notion Structure
teamspace_name: Pith Memory
reference_database: Reference
project_index_database: Project Index
```

### How the agent interacts with Notion

This is a **hybrid provider**: some documents live on disk, others in Notion.

| What the agent does | How it does it |
|---|---|
| Read entry point (`AGENTS.md`) | Native file read (on disk) |
| Read methodology + system index (METHODOLOGY.yaml, SYSTEM.yaml) | Native file read (on disk) |
| Read/update reference documents (ARCHITECTURE, etc.) | MCP tools: fetch/update Notion Pages |
| Read/update project documents (CURRENT_STATUS, etc.) | MCP tools: fetch/update Notion Pages (sub-pages) |
| Read/update project index | MCP tools: search/query Notion Database |
| Read/update module context | Native file read/write (on disk, always) |
| Read cached entity IDs | Native file read: `pith-framework/PROVIDER_CACHE.md` (on disk) |
| Create a new project | MCP tools: create Page in Database + create sub-pages |
| Close a project | MCP tools: update Status property, archive page |

The agent uses Notion MCP tools exactly like it uses file tools — the distillation protocol and lifecycle rules work identically.

### 7. Generate Provider Cache

Once the MCP server is configured and the Notion structure is in place, ask the agent to generate the cache:

> "Generate the provider cache for Notion"

The agent will query the Notion workspace, resolve all entity IDs (Teamspace, Databases, Pages), and write them to `pith-framework/PROVIDER_CACHE.md`. This file is gitignored and local to your machine.

**What this gives you**: On subsequent sessions, the agent reads the cache on startup and has instant access to all Notion IDs without making MCP search calls. This saves time and tokens.

**If you skip this step**: The agent will still work — it will generate the cache automatically the first time it needs to access Notion entities. The explicit step here just front-loads the generation.

### 8. Test it

Open your agent and say:

> "Read ARCHITECTURE from Notion and tell me what the system overview says."

The agent should follow the boot sequence: read AGENTS.md → CONFIG.md → METHODOLOGY.yaml → SYSTEM.yaml → PROVIDER_CACHE (or generate it) → Ready.

## Multi-User Setup (optional)

If multiple people use the agent on the same codebase and Notion workspace:

### 1. Set current_user in CONFIG.md

Each user sets their identity in their local `pith-framework/CONFIG.md` (which is gitignored):

```markdown
## User
current_user: Alice
```

The value must match the user's Notion display name or email so that the MCP server can resolve Person properties.

### 2. Use the Assignee property on Project Index

The `Assignee` (Person) property on the Project Index database identifies project ownership. When `current_user` is set, the agent:
- **Creates** new projects with Assignee = `current_user`
- **Filters** the Project Index by Assignee when listing "my projects"
- **Can read** all projects regardless of Assignee

### 3. Per-user filtered Views (recommended)

On the Project Index database, create a filtered View for each user:
- View name: `{username}'s Projects`
- Filter: Assignee = {username}

This keeps the Notion UI clean. It is optional — the agent filters programmatically regardless.

### 4. Migration from single-user

If you already have projects without Assignee set:
1. Set Assignee on existing Project Index rows
2. No structural changes needed — projects remain as sub-pages of their database rows

> When `current_user` is set, the agent automatically sets Assignee when creating projects. Unlike folder-based providers, no user subdirectories are needed — Notion's Person property handles ownership natively.

## Access Control

| Framework document | Notion permission |
|---|---|
| CREDENTIALS | Restricted page — limit sharing to workspace admins |
| All other documents | Normal workspace member access |

Notion handles permissions natively at the Teamspace, Database, or Page level.

## Notion-Specific Considerations

### Content format

Notion uses its own rich text format. When the agent updates pages via MCP tools, content is typically written in Markdown and converted by the MCP server. Verify your MCP server supports Markdown input for page content updates.

### Page vs. Database row

In Notion, every row in a database is a page. This means:
- Reference documents are pages with properties from the Reference database schema
- Project containers are pages with properties from the Project Index database schema
- Both have a page body where the actual content lives

### Sub-pages

Project documents (CURRENT_STATUS, PLAN, etc.) are sub-pages of the project page. They appear in the page body as linked child pages and are listed when fetching the parent page content.
