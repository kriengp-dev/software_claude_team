---
name: c-tdd
description: TDD workflow for embedded C using the RED-GREEN-REFACTOR cycle. Delegates to the c-developer agent with TDD mode forced, then invokes c-coding-standard, c-doxygen-standard, and git-commit skills.
---

## When to Use

- Writing any new embedded C module, driver, or middleware using test-first discipline
- The user explicitly requests TDD or RED-GREEN-REFACTOR
- A plan exists and the task list includes unit tests before implementation

---

## Workflow

### Mandatory: Delegate to c-developer Agent

**Always launch the c-developer agent. Never implement inline.**

Launch **c-developer** agent with:
- Task description from `$ARGUMENTS`
- Instruction: **TDD mode is forced — answer the TDD question with Y automatically**
- The agent must follow Steps 0 → 9 from its own instruction set
- RED phase (failing tests) must exist and be verified before GREEN phase (implementation)

### TDD Mode Override

Tell the agent explicitly in the prompt:

```
TDD=Y — do not ask the user. Write failing tests before implementation.
Follow RED-GREEN-REFACTOR cycle strictly.
```

---

## Steps the Agent Must Follow

| Step | Action |
|------|--------|
| 0 | Confirm `<TARGET_REPO>` |
| 1 | Check host test toolchain (GCC, CMake, Unity) |
| 2 | Explore `<TARGET_REPO>` for reusable code |
| 3 | Design API (draft header, do not write yet) |
| 4 | Write failing tests (RED) — verify they fail |
| 5 | Implement to make tests pass (GREEN) |
| 6 | Self-review (memory safety, ISR, coverage) |
| 7 | Refactor while tests stay green (IMPROVE) |
| 8 | Verify coverage ≥ 80% (branches, functions, lines) |
| 9 | Skills gate → commit |

---

## Mandatory Skills Gate (Pre-Commit)

After the agent completes and before any commit, invoke all three skills in order:

1. **Invoke `Skill: c-coding-standard`** — on every `.c`/`.h` file written or modified
2. **Invoke `Skill: c-doxygen-standard`** — on every `.c`/`.h` file written or modified
3. **Invoke `Skill: git-commit`** — branch rules, commit message format, PR process

---

## Commit Format

```
<type>: <description>
subagent: c-developer

<optional body>
```

Valid types: `feat`, `fix`, `refactor`, `test`, `chore`, `perf`

---

## Key Principles

1. **Agent-first** — never implement inline; always delegate to c-developer
2. **TDD is non-negotiable** — no implementation line before a failing test
3. **Host-runnable tests** — tests run on Windows host using Unity or CUnit, not on target hardware
4. **Coverage gate** — 80%+ branches, functions, and lines for logic/middleware layers
5. **Skills gate always runs** — c-coding-standard → c-doxygen-standard → git-commit, no exceptions
