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

## Pre-execution Setup (Mandatory — do before Phase 1)

### A — Resolve Git Repo Root

Run this once and store as `<GIT_REPO_ROOT>`:

```bash
git -C "<TARGET_REPO>" rev-parse --show-toplevel
```

**Rules:**
- If the command succeeds → use the printed path as `<GIT_REPO_ROOT>` for all git operations in this workflow
- If it fails (no repo found) → STOP and ask the user which git repository to use
- **Never run `git init`** unless the user explicitly requests it

All commits in this workflow go to `<GIT_REPO_ROOT>`, not the Claude project repo.

### B — Create TodoWrite Task List

Before launching any agent, create a todo list covering every phase and gate:

```
[ ] Phase 1 — Plan
    [ ] 0a: dotnet-analyzer launched
    [ ] 0b: NuGet search complete
    [ ] 0c: Reuse decision documented
    [ ] 1: plan file exists on disk at <TARGET_REPO>/doc/
    [ ] GATE: plan committed to <GIT_REPO_ROOT> ← MUST be done before Phase 2

[ ] Phase 2 — Implement
    [ ] dotnet-backend-developer / dotnet-frontend-developer complete
    [ ] dotnet format — clean (no output)
    [ ] dotnet test — passed (or "no test project" documented)
    [ ] XML docs — verified (or "project uses no XML docs" documented)
    [ ] GATE: implementation committed to <GIT_REPO_ROOT> ← MUST be done before Phase 3

[ ] Phase 3 — Review
    [ ] dotnet-reviewer pass 1 complete
    [ ] if CRITICAL/HIGH found: fixes applied + NEW dotnet-reviewer pass launched
    [ ] no CRITICAL/HIGH remaining
    [ ] dotnet format --verify-no-changes — clean
    [ ] GATE: fix commits committed to <GIT_REPO_ROOT>
```

Mark each item done immediately when completed. **Do not proceed to the next phase until the current phase's GATE item is checked.**

---

## Phase 1 — Plan

**Must complete before Phase 2.**

Invoke **`Skill: dotnet-plan`** with the feature description from `$ARGUMENTS`.

The skill will:
1. Launch **dotnet-analyzer** to map the existing solution
2. Search NuGet for reusable packages
3. Launch **dotnet-planner** to produce the plan file

**Output:** `<TARGET_REPO>/doc/plan_<feature-name>.md`

**Skills gate:** `Skill: git-commit` (commit to `<GIT_REPO_ROOT>`)

**STOP — do not proceed to Phase 2 until the plan file is committed.**
If the commit fails for any reason, stop and ask the user how to proceed. Never silently skip this gate.

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

**Skills gate (inside dotnet-coding):** `dotnet format` → `dotnet test` → XML docs → `Skill: git-commit` (commit to `<GIT_REPO_ROOT>`)

**STOP — do not proceed to Phase 3 until all implementation is committed.**
If the commit fails for any reason, stop and ask the user how to proceed. Never silently skip this gate.

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
2. **Invoke `Skill: dotnet-review` again with a NEW agent** — the agent that applied fixes must not verify its own work
3. Repeat until no CRITICAL or HIGH issues remain

### If Review Passes

**Skills gate:** `dotnet format --verify-no-changes` → `Skill: git-commit` (commit to `<GIT_REPO_ROOT>`)

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
