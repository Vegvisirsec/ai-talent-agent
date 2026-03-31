# ai-talent-agent

```text
    _    ___   _____       _            _                        _
   / \  |_ _| |_   _|__ _ | | ___ _ __ | |_    __ _  __ _  ___ _ __ | |_
  / _ \  | |    | |/ _ \ || |/ _ \ '_ \| __|  / _` |/ _` |/ _ \ '_ \| __|
 / ___ \ | |    | |  __/ || |  __/ | | | |_  | (_| | (_| |  __/ | | | |_
/_/   \_\___|   |_|\___|\__/ \___|_| |_|\__|  \__,_|\__, |\___|_| |_|\__|
                                                    |___/
```

`ai-talent-agent` is a small two-agent workflow for tailoring resumes/CVs for roles that may be screened by:

- applicant tracking systems (ATS)
- AI screening or ranking systems
- recruiter search and autofill systems
- human recruiters and hiring managers

## Why This Exists

Many resumes fail before a human ever evaluates the real substance of the candidate.

That usually happens for boring reasons rather than dramatic ones:

- the resume does not use the exact title wording recruiters search for
- relevant keywords are missing or hidden behind synonyms
- employer, title, and dates are formatted in ways that parsing systems misread
- the layout looks polished but breaks autofill, extraction, or search visibility
- the resume is written like a biography instead of a role-matching document

This repo exists to solve that problem:

The working assumptions behind the tool are:

- discoverability matters, so exact target-title wording near the top matters
- parseability matters, so structure usually beats visuals
- recruiters and automated systems often reward literal alignment more than clever phrasing
- many job descriptions are wish lists, so a second evaluation pass should separate true blockers from inflated requirements
- truthful positioning is stronger than generic wording, but weaker than dishonest exaggeration

In short: this repo is for producing resumes that survive automated screening, remain readable to humans, and stay defensible in interview.

The core idea is simple:

- one agent tailors the CV for a specific role
- one agent evaluates the result like a recruiter or talent acquisition partner

The goal is not to create a flashy resume. The goal is to create a CV that is:

- extremely parseable by ATS and other automated systems
- clearly aligned to a target role
- polished enough for a human reviewer
- honest and interview-defensible

## Repo Contents

- `instructions.md`
  Lightweight entry point for the two-agent workflow
- `talent_agent_instructions.md`
  Rules for tailoring a CV toward a specific role
- `talent_acquisition_agent_instructions.md`
  Rules for evaluating the tailored CV from a recruiter-side perspective
- `render_cv.py`
  Converts a finished Markdown CV into HTML
- `render_cv_docx_pdf.py`
  Converts a finished Markdown CV into DOCX and/or PDF using optional Python libraries
- `deanonymize_cv.py`
  Replaces placeholder tokens such as `{{FULL_NAME}}` with local values from a JSON file
- `examples/sample_cv.md`
  Generic baseline CV example
- `examples/sample_tailored_role.md`
  Generic tailored CV example
- `examples/personal_profile_template.json`
  Generic token-value template for de-anonymizing example CVs locally

## How It Works

### 1. Talent Agent

The talent agent:

- reads the target role
- identifies the most relevant truthful positioning
- tailors the summary, core competencies, and experience ordering
- compresses or drops lower-value material when that improves the role-specific version
- improves keyword alignment without keyword stuffing
- highlights important missing or under-signaled areas for later review
- keeps claims honest and defensible

The tailored `Core Competencies` section should be selective and role-specific rather than a full inventory of everything the candidate can plausibly do.

The talent agent must not invent history, titles, scope, achievements, or direct experience that cannot be justified.

### 2. Talent Acquisition Agent

The talent acquisition agent:

- reviews the tailored CV like a recruiter or headhunter
- checks whether the top of the CV is clear and credible
- distinguishes `strict listing fit` from `practical hiring fit`
- flags inflated or risky wording
- provides expected compensation-range insight

This is important because many job descriptions are wish lists. A good review should separate:

- real blockers
- preferred extras
- likely wishlist inflation
- skills that can realistically be learned on the job

## Formatting Philosophy

This repo prefers:

- simple single-column structure
- explicit fields that ATS can parse cleanly
- conventional section names
- plain text over decorative layout
- human readability without sacrificing extraction quality

When there is a tradeoff between visual elegance and parseability, parseability wins.

Good default choices:

- `Employer`, `Title`, and `Duration` labels in work history
- standard section headings like `Professional Summary`, `Work Experience`, `Education`, `Certifications`, and `Skills`
- natural role keywords taken from the posting
- no tables, text boxes, icons, or multi-column layouts

For ATS-first versions, a photo is usually not recommended.

