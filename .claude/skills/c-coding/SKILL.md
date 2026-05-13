---
name: c-coding
description: Embedded C implementation workflow without forced TDD. Delegates to the c-developer agent, then invokes c-coding-standard, c-doxygen-standard, and git-commit skills.
---

## When to Use

- Writing new embedded C code (driver, middleware, application logic) without a strict TDD requirement
- Implementing according to a plan produced by c-planner
- Adding tests after implementation (test-after workflow)
- Small to medium tasks where the target files are already known

---

## Workflow

### Mandatory: Delegate to c-developer Agent

**Always launch the c-developer agent. Never implement inline.**

Launch **c-developer** agent with:
- Task description from `$ARGUMENTS`
- The agent will ask the user once whether to use TDD (answer determines Step 4 vs direct Step 5)
- The agent must follow Steps 0 → 9 from its own instruction set

---

## Steps the Agent Must Follow

| Step | Action |
|------|--------|
| 0 | Confirm `<TARGET_REPO>` |
| 1 | Check host test toolchain (GCC, CMake, Unity) |
| 2 | Explore `<TARGET_REPO>` for reusable code |
| 3 | Design API (draft header, do not write yet) |
| 4 | TDD decision — ask user once; if N, skip to Step 5 |
| 5 | Implement (GREEN) — write correct, safe, minimal C code |
| 6 | Self-review (memory safety, ISR safety, error handling) |
| 7 | Refactor while tests stay green |
| 8 | Add tests after implementation if TDD=N; verify coverage ≥ 80% |
| 9 | Skills gate → commit |

---

## Mandatory Skills Gate (Pre-Commit)

After the agent completes and before any commit, invoke in order:

1. **Invoke `Skill: c-coding-standard`** — on every `.c`/`.h` file written or modified
2. **Invoke `Skill: c-doxygen-standard`** — on every `.c`/`.h` file written or modified
3. Resolve the project git repo root:
   ```bash
   git -C "<TARGET_REPO>" rev-parse --show-toplevel
   ```
   Commit goes to **this repo**, not the Claude project repo.
   If no repo found — STOP and ask the user which repo to use. Never run `git init`.
4. **Invoke `Skill: git-commit`** — branch rules, commit message format, PR process

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
2. **Safety always** — no undefined behavior, no buffer overflows, no data races
3. **Minimal footprint** — static allocation only; no heap on bare-metal targets
4. **Tests required** — add tests before committing whether TDD=Y or TDD=N
5. **Skills gate always runs** — c-coding-standard → c-doxygen-standard → git-commit, no exceptions
