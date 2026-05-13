---
description: Bidirectional document conversion — any file/URL to Markdown, Markdown to styled HTML, HTML to Markdown, Markdown to DOCX. Powered by huashu-md-html. Run setup.py once before first use.
---

Follow the workflow defined in `.claude/skills/markdown-converter/SKILL.md`.

Task / conversion request: $ARGUMENTS

---

## Execution

### Step 0 — Check Setup

Verify that `tools/` exists next to the skill:

```bash
python .claude/skills/markdown-converter/setup.py
```

If tools/ is already present, setup.py will skip the clone and only verify packages.

### Step 1 — Determine Conversion Mode

From `$ARGUMENTS`, identify:

| If the user wants... | Use mode |
|----------------------|----------|
| PDF / DOCX / PPTX / image / audio / YouTube / URL → Markdown | `any-to-md` |
| Markdown → HTML for web / sharing | `md-to-html` |
| HTML page or URL → Markdown | `html-to-md` |
| Markdown → Word document | `md-to-docx` |

**Theme selection for `md-to-html`** — choose based on content:
- Prose / essay / blog → `--theme article`
- Technical spec / tables → `--theme report`
- Simple readable output → `--theme reading`
- Long document with navigation → `--theme interactive`

### Step 2 — Run Conversion

```bash
python .claude/skills/markdown-converter/convert.py <mode> <source> [options]
```

**Common patterns:**

```bash
# Any file or URL to Markdown
python .claude/skills/markdown-converter/convert.py any-to-md <file|url> -o output.md

# Markdown to styled HTML
python .claude/skills/markdown-converter/convert.py md-to-html input.md --theme article -o output.html
python .claude/skills/markdown-converter/convert.py md-to-html input.md --theme report --toc --inline-images

# HTML or URL to Markdown
python .claude/skills/markdown-converter/convert.py html-to-md <file|url> -o output.md

# Markdown to Word document
python .claude/skills/markdown-converter/convert.py md-to-docx input.md -o output.docx
python .claude/skills/markdown-converter/convert.py md-to-docx ch1.md ch2.md --book --title "Title" --author "Name"
```

### Step 3 — Report Result

After conversion completes, report:
- Output file path
- File size (if relevant)
- Any warnings from the conversion tool

$ARGUMENTS
