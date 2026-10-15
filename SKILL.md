---
name: write-good-docs
description: Drafts and reviews software docs using The Good Docs Project templates and guides — picks the right content type (README, how-to, tutorial, concept, reference, release notes, API docs, community docs, and more), then fills it from real project facts. Use when asked to write, draft, restructure, or review a doc — e.g. "write a README for X", "draft a how-to / tutorial", "write release notes / a changelog", "add a CONTRIBUTING guide / code of conduct", "document this API", "is this README missing anything", or "which kind of doc should I write".
argument-hint: "[content-type] [what to document]"
---

# write-good-docs

Docs written from a blank page drift toward whatever the author
happened to think of: READMEs with no "who is this for", how-tos that
silently become tutorials, release notes that are just commit logs.
The Good Docs Project templates encode researched structure for the
common content types, and each one ships a guide explaining *why* every
section exists — which is what lets a draft be adapted intelligently
rather than filled in mechanically. This skill puts that material one
`Read` away and says how to use it.

Everything under `references/` is vendored verbatim from
[gitlab.com/tgdp/templates](https://gitlab.com/tgdp/templates) (MIT-0,
see `LICENSE`); `references/UPSTREAM.md` records the tag and commit.
Never hand-edit those files, or the tables below: maintainers
regenerate both from an upstream release (see `CONTRIBUTING.md`).

## Pick the content type

If unsure, start from the **core pack**: it's the fundamental set
every documentation project needs. Files column: **T**emplate,
**G**uide, **P**rocess, **R**esources, **E**xample.

<!-- BEGIN generated: content types (maintainer/sync-references.py) -->
### Core documentation pack

| Type | Use it for | Files |
|---|---|---|
| [concept](references/concept/) | An explanation of a concept, context, or background information about a product or its features. | T G P R E |
| [how-to](references/how-to/) | A how-to is a concise set of numbered steps to do one task with the product. | T G |
| [readme](references/readme/) | README files include information users need to know about your project, including how users can engage with the project and get started with the tool. | T G P R E |
| [reference](references/reference/) | A reference article provides users with descriptions of specific components or characteristics of an application. | T G P R |
| [release-notes](references/release-notes/) | Release notes communicate new features, improvements, bug fixes, and known issues about a product to users and stakeholders. | T G P R |
| [troubleshooting](references/troubleshooting/) | A list of common problems (referred to as symptoms) experienced by users, an explanation of the causes, and steps to resolve the issue. | T G P R |
| [tutorial](references/tutorial/) | Instructions for setting up an example project using the product, intended for the purpose of hands-on learning. | T G |

### Open source community pack

| Type | Use it for | Files |
|---|---|---|
| [bug-report](references/bug-report/) | The bug report is an issue template that your users can fill out to provide you with higher-quality, actionable bug issues for your product. | T G |
| [changelog](references/changelog/) | Changelogs document significant product changes in reverse-chronological order. This template offers a more technical, comprehensive alternative to standard release notes. | T G P R |
| [code-of-conduct](references/code-of-conduct/) | A Code of Conduct helps you govern your open source or developer community to ensure it remains healthy and open. | T G |
| [code-of-conduct-incident-record](references/code-of-conduct-incident-record/) | Used as part of the Code of Conduct process, an incident record is a form that is filled out when a community moderator takes an incident report from a community member. | T G |
| [code-of-conduct-remediation-record](references/code-of-conduct-remediation-record/) | Used as part of the Code of Conduct process, a remediation record is a form that is filled out when a community moderator meets with a community member to explain the consequences of a Code of Conduct violation. | T G |
| [code-of-conduct-response-plan](references/code-of-conduct-response-plan/) | Used as part of the Code of Conduct process, the response plan explains the policy your team will follow as you handle Code of Conduct incidents. | T G |
| [contributing-guide](references/contributing-guide/) | A CONTRIBUTING document tells users how they can contribute to your open source project and join the community. | T G E |
| [our-team](references/our-team/) | Our team documents help you clearly communicate who belongs to your open source project or organization and how contributors can contact or work with them. | T G |
| readme | Also part of this pack — see Core documentation pack above | |

### Miscellaneous pack (for maturing doc sets)

