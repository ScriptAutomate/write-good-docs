#!/usr/bin/env python3
"""Re-vendor The Good Docs Project templates into references/.

Usage: maintainer/sync-references.py <tag> [--zip FILE] [--commit-date YYYY-MM-DD]

Downloads the tag's release archive from GitLab (no git needed), copies
every content-type dir (any top-level dir holding a guide_*.md) verbatim
plus writing-tips.md, regenerates references/UPSTREAM.md, and rewrites
the content-type tables in SKILL.md from upstream's index.json.
Deterministic: re-running against the same tag leaves no diff.

--zip uses a local archive instead of downloading it. The commit date
still comes from the GitLab tags API unless --commit-date is given.
"""
import argparse
import json
import re
import shutil
import sys
import tempfile
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path

PROJECT = "tgdp/templates"
ARCHIVE_URL = "https://gitlab.com/{p}/-/archive/{t}/templates-{t}.zip"
TAG_API = "https://gitlab.com/api/v4/projects/{p}/repository/tags/{t}"

# index.json pack key -> heading in SKILL.md, in display order.
PACKS = {
    "core": "Core documentation pack",
    "community": "Open source community pack",
    "misc": "Miscellaneous pack (for maturing doc sets)",
}
ROLES = [("template", "T"), ("guide", "G"), ("process", "P"),
         ("resources", "R"), ("example", "E")]
BEGIN = "<!-- BEGIN generated: content types (maintainer/sync-references.py) -->"
END = "<!-- END generated: content types -->"

SKILL_ROOT = Path(__file__).resolve().parent.parent
REFS = SKILL_ROOT / "references"
SKILL_MD = SKILL_ROOT / "SKILL.md"


def die(msg):
    sys.exit(f"error: {msg}")


