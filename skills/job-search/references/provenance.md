# Multiple resumes and evidence provenance

Read when the candidate supplies several resumes, old targeted drafts or a master CV. Use only files they supplied or explicitly authorized in this project's locations. Do not search their computer for unrelated material.

Preserve every original as a separate hashed source, extract readable text, and retain a file-by-file inventory: source ID, filename, date/version if known, candidate description of its origin, and master/current/older/AI-draft status. Ask about authorship only when it affects a material claim. File dates and repeated wording do not prove authorship or truth.

The existing `onboarding.resume.source_ids` can list several originals and text sources. Its `text_source_id` can point to a combined readable inventory that labels every section with its original source ID. Keep per-file extracted text too. Do not mark all files read when one failed; record the unread file and missing work explicitly. Update intake only after the actually readable sources have been reviewed; the remaining file stays pending in the next action.

When two or more original resumes are supplied, create `notes/provenance-ledger-v001.md` **before finishing that intake turn**, even if a conflict is still awaiting an answer. A combined extraction or a warning in a fact's `limits` does not replace this ledger. Record the source inventory and every material retained, derived, conflicting or excluded claim: employer/period, original excerpt/source ID, linked fact IDs if any, possible common ancestor, grade, rationale, and resolution or pending question. Explicitly include each D-graded claim; do not silently discard it or promote it into a candidate fact.

Write the draft in `W/scratch/ledger.md`, then run:

```sh
python S/scripts/provenance.py save --workspace W --draft scratch/ledger.md --expected-revision N
python S/scripts/provenance.py plan --workspace W
```

The helper preserves the previous ledger, imports the next immutable version, registers its `document` source, and advances `onboarding.resume.provenance_ledger` in **one state commit**. It adds the previous-version link automatically. The commit guard refuses a new ledger registration that leaves the old pointer behind. Read back the returned pointer and its actual contents. Keep all excluded-claim history in the new draft; the helper does not grade or verify prose for you.

Unchanged draft text and source inventory reuse the current version. On resume, `onboarding.py plan` includes `provenance.ready`, the current pointer, latest registered ledger and any unregistered files. An older stale pointer remains readable for recovery: use `provenance.py repair --workspace W --expected-revision N` to point to the latest registered version, then reread it. Do not use file modification times to select a ledger. A failed/concurrent commit can leave an unregistered immutable file; inspect it and retry the same draft after rereading the revision, rather than overwriting it or silently adopting different content. A missing ledger is unfinished AI work, not a reason to ask the candidate for already supplied facts.

| Grade | Meaning | Use |
| --- | --- | --- |
| A | Candidate-authored primary account or explicit current answer | Can support candidate-reported facts; it is not independent verification. |
| B | Repeated claim corroborated by an independent source or explicit candidate confirmation | Cite the corroboration. Repetition alone is insufficient. |
| C | Derived phrasing from an earlier source | Reuse wording only after matching its meaning and scope to A/B evidence. |
| D | Unverified enhancement or unresolved conflict | Exclude from employer-facing claims until resolved. |

For example, an unsupported “30% fewer no-shows” claim stays in a D row with its original source and “excluded pending confirmation”, even when no such fact is added to the evidence bank. A later candidate correction gets its own source and resolution; it does not erase the original row.

Resolve materially different claims separately. Denial of using a tool or managing a specific schedule does not also disprove a nearby metric or date. “I did not measure a reduction” leaves the reduction unverified; it does not establish that no reduction occurred. Preserve those distinctions in the ledger and chat summary. Exclusion is based on current evidence, not a permanent ban on a later sourced correction.

Several drafts may descend from one generated ancestor. Treat them as one claim lineage, not several independent witnesses. An attractive metric appearing in three AI drafts stays unverified without its origin. Grades are review metadata, not a replacement for `candidate_reported`, `verified`, `unresolved` or `superseded` status.

Reconcile disagreements in employer names, periods, scope, tools and metrics against original evidence, then ask one focused question if needed. Save the actual correction and supersede affected facts; do not silently choose the most impressive draft. Keep historical phrases as leads without manufacturing interviews that never happened. Reconcile the employer inventory across all readable sources before requesting the candidate's completeness confirmation.

## Updating current claim rows

Rebuild the current ledger as one claim per row: original excerpt/source, grade, current status, resolution source and rationale. Keep previous versions by the helper's link. Do not copy an old grouped resolution and add a contradictory sentence beneath it. A date conflict, denied tool, denied duty and unmeasured metric require separate rows.

New ledger saves and registrations refuse permanent-exclusion wording and a row that mixes denied/false with unverified/unmeasured statuses. Split such a row into its actual claims. Historical ledgers remain readable. These checks protect the observed bookkeeping/wording boundaries; they do not decide whether a candidate's account is true.
