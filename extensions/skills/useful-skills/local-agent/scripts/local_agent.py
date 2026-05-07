#!/usr/bin/env python3
"""
local_agent.py — Autonomous agent loop using a local LLM via OpenAI-compatible API.

Connects to LM Studio, Ollama, or any OpenAI-compatible server. The model decides
which tools to call, the script executes them, and feeds results back until the
model produces a final answer (no more tool calls).

Usage:
    python local_agent.py --task "analyze this project" --workdir /path/to/project
"""

import argparse
import glob
import json
import os
import re
import subprocess
import sys
from itertools import islice
from pathlib import Path

try:
    import requests
except ImportError:
    sys.exit("Error: 'requests' package required. Install with: pip install requests")


# ---------------------------------------------------------------------------
# Security
# ---------------------------------------------------------------------------

DANGEROUS_PATTERNS = re.compile(
    r"(rm\s+-rf|rmdir\s+/s|del\s+/[sfq]|format\s+[a-z]:|drop\s+database|truncate\s+table|"
    r"shutdown|mkfs|dd\s+if=|>\s*/dev/sd|powershell.*-enc|Remove-Item.*-Recurse.*-Force)",
    re.IGNORECASE,
)

BINARY_EXTENSIONS = frozenset({
    ".exe", ".dll", ".so", ".dylib", ".bin", ".obj", ".o", ".a", ".lib",
    ".zip", ".tar", ".gz", ".bz2", ".7z", ".rar", ".jar", ".war",
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".ico", ".webp", ".svg",
    ".mp3", ".mp4", ".avi", ".mov", ".mkv", ".wav", ".flac",
    ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
    ".pyc", ".pyo", ".class", ".wasm",
    ".db", ".sqlite", ".mdb",
})


def _is_binary(filepath: str) -> bool:
    if Path(filepath).suffix.lower() in BINARY_EXTENSIONS:
        return True
    try:
        with open(filepath, "rb") as f:
            chunk = f.read(1024)
            return b"\x00" in chunk
    except OSError:
        return True


def _resolve_path(path: str, workdir: str) -> str:
    p = Path(path)
    if not p.is_absolute():
        p = Path(workdir) / p
    p = p.resolve()
    wd = Path(workdir).resolve()
    try:
        p.relative_to(wd)
    except ValueError:
        raise PermissionError(f"Access denied: {p} is outside workdir {wd}")
    return str(p)


# ---------------------------------------------------------------------------
# Tool implementations
# ---------------------------------------------------------------------------

def tool_read_file(path: str, offset: int = 0, limit: int = 0, *, workdir: str) -> str:
    resolved = _resolve_path(path, workdir)
    size = os.path.getsize(resolved)

    if offset > 0 or limit > 0:
        start = max(0, offset)
        # Enforce minimum chunk size of 200 lines to prevent wasteful small reads
        if 0 < limit < 200:
            limit = 200
        with open(resolved, "r", encoding="utf-8", errors="replace") as f:
            for _ in range(start):
                if f.readline() == "":
                    break
            if limit > 0:
                selected = list(islice(f, limit))
            else:
                selected = f.readlines()
        end = start + len(selected)
        # Get total line count efficiently
        with open(resolved, "r", encoding="utf-8", errors="replace") as f:
            total_lines = sum(1 for _ in f)
        return f"[lines {start+1}-{end} of {total_lines}, file size {size} bytes]\n" + "".join(selected)

    if size > 50 * 1024:
        with open(resolved, "r", encoding="utf-8", errors="replace") as f:
            preview = list(islice(f, 100))
            # Count remaining lines
            remaining = sum(1 for _ in f)
            total_lines = 100 + remaining
        return (f"File too large ({size} bytes, {total_lines} lines). Showing first 100 lines. "
                f"Use offset/limit to read sections of 200-500 lines at a time.\n\n" + "".join(preview))

    with open(resolved, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def tool_write_file(path: str, content: str, *, workdir: str) -> str:
    resolved = _resolve_path(path, workdir)
    os.makedirs(os.path.dirname(resolved), exist_ok=True)
    with open(resolved, "w", encoding="utf-8") as f:
        f.write(content)
    return f"File written: {resolved} ({len(content)} bytes)"


def tool_run_command(command: str, *, workdir: str, timeout: int = 30) -> str:
    if DANGEROUS_PATTERNS.search(command):
        return f"BLOCKED: potentially destructive command: {command}"
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True,
            cwd=workdir, timeout=timeout,
        )
        output = result.stdout
        if result.stderr:
            output += f"\n[stderr]\n{result.stderr}"
        if result.returncode != 0:
            output += f"\n[exit code: {result.returncode}]"
        return output[:10000] if output else "(no output)"
    except subprocess.TimeoutExpired:
        return f"Error: command timed out after {timeout}s"


