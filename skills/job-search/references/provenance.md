# Multiple resumes and evidence provenance

Read when the candidate supplies several resumes, old targeted drafts or a master CV. Use only files they supplied or explicitly authorized in this project's locations. Do not search their computer for unrelated material.

Preserve every original as a separate hashed source, extract readable text, and retain a file-by-file inventory: source ID, filename, date/version if known, candidate description of its origin, and master/current/older/AI-draft status. Ask about authorship only when it affects a material claim. File dates and repeated wording do not prove authorship or truth.

The existing `onboarding.resume.source_ids` can list several originals and text sources. Its `text_source_id` can point to a combined readable inventory that labels every section with its original source ID. Keep per-file extracted text too. Do not mark all files read when one failed; record the unread file and missing work explicitly. Update intake only after the actually readable sources have been reviewed; the remaining file stays pending in the next action.

When two or more original resumes are supplied, create `notes/provenance-ledger-v001.md` **before finishing that intake turn**, even if a conflict is still awaiting an answer. A combined extraction or a warning in a fact's `limits` does not replace this ledger. Record the source inventory and every material retained, derived, conflicting or excluded claim: employer/period, original excerpt/source ID, linked fact IDs if any, possible common ancestor, grade, rationale, and resolution or pending question. Explicitly include each D-graded claim; do not silently discard it or promote it into a candidate fact.

Write the ledger through workspace `import-file`, register it as a `document` source, and save its returned file/hash/source ID in `onboarding.resume.provenance_ledger`. Read it back before calling reconciliation complete. On later corrections, save v002 (and so on), link the preceding ledger, preserve excluded-claim history, and update the pointer. Reuse the current ledger when the source inventory and resolutions are unchanged. A missing ledger is unfinished AI work, not a reason to ask the candidate again for facts already supplied.

| Grade | Meaning | Use |
| --- | --- | --- |
| A | Candidate-authored primary account or explicit current answer | Can support candidate-reported facts; it is not independent verification. |
| B | Repeated claim corroborated by an independent source or explicit candidate confirmation | Cite the corroboration. Repetition alone is insufficient. |
| C | Derived phrasing from an earlier source | Reuse wording only after matching its meaning and scope to A/B evidence. |
| D | Unverified enhancement or unresolved conflict | Exclude from employer-facing claims until resolved. |

For example, an unsupported “30% fewer no-shows” claim stays in a D row with its original source and “excluded pending confirmation”, even when no such fact is added to the evidence bank. A later candidate correction gets its own source and resolution; it does not erase the original row.

Several drafts may descend from one generated ancestor. Treat them as one claim lineage, not several independent witnesses. An attractive metric appearing in three AI drafts stays unverified without its origin. Grades are review metadata, not a replacement for `candidate_reported`, `verified`, `unresolved` or `superseded` status.

Reconcile disagreements in employer names, periods, scope, tools and metrics against original evidence, then ask one focused question if needed. Save the actual correction and supersede affected facts; do not silently choose the most impressive draft. Keep historical phrases as leads without manufacturing interviews that never happened. Reconcile the employer inventory across all readable sources before requesting the candidate's completeness confirmation.
