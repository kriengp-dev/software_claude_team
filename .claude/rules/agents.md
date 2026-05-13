# Agent Usage Rules

When to use each subagent, in what order, and under what conditions.

---

## Key Principles

1. **Agent-First**: Delegate to specialized agents for complex work — do not handle multi-step embedded tasks inline.
2. **Parallel by default**: Launch independent agents simultaneously; only serialize when one agent's output is another's input.
3. **Right agent, right scope**: Match the agent to the task type; do not use a general agent when a specialized one exists.

---

## Standard Workflow (Feature Development)

```
c-planner → c-developer → c-reviewer → [c-build-resolver if needed]
```

---

## Parallel Task Execution

ALWAYS use parallel agent execution for independent operations:

```markdown
# GOOD: Parallel execution
Launch agents in parallel:
1. Agent 1: c-reviewer  — review new driver code
2. Agent 2: c-developer — write unit tests for the same driver

# BAD: Sequential when unnecessary
First c-reviewer, then c-developer (when neither depends on the other's output)
```

**Independent = safe to parallelize:**
- c-analyser on module A + c-analyser on module B
- c-developer writing tests + c-reviewer reviewing implementation
- c-planner drafting a plan + c-analyser mapping an unfamiliar module

**Must serialize (output → input dependency):**
- c-planner must finish before c-developer starts (developer needs the plan)
- c-developer must finish before c-reviewer starts (reviewer needs the code)
- c-build-resolver must finish before c-reviewer starts (reviewer needs a passing build)

---

## c-planner

**Use when:**
- User requests a new feature with multiple files or cross-layer changes (driver / middleware / application)
- A refactor touches more than 3 files
- It is unclear which files need to change

**Skip when:**
- Target files are known and fewer than 3 files change
- Fixing a single isolated bug

**Output:** `doc/plan_<feature>.md` inside the target repo

---

## c-developer

**Use when:**
- Writing new C code (driver, middleware, application logic)
- Implementing according to a plan produced by c-planner
- Writing unit tests (TDD or test-after)

**Requirements:**
- Always confirm `<TARGET_REPO>` first — never write files into the Claude project
- Ask about TDD once before starting; do not ask again
- Must invoke `/c-coding-standard` and `/c-doxygen-standard` before every commit

**Called after:** c-planner (if a plan exists) or directly for small tasks

---

## c-reviewer

**Use when:**
- After c-developer writes or modifies any `.c` or `.h` file
- Before merging a branch into main
- Cleaning up dead code or duplicate logic

**Mandatory:** Must be invoked after every C code change — no exceptions.

**Internal order:**
1. Section 1 — Code Review (CRITICAL / HIGH / MEDIUM issues)
2. Section 2 — Refactor & Dead Code Cleanup (only when build and tests pass)

---

## c-build-resolver

**Use when:**
- Build fails with compilation, linker, or toolchain errors
- Error messages include `undefined reference`, `section overlaps`, `implicit declaration`

**Do not use when:**
- The error is a logic bug, not a build error — use c-developer instead

**Principle:** Apply surgical fixes only; do not refactor while resolving a build error.

---

## c-analyser

**Use when:**
- Encountering an unfamiliar codebase and needing to map its structure
- Needing ISR mapping before touching interrupt code
- Identifying unused code before a refactor
- Needing a function call hierarchy before adding a feature

**Output:** Markdown report in `doc/` of the target repo — never modifies source files.

**Called before:** c-planner or c-developer when the codebase is unfamiliar.

---

## deep-research-specialist

**Use when:**
- Need authoritative information from external sources (datasheets, application notes, standards)
- Comparing RTOS options, protocols, or middleware libraries
- Finding best practices for embedded patterns (DMA, watchdog, low-power, bootloader, OTA)
- Clarifying a standard (MISRA, AUTOSAR, ISO 26262, IEC 62443)
- Investigating unknown behaviour by searching vendor documentation
- Any technical topic requiring web search beyond the local codebase

**Skip when:**
- The answer is derivable from reading the local codebase — use c-analyser instead
- The question is about implementation details — use c-planner or c-developer

**Output:** Summary in chat (quick/standard) or Markdown report saved to `output/` in this Claude project (deep dive) — never committed.

**Can run in parallel with:** c-planner (research informs the plan), c-analyser (both are read-only)
