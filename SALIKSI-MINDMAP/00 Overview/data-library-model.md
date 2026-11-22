---
type: data
status: active
tags:
  - data
  - storage
  - core
updated: 2026-11-22
---

# Data model (client-only, no DB)
```
Folder { id, name, createdAt,
  articles:  SavedArticle[]   // id,title,authors:Author[],year,month?,day?,journal,credibility,abstract,keywords,localSource,url,savedAt,openAccess?,citationCount?
  notebooks: Notebook[]       // id,name,content(html),pages?:NotebookPage[],updatedAt,createdAt,wordCount?,citationFormat?,citedSourceIds?
  vault:     VaultFile[]      // id,name,type('article'|'notebook'|mime),size?,dataUrl?,linkedArticleId?,linkedNotebookId?,linkedFolderId?,addedAt
}
Author { firstName, middleName?, lastName }
```
Defined in [[lib-libraryStore]]; mutated by [[lib-libraryContext]] and [[lib-writerStorage]]; projected to `VaultSource` for AI by `getVaultSources` ([[lib-writer-types]]).
Where it's stored: [[data-storage-keys]].