def fetch(url, dest=None):
    req = urllib.request.Request(url, headers={"User-Agent": "write-good-docs-sync"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        if dest is None:
            return resp.read()
        with open(dest, "wb") as f:
            shutil.copyfileobj(resp, f)


def commit_date(tag):
    url = TAG_API.format(p=urllib.parse.quote(PROJECT, safe=""), t=tag)
    data = json.loads(fetch(url))
    return data["commit"]["committed_date"][:10]


def type_dirs(root):
    return sorted(d.name for d in root.iterdir()
                  if d.is_dir() and any(d.glob("guide_*.md")))


def files_column(type_dir):
    return " ".join(letter for role, letter in ROLES
                    if any(type_dir.glob(f"{role}_*")))


def type_row(slug, summary):
    summary = " ".join(summary.split()).replace("|", "\\|")
    exts = sorted({p.suffix for p in (REFS / slug).glob("template_*")} - {".md"})
    if exts:
        summary += " (" + "/".join(f"`{e}`" for e in exts) + " templates)"
    return f"| [{slug}](references/{slug}/) | {summary} | {files_column(REFS / slug)} |"


def group_by_pack(index, slugs):
    """Validate index.json against the archive's dirs; return pack -> rows."""
    by_pack = {k: [] for k in PACKS}
    for entry in index:
        template = entry["files"].get("template", "")
        m = re.match(r"template_(.+)\.[^.]+$", template)
        if not m:
            die(f"index.json entry {entry['name']!r} has no template file")
        slug = m.group(1)
        if slug not in slugs:
            die(f"index.json lists {slug!r} but the archive has no such dir")
        for pack in entry["packs"]:
            if pack not in PACKS:
                die(f"unknown pack {pack!r} for {slug!r}: add it to PACKS")
            by_pack[pack].append((slug, entry["summary"]))
    indexed = {s for rows in by_pack.values() for s, _ in rows}
    if indexed != set(slugs):
        die(f"dirs missing from index.json: {sorted(set(slugs) - indexed)}")
    return by_pack


def render_tables(by_pack):
    first_pack = {}
    out = []
    for pack, heading in PACKS.items():
        out += [f"### {heading}", "", "| Type | Use it for | Files |", "|---|---|---|"]
        for slug, summary in sorted(by_pack[pack]):
            if slug in first_pack:
                out.append(f"| {slug} | Also part of this pack — see "
                           f"{PACKS[first_pack[slug]]} above | |")
            else:
                first_pack[slug] = pack
                out.append(type_row(slug, summary))
        out.append("")
    return "\n".join(out).rstrip("\n")


def write_upstream(tag, commit, date, slugs):
    lines = [
        "# Upstream source",
        "",
        "Vendored verbatim from [The Good Docs Project templates](https://gitlab.com/tgdp/templates)",
        "(MIT-0, see `../LICENSE`) by `maintainer/sync-references.py` from the tag's",
        "release archive. Do not edit these files by hand: re-run the script against",
        "a newer tag instead.",
        "",
        f"- Tag: `{tag}`",
        f"- Commit: `{commit}`",
        f"- Commit date: {date}",
        "",
        "Included: every content-type directory (`template_`, `guide_`, `process_`,",
        "`resources_`, `example_` files and their assets) and `writing-tips.md`.",
        "",
        "Excluded: `STYLE-GUIDE.md` and `images/` (the TGDP project's own style guide),",
        "`template_deliverables.md`, `index.json`, `README.md`, governance files",
        "(CONTRIBUTING, GOVERNANCE, ADOPTERS, ...) and `.gitlab/`.",
        "",
        f"Content types ({len(slugs)}):",
        "",
        *[f"- `{s}/`" for s in slugs],
    ]
    (REFS / "UPSTREAM.md").write_text("\n".join(lines) + "\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("tag", help="TGDP release tag, e.g. v1.6.0")
    ap.add_argument("--zip", type=Path, help="use this local archive instead of downloading")
    ap.add_argument("--commit-date", help="skip the GitLab API lookup (YYYY-MM-DD)")
    args = ap.parse_args()

    skill = SKILL_MD.read_text()
    pattern = re.compile(re.escape(BEGIN) + r".*?" + re.escape(END), re.S)
    if not pattern.search(skill):
        die(f"SKILL.md lacks the {BEGIN!r} ... {END!r} markers")

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        archive = args.zip
        if archive is None:
            archive = tmp / "templates.zip"
            fetch(ARCHIVE_URL.format(p=PROJECT, t=args.tag), archive)
        with zipfile.ZipFile(archive) as zf:
            commit = zf.comment.decode().strip()
            if not re.fullmatch(r"[0-9a-f]{40}", commit):
                die(f"archive comment is not a commit SHA: {commit!r}")
            zf.extractall(tmp / "x")
        tops = [d for d in (tmp / "x").iterdir() if d.is_dir()]
        if len(tops) != 1:
            die("expected one top-level dir in the archive")
        src = tops[0]
        date = args.commit_date or commit_date(args.tag)

        new_types = type_dirs(src)
        if not new_types:
            die("no content-type dirs found in the archive")
        by_pack = group_by_pack(json.loads((src / "index.json").read_text()), new_types)

        REFS.mkdir(exist_ok=True)
        old_types = type_dirs(REFS)
        for d in REFS.iterdir():
            if d.is_dir():
                shutil.rmtree(d)
        for t in new_types:
            shutil.copytree(src / t, REFS / t)
        shutil.copy(src / "writing-tips.md", REFS / "writing-tips.md")

    write_upstream(args.tag, commit, date, new_types)

    tables = render_tables(by_pack)
    SKILL_MD.write_text(pattern.sub(lambda _: f"{BEGIN}\n{tables}\n{END}", skill))

    print(f"synced {args.tag} ({commit}) into {REFS}")
    added = sorted(set(new_types) - set(old_types))
    removed = sorted(set(old_types) - set(new_types))
    if added:
        print("added types: " + " ".join(added))
    if removed:
        print("removed types: " + " ".join(removed))
    if added or removed:
        print("SKILL.md tables are regenerated; review the 'Commonly confused pairs' list by hand")


if __name__ == "__main__":
    main()
