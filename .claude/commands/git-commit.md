---
description: Apply git branching, commit message format, and PR workflow rules before making any commit or opening a pull request.
---

Follow the rules defined in `.claude/skills/git-commit/SKILL.md` exactly.

Steps:
1. Check the current branch — if it is `main` or `master`, create a feature branch first using the correct prefix
2. **Separate commits per change type** — never mix in one commit:
   - Scan all changed files and group by type
   - If multiple types exist → create **one commit per type**, following the order and rules defined in the **"Separate Commits by Change Type"** section of `.claude/skills/git-commit/SKILL.md`
   - Stage only the files for the current type before each commit; do not stage across types
3. Determine the commit author line:
   - **If called from a subagent** (c-developer, c-reviewer, c-build-resolver, c-analyser, c-planner): use `subagent: <agent-name>`
   - **If called directly by the user** (no subagent context): ask the user — "What is your name for this commit?" — then use `author: <name>`
   - If the user declines to provide a name: omit the author line entirely
4. Write the commit message:
   ```
   <type>: <description>
   subagent: <agent>        ← if called from a subagent
   author: <name>           ← if called directly by user (and name provided)
   ```
5. Run through the Commit Checklist before finalizing

$ARGUMENTS
