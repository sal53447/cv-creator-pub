from .paths import e


# ---------------------------------------------------------------------------
# Sidebar renderers
# ---------------------------------------------------------------------------

def render_contact(contact: dict) -> str:
    parts = []

    def contact_row(label: str, value) -> str:
        if not value:
            return ""
        return (
            f'<div class="contact-row">'
            f'<span class="label">{e(label)}</span>'
            f'{e(value)}'
            f'</div>'
        )

    parts.append('<h2 class="sidebar-heading">Contact</h2>')
    parts.append(contact_row("Phone", contact.get("phone")))
    parts.append(contact_row("Email", contact.get("email")))
    parts.append(contact_row("Location", contact.get("location")))
    parts.append(contact_row("LinkedIn", contact.get("linkedin")))

    relocation = contact.get("relocation_note")
    if relocation:
        parts.append(f'<div class="relocation">{e(relocation)}</div>')

    return "\n".join(p for p in parts if p)


def render_languages(languages: list) -> str:
    if not languages:
        return ""
    parts = ['<h2 class="sidebar-heading">Languages</h2>']
    for lang in languages:
        name = e(lang.get("name", ""))
        level = e(lang.get("level", ""))
        parts.append(f'<div class="lang-item">{name} — {level}</div>')
    return "\n".join(parts)


def render_skills(skills: list) -> str:
    if not skills:
        return ""
    parts = ['<h2 class="sidebar-heading">Core Skills</h2>']
    for skill in skills:
        category = e(skill.get("category", ""))
        items = e(skill.get("items", ""))
        parts.append(
            f'<div class="skill-group">'
            f'<div class="skill-group-label">{category}</div>'
            f'<div class="skill-group-body">{items}</div>'
            f'</div>'
        )
    return "\n".join(parts)


def render_education_sidebar(education: dict) -> str:
    parts = []

    degrees = education.get("degrees", [])
    if degrees:
        parts.append('<h2 class="sidebar-heading">Education</h2>')
        for deg in degrees:
            degree = e(deg.get("degree", ""))
            field = e(deg.get("field", ""))
            institution = e(deg.get("institution", ""))
            location = e(deg.get("location", ""))
            date = e(deg.get("date", ""))
            thesis = deg.get("thesis")

            meta_parts = [p for p in [institution, location, date] if p]
            meta = " · ".join(meta_parts)
            thesis_html = f'<div class="edu-note">Thesis: {e(thesis)}</div>' if thesis else ""

            parts.append(
                f'<div class="edu-entry">'
                f'<div class="edu-degree">{degree}</div>'
                f'<div class="edu-field">{field}</div>'
                f'<div class="edu-meta">{meta}</div>'
                f'{thesis_html}'
                f'</div>'
            )

    certifications = education.get("certifications", [])
    if certifications:
        parts.append('<h2 class="sidebar-heading">Certifications</h2>')
        for cert in certifications:
            name = e(cert.get("name", ""))
            institution = e(cert.get("institution", ""))
            parts.append(
                f'<div class="cert-entry">'
                f'<div class="cert-name">{name}</div>'
                f'<div class="cert-inst">{institution}</div>'
                f'</div>'
            )

    return "\n".join(parts)


