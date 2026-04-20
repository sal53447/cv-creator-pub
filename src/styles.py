def build_css(theme: str, colors: dict, font_family: str) -> str:
    color_vars = "\n".join(
        f"  --{name}: {value};" for name, value in colors.items()
    )

    return f"""\
[data-theme="{theme}"] {{
{color_vars}
}}

*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

body {{
  font-family: '{font_family}', sans-serif;
  font-size: 9.0pt;
  font-weight: 400;
  line-height: 1.38;
  color: var(--ink);
  background: var(--page-bg);
}}

.page-wrapper {{
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 16mm 0;
  gap: 12mm;
}}

section.page {{
  width: 210mm;
  height: 297mm;
  max-height: 297mm;
  background: var(--bg);
  display: flex;
  flex-direction: row;
  box-shadow: 0 2px 16px rgba(15,29,46,0.13);
  overflow: hidden;
  position: relative;
}}

aside {{
  width: 68mm;
  min-width: 68mm;
  height: 100%;
  background: var(--sidebar-bg);
  padding: 7mm 5.5mm;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}}


main {{
  flex: 1;
  height: 100%;
  padding: 7mm 7mm 7mm 6.5mm;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}}

.sidebar-heading {{
  font-family: 'Merriweather', serif;
  font-size: 8.8pt;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--accent);
  border-bottom: 1.5px solid var(--accent);
  padding-bottom: 1.5px;
  margin-bottom: 3px;
  margin-top: 5mm;
}}
.sidebar-heading:first-child {{ margin-top: 0; }}

.contact-row {{ font-size: 7.8pt; color: var(--ink-soft); margin-bottom: 2px; }}
.contact-row span.label {{ font-size: 6.9pt; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; color: var(--muted); display: block; }}
.relocation {{ font-size: 7.3pt; font-style: italic; color: var(--muted); margin-top: 2px; }}

.lang-item {{ font-size: 7.8pt; color: var(--ink-soft); margin-bottom: 1px; }}

.skill-group {{ margin-bottom: 3px; }}
.skill-group-label {{ font-size: 7.3pt; font-weight: 700; color: var(--ink); }}
.skill-group-body {{ font-size: 7.3pt; color: var(--ink-soft); line-height: 1.35; }}

.edu-entry {{ margin-bottom: 5px; }}
.edu-degree {{ font-family: 'Merriweather', serif; font-size: 7.8pt; font-weight: 700; color: var(--ink); }}
.edu-field {{ font-size: 7.8pt; font-weight: 600; color: var(--ink-soft); }}
.edu-meta {{ font-size: 7.3pt; color: var(--muted); }}
.edu-note {{ font-size: 7.3pt; color: var(--ink-soft); line-height: 1.3; margin-top: 2px; }}

.cert-entry {{ margin-bottom: 4px; }}
.cert-name {{ font-family: 'Merriweather', serif; font-size: 7.8pt; font-weight: 700; color: var(--ink); }}
.cert-inst {{ font-size: 7.3pt; color: var(--muted); }}

.pub-entry {{ margin-bottom: 5px; }}
.pub-title {{ font-family: 'Merriweather', serif; font-size: 7.3pt; font-weight: 600; color: var(--ink); line-height: 1.3; }}
.pub-venue {{ font-size: 7.3pt; color: var(--muted); }}
.pub-url {{ font-size: 6.9pt; color: var(--ink-soft); word-break: break-all; }}
.pub-desc {{ font-size: 7.3pt; color: var(--ink-soft); line-height: 1.3; }}

.volunteer-text {{ font-size: 7.8pt; color: var(--ink-soft); line-height: 1.35; }}
.hobby-item {{ font-size: 7.8pt; color: var(--ink-soft); margin-bottom: 1px; }}

/* Main area */
.cv-name {{ font-family: 'Merriweather', serif; font-size: 23.1pt; font-weight: 800; color: var(--ink); letter-spacing: 0.01em; line-height: 1; margin-bottom: 2px; }}
.cv-title {{ font-family: 'Merriweather', serif; font-size: 10.5pt; font-weight: 600; color: var(--ink); margin-bottom: 2px; }}
.cv-tagline {{ font-size: 7.8pt; font-weight: 400; font-style: italic; color: var(--muted); line-height: 1.4; }}
.cv-header {{ padding-bottom: 5px; border-bottom: 1.5px solid var(--rule); margin-bottom: 6px; }}

.section-heading {{
  font-family: 'Merriweather', serif;
  font-size: 8.4pt;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--ink);
  border-bottom: 1.5px solid var(--ink);
  padding-bottom: 2px;
  margin-bottom: 4px;
  margin-top: 6px;
}}
.section-heading:first-child {{ margin-top: 0; }}

.profile-text {{ font-size: 7.8pt; color: var(--ink-soft); line-height: 1.4; }}

.job {{ padding-left: 10px; margin-bottom: 6px; position: relative; }}
.job::before {{ content: ''; position: absolute; left: 0; top: 4px; width: 5px; height: 5px; border-radius: 50%; background: var(--bg); border: 1.5px solid var(--ink); }}
.job-header {{ display: flex; justify-content: space-between; align-items: baseline; gap: 8px; }}
.job-title {{ font-family: 'Merriweather', serif; font-size: 9.0pt; font-weight: 700; color: var(--ink); }}
.job-date {{ font-size: 7.3pt; font-style: italic; color: var(--muted); white-space: nowrap; }}
.job-company {{ font-size: 7.8pt; color: var(--ink-soft); margin-bottom: 2px; }}
.job-loc {{ font-size: 7.3pt; color: var(--muted); margin-left: 6px; }}
.job-bullets {{ padding-left: 10px; margin: 1px 0 0 0; }}
.job-bullets li {{ font-size: 7.8pt; color: var(--ink-soft); line-height: 1.38; margin-bottom: 1px; }}

.tier-label {{ font-size: 7.3pt; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; color: var(--muted); border-bottom: 1px dashed var(--rule); padding-bottom: 2px; margin: 5px 0 3px 0; }}
.project {{ padding-left: 10px; margin-bottom: 4px; position: relative; }}
.project::before {{ content: ''; position: absolute; left: 0; top: 4px; width: 5px; height: 5px; border-radius: 50%; background: var(--bg); border: 1.5px solid var(--ink); }}
.project-name {{ font-family: 'Merriweather', serif; font-size: 8.4pt; font-weight: 700; color: var(--ink); }}
.project-note {{ font-size: 7.8pt; font-weight: 400; font-style: italic; color: var(--muted); margin-left: 4px; }}
.project-bullets {{ padding-left: 10px; margin: 1px 0 0 0; }}
.project-bullets li {{ font-size: 7.8pt; color: var(--ink-soft); line-height: 1.35; margin-bottom: 1px; }}

@media print {{
  body {{ background: white; }}
  .page-wrapper {{ padding: 0; gap: 0; }}
  section.page {{ box-shadow: none; page-break-after: always; break-after: page; height: 297mm; max-height: 297mm; }}
  section.page:last-child {{ page-break-after: avoid; break-after: avoid; }}
}}"""
