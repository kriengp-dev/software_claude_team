---
description: Embedded C build error resolution via c-build-resolver agent — diagnoses and fixes compilation, linker, and toolchain errors with surgical changes, then applies c-coding-standard, c-doxygen-standard, and git-commit.
---

Follow the workflow defined in `.claude/skills/c-build-resolve/SKILL.md` exactly.

Project path / error description: $ARGUMENTS

---

## Execution

### Step 1 — Launch c-build-resolver Agent

Launch **c-build-resolver** agent with:
- Project path / error output: $ARGUMENTS
- The agent must:
  1. Run the build command and capture the full error output
  2. Run `cppcheck` for static analysis
  3. Identify the root cause — read the affected file for context
  4. Apply the minimal fix required to resolve the error
  5. Re-run the build to verify the fix
  6. Check for newly introduced errors before declaring success

The agent applies **surgical fixes only** — no refactoring, no signature changes, no warning suppression.

### Stop Conditions

The agent stops and reports to the user if:
- Same error persists after 3 fix attempts
- Fix introduces more errors than it resolves
- Error requires architectural changes (linker script redesign, MCU memory map change)

### Step 2 — Skills Gate (after build succeeds)

Invoke in this exact order on every `.c`/`.h` file modified during the fix:

1. **Skill: c-coding-standard** — naming, types, brace style, ISR rules, include hygiene
2. **Skill: c-doxygen-standard** — `@file`, `@brief`, `@param`, `@return` on all functions and types
3. **Skill: git-commit** — branch rules, commit message format (`fix: <description>` + `subagent: c-build-resolver`)

$ARGUMENTS
