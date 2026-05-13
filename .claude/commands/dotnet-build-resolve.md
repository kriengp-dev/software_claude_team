---
description: Fix .NET build errors — delegates to dotnet-build-resolver agent to diagnose and fix MSBuild errors, NuGet restore failures, project reference issues, EF migration errors, and SDK conflicts with surgical changes.
---

Follow the workflow defined in `.claude/skills/dotnet-build-resolve/SKILL.md` exactly.

Project path / error description: $ARGUMENTS

---

## Execution

### Step 1 — Launch dotnet-build-resolver Agent

Launch **dotnet-build-resolver** agent with:
- Project path / error output: $ARGUMENTS
- The agent must:
  1. Run `dotnet restore` → identify NuGet failures
  2. Run `dotnet build` → capture all compiler errors
  3. Read the affected file for context
  4. Apply the minimal fix for the first error
  5. Re-run build to verify fix and check for new errors
  6. Repeat until `dotnet build` succeeds

**Surgical fixes only** — no refactoring, no signature changes, no `#pragma warning disable` without approval.

### Stop Conditions

Report to user and stop if:
- Same error persists after 3 fix attempts
- Fix introduces more errors than it resolves
- Error requires project restructuring or major version upgrade

### Step 2 — Skills Gate (after build succeeds)

1. Run `dotnet format <TARGET_REPO>` — apply any formatting fixes
2. **Skill: git-commit** — (`fix: <description>` / `subagent: dotnet-build-resolver`)

$ARGUMENTS