## Privacy-Preserving Workflow

The intended workflow is:

1. Start from an anonymized or partially anonymized Markdown CV.
2. Use the talent-agent instructions to create a tailored version for a target role.
3. Use the talent-acquisition-agent instructions to evaluate the result.
4. Iterate on the anonymized version until the structure, wording, and positioning are strong.
5. After that, fill in the real private details locally:
   company names
   personal links
   exact location
   contact information
   any sensitive context you do not want in prompts
6. Render the final local Markdown file to HTML if needed.

Storage rule:

- Treat anonymized files as private too. Even anonymized derivatives should stay local and should not be committed.
- If you are comfortable with repo-local ignored files, you can keep anonymized working materials under `private/`.
- Prefer a subdirectory per role or workstream, for example `private/company_role/`, instead of placing generated files directly in `private/`.
- Prefer keeping real personal data files and de-anonymized final outputs outside the repo entirely.
- Real personal data includes contact details, real employer names, real education names, and any de-anonymized final CV variants.

This keeps the reusable reasoning and structure in the repo while letting the most sensitive files stay fully outside the repo when preferred.

## Recommended Way To Use This Repo

### End-To-End Example

Example workspace layout:

```text
<private-workspace>/
  personal_profile.json
  company_role/
    role.md
    source_cv.md
    tailored_cv.md
    acquisition_agent_run.md
    role_signals.md
```

Example end-to-end flow:

1. Create an anonymized source CV from [examples/sample_cv.md](examples/sample_cv.md) and save it as `<private-workspace>/company_role/source_cv.md`.
2. Save the job description as `<private-workspace>/company_role/role.md`.
3. Use the `Talent Agent` instructions to produce `tailored_cv.md`.
4. Use the `Talent Acquisition Agent` instructions to produce `acquisition_agent_run.md` and `role_signals.md`.
5. De-anonymize the tailored CV with your real local data file.
6. Render the final Markdown to HTML, DOCX, or PDF.

Example agent inputs:

```text
Talent Agent
- instructions file: talent_agent_instructions.md
- source CV: <private-workspace>/company_role/source_cv.md
- target role: <private-workspace>/company_role/role.md
- expected output: <private-workspace>/company_role/tailored_cv.md

Talent Acquisition Agent
- instructions file: talent_acquisition_agent_instructions.md
- tailored CV: <private-workspace>/company_role/tailored_cv.md
- target role: <private-workspace>/company_role/role.md
- expected outputs:
  - <private-workspace>/company_role/acquisition_agent_run.md
  - <private-workspace>/company_role/role_signals.md
```

Example de-anonymization command:

```powershell
python .\deanonymize_cv.py --path "<private-workspace>/company_role/tailored_cv.md" --data "<private-workspace>/personal_profile.json" --output "<private-workspace>/company_role/tailored_cv.final.md" --strict
```

Example render commands:

```powershell
python .\render_cv.py --path "<private-workspace>/company_role/tailored_cv.final.md"
python .\render_cv_docx_pdf.py --path "<private-workspace>/company_role/tailored_cv.final.md" --both
python .\render_cv_docx_pdf.py --path "<private-workspace>/company_role/tailored_cv.final.md" --pdf --theme dark
```

### Step 1: Prepare a source CV

Create a local Markdown CV based on `examples/sample_cv.md`.

Recommended approach:

- keep the structure
- replace the content with your own background
- anonymize employer names if needed during drafting
- leave placeholders where you want to fill in private details later
- keep the anonymized file either under `private/` or in another local-only folder outside the repo

### Step 2: Tailor it

Use `talent_agent_instructions.md` against:

- your anonymized source CV
- the target job description

The tailored version should:

- move the strongest matching evidence upward
- reshape the `Core Competencies` / `Skills` section around the target role
- reflect the employer's wording when truthful
- strengthen positioning without crossing into fiction

For the competencies section, prefer a few stronger role-shaped clusters over a long generic list. Bring the most relevant themes to the top and drop lower-value categories that do not materially help with this specific role.

### Step 3: Evaluate it

Use `talent_acquisition_agent_instructions.md` to review the tailored CV.

Keep the tailored CV, the copied job description, and the review output together in a local-only role-specific folder. This can be under `private/` or outside the repo.

Also keep a local role-signals or keyword-notes file in that same role-specific folder so repeated themes can later be reviewed when improving the baseline CV.

That local notes file should also capture important things that may be missing from the current CV or present only weakly, so they can be checked later against real past experience before updating the baseline CV.

The evaluation should cover:

- recruiter readability
- ATS keyword coverage
- strict listing fit
- practical hiring fit
- credibility risks
- likely compensation range

