---
name: c-build-resolve
description: Embedded C build error resolution workflow. Delegates to the c-build-resolver agent to fix compilation, linker, and toolchain errors with minimal surgical changes, then invokes c-coding-standard, c-doxygen-standard, and git-commit skills.
---

## When to Use

- Build fails with compilation, linker, or toolchain errors
- Error messages include `undefined reference`, `section overlaps`, `implicit declaration`, `conflicting types`
- Toolchain configuration errors (wrong `-mcpu`, `-mthumb`, `-mfpu` flags)

**Do not use for logic bugs — use c-developer instead.**

---

## Workflow

### Mandatory: Delegate to c-build-resolver Agent

**Always launch the c-build-resolver agent. Never fix build errors inline.**

Launch **c-build-resolver** agent with:
- Project path from `$ARGUMENTS`
- Full error output (paste or instruct agent to run the build command)
- The agent detects the build system (Makefile, CMakeLists.txt, .projectSpec) automatically

---

## Resolution Workflow the Agent Follows

```text
1. Run build command      → Parse error message
2. Read affected file     → Understand context
3. Apply minimal fix      → Only what's needed to fix the error
4. Run build command      → Verify fix succeeded
5. Check for new errors   → Ensure nothing broke
```

---

## Common Error Patterns

| Error | Cause | Fix |
|-------|-------|-----|
| `undefined reference to X` | Missing implementation or library | Add source file or link library |
| `expected ';'` | Syntax error | Fix syntax |
| `use of undeclared identifier` | Missing include or typo | Add `#include` or fix name |
| `multiple definition of` | Duplicate symbol | Remove duplicate or use `static` |
| `cannot convert X to Y` | Type mismatch | Add explicit cast or fix types |
| `implicit declaration of function` | Missing prototype or include | Add declaration or correct header |
| `conflicting types for` | Mismatched declaration and definition | Align prototype with implementation |
| `undefined reference to Reset_Handler` | Missing startup file | Add startup `.s`/`.c` to build |
| `section overlaps` | Linker script region conflict | Adjust memory regions in `.ld` |
| `relocation truncated to fit` | Branch target out of range | Check memory map, use far-call workaround |

---

## Stop Conditions

The agent stops and reports if:
- Same error persists after 3 fix attempts
- Fix introduces more errors than it resolves
- Error requires architectural changes beyond scope (e.g., linker script redesign)

---

## Mandatory Skills Gate (Pre-Commit)

After the build succeeds and before committing, invoke all three skills in order:

1. **Invoke `Skill: c-coding-standard`** — on every `.c`/`.h` file modified during the fix
2. **Invoke `Skill: c-doxygen-standard`** — on every `.c`/`.h` file modified during the fix
3. **Invoke `Skill: git-commit`** — branch rules, commit message format, PR process

---

## Commit Format

```
fix: <description>
subagent: c-build-resolver

<optional body>
```

---

## Key Principles

1. **Agent-first** — never fix build errors inline; always delegate to c-build-resolver
2. **Surgical fixes only** — don't refactor, rename, or reorganize while resolving a build error
3. **Never suppress warnings** with `#pragma` or `-w` without explicit user approval
4. **Fix root cause** — never mask symptoms
5. **One fix at a time** — verify after each change before applying the next
6. **Skills gate always runs** — c-coding-standard → c-doxygen-standard → git-commit, no exceptions
