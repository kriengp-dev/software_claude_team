---
name: c-review
description: Embedded C code review workflow. Delegates to the c-reviewer agent to review for memory safety, concurrency, and embedded best practices, then invokes c-coding-standard, c-doxygen-standard, and git-commit skills.
---

## When to Use

- After c-developer writes or modifies any `.c` or `.h` file
- Before merging a branch into main
- Requested peer review of embedded C code
- After receiving code from an external source

---

## Workflow

### Mandatory: Delegate to c-reviewer Agent

**Always launch the c-reviewer agent. Never review inline.**

Launch **c-reviewer** agent with:
- Project path and scope from `$ARGUMENTS`
- Focus: Section 1 — Code Review only (not refactor/cleanup)
- The agent must run `git diff`, `cppcheck`, and the project build before reviewing

---

## Re-review Rule (CRITICAL)

If the c-reviewer agent finds and fixes CRITICAL or HIGH issues:
- **Launch a NEW c-reviewer agent** to confirm the fixes — the agent that applied the fixes must not verify its own work
- The new agent must re-run `cppcheck`, the project build, and re-read every fixed file
- Only when the new agent reports no CRITICAL or HIGH issues may the workflow proceed

---

## What the Agent Reviews

### Section 1 — Code Review (mandatory)

| Priority | Category | Examples |
|----------|----------|---------|
| CRITICAL | Memory Safety | buffer overflow, stack overflow, dangling pointers, null dereference |
| CRITICAL | Embedded Safety | missing `volatile`, missing critical sections, blocking in ISR, wrong integer types |
| CRITICAL | Security | command injection, format string attacks, integer overflow, hardcoded secrets |
| HIGH | Concurrency / RTOS | data races, deadlocks, missing mutex guards, ISR-safe API violations |
| HIGH | Code Quality | functions > 50 lines, deep nesting > 4, missing error handling |
| MEDIUM | Performance | busy-wait polling, unnecessary copies, missing `const` |
| MEDIUM | Best Practices | include hygiene, signed/unsigned mismatch, `sizeof` usage |

### Approval Criteria

- **Approve**: No CRITICAL or HIGH issues found
- **Warning**: MEDIUM issues only — noted for awareness, not blocking
- **Block**: Any CRITICAL or HIGH issue — must be resolved before merge

---

## Mandatory Skills Gate (Pre-Commit)

After the agent completes its review and any fixes are applied, invoke in order:

1. **Invoke `Skill: c-coding-standard`** — on every `.c`/`.h` file modified during review
2. **Invoke `Skill: c-doxygen-standard`** — on every `.c`/`.h` file modified during review
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
subagent: c-reviewer

<optional body>
```

Valid types: `fix`, `refactor`, `chore`

---

## Key Principles

1. **Agent-first** — never review inline; always delegate to c-reviewer
2. **CRITICAL and HIGH block merge** — no exceptions
3. **Section 1 only** — this skill is for review, not refactor; use `/c-refactor` for cleanup
4. **Skills gate always runs** — c-coding-standard → c-doxygen-standard → git-commit, no exceptions
