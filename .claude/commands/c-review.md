---
description: Embedded C code review via c-reviewer agent — reviews for memory safety, concurrency, and embedded best practices, then applies c-coding-standard, c-doxygen-standard, and git-commit.
---

Follow the workflow defined in `.claude/skills/c-review/SKILL.md` exactly.

Scope / project path: $ARGUMENTS

---

## Execution

### Step 1 — Launch c-reviewer Agent (Section 1 — Code Review)

Launch **c-reviewer** agent with:
- Project path / scope: $ARGUMENTS
- Focus: **Section 1 — Code Review only** (not refactor/cleanup — use `/c-refactor` for that)
- The agent must:
  1. Run `git diff -- '*.c' '*.h'` to identify changed files
  2. Run `cppcheck` on the project path
  3. Run the project build command
  4. Review all modified C files against CRITICAL / HIGH / MEDIUM priorities

### Step 2 — Skills Gate (after agent completes and any fixes are applied)

Invoke in this exact order on every `.c`/`.h` file modified during review:

1. **Skill: c-coding-standard** — naming, types, brace style, ISR rules, include hygiene
2. **Skill: c-doxygen-standard** — `@file`, `@brief`, `@param`, `@return` on all functions and types
3. **Skill: git-commit** — branch rules, commit message format (`fix`/`refactor`/`chore` + `subagent: c-reviewer`)

$ARGUMENTS
