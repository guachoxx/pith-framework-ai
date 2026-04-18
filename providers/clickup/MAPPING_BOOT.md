# ClickUp Provider — Boot Summary
> Lightweight version loaded on every boot. Full details: see MAPPING.md (on-demand).

## API Limitations

1. **No nested Folders** — project containers cannot be sub-folders of a "Projects" folder.
2. **No custom field creation via API** — use native fields (Status, Assignee) instead.
3. **Docs support multiple Pages** — native way to group related documents.
4. **Search does not match underscores in Doc/Page names** — use spaces instead (e.g., `LESSONS LEARNED`).
5. **Search with keywords + location filter returns incomplete results** — to list all items in a location, use only the `location` filter without `keywords`.
6. **Editing existing Pages is not surgically safe by default** — for long or historical Pages, do not trust append/prepend as partial edits. Safe flow: read full Page → merge locally → replace full content → read back to verify.

## Entity Mapping (summary)

| Framework concept | ClickUp entity |
|---|---|
| Reference document | Doc (single-page) in Reference folder |
| Project container | Doc (multi-page) in Projects folder |
| Project document | Page inside a project Doc |
| Project index | List with tasks (one task per project) |
| Module context | **On disk**: `{module}/CLAUDE.md` |

## Project Index — Query Pattern

```
clickup_search(filters: {
  asset_types: ["task"],
  location: { subcategories: ["<project_index_list ID from PROVIDER_CACHE>"] }
})
```

Do NOT add `keywords` — see API Limitation #5.
