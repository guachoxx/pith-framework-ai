---
name: pith-status
description: "Show project status and progress. Lighter than /pith-boot — assumes boot has already been completed this session. Use this skill when the user asks where are we, what is the status, qué falta, en qué estamos, siguiente paso, how far along are we, qué queda por hacer, or names a specific project after boot is already done. Also use when the user returns after a pause within the same session and wants to reorient. Do NOT use for listing all projects, starting a session, or loading framework config — that is boot's job."
---

# Pith Status - Project Status

Show the status of active projects or a specific project current state.

## Prerequisites

Boot must be completed this session. If boot has not run, suggest the user run `/pith-boot` first.

## Without arguments

1. Query the work unit index **live from the provider**. For hybrid providers, use the query pattern from MAPPING_BOOT.md. For `markdown-files`, compute the index path directly: if `current_user` is set, read `pith-framework/projects/{current_user}/_INDEX.md`; otherwise read `pith-framework/projects/_INDEX.md`. Do NOT read `providers/markdown-files/MAPPING.md` just to list work units. Do NOT use cache as a complete work unit list.
2. Display all active work units:
   - Name, state, owner, Last updated for each
   - Use `Last updated` from the work unit index metadata. Do not read entry point artifacts just to display or sort the no-argument listing.
3. If `current_user` is set in CONFIG.md, mark which projects belong to the current user.

## With argument (`$ARGUMENTS`)

1. Locate the project by name. For hybrid providers, try cache first and fall back to provider search/index. For `markdown-files`, use the same computed `_INDEX.md` path from the no-argument flow, then read the matching work unit directory.
2. Read the project entry point: the artifact named in `work_unit.entry_point`. Do not assume a specific artifact name.
3. **Staleness check**: only if `conventions.staleness.threshold_hours` exists. If configured and `last_updated` exceeds the threshold, warn the user:
   - "Project [name] was last updated [N] days ago. The status below may be outdated."
   - If user confirms, display the entry point as-is
   - If user declines or asks for something else, stop and ask which project to display instead
   - If no staleness convention exists, skip this check and do not treat it as an error.
4. Display the full entry point content, emphasizing the fields declared in `work_unit.entry_point_fields`:
   - last_updated
   - next_step
   - any additional fields the methodology declares
5. End with: "Ready to continue with: [next_step]. Say 'go' or give a different instruction."

## Output format

Keep it concise and actionable. The user wants to know where things stand, not read a report.
