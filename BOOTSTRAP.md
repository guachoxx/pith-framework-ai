# Bootstrapping Pith Framework

> This document is meant to be read by an AI agent (Claude Code, Cursor, Windsurf, Aider, GitHub Copilot, or any agent that reads text files and writes to a workspace).
>
> **How a human invokes it**: open the agent in the workspace where Pith Framework should be deployed, then say:
>
> > "Read this BOOTSTRAP.md from Pith Framework and walk me through setup."
>
> If the agent does not have the file locally, the human can paste the URL or the file's content into the conversation.

## What this document does

You (the agent) walk the user through deploying Pith Framework in their workspace, conversationally, in 4 phases:

1. **Discovery** — ask the user a small set of questions
2. **Plan** — show what you intend to do and get confirmation
3. **Execute** — create the files
4. **Verify** — confirm the Boot Checklist passes

Wait for user confirmation between phases. Do not skip Phase 2 or Phase 4.

## What the user will have at the end

```
their-workspace/
├── AGENTS.md                              ← entry point with project info
├── CLAUDE.md                              ← bridge for Claude Code (safe to keep regardless)
├── .gitignore                             ← appended with framework entries
└── pith-framework/
    ├── CONFIG.md                          ← provider, user identity (gitignored)
    ├── METHODOLOGY.yaml                   ← default methodology (committed)
    ├── SYSTEM.yaml                        ← project's documentation index (committed)
    ├── PROVIDER_CACHE.md                  ← entity ID cache (gitignored, hybrid providers only)
    ├── ARCHITECTURE.md                    ← empty skeleton (committed)
    ├── BUILD_COMMANDS.md                  ← empty skeleton (committed)
    ├── TESTING_METHODOLOGY.md             ← empty skeleton (committed)
    ├── CREDENTIALS.md                     ← empty skeleton (gitignored)
    ├── LESSONS_LEARNED.md                 ← empty skeleton (committed)
    ├── projects/
    │   └── {current_user}/
    │       └── _INDEX.md                  ← user's work unit index (markdown-files provider)
    ├── framework/
    │   └── ENGINE.md                      ← framework kernel (committed)
    └── providers/                         ← all three providers copied; active one selected via CONFIG.md
        ├── markdown-files/
        │   ├── MAPPING.md
        │   └── SETUP.md
        ├── clickup/
        │   ├── MAPPING.md
        │   ├── MAPPING_BOOT.md
        │   └── SETUP.md
        └── notion/
            ├── MAPPING.md
            ├── MAPPING_BOOT.md
            └── SETUP.md
```

The Boot Checklist defined in `AGENTS.md` will pass on the next session — that is the success criterion.

## Prerequisites

- The agent must be able to **read text files**, **write text files**, and ideally **make HTTP requests** (for the on-demand download mode).
- For hybrid providers (ClickUp, Notion): the corresponding MCP server must be configured in the user's agent so the cache can be generated.

---

## Phase 1 — Discovery

Ask the user one question at a time. Wait for the answer before moving to the next.

### Q1. Project identity

Ask:
- What is the name of this project? → save as `{{PROJECT_NAME}}`
- One-line description? → save as `{{DESCRIPTION}}`
- Tech stack? (e.g., "Node.js 20 / TypeScript / PostgreSQL 16") → save as `{{STACK}}`

### Q2. Which AI agent

Ask:
- "Which AI agent are you using right now to run this bootstrap?"
- Suggest the common options: Claude Code, Cursor, Windsurf, Aider, GitHub Copilot, other.

If the answer is **Claude Code**, remember to mention the plugin recommendation in the optional next steps at the end. For any other agent, skip the plugin mention.

### Q3. Memory provider

Ask:
- "Where should the framework's documents live? Three options:"
  - **`markdown-files`** *(recommended for first-time users)* — everything on disk in this repo.
  - `clickup` — hybrid: framework files on disk, project documents in ClickUp Docs.
  - `notion` — hybrid: framework files on disk, project documents in Notion pages.

If the user picks **`markdown-files`**: skip Q4 entirely.