def tool_search_files(pattern: str, path: str = ".", *, workdir: str) -> str:
    resolved = _resolve_path(path, workdir)
    matches = glob.glob(os.path.join(resolved, pattern), recursive=True)
    wd = Path(workdir).resolve()
    relative = [str(Path(m).relative_to(wd)) for m in matches[:500]]
    if not relative:
        return "No files found."
    return "\n".join(relative)


def tool_grep_files(pattern: str, path: str = ".", file_glob: str = "*", *, workdir: str) -> str:
    resolved = _resolve_path(path, workdir)
    results = []
    files = glob.glob(os.path.join(resolved, "**", file_glob), recursive=True)
    regex = re.compile(pattern, re.IGNORECASE)
    for filepath in files[:200]:
        if not os.path.isfile(filepath) or _is_binary(filepath):
            continue
        try:
            with open(filepath, "r", encoding="utf-8", errors="replace") as f:
                for i, line in enumerate(f, 1):
                    if regex.search(line):
                        rel = str(Path(filepath).relative_to(Path(workdir).resolve()))
                        results.append(f"{rel}:{i}: {line.rstrip()}")
                        if len(results) >= 50:
                            break
        except (OSError, UnicodeDecodeError):
            continue
        if len(results) >= 50:
            break
    return "\n".join(results) if results else "No matches found."


def tool_git(args: str, *, workdir: str, timeout: int = 30) -> str:
    allowed_subcommands = {"log", "diff", "status", "blame", "show", "branch", "tag", "shortlog", "ls-files"}
    parts = args.strip().split()
    if parts and parts[0] not in allowed_subcommands:
        return f"Error: git {parts[0]} not allowed. Read-only commands: {', '.join(sorted(allowed_subcommands))}"
    return tool_run_command(f"git {args}", workdir=workdir, timeout=timeout)


def tool_list_directory(path: str = ".", *, workdir: str) -> str:
    resolved = _resolve_path(path, workdir)
    entries = []
    for entry in sorted(os.listdir(resolved))[:100]:
        full = os.path.join(resolved, entry)
        kind = "dir" if os.path.isdir(full) else "file"
        size = os.path.getsize(full) if os.path.isfile(full) else ""
        entries.append(f"[{kind}] {entry}" + (f"  ({size} bytes)" if size else ""))
    return "\n".join(entries) if entries else "(empty directory)"


# ---------------------------------------------------------------------------
# Tool registry
# ---------------------------------------------------------------------------

COMMAND_TOOLS = {
    "run_command": {
        "fn": tool_run_command,
        "spec": {
            "name": "run_command",
            "description": "Execute a shell command. Destructive commands are blocked. Timeout: 30s. Output truncated at 10KB.",
            "parameters": {
                "type": "object",
                "properties": {"command": {"type": "string", "description": "Shell command to execute"}},
                "required": ["command"],
            },
        },
    },
    "git": {
        "fn": tool_git,
        "spec": {
            "name": "git",
            "description": "Run read-only git commands (log, diff, status, blame, show, branch, tag, ls-files).",
            "parameters": {
                "type": "object",
                "properties": {"args": {"type": "string", "description": "Git arguments (e.g. 'log --oneline -10')"}},
                "required": ["args"],
            },
        },
    },
}

