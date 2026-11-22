---
type: architecture
path: "saliksi/app/layout.tsx"
status: active
tags:
  - architecture
  - layout
updated: 2026-11-22
---

# App shell & layouts
- `app/layout.tsx` — root HTML, Geist fonts, metadata (title "SaLiksi", icon `/logo.png`), `globals.css` (91 LoC; Neue Montreal, noise texture, scrollbar).
- `app/page.tsx` — `redirect('/researcher')`.
- `app/(dashboard)/layout.tsx` — `DevModeProvider` › `LibraryProvider` › [[comp-Sidebar]] + content + [[comp-DevModeOverlay]]. Background `#FAF8F5`, grain overlay, maroon `#521118` gradient.

So **every dashboard page can use** [[lib-libraryContext]] and [[lib-devModeContext]].
Config: `next.config.ts` (`allowedDevOrigins`, `serverExternalPackages: ['pdf-parse']`, supabase image pattern — unused). Package name is still `"dunong"`.
