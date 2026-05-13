---
description: Refactor .NET code — delegates to dotnet-reviewer agent (Section 2) to remove dead code, eliminate duplicates, fix SOLID violations, and apply performance optimizations on a stable, passing codebase.
---

Follow the workflow defined in `.claude/skills/dotnet-refactor/SKILL.md` exactly.

Scope / project path: $ARGUMENTS

---

## Prerequisite Check

Before launching the agent, confirm:
- [ ] `dotnet build` passes with no errors
- [ ] `dotnet test` — all tests green
- [ ] No active feature development on the same files

If any prerequisite fails, stop and notify the user.

---

## Execution

### Step 1 — Launch dotnet-reviewer Agent (Section 2 — Refactor & Dead Code Cleanup)

Launch **dotnet-reviewer** agent with:
- Project path / scope: $ARGUMENTS
- Focus: **Section 2 — Refactor & Dead Code Cleanup**
- The agent must:
  1. Detect unused code (`dotnet format --diagnostics IDE0005`, grep for TODO/FIXME)
  2. Categorize candidates: SAFE / CAREFUL / RISKY
  3. Remove SAFE items first; rebuild + retest after each category
  4. Consolidate duplicate logic
  5. Apply async, LINQ, EF, and allocation optimizations

### Step 2 — Skills Gate (after each passing batch)

1. Run `dotnet format <TARGET_REPO>` — style enforcement
2. Run `dotnet build` + `dotnet test` — verify nothing broke
3. **Skill: git-commit** — (`refactor: <description>` / `subagent: dotnet-reviewer`) — one commit per batch

$ARGUMENTS
