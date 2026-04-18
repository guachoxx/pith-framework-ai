# Providers

## What is a Provider?

A **provider** is the persistence backend where the framework's documents are stored. The framework defines *what* information to maintain and *when* to update it — the provider defines *where* and *how* that information is persisted.

The framework is designed to be provider-agnostic. All core concepts (3-layer architecture, project documents, distillation protocol, lifecycle) work the same regardless of where documents live.

## Available Providers

| Provider | Description | Best for |
|----------|-------------|----------|
| [markdown-files](markdown-files/) | Local `.md` files in the repository | Solo developers, simple setups, full offline access |
| [clickup](clickup/) | ClickUp Docs and Tasks | Teams already using ClickUp for project management |
| [notion](notion/) | Notion Pages and Databases | Teams already using Notion for documentation |

## Hybrid Providers

Most external providers (ClickUp, Notion, etc.) are **hybrid**: some documents always live on disk, while the rest live in the external platform.

**Always on disk (regardless of provider):**
- **Entry point** (`AGENTS.md`) — Universal agent entry point. Must exist at the project root.
- **Agent bridge** (e.g., `CLAUDE.md` for Claude Code) — Redirects to `AGENTS.md`. Optional per agent.
- **Framework files** (`pith-framework/framework/ENGINE.md`, `pith-framework/METHODOLOGY.yaml`, `pith-framework/SYSTEM.yaml`) — Framework kernel, methodology rules, and system documentation index.
- **Configuration** (`pith-framework/CONFIG.md`) — Provider type, connection settings, user identity. Gitignored (per-user, may contain API keys).
- **Module context** (`{module}/CLAUDE.md`) — Code documentation co-located with the code. Read natively when working on a module.

**In the external platform:**
- Reference documents (ARCHITECTURE, BUILD COMMANDS, etc.)
- Project documents (CURRENT STATUS, TECHNICAL ANALYSIS, PLAN, etc.)
- Project index

The **markdown-files** provider is the only fully local provider — everything lives on disk. All other providers are hybrid by nature.

**Provider Cache (on disk, gitignored):**
- `pith-framework/PROVIDER_CACHE.md` — Auto-generated key-value file mapping framework document names to provider entity IDs. Eliminates redundant MCP lookups on session startup. Only used by hybrid/external providers. See the provider's `MAPPING.md` for cache template and rules.

## Choosing a Provider

Consider:
- **Where does your team already work?** — If you live in ClickUp, use the ClickUp provider. If you prefer everything in the repo, use markdown-files.
- **Collaboration needs** — External providers (ClickUp, Notion) offer real-time collaboration. Markdown files use git for collaboration.
- **Offline access** — Markdown files work offline. External providers require connectivity.
- **Agent access** — Agents can read/write local files natively. External providers require MCP servers or API integrations for agents to access them directly.

## Provider Structure

Each provider folder contains:

| File | Purpose |
|------|---------|
| `SETUP.md` | Step-by-step instructions to configure the provider |
| `MAPPING.md` | How each framework document maps to the provider's entities |

## Multi-User Support

When `current_user` is configured in `CONFIG.md`, each provider must handle project ownership. Each provider's `MAPPING.md` and `SETUP.md` document:
- How project ownership is tracked (assignee fields, filtered views, etc.)
- How `current_user` maps to the provider's identity system
- The migration path from single-user to multi-user

See `METHODOLOGY.yaml` → `conventions` for the methodology-level rules.

## Creating a New Provider

To add support for a new platform (Linear, Jira, Google Docs, etc.):

1. Create a folder under `providers/` with the platform name (kebab-case)
2. Create `SETUP.md` with configuration instructions
3. Create `MAPPING.md` with a complete mapping of:
   - Each framework document → platform entity type
   - Each container (project container, module context) → platform structure
   - Cross-references → how documents link to each other
   - The distillation workflow → how the agent reads/writes on the platform
4. Submit a PR

### Mapping Checklist

Your `MAPPING.md` must cover how the provider handles:

- [ ] **Entry point**: `AGENTS.md` — always on disk. State this explicitly.
- [ ] **Agent bridge**: Optional per agent (e.g., `CLAUDE.md` for Claude Code). State this explicitly.
- [ ] **Framework files**: `ENGINE.md`, `METHODOLOGY.yaml`, `SYSTEM.yaml` — always on disk. State this explicitly.
- [ ] **Configuration**: `pith-framework/CONFIG.md` — always on disk, gitignored. State this explicitly.
- [ ] **Reference documents**: ARCHITECTURE, BUILD COMMANDS, TESTING METHODOLOGY, CREDENTIALS, LESSONS LEARNED
- [ ] **Module context**: Always on disk as `{module}/CLAUDE.md`. State this explicitly.
- [ ] **Project containers**: How projects are organized
- [ ] **Project documents**: CURRENT STATUS, SPECIFICATIONS, TECHNICAL ANALYSIS, PLAN, CHANGELOG, TECHNICAL REPORT, TESTING
- [ ] **Project index**: How project metadata is tracked (status, ownership, branch)
- [ ] **Cross-references**: How documents point to each other
- [ ] **Read/write operations**: How the agent accesses documents (native file tools for on-disk, MCP/API for external)
- [ ] **Boot sequence**: How the agent discovers provider structure (warm start with cache, cold start without)
- [ ] **Version control**: How changes are tracked
- [ ] **Access control**: Credentials, permissions, sensitive documents
- [ ] **Multi-user**: How ownership is tracked, migration path from single-user
- [ ] **Provider Cache**: Cache template (key-value format), generation workflow, update triggers
- [ ] **Provider limitations**: API constraints that affect the mapping (e.g., no custom field creation, no nested containers)
