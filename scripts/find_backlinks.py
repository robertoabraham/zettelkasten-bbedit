#!/usr/bin/env python3
"""
find_backlinks.py
Finds all notes in ~/Zettelkasten that reference the given note.
Results open as an HTML page in your browser; clicking a filename opens it in BBEdit.
Usage: python3 find_backlinks.py /path/to/note.txt
"""

import os
import re
import sys
import subprocess
import tempfile

# ── Configuration ──────────────────────────────────────────────────────────────

NOTES_DIR = os.path.expanduser("~/Zettelkasten")

# ── Helpers ────────────────────────────────────────────────────────────────────

def find_note_files(root: str) -> list[str]:
    """Recursively find all .txt and .md files under root."""
    result = subprocess.run(
        ["find", root, "-type", "f", "(", "-name", "*.txt", "-o", "-name", "*.md", ")"],
        capture_output=True, text=True
    )
    return [f for f in result.stdout.splitlines() if f.strip()]


def build_patterns(stem: str, filename: str) -> list[re.Pattern]:
    """
    Match common ways a note can be referenced:
      [[note-name]]  [[note-name.txt]]  [[note-name.md]]
      [text](note-name.txt)  [text](note-name.md)  [text](note-name)
    """
    escaped_stem = re.escape(stem)
    escaped_filename = re.escape(filename)
    return [
        re.compile(rf'\[\[{escaped_stem}(?:\.txt|\.md)?\]\]', re.IGNORECASE),
        re.compile(rf'\]\({escaped_filename}\)', re.IGNORECASE),
        re.compile(rf'\]\({escaped_stem}\)', re.IGNORECASE),
    ]


def find_backlinks(target_path: str, search_dir: str) -> list[dict]:
    """
    Search all note files in search_dir for references to target_path.
    Returns a list of dicts with 'path' and 'lines' (matching line number + text).
    """
    target_filename = os.path.basename(target_path)
    target_stem = os.path.splitext(target_filename)[0]
    patterns = build_patterns(target_stem, target_filename)

    results = []
    for note_path in find_note_files(search_dir):
        if os.path.realpath(note_path) == os.path.realpath(target_path):
            continue
        try:
            with open(note_path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
        except OSError:
            continue

        matching_lines = []
        for line_num, line in enumerate(lines, start=1):
            if any(p.search(line) for p in patterns):
                matching_lines.append((line_num, line.rstrip()))

        if matching_lines:
            results.append({"path": note_path, "lines": matching_lines})

    return results


def show_dialog(title: str, message: str):
    safe = message.replace('"', '\\"')
    script = f'display dialog "{safe}" with title "{title}" buttons {{"OK"}} default button "OK" with icon note'
    subprocess.run(["osascript", "-e", script], check=False)


def resolve_search_dir() -> str:
    if not os.path.isdir(NOTES_DIR):
        show_dialog(
            "Backlink Finder",
            f"Notes folder not found at:\n{NOTES_DIR}\n\n"
            "Please create it or edit the NOTES_DIR variable in find_backlinks.py."
        )
        sys.exit(1)
    return NOTES_DIR



# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("Usage: find_backlinks.py <path-to-note>")
        sys.exit(1)

    target_path = sys.argv[1]

    if not os.path.isfile(target_path):
        show_dialog("Backlink Finder", f"File not found:\n{target_path}")
        sys.exit(1)

    search_dir = resolve_search_dir()
    target_name = os.path.basename(target_path)
    target_stem = os.path.splitext(target_name)[0]

    all_notes = find_note_files(search_dir)
    results = find_backlinks(target_path, search_dir)

    if not results:
        lines = [f'No backlinks found for "{target_stem}".',
                 f'Searched {len(all_notes)} file(s) in {search_dir}']
    else:
        lines = [f'Backlinks to "{target_stem}"',
                 f'Found in {len(results)} note(s):', ""]
        for entry in sorted(results, key=lambda x: x["path"]):
            lines.append(entry["path"])
            for line_num, line_text in entry["lines"]:
                display = line_text.strip()
                if len(display) > 120:
                    display = display[:117] + "..."
                lines.append(f"  Line {line_num}: {display}")
            lines.append("")

    output = "\n".join(lines)
    tmp = tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".txt",
        prefix=f"backlinks_{target_stem}_",
        delete=False
    )
    tmp.write(output)
    tmp.close()
    subprocess.run(["open", tmp.name], check=False)


if __name__ == "__main__":
    main()
