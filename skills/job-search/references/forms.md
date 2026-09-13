# Forms, letters and upload copies

Read when entering an application. Reuse scoped standing answers and exact evidence. Complete routine supported fields within the candidate's authorization; keep specific consent, live assessments and final submission separate.

After resume parsing, compare the actual saved form with the evidence. Remove parser-invented jobs while retaining all genuine entries intended for this application. Put work history in reverse chronological order. In plain-text role-description fields, use one `- ` line per relevant achievement, not a prose block or rich-text bullets. Trigger the form's actual save/blur behavior and verify persistence; do not assume typed text was retained.

Preserve date precision. If only month/year is known and the form requires a day, first check instructions and whether a month-only route exists. Otherwise explain a proposed consistent convention, such as the first day of the known month, obtain the candidate's authorization for that approximation, and record it separately from the actual history. Never invent a month for a year-only date, or describe a conventional day as verified. A request for the actual exact date requires clarification.

For a constrained degree selector, use the nearest supported level only when equivalent enough to be truthful; preserve the exact credential in an available text field. Do not upgrade a diploma to a degree. If the language or credential choice is absent, use a truthful Other/text route or report the limitation; do not select a wrong language or credential to complete the form.

Follow [writing](writing.md#cover-letter) for every available letter route, including supporting documents. Verify the actual resume, letter and parsed fields at final review. Failed controls require the one retry and disclosure described there.

## Clean upload files

Keep internal versioned originals. After visually reviewing the exact source file, run `scripts/uploads.py` to create a byte-identical upload copy; opening `--help` is not this operation. This applies when preparing files offline for someone who asks for “ready to upload”, as well as during portal entry. Do not upload or present an internal `resume-v003.pdf` as the ready upload file.

The basename is at most 80 characters, normally `Name - Employer - Role - Resume.pdf`. The full name is preserved, including accents and safe apostrophes. Parentheticals are always stripped from employer and role. If needed, whole employer words are shortened or the employer is omitted **before** touching the role. The role is kept whole or omitted whole if it cannot fit even without the employer; no head-noun guessing or fragments such as “Senior”, “Dental” or “IT” are generated. The helper then restores as much employer text as fits. It budgets for the actual document type and extension, so a letter stem can differ. If even the full name plus document label cannot fit safely, ask for an approved filename name rather than altering identity. Respect stricter portal limits.

Save a JSON visual-review record in the workspace using actual observations:

```json
{
  "file": "applications/APP_ID/resume-v003.pdf",
  "sha256": "ACTUAL_DOCUMENT_HASH",
  "status": "reviewed",
  "unresolved_defects": [],
  "page_count": 1,
  "pages_inspected": [1],
  "renderer": "ACTUAL_RENDERER",
  "inspection": {
    "method": "image_tool",
    "tool": "ACTUAL_IMAGE_VIEWING_TOOL",
    "images": [{"page": 1, "file": "notes/review-images/resume-page-1.png", "sha256": "ACTUAL_IMAGE_HASH"}]
  },
  "reviewed_at": "OBSERVED_OFFSET_TIMESTAMP",
  "findings": "Actual findings and corrections; no unresolved layout defect."
}
```

This record must follow real inspection of every page; producing it does not itself constitute visual review. Use the available image-viewing tool (`view_image` in Codex; `Read` on PNGs in Claude Code) so every page actually enters the model's vision context. Preserve the viewed PNGs in `notes/review-images/` through workspace import and record their hashes. Rendering files, reading extracted text or examining page dimensions does not count. If no image tool is available, stop upload readiness rather than inventing findings. Legacy reviews without image references need actual page inspection and a new versioned review before another upload copy is prepared. For DOCX, inspect PNGs rendered from that exact DOCX through the available office converter. Use an approved current identity fact for the supplied name:

```sh
python S/scripts/uploads.py --workspace W --application APP_ID --source applications/APP_ID/resume-v003.pdf --review notes/review.json --name "Candidate Name" --name-fact-id IDENTITY_FACT_ID --kind resume
```

The helper checks paths, name evidence, page coverage and the current hash, preserves the exact review JSON under `notes/upload-reviews/`, then creates an immutable copy under the application. Add its returned file/hash and returned review reference to the application's upload records; do not substitute the original scratch path. It checks the review record's consistency, not whether the AI actually looked at the pages. Before uploading, verify the copy's hash still matches. A new content hash requires another visual review; a byte-identical rename preserves the reviewed content.

Before saying “ready to upload”, finish this checklist for **each** requested resume/CV and letter: inspect the actual pages; save its JSON review record; execute the helper with that record; verify the returned copy/hash; commit its copy and review references in the application and read them back. Report the actual clean filenames with links. If any step is blocked, name the unfinished step and keep the document labelled draft. Do not claim readiness from export success, a Markdown-only visual note, or a planned helper command. Respect the other format/evidence gates too.

Use the helper's returned `markdown_link` verbatim in the final reply. Never retype or reconstruct its hash directory or filename. Check that each linked target is the returned existing copy. On a later request for the links, rerun the idempotent helper with the current reviewed source if needed, rather than reconstructing paths from memory.

Prepare and review the format actually requested or accepted by the portal. If PDF is sufficient, an additional DOCX export may remain a draft; do not incur another render/upload-copy pass just because it exists. If the candidate requests both formats, finish both. Reuse a valid visual review only when its exact file hash is unchanged; changed files still need inspection. Never reduce checks for a requested upload file merely to save cost.

## Verification messages

If the candidate has authorized the connected mailbox for this workflow, retrieve an email code only for the active application/account and use it transiently. Do not echo, summarize, save or include the code in source archives, notes or logs. Save only that verification succeeded, if observed. If access is missing or the focused search fails, ask the candidate for the needed action. Do not scan unrelated mail or use a code to authorize a different action.
