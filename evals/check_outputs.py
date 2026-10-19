#!/usr/bin/env python3
"""Grade the [script] expectations in evals.json for one run's outputs.

Usage: evals/check_outputs.py <eval-name> <outputs-dir>

Reads every .md, .yml and .yaml file under <outputs-dir> and prints a JSON list of
{"text", "passed", "evidence"} objects, one per [script] expectation of
that eval, in the shape skill-creator's grading.json uses. The grader
merges these with its own judgements for the remaining expectations.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

EVALS_DIR = Path(__file__).resolve().parent
SKILL_ROOT = EVALS_DIR.parent
FIXTURE = EVALS_DIR / "files" / "tidyfeed"
TEMPLATES = SKILL_ROOT / "references"

# Template each eval's output should be checked against for leftovers.
TEMPLATE_FOR = {
    "readme-from-project": "readme/template_readme.md",
    "howto-rotate-token": "how-to/template_how-to.md",
    "release-notes-from-log": "release-notes/template_release-notes.md",
    "tutorial-first-reading-list": "tutorial/template_tutorial.md",
}
# Lines running other tools, whose flags aren't tidyfeed's.
OTHER_TOOL = re.compile(r"^\s*(?:\$\s*)?(?:pip|pipx|python3?|git|cp|cd|mkdir|export|curl)\b")
# A URL naming tidyfeed (its repo, package page, docs or API host) is a project
# fact that must come from the fixture. Links to dependencies' docs are fine.
FACT_URL = re.compile(r"tidyfeed", re.I)
# A placeholder repo URL (github.com/<org>/..., OWNER/...) is unfinished unless marked TODO.
PLACEHOLDER_URL = re.compile(r"<[^>]*>|\bOWNER\b|your[-_]?(?:org|user|name)", re.I)
# Phrases that only appear if an internal-only commit was copied through.
INTERNAL_PHRASES = ["cache pip", "pip download", "Client.__init__",
                    "session setup", "--since parsing", "chore(release)",
                    "test coverage", "test matrix", "test-matrix", "internal refactor"]
# --config belongs to the top-level parser; after a subcommand argparse rejects it.
SUBCOMMAND_THEN_CONFIG = re.compile(r"\btidyfeed[ \t]+(?:fetch|export|check-token)\b[^\n`]*?[ \t]--config\b")


def fixture_text():
    return "\n".join(p.read_text() for p in FIXTURE.rglob("*")
                     if p.is_file() and "__pycache__" not in p.parts)


def code_text(doc):
    """Text inside code blocks and inline code spans.

    Fences close only on the same character with at least the opening length
    (CommonMark), so a ````markdown block can hold ```sh blocks. A markdown or
    md block is an embedded document, such as a draft quoted in a response, so
    only the code inside it counts, not its prose.
    """
    blocks, lines, i = [], doc.splitlines(), 0
    while i < len(lines):
        m = re.match(r"^\s*(`{3,}|~{3,})\s*(\S*)", lines[i])
        if not m:
            i += 1
            continue
        fence, lang = m.group(1), m.group(2).lower()
        close = re.compile(rf"^\s*{re.escape(fence[0])}{{{len(fence)},}}\s*$")
        body, i = [], i + 1
        while i < len(lines) and not close.match(lines[i]):
            body.append(lines[i])
            i += 1
        i += 1
        inner = "\n".join(body)
        blocks.append(code_text(inner) if lang in ("markdown", "md") else inner)
    inline = re.findall(r"`([^`\n]+)`", doc)
    return "\n".join(blocks + inline)


def check_leftovers(doc_path, template):
    r = subprocess.run([str(SKILL_ROOT / "scripts" / "check-leftovers.sh"),
                        str(TEMPLATES / template), str(doc_path)],
                       capture_output=True, text=True)
    return r.returncode == 0, r.stdout.strip() or r.stderr.strip()


