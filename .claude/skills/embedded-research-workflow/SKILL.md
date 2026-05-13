---
name: embedded-research-workflow
description: Step-by-step research workflow for embedded systems and C language topics. Defines how to search, fetch, validate, and present technical findings from datasheets, application notes, vendor SDKs, and community sources.
origin: user-provided
---

## When to Use

- Researching MCU-specific peripheral behaviour, register values, or timing
- Finding vendor datasheet sections, application notes, or errata
- Looking up RTOS internals, HAL API behaviour, or driver examples
- Validating community solutions against official vendor documentation

---

## Research Workflow

### Step 1 — Define Problem (What + Why)

Lock the target before searching. Answer both questions explicitly:

- **What**: What exactly are we looking for? (error code definition / peripheral behaviour / solution / trade-off)
- **Why**: Why does this matter? (to fix a bug / make a design decision / write a plan)

> Example: What: "EtherCAT error -20 meaning" / Why: "To resolve communication failure on the production board"

Do not proceed until both are clear. If ambiguous, state your assumption and continue.

### Step 2 — Scope & Context (Where + When)

Narrow the search space before fetching anything:

- **Where**: In what context does this apply? (bare-metal / RTOS / Linux driver / FPGA / specific HAL layer)
- **When**: Which version? (silicon revision, SDK version, kernel version, RTOS release)
  - Outdated datasheets are a leading cause of wrong fixes — always pin the version

> Example: Where: Linux driver + FPGA interface / When: Kernel 5.x + vendor SDK latest release

### Step 3 — Source Strategy (4 Tiers)

Choose sources in priority order — never skip a tier unless it yields nothing:

| Tier | Type | Embedded examples |
|------|------|------------------|
| **Primary** | Official specs & docs | Datasheet, reference manual, application note, errata, CMSIS spec |
| **Secondary** | Expert-written articles | Vendor blog, Embedded Artistry, interrupt.memfault.com, SEGGER knowledge base |
| **Community** | Peer experience | Stack Overflow, GitHub issues, forums.st.com, esp32.com, AVR Freaks, EEVblog |
| **Empirical** | Observed evidence | Debug logs, logic analyzer captures, oscilloscope readings, test results |

**Rule:** Always start from Primary and work down. Community answers are hypothesis generators — verify against Primary before trusting.

Construct targeted queries:
```
<MCU family> <peripheral> <specific keyword> site:st.com
STM32 DMA circular mode reference manual
RP2040 SPI hardware errata site:raspberrypi.com
FreeRTOS task notification vs semaphore
```

### Step 4 — Decompose (Sub-questions)

Break the main question into smaller, independently searchable questions:

1. What is it? (definition, purpose)
2. What causes it? (root cause, trigger condition)
3. Under what conditions does it occur? (version, config, load, timing)
4. What solutions exist? (workaround, fix, alternative)
5. What are the trade-offs? (performance, safety, complexity)

Search and fetch answers for each sub-question separately. Do not try to answer all at once from a single source.

### Step 5 — Data Collection (Structured Notes)

For every useful piece of information found, record in this format — do not read passively:

```
Fact:    <the technical claim — register value, API behaviour, timing spec>
Source:  <document title, section, page> — <URL>
Insight: <why this matters for the current problem>
Doubt:   <anything uncertain, conflicting, or version-restricted>
```

Capture every relevant fact this way before moving to validation. This prevents losing context mid-research.

### Step 6 — Validation (Cross-check Authority)

Before accepting any finding, validate it:

- Compare across at least **2 sources** for register-level or safety-critical claims
- Check **who** the source is — apply authority hierarchy:
  - Vendor official > independent expert > community post > forum speculation
- If sources conflict: **trust official over expert over community**
- Flag all conflicts explicitly — do not silently pick one

### Step 7 — Synthesis (Actionable Output)

Produce output the developer can use immediately:

Answer these three questions:
1. **Root cause** — what is actually happening and why?
2. **Best solution** — which fix/approach fits this specific context?
3. **Applicability** — does it apply to our version, hardware, and constraints?

Present as one of:
- **Checklist** — for step-by-step fix or setup
- **Decision table** — for choosing between options (trade-off comparison)
- **Structured finding** — for research-style output (see format below)

---

### Output Format

```
## Research Result: <topic>

### Summary
<2–4 sentences: direct answer — root cause + best solution>

### Problem Definition
- What: <locked target from Step 1>
- Why: <motivation from Step 1>
- Scope: <context + version from Step 2>

### Findings

#### [Sub-question / Finding title]
Fact:    <technical detail — register name, value, timing, API behaviour>
Source:  <document title, section> — <URL> (Revision: <if known>)
Insight: <why this matters>
Doubt:   <any uncertainty or version restriction>

### Code Example (if applicable)
```c
/* Source: <URL> */
<embedded-safe C code — fixed-width types, no dynamic allocation>
```

### Trade-offs
| Option | Pros | Cons | Use when |
|--------|------|------|----------|
| ...    | ...  | ...  | ...      |

### Caveats / Errata
- <Silicon errata ID, version restriction, or source conflict>

### Recommended Next Steps
- <Specific action with file, section, or tool reference>
```

If no reliable information is found:
```
## Research Result: <topic>

### Not Found

Sub-questions searched:
- <question> — <query used> — <result summary>

Conflicts: <any contradictory information found>
Suggested action: <where to look manually — specific datasheet section or vendor support channel>
```

---

## Rules

- **Never fabricate register values, addresses, or timing specs** — only report what is explicitly found
- **Always cite the source URL and document section** for every technical claim
- **Note the document revision** when returning datasheet or reference manual content — specs change between silicon revisions
- **Prefer official vendor docs over community posts** for register-level details
- **Prefer community posts** for integration patterns, gotchas, and real-world usage
- **Flag errata** — if a known errata affects the finding, highlight it clearly
- **Write code examples in C** — no C++, Python, or pseudo-code unless explicitly asked
- **Keep code embedded-safe** — no dynamic allocation, use fixed-width types (`uint8_t`, `uint32_t`)
