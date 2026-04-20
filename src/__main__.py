#!/usr/bin/env python3
import argparse
import os
import sys

from src.pages import build_html, build_page1, build_page2, build_page3
from src.paths import ROOT_DIR, asset_path, load_json, load_yaml
from src.styles import build_css


def export_pdf(html_path: str, pdf_path: str) -> None:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f"file://{html_path}", wait_until="networkidle")
        page.pdf(
            path=pdf_path,
            format="A4",
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
        )
        browser.close()


def main():
    parser = argparse.ArgumentParser(description="Build an A4 HTML CV from YAML content files.")
    parser.add_argument("--company", default="default", help="Company name — determines output folder (default: default)")
    parser.add_argument("--theme", default=None, help="Color theme name (default: same as --company)")
    parser.add_argument("--profile", default=None, help="Content profile under profiles/ (default: same as --company)")
    parser.add_argument("--output", default="cv.html", help="Output filename (default: cv.html)")
    parser.add_argument("--pdf", action="store_true", help="Also export a PDF alongside the HTML")
    args = parser.parse_args()

    company = args.company
    theme = args.theme or company
    profile = args.profile or company
    output_filename = args.output

    colors_file = asset_path("colors", f"{theme}.json")
    if not os.path.exists(colors_file):
        print(f"Error: color theme file not found: {colors_file}", file=sys.stderr)
        sys.exit(1)

    fonts_file = asset_path("fonts", "default.json")
    if not os.path.exists(fonts_file):
        print(f"Error: fonts file not found: {fonts_file}", file=sys.stderr)
        sys.exit(1)

    colors = load_json(colors_file).get("colors", {})
    primary_font = load_json(fonts_file).get("primary", {})
    font_family = primary_font.get("family", "sans-serif")
    font_import = primary_font.get("google_import", "")

    profile_data = load_yaml("profile.yaml", profile)
    contact = load_yaml("contact.yaml", profile)
    work_experience = load_yaml("work_experience.yaml", profile)
    education = load_yaml("education.yaml", profile)
    projects = load_yaml("projects.yaml", profile)
    publications_data = load_yaml("publications.yaml", profile)

    css = build_css(theme, colors, font_family)
    pages = [
        build_page1(profile_data, contact, work_experience.get("jobs", []), education),
        build_page2(publications_data, work_experience.get("jobs", []), projects.get("tiers", [])),
        build_page3(projects.get("tiers", [])),
    ]
    html_output = build_html(theme, css, font_import, pages)

    output_dir = os.path.join(ROOT_DIR, "output", company)
    os.makedirs(output_dir, exist_ok=True)
    html_path = os.path.join(output_dir, output_filename)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_output)
    print(f"HTML written to: {html_path}")

    if args.pdf:
        pdf_filename = os.path.splitext(output_filename)[0] + ".pdf"
        pdf_path = os.path.join(output_dir, pdf_filename)
        export_pdf(html_path, pdf_path)
        print(f"PDF  written to: {pdf_path}")


if __name__ == "__main__":
    main()