def check_cli(doc):
    cli = (FIXTURE / "tidyfeed" / "cli.py").read_text()
    # Flags named in the commit log (e.g. the renamed --max-items) are facts too.
    log = (FIXTURE / "git-log-2.0.txt").read_text()
    flags = (set(re.findall(r'"(--[a-z][a-z-]*)"', cli)) | {"--help", "-o", "-h"}
             | set(re.findall(r"--[a-z][a-z-]*", log)))
    commands = set(re.findall(r'add_parser\("([a-z-]+)"', cli))
    lines = [l for l in doc.splitlines() if not OTHER_TOOL.match(l)]
    bad_flags = sorted({f for l in lines for f in re.findall(r"(?<![\w-])--[a-z][a-z-]*", l)} - flags)
    # A subcommand is the word after `tidyfeed` at the start of a code line or span.
    code_lines = code_text(doc).splitlines()
    used_cmds = {m.group(1) for l in code_lines
                 if (m := re.match(r"\s*(?:\$\s*)?tidyfeed[ \t]+([a-z][a-z-]*)", l))}
    bad_cmds = sorted(used_cmds - commands)
    misplaced = sorted({m.group(0).strip() for m in SUBCOMMAND_THEN_CONFIG.finditer(code_text(doc))})
    ok = not bad_flags and not bad_cmds and not misplaced
    if ok:
        evidence = "all flags and subcommands exist in cli.py"
    else:
        evidence = f"not in cli.py: flags {bad_flags}, subcommands {bad_cmds}"
        if misplaced:
            evidence += f"; --config after a subcommand fails (top-level option): {misplaced}"
    return ok, evidence


def check_urls(doc):
    known = fixture_text()
    bad = []
    lines = doc.splitlines()
    for i, line in enumerate(lines):
        # A TODO on this line or just above it marks the URL as a known gap.
        marked = "TODO" in "\n".join(lines[max(0, i - 2):i + 1]).upper()
        for url in re.findall(r"https?://[^\s)\]`'\"]+", line):
            url = url.rstrip(".,;:>")
            if url in known or marked:
                continue
            if FACT_URL.search(url) or PLACEHOLDER_URL.search(url):
                bad.append(url)
    return not bad, "no invented project URLs" if not bad else f"not in project files: {sorted(set(bad))}"


def check_env(doc):
    bad = sorted(set(re.findall(r"\bTIDYFEED_[A-Z_]+\b", doc)) - {"TIDYFEED_TOKEN"})
    return not bad, "only TIDYFEED_TOKEN used" if not bad else f"invented: {bad}"


def check_hashes(doc):
    hashes = re.findall(r"^([0-9a-f]{7}) ", (FIXTURE / "git-log-2.0.txt").read_text(), re.M)
    found = [h for h in hashes if h in doc]
    return not found, "no commit hashes" if not found else f"hashes present: {found}"


def check_internal(doc):
    found = [p for p in INTERNAL_PHRASES if p.lower() in doc.lower()]
    return not found, "no internal-only commits" if not found else f"internal changes listed: {found}"


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    name, outputs = sys.argv[1], Path(sys.argv[2])
    spec = next((e for e in json.loads((EVALS_DIR / "evals.json").read_text())["evals"]
                 if e["name"] == name), None)
    if spec is None:
        sys.exit(f"unknown eval: {name}")
    docs = sorted(p for p in outputs.rglob("*") if p.suffix in (".md", ".yml", ".yaml"))
    # Judge what a reader sees: HTML comments (notes to maintainers) don't render,
    # but a TODO inside one still marks the nearby text as a known gap.
    doc = re.sub(r"<!--.*?-->", lambda m: "TODO" if "TODO" in m.group(0).upper() else "",
                 "\n".join(p.read_text() for p in docs), flags=re.S)

    results = []
    for text in (t for t in spec["expectations"] if t.startswith("[script]")):
        if not docs:
            ok, ev = False, f"no .md or .yml output in {outputs}"
        elif "placeholders" in text:
            outcomes = [check_leftovers(p, TEMPLATE_FOR[name]) for p in docs]
            ok = all(o for o, _ in outcomes)
            ev = "; ".join(e for _, e in outcomes)
        elif "subcommand and flag" in text:
            ok, ev = check_cli(doc)
        elif "URLs" in text:
            ok, ev = check_urls(doc)
        elif "environment variables" in text:
            ok, ev = check_env(doc)
        elif "commit hashes" in text:
            ok, ev = check_hashes(doc)
        elif "internal-only" in text:
            ok, ev = check_internal(doc)
        else:
            sys.exit(f"no check implements: {text}")
        results.append({"text": text, "passed": ok, "evidence": ev})
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
