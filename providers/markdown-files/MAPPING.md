# Markdown Files Provider — Document Mapping

> How each framework concept maps to local `.md` files.

## Tier 1: Entry Point and Framework

| Framework document | Persisted as |
|---|---|
| Entry point | `AGENTS.md` at project root |
| Bridge (Claude Code) | `CLAUDE.md` → redirects to `AGENTS.md` |
| Framework kernel | `pith-framework/framework/ENGINE.md` |
| Methodology | `pith-framework/METHODOLOGY.yaml` |
| System index | `pith-framework/SYSTEM.yaml` |
| Configuration | `pith-framework/CONFIG.md` (gitignored, per-user) |

The agent reads `AGENTS.md` first on every session. It contains the system overview and boot sequence. Then reads `CONFIG.md`, `METHODOLOGY.yaml`, and `SYSTEM.yaml`.

## Tier 2: Reference Documents

| Framework document | Persisted as |
|---|---|
| Architecture | `pith-framework/ARCHITECTURE.md` |
| Build commands | `pith-framework/BUILD_COMMANDS.md` |
| Testing methodology | `pith-framework/TESTING_METHODOLOGY.md` |
| Credentials | `pith-framework/CREDENTIALS.md` (.gitignored) |
| Lessons learned | `pith-framework/LESSONS_LEARNED.md` |

## Tier 3: Module Context

| Framework document | Persisted as |
|---|---|
| Module context | `{module}/CLAUDE.md` (~50 lines max) |

One file per code module, placed alongside the code it describes.

## Project Containers

| Framework concept | Single-user | Multi-user |
|---|---|---|
| Project container | `pith-framework/projects/{project-name}/` | `pith-framework/projects/{username}/{project-name}/` |
| Project index | `pith-framework/projects/_INDEX.md` | `pith-framework/projects/{username}/_INDEX.md` |
| Team overview | (same as project index) | `pith-framework/projects/_INDEX.md` (optional) |

Naming: kebab-case for project directories (e.g., `auth-refactor/`, `api-migration/`).

## Project Documents

| Framework document | Persisted as |
|---|---|
| Current Status | `pith-framework/projects/{name}/CURRENT_STATUS.md` |
| Specifications | `pith-framework/projects/{name}/SPECIFICATIONS.md` |
| Technical Analysis | `pith-framework/projects/{name}/TECHNICAL_ANALYSIS.md` |
| Plan | `pith-framework/projects/{name}/PLAN.md` |
| Changelog | `pith-framework/projects/{name}/CHANGELOG.md` |
| Technical Report | `pith-framework/projects/{name}/TECHNICAL_REPORT.md` |
| Testing | `pith-framework/projects/{name}/TESTING.md` |

## Multi-User Mode

When `current_user` is set (via `pith-framework/CONFIG.md`), the project directory structure adds a user namespace:

```
pith-framework/projects/
├── _INDEX.md                              ← Team overview (optional)
├── alice/
│   ├── _INDEX.md                          ← Alice's project index
│   ├── auth-refactor/
│   │   ├── CURRENT_STATUS.md
│   │   ├── TECHNICAL_ANALYSIS.md
│   │   └── ...
│   └── api-migration/
│       └── ...
└── bob/
    ├── _INDEX.md                          ← Bob's project index
    └── checkout-fix/
        └── ...
```

The agent resolves all project paths using `current_user`. Cross-user references use the full path:
```markdown
See `pith-framework/projects/bob/api-migration/TECHNICAL_REPORT.md`
```

When `current_user` is NOT set, the structure is flat (single-user mode) — no user directories.

## Cross-references

Documents reference each other using relative file paths:
```markdown
See `pith-framework/ARCHITECTURE.md` → "System Overview"
```

## Version Control

- Changes are tracked via git (commits, branches, PRs)
- Credentials and logs are excluded via `.gitignore`
- All other memory documents are versioned with the codebase

## Read/Write Operations

The agent accesses documents natively through its file read/write tools. No MCP server or API integration required.

## Provider Cache

Not applicable. The markdown-files provider accesses all documents via native file tools — no entity IDs to cache. The `pith-framework/PROVIDER_CACHE.md` file is only used by external/hybrid providers.