### Step 4: Fill in the blanks locally

Once the structure and wording are solid, fill in:

- real employer names
- real LinkedIn and GitHub links
- real contact details
- any other private identifiers

This step should happen after the generic reasoning and tailoring work is already done.
Prefer keeping the completed de-anonymized version outside the repo entirely.

### Step 4.5: De-anonymize Outside The Repo

Use the token-replacement script with files outside the repo whenever possible:

```powershell
python .\deanonymize_cv.py --path "<private-workspace>/company_role/tailored_cv.md" --data "<private-workspace>/personal_profile.json" --output "<private-workspace>/company_role/tailored_cv.final.md" --strict
python .\deanonymize_cv.py --path ".\examples\sample_tailored_role.md" --data ".\examples\personal_profile_template.json" --output ".\examples\sample_tailored_role.final.md"
```

This lets you:

- keep anonymized working files in the repo if that is convenient
- keep real personal data outside the repo
- keep final de-anonymized outputs outside the repo

### Step 5: Render to HTML

Render the finished Markdown file with:

```powershell
python .\render_cv.py --path .\your_cv.md
python .\render_cv.py --path .\your_cv.md --portrait "<portrait-image>"
python .\render_cv.py --path ".\examples\sample_tailored_role.md" --output ".\examples\sample_tailored_role.html"
```

The renderer supports:

- a clean HTML output from Markdown
- optional portrait embedding when `portrait.png` exists next to the target Markdown file, or when passed explicitly with `--portrait`
- a best-effort 1.5 MB output target by compressing the portrait when needed
- the current HTML renderer uses a dark-styled on-screen theme and switches to a cleaner print style when printed

### Step 6: Render to DOCX or PDF

Render the finished Markdown file to Word or PDF with:

```powershell
python .\render_cv_docx_pdf.py --path .\your_cv.md --both
python .\render_cv_docx_pdf.py --path .\your_cv.md --both --portrait "<portrait-image>"
python .\render_cv_docx_pdf.py --path ".\examples\sample_tailored_role.md" --docx
```

Or generate just one format:

```powershell
python .\render_cv_docx_pdf.py --path .\your_cv.md --docx
python .\render_cv_docx_pdf.py --path .\your_cv.md --pdf
```

For a more human-facing dark PDF render:

```powershell
python .\render_cv_docx_pdf.py --path .\your_cv.md --pdf --theme dark
python .\render_cv_docx_pdf.py --path ".\examples\sample_tailored_role.md" --pdf --theme dark
```

The DOCX/PDF renderer supports:

- automatic portrait embedding when `portrait.png` exists next to the target Markdown file
- optional explicit portrait path via `--portrait`
- optional `--theme light` or `--theme dark`
- a best-effort 1.5 MB output target for DOCX and PDF by compressing the portrait when needed
- conservative DOCX styling for compatibility
- a more polished dark PDF option for human-facing sharing

Suggested usage:

- use the normal light render for ATS-safe and recruiter-system-friendly submissions
- use the dark PDF render only for human-facing sharing where presentation matters more than strict ATS conventions

Dependencies:

- `.docx` export requires `python-docx`
- `.pdf` export requires `reportlab`
- portrait compression for output-size control benefits from `Pillow`

Install them with:

```powershell
pip install python-docx reportlab Pillow
```

## Notes On Examples

The examples in this repo are intentionally generic.

They are meant to show:

- structure
- tone
- parseable formatting
- the difference between a baseline CV and a tailored CV
- a token-based approach for filling in personal details locally

They are not meant to represent a real person, real employer, or real job target.

The example CVs use tokens such as `{{FULL_NAME}}` and `{{EMAIL}}` so the public examples stay generic while local workflows can replace those fields with real values.
That same token approach can also be used for one-line employer context notes such as `{{EMPLOYER_1_DESC}}` when local company names need extra explanation for international readers.

Any workflow for collecting keywords, role signals, or expansion ideas from real job listings should stay local under `private/` or in another local-only folder rather than in version-controlled examples.

## Publishing Guidance

If you publish a repo based on this workflow:

- keep only generic examples in version control
- keep anonymized working files under ignored paths if needed
- keep real personal-data files and final de-anonymized CV variants outside the repo entirely when possible
- review commit history before publishing
- do not commit real tailored resumes even temporarily

The included `.gitignore` already excludes common local-only artifacts such as:

- generated HTML files
- `private/`
- local portrait files

## License / Reuse

Adapt the instructions, examples, and renderer to your own workflow.
The main value of the repo is the process:

- tailor honestly
- optimize for parseability
- pressure-test with a recruiter lens
- only fill in private details after the structure is right


