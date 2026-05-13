---
name: dotnet-analyze
description: .NET solution analysis workflow. Delegates to dotnet-analyzer agent to map project structure, dependencies, architecture patterns, EF Core models, and API surface. Produces a Markdown report in the target repo's doc/ folder.
---

## When to Use

- Exploring an unfamiliar .NET solution before planning or development
- Mapping architecture before a major refactor
- Identifying unused NuGet packages or dead code before cleanup
- Understanding EF Core model and migration history

---

## Workflow

### Mandatory: Delegate to dotnet-analyzer Agent

**Always launch the dotnet-analyzer agent. Never analyze inline.**

Launch **dotnet-analyzer** agent with:
- Target repo path from `$ARGUMENTS`
- The agent reads solution/project files, runs `dotnet build`, and extracts architecture signals

### What the Agent Produces

| Section | Content |
|---------|---------|
| Solution Overview | .NET version, project count, architecture pattern, ORM, auth |
| Project Map | All .csproj files, types, frameworks, key NuGet packages |
| Architecture Diagram | Mermaid block diagram of layers |
| API Surface | All controllers/endpoints with routes and auth |
| Data Model | DbSet entities and relationships |
| Dependency Graph | Inter-project references as Mermaid graph |
| Testing Coverage | Test projects, frameworks, test count |
| Build Health | Restore, build, nullable status |
| Findings | Reuse opportunities and red flags |

---

## Mandatory Skills Gate (Pre-Commit)

After the report is written:

1. **Invoke `Skill: git-commit`** — branch rules, commit message format

---

## Commit Format

```
docs: add codebase analysis for <solution-name>
subagent: dotnet-analyzer
```

---

## Key Principles

1. **Agent-first** — never analyze inline; always delegate to dotnet-analyzer
2. **Read-only** — agent never modifies source files
3. **Run `dotnet build` first** — confirms the build state before analyzing
