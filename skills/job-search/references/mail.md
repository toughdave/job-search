# Connect the right inbox

Email access is optional. Offer it after confirming the application email, before configuring inbox checks in a daily routine. Use the saved `mail-choice` topic, dimension `decision`, and ask one question: **“Would you like me to connect the inbox for {confirmed application email} so I can check job-related replies?”** Save yes, no or later. Do not ask again when a current answer exists. A Gmail address on a resume is not permission, and signing into the AI app with Google does not prove a Gmail connector is connected.

If yes, use the application address as the default. If the person wants another primary inbox, ask for that mailbox and save the explicit choice. Do not silently equate aliases, remove dots or plus tags, or infer that a custom-domain mailbox uses Gmail. Keep the confirmed application address on resumes unless the person changes it. This setup handles one selected primary inbox per project; do not combine other accounts without a separate explicit scope decision.

## Reuse setup done in the app

The first-time guide offers optional Gmail connection in step 1, before the skill installation prompt. The person may therefore arrive with a working connection. After confirming their application email and job-mail read permission, discover the current host's tools and verify the existing authenticated account and bounded read. Do not make them reinstall, disconnect/reconnect or answer a connection question when that verification succeeds. Only guide a connection or account switch when tools, identity or access checks show it is necessary.

Connecting the app beforehand is not itself this project's read consent, identity verification or permission to send mail. Save the one project-specific mail choice as usual. If they skipped app setup or choose no/later, continue the rest of the interview without requiring Gmail; use the connection recovery below only when they choose inbox help.

## Connection interview and verification

1. Save the confirmed application email as a current profile fact containing exactly one address. Save the permission response with `save-answer`, or `record-statement` when volunteered. The `choose` helper makes `mail-choice` coverage derive from this saved decision, so it is not asked again. An application-email change reopens the decision. Offer a bounded job-mail lookback, initially 14 days, and save the agreed scope. Reading relevant replies is separate from sending, labels, archive, deletion, draft creation inside Gmail or calendar changes.
2. Discover the mail tools and plugin/connector available in the **current harness**. If absent, use an available plugin-discovery/connection tool or the host's official UI. Ask for just the next human action: connect Gmail and choose the displayed email. Do not request passwords, OAuth codes, tokens or credentials files. Do not install an arbitrary third-party mail server or disconnect another account to bypass a missing capability.
3. The person completes Google's sign-in/consent flow. Then call the connector's authenticated-profile/account tool, such as an exposed Gmail `get_profile`, and compare its actual returned email with the saved mailbox. Inspect account metadata before reading message content. Neither an installation badge, recipient header, search filter, browser tab nor “yes, connected” answer proves the connector's identity. If no identity method exists, inspect an authoritative connected-account UI; if identity remains uncertain, keep mail blocked.
4. If the account differs, explain the mismatch and ask the person to connect/select the intended mailbox. Do not search the wrong inbox to see whether their messages happen to be there. If they explicitly choose the other mailbox instead, save the new scoped decision and repeat setup. No implicit Gmail alias equivalence.
5. After an identity match, perform one bounded, read-only job-mail search within the agreed lookback (at most 20 results for setup). Prefer known application employers/thread IDs. A successful query returning zero messages verifies query access, not absence of every job reply. A permission error, missing tool, quota or expired connection is blocked. Save minimal metadata, not unrelated email contents.
6. Read back the saved binding. Say “Inbox ready for job-related reads” only after identity and read access are verified in this harness. Codex and Claude have separate binding records; a successful connection in one does not establish access in the other. Continue resume work or discovery while connection is pending, declined or unavailable.

## Where the person connects

