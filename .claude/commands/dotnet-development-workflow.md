---
description: Full .NET development workflow — Plan → Implement → Review. Orchestrates dotnet-plan, dotnet-coding (backend + frontend in parallel when independent), and dotnet-review in sequence.
---

Follow the workflow defined in `.claude/skills/dotnet-development-workflow/SKILL.md` exactly.

Feature / task: $ARGUMENTS

---

## Step 0 — Ask Before Starting (once)

```
Feature: $ARGUMENTS

1. Scope:
   [F] Frontend only (Blazor / Razor)
   [B] Backend only  (API / EF / services)
   [A] Both frontend and backend

2. Requires new DB table or column?
   [Y] Yes — EF migration needed
   [N] No
```

Store as `<SCOPE>` and `<MIGRATION>`. Proceed immediately after answer.

---

## Phase 1 — Plan

Invoke **`Skill: dotnet-plan`**:
- Feature: $ARGUMENTS
- Runs: dotnet-analyzer (codebase map) + NuGet search → dotnet-planner
- Output: `<TARGET_REPO>/doc/plan_<feature-name>.md`
- Gate: `Skill: git-commit`

Wait for plan file to be committed before proceeding.

---

## Phase 2 — Implement (sequential after Phase 1)

Invoke **`Skill: dotnet-coding`**:
- Feature: $ARGUMENTS  
- Plan: `<TARGET_REPO>/doc/plan_<feature-name>.md`
- Scope: `<SCOPE>`

Agent launch:
- **A (both), independent tasks** → launch dotnet-backend-developer + dotnet-frontend-developer **in parallel**
- **A (both), frontend needs backend types** → backend first, then frontend
- **B only** → dotnet-backend-developer
- **F only** → dotnet-frontend-developer

Gate: `dotnet format` → XML docs → `Skill: git-commit`

Wait for implementation committed + `dotnet test` passing before proceeding.

---

## Phase 3 — Review (sequential after Phase 2)

Invoke **`Skill: dotnet-review`**:
- Scope: `<TARGET_REPO>`
- Reviews all `.cs` / `.razor` changes from Phase 2

### If BLOCKED (CRITICAL or HIGH found)

1. Invoke **`Skill: dotnet-coding`** — fix the reported issues
2. Invoke **`Skill: dotnet-review`** — re-review
3. Repeat until review passes

### If PASSES

Gate: `dotnet format` → XML docs → `Skill: git-commit`

Workflow complete — open PR via `Skill: git-commit` PR process.

$ARGUMENTS
