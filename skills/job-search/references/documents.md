# Resumes, CVs and letters

The person reviews the content; the AI operates the document tools. Do not tell them to fill a template, run a script, inspect XML or convert files themselves.

When drafting an employment entry or employer-specific cover-letter story, retrieve its `experience_id`, employer, role, period and linked facts/Q&A from onboarding. Keep achievements under the employer and period where they occurred. Check superseded entries and facts; a transferable skill may support a job requirement without relocating the underlying achievement to another employer. Preserve approximate dates and unresolved gaps; never use expected duties as candidate experience.

Use relevant fact IDs to make a requirement-to-evidence map before drafting. Keep candidate-reported evidence qualified internally; do not claim independent verification. Every candidate-facing identity line, summary, skill and achievement must be supported. Check the meaning of each phrase against both the fact and its limits: appointment coordination by phone does not establish front-desk or in-person patient service. A target job's duties are not candidate experience. If the fit map flags missing experience, the summary must preserve that gap too. Preserve a master and make a new filename for each tailored draft. Never rewrite a submitted file.

Before formatting the first resume/CV, follow [LinkedIn](linkedin.md) to resolve the profile URL and inclusion choice from saved evidence or one missing question. Include the confirmed URL in `contact.text` with its fact ID when requested; a none/declined/deferred answer means omit it and continue. An unavailable LinkedIn page does not prevent using a candidate-confirmed URL. Reconcile material profile/resume conflicts before using the affected claims. On later corrections, use saved fact maps to identify drafts needing a new version; never overwrite submitted files.

## Default design

First follow [destination and length decisions](document-format.md). Use the latest candidate-approved standard for the actual destination, occupation, language and document context; do not infer it from their nationality or computer locale. A country-specific employer instruction outranks a generic template and may require a separately approved application variant.

One column, 11 pt body text, standard headings, real Word bullets, no photo/text boxes, contact details in the body, restrained dark blue headings. Use Arial in DOCX. The PDF helper detects installed Unicode TrueType fonts, pairs their matching bold faces (including macOS `Arial Bold.ttf`), and uses character-level fallback for mixed languages. With no matching bold face it uses the same regular family instead of unrelated Helvetica. A missing glyph reports its Unicode code point before publication; supply a suitable `.ttf`/TrueType `.ttc` with `--font` or use an available document runtime. No font covers every writing system, and complex scripts still need actual rendering review. DOCX font substitution also depends on the receiving computer. Role and month/year dates occupy one line, employer/location the following line. Letter or A4 is chosen for the destination. Resume length is usually one or two pages; employer rules and local conventions decide. Academic CVs may need more pages and sections. Do not impose a universal photo or page-count rule across countries.

Bundled `assets/document-example.json` illustrates the layout model with fictional placeholder text. Replace all candidate content and IDs. Do not copy its examples into a real resume. `requirements-documents.txt` supplies the tested Python packages. Prefer an already available document runtime/skill when it produces the required editable DOCX and text-based PDF and permits visual verification. Otherwise follow [runtime setup](runtime.md) and run `scripts/setup_runtime.py --workspace W` to install and verify the private document environment. Never change global packages or another pipeline environment. Ask for runtime/network approval only if the harness requires it.

## Export

Create a model JSON in W/scratch using this structure:

```json
{
  "kind": "resume",
  "page_size": "Letter",
  "name": {"text": "Candidate name", "fact_ids": ["identity-1"]},
  "contact": {"text": "City | candidate@example.com", "fact_ids": ["contact-1"]},
  "sections": [
    {"heading": "Experience", "entries": [
      {"title": {"text": "Role | Jan 2023 - Dec 2025", "fact_ids": ["job-1"]},
       "subtitle": {"text": "Employer | City", "fact_ids": ["job-1"]},
       "bullets": [{"text": "A supported achievement.", "fact_ids": ["achievement-1"]}]}
    ]}
  ]
}
```

Every text item requires one or more current supported fact IDs. Headings are formatting labels. Sections can instead contain `paragraphs` or `bullets`, useful for summaries, skills, education, academic CV sections and letters. `kind` accepts resume, cv, or cover_letter. For a letter, employer-address/salutation text can cite an `other` fact sourced to the posting. Keep the original full job history in state even when a tailored draft selects fewer entries.

```sh
python S/scripts/documents.py --workspace W --model W/scratch/resume.json --stem applications/example-role/resume-v001
```

The helper validates state and evidence IDs, exports DOCX/PDF, saves the source model and claim map, and returns their hashes. It refuses existing filenames and unsupported facts. It checks PDF text extraction, but **cannot prove semantic truth or visual layout**. You must review that yourself. Generated files initially remain drafts even if export succeeds.