- **Codex desktop:** open **Plugins**, find Gmail, install/enable it if needed, and complete its connection flow. Start a new session if tools do not appear. **Codex CLI:** `/plugins` opens the plugin browser. Verify that the chosen plugin actually exposes mail tools in that session. Availability can depend on authentication and organization settings. [Official plugin instructions](https://learn.chatgpt.com/docs/plugins).
- **Claude Code desktop:** in a local/SSH session, use **+ → Connectors**; manage connections through **Settings → Connectors** or **Manage connectors**. Authenticate the intended Google account. A separately configured legacy desktop-chat MCP server is not automatically a Code-tab server. In CLI, inspect the supported connector/MCP configuration available there rather than promising that a desktop setting propagated. [Claude Code desktop connectors](https://code.claude.com/docs/en/desktop), [Google Workspace connectors](https://support.claude.com/en/articles/10166901-use-google-workspace-connectors).

These official routes were checked on 14 September 2026. Follow the actual UI if labels change. The job-search skill itself does not ship credentials, install Gmail silently, or grant account permissions.

If the person must connect it, save one pending question before asking them to act. Create an optional shared profile topic `mail-connection` with dimension `connection` through the [state transaction workflow](state-schema.md), then use `ask --topic mail-connection --dimension connection` with a single request such as “Please connect Gmail through Settings → Connectors as {selected email}, then tell me when it is connected.” Save their response and verify actual identity/access before marking that topic answered. Keep the permission choice separate. A saved account-level connector can persist across sessions, but its tools may be unavailable in a particular session; do not claim that all connections disappear between sessions.

When no authenticated identity can be obtained, leave `bindings` empty and report `needs_connection`. Do not create an observation with a guessed email or placeholder identity tool. Connector availability alone belongs in a local status note, not an authenticated-account record.

## Private record and helper

The AI runs the commands; the candidate never edits these records. `W` is the private workspace. All helpers use its verified Python runtime.

```sh
python S/scripts/mail_accounts.py choose --workspace W --choice enabled --email-fact EMAIL_FACT_ID --decision-source ANSWER_SOURCE_ID --lookback-days 14 --expected-revision N
```

Use `--mailbox-email OTHER_EMAIL` only for the person's explicit alternative choice. `--choice declined` or `deferred` requires their decision source but no email fact. Changing the choice resets saved bindings; old source snapshots remain preserved. Renew permission when the scope or account changes, not every ordinary read in the already agreed scope.

After actual host tool calls, write a sanitized observation to `W/scratch/mail-check.json`:

```json
{
  "harness": "codex",
  "connector": "actual exposed Gmail connection ID",
  "authenticated_email": "person@example.com",
  "checked_at": "2026-09-14T12:00:00+00:00",
  "identity_tool": "actual profile tool name",
  "identity_call_id": "actual tool call or account-UI observation reference",
  "read_tool": "actual search tool name",
  "read_call_id": "actual search call reference",
  "read_status": "complete",
  "query": "the bounded job-related query actually used",
  "inspected": 0
}
```

Values above are illustrative, never evidence to copy. Use `claude-code` or `other` for the actual harness. `read_status` is `complete`, `blocked` or `not_attempted`; use empty read fields and zero inspected when identity mismatches and no search was made. Save no tokens, passwords, full mailbox export or unrelated message bodies. The helper rejects extra fields and successful-read claims for a mismatched account.

```sh
python S/scripts/mail_accounts.py observe --workspace W --file scratch/mail-check.json --expected-revision N
python S/scripts/mail_accounts.py plan --workspace W --harness codex --authenticated-email EMAIL_FROM_FRESH_PROFILE_CALL
```

Only `ready_for_read: true` permits continuing this mail workflow. Without a fresh identity argument the helper returns `needs_live_identity_check`, even with a recent saved binding. Older-than-24-hour or future-dated observations require re-verification. A changed/superseded application-email fact, another harness, account mismatch, or failed read blocks readiness. Run `choose` again after an explicitly confirmed account/email change. Tool observation files are recorded by the AI: schema, hashes and references establish consistency, not proof that a remote call actually happened. Always inspect the real tool/UI result and preserve its reference.

## Daily use and interruptions

Before each mailbox session or scheduled run, check current connector identity and access again; never rely on a previous host or login. Use the saved lookback, watermark plus overlap, thread IDs and pagination for relevant mail. Store coverage per chosen mailbox. If permission is revoked or the tool fails mid-run, record blocked/partial coverage and retain the cursor. If mail is required, the run is incomplete; independent job discovery can still proceed. Never substitute “no new replies” for inaccessible mail.

Google Calendar is a separate optional connection. The person may connect it during app setup too; reuse and verify that existing connection instead of prompting another sign-in. Offer it when interview scheduling is useful, verify its account/calendar ID independently and record its own consent; Gmail access does not authorize creating events. Sending email or changing a calendar always requires the applicable action authorization. Local reply drafts need no connected mailbox.
