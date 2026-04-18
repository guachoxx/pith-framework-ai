# Pith Framework — Claude Code Plugin

Extensions for the Pith Framework: skills, subagents, and hooks that make the framework faster, more reliable, and easier to use with Claude Code.

## What's included

### Skills (slash commands)

| Command | What it does |
|---------|-------------|
| `/pith-boot [project]` | Initialize session. Without args: loads config + shows active projects. With project name: enters project context immediately. |
| `/pith-consolidate` | Distill session into memory artifacts. Reads methodology, identifies phase, updates the right documents. |
| `/pith-status [project]` | Show active projects or a specific project's current status. |
| `/pith-new-project <name>` | Create a new project following the active methodology. |
| `/pith-close-project <name>` | Close a completed project following the close protocol. |

### Subagents

| Agent | What it does |
|-------|-------------|
| `pith-writer` | Writes prepared content to framework artifacts via the provider. Used by `/pith-consolidate` for parallel writes. |
| `pith-explorer` | Explores codebase with documentation context loaded first (docs-before-code principle). Returns structured findings. |

### Hooks

| Hook | When | What it does |
|------|------|-------------|
| docs-before-code | PreToolUse (Grep/Glob) | Advisory non-blocking reminder of the docs-before-code invariant from ENGINE.md §5 before exploring code. |
| auto-distill-reminder | PreCompact | Warns before context compaction if work hasn't been distilled. |
| notify-on-stop | Stop | Desktop notification when a long task completes. |

## Installation

### Option A — Copy to your project

```bash
# Skills and agents
cp -r extensions/claude-code/plugin/src/skills/*  your-project/.claude/skills/
cp -r extensions/claude-code/plugin/src/agents/*  your-project/.claude/agents/

# Hooks — configure via /hooks in Claude Code (see extensions/claude-code/plugin/src/hooks/hooks.json)
```

### Option B — Selective

Copy only what you want. Skills and agents work independently — though `/pith-consolidate` benefits from `pith-writer` for parallel writes.

## Prerequisites

- Pith Framework installed in your project (AGENTS.md, CONFIG.md, METHODOLOGY.yaml, SYSTEM.yaml)
- Claude Code v2.1+

## Notes

- All skills use the `pith-` prefix. Type `/pith-` in Claude Code to see all available commands.
- Skills read your METHODOLOGY.yaml to determine states, artifacts, and conventions. They work with any methodology that follows the engine contract.
- `/pith-new-project` and `/pith-close-project` have `disable-model-invocation: true` — Claude will never trigger them automatically. They must be invoked explicitly via slash command, as they are destructive operations (create/delete project structure).
- These extensions don't modify the framework core (ENGINE.md, METHODOLOGY.yaml, SYSTEM.yaml). The framework works without them.
