# Benchmark results

Does write-good-docs improve the docs an AI agent writes? This page records
the measured answer for each model tested. Each section is a dated
snapshot, newest first: re-run the benchmark whenever `SKILL.md` changes
and add a new dated results folder.

## 2026-10-21: when the skill triggers

The earlier sections measure the docs an agent writes once it uses the
skill. This one measures whether the agent uses the skill at all. Claude
decides that from the skill's `description` alone.

[`trigger-evals.json`](trigger-evals.json) holds 20 requests. 10 should
use the skill: release notes, a how-to, contributor files, a README
review, a tutorial, a config reference, "which doc should I write?",
a troubleshooting page, a concept explainer and a code of conduct. 10
are near-misses that shouldn't: docstrings, a commit message, README badge
fixes, docs-site setup, a blog post, a PR description, a Word document, a
translation, an OpenAPI fix and a summary. Each request ran 3 times per
model in headless Claude Code (`claude -p`). A request passes when it
triggers in at least 2 of 3 runs, or, for a near-miss, in at most 1.

| Model | Should use the skill | Near-misses left alone | Pass |
|---|---|---|---|
| Opus 5.5 | 10 of 10 | 10 of 10 | 20/20 |
| Sonnet 5 | 10 of 10 | 10 of 10 | 20/20 |
| Haiku 4.5 | 5 of 10 | 10 of 10 | 15/20 |

No model used the skill for a near-miss in any run. Haiku skipped it for
release notes and the README review in all 3 runs, and used it in only 1
of 3 runs for contributor files, the concept explainer and the code of
conduct. The description names release notes, README reviews and codes
of conduct explicitly, so Haiku seems to decide it can write these
without help rather than fail to match them. The description wasn't
changed: it already works for Opus and Sonnet.

These runs used skill-creator's `run_eval.py` with three fixes. Without
them, the results would be wrong:

- **Parallel runs:** every run wrote its copy of the skill into one
  shared `.claude/commands/` folder, so a run could use another run's
  copy and be scored as not triggering. Each run now gets its own folder.
- **First tool only:** a run was scored as not triggering if its first
  tool call wasn't the skill, even if it used the skill next. The whole
  run is now checked.
- **Failed runs:** a run that failed, for example on a usage limit, was
  scored as not triggering. It's now reported as a failure. One Opus pass
  hit a usage limit and was re-run in full.

Raw results are in [`results/2026-10-21/`](results/2026-10-21/).

## 2026-10-19: tutorial and doc-type tasks, and the split rule

This round added two tasks to [`evals.json`](evals.json): task 5 writes a
tutorial for first-time users, and task 6 asks for one doc that serves
two reader goals. A third candidate, a GitHub bug report form, showed
little difference with the skill and was dropped. Grading was blind, by
Opus 5.5, as before.

**Tutorial (task 5): the skill helps both models**

| Model | With skill | Without skill | Gain |
|---|---|---|---|
| Haiku 4.5 | 100% | 80% | +20 points |
| Sonnet 5 | 100% | 87% | +13 points |

Without the skill, tutorials often failed to say up front who they're
for and what the reader will learn (all 3 Haiku runs, 2 of 3 Sonnet
runs). Some also didn't end with a summary.

**Choosing a doc type (task 6): the skill needed a clearer rule**

