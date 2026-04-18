# Notion Provider — Boot Summary
> Lightweight version loaded on every boot. Full details: see MAPPING.md (on-demand).

## API Considerations

1. **Block-based content** — Notion stores content as blocks, not raw Markdown. The MCP server handles conversion, but complex Markdown (nested lists, tables inside toggles) may not round-trip perfectly. For long/historical pages, use a read → merge → replace → verify flow rather than trusting partial edits.
2. **Databases as containers and indexes** — Each row is a page with properties (Status, Assignee) and a page body for content.
3. **Sub-pages for grouping** — Project documents are sub-pages of a project page. This is Notion's native way to group related content under a single database row.
4. **Person property for ownership** — Ownership is tracked via the native Person property on database rows. No per-user folders or namespaces needed.
5. **Data source IDs are distinct from database IDs** — Some MCP operations require both; cache both (see Provider Cache section of MAPPING.md).

## Entity Mapping (summary)

| Framework concept | Notion entity |
|---|---|
| Reference document | Page (row) in the Reference database, content in page body |
| Project container | Page (row) in the Project Index database |
| Project document | Sub-page of a project page |
| Project index | Database with Status + Assignee properties |
| Module context | **On disk**: `{module}/CLAUDE.md` |

## Project Index — Query Pattern

To list all projects (rows in the Project Index database), query the database directly using the ID from PROVIDER_CACHE:

```
notion-fetch(id: "<project_index_database ID from PROVIDER_CACHE>")
```

To filter by the current user in multi-user mode, apply a filter on the `Assignee` Person property.

Do NOT rely on the cache's `## Projects` section as a complete list — it is an ID reference for already-known projects. Always query the database live when listing active projects.