TOOLS = {
    "read_file": {
        "fn": tool_read_file,
        "spec": {
            "name": "read_file",
            "description": "Read the contents of a file. For large files (>50KB), the first 100 lines are shown automatically with total line count. Use offset and limit to read specific ranges — minimum 200 lines per read, recommended 300-500 for efficiency.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path to read (relative to workdir)"},
                    "offset": {"type": "integer", "description": "Start reading from this line number (0-based). Use with limit for large files.", "default": 0},
                    "limit": {"type": "integer", "description": "Maximum number of lines to read. 0 means all lines.", "default": 0},
                },
                "required": ["path"],
            },
        },
    },
    "write_file": {
        "fn": tool_write_file,
        "spec": {
            "name": "write_file",
            "description": "Write content to a file. Creates parent directories if needed. Overwrites existing files completely.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path to write"},
                    "content": {"type": "string", "description": "Content to write"},
                },
                "required": ["path", "content"],
            },
        },
    },
    "search_files": {
        "fn": tool_search_files,
        "spec": {
            "name": "search_files",
            "description": "Find files matching a glob pattern. Use **/ for recursive. Example: '**/*.py'. Returns up to 500 matches. Use this FIRST for exhaustive listing tasks — one recursive glob covers the whole tree.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pattern": {"type": "string", "description": "Glob pattern (e.g. '**/*.py')"},
                    "path": {"type": "string", "description": "Starting directory (default: workdir)", "default": "."},
                },
                "required": ["pattern"],
            },
        },
    },
    "grep_files": {
        "fn": tool_grep_files,
        "spec": {
            "name": "grep_files",
            "description": "Search for a regex pattern in file contents. Returns matching lines with file:line: prefix. Skips binary files. Returns up to 50 matches.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pattern": {"type": "string", "description": "Regex pattern to search for"},
                    "path": {"type": "string", "description": "Starting directory (default: workdir)", "default": "."},
                    "file_glob": {"type": "string", "description": "Only search in files matching this glob (default: '*')", "default": "*"},
                },
                "required": ["pattern"],
            },
        },
    },
    "list_directory": {
        "fn": tool_list_directory,
        "spec": {
            "name": "list_directory",
            "description": "List files and directories in a path. Shows [file] or [dir] prefix with exact file sizes in bytes (e.g. '[file] app.py  (2340 bytes)'). This is the ONLY tool you need to get file sizes — do not use shell commands for this. Returns up to 100 entries sorted alphabetically.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Directory path (default: workdir)", "default": "."},
                },
            },
        },
    },
}


SYSTEM_PROMPT_TEMPLATE = """You are an autonomous coding agent. You have access to tools to explore and modify a codebase.

Platform: {platform}

Your workflow:
1. Understand the task and PLAN your strategy before making any tool calls. For listing/counting tasks, prefer search_files with recursive globs (**/) to get maximum coverage in one call, then list_directory only for directories where you need sizes
2. Use tools to explore the codebase as needed
3. Take action (write files, run commands) if the task requires it
4. When done, provide a clear summary of what you found or did

Important rules:
- Be efficient — don't read files you don't need. You have a LIMITED number of tool calls (iterations), so plan ahead
- Be precise — give exact file paths and line numbers when referencing code. Only report facts you can back with a specific line range — do not infer or classify without evidence
- NEVER create or delete files unless explicitly asked in the task description
- For large files: read_file shows the first 100 lines and total line count. You can safely read up to 500 lines per call using offset/limit params. Strategy for large files: use grep_files to locate relevant sections FIRST, then read_file with offset/limit to read those sections in chunks of 200-500 lines. Do NOT read 10 lines at a time — that wastes iterations
- You do NOT have access to shell commands by default. Use ONLY the built-in tools provided: read_file, write_file, search_files, grep_files, list_directory. These tools cover reading, writing, searching, and listing — do not attempt to use shell commands for any of these operations
- list_directory already provides exact file sizes in bytes — never try to get file sizes through any other method
- Verify work actually works before claiming done. If you counted items, recount them. If you classified something, confirm the evidence supports that classification
- ALWAYS provide a final answer. If you're running low on iterations, summarize what you've found so far rather than making more tool calls. A partial answer is better than no answer
- When the task is complete, respond with your final answer WITHOUT calling any more tools"""


