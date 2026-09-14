# Evidence-backed onboarding for the AI

Pacing, questions, file management and saving are defaults. The person can simply say “Use job-search.” Never require the person to repeat operating instructions or edit a checklist.

## Identify this project first

Read the actual selected project path P and the explicitly supplied or project-recorded workspace W. Resolve real absolute paths, not names inferred from the computer account. Use a new private workspace for a new project or independent occupation search. Never scan, adopt or write another project's evidence bank just because it belongs to the same person. If the person explicitly requests reuse, ask which source workspace/files to copy; preserve originals, copy only authorized material into the new W, retain provenance, and assess relevance for the new occupation. Do not copy its completion flags, consent or project binding.

After initializing W (or upgrading an existing schema-v1 workspace), bind it once:

```sh
python S/scripts/onboarding.py bind --workspace W --project P
python S/scripts/onboarding.py plan --workspace W --project P
```

`bind` writes `.job-search-project.json` in P with W's exact path and workspace ID (plus a relative path if W is within P). Read this pointer first in each new session; never search parent folders for candidate records. A repeat `bind` repairs a missing pointer for the same workspace. It refuses to overwrite a pointer belonging to another workspace. Do not put the pointer in a public checkout or global instructions. On each turn, use the real current project path for `--project`; do not substitute the saved path to bypass a mismatch.

For a renamed/moved project, `workspace.py show` still reads and validates the evidence. Ask the candidate to confirm the new project location and save that decision as a candidate source. Run `rebind --workspace W --project P --workspace-id ID --decision-source SOURCE_ID --expected-revision REVISION`. This preserves answers and identity, appends binding history, and refreshes the pointer. It pauses any active saved routine until native schedule paths are checked again; it cannot change the actual host timer. If the pointer's old absolute W path is unavailable and there is no working relative path, ask for the new records location once. Never scan the computer or start a replacement empty bank. A copy for a different candidate/search must be a separately authorized import into a new workspace, not a rebind.

## Save one question and answer

Use these transactions instead of hand-building pending Q&A records:

```sh
python S/scripts/onboarding.py ask --workspace W --project P --topic target-work --dimension occupation --question "What kind of work would you like to find?" --expected-revision REVISION
python S/scripts/onboarding.py save-answer --workspace W --project P --question-id QUESTION_ID --answer-file W/scratch/answer.txt --interpretation "Candidate's stated target work" --expected-revision REVISION
```

Resolve `python` to the detected runtime (`python3` on many Macs/Linux systems; `py -3` or a full executable path on Windows). Write the exact received answer to the UTF-8 input file. `ask` returns the saved question ID; present that exact question and wait. `save-answer` saves the source and exact Q&A, updates `session.next_action`, and leaves coverage pending. Then use the [schema examples](state-schema.md) to map only supported facts and evidence and commit. Run `plan` again. A retry with the same answer is idempotent; a changed answer needs an explicit sourced correction. Do not ask a second question while a pending question or unmapped answer needs attention. One topic can have multiple dimensions, but one question must address only one decision.

## Resume intake is a real check

For `save-answer`, copy the **entire received message**, including a pasted posting, additional facts, punctuation and line breaks. Do not keep only the sentence that answers the pending question. Read back `answer.answer` and `captured_characters` against the received message. This checks your copy, not an automatic connection to the composer. You may also preserve the posting separately as an employer source; that does not replace the full original message, and posting duties must never become candidate facts.

Use topic `linkedin-url` / dimension `url` for the profile URL or its inclusion/omission on the resume. Topic `linkedin` / dimension `decision` is solely the optional profile review choice. These are separate questions and separate decisions. The helper catches common English topic mismatches and obvious compound interrogatives; you must still check the meaning and keep each turn to one decision in every language.

Inspect the current attachments, supplied paths and this workspace's saved sources. An installation is not evidence of an attachment. A file icon or the candidate saying “yes” is not proof that the file was received or read.

