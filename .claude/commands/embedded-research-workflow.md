---
description: Launch the deep-research-specialist agent to research embedded systems or C language topics using the embedded-research-workflow skill. Always delegates to the agent — never handles research inline.
---

**Always delegate to the `deep-research-specialist` agent. Do not answer inline.**

Launch the `deep-research-specialist` agent with the following instruction:

> Follow the research workflow defined in `.claude/skills/embedded-research-workflow/SKILL.md` exactly.
>
> Research topic: $ARGUMENTS
>
> Steps:
> 1. Clarify the query — identify target MCU, peripheral, and question type
> 2. Search using the priority source order defined in the skill (vendor docs first)
> 3. Fetch and extract technical details from the most relevant pages
> 4. Cross-validate register values and hardware-specific findings against at least two sources
> 5. Return results in the structured format defined in the skill (Summary → Findings → Code Example → Caveats → Next Steps)
> 6. If no reliable information is found, use the "Not Found" format defined in the skill

$ARGUMENTS