If the user picks `clickup` or `notion`: continue to Q4.

### Q4. Provider configuration (only if hybrid)

Ask the user for the connection settings appropriate to their provider. For details on what is required, read the chosen provider's `SETUP.md` (location depends on Q6 — see source modes below).

Always tell the user explicitly: API tokens go into `pith-framework/CONFIG.md`, which is gitignored. **Never commit them.**

### Q5. User identity and ownership mode

Ask:
- "What user identity should the framework put in `pith-framework/CONFIG.md` as `current_user`? Use the name/handle this agent should use for project ownership."
- "Will multiple people use this agent on this codebase, with per-user project ownership?"

Always save the identity as `current_user`. `CONFIG.md` always defines `current_user`, even for single-user installs.

If **no** to multi-user mode (the default): proceed. This is still a single-user namespace named after `current_user`.

If **yes**: keep the same `current_user` value for this user. Other users will have their own gitignored `CONFIG.md` and their own provider/user namespace.

For `markdown-files`, any defined `current_user` means the boot path is `pith-framework/projects/{current_user}/_INDEX.md`. Therefore bootstrap must create that index for both single-user and multi-user installs.

### Q6. Source of framework templates

Ask:
- "Do you have the `pith-framework` repository cloned locally, or should I download the templates from GitHub?"

Two valid modes:

- **Cloned mode**: user provides the local path to the cloned repo. You will read templates from `<local-path>/templates/`, `<local-path>/methodologies/default/`, etc.
- **Download mode**: you fetch templates from the GitHub raw URLs listed in Phase 3 (see "GitHub raw URLs"). Requires the user's agent to have HTTP fetch capability.

If the user is unsure, default to **download mode**.

---

## Phase 2 — Plan

Present a concrete plan to the user in plain language. Example:

> Here's what I'll do based on what you've told me:
>
> **Provider**: markdown-files (everything on disk)
> **Source**: download from GitHub
>
> **Files I'll create:**
> 1. `AGENTS.md` (with your project info)
> 2. `CLAUDE.md` (bridge for Claude Code, safe to keep regardless of which agent you use)
> 3. `pith-framework/CONFIG.md` (gitignored)
> 4. `pith-framework/METHODOLOGY.yaml` (default methodology)
> 5. `pith-framework/SYSTEM.yaml` (your documentation index, with your project info)
> 6. `pith-framework/framework/ENGINE.md` (framework kernel)
> 7. `pith-framework/ARCHITECTURE.md`, `BUILD_COMMANDS.md`, `TESTING_METHODOLOGY.md`, `CREDENTIALS.md` (gitignored), `LESSONS_LEARNED.md` — empty reference-document skeletons ready to fill in as your project grows
> 8. If provider is `markdown-files`: `pith-framework/projects/{current_user}/_INDEX.md`
> 9. `pith-framework/providers/markdown-files/` — `MAPPING.md`, `SETUP.md`
> 10. `pith-framework/providers/clickup/` — `MAPPING.md`, `MAPPING_BOOT.md`, `SETUP.md`
> 11. `pith-framework/providers/notion/` — `MAPPING.md`, `MAPPING_BOOT.md`, `SETUP.md`
>
> All three providers are copied. The active provider is determined by `pith-framework/CONFIG.md` at runtime — only its docs are read at boot. The other providers stay on disk so you can switch later by editing `CONFIG.md` (no need to re-run this bootstrap).
>
> **Files I'll modify or create:**
> - `.gitignore` — append framework-specific entries (CONFIG.md, PROVIDER_CACHE.md, temp/, logs/, scripts/ excluding scripts/permanent/). If `.gitignore` does not exist, I'll create it from the template.
>
> **Total**: about 20 new files for `markdown-files` (19 for hybrid providers), 1 modified or created.

If `AGENTS.md` **already exists** at the workspace root, mention it explicitly in the plan:

> "I see you already have an `AGENTS.md`. I'll prepare the new content from the framework template and show you both side by side before writing anything — you decide what to keep, merge, or replace."

### "Will not modify" list — always include in the plan

