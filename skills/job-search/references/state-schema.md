# State values and small transactions

For the AI, not a form for the candidate. Start with `workspace.py show`; copy that current state into a scratch draft and preserve all existing records. `assets/state-example.json` is a valid blank schema-v1 envelope for orientation, not a replacement for an initialized bank. Never copy its identity or timestamps into live state.

## Allowed values

| Field | Values |
| --- | --- |
| `sources[].kind` | `resume`, `candidate_answer`, `document`, `employer`, `official`, `candidate_report` |
| `profile.facts[].category` | `employment`, `project`, `volunteering`, `education`, `certification`, `skill`, `preference`, `identity`, `other` |
| `profile.facts[].status` | `candidate_reported`, `verified`, `unresolved`, `superseded` |
| `applications[].stage` | `discovered`, `qualified`, `preparing`, `ready`, `submitted_unverified`, `submitted`, `blocked`, `skipped`, `withdrawn` |
| `applications[].outcome` | `none`, `awaiting`, `positive`, `action`, `offer`, `declined` |
| `applications[].posting_status` | `unknown`, `open`, `closed`, `expired`, `cancelled` |
| `applications[].fit[].assessment` | `supported`, `unknown`, `gap`, `not_required` |
| `runs[].status` | `running`, `complete`, `incomplete` |
| `runs[].checks[].status` | `complete`, `partial`, `blocked`, `not_configured` |
| `pending_actions[].status` | `pending`, `resolved` |
| `onboarding.resume.status` | `unchecked`, `awaiting_file`, `unreadable`, `read`, `no_resume` |
| `onboarding.topics[].kind` | `profile`, `example`, `linkedin` |
| `onboarding.dispositions[].status` | `declined`, `deferred`, `not_applicable`, `no_example`, `reopen` |
| `onboarding.experiences[].kind` | `employment`, `self_employment`, `volunteering`, `project`, `education` |
| `onboarding.history_reviews[].status` | `complete`, `more_to_add` |

Every source has `{id, kind, recorded_at, file, sha256}`. Get `file` and `sha256` from `import-file`; never invent a hash. Timestamps include an offset. Facts have `{id, claim, category, status, limits, source_ids}`; a candidate answer supports `candidate_reported`, not independent `verified`. A disposition needs a saved candidate decision, source IDs and a reason. Unknown details stay unresolved. See [onboarding](onboarding.md) for employer questions and [routine](routine.md) for schedule fields.

## Map a saved target-work answer

`save-answer` returns the exact interview record and source IDs. If its exact answer was “Office coordination,” the following records illustrate a valid mapping. Substitute the real returned answer/source IDs and new unique IDs. Append to the latest state; do not invent an answer for this example.

```json
{
  "fact": {
    "id": "target-office",
    "claim": "Wants to find office coordination work.",
    "category": "preference",
    "status": "candidate_reported",
    "limits": "Desired work, not proof of experience or qualifications.",
    "source_ids": ["ANSWER_SOURCE_ID"]
  },
  "track": {
    "id": "office",
    "occupation": "Office coordination",
    "source_ids": ["ANSWER_SOURCE_ID"]
  },
  "evidence": {
    "id": "target-office-evidence",
    "topic_id": "target-work",
    "dimension": "occupation",
    "fact_ids": ["target-office"],
    "source_ids": ["ANSWER_SOURCE_ID"],
    "answer_ids": ["ANSWER_ID"],
    "rationale": "The candidate explicitly named their desired work."
  }
}
```

Append `fact` to `profile.facts`, `track` to `onboarding.tracks`, and `evidence` to `onboarding.evidence`; set `onboarding.active_track` to the track ID. Set `session.next_action` to the next actual task, commit with the revision just read, then run `plan`. Do not mark unrelated background dimensions answered by a career preference.

## Add an employer period

First save or reuse identity/date facts sourced to the actual resume or candidate answer. Append one entry to `onboarding.experiences`:

```json
{
  "id": "cedar-office-2022",
  "employer": "Cedar Clinic",
  "role": "Office Assistant",
  "start": "2022",
  "end": "2024",
  "kind": "employment",
  "fact_ids": ["ROLE_AND_DATES_FACT_ID"],
  "source_ids": ["ROLE_SOURCE_ID"]
}
```

Create a shared `profile` topic with `experience_id` and `dimensions:["responsibilities"]`, plus an occupation-specific `example` topic with that same experience ID and `dimensions:["context","personal_action","tools","result"]`. Topics require `id`, `track_id` (null for shared), `kind`, `title`, `required:true` and `dimensions`. The source must actually support the employer, title and date precision. Save role-specific facts with `experience_id`, map one dimension at a time, and retain exact Q&A. Reuse existing facts before asking. Never translate expected duties into experience.

Use a new sourced superseding fact for corrections. Do not edit saved sources, interviews, employer entries, evidence mappings or helper-owned history. For less common fields, read the corresponding reference; the schema validator checks structure and reference consistency, not the truth of arbitrary prose.
