# Harness capabilities and optional setup

Keep one portable skill body. Use actual tools exposed by the current host; do not assume a Codex tool exists in Claude Code or vice versa. Detect installed skill location, writable private workspace, resume readability, Python, document export/rendering, live web search, browser interaction, and optional scheduler/connected accounts. Inspect only what the current task needs. Ask for access as a short human action, never a technical checklist.

## Codex

Project skills use `.agents/skills`; Codex CLI/IDE allow `$job-search`, and matching natural-language prompts can select it implicitly. In Codex / ChatGPT desktop, use `@` to select job-search, or the `$` picker if that is what the current composer exposes. This release does not install globally or change global memory; preserve existing project instructions when adding startup reminders. Use the supported local file/browser/document tools. Native goal tools may be available; call them only when the candidate explicitly asks for a goal, preserve any active unrelated goal, and check the reported state. `/goal` is a host command, not ordinary text the skill can silently activate everywhere.

## Claude Code

Project skills use `.claude/skills`; invoke `/job-search` or a matching request. Use Read/Write/Edit/shell and available browsing/document tools within permissions. The skill uses only standard Agent Skills frontmatter; it does not depend on Claude-specific dynamic injection or a forked skill context. Keep candidate questions in the main conversation. Current versions document `/goal` as a host feature; when needed, provide one exact goal message or use an actually exposed supported mechanism. Do not claim a goal is active simply because the skill mentions it.

## OpenCode

The pinned skills installer uses `.agents/skills/job-search` for OpenCode. Manual copies can instead use `.opencode/skills/job-search`; compatible `.claude/skills` is also discovered. No `opencode.json` change is needed for these standard folders. Prefer the existing valid copy rather than adding duplicates. The portable composer message is `Use job-search to continue my job search.` Verify native loading through the `skill` tool. Some versions expose skills in a slash menu; recommend `/job-search` only when actually listed. Do not invent a custom slash command or change global configuration to make it appear.

## T3 Code and wrappers

T3 is a UI over a selected provider. Detect that provider and its actual project/environment; use the corresponding installation target (`codex`, `claude-code` or `opencode`) and directories. Current T3 documentation uses `$` to choose provider skills, with optional skills in the `/` menu. Recommend selecting **job-search** from that picker, not blindly forwarding the provider's native slash syntax. Older versions may differ; when discovery is unavailable, read the installed file and use an explicit natural-language invocation without claiming the picker works. A remote environment needs the skill and records on that environment's machine.

## Loading and refresh

After copying, load the installed SKILL.md and supporting resources in the current conversation when possible. This can start onboarding immediately; it does not prove native discovery. Check the host's available-skill list/tool or picker separately. Do not demand a restart on every install.

- Codex documents automatic skill-change detection; restart Codex if discovery remains stale.
- Claude Code watches existing skill directories. If the top-level skill directory did not exist at session start, its docs require restarting Claude Code to watch the new directory. File loading can still allow useful work now.
- OpenCode versions differ: try current loading first, then a fresh session in the same project if missing; restart the app/server only for a persistently stale catalog.
- T3: verify project, environment and provider first, then try a new task if discovery is missing. If that does not refresh it, restart the affected provider/app. Restarting a UI does not necessarily restart its remote provider.

When recovery is needed, save existing progress and give exactly one human action with the same project location and return message. Explain whether it means a new conversation or closing/reopening the app/provider. Never clear records, reinstall in a loop, or call a file copy verified activation.

## First setup handoff

When the person stops, asks how to return, or reaches the first useful handoff after setup/interview, write a short private `notes/how-to-return.md` under the verified records workspace, even during partial setup. Include the current app/provider, actual project and records locations, the chosen summon action, native discovery status (observed or unverified), and the one current next action. Save that concrete next step in `session.next_action`; if fact mapping is unfinished, say exactly what remains rather than claiming the profile is complete. Keep account credentials out. Update it on an app/provider change; reread the project pointer and pending question before resuming. Do not invent a new state-schema field or mark pending interview topics complete to create the note.

