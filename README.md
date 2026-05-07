# Pith Framework

A protocol for structured project memory across LLM agents.

> **TL;DR** — Pith turns project knowledge and your chosen methodology into an operating memory protocol for AI agents. Agents boot into the current project state, load the right context only when needed through `resource_hints`, and distill work back into durable artifacts. Continuity lives with your project, not inside a single chat or tool.

Pith is built around three portable layers: **what your project is** (`SYSTEM`), **how you work** (`METHODOLOGY`), and **where the information lives** (`PROVIDER`).

Pith gives your AI agent persistent, structured memory that survives across sessions. Instead of losing context when a conversation ends, the agent distills what it learned into versioned artifacts — and picks up exactly where it left off next time.

## What you actually get

**The pain it eliminates**: every new session, your agent forgets everything about your project — architecture, credentials, decisions made last week, what was half-done. You re-explain. Every time.

**With Pith, four things change:**

- **Your agent picks up where you left off.** `CURRENT_STATUS` tells it what was done, what's next, and what's blocked — so you don't have to.
- **The right context loads at the right moment.** `resource_hints` route the agent to the docs it needs before acting: architecture, module notes, API docs, build commands, testing strategy, credentials, or lessons learned. Boot stays small; work starts informed.
- **What your team knows becomes what every agent knows.** Reference docs (ARCHITECTURE, BUILD_COMMANDS, LESSONS_LEARNED) live in one place. Switch from Claude Code to Cursor and the context comes with you. Onboard a junior and their agent has the same context the senior's agent has.
- **Your methodology stops being oral tradition.** States, artifacts, distillation rules, and when-to-load-what conventions are declared in `METHODOLOGY.yaml` — the agent follows them automatically, even the new teammate's agent.

This is the difference between "the agent has docs somewhere" and "the agent knows which docs matter right now."

See the [example/](example/) directory for a real project mid-execution if you want to see this in practice before reading further.

## Why not just AGENTS.md?

`AGENTS.md` is the entry point — this framework is everything that comes after it: structured memory, lifecycle management, distillation protocol, and cross-session continuity.

## Three Axes of Agnosticism

| Axis | What it means | Examples |
|------|---------------|----------|
| **Agent-agnostic** | Works with any agent that can read text files | Claude Code, Cursor, Windsurf, Copilot, custom agents |
| **Provider-agnostic** | Documents can live anywhere | Local markdown files, ClickUp, Notion, or any custom backend |
| **Methodology-agnostic** | How you work is pluggable | Default (7 artifacts, 6 states), OpenSpec (spec-driven), Kanban-Lite (minimal), or your own |

## Providers

A **provider** determines where your framework documents live. Ships with 3:

| Provider | Storage | Best for |
|----------|---------|----------|
| **`markdown-files`** *(default)* | Local `.md` files in your repo | Solo developers, full offline access, docs versioned alongside code |
| **`clickup`** | Hybrid — framework files on disk, project docs as ClickUp Docs + Tasks | Teams already using ClickUp for project management |
| **`notion`** | Hybrid — framework files on disk, project docs as Notion pages | Teams already using Notion |

Adding a new provider (Linear, Jira, Google Docs, or your own) is a well-defined extension — see [`providers/README.md`](providers/README.md) for the contract.

## Methodologies

A **methodology** defines how work is organized (states, artifacts, distillation rules, conventions). Ships with 3:

| Methodology | Shape | Best for |
|-------------|-------|----------|
| **`default`** | 7 flexible artifacts (CURRENT_STATUS, PLAN, TECHNICAL_ANALYSIS, ...), 6 states (PLANNING → RELEASED) | Full-featured projects with structured phases |
| **`openspec`** | Spec-driven development | Projects where specifications precede implementation |
| **`kanban-lite`** | Minimal (just states + CURRENT_STATUS) | Simple task tracking, small teams |

