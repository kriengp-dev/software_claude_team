---
description: TDD workflow for embedded C — forces RED-GREEN-REFACTOR cycle via c-developer agent, then applies c-coding-standard, c-doxygen-standard, and git-commit.
---

**TDD mode is mandatory. Do not ask the user — TDD=Y is set automatically.**

Follow the workflow defined in `.claude/skills/c-tdd/SKILL.md` exactly.

Task: $ARGUMENTS

---

## Execution

### Step 1 — Launch c-developer Agent (TDD=Y forced)

Launch **c-developer** agent with:
- Task: $ARGUMENTS
- Instruction to the agent: **TDD=Y — skip the TDD question and proceed directly to writing failing tests (Step 4) before any implementation**
- The agent must follow Steps 0 → 9 from its instruction set
- RED phase: tests must be written and confirmed failing before GREEN phase begins
- GREEN phase: implement only enough to make tests pass
- IMPROVE phase: refactor while tests stay green

### Step 2 — Skills Gate (after agent completes)

Invoke in this exact order on every `.c`/`.h` file written or modified:

1. **Skill: c-coding-standard** — naming, types, brace style, ISR rules, include hygiene
2. **Skill: c-doxygen-standard** — `@file`, `@brief`, `@param`, `@return` on all functions and types
3. **Skill: git-commit** — branch rules, commit message format (`feat`/`fix`/`test`/`refactor` + `subagent: c-developer`)

$ARGUMENTS
