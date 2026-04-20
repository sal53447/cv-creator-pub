---
name: cv-color-theme
description: Extract a company's brand colors from a job ad and generate a CV color theme JSON for the cv-creator project. Trigger whenever the user mentions a job ad, job posting, company URL, or wants to create/generate a color theme for a CV. Also trigger on phrases like "color theme", "theme for this job", "match the company colors", "job application color", or when the user pastes a job ad or URL and asks to apply it to their CV.
---

# CV Color Theme Generator

Generate a color theme JSON for the cv-creator project by extracting brand colors from a company's job ad or website.

## Step 1: Get the URL

The user may provide:
- **A direct URL** — use it as-is
- **Job ad text** — scan the text for a URL (company website, LinkedIn, job board link that reveals the company, etc.). Also extract the company name from the text if no URL is present.
- **Just a company name** — search for the company's main website URL

If you can't find any URL and no company name is clear, ask the user: "Could you share the company's website URL or the job ad link?"

## Step 2: Fetch the page and extract brand colors

Use `WebFetch` to load the URL. If the URL is a job board (LinkedIn, Indeed, Stepstone, etc.) rather than the company's own site, also fetch the company's main website — the brand colors live there, not on the job board.

From the fetched HTML/CSS, look for:
- CSS custom properties or variables (e.g. `--primary`, `--brand-color`, `--color-*`)
- Inline styles on prominent elements (header, nav, hero section, buttons)
- `<meta name="theme-color">` or `<meta name="msapplication-TileColor">`
- Logo colors described in SVG `fill` attributes
- Repeated hex codes or rgb() values in `<style>` blocks

Extract 2–4 dominant brand colors. Note whether the brand is light or dark, warm or cool.

## Step 3: Design the theme

Map the brand colors to these 8 CV slots:

| Slot | Purpose | Guidance |
|------|---------|----------|
| `ink` | Primary body text | Very dark — must be readable on white. Use dark brand color or near-black derived from brand hue. |
| `ink-soft` | Secondary text (job titles, dates) | Slightly lighter than ink — same hue family. |
| `muted` | Tertiary / metadata text | Medium gray-ish — readable but recedes. |
| `rule` | Borders and dividers | Light, subtle — same hue family as sidebar-bg. |
| `bg` | Main content area background | White or very light neutral. |
| `sidebar-bg` | Left sidebar background | A tinted light color — this is where brand color shows most. Use a pale tint of the primary brand color. |
| `page-bg` | Outer page background (behind the white sheet) | Slightly darker than sidebar-bg or a complementary neutral. |
| `accent` | Headings, section titles, name | The most saturated / distinctive brand color. Should pop on white. |

**Design principles:**
- The CV must be print-ready and professional — never use garish or hard-to-read colors
- Sidebar-bg should be a soft tint (10–20% saturation) of the brand's primary color, not the full saturated brand color
- If the brand is dark/moody, lighten considerably for sidebar-bg — the user's name and text must remain legible
- When in doubt, derive colors from the brand hue but adjust lightness/saturation for readability

## Step 4: Derive the company name

Extract a clean company name for the filename:
- Lowercase, spaces replaced with hyphens, no special characters
- Examples: `siemens`, `deutsche-bank`, `google`, `bmw-group`

## Step 5: Write the JSON file

Save to `themes/colors/{company-name}.json`:

```json
{
  "theme": "{company-name}",
  "description": "{one-line description of the palette — brand vibe + color names}",
  "colors": {
    "ink":        "#xxxxxx",
    "ink-soft":   "#xxxxxx",
    "muted":      "#xxxxxx",
    "rule":       "#xxxxxx",
    "bg":         "#ffffff",
    "sidebar-bg": "#xxxxxx",
    "page-bg":    "#xxxxxx",
    "accent":     "#xxxxxx"
  }
}
```

## Step 6: Confirm

Tell the user:
- The file path it was saved to
- A brief description of the palette and where each key color came from
- The command to preview: `python build_cv.py --theme {company-name} --output preview.html`
