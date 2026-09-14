# Detailed setup guide

Your job search, guided through a conversation in **Codex or Claude Code**. You supply your experience and decisions. The AI organizes the files, asks questions, and prepares applications for your review.

**[First time: start here](#first-time-step-by-step)** · **[Summon the skill](#summon-the-skill)** · **[Coming back later](#coming-back-later)** · **[Daily search](#your-weekday-morning-search)** · **[Need help?](#if-something-stops-you)**

**Share the short guide:** [PDF](job-search-guide.pdf) · [PowerPoint slides](job-search-guide.pptx). Both include app download links, project screenshots, the exact first message and daily-search setup.

## First time: step by step

### Prerequisites and dependencies

Use a signed-in Codex or Claude Code session with a local project folder, file read/write permission and internet access. Bring your resume if you have one; starting without a resume is supported. The AI runs the setup steps for you.

| Tool | Purpose | Who handles it |
| --- | --- | --- |
| Python 3.9+ | Save evidence and run helpers. A maintained 3.12+ runtime is preferred for new setup. | The AI checks an existing interpreter or arranges a private one with uv. |
| python-docx, ReportLab, pypdf, pypdfium2, tzdata | Create Word/PDF files, read them back, render PDF pages and interpret timezones. | The AI installs the shipped requirements in this search's private runtime. |
| A visual viewing tool | Inspect every page of the actual upload document. | The AI uses the host's image/PDF viewing capability. |
| Word, LibreOffice or another DOCX renderer | Check actual Word-document layout when that format will be uploaded. | The AI checks converters, including standard LibreOffice locations outside PATH. |
| Node.js 22.20+ | Run the optional npx skill installer. | Optional. Download-and-copy installation needs neither Node nor Git. |

Software packages stay in a local cache outside your records. The [runtime instructions](../skills/job-search/references/runtime.md) cover checks, setup, repair and cleanup. If downloads or a required viewing tool are unavailable, the interview can continue with supported local saves, but affected document uploads remain pending. An ordinary browser chat cannot gain local file access simply by receiving this skill.

### 1. Open Codex or Claude Code

**Need the desktop app? Choose your computer below.** These official pages let you select and download the app before returning here.

| App | Mac | Windows |
| --- | --- | --- |
| Codex | [Mac download page (Apple Silicon)](https://learn.chatgpt.com/docs/app) | [Windows download page](https://learn.chatgpt.com/docs/windows/windows-app#download-the-chatgpt-desktop-app) |
| Claude Code | [Claude downloads: choose macOS](https://claude.com/download) | [Claude downloads: choose Windows or Windows ARM64](https://claude.com/download) |

Open a link in a new tab with **Ctrl+click** on Windows or **Command+click** on Mac, or right-click and choose **Open link in new tab**. This README uses explicit computer choices rather than trying to detect your operating system.

For Codex, the current download is the **ChatGPT desktop app**; open it and select **Codex**. For Claude Code, install **Claude**, then open its **Code** tab. The apps have their own account requirements; check the [Claude Code setup page](https://code.claude.com/docs/en/desktop-quickstart) if Code prompts you to upgrade. Already installed? Continue below. Sources: [OpenAI desktop setup](https://learn.chatgpt.com/docs/app), [Claude downloads](https://claude.com/download).

Sign in to a version that can work with files on your computer. Start a conversation in a **dedicated local project/folder**, such as **My Job Search**. Here, “project” simply means the folder the AI is working in.

Use a local session, rather than an ordinary browser chat. You do not need to download this repository or create the skill's internal folders yourself.

**Follow the instructions for your app, then check permissions below.**

#### a. Choose your project

**Codex:** above the message box, click **Choose project**. Select your existing **My Job Search** project, or open **Create project** to make one.

![Codex message box with Choose project above it and the permission selector at the lower left.](images/codex-choose-project.png)

**Claude Code:** open the **Code** tab and select **Local**, then choose the folder as described below.

#### b. Select or create your folder

**Codex:** in **Create project**, enter **My Job Search**. Under **Source folders**, choose **Add a folder on this computer**, then click **Add**.

<img src="images/codex-create-project.png" alt="Codex Create project dialog with Project name, Source folders, Add a folder on this computer, Add, and Create project controls." width="620" />

- Select a dedicated folder in the folder picker. To make one, use **New folder** if available, or create **My Job Search** in Documents with File Explorer (Windows) or Finder (Mac) first.
- Confirm the folder selection, then click **Create project**. Check that project is selected above the message box. A project name alone does not select a disk folder.

**Claude Code:** click **Select folder**, choose your **My Job Search** folder and confirm. Create the folder in your file manager first if needed. See the [Claude setup walkthrough](https://code.claude.com/docs/en/desktop-quickstart#start-your-first-session).

The screenshots above show Codex. Labels can vary by version; see the [Codex project guide](https://learn.chatgpt.com/docs/projects). Using a terminal or editor? Open the dedicated folder as the working directory before starting the AI.

<a name="allow-the-ai-to-read-and-save-files"></a>

The skill needs to read your resume, create folders, save records and run its tools. Choose the setting below for your app; these settings are separate from model selection.

#### c. Codex: Full access

Click the permission label at the lower left of the message box, then select **Full access**. Check that **Full access** appears beside the shield icon. This allows unrestricted internet and file access, including files outside the selected project.

![Codex permission dropdown showing Ask for approval, Approve for me, and Full access, with Full access selected.](images/codex-permissions.png)

#### d. Claude Code: Auto

Click the mode label at the lower left of the message box, then select **Auto**. Check that **Auto** appears below the message box. Claude handles permission decisions using background safety checks; some actions can still require your input.

![Claude Code mode dropdown showing Auto, Manual, Accept edits, Plan, and Bypass permissions, with Auto selected.](images/claude-permissions.png)

These screenshots show the guide author's current desktop apps. **Full access grants access beyond your project folder; Claude's Auto keeps automatic safety checks.** These are the settings chosen for this walkthrough. More restrictive modes can also run the skill with your approvals. If a setting is unavailable, check your app version or organization policy. Sources: [Codex permissions](https://learn.chatgpt.com/docs/agent-approvals-security), [Claude permission modes](https://code.claude.com/docs/en/desktop#choose-a-permission-mode).

The skill normally creates a private `records` subfolder in your dedicated project. Access to your whole computer is not required by the helpers. If the AI needs a separate private records folder outside the selected project, approve that **specific folder** when asked, or give it another writable location. Keep candidate records outside the downloaded public repository and installed skill. Protected skill folders can still require installation approval even when ordinary project files are writable.

**Before continuing:** the correct project is selected, file editing is allowed, and you are ready to approve the installation if asked. The AI handles the remaining folders and files. On later visits, check the selected project and permission mode again if saving stops working.

### 2. Add your resume before sending

Use **one** method:

- **Attach it:** if your app accepts the document, add your PDF or Word resume using its attachment control. Check that the attachment appears before sending.
- **Supply its location:** copy the full location of the resume on your computer. Paste it beneath the message in step 3, after `My resume is at:`. Use the actual location of your file.
- **No resume yet:** add `I do not have a resume yet. Help me build one.` The AI can start by asking about your work or study.

The AI must confirm it can read the file. An attachment icon alone does not prove that it received readable resume text.

<a name="3-paste-this-message-then-press-send"></a>

### 3. Copy the start message, then press Send

Copy the complete message below into the **same message box** where you added your resume or its location:

```text
Install https://github.com/toughdave/job-search for this project.
Then use job-search to start my search.
```

**Send this once.** It asks the AI to install and begin; you do not also need a terminal command or “Continue my job search” now. Include your resume location or no-resume line before sending if you chose that option.

One-question pacing, waiting for your answers, saving progress and managing files are built into the skill. You do not need to repeat those instructions. A native goal is optional. During setup, the AI also offers an optional weekday morning search.

### 4. Let the AI set up, then answer its questions

**The AI handles the software setup too.** It checks Python, installs missing document and timezone packages in a private environment, and verifies that documents can be created and PDFs rendered. If Python is missing, it arranges a private runtime. You may see a download or approval request. Node is only needed for the optional terminal installer; the AI can install the skill without it.

The terminal command below copies the skill. Summoning it afterward starts these setup checks. If a required tool cannot be installed, the AI explains the specific next action and keeps unfinished setup visible.

The AI should check the installation, read your resume, and ask one useful question at a time. Your answers and documents usually go in a private **records** folder inside your project. Large software packages stay in a separate local cache. The AI tells you where it saved your search. If it needs an installation approval, a writable location, or a restart, follow that specific instruction before continuing.

Setup also leaves small project startup notes so Codex and Claude can find your saved conversation context when you return with a short answer. Keep those notes with the project. Existing project instructions are preserved. If your app still asks for context that you already provided, summon `job-search` again in the same project rather than starting over.

For example, after reading your resume it might ask:

> **AI:** What kind of work would you most like to do next?
>
> **You:** Office administration or customer support.

Give your own answer. The AI saves it and asks the next question when needed. You do not fill out a tracker or arrange application folders.

The AI builds a separate evidence section for **each employer, role and period of work**. With a resume, it uses the employers and bullets already there. Without one, it asks you about your employers, roles and dates, one missing detail at a time. It also confirms whether you have finished listing your employers.

For each role it asks directed questions about responsibilities and real examples: what happened, what you personally did, which tools you used, and the result or lesson. For example, if your resume lists scheduling work at a fictional Cedar Clinic:

> **AI:** At Cedar Clinic, tell me about one scheduling problem you handled as an office assistant.

Your answer stays linked to that employer and work period for future resumes, CVs and cover letters. One employer's story cannot complete another employer's checklist. Saved answers are checked before asking again; an interrupted interview resumes its missing detail. You can decline or defer a topic. The AI can prepare useful drafts while the rest of your history remains pending. It captures your LinkedIn link early for your resume, if you want to include one. With your permission it also reconciles additional profile information with your private evidence bank, then offers a fuller review once your career information is gathered. You can say yes, no, or later. See [LinkedIn workflow](../skills/job-search/references/linkedin.md).

It also checks your name, email, phone, city/region, relocation preferences, education, certifications and relevant skills. Each degree, diploma or certification keeps its own institution/issuer, dates and status. It asks about relevant projects, languages, awards or other CV details where useful. It reuses information you already supplied and remembers “none,” declined and deferred answers. A full street address is optional, not a routine resume requirement.

You can also save common application answers during setup or when a form needs them: work authorization, sponsorship, start dates, salary expectations, working arrangements and relevant screening questions. The AI remembers each answer's scope and date, checks the actual form wording, and asks again only when something material differs. Employer-specific questions wait for that employer; sensitive disclosures remain optional. Your private answers are never included in the shared skill.

### 5. Review the first useful result

After reviewing your experience and target destination, the AI recommends one or two pages and asks for your approval. A longer CV needs a relevant reason. It saves your choice and checks the actual pages for readable spacing and useful detail before presenting a draft.

When enough is known and the tools are available, the AI works toward a suitable application draft. Open its documents, check the facts, and give corrections in the conversation. For example: `That role was volunteering. Please correct it.`

If it cannot search the web, it may ask for a job posting. If a required fact or tool is missing, it should explain the next action instead of claiming the application is ready. Review the employer, role and document versions before authorizing a final submission.

**Visual review happens before upload.** The AI opens every page of the actual resume/CV file it will attach, checks spacing, alignment, clipping, page breaks and readability, and corrects problems. It inspects corrected versions again and records the reviewed file's hash. For a Word upload, it renders that exact DOCX through an available office converter; a separately generated PDF does not verify the DOCX. If it cannot view the required file, it keeps the draft and pauses the upload. This applies to manual applications and scheduled job hunting alike.

**That is the first-time process. The sections below are for later visits or optional help.**

<a name="already-installed"></a>

## Summon the skill

**Updating an earlier installation?** Send: `Update job-search from https://github.com/toughdave/job-search. Preserve my private records and any local customizations, then continue my search.` The AI should reconcile existing answers with the new checklist.

Once installed, open the **same local project**. Use the message box in your AI app, not your computer's terminal:

| App | How to summon `job-search` |
| --- | --- |
| Codex / ChatGPT desktop | Type `@`, then select **job-search** from the skill picker. If your Codex composer offers a `$` skill picker, select **job-search** there. |
| Codex CLI or IDE extension | Type `$job-search`, select the matching skill if a menu appears, then add your request. |
| Claude Code | Type `/job-search`, select the matching skill if a menu appears, then add your request. |

After selecting the skill, add **Start my search** or **Continue my job search**, then send. For a first search, supply your resume or its location if you have not already done so. Sources: [OpenAI skill invocation](https://learn.chatgpt.com/docs/build-skills#how-chatgpt-and-codex-use-skills), [Claude Code skills](https://code.claude.com/docs/en/skills).

**No matching skill in the picker?** Send `Use job-search.` If it cannot find the installation, use [Need help?](#if-something-stops-you). A shortcut works only after the app has loaded the installed skill; it does not install it.

If you installed it during the current conversation, start a new conversation in the same project and try the shortcut again. The AI should check the actual installed files if it is still unavailable.

<a name="coming-back-later"></a>

## 6. Coming back later

**a. Reopen** the same project and conversation you used before.

**b. Summon** the skill using your app's option [above](#summon-the-skill), then add:

```text
Continue my job search.
```

**c. Continue** from the saved progress. Answer any new question or review the next result.

You do not normally reinstall or attach the same resume again. Supply a new resume when it changes. If a new conversation cannot find your records, provide the private workspace location from step 4 and say `Resume my existing search at this location; do not start over.` Records on one computer do not automatically appear on another.

For an independent search in a different occupation, use a new project and say `Use job-search for my new occupation.` It creates separate records and asks the relevant questions there. It must not read or reuse another project's private evidence or consent unless you explicitly ask it to copy specified material.

## Your weekday morning search

**a. Review the suggestions.** The AI proposes several suitable job titles and search sites from your experience and location. Keep the suggestions or tell it what to change.

**b. Choose your routine.** It offers **once each weekday at 9 a.m.**, asks your timezone and confirms your preferences. You can choose another time or keep searches manual. It also confirms a morning window so missed searches do not restart at night.

**c. Let the AI set it up.** It saves the daily instructions and creates the supported local scheduled task. In Codex desktop, review it in **Scheduled**. In Claude Code Desktop, review it in **Code → Routines**. If a tool is unavailable, it gives you the next simple action. No technical prompt-writing is required.

**d. Check the first result.** Keep your computer awake and the desktop app running for local searches. The AI tests access and shows what it found or what needs attention. A test run and a real scheduled run are recorded separately.

Each run checks unfinished applications and new listings, avoids duplicates, and prepares suitable drafts within your agreed limits. You still review applications before authorizing submission. If a site or account is unavailable, the AI records the gap and continues useful work where possible.

To change it, say **“Move my daily search to 8 a.m.”**, **“Change my job titles”** or **“Pause my scheduled search.”** The AI updates the existing routine. No reinstall is needed.

**Using only a terminal?** Codex CLI can prepare the routine, but activation needs the desktop scheduling interface. Claude Code's `/loop` is for a running session; use its Desktop local task for this daily workflow. Cloud tasks do not automatically have your local resume and records.

Official scheduling guidance: [Codex / ChatGPT desktop](https://learn.chatgpt.com/docs/automations), [Claude Code Desktop](https://code.claude.com/docs/en/desktop-scheduled-tasks), [Claude Code CLI](https://code.claude.com/docs/en/scheduled-tasks).

## If something stops you

| What happened | What to do |
| --- | --- |
| “I cannot read your resume.” | Attach it again if supported, or supply its actual file location. If still unreadable, paste the resume text when asked. |
| “The skill is not available.” | Send `Check whether job-search is installed in this project and help me load it.` Follow a restart instruction only if needed. |
| The app asks for permission or a missing tool. | Review the request and allow what you want it to do. If you cannot proceed, tell the AI what the message says. |
| It asks questions you already answered. | Say `Read my saved job-search records first.` Supply the saved location if this is a different conversation. |

## What happens automatically?

Once installed and available, the skill instructs the AI to manage setup, saved answers, evidence, job screening, document versions and application records. **Sharing or opening the GitHub link alone does not install or start it**—send the first-time message in the AI app.

The AI still needs your real answers and your app's file, web and document capabilities. It may need approval for access or installation. Accounts, recurring searches and final submissions are not activated by installation. During setup, the AI offers a regular search schedule and confirms your choices before creating it. You can keep searches manual.

<details>
<summary><strong>Optional: install using a terminal</strong></summary>

Use this alternative only if you prefer a terminal. Run it in your chosen job-search project with Node.js 22.20 or newer:

```sh
npx skills@1.5.26 add toughdave/job-search --skill job-search --agent codex claude-code --copy -y
```

This installs project copies for both apps. Then follow [Summon the skill](#summon-the-skill). Installing in one project does not make the skill available in every project.

</details>

<details>
<summary><strong>How this works</strong></summary>

The [installing instructions](../INSTALL.md) are for the AI. The reusable skill is in [skills/job-search](../skills/job-search/SKILL.md). It keeps private records outside the installed skill and public repository. Installation does not alter another candidate's pipeline.

The state helper uses Python 3.9+; document tools may need extra packages or a renderer. The AI checks these and handles supported local setup. Other AI tools need separate capability checks. No hiring outcome is guaranteed.

Official instructions checked for this guide: [Codex skills](https://learn.chatgpt.com/docs/build-skills), [local projects](https://learn.chatgpt.com/docs/projects), [Claude Code desktop setup](https://code.claude.com/docs/en/desktop-quickstart), [Claude Code skills](https://code.claude.com/docs/en/skills), and [GitHub section links](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#section-links). App labels and attachment methods can vary by version.

</details>

## Connect your job-search inbox

After confirming your application email, the AI asks whether you want inbox help. If you agree, it guides you to Gmail in Codex Plugins or Claude Code Connectors. Sign in to the account you want to use. The AI checks the account address and a small job-related search before calling it ready. A different connected account stays blocked until you resolve it. You can decline or continue without email; Calendar is offered separately when useful. [Full connection workflow](../skills/job-search/references/mail.md).