Methodologies are plugins — the engine ignores their conventions and only validates a tiny contract (see [`ENGINE.md` §6](ENGINE.md)). You can write your own by satisfying the contract, or extend any existing one just by including your own conventions and rules in its **free zone**. See [`methodologies/README.md`](methodologies/README.md).

## Quick Start

**Agent-driven (recommended)**: open your AI agent in your project root and say:

> "Read [BOOTSTRAP.md](BOOTSTRAP.md) from Pith Framework and walk me through setup."

The agent asks a few questions (project identity, provider choice, etc.), generates the right files in your workspace from the `templates/` templates, and verifies the deployment with the Boot Checklist. Works with Claude Code, Cursor, Windsurf, Aider, GitHub Copilot, or any agent that reads markdown. Two source modes: clone the repo locally, or have the agent download templates on demand from GitHub raw URLs (configurable in the bootstrap).

**Manual (5-minute alternative)**: follow the steps below.

1. **Copy framework templates** to your project root:
   ```bash
   cp templates/AGENTS.md.template    your-project/AGENTS.md
   cp templates/CLAUDE.md.template    your-project/CLAUDE.md
   cp templates/CONFIG.md.template    your-project/pith-framework/CONFIG.md
   mkdir -p your-project/pith-framework/projects
   cp templates/PROJECT_INDEX.md.template your-project/pith-framework/projects/_INDEX.md
   cat templates/.gitignore.template >> your-project/.gitignore
   ```

2. **Copy framework files**:
   ```
   cp ENGINE.md                                  your-project/pith-framework/framework/ENGINE.md
   cp methodologies/default/MANIFEST.yaml        your-project/pith-framework/METHODOLOGY.yaml
   cp templates/SYSTEM.yaml.template             your-project/pith-framework/SYSTEM.yaml
   cp templates/ARCHITECTURE.md.template         your-project/pith-framework/ARCHITECTURE.md
   cp templates/BUILD_COMMANDS.md.template       your-project/pith-framework/BUILD_COMMANDS.md
   cp templates/TESTING_METHODOLOGY.md.template  your-project/pith-framework/TESTING_METHODOLOGY.md
   cp templates/CREDENTIALS.md.template          your-project/pith-framework/CREDENTIALS.md
   cp templates/LESSONS_LEARNED.md.template      your-project/pith-framework/LESSONS_LEARNED.md
   ```

3. **Replace placeholders across all copied templates** — `{{PROJECT_NAME}}`, `{{DESCRIPTION}}`, and `{{STACK}}` appear in several files (AGENTS.md, CLAUDE.md, SYSTEM.yaml, and the 5 empty reference-doc skeletons: ARCHITECTURE, BUILD_COMMANDS, TESTING_METHODOLOGY, CREDENTIALS, LESSONS_LEARNED). See [BOOTSTRAP.md](BOOTSTRAP.md) Phase 3 for the full substitution table.

4. **Edit `pith-framework/CONFIG.md`** — set your provider and user identity.

5. **Edit `pith-framework/SYSTEM.yaml`** — uncomment and fill in the documents that apply.

6. **Start working.** Open your agent. The boot sequence reads AGENTS.md → CONFIG.md → METHODOLOGY.yaml → SYSTEM.yaml → ready.

> **Want to see what a real project looks like?** Check out the [example/](example/) directory — a complete auth-refactor project mid-execution.
> **New to the framework?** Read [docs/HUMANS_START_HERE.md](docs/HUMANS_START_HERE.md) for the full guide on daily workflow, distillation, and project documents.

## Extensions

The framework can be used with plain repo files only, but `extensions/` provides optional agent-specific accelerators.

