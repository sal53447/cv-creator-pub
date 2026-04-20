# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build command

```bash
python -m src --company <name> [--theme <name>] [--profile <name>] [--output <file>] [--pdf]
```

| Flag | Default | Purpose |
|------|---------|---------|
| `--company` | `default` | Output folder name — use the company you're applying to |
| `--theme` | same as `--company` | Color theme from `themes/colors/`. Can differ from company if reusing a theme |
| `--profile` | same as `--company` | Content profile under `profiles/` — falls back to `default` for missing files |
| `--output` | `cv.html` | Output filename |
| `--pdf` | off | Also export a PDF via headless Chromium alongside the HTML |

Output is written to `output/{company}/{filename}`.

Example:
```bash
python -m src --company example-company --output cv_example.html --pdf
```

## Architecture

**Data flow:** YAML content + JSON theme configs → Python renderer → self-contained HTML → (optional) PDF via Playwright.

**Three layers of inputs:**

| Layer | Location | Controls |
|-------|----------|---------|
| Content | `profiles/{profile}/data/*.yaml` | Text: name, jobs, skills, projects, etc. |
| Colors | `themes/colors/{theme}.json` | 8 CSS custom properties mapped to CV slots |
| Fonts | `themes/fonts/default.json` | Font family + Google Fonts import URL |

**Profile folder layout:**

```
profiles/{slug}/
├── data/                    ← YAML — machine-readable, what the build reads
│   ├── profile.yaml
│   ├── contact.yaml
│   ├── work_experience.yaml
│   ├── education.yaml
│   ├── projects.yaml
│   └── publications.yaml
├── docs/                    ← Markdown — human-readable reference + persona
│   ├── *.md                 ← YAML mirrors (written by tailoring skills)
│   └── persona.md           ← beliefs/voice/values (default) or overlay (slug)
└── job-description.yaml     ← application metadata (only for tailored profiles)
```

- `data/` is the source of truth for the build. `src/paths.py` resolves `profiles/{slug}/data/{file}` and falls back to `profiles/default/data/{file}` if missing.
- `docs/` holds two kinds of markdown: human-readable mirrors of the YAML (written by tailoring skills), and `persona.md` — the canonical file for the user's beliefs, voice, red lines, and working style. The default persona is at `profiles/default/docs/persona.md`; per-application overlays (section-level, only for company-specific gaps) live at `profiles/{slug}/docs/persona.md`.
- `job-description.yaml` is the dossier written by the `job-describe` skill: role, responsibilities, requirements, keywords, and company research. Used by `cv-talent-advisor` and `cover-letter-coach` as the primary source for tailoring and cover-letter decisions.

**Color theme schema** (`themes/colors/*.json`):
```json
{
  "theme": "name",
  "description": "...",
  "colors": {
    "ink":        "#...",  // primary body text
    "ink-soft":   "#...",  // secondary text
    "muted":      "#...",  // tertiary/metadata
    "rule":       "#...",  // borders
    "bg":         "#...",  // main content background
    "sidebar-bg": "#...",  // left sidebar background
    "page-bg":    "#...",  // outer page background
    "accent":     "#..."   // headings, name, section titles
  }
}
```

**Source modules** (`src/`):
- `paths.py` — `ROOT_DIR`, path helpers, file loaders, `e()` HTML-escape util
- `styles.py` — `build_css()` generating the full CSS string
- `renderers.py` — all `render_*()` functions for sidebar and main area sections
- `pages.py` — `build_page1/2/3()` and `build_html()` assembler

**Layout:** Always exactly 3 A4 pages. Each page has a left `<aside>` (sidebar) and `<main>` column. Page splits are hardcoded in `build_page1/2/3()` — not dynamic.

## Adding a new job application

The `application-create` skill orchestrates the full pipeline (CV + cover letter). Just give it the job ad URL/text and a company slug:

1. **`job-describe`** runs first (blocking requirement) — writes `profiles/{slug}/job-description.yaml` (role, requirements, plus company research from the `job-ad-researcher` subagent). Re-used on subsequent runs unless `refresh` is passed.
2. **Content preparation** (parallel, both depend only on Step 1):
   - **`cv-color-theme`** — extracts brand colors from the company site → `themes/colors/{slug}.json`
   - **`cv-talent-advisor`** — reads the dossier + does narrow candidate-fit research, writes tailored YAML to `profiles/{slug}/data/` and MD mirrors to `profiles/{slug}/docs/`
3. **Artifact materialization** (parallel, both depend only on Step 2):
   - **CV HTML build**: `python -m src --company {slug} --profile {slug} --output cv_{slug}.html` → `output/{slug}/*.html`
   - **`cover-letter-coach`** — reads default persona + default CV + dossier + tailored CV; if the role demands convictions the default persona doesn't cover, invokes `persona-comparison` to write the overlay to `profiles/{slug}/docs/persona.md`; then drafts the cover letter → `output/{slug}/cover_letter.md`
4. Approve both artifacts → export CV PDF.

Manual build (without tailoring) still works: `python -m src --company {slug} --pdf` falls back to `profiles/default/data/` for anything the slug profile doesn't override. The cover letter is only produced via the pipeline or by invoking `cover-letter-coach` directly.

## Skills and agents

**Skills** (`.claude/skills/`):
- `application-create` — full pipeline orchestrator (job-describe → theme + CV tailoring → CV HTML build + cover letter → approve → PDF)
- `job-describe` — captures the job+company dossier to `profiles/{slug}/job-description.yaml` (spawns `job-ad-researcher`)
- `cv-color-theme` — extracts brand colors from a job ad / company site → theme JSON
- `cv-comparison` — standalone CV content tailoring (reads `profiles/default/data/`, writes changed files to `profiles/{slug}/data/` + MD mirrors to `docs/`)
- `persona-comparison` — standalone persona overlay writer (reads `profiles/default/docs/persona.md` + instructions, writes only changed/new sections to `profiles/{slug}/docs/persona.md`)

**Agents** (`.claude/agents/`):
- `cv-talent-advisor` — strategic CV coach; reads `job-description.yaml`, layers candidate-fit research, drives CV tailoring via `cv-comparison`
- `cover-letter-coach` — HR specialist; reads default persona + CV + dossier, identifies persona gaps, writes overlay via `persona-comparison`, drafts the cover letter to `output/{slug}/cover_letter.md`
- `job-ad-researcher` — broad company research (site, news, LinkedIn, Glassdoor, team pages); returns the `research:` block for the dossier
- `cv-html-designer` — HTML/CSS design assistance for the renderer
