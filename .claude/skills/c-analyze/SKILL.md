---
name: c-analyze
description: Source code and software project analysis for embedded C/C++ repositories. Defines the scope, analysis steps, and report format used by the c-analyser agent when mapping an unfamiliar codebase.
---

## When to Use

- Before adding a feature to an unfamiliar codebase — understand structure first
- Before refactoring — identify unused code and dependencies
- Before touching interrupt code — map ISR sources and handlers
- When onboarding to a new embedded project — get the full picture quickly

---

## Analysis Scope

Define what to analyse before starting. Choose one or more:

| Scope | What it covers |
|-------|---------------|
| **Module overview** | File list, purpose per module, public API, include dependencies |
| **Call hierarchy** | Function call trees from entry points (main, tasks, ISRs) |
| **ISR mapping** | Interrupt vector → handler → peripheral → shared variables |
| **Unused code** | Functions, macros, typedefs with no callers or references |
| **Shared state** | Global and volatile variables, extern declarations, concurrency risks |
| **Full analysis** | All of the above |

---

## Analysis Steps

### Step 1 — Discover Files

Locate all relevant source files in the target repo:
- `**/*.c` — translation units
- `**/*.h` — headers
- `**/*.s` / `**/*.S` — startup and assembly (vector table)
- `**/CMakeLists.txt`, `**/Makefile` — build system
- `**/linker*.ld`, `**/*.ld` — linker scripts

Count lines of code per file. Sort by size to identify the heaviest modules.

### Step 2 — Module Structure

For each `.c` file:
- Read the file header for purpose
- List public functions (from paired `.h`)
- List `static` (private) functions
- List global and static variables
- Note `#include` dependencies

Produce a **module table**:

| File | Purpose | Public API | Key Dependencies |
|------|---------|-----------|-----------------|

### Step 3 — Function Call Hierarchy

Trace call trees from entry points (`main`, RTOS tasks, ISR handlers). Depth ≤ 5 levels. Use grep cross-reference to find callers and callees.

```
main()
├── system_init()
│   ├── clock_config()
│   └── gpio_init()
└── app_run()
    └── sensor_read()
```

For large codebases, produce one tree per entry point or module.

### Step 4 — ISR Mapping

Find the vector table (startup `.s` or `*_it.c`). For each ISR:
- Which peripheral it services
- Which shared variables it modifies (check `volatile`)
- Which semaphore/queue/flag it signals

Produce an **ISR mapping table**:

| Vector / IRQ Name | Handler | Peripheral | Action | Shared Variables |
|-------------------|---------|-----------|--------|-----------------|

Flag any ISR that calls a blocking function, accesses shared data without a critical section, or is defined but never enabled.

### Step 5 — Unused Code

Cross-reference all defined symbols against all call sites:
- Functions defined but never called
- Macros defined but never referenced
- Typedefs replaced by newer ones

Do **not** flag: weak ISR stubs, HAL callbacks, symbols with `__attribute__((used))`, startup symbols.

Classify confidence: HIGH (no callers anywhere) / MEDIUM (may be used by external tool or linker).

### Step 6 — Shared State & Data Flow

Identify all non-local mutable state:
- Global variables and their writers/readers
- `volatile` variables shared with ISRs
- `extern` declarations

Produce a **shared state table**:

| Variable | Type | Declared In | Written By | Read By | ISR-safe? |
|----------|------|------------|-----------|--------|----------|

### Step 7 — Developer Notes & Risks

Summarise findings in plain language:
- **Architecture summary** — layered / flat / RTOS / bare-metal
- **Key entry points** — `main()`, RTOS tasks, ISR entry points
- **Known risks** — missing `volatile`, blocking ISR calls, unused dangerous paths, include cycles, functions > 50 lines or > 4 nesting levels
- **Recommended next steps** — prioritised action list

---

## Report Format

Save the report to `<target-repo>/doc/analysis_<slug>_<YYYYMMDD>.md`.

```markdown
# C Code Analysis Report
**Target:** `<path>`
**Date:** YYYY-MM-DD
**Scope:** <selected scope>

---

## 1. Module Overview
...

## 2. Function Call Hierarchy
...

## 3. ISR Mapping
...

## 4. Unused Code
...

## 5. Shared State & Data Flow
...

## 6. Developer Notes & Risks
...

## 7. Recommended Next Steps
...
```

---

## Key Principles

1. **Read before reporting** — always read source files; never infer from filenames alone
2. **Cite evidence** — every claim links to a file path and line number
3. **No source modifications** — analysis is read-only; only the report is written
4. **Structured tables** — use Markdown tables for all mappings
5. **Flag risks clearly** — use `> ⚠️ WARNING:` for ISR safety, concurrency, and missing critical sections
