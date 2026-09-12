# Job Search

An AI skill that runs your job search through a conversation. Give it your resume, answer a few questions, and let it organize the work.

## Start here

Paste this into **Codex or Claude Code**, with your resume attached or its file path supplied:

> Install https://github.com/toughdave/job-search for this project. Use job-search with my resume, handle the setup, and ask one question at a time. Set a goal to prepare my first suitable application for review.

The AI may need you to approve installation or choose a writable folder. It should read this repository's [INSTALL.md](INSTALL.md), verify installation, and begin. If a fresh turn is needed for skill discovery, it should give you one short message to send. You do not need to fill out templates or edit tracking files.

When you return, say **“Continue my job search.”** Use the same project so the AI can find your saved workspace. In a different project, supply the private workspace location once.

## What it does for you

- Learns your experience and preferences without making up qualifications.
- Saves your answers and corrections as you talk, so you can pick up later.
- Checks unfinished applications and discovers new suitable jobs.
- Produces editable resumes/CVs and PDFs with a simple, readable design.
- Organizes postings, drafts, exact application answers, and confirmation evidence.
- Prepares applications for your review and supports optional scheduled searches.

The skill asks you for decisions, missing personal facts, and required approvals. It manages the folders, records, and formatting. Your private workspace is separate from the installed skill and this public repository.

## Command installation

If you prefer a terminal, with Node.js 22.20 or newer:

```sh
npx skills@1.5.26 add toughdave/job-search --skill job-search --agent codex claude-code --copy -y
```

This installs into the current project. Add `--global` only if you intentionally want it available in all projects. Then say “Use job-search with my resume.” Codex CLI also supports `$job-search`; Claude Code supports `/job-search`.

## Availability

Designed for local Codex and Claude Code sessions with file access. Other Agent Skills-compatible tools can use the core instructions, but their file, browser, document and scheduling capabilities must be checked. Installing a skill does not connect accounts or start a schedule. The AI helps set those up when you ask.

This is a workflow assistant, not a guarantee of interviews or employment. You review factual claims and final submissions. [Validation and limitations](docs/VALIDATION.md).

## For maintainers

The reusable skill is in [skills/job-search](skills/job-search/SKILL.md). The state helper uses Python 3.10+ with no third-party packages. Document export dependencies are installed only inside a private workspace environment. [Design](docs/DESIGN.md) · [Tests](tests) · [Attribution](NOTICE.md).
