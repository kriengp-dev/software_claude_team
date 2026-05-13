# Command Usage Rules

When to use each slash command and what it does.

---

## /git-commit

**Use when:**
- Asking Claude to commit with the correct message format
- Verifying branch before committing
- Formatting a commit message that follows project conventions

**What it does:**
1. Checks current branch — creates a feature branch first if on `main`/`master`
2. Stages only files belonging to the same change type
3. Writes commit message in `<type>: <description>` + `subagent: <agent>` format

**Accepts argument:** branch name or commit description (optional)

---

## /c-coding-standard

**Use when:**
- Asking Claude to review and fix C code in scope against the coding standard
- Before committing `.c`/`.h` files
- After receiving code from an external source that needs to be normalized

**What it does:**
- Checks all 13 rule categories in the c-coding-standard skill
- Applies fixes and presents a checklist before returning

**Accepts argument:** file name or module to check (optional)

---

## /c-doxygen-standard

**Use when:**
- Adding or fixing Doxygen comments in `.c`/`.h` files
- Before committing `.c`/`.h` files
- After adding a new function, struct, or enum

**What it does:**
1. Asks user for `@author` name
2. Applies file header, function doc, struct/enum/macro doc per all rules
3. Presents a checklist before returning

**Accepts argument:** file name or module to apply (optional)

---

## /markdown-converter

**Output directory:** Always save converted files to `output/` (relative to project root). Create `output/` if it does not exist.

**What it does:**
- `any-to-md` — converts PDF / DOCX / PPTX / image / URL → Markdown
- `md-to-html` — renders Markdown → styled HTML (themes: article, report, reading, interactive)
- `html-to-md` — extracts clean Markdown from HTML file or URL
- `md-to-docx` — generates Word document from Markdown

**Example:**
```bash
python .claude/skills/markdown-converter/convert.py any-to-md report.pdf -o output/report.md
```

---

## Order before committing

```
/c-coding-standard → /c-doxygen-standard → /git-commit
```
