---
type: guide
status: active
tags:
  - meta
  - guide
updated: 2026-11-23
---

# How to build and use the SaLiksi mind map

**Goal:** an agent (or a developer) answers "where is X and what does it touch?" from this vault alone, and opens only the 2–5 source files that matter. Exploring the whole codebase on every run is the thing this vault exists to prevent. See [[README]] for conventions and [[00 Home]] for the entry point.

## 1. Principles
1. **One note per source file.** The note stands in for the file. It says what the file does, its important functions with line numbers, what it calls and what calls it.
2. **Small notes, small index.** Token cost is the point. Budgets:
   - `00 Home.md`: under 150 lines. It's only tables and links.
   - Any other note: under 60 lines. If a note needs more, split it.
   - No code dumps. Name functions, give line numbers, link out.
3. **Links are the map.** Every dependency is a `[[wikilink]]`, written on **both** ends (caller lists callee, callee lists caller). Then one hop from any note reaches everything it touches.
4. **Frontmatter points to the code.** `path:` is the exact repo-relative source file, so the agent can open it directly instead of searching.
5. **Honest status.** `active`, `partly-used` or `unused`, so agents skip dead code. Known bugs go in `70 Issues/`, not in the notes.
6. **Facts, not opinions.** A note records what the code does today, with names and numbers an agent can verify. When unsure, write "unverified".

## 2. Layout (shallow, prefixed, unique names)
| Folder | Holds | Prefix |
|---|---|---|
| `00 Overview/` | architecture, data model, storage keys | `app-`, `data-` |
| `10 Pages/` | one note per route page | `page-` |
| `20 API/` | one per `app/api/**/route.ts` | `api-` |
| `30 Lib/` | one per `lib/*` file | `lib-` |
| `40 Components/` | one per component | `comp-` |
| `50 External/` | third-party services | `ext-` |
| `60 Flows/` | end-to-end paths across files | `flow-` |
| `70 Issues/` | bugs, risks, dead code | `issues-` |
| `_templates/` | note templates | — |

Names are unique across the vault, so `[[api-writer]]` never collides and `grep -rl "api-writer"` finds every reference.

## 3. How to build it from scratch (for an agent)
Work in this order. Use the cheapest tool for each step: scripted extraction first, reading only where a script can't answer.
1. **Inventory:** `git ls-files` and line counts. This is the checklist of notes to write.
2. **Extract structure by script:** imports, exports, `fetch(` targets, `localStorage` / `sessionStorage` / `indexedDB` keys, and external URLs, one `grep -n` per file. This gives the links without reading whole files.
3. **Read for meaning only where needed:** the shared core (`lib/groq.ts`, the context/store files, layouts) in full, then big pages in outline (function list and the `fetch` calls).
4. **Write leaf notes first** (API routes, lib, components), then pages (which link down to them), then flows, then `00 Home.md` last.
5. **Add the visual layer:** a Canvas (pages → API → lib → external) and graph colour groups per folder.
6. **Validate** (section 5). The vault isn't finished until the checks pass.

## 4. Note templates
Use the files in `_templates/`. Minimum required for every note:
```yaml
---
type: page | api-route | lib | component | external | flow | data | issues | architecture
path: "saliksi/<repo-relative source file>"   # omit for flows/external/data
status: active | partly-used | unused
tags: [ ... ]
updated: YYYY-MM-DD
---
```
Body, in this order: one-line purpose · key functions with line numbers · **Calls** · **Called by** · gotchas.

## 5. Keeping it trustworthy (drift checks)
A stale map is worse than none, because the agent will trust it. Add one check script (`scripts/mindmap-check.mjs`, about 80 lines, no dependencies) and run it before every commit. It should fail when:
- a tracked source file under `app/`, `components/` or `lib/` has no note with a matching `path:`,
- a note's `path:` file no longer exists,
- any `[[link]]` points to a missing note,
- a note isn't linked from [[00 Home]] or a parent note (orphan),
- a source file's last git commit is newer than its note's `updated:` date (**stale**). Print these as warnings, not failures.

Optionally run it from a git pre-commit hook or CI. Until the script exists, the same rules are done by hand using the checklist in [[README]].

## 6. How to make agents use it instead of exploring
Be honest about the mechanism: instructions are **advisory**, and only a hook is enforcement. Use all three layers.

**Layer 1: CLAUDE.md (already in place).** The repo-root `CLAUDE.md` loads every session and says: read `00 Home.md` first, open only the notes you need, read only the source files their `path:` names, don't glob or grep the whole `saliksi/` tree. Keep it short. The longer it gets, the less it is followed.

**Layer 2: make the vault answer the question in one read.** If `00 Home.md` doesn't answer it, agents go exploring. So Home must hold:
- the page → API → lib table,
- a **"I want to change X → open these notes"** lookup (extend it whenever a task type comes up that it doesn't cover),
- the quick facts (stack, storage keys, env vars, run command).
When an agent has to explore anyway, treat that as a vault bug: add the missing note or lookup row.

**Layer 3: a hook for real enforcement (optional, ask the user before adding).** A project `.claude/settings.json` can add a `PreToolUse` hook on `Grep` and `Glob` that:
- allows the call if the vault's Home note was already read in this session,
- otherwise denies it with the message "Read SALIKSI-MINDMAP/00 Home.md first, then open only the notes you need,"
- allows any search scoped inside `SALIKSI-MINDMAP/` or to a single file path that a note named.
This turns "please read the map" into "you can't wander before reading the map." Write it with the `update-config` skill so the JSON is right, and test that a normal edit-a-known-file workflow isn't blocked.

## 7. Agent run protocol (what every run should look like)
1. Read `00 Home.md` (about 150 lines).
2. Open 2–5 notes the lookup points to. Follow `[[links]]` at most one hop.
3. Read only the source files and line ranges those notes name.
4. Check `issues-known` and `issues-dead-code` for traps.
5. Change the code.
6. **Update the vault in the same change:** the touched file's note (calls, called-by, `updated:`), plus every note whose link list changed. New file → new note from the template, linked from Home. Deleted/renamed file → update or remove the note and fix every link to it.
7. Run the drift check (once the script exists).

Escape hatch: if the vault has no note for something the task needs, search the code for that one thing, then **write the missing note** before finishing, so the next run doesn't need to search.

## 8. Signs the vault is working or failing
| Working | Failing |
|---|---|
| Agents open 2–5 source files per task | Agents glob/grep the whole `saliksi/` tree |
| Home answers "where is X" in one read | Agents ask or search because Home didn't say |
| Drift check passes, `updated:` dates track commits | Notes describe functions that no longer exist |
| Notes stay under 60 lines | Notes grow into copies of the code |

Spot-check once a month: pick three recent commits and compare the vault against the diff. Anything the vault got wrong is a note to fix.
