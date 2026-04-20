---
name: cv-comparison
description: Tailor the default CV profile for a specific job application by applying targeted instructions to profile sections, then saving only the modified YAML files to profiles/{company}/. Use this skill whenever the user wants to customize their CV for a company, tailor sections of their profile, adapt their CV content for a job ad, or update specific sections (summary, jobs, projects, skills) for a new application. Trigger on phrases like "tailor my CV for", "customize for this job", "adapt my profile for", "update my CV for [company]", or when the user pastes a job description and wants their profile adjusted.
---

# CV Comparison / Tailoring Skill

This skill reads the default profile, applies user-specified modifications to individual sections, and saves only the changed YAML files to `profiles/{company}/data/`. The build system falls back to `profiles/default/data/` for any file not present in the company folder.

## Profile files (all in `profiles/default/data/`)

| File | Contains |
|------|----------|
| `profile.yaml` | name, title, tagline, summary |
| `contact.yaml` | phone, email, location, languages, skills |
| `work_experience.yaml` | jobs (title, company, dates, bullets) |
| `education.yaml` | degrees, certifications |
| `projects.yaml` | tiers of projects with bullets |
| `publications.yaml` | publications, volunteer, hobbies |

## Workflow

### Step 1 — Gather inputs

If not already provided, ask:
- **Company name** (used as folder name, e.g. `siemens-energy`)
- **Instructions** — what to change and why (e.g. "emphasize climate/energy projects, shorten the summary, remove unrelated freelance bullets")

You can also accept a job ad text or URL as input and derive the instructions yourself.

### Step 2 — Read and modify

1. Read only the YAML files relevant to the requested changes.
2. Apply the instructions thoughtfully — don't just delete things, reorder and reframe where useful.
3. Keep the YAML structure identical (same keys, same nesting). Only content values should change.
4. Preserve all entries the user didn't ask to change.

### Step 3 — Diff and save

For each YAML file you modified:
1. Compare the modified content against the original default.
2. If the content differs (even slightly):
   - Write the YAML file to `profiles/{company}/data/{filename}`.
   - Write a human-readable `.md` mirror to `profiles/{company}/docs/{basename}.md` (same base name, `.md` extension). The markdown mirror should present the same content in readable prose or structured markdown — not raw YAML.
3. If it's unchanged, **do not write it** — the build will fall back to default automatically.

Write YAML files with clean YAML using proper indentation. Do not add extra comments or metadata.

### Step 4 — Report

Tell the user:
- Which files were written to `profiles/{company}/data/` and `profiles/{company}/docs/`
- A brief summary of each change made
- The build command to try it:
  ```bash
  python build_cv.py --company {company} --profile {company} --output cv_{company}.html --pdf
  ```

## Fallback behavior

`src/paths.py` is already patched: if a file doesn't exist in `profiles/{company}/data/`, it automatically loads from `profiles/default/data/`. So a company profile can contain as few as one modified file.

## Quality guidelines

- **Relevance over volume** — fewer, stronger bullets beat many weak ones.
- **Match the job** — if the role is technical, surface technical achievements; if strategic, lead with impact.
- **Don't invent facts** — only rephrase, reorder, or omit existing content.
- **Preserve voice** — keep the user's first-person-implied, direct writing style.
