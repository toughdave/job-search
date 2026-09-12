# Evidence-backed onboarding for the AI

Pacing, questions, file management and saving are defaults. The person can simply say “Use job-search.” Never require the person to repeat operating instructions or edit a checklist.

## Identify this project first

Read the actual selected project path P and the explicitly supplied or project-recorded workspace W. Resolve real absolute paths, not names inferred from the computer account. Use a new private workspace for a new project or independent occupation search. Never scan, adopt or write another project's evidence bank just because it belongs to the same person. If the person explicitly requests reuse, ask which source workspace/files to copy; preserve originals, copy only authorized material into the new W, retain provenance, and assess relevance for the new occupation. Do not copy its completion flags, consent or project binding.

After initializing W (or upgrading an existing schema-v1 workspace), bind it once:

```sh
python S/scripts/onboarding.py bind --workspace W --project P
python S/scripts/onboarding.py plan --workspace W --project P
```

The helper refuses a different project on subsequent use. Store W's exact path and workspace ID in an allowed note in this dedicated project so the next conversation can find it. Do not put the pointer in a public checkout or global instructions. On each turn, use the real current project path for `--project`; do not substitute the saved path merely to bypass a mismatch. A relocation needs an explicit user-directed transfer; do not silently rewrite the binding.

## Resume intake is a real check

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

## Optional daily search

After target work and region are known, follow [daily routine](routine.md). The required `routine-choice` topic means the choice must be offered and recorded, not that automation is mandatory. Save yes, declined or deferred using the usual evidence/disposition process. Read saved answers before asking again. Confirmed yes starts the separate routine setup; preserve its incomplete state until the actual scheduler and prompt are verified.
