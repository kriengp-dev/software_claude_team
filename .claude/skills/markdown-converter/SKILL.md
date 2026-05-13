---
name: markdown-converter
description: Bidirectional document conversion pipeline powered by huashu-md-html. Converts any file/URL to Markdown, Markdown to styled HTML (4 themes), HTML to Markdown, and Markdown to publication-grade DOCX. Scripts are in the same folder as this SKILL.md.
---

## When to Use

- Converting PDF / DOCX / PPTX / image / audio / YouTube URL → Markdown
- Rendering Markdown → beautiful HTML for sharing or publishing
- Archiving a web page or HTML file → clean Markdown
- Producing a Word document from Markdown (standard or book layout)

---

## First-Time Setup (run once)

```bash
python .claude/skills/markdown-converter/setup.py
```

This installs all Python dependencies and clones the huashu-md-html scripts into
`.claude/skills/markdown-converter/tools/`. Re-run if tools/ is missing or outdated.

**Pandoc** is required for `md-to-html` — install separately if missing:
```bash
winget install JohnMacFarlane.Pandoc   # Windows
# or: choco install pandoc
```

---

## Usage — Unified CLI

All conversions go through `convert.py` in the same folder:

```bash
python .claude/skills/markdown-converter/convert.py <mode> [options]
```

---

## Mode 1 — Any Format → Markdown (`any-to-md`)

Converts PDF, DOCX, PPTX, XLSX, EPUB, images, audio, YouTube URLs, and web URLs.

```bash
python convert.py any-to-md <source> [options]
```

| Option | Description |
|--------|-------------|
| `source` | File path or URL (http/https, YouTube) |
| `-o <output.md>` | Output path (default: `<source-name>.md`) |
| `--llm-describe` | AI image descriptions (needs `OPENAI_API_KEY`) |
| `--llm-model <model>` | LLM model for image descriptions (default: `gpt-4o`) |
| `--azure-doc-intel <endpoint>` | Azure OCR for scanned PDFs |
| `--quiet` | Suppress progress messages |

**Examples:**
```bash
python convert.py any-to-md report.pdf -o report.md
python convert.py any-to-md slide_deck.pptx -o slides.md
python convert.py any-to-md https://example.com/article -o article.md
python convert.py any-to-md diagram.png --llm-describe -o described.md
```

---

## Mode 2 — Markdown → HTML (`md-to-html`)

Renders Markdown into a styled, self-contained HTML file using Pandoc.

```bash
python convert.py md-to-html <input.md> [options]
```

| Option | Description |
|--------|-------------|
| `input` | Markdown file path |
| `-o <output.html>` | Output path (default: same name as input) |
| `--theme <name>` | Design theme (default: `article`) |
| `--toc` | Add table of contents |
| `--no-toc` | Disable TOC |
| `--inline-images` | Embed images as base64 data URIs |
| `--copy-images` | Copy images alongside the HTML output |
| `--katex` | Render math via KaTeX CDN |
| `--title <text>` | Override document title |
| `--highlight-style <name>` | Pandoc syntax highlighting (default: `pygments`) |
| `--quiet` | Suppress progress messages |

### Theme Guide

| Theme | Best for |
|-------|---------|
| `article` | Essays, blog posts, long-form writing — Tufte-inspired layout |
| `report` | Technical documents, white papers, dense tables |
| `reading` | Minimal single-column — Medium-style reader experience |
| `interactive` | Long documents with collapsible TOC and sidebar navigation |

**Examples:**
```bash
python convert.py md-to-html doc.md --theme article -o doc.html
python convert.py md-to-html spec.md --theme report --toc -o spec.html
python convert.py md-to-html guide.md --theme reading --inline-images -o guide.html
python convert.py md-to-html manual.md --theme interactive --toc --katex
```

---

## Mode 3 — HTML → Markdown (`html-to-md`)

Extracts clean Markdown from a local HTML file or URL. Strips navigation, sidebars, and ads automatically.

```bash
python convert.py html-to-md <source> [options]
```

| Option | Description |
|--------|-------------|
| `source` | Local `.html` path or URL |
| `-o <output.md>` | Output path (default: `<source-name>.md` or `fetched.md`) |
| `--engine auto\|html-to-markdown\|markdownify` | Conversion engine (default: `auto`) |
| `--no-extract` | Skip trafilatura content extraction for URLs |
| `--strip <tags>` | HTML tags to strip (markdownify only) |
| `--user-agent <string>` | Custom User-Agent header for URL fetches |
| `--quiet` | Suppress progress messages |

**Examples:**
```bash
python convert.py html-to-md https://example.com/article -o article.md
python convert.py html-to-md page.html -o page.md
python convert.py html-to-md https://docs.example.com --no-extract -o raw.md
```

---

## Mode 4 — Markdown → DOCX (`md-to-docx`)

Generates a Word document from one or more Markdown files.

```bash
python convert.py md-to-docx <file.md> [files...] [options]
```

| Option | Description |
|--------|-------------|
| `md_files` | One or more Markdown files |
| `-o <output.docx>` | Output path (default: derived from first file) |
| `--images-dir <dir>` | Directory containing images (default: md file's parent) |
| `--page-size book\|a4` | Page format (default: `book`) |
| `--book` | Enable book mode (cover, TOC, chapter breaks, headers/footers) |
| `--title <text>` | Book title — **required** with `--book` |
| `--subtitle <text>` | Book subtitle |
| `--author <text>` | Author name |
| `--extra-info <text>` | Small text on cover (e.g., `"2026 · Series Name"`) |
| `--chapter-labels <csv>` | Chapter labels (e.g., `"Chapter 1,Chapter 2,Epilogue"`) |

**Examples:**
```bash
# Standard document
python convert.py md-to-docx report.md -o report.docx --page-size a4

# Book with multiple chapters
python convert.py md-to-docx ch1.md ch2.md ch3.md \
    --book --title "Embedded Systems Guide" --author "K. Dev" \
    --subtitle "From HAL to Application" -o book.docx
```

---

## Decision Guide — Which Mode to Use?

```
Source format?
  ├─ PDF / PPTX / XLSX / image / audio / YouTube → any-to-md
  ├─ HTML file or webpage                          → html-to-md
  ├─ Markdown → need to share as webpage?          → md-to-html
  └─ Markdown → need a Word document?              → md-to-docx

Output audience?
  ├─ Reader / blog                                 → md-to-html --theme reading
  ├─ Technical reviewer                            → md-to-html --theme report
  ├─ Long document with navigation                 → md-to-html --theme interactive
  └─ Publisher / print                             → md-to-docx --book
```

---

## File Locations

```
.claude/skills/markdown-converter/
├── SKILL.md        ← this file
├── setup.py        ← run once to install dependencies + clone tools
├── convert.py      ← unified CLI wrapper
└── tools/          ← cloned by setup.py (huashu-md-html repo)
    ├── scripts/
    │   ├── any_to_md.py
    │   ├── md_to_html.py
    │   ├── html_to_md.py
    │   └── md_to_docx.py
    └── templates/  ← HTML themes
```

---

## Key Principles

1. **Setup before use** — always check that `tools/` exists; run `setup.py` if missing
2. **Choose the right theme** — `article` for prose, `report` for technical, `interactive` for long docs
3. **`--inline-images` for portability** — use when sharing a single self-contained HTML file
4. **Book mode requires `--title`** — always pass `--title` when using `--book`
5. **URL extraction is automatic** — `html-to-md` strips ads and navigation by default for URLs
