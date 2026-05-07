# Changelog

## v2.0.1 — 2026-05-07

Canonical alignment and standalone skills.

### Changed
- Updated canonical GitHub references to `guachoxx/pith-framework-ai`.
- Aligned core skills with the engine methodology contract instead of default-methodology assumptions.
- Added fast paths for no-argument boot/status, including direct `_INDEX.md` resolution for `markdown-files`.
- Clarified `ENGINE.md` as contract source and `pith-boot` as procedural boot source when available.
- Updated default close protocol to preserve `TECHNICAL_REPORT`, `SPECIFICATIONS`, and `TESTING`.
- Reorganized `extensions/skills` into `core-skills` and `useful-skills` for standalone skill installation.

### Fixed
- Fixed stale raw GitHub URLs in `BOOTSTRAP.md`.
- Fixed ShopFast example `SYSTEM.yaml` and `AGENTS.md` to match current templates and boot semantics.
- Fixed provider/cache assumptions across `pith-boot`, `pith-status`, `pith-new-project`, `pith-close-project`, and `pith-consolidate`.
- Fixed `pith-writer`/`pith-explorer` instructions so they no longer assume unavailable MCP tools or fixed documentation layouts.

### Notes
- Standalone core skills mirror the Claude Code plugin skill sources and should remain synchronized.
- Full LLM trigger evals were not run; static and targeted validation checks were performed.

## v2.0 — 2026-04-18

Public release of Pith Framework.

**Architecture**:
- 3-layer: Engine (immutable) → Methodology (plugin) → System (self-defined).
- Agent-agnostic (universal `AGENTS.md` entry point), provider-agnostic (markdown, ClickUp, Notion, or custom), methodology-agnostic (pluggable via `METHODOLOGY.yaml` manifest).
- 3-phase boot: parallel config load → resource hints → ready, with a 6-row Boot Checklist that halts on any missing configuration.

**Engine (`ENGINE.md`)**:
- Primitive services: Boot Protocol, Persistence Layer, Retrieval Protocol, Namespace & Registry, Context Budget.
- Two-tier cache discipline: stable infrastructure/reference IDs vs. dynamic work-unit list; project discovery always queries the provider live.
- "Documentation-first exploration" invariant: REFERENCE docs are loaded before code is explored.
- Methodology contract with required fields + extensible free zone for conventions.
- Coexistence with native agent memories (framework prevails on conflict).

**Methodologies**:
- `default/MANIFEST.yaml` — 7 flexible artifacts, 6 states, phase-based distillation. Includes `workspace_rules`, `provider_operations` (reads in main agent, writes delegated to parallel subagents), MANDATORY rule in `persistence_rules` to consult provider docs, and 10 generic `resource_hints`.
- `openspec/MANIFEST.yaml` — spec-driven development.
- `kanban-lite/MANIFEST.yaml` — minimal workflow.

**Providers**:
- `markdown-files/` — local `.md` files, everything on disk.
- `clickup/` — hybrid storage with `MAPPING.md` (full, on-demand) and `MAPPING_BOOT.md` (lightweight boot summary loaded every session). 6 documented API limitations including search+location bug and unsafe page edits. Safe Update Protocol for existing pages. Recommended query pattern for Project Index. Lite Mode for minimal projects.
- `notion/` — hybrid storage.

**Templates** (all unified under `templates/`):
- **Project-root templates**: `AGENTS.md.template` (3-phase boot + Boot Checklist + invariants + context budget, all mirrored from `ENGINE.md` with source-of-truth attribution markers), `CLAUDE.md.template` (bridge for Claude Code), `.gitignore.template` (entries for framework-managed files).
- **Project-framework config**: `CONFIG.md.template` (provider + user identity), `SYSTEM.yaml.template` (Layer 3 system index).
- **Empty reference-document skeletons**: `ARCHITECTURE.md.template`, `BUILD_COMMANDS.md.template`, `TESTING_METHODOLOGY.md.template`, `CREDENTIALS.md.template`, `LESSONS_LEARNED.md.template` — starting points with suggested section headings, adopters fill them as the project grows. These close the contract declared by the markdown-files provider's SETUP (which always referenced these files as "empty templates").

**Setup**:
- `BOOTSTRAP.md` — agent-driven setup walkthrough at the canonical repo root. The user opens their AI agent in the workspace, asks it to read `BOOTSTRAP.md`, and the agent walks them through 4 phases (Discovery → Plan → Execute → Verify): asks a small set of questions, hydrates the `templates/` templates with project info, writes all files to the workspace, and verifies the Boot Checklist. Agent-agnostic (works with Claude Code, Cursor, Windsurf, Aider, GitHub Copilot, or any agent that reads markdown). Supports two source modes — cloned-repo or on-demand download from GitHub raw URLs.

**Extensions (Claude Code plugin)**:
- Plugin at `extensions/claude-code/plugin/src/` (v1.0).
- 5 skills: `pith-boot`, `pith-consolidate`, `pith-status`, `pith-new-project`, `pith-close-project` (last two gated with `disable-model-invocation: true`).
- 2 subagents: `pith-writer` (parallel writes), `pith-explorer` (docs-before-code).
- Hooks: `docs-before-code` (PreToolUse), `auto-distill-reminder` (PreCompact), `notify-on-stop` (Stop).
- Trigger evaluation suites for `boot`, `consolidate`, `status`.

**Example**:
- Complete ShopFast `auth-refactor` worked project in `example/`.

**Distribution docs**:
- `README.md` (root) — front door: pitch, install, architecture, comparison.
- `CHANGELOG.md` (root) — this file.
- `BOOTSTRAP.md` (root) — agent-driven install walkthrough.
- `ENGINE.md` (root) — framework kernel, on-demand reference.
- `docs/HUMANS_START_HERE.md` — daily workflow guide.
- License: Unlicense (public domain).

**Repository layout**:
- Top-level files: `README.md`, `BOOTSTRAP.md`, `ENGINE.md`, `CHANGELOG.md`, `LICENSE`, `.gitignore`.
- Top-level dirs: `docs/`, `templates/` (unified — replaces earlier `framework-templates/` + `system-templates/` split), `methodologies/`, `providers/`, `extensions/`, `example/`.

**Directory naming**:
- Framework directory is `pith-framework/` (agent-agnostic). Earlier drafts used `claude-memory/`, now superseded.
