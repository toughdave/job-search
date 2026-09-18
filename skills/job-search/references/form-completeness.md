# Saved-form completion checks

Run before describing an application as ready, recommending submission or clicking Submit, in manual and scheduled work. Document visual review is a separate earlier requirement. A valid resume, a parser's result or an enabled Continue/Submit button does not establish that the form is complete.

## Inspect and correct

1. Build the expected work-history and education inventory from this candidate's current evidence bank, employer periods, credentials and instructions **before** comparing it with the parsed form. Use stable labels for each employer/role/period and each qualification. Include all supported entries requested by the form, even when parsing missed them or the section is optional. Apply employer limits (such as most recent three roles) or the candidate's exclusions explicitly; do not copy the form's omissions into the expected list. No resume or no history is valid when established by the candidate, not inferred from a blank parser result.
2. Inspect every page and section, including collapsed panels and conditional fields. Review legal/contact details, profile links, skills, each employment title/date/description, education institution/credential/field/dates, certifications where offered, screening answers, compensation, availability and attachments. Fill required fields and relevant, supported recommended/optional fields within the candidate's authorization. Do not fill irrelevant fields, invent qualifications, volunteer sensitive information or override saved privacy choices just to remove blanks. A supported omission needs a specific reason and source; an unknown optional fact can remain blank with the reason recorded. A required unknown blocks readiness until resolved or a truthful not-applicable route is confirmed.
3. Compare credential dropdowns with the exact evidence. Use a truthful Other/text route or a genuinely equivalent approved category and retain the exact title where possible. A missing dropdown label is not permission to omit education or upgrade the qualification. Explain an unresolved limitation before recommending submission. Do not generalize one person's approved credential mapping, GPA exclusion or contact details to another candidate.
4. Save/blur each changed field, navigate forward and re-open the final review. Compare **saved values** with intended values. Check for parser-invented entries, duplicates, truncation, wrong dates, stale profile data, missing fields and the actual attached filenames. If a text snapshot omits a value, use a visual or supported DOM inspection. Unseen values stay unverified. Preserve a private snapshot or screenshots of the saved review; never retain passwords, session tokens or verification codes.
5. Save and check the evidence record below. Any unresolved check, missing expected entry or supported field left blank without a justified exclusion blocks `ready` and a submission recommendation. Correct the form and repeat the affected inspection; then recheck the final review. Show the person a short result and any intentional omissions. Final submission authorization remains separate from passing this check.

Recheck after material form edits, attachment changes, candidate corrections or expired-session recovery, and inspect the live form again immediately before submission. A local PASS cannot prove that the remote form still has the same values. If the browser or validator is unavailable, preserve the draft and report the blocker. If the person already submitted independently, record the actual outcome and disclose any omission; never manufacture a retrospective pre-submission pass.

## Private evidence record

The AI operates these commands using the configured interpreter; the candidate does not fill JSON.

```sh
python S/scripts/form_review.py context --workspace W --application APP_ID
```

Use its actual `workspace_id`, `application`, `context_sha256` and `revision`. Prepare `scratch/form-review.json` with:

| Key | Required evidence |
| --- | --- |
| `schema_version` | `1` |
| `workspace_id`, `application`, `context_sha256` | Values returned by `context`, after application answers and upload references are saved. |
| `reviewed_at`, `review_url` | Actual offset timestamp and the observed portal review URL without secret query tokens. |
| `inventory_source_ids` | Registered sources supporting the independently derived expected inventory. Include no-history confirmation when applicable. |
| `evidence_files` | Existing private `{file, sha256}` references for inspected saved-form snapshots/screenshots. Use `workspace.py import-file` to retain them. |
| `expected_work_history`, `observed_work_history` | Unique stable entry labels from the bank and from the saved form respectively. |
| `expected_education`, `observed_education` | Unique qualification labels from the bank and from the saved form respectively. |
| `exclusions` | Normally `[]`. Each omitted inventory entry needs `{section, id, reason, source_ids, candidate_disclosed: true}`. `section` is `work_history` or `education`; sources must substantiate the actual employer/candidate instruction or absent portal section. |
| `checks` | All eight named checks below. |
| `fields` | One observation per inspected field/control, covering each verified section, including supported optional fields. |

The eight checks are `identity_contact`, `work_history`, `education`, `profile_links_skills`, `answers_dates`, `attachments`, `saved_final_review` and `consent`. Each contains `{status: "verified", evidence: "Specific observation from the saved form"}`. Use `not_applicable` only for a genuinely absent/inapplicable section, with `reason` and `candidate_disclosed: true`. Identity and final saved review cannot be skipped. Expected history minus documented exclusions must equal observed history, even for an absent section; an unexplained `not_applicable` never excuses missing entries. If there is no history, both lists are empty and the check explains the candidate's confirmation.

Each `fields` entry has a unique `id`, actual `label`, `section` from the eight checks, `requirement` (`required`, `recommended` or `optional`), boolean `supported`, `status` (`verified`, `omitted` or `not_applicable`) and specific `evidence`. Verified fields also include nonempty `expected_value` and `saved_value`; they must match. Describe checkbox selections and attachments as their actual visible labels. For a truthful approved dropdown mapping, the expected value is the approved selectable label, with the exact qualification and mapping explained in evidence. Unverified values must not be made to match by editing the review record instead of the form.

An omitted/not-applicable field needs `reason`; supported or non-optional omissions also need substantiating `source_ids` and `candidate_disclosed: true`. A required field cannot be `omitted`. `consent` checks existing saved consent selections against actual authorization; it does **not** assert final-submit permission. A consent action that takes effect only on Submit remains for that separately authorized action.

```sh
python S/scripts/form_review.py save --workspace W --application APP_ID --draft scratch/form-review.json --expected-revision N
python S/scripts/form_review.py check --workspace W --application APP_ID
```

`save` validates the record, retains an immutable hash-named copy under `applications/APP_ID/form-reviews/`, registers its document source, and commits `applications[].form_review`. Read back its returned reference and revision. Identical retries reuse the saved reference. `check` returns PASS only for a valid current record; failure exits nonzero. Keep earlier versions and append a new observation after corrections. Do not edit the JSON in place, invent hashes or bypass refusal with a manual state write.

New/changed `ready` applications are guarded at workspace commit. Candidate profile, employer inventory, application answers and upload-reference changes make a saved review stale. Move an affected ready application back to `preparing` in the same update, then inspect and save a fresh review. Legacy ready entries remain readable for migration, but require this check before being recommended or submitted again. Offline document readiness uses the `materials_ready_at` milestone or a preparing-stage next action; it is not proof of a completed portal form. Recording an actual employer receipt remains possible even when the person submitted independently without this review.

The helper validates recorded evidence and consistency. It cannot observe omitted browser fields, judge the truth of arbitrary prose or prove that the AI inspected the browser. The live review and independent inventory are mandatory alongside the helper.
