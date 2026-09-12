# Workspace operations for the AI

The person never edits these files. Locate a Python 3.10+ runtime (`python`, `python3`, `py -3`, or a harness-bundled runtime). Do not install system packages or change PATH. If none is available, ask for the single missing runtime or use the harness's supported package environment with permission. Do not fall back to unguarded state writes.

`S` below is this installed skill's absolute directory. `W` is the NEW private workspace's absolute path. Resolve both from actual locations; do not copy example machine paths.

```sh
python S/scripts/workspace.py init --workspace W
python S/scripts/workspace.py show --workspace W
```

Initialization refuses an existing directory, filesystem roots, links/junctions, and paths inside a Git repository or installed skill. Choose a new empty sibling under an already existing writable parent. It never adopts an existing job-search folder. It writes a workspace identity marker, authoritative `.job-search/state.json`, content directories and a friendly status note. Initialization alone does not know the candidate's identity.

Remember W in the current conversation/project through an allowed project-local note if needed; do not modify global memory, another project's AGENTS.md/CLAUDE.md, or the shared installed skill. If the project is the public source repository, keep all personal pointers and state outside it. In a new conversation without an accessible pointer, ask for the workspace location once instead of searching unrelated folders.

## Save an answer or other update

1. Read state with `show`. Note `revision` and `workspace_id`.
2. Write the raw answer or source to a temporary file inside W, then use `import-file` to save an immutable, versioned content file. It accepts a source path outside W only for an explicitly supplied file; never search unrelated files.

```sh
python S/scripts/workspace.py import-file --workspace W --source TEMP --relative sources/answer-001.txt
```

3. Copy the current state into a temporary draft within W (for example `scratch/draft.json`). Add the source using the returned `file` and `sha256`, a unique `id`, `kind` and timestamp with timezone. Add the exact interview Q&A, its interpretation, and relevant facts/preferences. Keep every existing record.
4. Commit through the helper, supplying the revision you actually read:

```sh
python S/scripts/workspace.py commit --workspace W --input W/scratch/draft.json --expected-revision 0 --summary "Saved target work preference"
python S/scripts/workspace.py show --workspace W
```

On Windows, preserve the JSON strings exactly. Some PowerShell JSON conversions reinterpret ISO timestamps and rewrite them. Prefer Python's `json.load`/`json.dump` when editing the draft; never parse or reformat `created_at`, `workspace_id` or history. Write source text through a file argument instead of embedding unescaped candidate text in a shell command.

The helper verifies references and content hashes, preserves the previous state in backups, writes atomically and increments the revision. A revision conflict means reread and merge; never just alter the revision on an old draft. A saved source without a committed state is an unfinished step that can be resumed using the same immutable file.

Create temporary scratch files/runtimes only within W. Persistent sources and final outputs use `import-file`; documents use the document helper, which calls the same guarded import. Never write directly to `.job-search/state.json`, backups, marker or referenced evidence files.

## State shape

Read the initialized state instead of constructing an envelope from memory. Schema v1 contains:

- `profile.facts`: `{id, claim, category, status, limits, source_ids, supersedes?}`.
- `profile.preferences`: named entries `{value, source_ids}`.
- `sources`: `{id, kind, recorded_at, file, sha256, url?}`; immutable.
- `interviews`: `{id, question, answer, interpretation, recorded_at, source_ids}`; immutable.
- `decisions`: `{id, decision, scope, source_ids}`; immutable.
- `applications`: `{id, employer, role, job_id, url, location, stage, outcome, posting_status, next_action, source_ids, posting_source_ids, outcome_source_ids, fit?, submission?}`.
- `fit`: entries `{requirement, assessment, fact_ids}`. Assessment is supported, unknown, gap or not_required.
- `submission`: `{confirmed_at, source_ids, files:[{file,sha256}]}`; immutable once saved. Employer confirmation required.
- `runs`: `{id, scope, status, checks:[{source,query,status,required,checked_at,inspected,source_ids}], ...}`.
- `pending_actions`: `{id, application_id, action, status, next_check, ...}`.
- `integrations`: capability records with `status` (not_configured/configured/tested/observed_scheduled), actual ID if created, scope, timezone, consent source, observed evidence references; never credentials.
- `session`: current phase, next_action, unresolved questions and workspace-local paths as useful.
- `history`: helper-owned commit summaries. Never edit it.

Additional fields may hold useful details; keep all candidate facts sourced. IDs use letters, numbers, underscore or hyphen (max 80 characters). Paths are workspace-relative forward-slash paths, never machine-specific paths or URLs. A source file reference is not a claim that its content was independently verified.

## Recovery and concurrency

Read from disk every turn. Keep one writer per workspace. The helper's exclusive lock refuses concurrent writes; a lock's age is not evidence that its owner stopped. If a process was interrupted, inspect the recorded PID and the actual host process/session. Only remove its exact lock file after establishing that owner is stopped and no write is running. Preserve the state and backups; ask for help if ownership is uncertain.

On recovery, validate state hashes, inspect pending actions and resume the recorded next action. Unsupported schemas, missing evidence or altered submitted snapshots must stop state writes until resolved. Never “repair” by silently deleting the conflicting history. Before repeating any pending submission, check employer state to avoid duplicate applications.

Installing/updating the skill is separate from these records. Do not reinitialize W after an update. Validate its current schema, workspace ID, revision and evidence before continuing.
