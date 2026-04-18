# ClickUp Provider — Setup

> Documents are stored as ClickUp Docs within a dedicated Space. The agent accesses them via the ClickUp MCP server.

## Prerequisites

- A ClickUp workspace with permissions to create Spaces, Folders, Lists, and Docs
- A ClickUp API token (personal or app token) OR a ClickUp MCP server
- An AI agent that supports MCP (e.g., Claude Code)

## ClickUp Structure

Create the following structure in your ClickUp workspace:

```
Workspace
└── Space: "Pith Memory"
    ├── Folder: "Reference"                    ← Tier 2 (reference documents)
    │   ├── Doc: "ARCHITECTURE"
    │   ├── Doc: "BUILD COMMANDS"
    │   ├── Doc: "TESTING METHODOLOGY"
    │   ├── Doc: "CREDENTIALS"                 ← Restrict permissions
    │   └── Doc: "LESSONS LEARNED"
    └── Folder: "Projects"                     ← Project containers
        ├── List: "Project Index"              ← One task per project
        └── Doc: "{project-name}"              ← One Doc per project
            ├── Page: "CURRENT STATUS"
            ├── Page: "SPECIFICATIONS"
            ├── Page: "TECHNICAL ANALYSIS"
            ├── Page: "PLAN"
            ├── Page: "CHANGELOG"
            ├── Page: "TECHNICAL REPORT"
            └── Page: "TESTING"
```

> **Key design decisions**:
> - **Reference documents** = individual Docs (one Doc, one Page each) inside the Reference folder.
> - **Project documents** = Pages inside a single multi-page Doc per project. ClickUp does not support nested Folders, so this is the native way to group project documents.
> - **Tier 3 (Module Context)** always lives on disk alongside the code as `{module}/CLAUDE.md`, regardless of provider.
> - **Naming: use SPACES, not underscores** — ClickUp search (`clickup_search`) cannot find Docs or Pages with underscores in their names. Use `LESSONS LEARNED`, not `LESSONS_LEARNED`. This is critical for cold start discovery.
> - **Cross-provider naming note**: the canonical reference-document names use `UPPER_SNAKE_CASE` (e.g., `LESSONS_LEARNED`). ClickUp's search limitation forces the space variant here. The Notion provider preserves the canonical form — both map to the same abstract documents. See `providers/notion/SETUP.md`.

## Step-by-step Setup

### 1. Create the Space

Create a Space named `Pith Memory` (or embed it in your existing project Space). This is the top-level container for all framework documents.

### 2. Create the Reference folder

Inside the Space, create a Folder named `Reference`. Create one Doc for each reference document:
- ARCHITECTURE
- BUILD COMMANDS
- TESTING METHODOLOGY
- CREDENTIALS (restrict access — this is sensitive)
- LESSONS LEARNED

### 3. Set up the Entry Point

Place `AGENTS.md` at your project root. This is the universal agent entry point. It must include:
- System overview
- Boot sequence (pointing to CONFIG.md, METHODOLOGY.yaml, SYSTEM.yaml, and PROVIDER_CACHE)
- On-disk resources table

Optionally, create a bridge file for your agent (e.g., `CLAUDE.md` for Claude Code) that redirects to `AGENTS.md`.

### 4. Create CONFIG.md

Create `pith-framework/CONFIG.md` from `templates/CONFIG.md.template` and fill in your settings. CONFIG.md is gitignored (it contains per-user configuration and may contain API keys).

```markdown
# Memory Configuration
> Per-user, per-machine. This file is gitignored — do not commit.
> See `providers/` for available providers and setup instructions.

## User
current_user: Your Name

## Provider
provider: clickup

## Connection
# Option 1: MCP server (preferred — auth handled by MCP config)
mcp_server: clickup

# Option 2: API key (if no MCP server available)
# api_key: pk_your_key_here

## ClickUp Structure
space_name: Pith Memory
reference_folder: Reference
projects_folder: Projects
project_index_list: Project Index
```

### 5. Create the Projects folder

Create a Folder named `Projects`. Inside it:

**a) Create the Project Index List**

Create a List named `Project Index`. Each project will have a task in this list.

**b) Configure statuses on the List (or Space)**

The Project Index must have statuses matching the framework's project lifecycle. Configure these **manually in the ClickUp UI** (statuses cannot be created via API):

| Status name   | Type   | Framework phase          |
| ------------- | ------ | ------------------------ |
| `PLANNING`    | Open   | Analysis + Planning      |
| `IN_PROGRESS` | Open   | Active development       |
| `TESTING`     | Open   | QA validation            |
| `READY`       | Open   | Pre-release              |
| `ON_HOLD`     | Open   | Temporarily paused       |
| `RELEASED`    | Closed | Completed, in production |

> **Note**: You can configure these at the Space level (applies to all Lists) or at the List level (override for Project Index only). Space-level is simpler if you don't use other Lists with different statuses.