- If a resume is actually available, preserve the source, read/extract it, save readable text, and record `resume.status=read`, the original resume source ID(s), and `text_source_id`. The helper requires a saved `resume` source plus nonempty UTF-8 TXT/MD text. Check extraction meaning and completeness yourself; the helper cannot prove the extraction matches the original.
- If no resume was supplied and no previous intake decision exists, ask: “Do you have a resume you would like me to use?”
- If yes, save the exact answer, record `awaiting_file`, ask for the attachment or its full location, and wait. If unreadable, record `unreadable` and request readable text or another copy. Do not claim to have read it.
- If no, save the answer and record `no_resume`. Continue with work, study, projects and volunteering. Build a general resume from supported facts; leave genuinely missing details unresolved rather than fill them with fictional defaults.
- Resume this state after interruptions. Do not repeatedly ask a person who already said no. Check for newly supplied documents on later turns and update intake with sourced evidence.

## Expand beyond resume bullets

Establish the target occupation, then create an occupation track with a unique ID, label and candidate source IDs. Set `active_track`. Baseline topics cover location/constraints, background/education and the LinkedIn choice. Read the resume and saved facts to fill what is already known.

## Resume and CV profile details

Collect these through the same one-question, save-and-resume workflow. Read the resume and existing answers first. Required topics mean they must be addressed or explicitly declined/not applicable; they do not require the candidate to disclose every item. Save explicit none/no answers as candidate-reported facts, and use dispositions for declined or deferred topics.

- **Contact:** name to use, email and phone (including country code when needed), and city/region/country through the location topic. Confirm which contact details to use if sources conflict or may be outdated. A full street/postal address is optional and normally omitted from a resume; ask only when the candidate wants it or a particular form requires it. Never infer a private address from the computer account.
- **Education:** inventory all relevant degrees, diplomas and other formal qualifications. For each, save the exact qualification/program, institution, dates or expected completion, and completed/in-progress/incomplete status. Ask about missing details one at a time, and whether any qualifications remain unlisted. Add a required profile topic per qualification with dimensions `qualification`, `institution`, `dates`, `status`; reuse facts already in the resume. An explicit no-formal-qualification answer is valid. Do not promote a course to a degree.
- **Certifications and licences:** ask whether any exist beyond the resume. For each, save its exact name, issuer, achieved/in-progress/planned status, issue date and expiry/current standing when applicable. Ask only missing details, then confirm the list is complete. Add a required profile topic per credential with dimensions `name`, `issuer`, `status`, `dates`. Use candidate-confirmed unknown/not-applicable date facts honestly. A public verification link is useful if available; never require a private credential number. A course, exam preparation or expired certificate cannot become a current certification claim.
- **Search preferences:** target roles, city/region/country, remote/hybrid/on-site preference, willingness to relocate and destination limits, plus relevant work authorization/sponsorship constraints. Relocation willingness does not establish residence or work authorization. Ask about travel, shifts, employment type, availability/notice period or compensation expectations only when they affect this search or application. Store scoped answers; do not import the guide author's preferences.
- **Additional evidence:** review skills and tools with proficiency/context, languages, portfolios/GitHub, relevant projects, volunteering, achievements/awards, publications, presentations and professional memberships where useful for that occupation or CV. Offer relevant categories rather than interrogating everyone about every category. Add separate topics for material gaps. References are optional; do not collect or publish another person's private contact details by default.

Keep education and certification records distinct from employer experience entries. Use titled profile topics and linked facts for each qualification; do not require an employer story for a degree. Complete the shared education/certifications dimensions only after reconciling the actual inventory and its candidate confirmation; a mention of one degree or certificate is not confirmation that none are missing. Resume facts can fill individual details without invented Q&A. Professional licences, current certification status and unsupported skill claims need explicit review before employer-facing use.

On upgrades, `plan.missing_baseline_topics` supplies new topic definitions. Append these to onboarding, reconcile saved facts and exact answers, then ask only for what is still missing. Do not clear old answers or restart the interview. Location, education, contact, certification and relocation coverage use the same derived evidence checks and saved dispositions as other topics.

## Employer-specific evidence

Build an **employer/role-period inventory** before declaring history coverage complete. Every employer in the resume needs an entry; split promotions, different duties and separate periods at the same employer. Preserve reported date precision (years alone are valid), `Present`, and genuinely unknown dates. Ask for missing dates separately; never invent months or collapse different employers into one story.

