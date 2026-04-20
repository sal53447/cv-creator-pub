---
name: application-create
description: Full end-to-end application workflow for a new job — produces a tailored CV (HTML + PDF) and a cover letter in one pipeline. Orchestrates job/company dossier research, color theme extraction, CV content tailoring, persona overlay, cover letter drafting, approval, and PDF export. Trigger whenever the user wants to apply for a job, create a CV and/or cover letter for a company, start a new application, or says things like "I want to apply to X", "create an application for [company]", "make a CV and cover letter for this job", or pastes a job ad URL and wants a complete application package. This skill runs the full pipeline — don't just answer with steps, invoke this skill and do the work.
---

# Application Create — Full Application Workflow

This skill produces the complete application package for a new job:

**job dossier** → **(color theme + CV tailoring in parallel)** → **(CV HTML build + cover letter in parallel)** → **approval** → **PDF**.

## Step 1 — Gather inputs

You need two things:
- **Job ad URL** — posting or company website (used for dossier and color extraction)
- **Company slug** — lowercase hyphenated name (e.g. `agora-energiewende`, `siemens-energy`)

If the user didn't provide both, ask once. Derive the slug from the URL or company name if obvious — don't ask unnecessarily.

## Step 2 — Requirement: job + company dossier

Invoke the `job-describe` skill with the URL and slug:
> Research the job ad at `{job_ad_url}` and the company behind it, then write a comprehensive dossier to `profiles/{slug}/job-description.yaml`.

This file is the **primary source** consumed by both downstream agents in Step 4. It must exist before Step 3 runs.

**Refresh semantics:**
- **Default** — if `profiles/{slug}/job-description.yaml` already exists, re-use it and skip this step.
- **Refresh** — if the user says "refresh", "re-research", "regenerate the job description", or passes a refresh flag, run `job-describe` again and overwrite.

If the dossier is missing after this step (skill failed, wrong path), **stop the pipeline and surface the error** — do not let later steps silently fall back to reading the URL directly.

## Step 3 — Parallel content preparation

Spawn both in the same turn so they run simultaneously. Both depend only on Step 2's dossier; they do not depend on each other.

**Agent 1 — Color theme** (skill: `cv-color-theme` at `.claude/skills/cv-color-theme/`):
> Extract brand colors from `{job_ad_url}` for company `{slug}` and write the theme JSON to `themes/colors/{slug}.json`.

**Agent 2 — CV content tailoring** (agent: `cv-talent-advisor`):
> For company `{slug}`, read `profiles/{slug}/job-description.yaml` as your primary source, run any targeted candidate-fit research you need on top of it, apply content changes to the profile, and write only the modified YAML files to `profiles/{slug}/data/`. For each YAML file written, also write a human-readable `.md` mirror to `profiles/{slug}/docs/`. Report which files you wrote and a summary of changes.

Both must complete before Step 4.

## Step 4 — Parallel artifact materialization

Once Step 3 is done, spawn two actions in parallel. Both depend on Step 3's outputs but not on each other.

**Action A — Build CV HTML** (deterministic shell command):
```bash
python -m src --company {slug} --profile {slug} --output cv_{slug}.html
```
Produces `output/{slug}/cv_{slug}.html`.

If the build fails (missing theme, YAML error), diagnose and fix before continuing.

**Action B — Cover letter + persona overlay** (agent: `cover-letter-coach`):
> For company `{slug}`, read the default persona (`profiles/default/docs/persona.md`), default CV YAMLs, `profiles/{slug}/job-description.yaml`, and tailored CV YAMLs in `profiles/{slug}/data/` if they exist. Run gap analysis: if the role requires convictions or framings the default persona does not already express, invoke the `persona-comparison` skill to write the overlay to `profiles/{slug}/docs/persona.md`. Then draft the cover letter and write it to `output/{slug}/cover_letter.md`. Report which persona sections were overlaid (if any), the cover letter path, and the lead angle.

Both must complete before Step 5. Neither blocks the other.

## Step 5 — Ask for approval on both artifacts

Tell the user:
> "HTML CV at `output/{slug}/cv_{slug}.html`. Cover letter at `output/{slug}/cover_letter.md`. Open both and let me know if they look good — I'll generate the CV PDF once you approve."

Try to open the CV HTML in the browser:
```bash
xdg-open output/{slug}/cv_{slug}.html 2>/dev/null || true
```

Wait for the user's response. Address feedback before asking again:
- **CV content changes** → re-run `cv-talent-advisor` → re-build HTML
- **Cover letter changes** → re-run `cover-letter-coach` (or edit directly for small tweaks)
- **Color changes** → edit `themes/colors/{slug}.json` → re-build HTML
- **Persona overlay changes** → re-run `cover-letter-coach`, which rewrites both overlay and letter

## Step 6 — Generate CV PDF

Once approved, run:
```bash
python -m src --company {slug} --output cv_{slug}.html --pdf
```

Report final paths:
- **CV PDF**: `output/{slug}/cv_{slug}.pdf`
- **CV HTML**: `output/{slug}/cv_{slug}.html`
- **Cover letter**: `output/{slug}/cover_letter.md`

## Notes

- `cv-talent-advisor` writes only **changed** YAML files to `profiles/{slug}/data/`; unchanged files fall back to `profiles/default/data/` via `src/paths.py`.
- `cover-letter-coach` writes the persona overlay only if genuine gaps exist. If the default persona already covers the role, no overlay file is created — the default is used as-is downstream.
- If a color theme for this company already exists, skip Agent 1 in Step 3 and confirm with the user.
- If a profile folder for this company already exists with content, ask whether to overwrite or keep it.
- Cover letter is markdown for now. PDF export for the cover letter is not part of this pipeline yet — follow-up if requested.