With the skill at commit
[`ef4096b`](https://github.com/ScriptAutomate/write-good-docs/commit/ef4096b),
Haiku scored no better than without it (50% against 61%). It usually
recommended one combined doc with a section for each goal. Commit
[`87a01f6`](https://github.com/ScriptAutomate/write-good-docs/commit/87a01f6)
made the rule explicit: recommend separate docs, even when the user asked
for one.

| Model | Before the rule | With the rule |
|---|---|---|
| Haiku 4.5 | 61% (1 of 3 runs recommended two docs) | 100% (3 of 3) |
| Sonnet 5 | not run | 100% (3 of 3) |

**Regression check for the split rule (Haiku 4.5)**

| Task | Before (2026-10-18) | With the rule |
|---|---|---|
| README | 93% | 93% |
| README review | 100% | 94% |

The review dip is one failed check out of 18: one run didn't note that
the draft leads with its tech stack. No run proposed splitting the
README, so the rule doesn't seem to be the cause. Both README failures
are invented URLs, as on 2026-10-18.

Graders also noted problems that no check covers yet: `--config` documented
as a subcommand option (it must come before the subcommand), invented
claims about the web app, and `pip install tidyfeed` for a package that
isn't published.

Raw results are in [`results/2026-10-19/`](results/2026-10-19/).

## 2026-10-18: explicit rules for procedures, URLs and release notes

The 2026-10-15 benchmark (below) showed no gain for Haiku on how-tos or
release notes. Commit
[`ef4096b`](https://github.com/ScriptAutomate/write-good-docs/commit/ef4096b)
added a "Check before you deliver" step and type-specific rules to
`SKILL.md`. These runs measured that change. They use the same tasks, test
project and blind Opus 5.5 grading as before, with the stricter checks
from commit
[`b8e308c`](https://github.com/ScriptAutomate/write-good-docs/commit/b8e308c).
Those checks don't change any earlier with-skill score.

**Haiku 4.5, old skill against new skill, in the same round (3 runs each):**

| Task | Old skill | New skill | Change |
|---|---|---|---|
| How-to | 74% | 85% | +11 points |
| Release notes | 92% | 100% | +8 points |

- **Release notes:** internal CI, test and refactor changes were listed in 2
  of 3 old-skill runs and in none with the new skill.
- **How-to:** 2 of 3 runs now say which token setting wins (0 of 3 before).
  Condition-first steps improved only from 0 of 3 to 1 of 3; Haiku still
  often writes "Option A/B".

**Regression check: the new skill against the 2026-10-15 with-skill scores**

| Model | README | How-to | Release notes | Review |
|---|---|---|---|---|
| Opus 5.5 | not re-run | 100% (was 100%) | 100% (was 100%) | not re-run |
| Sonnet 5 | 100% (was 100%) | 100% (was 96%) | 100% (was 100%) | 100% (was 100%) |
| Haiku 4.5 | 93% (was 96%) | 85% (was 82%) | 100% (was 88%) | 100% (was 100%) |

The only dip is Haiku's README: one more failed check out of 27, within
the noise of 3 runs. One of those READMEs invented an API docs URL, which
the new rule is meant to prevent. For Haiku, the rule reduces invented URLs
but doesn't eliminate them.

Raw results are in [`results/2026-10-18/`](results/2026-10-18/).

## 2026-10-15: with and without the skill

### How this was measured

| | |
|---|---|
| Date | 2026-10-15 |
| Skill version | commit [`9d7245d`](https://github.com/ScriptAutomate/write-good-docs/tree/9d7245d), The Good Docs Project templates v1.6.0 |
| Tasks | Tasks 1 to 4 in [`evals.json`](evals.json): write a README, write a how-to, write release notes from a git log, and review a weak README. All are about the test project in [`files/tidyfeed/`](files/tidyfeed/). |
| Runs | Each task 3 times with the skill and 3 times without it, per model (24 runs per model) |
| Grading | Blind: outputs were shuffled and anonymised, then graded by Claude Opus 5.5 against the checks in `evals.json`. Checks marked `[script]` were run by [`check_outputs.py`](check_outputs.py). |
| Tooling | Anthropic's [skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator), in Claude Code |

Raw per-run scores, token counts and analyst notes are in
[`results/2026-10-15/`](results/2026-10-15/).

### Summary

| Writer model | With skill | Without skill | Gain | Extra tokens |
|---|---|---|---|---|
| Claude Opus 5.5 (`claude-opus-5-5`) | 99% | 83% | **+15 points** | +32% |
| Claude Sonnet 5 (`claude-sonnet-5`) | 99% | 88% | **+11 points** | +35% |
| Claude Haiku 4.5 (`claude-haiku-4-5-20251001`) | 91% | 82% | **+9 points** | +28% |

The skill improved the docs for every model tested. Haiku with the skill
(91%) scored higher than Opus and Sonnet without it (83% and 88%), and used
fewer tokens than either.

### Per task

| Task | Opus: with / without | Sonnet: with / without | Haiku: with / without |
|---|---|---|---|
| README | 100% / 89% | 100% / 85% | 96% / 82% |
| How-to | 100% / 89% | 96% / 93% | 82% / 82% |
| Release notes | 100% / 83% | 100% / 92% | 88% / 88% |
| README review | 94% / 72% | 100% / 83% | 100% / 78% |

### What the skill changes

Without the skill, every model left the same gaps. With it, most of them
closed:

- **Saying who a README is for:** 0 of 9 runs did this without the skill,
  and 9 of 9 with it.
- **Reviewing a README:** without the skill, no review noticed that the draft
  never says who the project is for (0 of 9). With the skill, 8 of 9 did.
- **How-to procedures:** without the skill, models often used "Step N"
  headings or "Option A/B" instead of a numbered list with "If …, then …"
  steps. The skill fixed this for Opus and Sonnet, but only partly for Haiku.
- **Release notes:** without the skill, Opus and Sonnet sometimes listed every
  commit hash and internal change. With the skill they didn't.

### Where the skill falls short

On Haiku, the gains came from the README (+14 points) and the review (+22),
with no gain on the how-to or release notes. Even with the skill, 2 of 3
Haiku runs:

- invented documentation URLs in the how-to
- listed internal refactor and CI changes as release-note items
- presented alternatives as "Option A/B" rather than conditional steps

### Caveats

- **Small sample:** 3 runs per task and setup. The overall gains are
  consistent across models, but per-task numbers can shift by one run.
- **Timing isn't comparable across models:** a usage-limit interruption meant
  some runs were re-done later under different load. Compare token counts,
  not seconds.
- **Not yet checked:** graders also flagged problems that no check covers,
  including invented UI labels and error messages, `--config` placed after a
  subcommand (where it fails), `pip install` for an unpublished package, and
  printing the API token with `echo`. Checks for these would make the
  benchmark stricter.

To run the benchmark yourself, see "Measure the skill" in
[`CONTRIBUTING.md`](../CONTRIBUTING.md#measure-the-skill).
