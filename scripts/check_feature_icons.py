#!/usr/bin/env python3

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CONTENT_PATTERNS = (
    "_guides/*.md",
    "_posts/*.md",
    "_projects/*.md",
    "_reading_series/*.md",
)
ICON_INCLUDE = ROOT / "_includes/feature-icon.html"
ICON_CATALOG = ROOT / "ICONS.md"

FRONT_MATTER = re.compile(r"\A---\s*\n(.*?)\n---(?:\s*\n|\Z)", re.DOTALL)
ICON_FIELD = re.compile(r'^icon:\s*["\']?([a-z0-9-]+)["\']?\s*$', re.MULTILINE)
IMPLEMENTED_ICON = re.compile(r'{%\s*when\s+["\']([a-z0-9-]+)["\']\s*%}')
DOCUMENTED_ICON = re.compile(r"^\| `([a-z0-9-]+)` \|", re.MULTILINE)
LITERAL_ICON = re.compile(
    r'{%\s*include\s+feature-icon\.html\s+name=["\']([a-z0-9-]+)["\']\s*%}'
)


def content_paths() -> list[Path]:
    return sorted(path for pattern in CONTENT_PATTERNS for path in ROOT.glob(pattern))


def icon_assignment(path: Path) -> str | None:
    document = path.read_text()
    front_matter = FRONT_MATTER.match(document)
    if front_matter is None:
        return None
    match = ICON_FIELD.search(front_matter.group(1))
    return match.group(1) if match else None


def validate_feature_icons() -> tuple[int, int]:
    implemented = set(IMPLEMENTED_ICON.findall(ICON_INCLUDE.read_text()))
    documented = set(DOCUMENTED_ICON.findall(ICON_CATALOG.read_text()))
    paths = content_paths()
    errors: list[str] = []

    for path in paths:
        relative_path = path.relative_to(ROOT)
        icon = icon_assignment(path)
        if icon is None:
            errors.append(f"{relative_path}: missing icon in front matter")
        elif icon not in implemented:
            errors.append(
                f'{relative_path}: icon "{icon}" is not implemented in '
                f"{ICON_INCLUDE.relative_to(ROOT)}"
            )

    for path in sorted(ROOT.glob("_site_pages/*.md")):
        for icon in LITERAL_ICON.findall(path.read_text()):
            if icon not in implemented:
                errors.append(
                    f'{path.relative_to(ROOT)}: icon "{icon}" is not implemented in '
                    f"{ICON_INCLUDE.relative_to(ROOT)}"
                )

    for icon in sorted(implemented - documented):
        errors.append(f'{ICON_CATALOG.relative_to(ROOT)}: implemented icon "{icon}" is not documented')
    for icon in sorted(documented - implemented):
        errors.append(f'{ICON_CATALOG.relative_to(ROOT)}: documented icon "{icon}" is not implemented')

    if errors:
        details = "\n".join(f"- {error}" for error in errors)
        raise ValueError(f"Feature icon validation failed:\n{details}")

    return len(paths), len(implemented)


def main() -> int:
    try:
        assignment_count, implementation_count = validate_feature_icons()
    except ValueError as error:
        print(error, file=sys.stderr)
        return 1

    print(
        f"Validated {assignment_count} feature icon assignments against "
        f"{implementation_count} implemented icons."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
