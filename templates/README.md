# Framework Templates

Ready-to-copy templates for adopting Pith Framework in your project. Each `.template` file is a skeleton that gets hydrated (placeholders replaced with your project info) and placed at its target location.

## How to use

**Recommended** — agent-driven bootstrap. Open your AI agent in your project, point it at [`BOOTSTRAP.md`](../BOOTSTRAP.md) at the repo root, and it walks you through hydrating these templates conversationally.

**Manual** — copy each `.template` to the destination below, remove the `.template` extension, replace placeholders (`{{PROJECT_NAME}}`, `{{DESCRIPTION}}`, `{{STACK}}`), and fill in sections that apply.

## Templates at project root

| Template | Destination | Purpose |
|----------|-------------|---------|
| `AGENTS.md.template` | `AGENTS.md` | Universal entry point with boot sequence |
| `CLAUDE.md.template` | `CLAUDE.md` | Bridge for Claude Code (optional, safe to keep regardless of which agent you use) |
| `.gitignore.template` | Append to `.gitignore` | Entries for framework-managed gitignored files |

## Templates inside `pith-framework/` (the project's framework directory)

| Template | Destination | Purpose |
|----------|-------------|---------|
| `CONFIG.md.template` | `pith-framework/CONFIG.md` *(gitignored)* | Provider + user identity, connection settings |
| `SYSTEM.yaml.template` | `pith-framework/SYSTEM.yaml` | System documentation index (Layer 3) |
| `ARCHITECTURE.md.template` | `pith-framework/ARCHITECTURE.md` | System architecture, components, patterns |
| `BUILD_COMMANDS.md.template` | `pith-framework/BUILD_COMMANDS.md` | Build, run, test, deploy commands |
| `TESTING_METHODOLOGY.md.template` | `pith-framework/TESTING_METHODOLOGY.md` | Testing strategy, environments, debugging |
| `CREDENTIALS.md.template` | `pith-framework/CREDENTIALS.md` *(gitignored)* | API keys, connection strings, service accounts |
| `LESSONS_LEARNED.md.template` | `pith-framework/LESSONS_LEARNED.md` | Reusable technical findings from the project |

## About SYSTEM.yaml

`SYSTEM.yaml` is a **self-defined index** of the project's technical documentation (Layer 3 in the framework's 3-layer architecture). It tells the agent:

- What reference documents exist (ARCHITECTURE, BUILD_COMMANDS, etc.)
- Where to find them (file paths for markdown-files provider, or platform references for ClickUp/Notion)
- What module context files exist and their expected structure
- Optionally, the project's data model

**Independent of the methodology**: a methodology defines *how you work* (states, artifacts, distillation); `SYSTEM.yaml` defines *what documentation your system has*. You can swap methodology without touching SYSTEM.yaml.

**Index, not content**: SYSTEM.yaml points to documents, it doesn't contain them. The agent reads it on boot to discover what exists, then loads document content lazily only when needed.

## Empty reference-document templates

`ARCHITECTURE.md.template`, `BUILD_COMMANDS.md.template`, `TESTING_METHODOLOGY.md.template`, `CREDENTIALS.md.template`, and `LESSONS_LEARNED.md.template` are **empty skeletons with suggested section headings**. They're starting points, not mandatory layouts — fill them in as your project grows, keep or remove sections as needed.

These 5 templates cover the reference documents declared by the default methodology and referenced by every provider's `MAPPING.md`. Without them, the boot sequence finds dangling references in `SYSTEM.yaml`.
