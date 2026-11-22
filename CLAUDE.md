# CLAUDE.md — read the mind map first

This repo has an Obsidian vault that maps how the code connects: **`SALIKSI-MINDMAP/`**.
**Before you open any source file, read the vault.** It shows which files matter for a task, so you can skip exploring the whole codebase.

## Required workflow (every task)
1. Read `SALIKSI-MINDMAP/00 Home.md`. It has the page → API → lib tables and a "I want to change X" lookup.
2. Open only the 2–5 notes relevant to the task (`10 Pages/page-*`, `20 API/api-*`, `30 Lib/lib-*`, `40 Components/comp-*`, `60 Flows/flow-*`).
3. Each note's frontmatter `path:` names the exact source file. Read **only those files**, and only the parts you need (most notes give the line numbers of the main functions).
4. Check `70 Issues/issues-known.md` and `issues-dead-code.md` so you don't "fix" unused code or trip over known bugs.
5. Don't grep or glob the whole `saliksi/` tree unless the vault has no note for what you need.

## After changing code: keep the vault in sync
- Edited a file → update its note (what it calls, what calls it, LoC if it changed a lot) and set `updated:` to today.
- New file → new note from `SALIKSI-MINDMAP/_templates/`, linked from `00 Home.md` (no orphan notes).
- Deleted or renamed a file → update or remove its note and fix every `[[link]]` to it.
- New API call between files → add the `[[wikilink]]` on **both** notes (caller and callee).
- Fixed a known issue → remove it from `70 Issues/issues-known.md`.

## Quick facts (so you don't have to look them up)
- The app is in `saliksi/` (Next.js 16 App Router, React 19, TS, Tailwind 4). Run with `cd saliksi && npm run dev`.
- All AI calls run server-side through `saliksi/lib/groq.ts` (`askGroq` / `askGroqJSON`). Env: `GROQ_API_KEY`.
- There is no database. All user data lives in localStorage `dunong_library_v2` (plus IndexedDB `dunong_files_db`).
- Every dashboard page sits inside `LibraryProvider` and `DevModeProvider` (`app/(dashboard)/layout.tsx`).
- Old project name is "dunong", so expect `dunong_*` keys and `"name": "dunong"` in package.json.
