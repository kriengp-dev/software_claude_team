---
description: Full embedded C development workflow — Plan → Implement → Review. Orchestrates c-plan, c-coding/c-tdd, and c-review in sequence. Each phase delegates to its own agent.
---

Follow the workflow defined in `.claude/skills/c-development-workflow/SKILL.md` exactly.

Feature / task: $ARGUMENTS

---

## Step 0 — Ask Implementation Mode (once, before starting)

Ask the user:

```
Implementation mode for: $ARGUMENTS
  [T] TDD  — RED-GREEN-REFACTOR (failing tests before implementation)
  [C] Code — implement first, tests after
```

Store as `<MODE>`. Proceed immediately after the user answers.

---

## Phase 1 — Plan

Invoke **`Skill: c-plan`**:
- Feature: $ARGUMENTS
- The skill runs research → c-planner → produces plan file → git-commit

Wait for the plan file to exist at `<TARGET_REPO>/doc/plan_<feature-name>.md` before proceeding.

---

## Phase 2 — Implement (sequential after Phase 1)

### If `<MODE>` = T (TDD)

Invoke **`Skill: c-tdd`**:
- Task: $ARGUMENTS
- Plan file: `<TARGET_REPO>/doc/plan_<feature-name>.md` (produced in Phase 1)
- Pass to agent: **TDD=Y — skip the TDD question; go directly to Step 4 (RED phase)**

### If `<MODE>` = C (Code)

Invoke **`Skill: c-coding`**:
- Task: $ARGUMENTS
- Plan file: `<TARGET_REPO>/doc/plan_<feature-name>.md` (produced in Phase 1)
- Pass to agent: **Plan is available (Case A) — read it and implement directly**

Wait for implementation to be committed and all tests to pass before proceeding.

---

## Phase 3 — Review (sequential after Phase 2)

Invoke **`Skill: c-review`**:
- Project path: `<TARGET_REPO>` (from Phase 1)
- Scope: all `.c`/`.h` files changed during Phase 2

### If review is BLOCKED (CRITICAL or HIGH issues found)

1. Invoke **`Skill: c-coding`** — fix the issues reported by c-reviewer
2. Invoke **`Skill: c-review`** — re-review to confirm resolution
3. Repeat until review passes

### If review PASSES

Workflow complete. All three phases are committed on the feature branch.
Open a Pull Request via the `git-commit` skill's PR process.

$ARGUMENTS