| Path | What it contains | Use when |
|------|------------------|----------|
| `extensions/claude-code/plugin/` | Claude Code plugin packaging: Pith skills, writer/explorer agents, hooks, and eval harness | You want the full Claude Code plugin experience |
| `extensions/skills/core-skills/` | Standalone copies of the core Pith skills: `boot`, `consolidate`, `status`, `new-project`, `close-project` | You want to install Pith skills directly into an agent skill directory without the Claude Code plugin |
| `extensions/skills/useful-skills/` | Optional general-purpose skills: `lm-studio-expert`, `local-agent`, `user-docs` | You want extra workflow helpers alongside Pith |

The `core-skills` copies mirror `extensions/claude-code/plugin/src/skills/`. Keep both in sync when changing core skill behavior.

To install standalone skills, copy the selected skill directories into your agent's skills directory (for example `$CODEX_HOME/skills` for Codex or `~/.claude/skills` for Claude Code).

## Repository Structure

```
├── README.md                           ← You are here
├── BOOTSTRAP.md                        ← Agent-driven setup walkthrough (read by your AI agent)
├── ENGINE.md                           ← Framework kernel (immutable)
├── CHANGELOG.md                        ← Version history
├── LICENSE                             ← Unlicense
├── docs/
│   └── HUMANS_START_HERE.md            ← Full guide for humans (daily workflow)
├── templates/                          ← Unified templates (hydrated by BOOTSTRAP or manually)
│   ├── README.md
│   ├── AGENTS.md.template              ← Entry point with boot sequence
│   ├── CLAUDE.md.template              ← Bridge for Claude Code
│   ├── CONFIG.md.template              ← Provider configuration (gitignored)
│   ├── SYSTEM.yaml.template            ← System documentation index
│   ├── ARCHITECTURE.md.template        ← Architecture skeleton
│   ├── BUILD_COMMANDS.md.template      ← Build/run/test commands skeleton
│   ├── TESTING_METHODOLOGY.md.template ← Testing strategy skeleton
│   ├── CREDENTIALS.md.template         ← Credentials skeleton (gitignored)
│   ├── LESSONS_LEARNED.md.template     ← Lessons learned skeleton
│   ├── PROJECT_INDEX.md.template       ← Empty markdown-files work unit index
│   └── .gitignore.template             ← Lines to add to .gitignore
├── methodologies/
│   ├── README.md                       ← What methodologies are, how to create one
│   ├── default/MANIFEST.yaml           ← Full-featured methodology
│   ├── openspec/MANIFEST.yaml          ← Spec Driven Development
│   └── kanban-lite/MANIFEST.yaml       ← Minimal workflow
├── providers/
│   ├── README.md                       ← How to choose and create providers
│   ├── markdown-files/                 ← Local .md files (default)
│   ├── clickup/                        ← ClickUp Docs and Tasks
│   └── notion/                         ← Notion Pages and Databases
├── extensions/
│   ├── claude-code/plugin/             ← Claude Code plugin (skills, agents, hooks, evals)
│   └── skills/                         ← Standalone skills
│       ├── core-skills/                ← Pith skills copied from the plugin source
│       │   ├── boot/
│       │   ├── consolidate/
│       │   ├── status/
│       │   ├── new-project/
│       │   └── close-project/
│       └── useful-skills/              ← Optional helper skills
│           ├── lm-studio-expert/
│           ├── local-agent/
│           └── user-docs/
└── example/                            ← Worked end-to-end project (ShopFast auth-refactor)
```

## Architecture

The framework has 3 layers:

| Layer | What | Where |
|-------|------|-------|
| **Engine** (immutable) | Primitive services: boot, persistence, retrieval, distillation contract | `ENGINE.md` — read on demand |
| **Methodology** (pluggable) | How work is organized: states, artifacts, conventions | `METHODOLOGY.yaml` — read on boot |
| **System Knowledge** (self-defined) | What your project has: reference docs, module context, data model | `SYSTEM.yaml` — read on boot |

The engine never changes. The methodology is chosen per team. System knowledge is defined per project or across the entire codebase.

## License

[Unlicense](LICENSE) — public domain. Use it however you want.