| Type | Use it for | Files |
|---|---|---|
| [api-getting-started](references/api-getting-started/) | API getting started describes the easiest way for readers to achieve a result that shows off the capabilities of your service. | T G P R |
| [api-reference](references/api-reference/) | API references are technical manuals that provide API specifications and integration instructions to help your audience understand the service. | T G E |
| [contact-support](references/contact-support/) | A contact support page typically includes a list of the communication channels, discussion forums, and links to other resources to assist users with issues that they are having with your product. | T G P R |
| [glossary](references/glossary/) | A reference document that lists and organizes terms and their definitions that are unique to your organization or which you use in a specific way. | T G P R |
| [installation-guide](references/installation-guide/) | An installation guide explains all the necessary steps to install the product and set it up for further use. | T G P R |
| [quickstart](references/quickstart/) | A quickstart introduces your users to your application for the first time. It focuses on the primary feature of the application and helps your users to start using the application as quickly as possible. | T G |
| [sdk-overview](references/sdk-overview/) | An SDK overview is a high-level introduction that explains what the SDK does, who it's for, and how to use it. It provides readers with a clear understanding of the SDK's purpose, requirements, and key features. | T G P R |
| [style-guide](references/style-guide/) | A style guide provides project contributors with general guidelines for writing project documentation. | T G |
| [terminology-system](references/terminology-system/) | Using this template, writing teams can ensure they consistently use and translate the same terms across all the documentation in their system. (`.csv`/`.htm` templates) | T G P R E |
| [user-personas](references/user-personas/) | User personas are a framework to identify the characteristics that differentiate each user type for your product or service. Discovering more about your users will help you make user-centric product decisions and produce better documentation. | T G P R |
<!-- END generated: content types -->

Commonly confused pairs — decide deliberately:
- **how-to vs tutorial**: how-to assumes competence and gets one task
  done; tutorial teaches by building something, and learning is the goal.
- **quickstart vs tutorial vs installation-guide**: quickstart is the
  shortest path to first value; installation-guide is exhaustive setup;
  tutorial is guided learning.
- **release-notes vs changelog**: release notes are curated for users;
  a changelog is the comprehensive, technical record.
- **concept vs reference**: concept explains *why/what it means*;
  reference lists *what exists* for lookup.

## File roles

Each type dir holds `<role>_<type>.<ext>`. Not every type has all five.

| File | What it's for |
|---|---|
| `template_` | The raw outline, with embedded writing tips. Placeholders are in `{curly brackets}`; a `>` blockquote at top and bottom is TGDP boilerplate. |
| `guide_` | Why each section exists and how to fill it in. Read this first. |
| `process_` | Researching, writing, and *maintaining* this content type over time. |
| `resources_` | The research sources and inspiring real-world examples behind the template. |
| `example_` | The template filled in for The Chronologue, TGDP's model documentation project. |

`references/writing-tips.md` holds general writing guidelines
(language and tone, procedural steps, …) that apply to every type.

## Instructions

1. **Pick the type before writing anything.** Use the tables above.
   If you were invoked as `/write-good-docs <args>` and the first word
   names a content type (e.g. `how-to`, `readme`), use that type and
   treat the rest as the subject. If the request spans several types (a README that wants to be a
   quickstart too), say so and propose splitting — each template
   is designed around one reader goal, and a doc serving two serves
   both badly.
2. **Read `guide_` before `template_`.** The guide explains what each
   section must achieve; without it the template is just headings, and
   headings get filled with filler. Read `example_` too when one exists
   — it shows the intended depth and tone.
3. **Gather real facts first.** Fill sections from the actual project
   (code, CLI `--help`, config, existing docs, git history). Never
   invent commands, flags, API fields, versions, or URLs; if a fact is
   unknown, leave a clearly marked TODO and tell the user.
4. **Adapt the structure; don't transcribe it.** Drop optional sections
   that don't apply, merge thin ones, and rename headings to fit the
   project. The user's existing conventions (their style guide, doc
   framework, heading style, docs-site front matter) win over the
   template's when they conflict.
5. **Strip all template scaffolding.** Remove every `{placeholder}`,
   the instructional text, and TGDP's top/bottom `>` boilerplate
   (the "read the accompanying guide" and "Explore other templates"
   notes). Then run
   `scripts/check-leftovers.sh references/<type>/template_<type>.md <draft>`:
   it flags any placeholder from *that template* still in the draft and
   ignores fenced code, so real braces in JSON or code samples don't
   trip it. It can't see placeholders that span several lines in the
   template, or instructional text that doesn't use braces, so still
   reread the draft yourself.
6. **Don't paste guide prose into the doc.** The guides are advice to
   the writer, not content for the reader.
7. **Apply `writing-tips.md`** as a final pass: consistent tone, spelled
   out acronyms on first use, single-sentence steps, chunked procedures,
   `Optional:` and `If …, then …` conventions.
8. **For reviews, compare against the guide.** When asked "is this doc
   good / missing anything", identify its type, then report which guide
   sections are missing, misplaced, or doing another type's job —
   ranked by reader impact — before rewriting anything.
9. **Use `process_` for lifecycle questions** (who owns the doc, when to
   update it, how to research it). `resources_` is further reading only;
   cite from it when the user wants sources.