def _detect_platform() -> str:
    if sys.platform == "win32":
        return "Windows (use PowerShell syntax for run_command, not Unix/bash)"
    elif sys.platform == "darwin":
        return "macOS (Unix shell)"
    else:
        return "Linux (Unix shell)"


# ---------------------------------------------------------------------------
# Agent loop
# ---------------------------------------------------------------------------

def call_llm(messages: list, api_url: str, model: str, active_tools: dict = None) -> dict:
    tools_dict = active_tools or TOOLS
    tools_spec = [{"type": "function", "function": t["spec"]} for t in tools_dict.values()]
    payload = {
        "model": model,
        "messages": messages,
        "tools": tools_spec,
        "tool_choice": "auto",
        "stream": False,
    }
    resp = requests.post(f"{api_url}/chat/completions", json=payload, timeout=600)
    if resp.status_code != 200:
        error_detail = resp.text[:500]
        raise RuntimeError(f"API returned {resp.status_code}: {error_detail}")
    return resp.json()


ALL_TOOLS = {**TOOLS, **COMMAND_TOOLS}


def execute_tool(name: str, arguments: dict, workdir: str, timeout: int) -> str:
    if name not in ALL_TOOLS:
        return f"Error: unknown tool '{name}'"
    fn = ALL_TOOLS[name]["fn"]
    # Only pass timeout to tools that accept it
    kwargs = {"workdir": workdir}
    if name in ("run_command", "git"):
        kwargs["timeout"] = timeout
    # Filter arguments to only those the function accepts
    import inspect
    sig = inspect.signature(fn)
    valid_args = {k: v for k, v in arguments.items() if k in sig.parameters}
    try:
        return fn(**valid_args, **kwargs)
    except Exception as e:
        return f"Error executing {name}: {type(e).__name__}: {e}"


