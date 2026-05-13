---
name: c-refactor
description: Embedded C refactor and dead code cleanup workflow. Delegates to the c-reviewer agent to identify and remove dead code, duplicate logic, and orphaned headers on a stable codebase, then invokes c-coding-standard, c-doxygen-standard, and git-commit skills.
---

## When to Use

- Cleaning dead code, duplicate logic, or orphaned headers from a stable codebase
- After a build passes and all unit tests are green
- Before a major feature addition to reduce noise
- Identified by c-reviewer as needing a refactor pass (Section 2)

**Never run during active feature development on the same files.**

---

## Workflow

### Mandatory: Delegate to c-reviewer Agent

**Always launch the c-reviewer agent. Never refactor inline.**

Launch **c-reviewer** agent with:
- Project path and scope from `$ARGUMENTS`
- Focus: **Section 2 — Refactor & Dead Code Cleanup** (skip Section 1 code review unless explicitly requested)
- Prerequisite: build must pass and unit tests must be green before the agent starts

---

## What the Agent Does (Section 2)

### 1. Analyze — Build Candidate List

| Risk | Category | Examples |
|------|----------|---------|
| SAFE | Clearly unused, confirmed by grep | Private `static` functions with zero callers, `#define` never referenced |
| CAREFUL | Used via function pointers, macros, or indirect refs | Callback signatures, HAL weak overrides |
| RISKY | Public API or used by external modules | Any symbol declared in a public `.h` |

### 2. Verify Before Delete

For every candidate:
- Grep all `.c` and `.h` files for the exact symbol name
- Check linker scripts (`.ld`), startup files, and assembly (`.s`)
- Check ISR vector tables — never remove weak handler stubs
- Review git log for context

### 3. Remove Safely

- Start with **SAFE** items only
- One category at a time: unused macros → unused static functions → orphaned headers → duplicate logic
- Build and run tests after each batch before proceeding

### 4. Consolidate Duplicates

- Find duplicate utilities (e.g., two `crc16` implementations, two ring buffers)
- Keep the best implementation: most complete, best tested, lowest coupling
- Update all call sites, delete the duplicate, verify build and tests

### 5. Optimize

After dead code removal:

| Category | Check |
|----------|-------|
| `const` correctness | Add `const` to pointer params not modified; const global lookup tables |
| Unnecessary copies | Pass large structs by pointer, not by value |
| Loop invariants | Hoist invariant expressions out of loops |
| Busy-wait → interrupt | Replace polling with interrupt/semaphore where applicable |
| `static inline` helpers | Mark small, frequently-called private helpers `static inline` |

---

## Mandatory Skills Gate (Pre-Commit)

After each batch of changes and before committing, invoke all three skills in order:

1. **Invoke `Skill: c-coding-standard`** — on every `.c`/`.h` file modified
2. **Invoke `Skill: c-doxygen-standard`** — on every `.c`/`.h` file modified
3. **Invoke `Skill: git-commit`** — branch rules, commit message format, PR process

Commit after each passing batch, not all at once.

---

## Commit Format

```
refactor: <description>
subagent: c-reviewer

<optional body>
```

---

## Key Principles

1. **Agent-first** — never refactor inline; always delegate to c-reviewer
2. **Verify before delete** — never trust tooling alone; always grep for the symbol
3. **One category at a time** — batch by type, test after each batch
4. **Conservative on RISKY** — when in doubt, leave it and document it
5. **Never remove embedded safety stubs** — ISR handlers and HAL callbacks must be preserved
6. **Skills gate always runs** — c-coding-standard → c-doxygen-standard → git-commit, no exceptions
