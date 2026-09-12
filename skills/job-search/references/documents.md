# Resumes, CVs and letters

The person reviews the content; the AI operates the document tools. Do not tell them to fill a template, run a script, inspect XML or convert files themselves.

When drafting an employment entry or employer-specific cover-letter story, retrieve its `experience_id`, employer, role, period and linked facts/Q&A from onboarding. Keep achievements under the employer and period where they occurred. Check superseded entries and facts; a transferable skill may support a job requirement without relocating the underlying achievement to another employer. Preserve approximate dates and unresolved gaps; never use expected duties as candidate experience.

Use relevant fact IDs to make a requirement-to-evidence map before drafting. Keep candidate-reported evidence qualified internally; do not claim independent verification. Every candidate-facing identity line, summary, skill and achievement must be supported. Check the meaning of each phrase against both the fact and its limits: appointment coordination by phone does not establish front-desk or in-person patient service. A target job's duties are not candidate experience. If the fit map flags missing experience, the summary must preserve that gap too. Preserve a master and make a new filename for each tailored draft. Never rewrite a submitted file.

Before formatting the first resume/CV, follow [LinkedIn](linkedin.md) to resolve the profile URL and inclusion choice from saved evidence or one missing question. Include the confirmed URL in `contact.text` with its fact ID when requested; a none/declined/deferred answer means omit it and continue. An unavailable LinkedIn page does not prevent using a candidate-confirmed URL. Reconcile material profile/resume conflicts before using the affected claims. On later corrections, use saved fact maps to identify drafts needing a new version; never overwrite submitted files.

## Default design

One column, 11 pt body text, standard headings, real Word bullets, no photo/text boxes, contact details in the body, restrained dark blue headings. Use Arial in DOCX. The PDF helper detects installed Unicode TrueType fonts, pairs their matching bold faces (including macOS `Arial Bold.ttf`), and uses character-level fallback for mixed languages. With no matching bold face it uses the same regular family instead of unrelated Helvetica. A missing glyph reports its Unicode code point before publication; supply a suitable `.ttf`/TrueType `.ttc` with `--font` or use an available document runtime. No font covers every writing system, and complex scripts still need actual rendering review. DOCX font substitution also depends on the receiving computer. Role and month/year dates occupy one line, employer/location the following line. Letter or A4 is chosen for the destination. Resume length is usually one or two pages; employer rules and local conventions decide. Academic CVs may need more pages and sections. Do not impose a universal photo or page-count rule across countries.

Bundled `assets/document-example.json` illustrates the layout model with fictional placeholder text. Replace all candidate content and IDs. Do not copy its examples into a real resume. `requirements-documents.txt` supplies the tested Python packages. Prefer an already available document runtime/skill when it produces the required editable DOCX and text-based PDF and permits visual verification. Otherwise create a Python virtual environment **inside W/.runtime** and install only this requirements file there. Never change global packages or another pipeline environment. Ask for runtime/network approval only if the harness requires it.

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

## Quality gate

Open and inspect every exported PDF page, using the harness's available rendering/view tools or a workspace-contained renderer. Check cropping, bullet indentation, headings, dates, page breaks, readability and reading order. Render the DOCX through Word or a supported office converter as well when available; the bundled PDF is a separate rendering of the same content model, not proof of identical DOCX pagination. Check the actual DOCX output if the employer asks for Word format.

Do not mark an application ready until factual review and the relevant final-file layout review are complete. If rendering is unavailable, save drafts and report that single limitation. Prefer finding an available renderer over handing technical chores to the candidate. Record QA evidence, inspected pages, file hashes and remaining limits in an application note. Recheck parsed portal fields after upload. Never claim ATS certification or guaranteed hiring outcomes.
