# Runtime setup

The installing AI performs these steps. The beginner sends the normal start message and responds only to a specific host approval or missing capability. Installing/copying a skill does not run a package-install hook: complete this setup after installation and on first invocation.

## a. Find or install Python

Use a verified harness-supplied Python, `py -3` on Windows, or `python3` on macOS/Linux. Run it to check its version; a PATH entry or Windows Store alias is not evidence that it works. Existing Python 3.9+ is supported. Prefer maintained Python 3.12+ for a new private runtime. Do not change system Python, shell profiles or another candidate's environment.

If Python is missing, use an available **uv** executable to install a private Python. If uv is also missing, download the official installer to a local file, read it and verify its official origin before executing it. Use the current [uv installation instructions](https://docs.astral.sh/uv/getting-started/installation/) and [unmanaged installation option](https://docs.astral.sh/uv/reference/installer/#unmanaged-installations). Do not pipe uninspected remote content into a shell. Respect host approvals; do not bypass a blocked action.

Choose a NEW `.job-search-tools` folder in the selected private project, outside the installed skill and public checkout. Create a `.gitignore` containing `*` there before downloads. Never adopt an unrelated existing tools folder. Save the owned location for continuation. For the installer process, set `UV_UNMANAGED_INSTALL` to its `bin` subfolder; this prevents shell/PATH changes. Then invoke that absolute uv executable with process-local settings:

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

The helper creates `W/.runtime/job-search-venv`, installs `requirements-documents.txt` there, and saves `W/.runtime/runtime.json`. The manifest includes DOCX creation, PDF creation/reading, timezone data and PDF rendering. Transitive packages are installed by pip. Requirements files belong in the shared skill; downloaded packages, interpreter binaries, caches and installation results do not.

It preserves other environments under `.runtime`, rejects a conflicting unowned target or foreign workspace, and refuses the public source/installed skill as a runtime location. Re-running resumes or repairs the same owned environment. If Python lacks working `venv`/`ensurepip`, invoke the helper with `--uv /absolute/path/to/uv` to use uv for environment creation. Never install packages globally to get past that failure.

Read the JSON result and use its absolute `python` path for all later helpers, including native routine prompts. Setup must pass package/version checks, timezone lookup, actual DOCX/PDF creation and readback, and a PDF-to-image render. A failed command leaves setup incomplete. A `runtime-ready` result covers these local capabilities only.

## c. Recheck and finish capability setup

On return or update, run the helper with `--check-only`. This performs local checks without downloading packages. If the requirements changed, packages are missing or the environment is broken, run normal setup again before dependent work. Existing older `.runtime` environments remain untouched; this helper owns only its named subfolder and records.

Before announcing that the full workflow is ready, also check what the intended work requires:

- **Actual resume input:** verify readable text; scanned PDFs may require the host's OCR tool. Request readable text only when no suitable OCR capability is available.
- **Fonts:** verify the candidate's actual script and glyphs with the exporter. If missing, obtain a suitable licensed font from its official source into the private tools area, or use a verified host document tool. Do not claim support for an untested writing system.
- **PDF review:** the installed `pypdfium2` can render page images locally. The AI must inspect every final page; creating an image does not count as inspecting it.
- **DOCX review:** detect a verified host document renderer, Word or LibreOffice. Python DOCX creation does not render Word pages. Use a supported available renderer; if one is absent, arrange an official installation only within the person's permissions or clearly leave DOCX visual review pending. Do not report PDF pagination as DOCX pagination.
- **Web and browser:** use the harness's available tools; Python/Node cannot grant accounts or browser integrations. Verify a real search/read before claiming online search works.
- **Scheduled work:** save the verified interpreter path with the local routine instructions. Check native scheduler availability and read back its configuration separately. No dependency install activates a timer or grants consent.

Install capability-specific extras when needed and authorized; do not install an entire browser/office stack unnecessarily. A dependency failure can leave interviewing available while export or automation stays pending. Never present that partial state as a fully working installation.

## Node and the optional CLI

Node is only needed for the third-party `npx skills add` route, not this Python workflow. With compatible Node, use the documented CLI command, then summon the skill to run setup. Without Node, the AI should use the complete release ZIP or source download-and-copy route from `INSTALL.md` in the repository. This avoids requiring the person to install Node solely for copying a skill.

If the person specifically chooses the npx route, check `node --version` and `npx --version`, and arrange a supported Node runtime through the host's runtime provider or [official Node downloads](https://nodejs.org/en/download) before invoking npx. Verify the commands afterward. Do not tell the person that a skill can execute a command whose interpreter does not yet exist.
