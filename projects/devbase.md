# devbase — World Model Compiler

> **Developer workspace compiler. 12 crates, 56K LOC, 71 MCP tools.**
>
> https://github.com/juice094/devbase

---

## What It Does

devbase compiles a developer's workspace into a structured model: code context, knowledge memories, and agent reasoning paths. It replaces fragmented repo managers, note-taking apps, and AI context windows with a single Rust-native engine.

---

## Architecture

```
compiler pipeline
  ├── tree-sitter          Multi-language code parsing
  ├── devbase-vault-*      Markdown vault management (Frontmatter + Wikilink)
  ├── devbase-symbol-links  Code symbol resolution
  └── devbase-workflow-*   Declarative workflow engine

skill system
  ├── devbase-skill-runtime-types    Skill type definitions
  ├── devbase-skill-runtime-parser   Skill file parser
  └── devbase-registry               Local skill registry

search & sync
  ├── Tantivy BM25          Full-text index
  ├── devbase-embedding     Multi-provider embedding (local + cloud)
  ├── devbase-sync-protocol  Workspace sync protocol
  └── devbase-syncthing-client  Syncthing integration

core
  └── devbase-core-types    Shared type system
```

---

## Key Technical Decisions

| Decision | Why |
|:---|:---|
| **Pure SQL cosine_similarity UDF** | Replaced external vector DB → deployment steps 4→1 |
| **tree-sitter parsing** | Language-agnostic AST → works across Rust/Python/TS/Go |
| **Tantivy BM25** | Fast full-text search without ML runtime |
| **Declarative workflows** | MD-driven → readable, versionable, auditable |
| **Syncthing integration** | Built on syncthing-rust → P2P workspace sync |

---

## Scale

| Metric | Value |
|:---|:---|
| Crates | 12 |
| MCP tools | 71 |
| Lines of Rust | 56,000 |
| Binary size | ~8.7MB |
| Storage | SQLite WAL + OpLog audit |