def render_publications_sidebar(publications_data: dict) -> str:
    parts = []

    publications = publications_data.get("publications", [])
    if publications:
        parts.append('<h2 class="sidebar-heading">Publications</h2>')
        for pub in publications:
            title = e(pub.get("title", ""))
            venue = e(pub.get("venue", ""))
            url_display = e(pub.get("url_display", ""))
            url = pub.get("url", "")
            description = e(pub.get("description", ""))

            if url_display and url:
                url_html = f'<div class="pub-url"><a href="{e(url)}">{url_display}</a></div>'
            elif url_display:
                url_html = f'<div class="pub-url">{url_display}</div>'
            else:
                url_html = ""

            desc_html = f'<div class="pub-desc">{description}</div>' if description else ""

            parts.append(
                f'<div class="pub-entry">'
                f'<div class="pub-title">{title}</div>'
                f'<div class="pub-venue">{venue}</div>'
                f'{url_html}'
                f'{desc_html}'
                f'</div>'
            )

    volunteer = publications_data.get("volunteer", {})
    vol_desc = volunteer.get("description", "") if volunteer else ""
    if vol_desc:
        parts.append('<h2 class="sidebar-heading">Volunteer</h2>')
        parts.append(f'<div class="volunteer-text">{e(vol_desc)}</div>')

    hobbies = publications_data.get("hobbies", [])
    if hobbies:
        parts.append('<h2 class="sidebar-heading">Hobbies</h2>')
        for hobby in hobbies:
            parts.append(f'<div class="hobby-item">{e(hobby)}</div>')

    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Main area renderers
# ---------------------------------------------------------------------------

def render_header(profile: dict) -> str:
    name = e(profile.get("name", ""))
    title = e(profile.get("title", ""))
    tagline = e(profile.get("tagline", ""))
    return (
        f'<div class="cv-header">'
        f'<div class="cv-name">{name}</div>'
        f'<div class="cv-title">{title}</div>'
        f'<div class="cv-tagline">{tagline}</div>'
        f'</div>'
    )


def render_profile_summary(profile: dict) -> str:
    summary = e(profile.get("summary", ""))
    return (
        f'<h2 class="section-heading">Profile</h2>'
        f'<div class="profile-text">{summary}</div>'
    )


def render_job(job: dict) -> str:
    title = e(job.get("title", ""))
    company = e(job.get("company", ""))
    location = e(job.get("location", ""))
    start = e(job.get("start", ""))
    end = e(job.get("end", "Present"))
    bullets = job.get("bullets", [])

    date_str = f"{start} – {end}" if start else end
    loc_html = f'<span class="job-loc">{location}</span>' if location else ""

    bullets_html = ""
    if bullets:
        items = "".join(f'<li>{e(b)}</li>' for b in bullets)
        bullets_html = f'<ul class="job-bullets">{items}</ul>'

    return (
        f'<div class="job">'
        f'<div class="job-header">'
        f'<span class="job-title">{title}</span>'
        f'<span class="job-date">{date_str}</span>'
        f'</div>'
        f'<div class="job-company">{company}{loc_html}</div>'
        f'{bullets_html}'
        f'</div>'
    )


def render_jobs(jobs: list, start_idx: int, end_idx: int) -> str:
    subset = jobs[start_idx:end_idx]
    if not subset:
        return ""
    parts = ['<h2 class="section-heading">Work Experience</h2>']
    for job in subset:
        parts.append(render_job(job))
    return "\n".join(parts)


def render_project(project: dict) -> str:
    name = e(project.get("name", ""))
    note = project.get("note")
    bullets = project.get("bullets", [])

    note_html = f'<span class="project-note">{e(note)}</span>' if note else ""

    bullets_html = ""
    if bullets:
        items = "".join(f'<li>{e(b)}</li>' for b in bullets)
        bullets_html = f'<ul class="project-bullets">{items}</ul>'

    return (
        f'<div class="project">'
        f'<div><span class="project-name">{name}</span>{note_html}</div>'
        f'{bullets_html}'
        f'</div>'
    )


def render_project_tier(tier: dict) -> str:
    label = e(tier.get("name", ""))
    projects = tier.get("projects", [])
    parts = [f'<div class="tier-label">{label}</div>']
    for project in projects:
        parts.append(render_project(project))
    return "\n".join(parts)


def render_project_tiers(tiers: list, start_idx: int, end_idx: int, include_heading: bool = True) -> str:
    subset = tiers[start_idx:end_idx]
    if not subset:
        return ""
    parts = []
    if include_heading:
        parts.append('<h2 class="section-heading">Projects</h2>')
    for tier in subset:
        parts.append(render_project_tier(tier))
    return "\n".join(parts)