With a resume, extract each employer, title, period and bullet into sourced facts and reconcile the list with the candidate. Without a resume, ask for the most recent employer or work arrangement, then the role, start and end period in separate turns where missing. Ask about responsibilities and examples for that entry, then ask for another employer. Include self-employment and volunteering under their actual category. If there is no employment history, record that answer and use study, projects or volunteering where available.

Ask explicitly whether any other employers or periods remain to be added. A readable resume, a list of roles, or silence does not confirm an exhaustive inventory. Save the exact yes/no answer and the inventory it confirms in `history_reviews`. If the candidate says there are more, keep collecting them. If they pause or decline, preserve progress and leave full-history confirmation pending; useful drafts can still proceed.

Reuse the latest history review when its inventory, candidate source and status are unchanged. Do not append a second confirmation from the same statement. A changed inventory, decision or genuinely new candidate confirmation can produce a new review. Historical duplicates remain readable; do not rewrite or delete old evidence to tidy them.

For **each entry**, add a required shared `profile` topic with dimension `responsibilities`, and at least one required occupation-specific `example` topic, both with `experience_id`. Title them with employer, role and period. Review all existing bullets and answers first: use already supported details; ask targeted follow-ups for vague duties, outcomes, tools, individual contribution or distinctive achievements. Add complementary topics where different bullets or a posting reveal a meaningful gap, not a fixed two-story cap across the whole career.

If there are no experience entries, add one required general occupation-specific `example` topic without an employer ID. Ask whether a study, personal or other relevant example exists. An explicit `no_example` disposition is valid; no employer or achievement should be invented to complete onboarding.

For example, if a resume says “Coordinated shift schedules” at Cedar Clinic, Office Assistant, 2022-2024, ask: “At Cedar Clinic, you mention coordinating shifts. Tell me about one scheduling problem you handled in that role.” Follow with only missing details. Without a resume, first establish what the candidate actually did there, then choose a specific scenario question. Expected duties can inform neutral questions such as “Did that role involve scheduling?”; they must not become resume bullets unless the candidate confirms them. Never suggest invented achievements or metrics.

For each story use dimensions `context`, `personal_action`, `tools`, `result`. Keep the employer, role and period attached to its question, exact answer and derived facts. Ask only missing follow-ups, one per turn: what the person personally did, which tools/methods they used, what changed, and how the result is known. Keep collaborators' work separate. Results may be qualitative or a lesson; never pressure the person to invent a metric. A declined/no-example disposition records a limitation rather than fabricated experience. Deferred employer topics remain incomplete and resume only when appropriate.

This is a finite initial interview, not a repeated daily questionnaire. Save progress after every answer. Start useful drafts while deeper topics remain pending; do not mark onboarding complete until required topics are answered or have explicit dispositions. A candidate may decline, defer, report no example, or explain why something is not applicable. Save that decision and its limitation, then continue useful work. Deferred topics stay incomplete but are not asked repeatedly until the person asks to resume or the topic becomes necessary for a specific task.

## The checkbox is a view, not proof

Run `plan` every time this workflow resumes. It computes status from current evidence and lists missing dimensions, saved unanswered questions and answers awaiting evidence mapping. It ignores manually supplied `checked` flags. The derived checklist appears in `notes/STATUS.md`.

Before asking about any missing dimension, read the existing facts AND exact interview answers in W. Search semantically: an answer about “restoring service” may satisfy “incident resolution” even with different words. A status of unanswered means coverage has not been recorded, not necessarily that the person never answered.

If a saved answer already resolves it, map that evidence and commit, then recompute; **do not ask again**. If a saved answer is partial, ask only for the missing detail. If a question was saved but the answer was not received, resume that question. If the answer is in the transcript but the commit was interrupted, persist it first. Unknown or superseded facts cannot complete a dimension. On a correction, supersede the old fact, add its replacement, and map only what the new fact supports. Preserve prior questions and evidence.

## State records

Use the existing workspace `commit` command to save all changes with the revision read from disk. `onboarding` is an optional version-1 extension, bound to workspace ID and canonical project path; old workspace facts are preserved. The helper derives completion but the AI must judge whether the linked claims actually answer the question.

