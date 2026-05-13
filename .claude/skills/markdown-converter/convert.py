#!/usr/bin/env python3
"""
Unified CLI for markdown-converter skill.

Routes to the correct huashu-md-html script based on conversion mode.
Run setup.py once before first use.

Usage:
    python convert.py <mode> [args...]

Modes:
    any-to-md   PDF/DOCX/PPTX/image/audio/URL -> Markdown
    md-to-html  Markdown -> styled HTML  (themes: article/report/reading/interactive)
    html-to-md  HTML file or URL -> Markdown
    md-to-docx  Markdown -> Word document (supports book mode)

Examples:
    python convert.py any-to-md report.pdf -o report.md
    python convert.py any-to-md https://example.com -o page.md
    python convert.py md-to-html doc.md --theme report --toc -o doc.html
    python convert.py md-to-html doc.md --theme interactive --inline-images
    python convert.py html-to-md https://example.com -o page.md
    python convert.py html-to-md page.html --engine markdownify
    python convert.py md-to-docx chapter.md -o output.docx
    python convert.py md-to-docx ch1.md ch2.md --book --title "My Book" --author "Name"
"""

import argparse
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).parent
TOOLS_DIR = SKILL_DIR / "tools"
SCRIPTS_DIR = TOOLS_DIR / "scripts"

SCRIPT_MAP = {
    "any-to-md":  "any_to_md.py",
    "md-to-html": "md_to_html.py",
    "html-to-md": "html_to_md.py",
    "md-to-docx": "md_to_docx.py",
}

MODE_HELP = {
    "any-to-md": (
        "Convert any file or URL to Markdown.\n"
        "Supports: PDF, DOCX, PPTX, XLSX, EPUB, images, audio, YouTube URLs.\n"
        "Key options:\n"
        "  -o <output.md>          output path (default: <source>.md)\n"
        "  --llm-describe          use AI to describe images (needs OPENAI_API_KEY)\n"
        "  --quiet                 suppress progress messages"
    ),
    "md-to-html": (
        "Convert Markdown to styled, self-contained HTML.\n"
        "Themes:\n"
        "  article     Tufte-inspired essay layout (default)\n"
        "  report      Wide-body for technical documents and dense tables\n"
        "  reading     Minimal Medium-style single-column layout\n"
        "  interactive Long-form with collapsible TOC and sidebar\n"
        "Key options:\n"
        "  -o <output.html>        output path\n"
        "  --theme <name>          choose theme (default: article)\n"
        "  --toc                   add table of contents\n"
        "  --inline-images         embed images as base64\n"
        "  --katex                 render math via KaTeX\n"
        "  --title <text>          override document title"
    ),
    "html-to-md": (
        "Extract and convert HTML (file or URL) to Markdown.\n"
        "Strips navigation, sidebars, ads automatically for URLs.\n"
        "Key options:\n"
        "  -o <output.md>          output path\n"
        "  --engine auto|html-to-markdown|markdownify\n"
        "  --no-extract            skip trafilatura content extraction\n"
        "  --user-agent <string>   custom UA header for fetches"
    ),
    "md-to-docx": (
        "Convert Markdown to Word document (.docx).\n"
        "Standard mode:  single document, A4 or book page size.\n"
        "Book mode:      auto cover, TOC, chapter breaks, headers/footers.\n"
        "Key options:\n"
        "  -o <output.docx>        output path\n"
        "  --page-size book|a4     page format (default: book)\n"
        "  --book                  enable book mode\n"
        "  --title <text>          book title (required with --book)\n"
        "  --subtitle <text>       book subtitle\n"
        "  --author <text>         author name\n"
        "  --chapter-labels <csv>  e.g. 'Chapter 1,Chapter 2,Epilogue'"
    ),
}


def check_setup():
    if not SCRIPTS_DIR.exists():
        print("ERROR: markdown-converter tools not installed.")
        print(f"Run setup first:")
        print(f"  python \"{SKILL_DIR / 'setup.py'}\"")
        sys.exit(1)


def run_mode(mode, extra_args):
    script = SCRIPTS_DIR / SCRIPT_MAP[mode]
    if not script.exists():
        print(f"ERROR: Script not found: {script}")
        print("Re-run setup.py to restore missing scripts.")
        sys.exit(1)
    cmd = [sys.executable, str(script)] + extra_args
    result = subprocess.run(cmd)
    sys.exit(result.returncode)


def print_mode_help(mode):
    print(f"\nmarkdown-converter {mode}")
    print("-" * 50)
    print(MODE_HELP.get(mode, ""))
    print(f"\nFor full options:")
    print(f"  python convert.py {mode} --help")


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)

    mode = sys.argv[1]

    if mode not in SCRIPT_MAP:
        print(f"ERROR: Unknown mode '{mode}'")
        print(f"Valid modes: {', '.join(SCRIPT_MAP)}")
        sys.exit(1)

    extra_args = sys.argv[2:]

    # Show mode-specific help summary when no source is provided
    if not extra_args or extra_args == ["--help"]:
        print_mode_help(mode)
        if extra_args == ["--help"]:
            print()
            check_setup()
            run_mode(mode, ["--help"])
        sys.exit(0)

    check_setup()
    run_mode(mode, extra_args)


if __name__ == "__main__":
    main()
