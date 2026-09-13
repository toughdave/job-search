# Forms, letters and upload copies

Read when entering an application. Reuse scoped standing answers and exact evidence. Complete routine supported fields within the candidate's authorization; keep specific consent, live assessments and final submission separate.

After resume parsing, compare the actual saved form with the evidence. Remove parser-invented jobs while retaining all genuine entries intended for this application. Put work history in reverse chronological order. In plain-text role-description fields, use one `- ` line per relevant achievement, not a prose block or rich-text bullets. Trigger the form's actual save/blur behavior and verify persistence; do not assume typed text was retained.

Preserve date precision. If only month/year is known and the form requires a day, first check instructions and whether a month-only route exists. Otherwise explain a proposed consistent convention, such as the first day of the known month, obtain the candidate's authorization for that approximation, and record it separately from the actual history. Never invent a month for a year-only date, or describe a conventional day as verified. A request for the actual exact date requires clarification.

For a constrained degree selector, use the nearest supported level only when equivalent enough to be truthful; preserve the exact credential in an available text field. Do not upgrade a diploma to a degree. If the language or credential choice is absent, use a truthful Other/text route or report the limitation; do not select a wrong language or credential to complete the form.

Follow [writing](writing.md#cover-letter) for every available letter route, including supporting documents. Verify the actual resume, letter and parsed fields at final review. Failed controls require the one retry and disclosure described there.

## Clean upload files

Keep internal versioned originals. After visually reviewing the exact source file, create a byte-identical upload copy with `scripts/uploads.py`; do not upload an internal `resume-v003.pdf`. The basename is at most 80 characters, normally `Name - Employer - Role - Resume.pdf` or a matching `Cover Letter` name, with no internal version/final label. The helper removes unsafe punctuation and shortens the common stem deterministically. Respect any stricter portal limit.

Save a JSON visual-review record in the workspace using actual observations:

```json
{"file":"applications/APP_ID/resume-v003.pdf","sha256":"ACTUAL_HASH","status":"reviewed","unresolved_defects":[],"page_count":2,"pages_inspected":[1,2],"renderer":"ACTUAL_VIEWER","reviewed_at":"OBSERVED_OFFSET_TIMESTAMP","findings":"Actual findings and corrections; no unresolved layout defect."}
```

This record must follow real inspection of every page; producing it does not itself constitute visual review. For DOCX, the record concerns that exact DOCX rendered through the available office converter. Use an approved current identity fact for the supplied name:

```sh
python S/scripts/uploads.py --workspace W --application APP_ID --source applications/APP_ID/resume-v003.pdf --review notes/review.json --name "Candidate Name" --name-fact-id IDENTITY_FACT_ID --kind resume
```

The helper checks paths, name evidence, page coverage and the current hash, then creates an immutable copy under the application. Add its returned file/hash and review reference to the application's upload records. It checks the review record's consistency, not whether the AI actually looked at the pages. Before uploading, verify the copy's hash still matches. A new content hash requires another visual review; a byte-identical rename preserves the reviewed content.

## Verification messages

If the candidate has authorized the connected mailbox for this workflow, retrieve an email code only for the active application/account and use it transiently. Do not echo, summarize, save or include the code in source archives, notes or logs. Save only that verification succeeded, if observed. If access is missing or the focused search fails, ask the candidate for the needed action. Do not scan unrelated mail or use a code to authorize a different action.
