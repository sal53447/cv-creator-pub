---
name: job-describe
description: Capture a structured description of a job application by fetching the job ad, extracting role/responsibilities/requirements/keywords, and enriching it with company research. Writes the combined result to profiles/{slug}/job-description.yaml as application metadata. Trigger on phrases like "describe this job", "create job description", "analyze this job ad", "generate job description yaml", "capture this job posting", "research this role", or when the user provides a job ad URL/text plus a company slug and wants it summarized into the project profile. Pass `refresh` as the argument to regenerate an existing file; otherwise the skill reuses what is already on disk.
---

# Job Describe — Structured Job Ad + Company Research

This skill produces `profiles/{slug}/job-description.yaml` — a single file that captures everything we know about a specific job application. It combines two sources:

1. **The job ad itself** (URL or pasted text) — role, responsibilities, requirements, keywords.
2. **Company research** — mission, values, recent initiatives, culture, and alignment angles. This is delegated to the `job-ad-researcher` subagent defined in `.claude/agents/job-ad-researcher.md`.

The resulting YAML is application metadata that lives **directly under the slug folder**, peer to `data/` and `docs/` — NOT inside them. Downstream skills (`cv-comparison`, `application-create`) can read this file to tailor content.

## Step 1 — Gather inputs and check for existing file

You need:
- **Company slug** (e.g. `agora-energiewende`) — lowercase, hyphenated, used as the folder name
- **Job ad source** — either a URL or pasted job ad text

If either is missing, ask once. Derive the slug from the URL or company name if obvious.

**Before doing any work, check if `profiles/{slug}/job-description.yaml` already exists:**

- If it exists AND the user did NOT pass `refresh` (or explicitly ask to regenerate): read it, report that it is already in place, and stop. Do not re-run the research.
- If it exists AND the user passed `refresh` or said "refresh this", "regenerate", "redo the research": overwrite it.
- If it does not exist: proceed to Step 2.

## Step 2 — Extract ad-derived data yourself

From the URL or pasted text, extract:

- **URL input** → use WebFetch to retrieve the page, then parse the text content.
- **Pasted text** → parse directly, no fetch needed.

Pull out:

- `role.title`, `role.seniority` (if stated), `role.location`, `role.work_model` (Remote/Hybrid/On-site), `role.employment_type` (full-time/part-time/contract), `role.language` (working language if stated)
- `summary` — one paragraph distilling what the role is about
- `responsibilities` — bullet list, verbatim or lightly rephrased
- `requirements.must_have` — hard requirements ("must", "required", "X+ years of")
- `requirements.nice_to_have` — soft/plus-if requirements
- `keywords` — ATS-style terms: tools, frameworks, domains, certifications, methodologies

Omit any field you cannot determine from the ad — do not leave `""` placeholders.

## Step 3 — Spawn the job-ad-researcher subagent for company research

Spawn the project agent `job-ad-researcher` (defined in `.claude/agents/job-ad-researcher.md`) with this brief:

> Research the company `{company name}` (website: `{company_website_url}`) for a CV application. Return a YAML block matching exactly the `research:` schema from the job-describe skill — keys: `company_overview`, `mission`, `values`, `products_or_focus_areas`, `recent_initiatives`, `culture_signals`, `alignment_angles`, `sources`. Keep it roughly 5–10 minutes of work. Focus on what a candidate (the user — background in AI, data engineering, digital transformation, responsible-AI work, organizational change) would want to know to tailor a CV and cover letter. Return only the YAML, no prose wrapper.

Derive the `{company_website_url}` from the job ad URL's domain, or from the company name via a quick search if the ad is pasted text.

## Step 4 — Merge and write the YAML

Combine your ad-derived data (meta, role, summary, responsibilities, requirements, keywords) with the subagent's YAML output (paste it into the `research:` block). Use today's date (from the environment context) for `meta.captured_at`.

Write to `profiles/{slug}/job-description.yaml` using this schema (top-level keys are fixed; sub-keys under `research` may adapt as the researcher sees fit, but keep the canonical ones):

```yaml
meta:
  company: "..."
  slug: "..."
  captured_at: "YYYY-MM-DD"
  source_url: "..."

role:
  title: "..."
  seniority: "..."               # optional
  location: "..."
  work_model: "..."              # Remote / Hybrid / On-site
  employment_type: "..."         # optional
  language: "..."                # optional

summary: |
  One-paragraph distillation of what the role is about.

responsibilities:
  - "..."

requirements:
  must_have:
    - "..."
  nice_to_have:
    - "..."

keywords:
  - "..."

research:
  company_overview: |
    ...
  mission: "..."
  values:
    - "..."
  products_or_focus_areas:
    - "..."
  recent_initiatives:
    - "..."
  culture_signals:
    - "..."
  alignment_angles:
    - "..."
  sources:
    - "..."

notes: |
  # Free-form. Usually empty.
```

Rules:
- Skip any field you cannot determine — do not emit empty strings as placeholders.
- `meta.captured_at` uses today's date in `YYYY-MM-DD` format.
- `meta.source_url` is the original job ad URL, or omit if only pasted text was provided.
- Preserve the indentation and key order above so the file is easy to diff across applications.

## Step 5 — Report

Tell the user:
- Path written: `profiles/{slug}/job-description.yaml`
- A 2–3 line digest: role title, key must-haves, and the strongest 1–2 `alignment_angles` the researcher surfaced.
- Suggest the natural next step:
  > "Ready to tailor the CV? Run the `cv-comparison` skill or the full `application-create` pipeline for `{slug}` — both can now read this job-description.yaml."

## Notes

- The `refresh` argument is the only way to regenerate an existing file. This avoids wasting time re-researching the same company.
- If the researcher subagent returns malformed YAML or is missing required keys, fix it manually (remove the bad key or re-prompt the subagent once) rather than writing broken YAML to disk.
- Do not write the researcher's output anywhere other than the `research:` block of the target file — no stray scratch files.
- `job-description.yaml` sits at `profiles/{slug}/` level — sibling to `data/` and `docs/`. Do not nest it under either.
