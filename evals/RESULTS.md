# Benchmark results

Does write-good-docs improve the docs an AI agent writes? This page records
the measured answer for each model tested. It's a snapshot: re-run the
benchmark whenever `SKILL.md` changes and add a new dated results folder.

## How this was measured

| | |
|---|---|
| Date | 2026-10-15 |
| Skill version | commit [`9d7245d`](https://github.com/ScriptAutomate/write-good-docs/tree/9d7245d), The Good Docs Project templates v1.6.0 |
| Tasks | The four tasks in [`evals.json`](evals.json): write a README, write a how-to, write release notes from a git log, and review a weak README. All are about the test project in [`files/tidyfeed/`](files/tidyfeed/). |
| Runs | Each task 3 times with the skill and 3 times without it, per model (24 runs per model) |
| Grading | Blind: outputs were shuffled and anonymised, then graded by Claude Opus 5.5 against the checks in `evals.json`. Checks marked `[script]` were run by [`check_outputs.py`](check_outputs.py). |
| Tooling | Anthropic's [skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator), in Claude Code |

Raw per-run scores, token counts and analyst notes are in
[`results/2026-10-15/`](results/2026-10-15/).

## Summary

| Writer model | With skill | Without skill | Gain | Extra tokens |
|---|---|---|---|---|
| Claude Opus 5.5 (`claude-opus-5-5`) | 99% | 83% | **+15 points** | +32% |
| Claude Sonnet 5 (`claude-sonnet-5`) | 99% | 88% | **+11 points** | +35% |
| Claude Haiku 4.5 (`claude-haiku-4-5-20251001`) | 91% | 82% | **+9 points** | +28% |

The skill improved the docs for every model tested. Haiku with the skill
(91%) scored higher than Opus and Sonnet without it (83% and 88%), and used
fewer tokens than either.

## Per task

| Task | Opus: with / without | Sonnet: with / without | Haiku: with / without |
|---|---|---|---|
| README | 100% / 89% | 100% / 85% | 96% / 82% |
| How-to | 100% / 89% | 96% / 93% | 82% / 82% |
| Release notes | 100% / 83% | 100% / 92% | 88% / 88% |
| README review | 94% / 72% | 100% / 83% | 100% / 78% |

## What the skill changes

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

## Where the skill falls short

On Haiku, the gains came from the README (+14 points) and the review (+22),
with no gain on the how-to or release notes. Even with the skill, 2 of 3
Haiku runs:

- invented documentation URLs in the how-to
- listed internal refactor and CI changes as release-note items
- presented alternatives as "Option A/B" rather than conditional steps

## Caveats

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
