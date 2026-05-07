# Markdown Files Provider — Setup

> This is the default provider. Documents are stored as `.md` files in the project repository.

## Prerequisites

- A git repository (recommended but not required)
- An AI agent that can read/write local files (e.g., Claude Code, Cursor, Windsurf)

## Installation

### 1. Copy framework files to your project root

```
your-project/
├── AGENTS.md                          ← Universal entry point
├── CLAUDE.md                          ← Bridge for Claude Code → redirects to AGENTS.md
└── pith-framework/
    ├── framework/
    │   └── ENGINE.md                  ← Framework kernel (committed)
    ├── METHODOLOGY.yaml               ← Methodology rules (committed)
    ├── SYSTEM.yaml                    ← System documentation index (committed)
    ├── CONFIG.md                      ← Provider + user identity (gitignored)
    ├── ARCHITECTURE.md                ← Empty template
    ├── CREDENTIALS.md                 ← Credentials (gitignored)
    ├── BUILD_COMMANDS.md              ← Empty template
    ├── TESTING_METHODOLOGY.md         ← Empty template
    ├── LESSONS_LEARNED.md             ← Empty template
    └── projects/
        └── _INDEX.md                  ← Project index
```

Create `_INDEX.md` from `templates/PROJECT_INDEX.md.template`. The index must include the fast-path metadata used by boot/status:

```markdown
| Project | State | Owner | Last updated | Branch | Summary |
|---------|-------|-------|--------------|--------|---------|
```

`Last updated` is updated when the project's entry point is updated, so agents can list and sort active work units without reading every project document.

### 2. Edit AGENTS.md

Replace the `## System Overview` section with 3-5 lines about your system:

```markdown
## System Overview
E-commerce platform built with Next.js 14 + PostgreSQL + Stripe.
Monorepo with apps/web (frontend) and apps/api (backend).
Auth via NextAuth.js, deployed on Vercel.
```

### 3. Add to .gitignore

Append to your project's `.gitignore`:

```
pith-framework/CONFIG.md
pith-framework/CREDENTIALS.md
pith-framework/logs/
pith-framework/temp/
.claude/
```

### 4. Test it

Open your agent and say:

> "Read AGENTS.md and tell me what projects we have active."

The agent should navigate to `_INDEX.md` and report no active projects.

### 5. Create your first project

> "Create a project called `my-feature` in pith-framework/projects/"

### 6. Work and distill

Work normally. When done, say **"Consolidate"**. The agent updates the memory documents.

## Multi-User Setup (optional)

If multiple people use the agent on the same codebase:

### 1. Set `current_user` in CONFIG.md

Each user creates `pith-framework/CONFIG.md` from `templates/CONFIG.md.template` (gitignored) and sets their identity:

```markdown
# Memory Configuration
> Per-user, per-machine. This file is gitignored — do not commit.

## User
current_user: alice

## Provider
provider: markdown-files
```

Add `pith-framework/CONFIG.md` to `.gitignore` so each user keeps their own identity locally.

### 2. Create your user namespace

```
pith-framework/projects/
└── alice/
    └── _INDEX.md          ← Create from PROJECT_INDEX.md.template
```

### 3. Migration from single-user

If you already have projects in the flat `pith-framework/projects/` structure:
1. Create `pith-framework/projects/{your-name}/`
2. Move existing project folders into it
3. Move `_INDEX.md` into your user folder
4. (Optional) Create a new root `_INDEX.md` as a team overview

> When `current_user` is set, the agent automatically scopes all project operations to your namespace.

## How the Agent Accesses Documents

The agent reads and writes `.md` files directly via its native file tools. No additional configuration is needed.

## Directory Conventions

| Framework concept | Markdown-files implementation |
|---|---|
| Entry point | `AGENTS.md` at project root |
| Bridge (Claude Code) | `CLAUDE.md` → redirects to `AGENTS.md` |
| Framework kernel | `pith-framework/framework/ENGINE.md` |
| Methodology | `pith-framework/METHODOLOGY.yaml` |
| System index | `pith-framework/SYSTEM.yaml` |
| Configuration | `pith-framework/CONFIG.md` (.gitignored) |
| Reference documents | `pith-framework/*.md` |
| Project container | `pith-framework/projects/{project-name}/` |
| Project index | `pith-framework/projects/_INDEX.md` |
| Module context | `{module}/CLAUDE.md` |
| Project container (multi-user) | `pith-framework/projects/{username}/{project-name}/` |
| Project index (multi-user) | `pith-framework/projects/{username}/_INDEX.md` |
| Team overview (multi-user) | `pith-framework/projects/_INDEX.md` |
| Logs | `pith-framework/logs/` (.gitignored) |
| Temporary files | `pith-framework/temp/` (.gitignored) |
| Credentials | `pith-framework/CREDENTIALS.md` (.gitignored) |
