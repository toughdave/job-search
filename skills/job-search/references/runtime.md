# Runtime setup

The installing AI performs these steps. The beginner sends the normal start message and responds only to a specific host approval or missing capability. Installing/copying a skill does not run a package-install hook: complete this setup after installation and on first invocation.

## a. Find or install Python

Read the saved interpreter path first. For initial setup or repair, prefer a maintained harness Python, then installed interpreters listed by `py -0p` on Windows or available `python3` commands. Run `S/scripts/setup_runtime.py --preflight` with a candidate interpreter: it verifies SSL, ensurepip, venv creation and child execution. A version string, PATH entry, Store alias or application-bundled Python is not enough. Skip an unsuitable interpreter. Existing Python 3.9+ is supported; prefer maintained Python 3.12+ for a new runtime. Do not change system Python or shell profiles.

If Python is missing, use an available **uv** executable to install a private Python. If uv is also missing, download the official installer to a local file, read it and verify its official origin before executing it. Use the current [uv installation instructions](https://docs.astral.sh/uv/getting-started/installation/) and [unmanaged installation option](https://docs.astral.sh/uv/reference/installer/#unmanaged-installations). Do not pipe uninspected remote content into a shell. Respect host approvals; do not bypass a blocked action.

Keep bootstrap tools in an owned `tools` folder under the nonsynced local cache: Windows `%LOCALAPPDATA%/job-search`, macOS `~/Library/Caches/job-search`, or Linux `$XDG_CACHE_HOME/job-search` (default `~/.cache/job-search`). Use a new folder or its recorded owned location; never adopt unrelated contents. Add `.gitignore` and `.ignore` containing `*`. Save the location for continuation. For the installer process, set `UV_UNMANAGED_INSTALL` to its `bin` child; this prevents shell/PATH changes. Invoke that absolute uv executable with process-local settings:

- `UV_PYTHON_INSTALL_DIR`: the tools folder's `python` subfolder.
- `UV_CACHE_DIR`: its `cache` subfolder.
- `UV_PYTHON_BIN_DIR`: its `bin` subfolder.

Run `uv python install 3.12`, then `uv python find --managed-python 3.12` with the same settings. Execute the returned absolute interpreter to verify it. This route does not require an existing Python or Node installation. Keep these environment settings confined to those commands; restore any temporary shell values. See [managed Python](https://docs.astral.sh/uv/guides/install-python/) and [uv environment paths](https://docs.astral.sh/uv/reference/environment/).

If downloads, the OS or organizational rules prevent installation, preserve progress and explain the single blocker. Do not claim Python was installed. On a later session use the saved absolute interpreter; after a project move, rebuild a private environment if its paths no longer work, preserving the old environment and all candidate records.

## b. Install the required packages

Use the verified interpreter for the standard-library `workspace.py` and `onboarding.py` initialization/binding steps. Read the existing project pointer first. `W` below means the verified private records folder; `S` means the installed skill folder. Substitute absolute paths and quote them correctly for the current shell.

```sh
python S/scripts/setup_runtime.py --workspace W
```

The helper creates a workspace-ID-specific environment in the local cache above and saves only a small pointer at `W/.runtime/runtime.json`. `JOB_SEARCH_CACHE_DIR` can select another private nonsynced base for controlled setup/tests. Large package trees must not live in Documents, OneDrive or iCloud. The manifest includes DOCX creation, PDF creation/reading, timezone data and PDF rendering. Corporate pip mirrors, certificates and proxies are respected; packages still target the private venv. Requirements files ship with the skill; installed packages and credentials do not.

It rejects an unowned target, foreign workspace or public-source/installed-skill location. A broken executable or removed base Python causes the owned environment to be preserved and rebuilt. Use a healthy bootstrap Python outside that environment. `--uv /absolute/path/to/uv` supports environment creation through uv. Never install packages globally to get past a failure.

Read the JSON result and use its absolute `python` path for all later helpers, including native routine prompts. Setup must pass package/version checks, timezone lookup, actual DOCX/PDF creation and readback, and a PDF-to-image render. A failed command leaves setup incomplete. A `runtime-ready` result covers these local capabilities only.

## c. Recheck and finish capability setup

On return or update, run `--check-only` once per session, then reuse its result unless a capability fails or dependencies change. It downloads nothing. A failed check retains the interpreter/cache paths and marks setup incomplete. Run normal setup with a healthy bootstrap interpreter to repair it before dependent work.

Setup locks record the host, parent process, installer child and token. Recover a stopped owner with `--unlock-token TOKEN`; live owners, foreign hosts and uncertain child-launch ownership are refused. Never remove a lock based on age. Re-run setup after recovery.

After verification, the helper moves its owned legacy `W/.runtime/job-search-venv` into the cache, preserving its contents. If the current process uses that old venv or a legacy setup lock exists, `legacy_cleanup_pending` identifies the remaining move. Use a healthy bootstrap interpreter outside it, and verify any old installer has stopped before recovering its lock. Candidate records are never moved. Use explicit saved paths rather than globbing the entire project.

Before announcing that the full workflow is ready, also check what the intended work requires:

Run `setup_runtime.py --detect-renderers` to check PATH and standard LibreOffice installations, including Program Files on Windows and `/Applications/LibreOffice.app` on macOS. Use the returned absolute executable path. Successful `--version` detection is not a visual review: follow the [document quality gate](documents.md#quality-gate) to render and inspect the actual file before uploading it.

- **Actual resume input:** verify readable text; scanned PDFs may require the host's OCR tool. Request readable text only when no suitable OCR capability is available.
- **Fonts:** verify the candidate's actual script and glyphs with the exporter. If missing, obtain a suitable licensed font from its official source into the private tools area, or use a verified host document tool. Do not claim support for an untested writing system.
- **PDF review:** the installed `pypdfium2` can render page images locally. The AI must inspect every final page; creating an image does not count as inspecting it.
- **DOCX review:** detect a verified host document renderer, Word or LibreOffice. Python DOCX creation does not render Word pages. Use a supported available renderer; if one is absent, arrange an official installation only within the person's permissions or clearly leave DOCX visual review pending. Do not report PDF pagination as DOCX pagination.
- **Web and browser:** use the harness's available tools; Python/Node cannot grant accounts or browser integrations. Verify a real search/read before claiming online search works.
- **Scheduled work:** save the verified interpreter path with the local routine instructions. Check native scheduler availability and read back its configuration separately. No dependency install activates a timer or grants consent.

Install capability-specific extras when needed and authorized; do not install an entire browser/office stack unnecessarily. A dependency failure can leave interviewing available while export or automation stays pending. Never present that partial state as a fully working installation.

## Runtime cache cleanup

Cleanup is optional and candidate-directed. Use a healthy bootstrap Python outside the cache. `setup_runtime.py --remove-cache --workspace W` previews the owned cache, exact package paths and approximate bytes. Show the candidate that preview; after explicit removal approval, repeat with `--confirm-workspace-id ID`. The helper keeps candidate records and its small owner marker, refuses a foreign owner or active setup lock, and marks the runtime for reinstallation. Close other work using that runtime first. It removes preserved environments and downloads in that same cache too.

For an abandoned project, `--list-caches` reads only job-search's cache ownership records. A missing records path may mean a project move; do not classify or remove it automatically. Ask the candidate to select the cache, then preview with `--remove-cache --cache-workspace-id ID`. The same confirmation flag is needed for removal. Never scan unrelated folders or delete a cache selected only by age. The helper rejects unsafe paths and junctions; it unlinks internal symbolic links without following their targets. Normal setup recreates removed software when the search resumes.

## Node and the optional CLI

Node is only needed for the third-party `npx skills add` route, not this Python workflow. With compatible Node, use the documented CLI command, then summon the skill to run setup. Without Node, the AI should use the complete release ZIP or source download-and-copy route from `INSTALL.md` in the repository. This avoids requiring the person to install Node solely for copying a skill.

If the person specifically chooses the npx route, check `node --version` and `npx --version`, and arrange a supported Node runtime through the host's runtime provider or [official Node downloads](https://nodejs.org/en/download) before invoking npx. Verify the commands afterward. Do not tell the person that a skill can execute a command whose interpreter does not yet exist.
