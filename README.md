# write-good-docs

An AI agent skill that drafts and reviews software docs with
[The Good Docs Project](https://thegooddocsproject.dev/) templates.

## Project description

With write-good-docs, AI agents can pick the right kind of doc for the job,
then build it from your project's real facts. You no longer have to start
from a blank page.

Docs written from scratch tend to drift. READMEs forget to say who they're
for, how-tos turn into tutorials partway through, and release notes end up
as commit logs. The Good Docs Project (TGDP) has researched templates for more
than 20 common content types. Each template comes with a guide that explains why
every section exists. This skill gives AI agents that material and a workflow
for using it:

1. Choose one content type, such as README, how-to, tutorial, release notes
   or API reference.
2. Read the guide for that type before reading its template.
3. Fill each section with facts from your code, CLI help, config and git
   history. Unknown facts become marked TODOs, never guesses.
4. Change the structure to suit your project, then remove all template
   scaffolding.

Unlike filling in a template by hand, the skill also covers reviews. Ask
"is this README missing anything?" and an agent compares your doc against the
guide for its type. It ranks the gaps by how much they affect the reader.

This README was itself written with the skill.

## Who this project is for

This project is for developers, technical writers and maintainers who use
AI agents and want docs that follow a proven structure. Use it to:

- Write a new README, how-to, tutorial, concept or reference page.
- Add community files such as a contributing guide or code of conduct.
- Turn a release into release notes or a changelog entry.
- Review an existing doc for missing or misplaced sections.
- Decide which kind of doc you need.

## What's included

The skill follows TGDP's three template packs:

| Pack | Content types (examples) |
|---|---|
| Core documentation | concept, how-to, readme, reference, release-notes, tutorial, troubleshooting |
| Open source community | bug-report, changelog, code-of-conduct, contributing-guide, our-team |
| Miscellaneous | api-getting-started, api-reference, glossary, installation-guide, quickstart, style-guide, user-personas |

For every type and what each one is for, see the tables in
[`SKILL.md`](SKILL.md).

| Path | Contents |
|---|---|
| `SKILL.md` | The instructions AI agents follow: how to choose a content type, the file roles and the writing workflow. |
| `references/<type>/` | TGDP files for each content type. These are the `template_` outline and `guide_`, plus `process_`, `resources_` and `example_` where TGDP provides them. |
| `references/writing-tips.md` | TGDP's general writing guidelines, which apply to every type. |
| `references/UPSTREAM.md` | The TGDP release tag and commit the references come from. |
| `scripts/check-leftovers.sh` | Finds template placeholders and boilerplate left behind in a finished draft. |
| `maintainer/` | Tools for maintainers only. See [`CONTRIBUTING.md`](CONTRIBUTING.md). |

## Prerequisites

Before using write-good-docs, make sure you have:

- An AI agent that loads Agent Skills (`SKILL.md` folders).
- `git` to install the skill.
- `bash`, `awk` and `grep` for the leftovers check.

## Install write-good-docs

> This example uses Claude Code as the AI agent.

The skill's name is `write-good-docs`, so install it into a directory with
that name.

1. Choose where to install the skill.

   - For all of your projects, use `~/.claude/skills/write-good-docs`.
   - For one project only, use `.claude/skills/write-good-docs` inside that
     project.

2. Clone the repository into the directory you chose:

   ```bash
   git clone https://github.com/ScriptAutomate/write-good-docs.git ~/.claude/skills/write-good-docs
   ```

3. Start a new Claude Code session so that it discovers the skill.

## Use write-good-docs

Ask the agent for a doc in plain language. The skill activates for requests
like these:

- "Write a README for this project."
- "Draft a how-to for rotating the API keys."
- "Write release notes for v2.3."
- "Add a CONTRIBUTING guide and a code of conduct."
- "Is this README missing anything?"
- "Which kind of doc should I write for this?"

AI agents may support invoking the skill directly and naming the
content type up front:

```text
/write-good-docs how-to rotating the API keys
/write-good-docs readme
/write-good-docs
```

The first word is used as the content type when it matches one. Without
arguments, the agent asks or chooses a type from your request.

If a request covers more than one content type, AI agents propose splitting
it into separate docs. An example is a README that also tries to be a
quickstart. Each template is built around a single reader goal.

### Check a draft for template leftovers

After the scaffolding is removed, the skill runs this check. You can also
run it yourself:

```bash
scripts/check-leftovers.sh references/<type>/template_<type>.md <draft>
```

The script reports two problems: `{placeholder}` text from that template
that is still in the draft, and TGDP's "read the accompanying guide" and
"Explore other templates" notes. It skips fenced code blocks, so braces in
JSON or code samples don't count as leftovers. It exits with `0` when the
draft is clean, `1` when it finds leftovers and `2` on a usage error.

The script can't detect placeholders that span several lines in the
template, or instructions that don't use braces. Reread the draft yourself
as well.

## Troubleshoot

| Issue | Solution |
|---|---|
| `check-leftovers.sh` flags braces in a code sample | Put the sample in a fenced code block. The script ignores fenced code but not inline text. |
| AI agent doesn't use the skill | Check that `SKILL.md` is directly inside `.../skills/write-good-docs/`, then start a new session. |

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) to change the skill or to update
it to a newer TGDP release. Updating the templates is a maintainer task;
you don't need to do it to use the skill.

Report problems with the templates or guides themselves to
[The Good Docs Project](https://www.thegooddocsproject.dev/feedback).

## How to get help

- For problems with the skill or the scripts, open an issue in this
  repository.
- For questions about the templates and guides, visit
  [thegooddocsproject.dev](https://thegooddocsproject.dev/).

## Terms of use

write-good-docs is licensed under the [MIT No Attribution License](LICENSE)
(MIT-0). The templates, guides and writing tips under `references/` are the
work of [The Good Docs Project](https://thegooddocsproject.dev/) and are
used under the same license.
