---
name: job-search
description: Start and continue a personal job search inside the conversation. Read a resume, interview the candidate, manage a separate private workspace, search and screen jobs, prepare formatted resumes or CVs, and track applications and replies. Use for onboarding or continuing this workflow; not for live assessments or recruiting other people.
license: MIT
metadata:
  version: "1.1.0"
  compatibility: Local AI agent with file access; Python 3.10+ for state management. Web, browser, document export and scheduling depend on available tools.
---

# Job Search

You operate the workflow; the person supplies their resume, answers, feedback and decisions. Keep the conversation in ordinary language. Never require them to edit JSON/Markdown, import/export a tracker, arrange folders, install a second skill, or read a manual. Do the work with available tools. Ask for one short action only when their input or the harness genuinely prevents progress.

## Start or resume

Read [workspace operations](references/workspace.md) before any workspace write. Resolve resources relative to **this installed skill**, not the current directory. Use `scripts/workspace.py` for state and file writes; do not replace it with ad hoc writes. It guards a NEW private workspace, uses revisions and backups, and refuses unknown schemas. Never modify another candidate's pipeline, global memory, global skill configuration, connections, or schedules as part of onboarding. Private files must stay outside the installed skill and public source checkout.

Find only the workspace explicitly supplied or recorded for this conversation/project; do not crawl home directories or infer identity from the machine account. If no workspace exists, propose a new empty sibling folder and initialize it within the available write permission. Explain its friendly name once. A scope or location decision can be the first short question if necessary. If a folder already contains files, choose a new one; never adopt it automatically. Preserve the resume as a source copy without moving or altering the original.

On every return, read current state from disk and any pending work before deciding the next action. A newer explicit correction outranks earlier candidate data. Use a workspace-local status note for handoff; the state file is authoritative. Do not rely on conversational memory or regenerate the candidate profile from an old draft.

## Conversational onboarding

Read [project onboarding](references/onboarding.md) and [interview and evidence](references/interview.md). One-question pacing, waiting for answers, evidence gathering and file management are defaults even when invoked with only “Use job-search.” Bind the private interview to the actual selected project, verify resume intake, and run the evidence-derived checklist on every return. Never infer an attached/read resume from installation or a candidate saying yes. If no resume exists, record that answer and help build one from supported experience.

Ask **one short question at a time**, then wait; use a recommendation for process choices and never suggest a personal fact as the answer. Check saved facts and exact answers before asking. Save a pending question before presenting it; save each answer or correction immediately, read it back, and reconcile coverage before proceeding. Missing checkmarks are not proof of missing answers.

Establish target work, country/region and essential constraints; ask about missing evidence when it affects a decision. One question means one decision: ask about target work first, then location in a later turn if still unknown. Do not bundle “what role and location?” into a single question. Let a candidate without a resume describe their most recent work or study. Begin one useful fit check or draft as soon as enough is known. Continue the interview only where the next task needs it. Do not conduct an endless “complete your whole profile first” interview.

Expand the evidence bank beyond resume bullets with a small set of real, occupation-relevant scenarios: context, personal actions, tools/methods and a supported result or lesson. Ask only missing details, accept an honest lack of experience, and preserve project/volunteer/study boundaries. Offer an optional LinkedIn review once and save the choice. A new project gets an independent interview and evidence bank; reuse another project's material only through explicitly authorized copying, never automatic access or inherited checkmarks/consent.

## Do the search and application work

Read [search and applications](references/search.md) when screening, searching, preparing forms or handling employer replies. Every recurring search covers unfinished work and fresh discovery in the agreed scope. Record what was actually checked, including blocked sources. Save complete postings when available, deduplicate, and explain fit using sourced evidence. A thin resume means “ask or investigate,” not “no experience.”

Read [documents](references/documents.md) when drafting or exporting a resume, CV or letter. Use the bundled layout and export helper or a verified available document tool. Handle dependencies in the private workspace only. Select relevant truthful evidence, preserve the master, create a new version for each draft, and inspect the actual exported pages. Present the documents and one next action, not implementation details.

Prepare supported application fields through final review within existing authorization. Ask for explicit approval for the specific final submission if not already authorized. Login, CAPTCHA and live assessments stay with the person under the harness's rules. Never invent an approval or reuse another candidate's consent. Confirm the employer's receipt before marking submitted; a report of clicking Submit without confirmation stays unverified. Posting closure is separate from the application outcome.

## Continue, goals and optional automation

“Continue my job search,” “What needs attention?” and “Tailor my resume for this job” all use the same private workspace and conversation workflow. Record corrections and progress after each meaningful step. Persist a pending action before a consequential browser action; inspect employer state on recovery before retrying so a crash cannot cause duplicate submissions.

Read [harness capabilities](references/harnesses.md) only when installing, connecting tools, setting a goal, or scheduling. A first goal should be measurable: private profile saved and one suitable application prepared for review, or an evidence-backed explanation that a required candidate decision prevents that result. Use native goal features only when the user explicitly requested a goal and the feature is available; verify activation. A goal is not a recurring schedule and does not broaden permissions.

The person may authorize a recurring schedule conversationally. Ask only for missing time, timezone, scope and notification preferences; create it with the harness's supported scheduler, record its actual ID, and verify an observed scheduled run. Do not claim a timer is working from a manual test. Keep unchanged monitoring quiet unless asked otherwise. Account connections are optional and must use this candidate's own authorization.

## Finish each interaction

Save and verify meaningful changes before responding. Summarize the useful result in a few sentences and show the next question **or** next action. Do not list file-maintenance chores. A turn that needs a candidate answer must wait for that answer; silence is not agreement. If tools are unavailable, identify the single missing capability honestly and preserve progress instead of pretending the action succeeded.
