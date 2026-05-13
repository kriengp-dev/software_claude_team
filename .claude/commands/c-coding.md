---
description: Embedded C implementation workflow via c-developer agent — implement-first or TDD (user chooses), then applies c-coding-standard, c-doxygen-standard, and git-commit.
---

Follow the workflow defined in `.claude/skills/c-coding/SKILL.md` exactly.

Task: $ARGUMENTS

---

## Execution

### Step 1 — Launch c-developer Agent

Launch **c-developer** agent with:
- Task: $ARGUMENTS
- The agent will ask the user once about TDD preference (Y/N)
- If Y: RED-GREEN-REFACTOR cycle (tests before implementation)
- If N: implement directly, add tests before committing
- The agent must follow Steps 0 → 9 from its instruction set

### Step 2 — Skills Gate (after agent completes)

Invoke in this exact order on every `.c`/`.h` file written or modified:

1. **Skill: c-coding-standard** — naming, types, brace style, ISR rules, include hygiene
2. **Skill: c-doxygen-standard** — `@file`, `@brief`, `@param`, `@return` on all functions and types
3. **Skill: git-commit** — branch rules, commit message format (`feat`/`fix`/`refactor` + `subagent: c-developer`)

$ARGUMENTS