- `tracks`: `{id, occupation, source_ids}`. Keep tracks; switch `active_track` instead of renaming an old occupation.
- `experiences`: `{id, employer, role, start, end, kind, fact_ids, source_ids}`. One entry per employer/role-period; `kind` is `employment`, `self_employment`, `volunteering`, `project` or `education`. Identity/date facts must substantiate the entry. Add `experience_id` to new role-specific facts. Older facts may be linked through the entry's `fact_ids` after semantic reconciliation; do not rewrite immutable facts to add metadata.
- `history_reviews`: `{id, status, experience_ids, resume_source_ids, answer_id, source_ids}`. Save the exact inventory-confirmation Q&A using a shared profile topic such as `background`/`roles`. `status` is `complete` or `more_to_add`; `experience_ids` lists the current entries and `resume_source_ids` copies the current intake's source IDs. Empty entries require an explicit no-work-history answer. A new entry or changed resume invalidates the old confirmation until reconciled and confirmed again.
- `topics`: `{id, track_id, kind, title, required, dimensions, experience_id?}`. `track_id:null` is shared only within this private workspace. Each new occupation gets its own employer-specific example topics. Reuse relevant local facts through new explicit mappings, not copied completion flags. General study/skills topics can omit `experience_id`.
- `questions`: `{id, topic_id, dimension, question, asked_at}`. Save the exact question **before** presenting it. Do not create a new duplicate while one is pending.
- Existing `interviews` can add `onboarding_question_id`. Save the exact received answer immediately. `plan` reports these answers even if evidence mapping was interrupted.
- `evidence`: `{id, topic_id, dimension, fact_ids, source_ids, answer_ids, rationale}`. Map one answered dimension per record; explain its relevance. Sources must support the facts. Map resume-established facts without fabricating a Q&A entry.
- `dispositions`: `{id, topic_id, status, source_ids, reason}` with `declined`, `deferred`, `not_applicable`, `no_example`, or `reopen`. A candidate decision is required. These resolve or defer a question, not prove professional experience. The latest disposition wins. `reopen` restores evidence-based evaluation.

Tracks, topics, questions, evidence mappings and dispositions are append-only. The saved fact/answer is authoritative; a missing or false checkbox must not erase it. `ready_to_close_interview` is an interview flag, not an application-ready or hiring-readiness judgment.

Experiences and history reviews are also append-only. Correct a role/date entry by appending a replacement with `supersedes` pointing to the old experience ID, then map new topics to the replacement and reconfirm the inventory. Keep old Q&A and topics for history; they are excluded from current coverage. Superseded identity facts reopen the affected role. Do not move a story between employers just to satisfy a checkbox.

Older workspaces remain readable. On upgrade, `plan.work_history` reports missing inventory and employer coverage even if a former generic interview was marked complete. Reconcile the existing resume, facts and answers into entries before asking for anything new. The helper checks references and scope, not whether every employer was extracted or the candidate really said the interpreted answer; the AI must inspect the source and confirmation meaning.

## Common application answers

After the essential profile or when a form needs it, use [reusable application questions](application-questions.md) for work authorization, sponsorship, start dates, compensation, logistics and scoped screening answers. Let the candidate choose now or just-in-time collection. Save their choice and each answer; do not turn installation into a compulsory long questionnaire.

## LinkedIn: early link, richer evidence, later review

Follow [LinkedIn and the evidence bank](linkedin.md). The `linkedin-url` topic captures a confirmed profile link for the resume or explicit omission early; the existing `linkedin` topic records the optional review choice separately. Reconcile authorized profile content during the interview, then prepare the fuller review after enough career information is gathered. `plan.linkedin` derives review freshness from saved evidence and profile snapshots. Declined/deferred choices remain respected; review freshness does not authorize public changes.

## Resume/CV standard after history review

Before formatting the first resume or CV, follow [destination and length decisions](document-format.md). The required `resume-format` topic records the initial recommendation and the person's approval, alternative, deferral or decline. Ask this after reconciling the employer/role inventory and target country, so the recommendation reflects actual relevant experience. Save the exact Q&A using `ask` / `save-answer`, then map its preference fact to this topic. A resume's existing length, an employer count, or silence is not authorization. Reuse an already saved equivalent answer rather than ask again.