For a saved resume/CV format decision, add `format_decision_id`, `target_country`, `language` and `document_context` to the model using the matching values in `integrations.document_formats.decisions`. The exporter rejects an old decision superseded within the same scope, wrong destination/paper/language/occupation, or changed employer inventory. It records the approved and actual page counts, estimated bottom gaps and underfilled pages in `.claims.json` and the CLI result. An old workspace without a decision can still export a provisional draft, labeled `format_review:not_configured`; it is not authorization to adopt that length.

Optional `layout` overrides apply to both outputs: `body_font_pt` (10.5-12), `line_spacing` (1.05-1.35), `paragraph_gap_pt` (3-8), `entry_gap_pt` (5-12), `vertical_margin_in` and `horizontal_margin_in` (0.55-1). Defaults are 11 pt, 1.2 line spacing, 5/8 pt paragraph/entry gaps, and 0.65/0.7 inch margins. Choose values consistent with the destination guidance; bounds are readability limits, not proof of regional compliance. The separate engines may paginate differently.

## Quality gate

Before export, run `documents.py --workspace W --model MODEL --review-only`. For a tailored model, include `posting_source_ids` referring to saved readable employer posting sources. The review compares each text item's vocabulary with its linked fact claims and highlights terms found only in the posting. Inspect the linked claims, their limits and original sources: synonyms can be flagged, and matching words do not prove truth. Do not add appointment confirmation, a fast-paced environment or other duties/context merely because the vacancy uses that wording. Correct unsupported wording or ask for a missing fact when it materially helps. The same report is included in the export's claim map; drafts never become semantically approved automatically.

Open and inspect every exported PDF page, using the harness's available rendering/view tools or a workspace-contained renderer. Check cropping, bullet indentation, headings, dates, page breaks, readability and reading order. Render the DOCX through Word or a supported office converter as well when available; the bundled PDF is a separate rendering of the same content model, not proof of identical DOCX pagination. Check the actual DOCX output if the employer asks for Word format.

Rendering is preparation, not inspection. Actually call the image-viewing tool on each page PNG (`view_image` in Codex or `Read` in Claude Code when available). Do not infer visual findings from extraction, geometry or the document model. Save the viewed image paths/hashes and actual viewer in the [upload review record](forms.md#clean-upload-files). Without an available vision tool, keep upload readiness blocked.

This is a **pre-upload gate**, including during scheduled searches. Inspect the actual format you will attach before opening the upload action. Run `setup_runtime.py --detect-renderers` before concluding that a DOCX converter is missing; use the returned absolute path. Render the actual DOCX to a separate PDF in private scratch space, with an isolated LibreOffice profile if needed, and visually inspect every resulting page. For PDF uploads, inspect that exact PDF. Save a review note with the upload file's SHA-256, renderer, page count, inspected page numbers, findings and resolved corrections. Recheck the hash immediately before upload; any later content/layout change invalidates the review. If no available tool can visually inspect the required format, keep it as a draft and pause the upload. Text extraction, successful export, or merely creating preview images is insufficient: the AI must actually view them.

Do not mark an application ready until factual review and the relevant final-file layout review are complete. If rendering is unavailable, save drafts and report that single limitation. Prefer finding an available renderer over handing technical chores to the candidate. Record QA evidence, inspected pages, file hashes and remaining limits in an application note. Recheck parsed portal fields after upload. Never claim ATS certification or guaranteed hiring outcomes.

Check `pagination.matches_approved_length` and every `underfilled_pages` flag. The 80% estimated body-fill threshold is a prompt to inspect, not an ATS rule or permission to pad content. For one page, bring forward relevant supported accomplishments, tools, education or projects before increasing spacing. For two pages, redistribute sections and employer detail so neither page has an avoidable large lower gap; remove manual breaks and excessive keep-together groups before altering margins. Keep headings with their following content and avoid a few lines spilling onto a new page. Tighten duplicated wording and tune spacing within the readable range when over budget. If useful evidence cannot support the chosen length, explain this and ask one question to change the standard or retain a clearly explained exception. Never stretch text, add irrelevant duties, fabricate metrics, or silently switch the approved page count. Normal margins and breathing room remain necessary.

Font loading stops once the document's glyphs are covered. ReportLab's bundled Vera family supplies a basic Latin fallback if system fonts are unavailable; unsupported glyphs still fail clearly. Arabic/Hebrew and other right-to-left text requires a shaping-capable alternative exporter; the helper reports that limitation before publishing files.

When wording review flags a new duty or responsibility, remove it or cite the original evidence before retaining it. “Served customers and processed payments” does not by itself establish retail sales responsibility; preserve customer service/payment processing wording unless actual sales duties are confirmed. Do not treat this as a harmless stylistic substitution.

Follow [writing craft](writing.md) for bullet selection, tone and cover-letter completion, and [forms](forms.md#clean-upload-files) for byte-identical clean upload filenames after actual-file visual review.
