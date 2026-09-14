# Harness capabilities and optional setup

Keep one portable skill body. Use actual tools exposed by the current host; do not assume a Codex tool exists in Claude Code or vice versa. Detect installed skill location, writable private workspace, resume readability, Python, document export/rendering, live web search, browser interaction, and optional scheduler/connected accounts. Inspect only what the current task needs. Ask for access as a short human action, never a technical checklist.

## Codex

Project skills use `.agents/skills`; Codex CLI/IDE allow `$job-search`, and matching natural-language prompts can select it implicitly. This release does not install globally or change the user's existing AGENTS.md or memory. Use the supported local file/browser/document tools. Native goal tools may be available; call them only when the candidate explicitly asks for a goal, preserve any active unrelated goal, and check the reported state. `/goal` is a host command, not ordinary text the skill can silently activate everywhere.

## Claude Code

Project skills use `.claude/skills`; invoke `/job-search` or a matching request. Use Read/Write/Edit/shell and available browsing/document tools within permissions. The skill uses only standard Agent Skills frontmatter; it does not depend on Claude-specific dynamic injection or a forked skill context. Keep candidate questions in the main conversation. Current versions document `/goal` as a host feature; when needed, provide one exact goal message or use an actually exposed supported mechanism. Do not claim a goal is active simply because the skill mentions it.

## Goal versus schedule

A first goal should finish at a verifiable point: saved profile plus first suitable application ready for candidate review. Start work on that target after sufficient answers. If blocked on a real candidate decision, ask and wait rather than repeating an empty loop. A goal does not authorize submission and does not create future scheduled runs.

During onboarding, offer the optional weekday morning search after target work and region are known. Follow [daily routine](routine.md) for the interview, generated prompt, actual host scheduling, run guard, recovery, tests and changes. A saved choice, installed skill or manual test is not proof of a working timer.

## Gmail and calendar

Follow the [mail connection interview and account checks](mail.md). They are optional. Use the candidate's own chosen connector and account. Connect through the host UI/approved tools; do not ask for passwords or copy another person's credentials. Check the requested scope with a bounded read. Preserve the distinction between drafting a reply/event and sending/creating it. Store consent and scope, never tokens. If mail is unavailable, process candidate-supplied messages as explicitly candidate-supplied evidence.

## Other agents

The open format makes the core instructions portable. Installation support alone is not full behavioral compatibility. Verify tools and permissions before claiming local saves, web discovery, browser application work or scheduling. An ordinary browser chatbot cannot acquire local filesystem control merely by receiving a skill attachment. Keep that distinction visible without making the candidate manage file formats.

## Official references checked 12 September 2026

- [OpenAI skills](https://learn.chatgpt.com/docs/build-skills)
- [OpenAI goals](https://learn.chatgpt.com/docs/long-running-work)
- [OpenAI scheduled tasks](https://learn.chatgpt.com/docs/automations)
- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [Claude Code goals](https://code.claude.com/docs/en/goal)
- [Claude Code Desktop scheduled tasks](https://code.claude.com/docs/en/desktop-scheduled-tasks)
- [Claude Code scheduling](https://code.claude.com/docs/en/scheduled-tasks)
- [Agent Skills specification](https://agentskills.io/specification)
- [Skills installer](https://github.com/vercel-labs/skills)

Recheck current host documentation when behavior differs. No account connections or schedules are distributed in this package.
