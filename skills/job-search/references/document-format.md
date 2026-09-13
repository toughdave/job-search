# Destination and resume length

## Recommend, ask once, save and reuse

Review the candidate's employer/role periods, relevant achievements, education, credentials and projects after reconciling the history inventory. Use the target country from the actual search or vacancy, plus the occupation and application context. Do not equate many short jobs with substantial relevant experience, or a single long role with little experience.

- **Short relevant history:** normally recommend one page. Use the available page well through useful, supported detail rather than large gaps or filler.
- **Substantial relevant history:** recommend two pages when one would omit useful evidence or become cramped. Consider breadth, depth, seniority, relevant employers, projects and credentials together.
- **More than two:** propose a specific length only when the context warrants it, such as an academic CV or explicit employer requirements and verified local guidance. Several employers alone do not justify an indefinitely long resume.

State the recommendation and its reason, then ask one short approval question. Examples: “Your two relevant roles should fit well on one page. May I use a one-page resume as your standard for these applications?” or “You have substantial relevant achievements across several roles. May I use a two-page resume as your standard for these applications?” Mention the already established destination/context in the preceding explanation. Do not repeat the whole intake or ask multiple new preferences in the same turn.

Save the exact answer immediately with `onboarding.py save-answer`, then record the sourced preference and format decision below. A recommendation is not approval. A different choice is valid; explain any conflict with employer requirements and agree an application-specific variant. Declined/deferred answers resolve or defer the interview topic without inventing authorization. Keep provisional drafts marked as such. Do not silently fill the `target_pages` field on the candidate's behalf.

## Research the actual destination

Before adopting a standard for a new country/context, inspect the employer's current application instructions first. Then use current official careers/employment guidance, a recognized local university career service or relevant professional body. Save a dated source snapshot and URL in this candidate's workspace. Follow explicit employer requirements; if they conflict with the person's saved standard, explain the difference and obtain the needed variant approval. Never assume one “worldwide CV standard.”

Check terminology (resume versus CV), page size, normal length for the role, language/spelling, section order, reverse chronology versus an employer template, date precision, contact/location conventions, photo/personal-information expectations, file format and any anonymization rule. Do not infer nationality, residence or work authorization. Explain photo/personal-detail choices and obtain the person's decision when relevant; never add sensitive personal information merely because a generic country guide mentions it. Preserve original credential names and do not invent local equivalence.

Starting sources checked on 12 September 2026, not a substitute for checking a new destination:

| Destination/source | Relevant guidance |
| --- | --- |
| [Canada: Job Bank](https://www.jobbank.gc.ca/findajob/resources/write-good-resume?wbdisable=true) | Advises a concise resume of no more than two pages; a photo is not the Canadian norm. Use this as career guidance, not a legal prohibition or a rule for every academic CV. |
| [United States: CareerOneStop](https://cloudfront.careeronestop.org/Veterans/JobSearch/ResumesAndApplications/resume-overview.aspx) | Recommends a simple one- or two-page resume with readable type and clear margins. Research specialized contexts separately. |
| [United Kingdom: National Careers Service](https://nationalcareers.service.gov.uk/careers-advice/cv-sections) | Recommends tailoring a CV, clear headings and bullets, and a clear font of at least 11 pt. Do not turn this source into an unsupported universal page-count rule. |
| [Europe: Europass](https://europass.europa.eu/en/create-europass-cv) | Provides a multilingual CV tool and encourages selecting experience for the application. It is an available format, not proof that every European employer requires it or shares the same conventions. Check the specific country and vacancy. |

For any other destination, use the same research-and-save process rather than copying one of these defaults. If current guidance is unavailable, state that limitation and ask whether to proceed with a clearly provisional, plain format. Do not invent a local convention. Letter and A4 are supported by the bundled exporter; an employer-mandated template, complex script or unsupported page size requires a suitable alternative document tool and its own layout review. Do not label a plain helper output as compliant with a template it cannot render.

## Saved decision schema

Append under `integrations.document_formats = {"version":1,"decisions":[...]}`. Each decision includes:

```json
{
  "id": "ca-general-resume-v1",
  "track_id": "CURRENT_TRACK_ID",
  "country": "CA",
  "kind": "resume",
  "language": "en-CA",
  "context": "general",
  "page_size": "Letter",
  "target_pages": 2,
  "rationale": "Explain the reviewed history, relevant evidence and destination guidance.",
  "recorded_at": "ACTUAL_OFFSET_TIMESTAMP",
  "answer_id": "EXACT_APPROVAL_ANSWER_ID",
  "source_ids": ["CANDIDATE_APPROVAL_SOURCE_ID"],
  "convention_source_ids": ["SAVED_REGIONAL_OR_EMPLOYER_GUIDANCE_SOURCE_ID"],
  "experience_ids": ["CURRENT_REVIEWED_EMPLOYER_PERIOD_IDS"]
}
```

Substitute actual values; these are placeholders, not a completed candidate decision. Country uses a two-letter uppercase code. `kind` is `resume` or `cv`. Context can be `general`, `academic`, or a specific employer/application identifier. `experience_ids` records the active history reviewed when recommending the length (an empty list is valid for no employment). Save the authorization as a preference fact and map it to `resume-format` / `decision`; the format record and interview coverage serve different purposes.

Decision history is append-only. The latest decision applies only within its occupation/country/kind/language/context scope. A new country or language needs its own researched standard and authorization. Reuse an equivalent existing choice on subsequent applications and sessions. New or corrected employer periods trigger a length review; routine daily use and minor wording edits must not repeat the question. To change the standard, save a new exact answer and decision, retaining the old one. Save any employer-specific exception in a distinct context so it does not replace the person's general standard.

For exports, copy the approved ID to `format_decision_id`, country to `target_country`, language to `language`, context to `document_context`, and the agreed `kind` and `page_size`. The helper validates their relationship and measures page count; it cannot judge whether the recorded recommendation or candidate answer was interpreted correctly. Review source meaning, useful page fill, and both PDF and DOCX renderings as described in [documents](documents.md).

## Honest provenance and volunteered approval

A formatting standard can cite `statement_id` instead of `answer_id` when the candidate volunteered explicit approval. Record the complete message with `record-statement`; do not invent an approval question. The helper accepts exactly one of those record IDs.

A URL is not proof that a page was fetched. Do not copy this reference table into a file labeled as newly checked official guidance. Save an actual web-tool response to support current external guidance. If only bundled guidance is available, save the excerpt as `kind: skill_reference` with this reference's provenance, explain that local convention checking is pending, and ask whether the candidate wants a provisional draft. Its export claim map reports `guidance_status: provisional_skill_reference`. Never describe that as verified local compliance. The source-file timestamp records when it was saved, not an invented external fetch.