def run_agent(task: str, workdir: str, api_url: str, model: str,
              max_iterations: int, timeout: int, verbose: bool,
              system_prompt_file: str = None, allow_commands: bool = False) -> dict:
    platform = _detect_platform()

    # Build active tool set: base tools + command tools if opted in
    active_tools = dict(TOOLS)
    if allow_commands:
        active_tools.update(COMMAND_TOOLS)
        if verbose:
            print("[commands enabled: run_command + git available]", file=sys.stderr)

    if system_prompt_file and os.path.isfile(system_prompt_file):
        with open(system_prompt_file, "r", encoding="utf-8") as f:
            system_prompt = f.read().replace("{platform}", platform)
    else:
        system_prompt = SYSTEM_PROMPT_TEMPLATE.format(platform=platform)

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": task},
    ]
    tools_log = []
    total_prompt = 0
    total_completion = 0

    for iteration in range(1, max_iterations + 1):
        if verbose:
            print(f"[iteration {iteration}/{max_iterations}]", file=sys.stderr)

        # Warn the model when approaching the iteration limit
        if iteration == max_iterations - 1:
            messages.append({
                "role": "user",
                "content": "[SYSTEM WARNING] You have only 2 iterations left. Stop using tools NOW and provide your final answer with everything you've found so far. A partial answer is much better than no answer.",
            })
        elif iteration == max_iterations:
            messages.append({
                "role": "user",
                "content": "[SYSTEM WARNING] This is your LAST iteration. You MUST respond with your final answer immediately. Do NOT call any more tools.",
            })

        try:
            response = call_llm(messages, api_url, model, active_tools)
        except requests.exceptions.ConnectionError:
            return {"success": False, "result": f"Cannot connect to {api_url}. Is the model server running?",
                    "tools_used": tools_log, "iterations": iteration,
                    "tokens_used": {"prompt": total_prompt, "completion": total_completion,
                                    "total": total_prompt + total_completion}}
        except Exception as e:
            return {"success": False, "result": f"LLM API error: {e}",
                    "tools_used": tools_log, "iterations": iteration,
                    "tokens_used": {"prompt": total_prompt, "completion": total_completion,
                                    "total": total_prompt + total_completion}}

        usage = response.get("usage", {})
        total_prompt += usage.get("prompt_tokens", 0)
        total_completion += usage.get("completion_tokens", 0)

        choice = response["choices"][0]
        message = choice["message"]
        messages.append(message)

        tool_calls = message.get("tool_calls") or []
        if not tool_calls:
            return {
                "success": True,
                "result": message.get("content", ""),
                "tools_used": tools_log,
                "iterations": iteration,
                "tokens_used": {"prompt": total_prompt, "completion": total_completion,
                                "total": total_prompt + total_completion},
            }

        for tc in tool_calls:
            fn = tc["function"]
            name = fn["name"]
            try:
                args = json.loads(fn["arguments"]) if isinstance(fn["arguments"], str) else fn["arguments"]
            except json.JSONDecodeError:
                args = {}

            if verbose:
                print(f"  -> {name}({json.dumps(args, ensure_ascii=False)[:120]})", file=sys.stderr)

            result = execute_tool(name, args, workdir, timeout)
            tools_log.append({"name": name, "args": args, "result_preview": result[:200]})

            # Use tool_call_id if available, generate fallback otherwise
            tc_id = tc.get("id") or f"call_{iteration}_{name}"
            messages.append({
                "role": "tool",
                "tool_call_id": tc_id,
                "content": result,
            })

    return {
        "success": False,
        "result": "Max iterations reached without final answer.",
        "tools_used": tools_log,
        "iterations": max_iterations,
        "tokens_used": {"prompt": total_prompt, "completion": total_completion,
                        "total": total_prompt + total_completion},
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Autonomous local LLM agent")
    parser.add_argument("--task", required=True, help="Task description for the agent")
    parser.add_argument("--workdir", default=".", help="Working directory (default: current)")
    parser.add_argument("--api-url", default=os.environ.get("LOCAL_AGENT_API_URL", "http://127.0.0.1:1234/v1"),
                        help="OpenAI-compatible API base URL")
    parser.add_argument("--model", default=os.environ.get("LOCAL_AGENT_MODEL", "qwen3-coder-next"),
                        help="Model identifier")
    parser.add_argument("--max-iterations", type=int,
                        default=int(os.environ.get("LOCAL_AGENT_MAX_ITERATIONS", "15")),
                        help="Maximum agent loop iterations")
    parser.add_argument("--timeout", type=int, default=30, help="Command timeout in seconds")
    parser.add_argument("--verbose", action="store_true", help="Print progress to stderr")
    parser.add_argument("--allow-commands", action="store_true",
                        help="Enable run_command and git tools (disabled by default)")
    parser.add_argument("--system-prompt-file", default=None,
                        help="Path to a custom system prompt file. Use {platform} as placeholder.")

    args = parser.parse_args()
    workdir = str(Path(args.workdir).resolve())

    if not os.path.isdir(workdir):
        print(json.dumps({"success": False, "result": f"Workdir not found: {workdir}"}))
        sys.exit(1)

    result = run_agent(
        task=args.task, workdir=workdir, api_url=args.api_url,
        model=args.model, max_iterations=args.max_iterations,
        timeout=args.timeout, verbose=args.verbose,
        system_prompt_file=args.system_prompt_file,
        allow_commands=args.allow_commands,
    )
    sys.stdout.buffer.write(json.dumps(result, ensure_ascii=False, indent=2).encode("utf-8"))
    sys.stdout.buffer.write(b"\n")


if __name__ == "__main__":
    main()
