---
type: readme
tags:
  - meta
updated: 2026-11-22
---

# Vault README — how this mind map works

This Obsidian vault documents **how the SaLiksi code is connected**. It is the first thing an AI agent (Claude Code) or a developer should read before touching the code. Start at [[00 Home]].

## Folder layout (shallow on purpose)
| Folder | Contains | Prefix |
|---|---|---|
| `00 Overview/` | architecture, data model, storage keys | `app-`, `data-` |
| `10 Pages/` | one note per dashboard page | `page-` |
| `20 API/` | one note per `app/api/**/route.ts` | `api-` |
| `30 Lib/` | one note per `lib/*` file | `lib-` |
| `40 Components/` | one note per component | `comp-` |
| `50 External/` | third-party services | `ext-` |
| `60 Flows/` | end-to-end user flows across files | `flow-` |
| `70 Issues/` | bugs, risks, dead code | `issues-` |
| `_templates/` | templates for new notes | — |

## Note conventions
- **Frontmatter** (flat YAML, works with Obsidian Properties): `type`, `path` (repo-relative source file), `status` (`active` / `unused` / `partly-used`), `tags`, `aliases`, `updated`.
- Every note links to what it **calls** and what **calls it** with `[[wikilinks]]` → the Graph view and Backlinks pane show the dependency map.
- File names are unique and prefixed so links never collide and `grep` is easy (`grep -l "api-writer" -r .`).
- No new orphans: every new note must be linked from [[00 Home]] or a parent note.
- Rename notes **inside Obsidian** so links update.

## Views
- **Graph view**: colour groups are preset per folder (pages, api, lib, components, external, flows, issues).
- **Canvas**: `SaLiksi Mindmap.canvas` is the visual mind map (pages → API → lib → external).
- **Tags pane**: `#core`, `#unused`, `#storage`, `#ai`, `#writer`, …

## Guide
Full build, maintenance and agent-usage rules: [[MINDMAP-GUIDE]].

## Keeping it in sync
When code changes: update the matching note (`path:` tells you which), its links, and `updated:`. New file → new note from `_templates/`, link it from [[00 Home]].
