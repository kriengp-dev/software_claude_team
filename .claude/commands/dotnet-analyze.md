---
description: Analyze a .NET solution — maps project structure, architecture layers, EF Core models, API surface, and NuGet dependencies. Produces a Markdown report via dotnet-analyzer agent.
---

Follow the workflow defined in `.claude/skills/dotnet-analyze/SKILL.md` exactly.

Target repo / solution: $ARGUMENTS

---

## Execution

### Step 1 — Launch dotnet-analyzer Agent

Launch **dotnet-analyzer** agent with:
- Target repo: $ARGUMENTS
- The agent reads all `.sln`, `.csproj`, `.cs`, `.razor` files
- Runs `dotnet restore` and `dotnet build` for health check
- Produces report at `<TARGET_REPO>/doc/analysis_<solution-name>.md`

### Step 2 — Skills Gate

1. **Skill: git-commit** — commit the report (`docs: add codebase analysis for <name>` / `subagent: dotnet-analyzer`)

$ARGUMENTS
