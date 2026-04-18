#!/usr/bin/env python3
"""Run trigger evaluation for pith plugin skills.

Tests whether a skill's description causes Claude to trigger (invoke the skill)
for a set of test queries. Cross-platform (Windows + Unix).

Usage:
    python run_trigger_eval.py --skill-path ../skills/boot --eval-set boot_trigger_eval.json
    python run_trigger_eval.py --all                       # Run all eval sets
    python run_trigger_eval.py --all --runs-per-query 3    # Multiple runs for variance
"""

import argparse
import json
import os
import subprocess
import sys
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


def parse_skill_md(skill_path: Path) -> tuple:
    """Parse a SKILL.md file, returning (name, description, full_content)."""
    content = (skill_path / "SKILL.md").read_text(encoding="utf-8")
    lines = content.split("\n")

    if lines[0].strip() != "---":
        raise ValueError("SKILL.md missing frontmatter (no opening ---)")

    end_idx = None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_idx = i
            break

    if end_idx is None:
        raise ValueError("SKILL.md missing frontmatter (no closing ---)")

    name = ""
    description = ""
    frontmatter_lines = lines[1:end_idx]
    i = 0
    while i < len(frontmatter_lines):
        line = frontmatter_lines[i]
        if line.startswith("name:"):
            name = line[len("name:"):].strip().strip('"').strip("'")
        elif line.startswith("description:"):
            value = line[len("description:"):].strip()
            if value in (">", "|", ">-", "|-"):
                continuation_lines = []
                i += 1
                while i < len(frontmatter_lines) and (
                    frontmatter_lines[i].startswith("  ")
                    or frontmatter_lines[i].startswith("\t")
                ):
                    continuation_lines.append(frontmatter_lines[i].strip())
                    i += 1
                description = " ".join(continuation_lines)
                continue
            else:
                description = value.strip('"').strip("'")
        i += 1

    return name, description, content


def find_project_root() -> Path:
    """Find the project root by walking up from cwd looking for .claude/."""
    current = Path.cwd()
    for parent in [current, *current.parents]:
        if (parent / ".claude").is_dir():
            return parent
    return current


def run_single_query(
    query: str,
    skill_name: str,
    skill_description: str,
    timeout: int,
    project_root: str,
    model: str = None,
) -> bool:
    """Run a single query and return whether the skill was triggered.

    Detection strategy: When the skill is already installed as a plugin,
    Claude will invoke the real skill (e.g., "pith:boot") instead of any
    temporary command we create. So we detect triggering by checking if
    Claude's FIRST tool call targets this skill (via Skill tool) or reads
    its SKILL.md file (via Read tool).

    We match on the skill_name (e.g., "pith-boot") which appears in the
    Skill tool input as "pith:boot" (colon-separated plugin:skill format)
    or in Read paths containing the skill directory name.
    """
    # Build match patterns for the skill
    # Plugin skills are invoked as "pith:boot", "pith:consolidate", etc.
    # The skill_name from SKILL.md is "pith-boot", "pith-consolidate", etc.
    base_name = skill_name.replace("pith-", "")  # "boot", "consolidate", etc.
    match_patterns = [
        skill_name,                    # "pith-boot"
        f"pith:{base_name}",          # "pith:boot"
        f"pith-{base_name}",          # "pith-boot" (legacy)
        f"/{base_name}",              # "/boot" in file paths
        f"/skills/{base_name}/",      # skill directory path
    ]

    try:
        # Resolve plugin directory (parent of evals/)
        plugin_dir = str(Path(__file__).parent.parent)

        cmd = [
            "claude",
            "-p", query,
            "--plugin-dir", plugin_dir,
            "--dangerously-skip-permissions",
            "--max-turns", "3",
            "--output-format", "stream-json",
            "--verbose",
        ]
        if model:
            cmd.extend(["--model", model])

        env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}

        result = subprocess.run(
            cmd,
            capture_output=True,
            timeout=timeout,
            cwd=project_root,
            env=env,
        )

        output = result.stdout.decode("utf-8", errors="replace")

        # Scan ALL assistant messages for tool_use targeting this skill
        for line in output.split("\n"):
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue

            if event.get("type") != "assistant":
                continue

            message = event.get("message", {})
            for content_item in message.get("content", []):
                if content_item.get("type") != "tool_use":
                    continue
                tool_name = content_item.get("name", "")
                tool_input = content_item.get("input", {})

                if tool_name == "Skill":
                    skill_ref = tool_input.get("skill", "")
                    if any(p in skill_ref or skill_ref in p for p in match_patterns):
                        return True

                elif tool_name == "Read":
                    file_ref = tool_input.get("file_path", "").replace("\\", "/")
                    if any(p in file_ref for p in match_patterns):
                        return True

        return False

    except subprocess.TimeoutExpired:
        return False
    except Exception as e:
        print(f"  [ERROR] Query failed: {e}", file=sys.stderr)
        return False


