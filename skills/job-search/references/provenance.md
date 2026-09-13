# Multiple resumes and evidence provenance

Read when the candidate supplies several resumes, old targeted drafts or a master CV. Use only files they supplied or explicitly authorized in this project's locations. Do not search their computer for unrelated material.

Preserve every original as a separate hashed source, extract readable text, and retain a file-by-file inventory: source ID, filename, date/version if known, candidate description of its origin, and master/current/older/AI-draft status. Ask about authorship only when it affects a material claim. File dates and repeated wording do not prove authorship or truth.

The existing `onboarding.resume.source_ids` can list several originals and text sources. Its `text_source_id` can point to a combined readable inventory that labels every section with its original source ID. Keep per-file extracted text too. Do not mark all files read when one failed; record the unread file and missing work explicitly. Update intake only after the actually readable sources have been reviewed; the remaining file stays pending in the next action.

Maintain a private provenance ledger in `notes/` linking each candidate claim, its employer/period, original excerpt/source, possible common ancestor, grade and resolution:

| Grade | Meaning | Use |
| --- | --- | --- |
| A | Candidate-authored primary account or explicit current answer | Can support candidate-reported facts; it is not independent verification. |
| B | Repeated claim corroborated by an independent source or explicit candidate confirmation | Cite the corroboration. Repetition alone is insufficient. |
| C | Derived phrasing from an earlier source | Reuse wording only after matching its meaning and scope to A/B evidence. |
| D | Unverified enhancement or unresolved conflict | Exclude from employer-facing claims until resolved. |

Several drafts may descend from one generated ancestor. Treat them as one claim lineage, not several independent witnesses. An attractive metric appearing in three AI drafts stays unverified without its origin. Grades are review metadata, not a replacement for `candidate_reported`, `verified`, `unresolved` or `superseded` status.

Reconcile disagreements in employer names, periods, scope, tools and metrics against original evidence, then ask one focused question if needed. Save the actual correction and supersede affected facts; do not silently choose the most impressive draft. Keep historical phrases as leads without manufacturing interviews that never happened. Reconcile the employer inventory across all readable sources before requesting the candidate's completeness confirmation.