For another country, language, document type or application context, add a scoped profile topic such as `format-gb-general` instead of overwriting the initial topic. A material history change reopens the recommendation; preserve the earlier decision. If the person defers, keep the topic deferred and any provisional export clearly unapproved. Useful evidence work can continue while the choice remains pending.

## Optional daily search

After target work and region are known, follow [daily routine](routine.md). The required `routine-choice` topic means the choice must be offered and recorded, not that automation is mandatory. Save yes, declined or deferred using the usual evidence/disposition process. Read saved answers before asking again. Confirmed yes starts the separate routine setup; preserve its incomplete state until the actual scheduler and prompt are verified.

## Volunteered information and question pacing

Use `onboarding.py record-statement --workspace W --project P --statement-id MESSAGE_ID --text-file UTF8_FILE --expected-revision R` for one complete unsolicited message. Keep MESSAGE_ID stable for retries. It saves one candidate-report source and one immutable statement without inventing interview questions. Map that source into as many supported facts/topic dimensions as it actually covers, with `answer_ids: []` when no question was asked. A volunteered explicit history or format approval can use `statement_id` instead of `answer_id`; never fill both.

Use `save-answer` only for the real pending question, preserving the full response. When sending the next reply, read the saved pending question and ask only that question; do not add another question in an introduction, example, approval request or final sentence. Save before sending and wait. A candidate may volunteer multiple facts; one-question pacing constrains the AI's questioning, not the candidate's answer.

## Check the actual reply and full input

Before sending each interview reply, including after volunteered facts and when `questions` is empty, run:

```sh
python S/scripts/onboarding.py check-reply --workspace W --project P --reply-file W/scratch/reply.txt --expected-revision N
```

Write the entire proposed reply in that UTF-8 file. If an answer is needed, save one `ask` first, then end the reply with that exact pending question. Keep the preceding progress summary short and declarative. Do not send numbered requests, combine email and phone, or add another employer example or scheduling choice beside it. Send the checked text unchanged and wait. With no pending question, a declarative progress update is valid; an unsaved request is not. The check reads state without changing it, checks its revision and uses English request heuristics; the AI must still judge meaning and must actually call it. It cannot intercept an unsubmitted composer reply.

The compound-question guard also recognizes `or` and semicolons between interrogative clauses. A genuine single alternative such as “Would you prefer remote or hybrid work?” remains valid.

Both `record-statement --text-file` and `save-answer --answer-file` take the **entire received message**, including extra requests, pasted postings, line breaks and punctuation. Verify the returned full text and `captured_characters` against the original before extracting facts. Do not reduce a statement to its personal-fact sentences. A posting can also be saved as an employer source; that extra copy never replaces the complete received message and never establishes that the candidate performed its duties. The helper cannot detect content that the caller omits.


`check-reply` returns `send_verbatim`. It may also return `review_notes` for a weekday/date whose year is missing: check the saved context without guessing the year. Output only `send_verbatim`: the first characters and the entire final reply must match it. A bold, italic or quoted final question is allowed when its wording still exactly matches the pending question. A heading such as “What I saved:” is declarative; common indirect requests and validation prefaces are refused. Either/or preference choices remain bounded English heuristics, not a general language parser or host composer interceptor.

For several resume versions, follow [provenance](provenance.md): preserve each original, map claim lineage and corroboration, and reconcile the combined employer inventory. Either/or checks now recognize preference/shared-verb constructions instead of topic names; judge whether the alternatives concern one decision. The checker can miss paraphrases such as “Feel free to add…” or validation narration and can flag legitimate phrasing. Its language checks are advisory in scope, while the exact pending-question/revision checks remain structural requirements.

## Original-message capture

Binding also creates small `AGENTS.md` and `CLAUDE.md` startup notes in the private project when those files do not already exist. They direct new host sessions to the installed skill and project pointer before asking for missing context. Existing files are never overwritten. If bind reports an existing file without a pointer reminder, read its instructions and add an appropriate reminder while preserving the person's content. If the host does not load project instructions, explicitly summon the skill. Re-running `bind` on the same project adds missing startup notes without resetting the interview.

The opening invocation and request belong to the exact message too. If the original starts “Use job-search. Please correct the last records,” those words must appear in the saved answer/statement. Copy from the original user turn rather than skill arguments, compare its opening and closing sentences, then verify the complete returned text before extracting facts. If the host exposes only a summary, report incomplete capture instead of calling it exact.

