from .paths import e
from .renderers import (
    render_contact,
    render_education_sidebar,
    render_header,
    render_jobs,
    render_languages,
    render_profile_summary,
    render_project_tiers,
    render_publications_sidebar,
    render_skills,
)


def build_page1(profile: dict, contact: dict, jobs: list, education: dict) -> str:
    aside_html = "\n".join([
        render_contact(contact),
        render_languages(contact.get("languages", [])),
        render_skills(contact.get("skills", [])),
        render_education_sidebar(education),
    ])
    main_html = "\n".join([
        render_header(profile),
        render_profile_summary(profile),
        render_jobs(jobs, 0, 3),
    ])
    return (
        f'<section class="page">'
        f'<aside>{aside_html}</aside>'
        f'<main>{main_html}</main>'
        f'</section>'
    )


def build_page2(publications_data: dict, jobs: list, tiers: list) -> str:
    aside_html = render_publications_sidebar(publications_data)
    jobs_html = render_jobs(jobs, 3, 6)
    projects_html = render_project_tiers(tiers, 0, 1)
    main_html = "\n".join(filter(None, [jobs_html, projects_html]))
    return (
        f'<section class="page">'
        f'<aside>{aside_html}</aside>'
        f'<main>{main_html}</main>'
        f'</section>'
    )


def build_page3(tiers: list) -> str:
    main_html = render_project_tiers(tiers, 1, len(tiers))
    return (
        f'<section class="page">'
        f'<aside></aside>'
        f'<main>{main_html}</main>'
        f'</section>'
    )


def build_html(theme: str, css: str, font_import: str, pages: list) -> str:
    pages_html = "\n".join(pages)
    return f"""\
<!DOCTYPE html>
<html lang="en" data-theme="{e(theme)}">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Curriculum Vitae</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="{e(font_import)}" rel="stylesheet" />
  <style>
{css}
  </style>
</head>
<body>
  <div class="page-wrapper">
{pages_html}
  </div>
</body>
</html>"""
