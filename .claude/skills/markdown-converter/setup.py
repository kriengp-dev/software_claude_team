#!/usr/bin/env python3
"""
Setup script for markdown-converter skill.

Run once before first use:
    python .claude/skills/markdown-converter/setup.py

What this does:
  1. Installs all Python dependencies via pip
  2. Clones huashu-md-html scripts into tools/ (next to this file)
  3. Checks for pandoc (required for md->html)
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).parent
TOOLS_DIR = SKILL_DIR / "tools"
REPO_URL = "https://github.com/alchaincyf/huashu-md-html.git"

PYTHON_DEPS = [
    "markitdown[all]",
    "html-to-markdown",
    "trafilatura",
    "markdownify",
    "python-docx",
    "Pillow",
]


def banner(msg):
    print(f"\n{'='*50}")
    print(f"  {msg}")
    print('='*50)


def check_pandoc():
    if shutil.which("pandoc"):
        print("  [OK] pandoc found:", shutil.which("pandoc"))
        return True
    print("  [MISSING] pandoc not found")
    print("  Required for: md-to-html conversion")
    print("  Install options:")
    print("    Windows : winget install JohnMacFarlane.Pandoc")
    print("    Choco   : choco install pandoc")
    print("    Manual  : https://pandoc.org/installing.html")
    return False


def install_python_deps():
    banner("Installing Python dependencies")
    cmd = [sys.executable, "-m", "pip", "install"] + PYTHON_DEPS
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print("\n[ERROR] pip install failed — check the error above")
        sys.exit(1)
    print("\n  [OK] All Python packages installed")


def clone_tools():
    banner("Downloading huashu-md-html scripts")
    if TOOLS_DIR.exists() and (TOOLS_DIR / "scripts").exists():
        print(f"  [OK] tools/ already present at {TOOLS_DIR}")
        print("  To update: delete tools/ and re-run this script")
        return
    if TOOLS_DIR.exists():
        shutil.rmtree(TOOLS_DIR)
    print(f"  Cloning {REPO_URL}")
    result = subprocess.run(
        ["git", "clone", "--depth=1", REPO_URL, str(TOOLS_DIR)]
    )
    if result.returncode != 0:
        print("\n[ERROR] git clone failed — check network or git installation")
        sys.exit(1)
    print(f"  [OK] Cloned to {TOOLS_DIR}")


def verify_scripts():
    banner("Verifying scripts")
    expected = ["any_to_md.py", "md_to_html.py", "html_to_md.py", "md_to_docx.py"]
    scripts_dir = TOOLS_DIR / "scripts"
    all_ok = True
    for s in expected:
        path = scripts_dir / s
        if path.exists():
            print(f"  [OK] {s}")
        else:
            print(f"  [MISSING] {s}")
            all_ok = False
    return all_ok


def main():
    banner("markdown-converter setup")
    print(f"  Skill dir : {SKILL_DIR}")
    print(f"  Tools dir : {TOOLS_DIR}")

    install_python_deps()
    clone_tools()
    scripts_ok = verify_scripts()

    banner("System dependencies")
    pandoc_ok = check_pandoc()

    banner("Setup summary")
    print(f"  Python deps : OK")
    print(f"  Scripts     : {'OK' if scripts_ok else 'FAILED'}")
    print(f"  Pandoc      : {'OK' if pandoc_ok else 'MISSING (install manually)'}")

    if not scripts_ok:
        print("\n[ERROR] Some scripts are missing — setup incomplete")
        sys.exit(1)

    print(f"""
Setup complete. Usage:
  python {SKILL_DIR}/convert.py any-to-md   <file|url> [options]
  python {SKILL_DIR}/convert.py md-to-html  <file.md>  [--theme article|report|reading|interactive]
  python {SKILL_DIR}/convert.py html-to-md  <file|url> [options]
  python {SKILL_DIR}/convert.py md-to-docx  <file.md>  [--book --title "Title"]
""")


if __name__ == "__main__":
    main()
