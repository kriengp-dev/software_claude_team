---
description: Embedded C dead code and refactor workflow via c-reviewer agent — identifies and removes unused symbols, duplicate logic, and orphaned headers on a stable codebase, then applies c-coding-standard, c-doxygen-standard, and git-commit.
---

Follow the workflow defined in `.claude/skills/c-refactor/SKILL.md` exactly.

Scope / project path: $ARGUMENTS

---

## Execution

### Prerequisite Check

Before launching the agent, confirm:
- [ ] Build passes with no errors
- [ ] All host-side unit tests are green
- [ ] No active feature development on the same files

If any prerequisite fails, stop and notify the user.

### Step 1 — Launch c-reviewer Agent (Section 2 — Refactor & Dead Code Cleanup)

Launch **c-reviewer** agent with:
- Project path / scope: $ARGUMENTS
- Focus: **Section 2 — Refactor & Dead Code Cleanup** (skip Section 1 unless explicitly requested)
- The agent must:
  1. Analyze and categorize candidates (SAFE / CAREFUL / RISKY)
  2. Verify each candidate by grep before deleting
  3. Remove one category at a time (macros → static functions → headers → duplicates)
  4. Build and run tests after each batch before proceeding
  5. Apply optimizations (`const`, struct-by-pointer, loop invariants) after cleanup

### Step 2 — Skills Gate (after each passing batch)

Invoke in this exact order on every `.c`/`.h` file modified in the batch:

1. **Skill: c-coding-standard** — naming, types, brace style, ISR rules, include hygiene
2. **Skill: c-doxygen-standard** — `@file`, `@brief`, `@param`, `@return` on all functions and types
3. **Skill: git-commit** — branch rules, commit message format (`refactor: <description>` + `subagent: c-reviewer`)

Commit after each passing batch — not all at once.

$ARGUMENTS
