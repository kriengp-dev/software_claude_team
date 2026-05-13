---
description: Add or verify Doxygen comments on all C functions, types, and files being written or modified. Apply this before presenting or committing any .c or .h files.
---

Follow the Doxygen comment rules defined in `.claude/skills/c-doxygen-standard/SKILL.md` exactly.

Steps:
1. Ask the user for the `@author` name before writing any code (Step 1 in the skill)
2. Apply all rules to every `.c` and `.h` file in scope:
   - Rule 1: File header (`@file`, `@brief`, `@author`)
   - Rule 2: Public functions (`@brief`, `@param[direction]`, `@return`)
   - Rule 3: Structs and typedefs
   - Rule 4: Enums
   - Rule 5: Macros and constants
   - Rule 6: Private (static) functions
3. Run through the Application Checklist before presenting any code

$ARGUMENTS