def run_eval(
    eval_set: list,
    skill_name: str,
    description: str,
    num_workers: int,
    timeout: int,
    project_root: Path,
    runs_per_query: int = 1,
    trigger_threshold: float = 0.5,
    model: str = None,
) -> dict:
    """Run the full eval set and return results."""
    results = []

    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        future_to_info = {}
        for item in eval_set:
            for run_idx in range(runs_per_query):
                future = executor.submit(
                    run_single_query,
                    item["query"],
                    skill_name,
                    description,
                    timeout,
                    str(project_root),
                    model,
                )
                future_to_info[future] = (item, run_idx)

        query_triggers = {}
        query_items = {}
        for future in as_completed(future_to_info):
            item, _ = future_to_info[future]
            query = item["query"]
            query_items[query] = item
            if query not in query_triggers:
                query_triggers[query] = []
            try:
                query_triggers[query].append(future.result())
            except Exception as e:
                print(f"  [WARN] Query exception: {e}", file=sys.stderr)
                query_triggers[query].append(False)

    for query, triggers in query_triggers.items():
        item = query_items[query]
        trigger_rate = sum(triggers) / len(triggers)
        should_trigger = item["should_trigger"]
        if should_trigger:
            did_pass = trigger_rate >= trigger_threshold
        else:
            did_pass = trigger_rate < trigger_threshold
        results.append({
            "query": query,
            "should_trigger": should_trigger,
            "trigger_rate": trigger_rate,
            "triggers": sum(triggers),
            "runs": len(triggers),
            "pass": did_pass,
        })

    passed = sum(1 for r in results if r["pass"])
    total = len(results)

    return {
        "skill_name": skill_name,
        "description_length": len(description),
        "results": results,
        "summary": {
            "total": total,
            "passed": passed,
            "failed": total - passed,
            "pass_rate": f"{passed}/{total} ({100*passed//total}%)" if total > 0 else "N/A",
        },
    }


def main():
    parser = argparse.ArgumentParser(
        description="Run trigger evaluation for pith plugin skills"
    )
    parser.add_argument(
        "--skill-path", help="Path to skill directory (containing SKILL.md)"
    )
    parser.add_argument("--eval-set", help="Path to eval set JSON file")
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run all eval sets in evals/ directory",
    )
    parser.add_argument(
        "--description", default=None, help="Override description to test"
    )
    parser.add_argument(
        "--num-workers", type=int, default=5, help="Parallel workers (default: 5)"
    )
    parser.add_argument(
        "--timeout", type=int, default=45, help="Timeout per query in seconds"
    )
    parser.add_argument(
        "--runs-per-query",
        type=int,
        default=1,
        help="Runs per query for variance (default: 1)",
    )
    parser.add_argument(
        "--trigger-threshold",
        type=float,
        default=0.5,
        help="Trigger rate threshold (default: 0.5)",
    )
    parser.add_argument("--model", default=None, help="Model override for claude -p")
    parser.add_argument(
        "--verbose", action="store_true", help="Print progress to stderr"
    )
    args = parser.parse_args()

    evals_dir = Path(__file__).parent
    plugin_dir = evals_dir.parent
    project_root = find_project_root()

    if args.all:
        # Run all eval sets
        eval_map = {
            "boot_trigger_eval.json": "boot",
            "status_trigger_eval.json": "status",
            "consolidate_trigger_eval.json": "consolidate",
        }

        all_results = {}
        for eval_file, skill_name in eval_map.items():
            eval_path = evals_dir / eval_file
            skill_path = plugin_dir / "skills" / skill_name

            if not eval_path.exists():
                print(f"[SKIP] {eval_file} not found", file=sys.stderr)
                continue
            if not (skill_path / "SKILL.md").exists():
                print(f"[SKIP] {skill_name}/SKILL.md not found", file=sys.stderr)
                continue

            name, description, _ = parse_skill_md(skill_path)
            eval_set = json.loads(eval_path.read_text(encoding="utf-8"))

            if args.verbose:
                print(f"\n{'='*60}", file=sys.stderr)
                print(f"Evaluating: {name}", file=sys.stderr)
                print(f"{'='*60}", file=sys.stderr)

            output = run_eval(
                eval_set=eval_set,
                skill_name=name,
                description=args.description or description,
                num_workers=args.num_workers,
                timeout=args.timeout,
                project_root=project_root,
                runs_per_query=args.runs_per_query,
                trigger_threshold=args.trigger_threshold,
                model=args.model,
            )

            if args.verbose:
                s = output["summary"]
                print(f"Results: {s['pass_rate']}", file=sys.stderr)
                for r in output["results"]:
                    status = "PASS" if r["pass"] else "FAIL"
                    rate = f"{r['triggers']}/{r['runs']}"
                    exp = "should" if r["should_trigger"] else "should NOT"
                    print(
                        f"  [{status}] rate={rate} ({exp} trigger): {r['query'][:60]}",
                        file=sys.stderr,
                    )

            all_results[name] = output

        print(json.dumps(all_results, indent=2))

    else:
        if not args.skill_path or not args.eval_set:
            parser.error("--skill-path and --eval-set required (or use --all)")

        skill_path = Path(args.skill_path)
        if not (skill_path / "SKILL.md").exists():
            print(f"Error: No SKILL.md at {skill_path}", file=sys.stderr)
            sys.exit(1)

        name, description, _ = parse_skill_md(skill_path)
        eval_set = json.loads(Path(args.eval_set).read_text(encoding="utf-8"))

        if args.verbose:
            print(f"Evaluating: {name} ({len(description)} chars)", file=sys.stderr)

        output = run_eval(
            eval_set=eval_set,
            skill_name=name,
            description=args.description or description,
            num_workers=args.num_workers,
            timeout=args.timeout,
            project_root=project_root,
            runs_per_query=args.runs_per_query,
            trigger_threshold=args.trigger_threshold,
            model=args.model,
        )

        if args.verbose:
            s = output["summary"]
            print(f"Results: {s['pass_rate']}", file=sys.stderr)
            for r in output["results"]:
                status = "PASS" if r["pass"] else "FAIL"
                rate = f"{r['triggers']}/{r['runs']}"
                exp = "should" if r["should_trigger"] else "should NOT"
                print(
                    f"  [{status}] rate={rate} ({exp} trigger): {r['query'][:60]}",
                    file=sys.stderr,
                )

        print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
