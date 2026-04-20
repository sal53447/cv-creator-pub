import html
import json
import os

import yaml

# Root of the project (one level up from src/)
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def content_path(filename: str, profile: str = "default") -> str:
    return os.path.join(ROOT_DIR, "profiles", profile, "data", filename)


def asset_path(*parts: str) -> str:
    return os.path.join(ROOT_DIR, "themes", *parts)


def load_yaml(filename: str, profile: str = "default") -> dict:
    path = content_path(filename, profile)
    if profile != "default" and not os.path.exists(path):
        path = content_path(filename, "default")
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_json(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def e(text) -> str:
    """HTML-escape a value, converting None to empty string."""
    if text is None:
        return ""
    return html.escape(str(text))
