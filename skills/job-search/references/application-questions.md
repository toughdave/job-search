# Reusable application questions

Use this after the basic resume/history interview, or when an actual form exposes a missing answer. These are question patterns, not prefilled candidate answers. Keep everything in this candidate's private workspace. Never import the guide author's answers, identity, consent, technical experience or search preferences.

## Choose the next useful question

Read the resume, profile facts, exact interviews and saved preferences first. Offer once: “Would you like to save common application answers now, or answer them when a form needs them?” Save the choice as `application_questions_timing`. If the person chooses later, continue useful work and ask when a real field makes it relevant. Do not repeat this offer on every visit.

Prioritize one unresolved question at a time:

- An eligibility or location constraint that could rule out the current search.
- A broadly reusable answer likely to occur across the person's target applications.
- A required field in an actual application that existing evidence does not answer.
- Optional material only if the person wants it or it improves the relevant application.

Do not run the entire catalog as a mandatory interview. Add selected questions as onboarding profile topics, using one decision/dimension per question and a clear country, employer, job or tool in the title where needed. Reuse existing contact, relocation, education and credential topics. Save the pending question, exact answer, source and interpretation through the normal onboarding process. No saved answer means unknown, not No.

## Useful questions during setup

Ask only missing items relevant to the agreed search. Text in braces is a placeholder the AI fills from the actual search, not something the candidate must edit.

| Pattern / suggested key | One question to ask | What to preserve or ask next |
| --- | --- | --- |
| `work_authorization` | Are you legally authorized to work in {country}? | Country and any stated restrictions. Do not request immigration document numbers. |
| `sponsorship_now` | Would you need employer sponsorship to work in {country} now? | Country and current situation. Ask future sponsorship separately if relevant. |
| `sponsorship_future` | Would you need employer sponsorship in {country} in the future? | Do not assume today's answer covers the future. |
| `work_arrangement` | What mix of on-site, hybrid or remote work suits your search? | Location, commute limits and any constraints; a particular office schedule still needs a match. |
| `relocation` | Would you be willing to relocate for a suitable role? | Ask destination limits separately if needed. Do not infer residence or work authorization. |
| `notice_period` | How much notice would you need before starting a new job? | Duration, conditions and confirmation date. |
| `earliest_start` | What is the earliest date you could start? | Actual date and conditions; refresh when a stored date is in the past or circumstances change. |
| `compensation` | What compensation range would you target for this kind of role? | Ask missing currency, hourly/annual basis, base/total compensation and role/location scope separately. Distinguish target from minimum. |
| `salary_delegation` | Would you like to choose each salary answer, or allow me to suggest one within your agreed range? | Exact authority and range. Permission to suggest is not permission to submit or accept an offer. |
| `employment_type` | Which types of work would you consider: permanent, contract, part-time or another arrangement? | Candidate's selections, location/role scope and limits. |
| `travel` | Would you consider a role that involves travel? | Ask maximum frequency or locations only when needed. |
| `schedule` | Are there working hours or days that you need to avoid? | Ask about a particular shift, weekend or on-call requirement only when relevant. |
| `languages` | Which languages would you like listed, and how would you describe your proficiency in each? | Separate spoken/written proficiency where a form requires it; no unsupported “fluent” label. |

Name, email, phone, city/country, education, certifications and optional portfolio links use the profile checklist in [onboarding](onboarding.md). For a form requesting a full address, collect the missing address fields in that private session; do not automatically put them on a resume.

## Questions tied to a particular employer or posting

These should normally wait for a real opportunity. Store answers with the named employer/job and exact wording; a No for one company cannot become a universal No.