**c) Creating projects**

Each project is a **Doc** (not a Folder) inside the Projects folder. The agent creates these via MCP tools:
- `clickup_create_document` → creates the project Doc
- `clickup_create_document_page` → creates each Page (CURRENT STATUS, PLAN, etc.)
- `clickup_create_task` → creates the Project Index entry with status and assignee

### 6. Configure agent access

The agent needs an MCP server to read/write ClickUp. Add it to your agent's MCP configuration (e.g., for Claude Code, `.claude/mcp.json` or global settings):

```json
{
  "mcpServers": {
    "clickup": {
      "command": "npx",
      "args": ["-y", "<clickup-mcp-server-package>"],
      "env": {
        "CLICKUP_API_TOKEN": "your-token-here"
      }
    }
  }
}
```

> **Finding an MCP server**: Search the [MCP server registry](https://github.com/modelcontextprotocol/servers) or npm for a ClickUp MCP server that supports reading/writing Docs and Pages, listing Folders, and managing List tasks.

Alternatively, set `api_key` in CONFIG.md if your setup accesses ClickUp directly without an MCP server.

### How the agent interacts with ClickUp

This is a **hybrid provider**: some documents live on disk, others in ClickUp.

| What the agent does | How it does it |
|---|---|
| Read entry point (`AGENTS.md`) | Native file read (on disk) |
| Read config (`CONFIG.md`) | Native file read (on disk, gitignored) |
| Read methodology + system index (METHODOLOGY.yaml, SYSTEM.yaml) | Native file read (on disk) |
| Read/update reference documents | MCP: `clickup_get_document_pages`, `clickup_update_document_page` |
| Read/update project Pages | MCP: `clickup_get_document_pages`, `clickup_update_document_page` |
| Read/update project index | MCP: `clickup_get_task`, `clickup_update_task` |
| Read/update module context | Native file read/write (on disk, always) |
| Read cached entity IDs | Native file read: `pith-framework/PROVIDER_CACHE.md` (on disk) |
| Create a new project | MCP: create Doc + Pages + task in Project Index |
| Close a project | MCP: update task status to RELEASED |

> **CRITICAL — `content_edit_mode`**: When calling `clickup_update_document_page`, **ALWAYS pass `content_edit_mode: "replace"` explicitly**. The tool's documented default is "replace" but the actual ClickUp API behavior defaults to "append", concatenating new content to existing content instead of replacing it.

### 7. Generate Provider Cache

Once the MCP server is configured and the ClickUp structure is in place, ask the agent to generate the cache:

> "Generate the provider cache for ClickUp"

The agent will query the ClickUp workspace, resolve all entity IDs (Space, Folders, Lists, Docs, Pages), and write them to `pith-framework/PROVIDER_CACHE.md`. This file is gitignored and local to your machine.

**What this gives you**: On subsequent sessions, the agent reads the cache on startup and has instant access to all ClickUp IDs without making MCP search calls.

**If you skip this step**: The agent will still work — it will generate the cache automatically the first time it needs to access ClickUp entities (cold start).

### 8. Test it

Open your agent and say:

> "Read ARCHITECTURE from ClickUp and tell me what the system overview says."

The agent should follow the boot sequence: read AGENTS.md → CONFIG.md → METHODOLOGY.yaml → SYSTEM.yaml → PROVIDER_CACHE (or generate it) → Ready.

## Multi-User Setup (optional)

If multiple people use the agent on the same codebase and ClickUp workspace:

### 1. Set current_user in CONFIG.md

Each user sets their identity in their local `CONFIG.md` (which is gitignored):

```markdown
## User
current_user: Alice
```

The value must be resolvable by the ClickUp MCP server's `clickup_resolve_assignees` tool (display name or email).

### 2. Project ownership via native Assignee

Project ownership is tracked via the **native Assignee** field on Project Index tasks (not a custom field). When `current_user` is set, the agent:
- **Creates** new tasks with Assignee = `current_user`
- **Filters** the Project Index by Assignee when listing "my projects"
- **Can read** all projects regardless of owner (freely accessible)

### 3. Create per-user Views (recommended)

On the `Project Index` List, create a filtered View for each user:
- View name: `{username}'s Projects`
- Filter: Assignee = {username}

This keeps the ClickUp UI clean. The agent filters programmatically regardless.

### Migration from single-user

If you already have projects without assignees:
1. Set `current_user` in your `CONFIG.md`
2. Assign existing Project Index tasks to the appropriate users
3. No structural changes needed — project Docs stay in the same location

## Access Control

| Framework document | ClickUp permission |
|---|---|
| CREDENTIALS | Restricted to workspace admins |
| All other documents | Normal workspace member access |

ClickUp handles permissions natively at the Space, Folder, or Doc level.
