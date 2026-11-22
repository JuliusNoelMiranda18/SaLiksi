---
type: lib
path: "saliksi/lib/devModeContext.tsx"
status: active
tags:
  - lib
  - devmode
  - react-context
updated: 2026-11-22
---

# lib/devModeContext.tsx — `DevModeProvider` / `useDevMode()`
222 LoC. Powers the "Dev Mode" side pane.

- State: `isDevModeEnabled`, `isPaneExpanded`, `groups: LogGroup[]` (each with `LogEntry[]`).
- `startLogGroup(route, title, source)` → groupId; `addLog(msg, groupId)`; `streamAITrace(operation, context, groupId)` → streams from [[api-dev-trace]].
- Enabled from [[comp-Sidebar]] ("Initialize Dev Mode?" dialog). Rendered by [[comp-DevModeOverlay]].

Used by: [[page-researcher]], [[page-credibility]], [[page-aitools]], [[page-citation]]. Flow: [[flow-dev-mode]]