## Outgoing drafts

An email drafted for an employer may need questions, such as “Could you let me know which day you intended?” Preserve that request when the candidate asks for clarification. The candidate interview's pacing rule applies to questions addressed to the candidate, not to the recipient of the draft.

Save one outgoing message as a UTF-8 `.txt` or `.md` file inside this workspace, then include its exact contents once in the proposed reply, inside a fenced block labelled `outgoing-draft`:

````text
Draft for the recruiter, not sent:

```outgoing-draft
Hello,
Could you let me know which day you intended for the call?
Thank you.
```
````

Run the final check with the additional workspace-relative file path:

```sh
python S/scripts/onboarding.py check-reply --workspace W --project P --reply-file W/scratch/reply.txt --outgoing-draft-file scratch/recruiter-reply.txt --expected-revision N
```

The checker requires one matching block and exact draft text (ignoring terminal newlines in the source file). It excludes only that block from candidate-request detection. Dates and evidence wording are checked across the entire reply, including the draft. Extra candidate questions outside the block still fail; any saved pending question must appear once at the very end, outside the block. A missing, duplicated, changed or nested-fence draft is refused. Without the flag there is no exemption.

Use this route only for a message the person asked you to draft for someone else. Do not move candidate interview questions into the block to evade pacing. Multiple outgoing messages can be separate saved files; include at most one in each checked reply and link the others. Inspect the meaning and recipient yourself: the checker cannot establish whom a sentence addresses or whether the candidate requested it. Return `send_verbatim` unchanged. No email, message or calendar action is authorized by this check.


## Application questions

Use the same question/answer tools for a particular application's availability, logistics or other missing decision:

```sh
python S/scripts/onboarding.py ask --workspace W --project P --application APP_ID --kind next-stage --question "Are you available for the proposed call?" --expected-revision N
python S/scripts/onboarding.py check-reply --workspace W --project P --reply-file scratch/reply.txt --expected-revision N
```

Use the returned revision for the second command. `--kind` is `next-stage` or `application`; do not combine this route with `--topic`/`--dimension`. The application must exist in these project records. One pending question is allowed across active onboarding and application questions. Resume an existing pending question before asking another. Never silently discard a question to switch applications.

`plan` returns `pending_application_questions` and `application_answers`. `save-answer` accepts the returned question ID and the entire response using the existing arguments. Its saved answer retains `application_id`; map that source into application facts/logistics without treating it as profile coverage. An answer is not automatically consent to send a message or accept an event. On restart, reuse the saved question or answer. Application replies may summarize delivered files in a short list, but must end with exactly the saved question and contain no other requests.

Saving an application answer updates that application's `next_action` to reconcile the answer and set the next step before any new external action. After reviewing the full response, replace that reminder with an accurate action such as “Prepare the candidate's confirmation reply; not sent.” Other applications remain unchanged.

## Correcting a pending question

Before repeating a saved question, verify its logistics against the original invitation. `ask` and `check-reply` refuse explicit English weekday/date mismatches and impossible dates. They return a nonblocking review note when the year is missing. Do not assume a year or repeat an error with a disclaimer above it.

If the one pending question is incorrect, append its correction in the same application/kind or topic/dimension scope:

```sh
python S/scripts/onboarding.py ask --workspace W --project P --application APP_ID --kind next-stage --replace-question OLD_QUESTION_ID --reason "The saved weekday was incorrect; checked the original invitation." --question "Are you available on Friday, September 18, 2026?" --expected-revision N
```

The example date is illustrative; use the actual invitation. Read the returned question ID and revision, then run `check-reply` with the corrected wording. For a profile question, use its original `--topic` and `--dimension` instead of application flags. Both replacement ID and reason are required. The helper appends a new question with `supersedes` and `correction_reason`, preserves the original, and makes only the replacement pending. Repeating the same correction is safe. Save the response against the new ID; the old ID is refused.

This route cannot change the question's scope or replace an answered question. Preserve an already received answer and record any later correction as a separate, complete candidate statement with sourced fact reconciliation. Never edit historical question text or silently reinterpret an answer to different wording.
