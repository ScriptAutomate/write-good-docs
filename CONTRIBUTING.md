# write-good-docs contributing guide

Thank you for helping improve write-good-docs. This guide is for
maintainers and contributors. If you only want to use the skill, the
[README](README.md) has everything you need.

We accept these contributions:

- Changes to how the skill works: see [Change the skill](#change-the-skill).
- Updates to a newer release of The Good Docs Project templates: see
  [Refresh the templates](#refresh-the-templates).
- Bug reports for the skill or its scripts: see
  [Report issues](#report-issues).

We don't accept hand edits to the files under `references/`, or to the
generated content-type tables in `SKILL.md`. Both come from an upstream
release, and the next refresh overwrites hand edits. To change a
template or guide, contribute it to
[The Good Docs Project](https://gitlab.com/tgdp/templates) instead.

## Project overview

write-good-docs is an Agent Skill. It gives an AI agent The Good Docs
Project (TGDP) templates and guides, plus a workflow for writing and
reviewing docs with them. See the [README](README.md) for the full
description.

## What lives where

| Path | Owner | Edit it by |
|---|---|---|
| `SKILL.md` (outside the generated block) | This project | Hand |
| `SKILL.md` between the `BEGIN generated` / `END generated` markers | TGDP's `index.json` | `maintainer/sync-references.py` |
| `references/` | TGDP | `maintainer/sync-references.py` |
| `scripts/` | This project. These scripts are for skill users. | Hand |
| `maintainer/` | This project. These scripts are for maintainers only. | Hand |
| `evals/` | This project. A benchmark for maintainers; the skill never loads it. | Hand |
| `README.md`, `CONTRIBUTING.md` | This project | Hand |

Everything in `SKILL.md` is loaded into the agent's context each time the
skill runs. Keep maintainer-only material out of it and put it here
instead.

## Before you start

Make sure you have:

- Python 3. The sync script uses only the standard library.
- `bash`, `awk` and `grep` for `scripts/check-leftovers.sh`.
- Network access to `gitlab.com` to refresh the templates.

You don't need git or a clone of the TGDP repository to refresh the
templates.

## Change the skill

1. Edit `SKILL.md` or the files in `scripts/`.
2. If you changed a doc in this repo, check it with the skill's own
   leftovers check, for example:

   ```bash
   scripts/check-leftovers.sh references/readme/template_readme.md README.md
   ```

3. Start a new agent session and try the skill on a real request, such
   as `/write-good-docs how-to <task>` in Claude Code.
4. If you changed `SKILL.md`, re-run the benchmark. See
   [Measure the skill](#measure-the-skill).

## Measure the skill

The `evals/` folder holds a benchmark. It checks whether the skill makes
an agent write better docs than the same agent without the skill. It
contains:

- `evals/evals.json`: four realistic requests, each with the checks a
  good answer must pass. Each one tests something the skill measurably
  improves: build a README from project facts, write a how-to as a real
  numbered procedure, curate release notes from a commit log, and review
  a weak README by ranking its gaps.
- `evals/files/tidyfeed/`: a small, made-up command-line tool. The
  requests are about this tool, so a doc that invents a flag, an
  environment variable or a URL can be caught.
- `evals/check_outputs.py`: runs the checks marked `[script]` in
  `evals.json` against one run's output. A grader agent judges the
  rest.

To run the benchmark, use Anthropic's
[skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator)
in Claude Code:

1. Install skill-creator, as described in
   [Run evals with skill-creator](https://code.claude.com/docs/en/skills#run-evals-with-skill-creator).
2. Ask Claude to use skill-creator to evaluate this skill with the evals
   in `evals/evals.json`. It runs each request with and without the
   skill, grades the results and produces a report with pass rates,
   time and tokens for each.
3. Keep the results outside this repository. skill-creator's
   `<skill-name>-workspace/` folder is for local use only.

A change to `SKILL.md` shouldn't lower the with-skill pass rate. Mention
the before and after pass rates in your pull request.

## Refresh the templates

When TGDP publishes a new release tag:

1. Run the sync script with the tag:

   ```bash
   maintainer/sync-references.py <tag>
   ```

   For example, `maintainer/sync-references.py v1.6.0`. The script:

   - downloads the tag's release archive from GitLab
   - replaces every content-type directory under `references/`, and
     `references/writing-tips.md`
   - rewrites `references/UPSTREAM.md` with the tag, commit and commit
     date
   - regenerates the content-type tables in `SKILL.md` from upstream's
     `index.json`

2. Review the changes:

   ```bash
   git diff --stat
   git diff SKILL.md references/UPSTREAM.md
   ```

3. If the script printed `added types:` or `removed types:`, review the
   "Commonly confused pairs" list in `SKILL.md` by hand. If upstream
   introduced a new pack, the script stops with `unknown pack`. In that
   case, add the pack to `PACKS` in `maintainer/sync-references.py` and
   run the script again.

Running the script twice with the same tag produces no changes.

### Sync options

| Option | Use it to |
|---|---|
| `--zip <file>` | Use a release archive you already downloaded instead of downloading it again. |
| `--commit-date YYYY-MM-DD` | Skip the GitLab API call that looks up the commit date. Combine this with `--zip` to run offline. |

### Troubleshoot the sync

| Error | Cause and fix |
|---|---|
| `SKILL.md lacks the ... markers` | The `BEGIN generated` or `END generated` comment in `SKILL.md` was removed. Restore both, then run the script again. |
| `index.json lists '<type>' but the archive has no such dir`, or `dirs missing from index.json` | Upstream's index and folders disagree. The script stops before changing any files. Report the problem to TGDP. |
| `archive comment is not a commit SHA` | The file isn't a GitLab release archive. Use the archive URL for the tag, or remove `--zip`. |

## Report issues

[Open an issue](https://github.com/ScriptAutomate/write-good-docs/issues/new/choose)
and choose the **Bug report** form. It
asks for the request you gave the agent, what it produced, and what you
expected. The form is defined in `.github/ISSUE_TEMPLATE/bug_report.yml`.

## Commit messages

Use [Conventional Commits](https://www.conventionalcommits.org/), as the
existing history does. For example: `feat(sync): read SHA from archive`.