Before asking for confirmation, scan the workspace root for non-empty files and directories that the bootstrap will **not** touch (anything that is not in the file-by-file list above and is not `.git/`, `node_modules/`, `.venv/`, `__pycache__/`, or similar tooling caches). List them explicitly to the user. Example:

> **I will not touch:** `existing-design-doc.md`, `vendor/`, `notes/`, `desktop.ini`.

This reassures the user that their existing work is safe and surfaces anything they did not expect to find. If the workspace is empty, say so and skip this list.

Wait for explicit "yes, go ahead" before moving to Phase 3.

---

## Phase 3 — Execute

For each file, fetch the source template (per Q6), substitute placeholders, write to the target path.

### File-by-file plan

| Target (in user's workspace) | Source template (relative to canonical repo root) | Substitutions |
|---|---|---|
| `AGENTS.md` | `templates/AGENTS.md.template` | `{{PROJECT_NAME}}`, `{{DESCRIPTION}}`, `{{STACK}}` |
| `CLAUDE.md` | `templates/CLAUDE.md.template` | `{{PROJECT_NAME}}` if present |
| `pith-framework/CONFIG.md` | `templates/CONFIG.md.template` | `{{PROVIDER}}`, `{{CURRENT_USER}}` (always), connection settings (if hybrid — uncomment the relevant block and fill values) |
| `pith-framework/METHODOLOGY.yaml` | `methodologies/default/MANIFEST.yaml` | none — copy verbatim |
| `pith-framework/SYSTEM.yaml` | `templates/SYSTEM.yaml.template` | `{{PROJECT_NAME}}`, `{{DESCRIPTION}}`, `{{STACK}}` |
| `pith-framework/framework/ENGINE.md` | `ENGINE.md` (root of canonical repo) | none |
| `pith-framework/ARCHITECTURE.md` | `templates/ARCHITECTURE.md.template` | `{{PROJECT_NAME}}` |
| `pith-framework/BUILD_COMMANDS.md` | `templates/BUILD_COMMANDS.md.template` | `{{PROJECT_NAME}}` |
| `pith-framework/TESTING_METHODOLOGY.md` | `templates/TESTING_METHODOLOGY.md.template` | `{{PROJECT_NAME}}` |
| `pith-framework/CREDENTIALS.md` | `templates/CREDENTIALS.md.template` | `{{PROJECT_NAME}}` |
| `pith-framework/LESSONS_LEARNED.md` | `templates/LESSONS_LEARNED.md.template` | `{{PROJECT_NAME}}` |
| `pith-framework/projects/{current_user}/_INDEX.md` | `templates/PROJECT_INDEX.md.template` | none — markdown-files provider only; create the parent directory first |
| `pith-framework/providers/markdown-files/MAPPING.md` | `providers/markdown-files/MAPPING.md` | none |
| `pith-framework/providers/markdown-files/SETUP.md` | `providers/markdown-files/SETUP.md` | none |
| `pith-framework/providers/clickup/MAPPING.md` | `providers/clickup/MAPPING.md` | none |
| `pith-framework/providers/clickup/MAPPING_BOOT.md` | `providers/clickup/MAPPING_BOOT.md` | none |
| `pith-framework/providers/clickup/SETUP.md` | `providers/clickup/SETUP.md` | none |
| `pith-framework/providers/notion/MAPPING.md` | `providers/notion/MAPPING.md` | none |
| `pith-framework/providers/notion/MAPPING_BOOT.md` | `providers/notion/MAPPING_BOOT.md` | none |
| `pith-framework/providers/notion/SETUP.md` | `providers/notion/SETUP.md` | none |
| `.gitignore` | `templates/.gitignore.template` | **append** to existing `.gitignore`, or create it from the template if it does not exist |

**Always copy all three providers** (markdown-files, clickup, notion), regardless of which one the user chose in Q3. The active provider is determined by `pith-framework/CONFIG.md` at runtime — only its docs are read at boot. The others stay on disk so the user can switch providers later by editing `CONFIG.md` alone, without having to re-run the bootstrap. Cost: ~56KB extra on disk; runtime cost: zero.

If a source provider file is missing in the cloned repo or returns 404 in download mode (e.g., `MAPPING_BOOT.md` only exists for hybrid providers), skip that single file and continue.

### GitHub raw URLs (download mode)

Fetch all of these. The provider URLs cover the three providers — fetch them all (see the "always copy all three providers" rule above).

> **Note for forks**: the URLs below point to the canonical `guachoxx/pith-framework-ai` repo on the `main` branch. If the user is working from a fork or a different branch, replace `guachoxx/pith-framework-ai` with `<owner>/<repo>` (and `main` with the branch name) in every URL. If unsure, ask the user before fetching.

```
https://raw.githubusercontent.com/guachoxx/pith-framework-ai/main/templates/AGENTS.md.template
https://raw.githubusercontent.com/guachoxx/pith-framework-ai/main/templates/CLAUDE.md.template
https://raw.githubusercontent.com/guachoxx/pith-framework-ai/main/templates/CONFIG.md.template
https://raw.githubusercontent.com/guachoxx/pith-framework-ai/main/templates/.gitignore.template
https://raw.githubusercontent.com/guachoxx/pith-framework-ai/main/methodologies/default/MANIFEST.yaml
https://raw.githubusercontent.com/guachoxx/pith-framework-ai/main/templates/SYSTEM.yaml.template
https://raw.githubusercontent.com/guachoxx/pith-framework-ai/main/templates/ARCHITECTURE.md.template
https://raw.githubusercontent.com/guachoxx/pith-framework-ai/main/templates/BUILD_COMMANDS.md.template
https://raw.githubusercontent.com/guachoxx/pith-framework-ai/main/templates/TESTING_METHODOLOGY.md.template
https://raw.githubusercontent.com/guachoxx/pith-framework-ai/main/templates/CREDENTIALS.md.template
https://raw.githubusercontent.com/guachoxx/pith-framework-ai/main/templates/LESSONS_LEARNED.md.template
https://raw.githubusercontent.com/guachoxx/pith-framework-ai/main/templates/PROJECT_INDEX.md.template
https://raw.githubusercontent.com/guachoxx/pith-framework-ai/main/ENGINE.md
https://raw.githubusercontent.com/guachoxx/pith-framework-ai/main/providers/markdown-files/MAPPING.md
https://raw.githubusercontent.com/guachoxx/pith-framework-ai/main/providers/markdown-files/SETUP.md
https://raw.githubusercontent.com/guachoxx/pith-framework-ai/main/providers/clickup/MAPPING.md
https://raw.githubusercontent.com/guachoxx/pith-framework-ai/main/providers/clickup/MAPPING_BOOT.md
https://raw.githubusercontent.com/guachoxx/pith-framework-ai/main/providers/clickup/SETUP.md
https://raw.githubusercontent.com/guachoxx/pith-framework-ai/main/providers/notion/MAPPING.md
https://raw.githubusercontent.com/guachoxx/pith-framework-ai/main/providers/notion/MAPPING_BOOT.md
https://raw.githubusercontent.com/guachoxx/pith-framework-ai/main/providers/notion/SETUP.md
```

If a URL returns 404 (provider file genuinely does not exist in the canonical repo), skip that single file and continue. Do not abort the whole bootstrap for a missing optional file.

### Existing `AGENTS.md` — confirmation flow (do not auto-merge)

If `AGENTS.md` already exists at the workspace root:

1. Read the existing file in full.
2. Prepare the proposed new content from `templates/AGENTS.md.template` with substitutions.
3. Show the user **both** in the conversation: their current `AGENTS.md` and the proposed new one. Highlight the differences clearly.
4. Ask the user explicitly: "How do you want to proceed?"
   - **Replace** with the new template (their current content is lost)
   - **Keep** their existing file (skip this file in the bootstrap; user knows their setup)
   - **Manual merge** — you (agent) propose a merge that preserves their custom sections (typically "System Overview" if it has project-specific content) and replaces the framework-defined sections (Boot Sequence, Invariants, Context Budget, On-disk Resources). Show the proposal, then write only after explicit confirmation.
5. Do not silently overwrite under any circumstance.

### `.gitignore` — append safely

If `.gitignore` already exists, append the contents of `templates/.gitignore.template` at the end. If any of the entries are already present, skip them to avoid duplicates.

If `.gitignore` does not exist, create it with the template contents.

### Provider-specific notes

**`markdown-files`** *(default)*:
- Create an empty work unit index from `templates/PROJECT_INDEX.md.template`.
  - Target: `pith-framework/projects/{current_user}/_INDEX.md`
  - This applies to both single-user and multi-user installs because `CONFIG.md` always defines `current_user`.
  - Do not create `pith-framework/projects/_INDEX.md` during bootstrap unless the user explicitly asks for a team overview or legacy flat fallback.
- Project documents live on disk under `pith-framework/projects/{current_user}/{project-name}/` once the user creates them.
- Skip `PROVIDER_CACHE.md` — not needed.

**`clickup`** *(hybrid)*:
- Read the user's chosen provider's `SETUP.md` for the workspace/space/folder structure prerequisites.
- After files are written, generate `pith-framework/PROVIDER_CACHE.md` by querying the ClickUp workspace once. This requires the ClickUp MCP server configured in the user's agent.
- The cache must include: workspace ID, space ID, Reference folder ID, Projects folder ID, Project Index list ID, and IDs for each reference Doc/Page if any exist.

**`notion`** *(hybrid)*:
- Same flow as `clickup`, with Notion's `SETUP.md` and the Notion MCP server.

---

## Phase 4 — Verify

After all files are written:

1. Read `AGENTS.md` you just created. Sanity-check it: is the System Overview filled in, are the placeholders gone?
2. Run the **Boot Checklist** as defined in `AGENTS.md`. The checklist has 5 applicable rows for `markdown-files` provider and 6 applicable rows for hybrid providers. For each row, confirm the file exists and the listed field is present.
3. Report results to the user:
   - Success: "Boot Checklist passed (X/X). Pith Framework is deployed and ready to use."
   - Partial failure: "Row N failed because Y." Diagnose, propose a fix, retry that row only.

The deployment is **successful** when the Boot Checklist is fully green.

---

## Optional next steps to mention to the user

After successful verification, suggest:

- **(If user said Claude Code in Q2)** "Since you're using Claude Code, consider installing the Pith Framework plugin for slash commands like `/pith-boot`, `/pith-consolidate`, `/pith-status`, `/pith-new-project`, `/pith-close-project`. See `extensions/claude-code/plugin/` in the canonical repo for installation instructions. The plugin is optional — the framework works without it."
- **(For everyone)** "Read `docs/HUMANS_START_HERE.md` in the canonical repo for a complete guide on the daily workflow with the framework, including distillation, work modes, and module context."
- **(For everyone)** "When you're ready to track structured work, create your first project work unit using your agent's normal interface (e.g., 'Create a project called auth-refactor')."

Do **not** install the plugin yourself, do **not** create the first project work unit. Both are user-driven actions outside the bootstrap scope.

---

## Recovery if something fails

- **Report what failed and why** (file unreadable, network error, permission denied, MCP not configured).
- **Do not silently proceed.** Stop and ask the user how to handle.
- **Do not delete files you have already created.** Leave the workspace in a recoverable state.
- **Tell the user the current state** of the workspace: which files exist, which were modified, which still need to be created.

If the user wants to start over from scratch: instruct them to delete `pith-framework/` and the framework-related lines from `.gitignore`, then re-run this bootstrap.

---

## Notes for you (the agent)

- This bootstrap is intentionally agent-agnostic. Use whatever tools you have to read/write files and fetch URLs. The user does not need to know your tool names.
- If at any point you are unsure (e.g., the user gave an ambiguous answer, a template seems missing, an MCP call fails), **stop and ask** — do not guess.
- Keep the conversation in plain language. Avoid exposing implementation details (paths, frontmatter fields, schema names) unless the user explicitly asks.
- The end goal is a working Pith Framework deployment that the user understands. If at the end the user has files but does not know what they are, the bootstrap has failed even if the Boot Checklist passed.
