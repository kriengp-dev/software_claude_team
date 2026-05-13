---
name: dotnet-development-workflow
description: Full .NET development workflow — orchestrates dotnet-plan → dotnet-coding → dotnet-review in sequence. Each phase delegates to its own agents. Frontend and backend are launched in parallel during the coding phase when independent.
---

## When to Use

- Starting a new .NET feature end-to-end (API + Blazor + EF migration)
- Any work that requires planning before coding and review after coding

**Skip when:** fixing a single isolated bug (use `/dotnet-coding` directly) or reviewing only (use `/dotnet-review`).

---

## Pre-flight: Ask Once Before Starting

Ask the user two questions before launching any agent:

```
1. Scope:
   [F] Frontend only (Blazor / Razor)
   [B] Backend only  (API / EF / services)
   [A] Both frontend and backend

2. Does this feature require a new DB table or column?
   [Y] Yes — EF migration needed
   [N] No
```

Store as `<SCOPE>` and `<MIGRATION>`.

---

## Phase 1 — Plan

**Must complete before Phase 2.**

Invoke **`Skill: dotnet-plan`** with the feature description from `$ARGUMENTS`.

The skill will:
1. Launch **dotnet-analyzer** to map the existing solution
2. Search NuGet for reusable packages
3. Launch **dotnet-planner** to produce the plan file

**Output:** `<TARGET_REPO>/doc/plan_<feature-name>.md`

**Skills gate:** `Skill: git-commit`

Do not proceed to Phase 2 until the plan file is committed.

---

## Phase 2 — Implement

**Starts only after Phase 1 is complete.**

Invoke **`Skill: dotnet-coding`** with:
- Feature description: `$ARGUMENTS`
- Plan file: `<TARGET_REPO>/doc/plan_<feature-name>.md`
- Scope: `<SCOPE>`

### Agent Launch Strategy

| Scope | Agent execution |
|-------|----------------|
| Backend only (B) | Launch **dotnet-backend-developer** |
| Frontend only (F) | Launch **dotnet-frontend-developer** |
| Both (A) — independent tasks | Launch **both agents in parallel** |
| Both (A) — frontend needs backend types | Backend first → then frontend |

**Skills gate (inside dotnet-coding):** `dotnet format` → XML docs → `Skill: git-commit`

Do not proceed to Phase 3 until all implementation is committed and `dotnet test` passes.

---

## Phase 3 — Review

**Starts only after Phase 2 is complete.**

Invoke **`Skill: dotnet-review`** with the target repo path.

The dotnet-reviewer agent:
1. Runs `git diff -- '*.cs' '*.razor'` to identify Phase 2 changes
2. Runs `dotnet build` + `dotnet format --verify-no-changes`
3. Reviews all modified files

### If Review Finds CRITICAL or HIGH Issues

1. Invoke **`Skill: dotnet-coding`** (backend or frontend agent as appropriate) to fix
2. Invoke **`Skill: dotnet-review`** again to confirm resolution
3. Repeat until no CRITICAL or HIGH issues remain

### If Review Passes

**Skills gate:** `dotnet format` → XML docs → `Skill: git-commit`

---

## Execution Flow

```
Ask <SCOPE> and <MIGRATION>
           │
           ▼
[Phase 1] Skill: dotnet-plan ─────────────────── commit: docs: add plan
           │
           ▼ (plan committed)
[Phase 2] Skill: dotnet-coding
  ├─ B: dotnet-backend-developer ────────────── commit: feat: ...
  ├─ F: dotnet-frontend-developer ───────────── commit: feat: ...
  └─ A: both (parallel if independent) ──────── commit: feat: ...
           │
           ▼ (implementation committed, tests pass)
[Phase 3] Skill: dotnet-review ────────────────── commit: fix: ... (if needed)
           │
           ▼
     Ready for PR
```

---

## Key Principles

1. **Sequential phases** — Phase 2 needs the plan; Phase 3 needs committed code
2. **Parallel agents** — backend and frontend run simultaneously when tasks are independent
3. **Review loop** — CRITICAL/HIGH issues must be fixed and re-reviewed before declaring done
4. **Each phase owns its gate** — this skill orchestrates; individual skills handle `dotnet format` and git-commit
