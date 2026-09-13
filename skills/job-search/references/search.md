# Search, prepare and record

Use only the current candidate's state. Start with urgent employer requests and active backlog (`qualified`, `preparing`, `ready`, `blocked`, `submitted_unverified`), then fresh discovery. Recheck deadlines and unresolved posting access. Do not duplicate submitted applications while investigating uncertain status.

Agree a manageable first scope from target roles and region. Use complementary source families: general board, relevant local/specialist source, direct employer sites. Broaden title/duty phrases only where evidence supports them. Do not present a fixed source count as exhaustive coverage.

For each source checked, record query, checked time, URLs, number inspected, and `complete`, `partial`, `blocked` or `not_configured`. Save the actual posting, distinguishing full vs partial content. If browsing is unavailable, ask for a posting only when it is the next blocker; do not pretend an offline exercise was live discovery.

Match employer plus requisition first; then canonical URL with tracking parameters removed. Different requisition IDs remain separate even with the same URL. Similar employer/title/location is a possible duplicate needing inspection. The helper rejects strong duplicate keys; do not evade that guard by changing IDs.

Check mandatory/equivalent/preferred wording, work location, central duties, credentials and deadlines against facts. Ask about unknown experience rather than infer absence. Use the current official authority for regulated requirements. Rank truthful fit before pay or recency, with urgency as a tie-breaker. No invented fit percentages or unsupported claims.

For each advancing application, create a saved posting, requirement-to-fact map, draft resume/CV, optional letter, exact screening Q&A, and a clear next action. Keep each application and draft version separate. Preserve master material. Review all parsed portal fields and attachments after upload.

Before any document upload, complete the [visual quality gate](documents.md#quality-gate) for that exact file and verify its hash still matches the review. Correct and re-inspect changed versions. If viewing/rendering is unavailable, pause the upload while continuing other authorized preparation. Checking parsed fields after upload does not replace the pre-upload visual review.

## Submission and recovery

Before submitting, show employer, role, selected document versions and unresolved items. Record the specific candidate authorization. Save a `pending_actions` entry before the external action, with application ID and intended action. If the session is interrupted, inspect the employer portal/receipt before retrying. Close the pending action only after the result is known.

Stage and outcome are independent:

- `stage`: discovered, qualified, preparing, ready, submitted_unverified, submitted, blocked, skipped, withdrawn.
- `outcome`: none, awaiting, positive, action, offer, declined.
- `posting_status`: unknown, open, closed, expired, cancelled.

Confirmed submission requires an `employer` source, observed time and an immutable saved copy/reference for each submitted document. Unverified candidate reports remain `submitted_unverified`, without a confirmed date. Later employer outcomes require their own employer source. A closed posting is not a rejection. Preserve confirmation and submitted files when an outcome changes.

## Email and calendar

Only use explicitly selected/authorized accounts. Read full relevant threads, match to application IDs, preserve ambiguous matches, and record lookback/query/pagination coverage. Do not confuse unread-only with all new replies. Candidate-pasted messages can be saved as candidate reports unless independently verified. Record deadlines/timezones and concrete next actions. Outbound messages, event creation or changes and reference sharing require the relevant candidate authorization; generating a draft is separate.

## End a run

Record `scope`, `checks`, application IDs advanced, start/end times, `complete`/`incomplete`, and one next action. `complete` means every required check in that scope succeeded, not that the market was exhausted or the candidate was hired. Unconfigured optional email is not failure unless email was agreed as required. Persist unfinished actions so the next conversation continues rather than starts over.

For recurring searches, use [daily routine](routine.md) and the generated private prompt. Claim the daily run before work. Completion must satisfy the run's saved `required_checks`, using those exact check source keys: backlog, deduplication, preparation, discovery:<source-id>, and mail when configured as required. Record a supported no-fit result under preparation when no draft is justified.

## Partial matches and precise wording

Use `assessment: partial` when evidence covers only part of a requirement; cite the supported facts and put the missing part in `remaining`. Phone scheduling alone does not establish greeting patients, reception/front-desk work, provider calendar ownership or use of a named EMR. Describe the specific verified duty, not the broader job-ad label. In a combined requirement, split supported and missing components or preserve them explicitly in the partial assessment. A plausible transferable skill is not proof of having performed that duty.


Before reporting a fit assessment or using it for preparation, run `python S/scripts/documents.py --workspace W --review-fit APPLICATION_ID` against the saved application. Review the flagged vocabulary in each `supported` requirement against its actual fact claims and limits. A requirement to “book and confirm appointments” is only partial when the evidence supports booking but says nothing about confirmation. Save the missing component in `remaining` or split the requirement. This read-only English vocabulary check does not prove semantic support or automatically change the assessment; verify all combined duties even when there are no flags.

Keep negative claims scoped too: “I have not used Dentrix” does not establish no experience with other EMRs or scheduling software. Review explanations and `remaining` notes against the exact source, including gap assessments; leave unmentioned tools unknown. The fit helper also compares all linked fact claims and limits, including gap evidence, with readable original source text in `fact_source_review`. Review its flags and any `manual_sources` before relying on the map; correct overbroad facts through a sourced, append-only correction. It cannot certify semantic truth or explanations, and words in a quoted job posting are not candidate experience.

The result also includes `explanation_review` for saved `remaining` notes, across supported/partial/gap/unknown assessments. Reconcile those notes whenever a linked fact changes: changing a fact ID alone does not correct stale prose. Review explanations with no linked evidence manually; do not turn missing evidence into a claim of no experience.
