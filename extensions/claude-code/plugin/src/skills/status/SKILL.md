---
name: pith-status
description: "Show project status and progress. Lighter than /pith-boot — assumes boot has already been completed this session. Use this skill when the user asks where are we, what is the status, qué falta, en qué estamos, siguiente paso, how far along are we, qué queda por hacer, or names a specific project after boot is already done. Also use when the user returns after a pause within the same session and wants to reorient. Do NOT use for listing all projects, starting a session, or loading framework config — that is boot's job."
---

# Pith Status - Project Status

Show the status of active projects or a specific project current state.

## Prerequisites

Boot must be completed this session. If boot has not run, suggest the user run `/pith-boot` first.

## Without arguments

1. Query the Project Index **live from the provider** (use query pattern from MAPPING_BOOT.md). Do NOT use cache as a complete project list.
2. Display all active work units:
   - Name, state, owner, last_updated for each
3. If `current_user` is set in CONFIG.md, mark which projects belong to the current user.

## With argument (`$ARGUMENTS`)

1. Locate the project by name (try cache for ID, fall back to provider search)
2. Read the project entry point (artifact named in `work_unit.entry_point`)
3. **Staleness check**: if `last_updated` exceeds `conventions.staleness.threshold_hours`, warn the user:
   - "Project [name] was last updated [N] days ago. The status below may be outdated."
   - If user confirms, display the entry point as-is
   - If user declines or asks for something else, stop and ask which project to display instead
4. Display the full entry point content:
   - Last updated
   - Last session summary
   - Next step + done when
   - Done / In Progress / Next Steps / Blockers sections
5. End with: "Ready to continue with: [next_step]. Say 'go' or give a different instruction."

## Output format

Keep it concise and actionable. The user wants to know where things stand, not read a report.