- **Previous employment, applications or interviews:** “Have you previously worked for {employer or its specified affiliates}?” Ask previous applications/interviews separately when that is what the form asks. Preserve affiliate scope and date range.
- **Referral or relatives:** “Were you referred by a current employee of {employer}?” Ask relatives/conflicts only if the form requires them. Never invent a referrer or obtain another person's private details by default.
- **Discovery source:** use the actual posting/discovery record to answer “How did you hear about this opportunity?” Do not carry LinkedIn, referral or another source from an unrelated job.
- **Office attendance:** “Could you work at {actual location} {required days/hours}?” Match the whole requirement, not just a generic willingness to relocate.
- **Licence, transport or travel:** ask about the specific required licence class and current validity, vehicle access, transport or travel requirement. Ability to commute does not prove vehicle ownership.
- **Minimum age or qualification:** ask the stated yes/no threshold where relevant; do not gather a birth date unnecessarily. Match the exact completed credential requirement, not merely attendance at an institution.
- **Restrictions, clearance or checks:** ask the actual question if needed. Holding a clearance, possible eligibility, willingness to undergo a check and consent to a particular check are separate. Never infer one from another or request government ID copies during generic setup.
- **Reason for leaving / motivation:** use the correct employer-period for a departure explanation; tailor “Why this role/company?” from the real posting and candidate priorities. Save the final wording for that application rather than treating it as a universal answer.
- **Assessments or supporting documents:** completion requires actual evidence. Do not mark a survey/test completed because a form requests it. Live assessments stay with the candidate under the harness rules.

## Technical and scenario questions

For “How many years of {tool or duty} experience?”, first retrieve the relevant employer-period entries and facts. Confirm scope: user/support work, configuration, administration, ownership, paid work, study or personal projects can mean different things. Ask a focused follow-up if the requested type is not established. Do not copy total career years into every tool field, double-count overlapping periods, or convert familiarity into administrator experience. Keep the candidate's confirmed amount, unit, date basis and limits; show an uncertain calculated estimate for confirmation before using it.

For grouped platform questions, preserve the actual AND/OR/grouped wording. A confirmed broad familiarity answer does not establish every named protocol, years, certification or employer attribution. Reuse only for a materially equivalent question. For unknown tools, search saved evidence before asking; absence from the bank is not proof of no experience. Once the person explicitly confirms no experience, save that answer and stop asking until new evidence changes it.

For “Describe a project/problem you handled”, choose the most relevant employer-specific story and ask only missing context, personal actions, tools or results. Keep the employer, role, dates and source attached. Do not reuse an answer about one system as proof of a different system. A technical definition can be researched separately; it does not prove the candidate used that technology.

## Optional choices and consent wording

Do not require demographic, disability, accommodation or other sensitive disclosures to finish onboarding. At a relevant form, offer the candidate the actual voluntary options, including decline/prefer-not-to-answer where available. Save a reusable disclosure preference only if the person chooses to, with its jurisdiction and wording limits. Do not infer sensitive traits from their name, photo, location or resume. An accommodation request need not include a diagnosis.

SMS updates, recruiting contact, talent-pool retention and AI-assisted resume review may be separate choices. Save what the person actually chose. For opt-out fields, record both the literal response and its meaning: “Yes, opt out” is not “Yes, allow AI review.” Check the wording each time. A broad background-check willingness or accuracy preference does not authorize a specific legal agreement, data disclosure or final submission. Apply the current harness rules and the candidate's actual authorization at that point.

## Save, reuse and refresh

Keep exact received Q&A in `interviews`, linked to its onboarding question and source. Store substantive claims as sourced profile facts. A convenient reusable index fits the existing `profile.preferences` format:

```json
{
  "application.work_authorization.country-code": {
    "value": {
      "question": "The exact question asked",
      "answer_id": "saved-interview-id",
      "fact_ids": ["supported-fact-id"],
      "meaning": "The candidate-confirmed meaning",
      "scope": {"country": "candidate's target country"},
      "confirmed_at": "date of the actual answer",
      "review_when": ["country or circumstances change"],
      "reuse": "equivalent fields only"
    },
    "source_ids": ["candidate-answer-source-id"]
  }
}
```

The AI constructs this privately using real IDs and values; the person never edits it. Add employer, job, occupation, tool, dates, units or permission scope when they change the meaning. Do not populate this example literally. Existing helper validation checks the preference's source references; semantic matching and refresh decisions remain the AI's responsibility.

Before reuse, read the latest state and exact answer; compare meaning, polarity, country, employer, job requirements and units. Check superseded facts, corrections and material changes. Do not re-ask just because the question has different words. Ask if its scope differs or the old answer cannot safely resolve it. Updating the index must preserve original interviews and correction history.

For each real application, preserve the exact portal question/options and the actual prepared answer in a versioned private Q&A file linked to the application record. Keep draft and submitted snapshots distinct. Mark an answer submitted only after verified submission; preserve later corrections separately. These saved form questions enrich future interviews without turning a previously submitted draft into independent proof of a candidate fact.
