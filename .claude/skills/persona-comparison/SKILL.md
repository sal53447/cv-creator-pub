---
name: persona-comparison
description: Tailor the default persona (profiles/default/docs/persona.md) for a specific job application by writing only the changed or newly-added sections as an overlay to profiles/{slug}/docs/persona.md. Use this skill whenever a persona needs company-specific gap coverage — for example, when a role requires convictions, framings, or stances the default persona doesn't already express. Trigger on phrases like "write persona overlay for", "tailor persona for", "fill persona gaps for [company]", or when the cover-letter-coach agent needs to persist company-specific persona additions.
---

# Persona Comparison / Overlay Skill

This skill reads the default persona, applies section-level instructions, and writes only the changed or newly-added sections to `profiles/{slug}/docs/persona.md`. It is the persona-layer analog of `cv-comparison` (which does the same for CV YAMLs).

## Fallback convention

Readers of the persona (cover-letter-coach, future tooling) check the slug's overlay at `profiles/{slug}/docs/persona.md` first for each section heading, then fall back to `profiles/default/docs/persona.md` for anything missing. The overlay is **section-level**: a file-level fallback would re-duplicate the default; sections not in the overlay silently resolve from default.

## Inputs

- **Default persona** — `profiles/default/docs/persona.md` (prose with numbered H2 sections — `## 1. How I think about AI`, etc.)
- **Company slug** — lowercase hyphenated, e.g. `agora-energiewende`
- **Instructions** — section-level directives from the caller (typically `cover-letter-coach`). Each instruction names a section heading and is one of:
  - **Extend** — *"Extend section X with additional content Y."* The overlay section will contain the combined result (default content + addition, merged into coherent prose).
  - **Override** — *"Replace section X with Y."* The overlay section contains only the new content.
  - **New section** — *"Create new section 'Z' with content W."* The overlay adds a heading not present in the default.

## Workflow

### Step 1 — Read the default persona

Read `profiles/default/docs/persona.md` and list its current H2 headings. These are the anchors any Extend / Override instruction must match exactly.

### Step 2 — Apply instructions

For each instruction, produce the final overlay content for that section:

- **Extend** → combine default + addition into coherent first-person prose. The output is the *combined section*, not just the delta. (This keeps downstream readers simple: they never have to merge.)
- **Override** → output contains only the replacement content.
- **New section** → output is entirely new.

Keep the same H2 heading structure, numbering, and first-person voice as the default.

### Step 3 — Write overlay

Write `profiles/{slug}/docs/persona.md` with:

1. A 1-paragraph preamble noting this is a company-specific overlay:
   > *This is a company-specific persona overlay of `profiles/default/docs/persona.md`. Sections present here override or extend the default with the same heading. Any section not present here falls back to the default.*
2. Only the sections that were extended, overridden, or newly created. **Do not include unchanged sections** — that's what fallback is for.

If the caller's instructions result in zero actual changes, **do not write the file**. Report "no overlay needed" back to the caller.

### Step 4 — Report

Tell the caller:
- File path written (or "no overlay written" if no changes)
- For each section in the overlay, which kind of change it is (extend / override / new) and a 1-line rationale

## Quality guidelines

- **Preserve voice** — first-person, layered-reasoning, no tech-bro language. Respect the anti-persona in section 10 of the default.
- **No duplication** — unchanged sections must be absent from the overlay file.
- **Additive, not redundant** — when extending, produce the combined result so downstream readers don't have to merge.
- **No fabrication** — only persist beliefs the user would actually hold. Do not invent convictions. If an instruction feels forced or off-voice, push back to the caller instead of writing it.
- **Keep it prose** — overlays are markdown prose in the same shape as the default, not YAML, not bullet lists (unless the default section itself uses bullets).
