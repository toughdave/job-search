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

Choose a small initial set of **occupation-specific examples**, normally two complementary stories, and add required `example` topics for that track. Adapt their titles and questions to the actual role: handling a difficult customer, diagnosing an incident, coordinating competing deadlines, improving a process, completing a design/project, or another relevant responsibility. Do not ask a developer's interview of a nurse or administrator. Use work, volunteer, academic or personal examples when appropriate, and preserve that category.

For each story use dimensions `context`, `personal_action`, `tools`, `result`. Start with one natural question, such as “Tell me about one occasion when you resolved a difficult customer issue.” Then ask only missing follow-ups, one per turn: what the person personally did, which tools/methods they used, what changed, and how the result is known. Keep collaborators' work separate. Results may be qualitative or a lesson; never pressure the person to invent a metric. Ask for a second complementary example once the first is usable. Add topics later only for a real gap in the target occupation or a specific posting.

This is a finite initial interview, not a repeated daily questionnaire. Save progress after every answer. Start useful drafts while deeper topics remain pending; do not mark onboarding complete until required topics are answered or have explicit dispositions. A candidate may decline, defer, report no example, or explain why something is not applicable. Save that decision and its limitation, then continue useful work. Deferred topics stay incomplete but are not asked repeatedly until the person asks to resume or the topic becomes necessary for a specific task.

## The checkbox is a view, not proof

Run `plan` every time this workflow resumes. It computes status from current evidence and lists missing dimensions, saved unanswered questions and answers awaiting evidence mapping. It ignores manually supplied `checked` flags. The derived checklist appears in `notes/STATUS.md`.

Before asking about any missing dimension, read the existing facts AND exact interview answers in W. Search semantically: an answer about “restoring service” may satisfy “incident resolution” even with different words. A status of unanswered means coverage has not been recorded, not necessarily that the person never answered.

If a saved answer already resolves it, map that evidence and commit, then recompute; **do not ask again**. If a saved answer is partial, ask only for the missing detail. If a question was saved but the answer was not received, resume that question. If the answer is in the transcript but the commit was interrupted, persist it first. Unknown or superseded facts cannot complete a dimension. On a correction, supersede the old fact, add its replacement, and map only what the new fact supports. Preserve prior questions and evidence.

## State records

Use the existing workspace `commit` command to save all changes with the revision read from disk. `onboarding` is an optional version-1 extension, bound to workspace ID and canonical project path; old workspace facts are preserved. The helper derives completion but the AI must judge whether the linked claims actually answer the question.

- `tracks`: `{id, occupation, source_ids}`. Keep tracks; switch `active_track` instead of renaming an old occupation.
- `topics`: `{id, track_id, kind, title, required, dimensions}`. `track_id:null` is shared only within this private workspace. Each new occupation gets its own example topics. Reuse relevant local facts through new explicit mappings, not copied completion flags.
- `questions`: `{id, topic_id, dimension, question, asked_at}`. Save the exact question **before** presenting it. Do not create a new duplicate while one is pending.
- Existing `interviews` can add `onboarding_question_id`. Save the exact received answer immediately. `plan` reports these answers even if evidence mapping was interrupted.
- `evidence`: `{id, topic_id, dimension, fact_ids, source_ids, answer_ids, rationale}`. Map one answered dimension per record; explain its relevance. Sources must support the facts. Map resume-established facts without fabricating a Q&A entry.
- `dispositions`: `{id, topic_id, status, source_ids, reason}` with `declined`, `deferred`, `not_applicable`, `no_example`, or `reopen`. A candidate decision is required. These resolve or defer a question, not prove professional experience. The latest disposition wins. `reopen` restores evidence-based evaluation.

Tracks, topics, questions, evidence mappings and dispositions are append-only. The saved fact/answer is authoritative; a missing or false checkbox must not erase it. `ready_to_close_interview` is an interview flag, not an application-ready or hiring-readiness judgment.

## Optional LinkedIn review

Offer once: “Would you like me to review your LinkedIn profile for improvements?” Save yes/no/later. A declined review resolves the choice; a deferral should not prompt again every visit. If yes, ask for their profile URL or pasted/exported profile content if absent. Verify it is the profile they supplied. Review only accessible authorized content, compare it with evidence, and draft specific headline, About, experience or skills improvements. Mark inaccessible sections as unreviewed. Do not claim to have inspected a profile based on its URL alone, infer qualifications from AI-written text, or publish profile changes without separate explicit authorization. Keep review outputs in this workspace. Consent in one project does not grant access in another.

An accepted offer is not a completed review. Save the requested review and missing profile/access in `session.next_action` until it is performed or explicitly deferred. Add a separate optional review topic if tracking multiple steps; keep the actual review evidence/output distinct from the yes/no choice.
