---
description: Launch the c-analyser agent to analyse a C/C++ source code project in a target repo. Always delegates to the agent — never handles analysis inline.
---

**Always delegate to the `c-analyser` agent. Do not answer inline.**

Launch the `c-analyser` agent with the following instruction:

> Follow the analysis scope and steps defined in `.claude/skills/c-analyze/SKILL.md` exactly.
>
> Target: $ARGUMENTS
>
> Steps:
> 1. Clarify the target path and analysis scope (module overview / call hierarchy / ISR mapping / unused code / shared state / full)
> 2. Discover all source files under the target path
> 3. Analyse module structure — build the module table
> 4. Trace function call hierarchies from all entry points
> 5. Map ISR vectors to handlers and flag any safety risks
> 6. Identify unused symbols — classify by confidence level
> 7. Map shared state and concurrency risks
> 8. Write the report to `<target-repo>/doc/analysis_<slug>_<YYYYMMDD>.md`
> 9. Commit the report with: `docs: add C code analysis report` / `subagent: c-analyser`

$ARGUMENTS