Show a brief version to the candidate: actual progress, “Next time, reopen [project] and [this app's exact summon action],” and one next action. For example, in T3: “Next time, reopen My Job Search, type `$`, choose job-search, and send ‘Continue my job search.’” Use the natural-language fallback if native discovery has not been observed and state that limitation briefly. If a saved question is pending, retain it as the final question; a return reminder is future-use information, not a second request now. Pass this reply through the usual `finish-reply` check. Do not show every app's instruction table or repeat this handoff during each interview turn.

## Goal versus schedule

A first goal should finish at a verifiable point: saved profile plus first suitable application ready for candidate review. Start work on that target after sufficient answers. If blocked on a real candidate decision, ask and wait rather than repeating an empty loop. A goal does not authorize submission and does not create future scheduled runs.

During onboarding, offer the optional weekday morning search after target work and region are known. Follow [daily routine](routine.md) for the interview, generated prompt, actual host scheduling, run guard, recovery, tests and changes. A saved choice, installed skill or manual test is not proof of a working timer.

## Gmail and calendar

Follow the [mail connection interview and account checks](mail.md). They are optional and may already be connected before skill installation. Verify and reuse a working connection; request setup only when needed. Use the candidate's own chosen connector and account. Connect through the host UI/approved tools; do not ask for passwords or copy another person's credentials. Check the requested scope with a bounded read. Preserve the distinction between drafting a reply/event and sending/creating it. Store consent and scope, never tokens. If mail is unavailable, process candidate-supplied messages as explicitly candidate-supplied evidence.

## Capability limits in other hosts

Verify local read/write, Python execution and model/tool support before starting. Image viewing must reach the model's vision context; generating PNGs is insufficient. Missing browsing, rendering, connectors or scheduling leaves that stage pending while independent work continues.

The current `routine.py` schema accepts active native schedules only for `codex_desktop` and `claude_desktop`. For OpenCode/T3, retain manual or pending routine status and provide the saved prompt; never label a wrapper as one of those desktops to bypass validation. `mail_accounts.py` uses `--harness other` for OpenCode and wrappers, with fresh current-host identity/read evidence and an explicit connector/provider description. A stored `other` binding or a desktop login cannot establish access in another wrapper. Never reuse an observation from a different live host.

## Other agents

The open format makes the core instructions portable. Installation support alone is not full behavioral compatibility. Verify tools and permissions before claiming local saves, web discovery, browser application work or scheduling. An ordinary browser chatbot cannot acquire local filesystem control merely by receiving a skill attachment. Keep that distinction visible without making the candidate manage file formats.

## Official references checked 14 September 2026

- [OpenAI skills](https://learn.chatgpt.com/docs/build-skills)
- [OpenAI goals](https://learn.chatgpt.com/docs/long-running-work)
- [OpenAI scheduled tasks](https://learn.chatgpt.com/docs/automations)
- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [Claude Code goals](https://code.claude.com/docs/en/goal)
- [Claude Code Desktop scheduled tasks](https://code.claude.com/docs/en/desktop-scheduled-tasks)
- [Claude Code scheduling](https://code.claude.com/docs/en/scheduled-tasks)
- [OpenCode skills](https://opencode.ai/docs/skills/)
- [OpenCode V2 skill catalog](https://opencode.ai/v2/docs/skills)
- [T3 commands and skills](https://github.com/pingdotgg/t3code/blob/main/docs/user/composer.md#commands-and-skills)
- [T3 Claude provider skills](https://github.com/pingdotgg/t3code/blob/main/docs/user/providers-claude.md#skills)
- [Agent Skills specification](https://agentskills.io/specification)
- [Skills installer](https://github.com/vercel-labs/skills)

Recheck current host documentation when behavior differs. No account connections or schedules are distributed in this package.
