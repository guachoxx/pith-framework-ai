---
name: local-agent
user-invocable: true
description: >
  MANDATORY delegation to a local LLM agent for token-heavy tasks. Runs on user hardware at zero API
  cost. You MUST use this skill instead of doing the work yourself or spawning Explore/general-purpose
  subagents whenever the task involves: reading multiple files to understand a codebase, searching for
  patterns or usages across files with grep, running tests and collecting results, analyzing git history
  (log, blame, diff), generating repetitive boilerplate code, listing and categorizing project files,
  or any exploration/grunt work that does not require deep multi-step reasoning. The local agent runs
  autonomously with tools (read/write files, execute commands, grep, git, search) and returns structured
  JSON results. Every time you are about to read more than 3 files to answer a question, or about to
  spawn an Explore agent, STOP and delegate to local-agent instead — it saves 45-55% of orchestrator
  tokens per session. Also triggers with: /local-agent, "delegate to local model", "use local LLM",
  "use Qwen", "use local agent", "run locally", "ask the local model", "offload this". If the local
  model server is not running, inform the user and fall back to normal operation.
---

# Local Agent — Delegate tasks to a local LLM

Offload work to a local LLM running on the user's hardware. The local model runs an autonomous
agent loop: it plans, calls tools (read files, run commands, search, git), reads results, iterates,
and returns a final answer. Works with any orchestrator agent — saves tokens and runs in parallel.

## When to delegate vs handle directly

**Good candidates for delegation:**
- Exploring a codebase (reading many files, understanding structure)
- Running tests and collecting results
- Searching for patterns, imports, usages across many files
- Generating boilerplate (models, CRUD endpoints, config files)
- Checking git history, blame, diffs
- Listing and categorizing project files
- Basic code review (find obvious bugs, security issues)

**Keep for the orchestrator:**
- Complex multi-step reasoning or architectural decisions
- Writing critical production code
- Tasks requiring deep context from the current conversation
- Anything the user explicitly asks the orchestrator to do personally
- Tasks requiring external integrations not available to the local agent

**Rule of thumb:** if the task is mostly about reading/searching code and doesn't need deep
reasoning, the local agent can handle it — and it costs zero API tokens.

## How to invoke

### Manual
The user provides the task directly (e.g., `/local-agent <task>`). Execute it immediately.

### Automatic
When the orchestrator detects a delegable task, it should briefly inform the user what it's
delegating and why, then run it. Example: "I'll have the local agent explore the project
structure while I work on the implementation."

## Execution

The agent script is located relative to this skill file at `scripts/local_agent.py`.
Resolve the absolute path from the skill's installation directory.

```bash
python3 <skill-dir>/scripts/local_agent.py \
  --task "your task description here" \
  --workdir "/path/to/project" \
  --verbose
```

Where `<skill-dir>` is the directory containing this SKILL.md file.

### Parameters
- `--task` (required): Clear, specific task description. Be precise about what you want.
- `--workdir` (required): The project directory to work in.
- `--api-url`: API endpoint (default: `http://127.0.0.1:1234/v1`, or `LOCAL_AGENT_API_URL` env var)
- `--model`: Model name (default: `qwen3-coder-next`, or `LOCAL_AGENT_MODEL` env var)
- `--max-iterations`: Max tool-use cycles (default: 15)
- `--timeout`: Command execution timeout in seconds (default: 30)
- `--verbose`: Print progress to stderr (recommended)
- `--allow-commands`: Enable `run_command` and `git` tools. **Disabled by default** — without this flag, the agent only has built-in tools (read_file, write_file, search_files, grep_files, list_directory). Pass this flag only when the task explicitly needs shell execution (running tests, builds, installs).
- `--system-prompt-file`: Path to a custom system prompt file. Use `{platform}` as placeholder for auto-detected OS. Overrides the built-in prompt.

### Running in background
The orchestrator can launch this script in the background and continue with other work.
Multiple agents can run in parallel — each as a separate process with different tasks.
Example: one exploring structure, another running tests, a third checking git history.

## Output format

The script outputs JSON to stdout:

```json
{
  "success": true,
  "result": "Final answer from the agent",
  "tools_used": [{"name": "search_files", "args": {"pattern": "**/*.py"}, "result_preview": "..."}],
  "iterations": 4,
  "tokens_used": {"prompt": 2400, "completion": 800, "total": 3200}
}
```

## Writing good task descriptions

The local model is capable but less reliable than you on complex reasoning. Help it succeed:

**Good tasks (specific, bounded):**
- "List all Python files in this project and describe the purpose of each based on its name and first 10 lines"
- "Run `pytest` and report which tests fail, including the error messages"
- "Find all functions that call `database.query()` and list them with file paths and line numbers"
- "Read the package.json and list all dependencies with their versions"

**For large files (>1000 lines):**
- "Use grep_files to find all public methods in LargeService.ts, then read only the method signatures with read_file offset/limit"
- "Find all SQL queries in the source files under src/services/ using grep_files, report file:line for each"
- Do NOT ask the agent to "read and analyze" a large file — tell it to grep first, then read sections

**Bad tasks (vague, unbounded):**
- "Understand this project" (too vague — what specifically?)
- "Refactor everything" (too broad, needs your judgment)
- "Fix the bug" (which bug? needs context from the conversation)
- "Read this 5000-line file and summarize it" (too large — tell it to grep for structure first)

## Interpreting results

When the agent returns:
1. **success: true** — Present the result to the user. Summarize if verbose, quote if concise.
2. **success: false** — Check the error. Common issues:
   - Connection refused: model server not running. Tell the user to start LM Studio/Ollama.
   - Max iterations: task was too complex. Break it down or handle it directly.
   - Tool errors: the agent hit a permission or path issue. Check workdir.
3. **Verify critical findings** — If the agent reports something important (security bug, test failures),
   verify independently before presenting it as fact. Local models can hallucinate.

## Configuration

Set these environment variables to change defaults:
- `LOCAL_AGENT_API_URL` — API base URL (default: `http://127.0.0.1:1234/v1`)
- `LOCAL_AGENT_MODEL` — Model identifier (default: `qwen3-coder-next`)
- `LOCAL_AGENT_MAX_ITERATIONS` — Max iterations (default: `15`)

## Available tools in the local agent

The local agent has access to these tools:
- **read_file** — Read file contents. Large files (>50KB) show first 100 lines + total count. Supports `offset`/`limit` params for reading sections of 200-500 lines at a time
- **write_file** — Create or overwrite files (full rewrite, no partial edits)
- **run_command** — Execute shell commands (destructive commands blocked, 30s timeout, output truncated at 10KB)
- **search_files** — Glob pattern file search (up to 500 matches). Use recursive globs (`**/`) first for full tree coverage
- **grep_files** — Regex search in file contents, skips binary files (up to 50 matches)
- **git** — Read-only git commands (log, diff, status, blame, show, branch, tag, ls-files)
- **list_directory** — List directory contents with sizes (up to 100 entries)

## Troubleshooting

If the agent can't connect:
1. Check if LM Studio is running: `curl http://127.0.0.1:1234/v1/models`
2. For Ollama: `curl http://localhost:11434/api/tags`
3. If using Ollama, set `--api-url http://localhost:11434/v1`
