# LinkedIn and the evidence bank

Use three stages: capture the profile link early, reconcile profile evidence when authorized, and offer a fuller profile review after enough career information is gathered. Keep everything in this candidate's private project. A URL, permission to review, a completed review and permission to publish are four different things.

## Early: the resume link

Before formatting the first resume/CV, check the supplied resume, profile and exact answers for the candidate's LinkedIn URL. Reuse an already confirmed link. If missing, ask one short question: “Would you like a LinkedIn profile link on your resume?” If yes, ask for the URL next; do not search by name and guess which person is theirs. A URL explicitly supplied as their own need not be confirmed again. If an old resume's link is ambiguous or outdated, ask whether it is still theirs.

Save the URL as a sourced identity fact and map it to the `linkedin-url` topic. Save the decision to include it as a sourced profile preference, for example `linkedin_on_resume`. Record none, declined or deferred explicitly; lack of a LinkedIn profile must not prevent a resume. If deferred, omit the link from the current draft and retain the pending choice. Capture the actual profile URL, normally `https://www.linkedin.com/in/<their-profile>/`, stripping tracking parameters while preserving the candidate's real profile identifier. Do not invent a vanity URL. A URL shape check does not verify ownership, accessibility or content.

Using a supplied link on the resume does not require browsing or an account connection. With confirmed ownership and inclusion choice, use the saved URL in the contact section and cite its identity fact in the document model. Check the complete URL after export and in uploaded portal fields. Do not substitute a LinkedIn search result, home/feed page, company page or login redirect. If clickable hyperlinks are added by a document tool, verify the actual target as well as the visible text; the bundled plain-text contact field does not itself guarantee clickable links.

## Early or during the interview: enrich the evidence

Offer the existing optional review choice once. If the candidate authorizes reading/review, read accessible profile sections now when that can fill interview gaps; do not wait until the resume is finished to discover additional employers or qualifications. Use only their supplied profile or authorized export/pasted content. An inaccessible page should lead to one simple request for profile text/export when needed, not repeated login attempts. Save which sections were accessible and their capture time. The URL alone is not a completed profile read.

Save an immutable profile snapshot as a `document` or `candidate_report` source, with its original URL and date. Publicly visible self-written profile content is still candidate-reported evidence, not independent employment or credential verification. An inaccessible section remains unreviewed; a missing item on LinkedIn does not prove the person lacks it. Treat endorsements, recommendations and AI-written copy as leads with their actual provenance; do not turn them into verified claims.

Compare the profile section by section with the current evidence bank: employers, role periods, responsibilities, projects, achievements, skills, education, certifications, volunteering, publications and portfolio links where relevant. For each item:

- **Already supported:** link the new source to a new evidence mapping or corroboration record without rewriting immutable facts. Do not ask the same question again.
- **Additional, consistent detail:** save it with the profile source and the correct employer/role/period. Use it to direct any missing follow-up; profile prose alone is not a complete scenario. Add newly found employers to the inventory and confirm completeness again.
- **Conflict or ambiguous claim:** retain both versions and ask one precise question, such as “Your resume says this role started in 2022, but LinkedIn says 2021. Which should I use?” Ask just the short factual question. Do not add claims that all other sections match unless they were actually compared. A recently captured page does not automatically outrank an explicit candidate correction. Keep unresolved dates, qualifications or achievements out of definitive resume claims.
- **Candidate correction:** save the exact answer, supersede the contradicted fact and append its replacement. Keep the original profile snapshot and old submitted files intact. Review affected current drafts and profile recommendations.

Do not copy private application answers, salary expectations, work-authorization documents, demographic disclosures, private contact details or references into public profile recommendations merely because they exist in the evidence bank. Select only public-facing information appropriate to the candidate's chosen profile.

## Later: review and propose improvements

After the employer history, relevant examples, qualifications and target direction are sufficiently reconciled, use the richer evidence bank to review the headline, About, experience, education, credentials and skills. Review available sections against the intended occupation and the candidate's voice. Save a concise section-by-section comparison: current text, proposed text, reason, supporting fact IDs and unresolved questions. If material information remains missing, label recommendations provisional. Useful resume drafts can proceed; optional LinkedIn review must not delay every application.

Reuse an accepted review request. Do not re-ask permission for the same authorized review because a session ended. Respect a declined choice and resume a deferred review only when requested or when it becomes necessary and the candidate agrees. One saved “yes” means requested, not completed. The work remains pending until actual profile content, reconciliation and a saved review draft exist, or the candidate explicitly defers it.

Show the proposed public changes for review. Publish only the specific edits covered by explicit candidate approval using available authorized browser/tools. If tools cannot edit the profile, provide ready-to-paste sections and say they are not published. Before writing, reread the live section to catch intervening edits; do not overwrite text changed since the draft without reconciling it. After each approved edit, inspect the saved profile and record the observed result. An uncertain save remains unverified; check the profile before retrying. Capture the resulting profile snapshot and reconcile it back into this workspace without treating our own newly published prose as independent corroboration.

## Keep both areas current without repeating the interview

On return, read current workspace state and `onboarding.py plan`. If the candidate supplies new profile content, a corrected URL, career evidence or a different occupation, reconcile that change and refresh affected recommendations. When already authorized, reread accessible profile sections during an actual profile-review task; do not poll LinkedIn every daily search by default. A profile can change remotely without the skill knowing. Describe freshness as “reviewed against the saved snapshot on [date],” not continuously synchronized.

After an evidence-bank correction, identify affected current resume/CV drafts through their saved fact maps and flag them for a new version. Compare the same correction to LinkedIn's relevant section and propose an update if needed. After a LinkedIn change, import newly supplied/observed details back through the same source-and-conflict process. Nothing silently overwrites the other side. Cross-project copying requires the candidate's explicit choice; another occupation folder has its own URL choice, profile sources and review history.

## Agent-maintained records

Use workspace.py import/commit; the candidate never edits these records. The existing `linkedin` onboarding topic stores the review choice. `linkedin-url` stores the link or explicit omission. Add missing baseline topics on upgrades and reconcile saved answers before asking.

Once a URL is established, save `integrations.linkedin` as:

```json
{
  "version": 1,
  "url": "https://www.linkedin.com/in/candidate-provided-slug/",
  "profile_fact_id": "candidate-link-fact",
  "profile_source_ids": [],
  "reviews": []
}
```

Replace the illustrative URL and IDs with the candidate's actual saved data. `profile_source_ids` identifies the latest accessible content snapshot, not merely the URL answer. Keep older sources in state when a newer snapshot replaces these references. With no profile, leave this integration absent and save the explicit topic disposition.

After reconciliation and draft review, append a review entry with `id`, `reviewed_at` (time with timezone), `track_id`, `profile_fact_id`, `profile_source_ids`, `fact_ids` and `output` (`file` and `sha256` returned by import-file). Snapshot the complete current non-preference, supported career/contact fact-ID set returned by `plan.linkedin.fact_ids`; list the actually used subset in the draft itself. Save exact approvals and publication outcomes separately as decisions and sources. Review entries are immutable; append a new version after changes.

The helper reports link-not-recorded, content-not-read, review-not-recorded, current or refresh-needed states. Changed career/contact facts, occupation, profile URL or snapshot reopen freshness automatically. These are structural checks against saved data, not proof of semantic agreement, live profile inspection, candidate approval or successful publication. Check unresolved facts, deferred choices and the saved draft before deciding the next action. A review status never grants publication permission.
