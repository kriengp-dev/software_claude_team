---
description: Review .NET code — delegates to dotnet-reviewer agent to check async correctness, EF anti-patterns, SOLID, security, and Blazor-specific issues. Section 1 (code review) only.
---

Follow the workflow defined in `.claude/skills/dotnet-review/SKILL.md` exactly.

Scope / project path: $ARGUMENTS

---

## Execution

### Step 1 — Launch dotnet-reviewer Agent (Section 1 — Code Review)

Launch **dotnet-reviewer** agent with:
- Project path / scope: $ARGUMENTS
- Focus: **Section 1 — Code Review only**
- The agent must:
  1. Run `git diff -- '*.cs' '*.razor' '*.csproj'` to identify changed files
  2. Run `dotnet build <TARGET_REPO>` — capture compiler warnings
  3. Run `dotnet format <TARGET_REPO> --verify-no-changes` — check style
  4. Review all modified files against CRITICAL / HIGH / MEDIUM priorities

### Step 2 — Skills Gate (after agent completes and fixes applied)

1. Run `dotnet format <TARGET_REPO>` — style enforcement
2. Verify XML doc comments on modified public APIs
3. **Skill: git-commit** — (`fix: <description>` / `subagent: dotnet-reviewer`)

$ARGUMENTS
