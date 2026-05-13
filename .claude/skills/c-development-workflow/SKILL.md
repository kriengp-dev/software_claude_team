---
name: c-development-workflow
description: Full embedded C development workflow — orchestrates c-plan → c-coding/c-tdd → c-review in sequence. Each phase delegates to its own agent and applies its own skills gate. Use for any new feature or driver that requires planning, implementation, and review in one workflow.
---

## When to Use

- Starting a new feature, driver, or middleware module end-to-end
- Any work that requires planning before coding and review after coding
- When the full Plan → Implement → Review cycle is needed in one invocation

**Skip when:** fixing a single isolated bug (use `/c-coding` directly) or reviewing existing code only (use `/c-review` directly).

---

## Pre-flight: Ask Once Before Starting

Before launching any agent, ask the user:

```
Implementation mode?
  [T] TDD  — write failing tests before implementation (RED-GREEN-REFACTOR)
  [C] Code — implement first, add tests after
```

Store as `<MODE>`. Do not ask again during the workflow.

---

## Phase 1 — Plan

**Must complete before Phase 2 starts.**

Invoke **`Skill: c-plan`** with the feature description from `$ARGUMENTS`.

The skill will:
1. Run research in parallel: deep-research-specialist (vendor docs) + GitHub code search
2. Run c-analyser on the target repo (after research completes)
3. Launch c-planner agent to produce the plan file

**Output:** `<TARGET_REPO>/doc/plan_<feature-name>.md` containing PRD, Architecture, System Design, API Contract, and Task List.

**Skills gate (inside c-plan):** `Skill: git-commit`

Do not proceed to Phase 2 until the plan file exists and has been committed.

---

## Phase 2 — Implement

**Starts only after Phase 1 is complete. Uses the plan file as input.**

### If `<MODE>` = TDD

Invoke **`Skill: c-tdd`** with:
- Feature description: `$ARGUMENTS`
- Plan file path: `<TARGET_REPO>/doc/plan_<feature-name>.md`
- Instruction: TDD=Y is forced — agent skips the TDD question and proceeds directly to RED phase

### If `<MODE>` = Code

Invoke **`Skill: c-coding`** with:
- Feature description: `$ARGUMENTS`
- Plan file path: `<TARGET_REPO>/doc/plan_<feature-name>.md`
- The c-developer agent follows the plan (Case A) and implements directly

**Skills gate (inside c-tdd / c-coding):** `Skill: c-coding-standard` → `Skill: c-doxygen-standard` → `Skill: git-commit`

Do not proceed to Phase 3 until implementation is committed and all tests pass.

---

## Phase 3 — Review

**Starts only after Phase 2 is complete.**

Invoke **`Skill: c-review`** with the target repo path from Phase 1/2.

The skill will:
1. Run `git diff -- '*.c' '*.h'` to identify all files changed in Phase 2
2. Run `cppcheck` and the project build
3. Review all modified files against CRITICAL / HIGH / MEDIUM priorities

### If review finds CRITICAL or HIGH issues

- c-reviewer reports the blocking issues
- Invoke **`Skill: c-coding`** to fix the issues (pass the review findings as input)
- Invoke **`Skill: c-review`** again to confirm resolution
- Repeat until no CRITICAL or HIGH issues remain

### If review passes (no CRITICAL or HIGH)

**Skills gate (inside c-review):** `Skill: c-coding-standard` → `Skill: c-doxygen-standard` → `Skill: git-commit`

---

## Execution Order

```
Ask <MODE> (T or C)
        │
        ▼
[Phase 1] Skill: c-plan ──────────────────────────────── commit: docs: add plan
        │
        ▼ (plan file ready)
[Phase 2] Skill: c-tdd (if T) / Skill: c-coding (if C) ─ commit: feat: ...
        │
        ▼ (implementation committed, tests pass)
[Phase 3] Skill: c-review ────────────────────────────── commit: fix: ... (if fixes needed)
        │
        ▼
  Done — all three phases committed, ready for PR
```

---

## Key Principles

1. **Sequential only** — Phase 2 cannot start before Phase 1 output exists; Phase 3 cannot start before Phase 2 is committed
2. **Agent-first** — every phase delegates to its own agent; never implement or review inline
3. **Single MODE decision** — ask TDD vs Code once at the start; do not re-ask in Phase 2
4. **Review loop** — if CRITICAL or HIGH issues are found in Phase 3, fix and re-review before declaring done
5. **Each phase owns its skills gate** — this skill orchestrates phases; individual skills handle c-coding-standard, c-doxygen-standard, and git-commit
