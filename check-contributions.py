#!/usr/bin/env python3
"""Validate contribution-specific repository conventions.

The checker focuses on files changed by a pull request. When no Git range is
provided, it validates all tracked files in the working tree. This keeps CI
focused on the contribution while allowing the script to be useful locally.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ALLOWED_CATEGORIES = {"appetizers", "mains", "desserts", "beverages"}
RECIPE_ROOT = Path("recipes")
IMAGE_ROOT = Path("images")
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
IGNORED_RECIPE_FILES = {".gitkeep"}

RECIPE_FILENAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*\.md$")
HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$", re.MULTILINE)
IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)\s]+)(?:\s+['\"][^'\"]*['\"])?\)")

REQUIRED_SECTIONS = {
    "title": set(),
    "description": {"description"},
    "ingredients": {"ingredients"},
    "preparation": {"preparation", "preparation steps", "instructions"},
    "cooking time": {"cooking time"},
    "difficulty": {"difficulty"},
    "servings": {"servings"},
    "author": {"author"},
    "image": {"image"},
}


def run_git(*args: str) -> list[str]:
    result = subprocess.run(
        ["git", *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def changed_files(base: str | None, head: str | None) -> list[Path]:
    if base:
        target = head or "HEAD"
        output = run_git("diff", "--name-only", "--diff-filter=ACMR", base, target)
        return [Path(p) for p in output]
    return [
        Path(p)
        for p in run_git("ls-files")
        if not p.startswith(".git/")
    ]


def is_recipe(path: Path) -> bool:
    return (
        len(path.parts) == 3
        and path.parts[0] == RECIPE_ROOT.name
        and path.suffix.lower() == ".md"
    )


def recipe_category(path: Path) -> str | None:
    if len(path.parts) >= 2 and path.parts[0] == RECIPE_ROOT.name:
        return path.parts[1]
    return None


def is_image(path: Path) -> bool:
    return path.suffix.lower() in IMAGE_EXTENSIONS


def normalise_heading(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().lower())


def read_recipe_sections(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8")
    headings = {normalise_heading(m.group(1)) for m in HEADING_RE.finditer(text)}
    sections = {
        key
        for key, aliases in REQUIRED_SECTIONS.items()
        if headings & aliases
    }
    if re.search(r"^\s*#\s+\S", text, re.MULTILINE):
        sections.add("title")
    return sections


def recipe_image_paths(path: Path) -> list[Path]:
    text = path.read_text(encoding="utf-8")
    result = []
    for raw in IMAGE_RE.findall(text):
        # Ignore remote images. Repository-local images are checked below.
        if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", raw):
            continue
        result.append(Path(raw.split("#", 1)[0]))
    return result


def resolve_recipe_image(recipe: Path, image_ref: Path) -> Path:
    return (recipe.parent / image_ref).resolve()


def find_recipe_for_image(image_path: Path, recipes: list[Path]) -> Path | None:
    stem = image_path.stem.lower()
    for recipe in recipes:
        if recipe.stem.lower() == stem:
            return recipe
    return None


def validate_recipe(path: Path, errors: list[str]) -> None:
    category = recipe_category(path)
    if category not in ALLOWED_CATEGORIES:
        allowed = ", ".join(sorted(ALLOWED_CATEGORIES))
        errors.append(
            f"Invalid recipe location:\n"
            f"  {path}\n"
            f"  Allowed categories: {allowed}"
        )

    if not RECIPE_FILENAME_RE.fullmatch(path.name):
        errors.append(
            f"Invalid recipe filename: {path.name}\n"
            "  Expected format: lowercase-words-separated-by-hyphens.md"
        )

    if not path.exists():
        return

    missing = sorted(set(REQUIRED_SECTIONS) - read_recipe_sections(path))
    if missing:
        errors.append(
            f"Missing required recipe sections in {path}:\n"
            + "\n".join(f"  - {section.title()}" for section in missing)
        )

    image_refs = recipe_image_paths(path)
    if not image_refs:
        errors.append(f"Missing recipe image in {path}")
        return

    expected_name = path.stem.lower()
    for image_ref in image_refs:
        resolved = resolve_recipe_image(path, image_ref)
        try:
            relative = resolved.relative_to(Path.cwd().resolve())
        except ValueError:
            relative = Path(image_ref)

        if not image_ref.parts or image_ref.parts[0] != IMAGE_ROOT.name:
            # Relative references from recipes/<category>/ are normally
            # ../../images/<name>.<ext>. Validate the resolved repository path.
            try:
                relative = resolved.relative_to(Path.cwd().resolve())
            except ValueError:
                relative = Path()
        if not relative or relative.parts[0] != IMAGE_ROOT.name:
            errors.append(
                f"Image stored outside images/:\n"
                f"  Recipe: {path}\n"
                f"  Image:  {image_ref}"
            )
            continue

        if Path(relative).stem.lower() != expected_name:
            errors.append(
                f"Image naming mismatch:\n"
                f"  Recipe: {path.name}\n"
                f"  Image:  {relative.name}\n"
                f"  Expected: {expected_name}{relative.suffix.lower()}"
            )

        if not resolved.exists():
            errors.append(
                f"Missing referenced image:\n"
                f"  Recipe: {path}\n"
                f"  Image:  {relative}"
            )


def validate_unsupported_files(paths: list[Path], errors: list[str]) -> None:
    by_directory: dict[Path, list[str]] = {}
    for path in paths:
        category = recipe_category(path)
        if category not in ALLOWED_CATEGORIES:
            continue
        if len(path.parts) != 3:
            continue
        if path.name in IGNORED_RECIPE_FILES:
            continue
        if path.suffix.lower() != ".md":
            by_directory.setdefault(path.parent, []).append(path.name)

    for directory, files in sorted(by_directory.items()):
        errors.append(
            f"Unsupported file in {directory}:\n"
            + "\n".join(f"  {name}" for name in sorted(files))
        )


def validate_changed_images(
    paths: list[Path],
    recipes: list[Path],
    changed_recipes: list[Path],
    errors: list[str],
) -> None:
    candidate_recipes = recipes + [p for p in changed_recipes if p not in recipes]
    for image in paths:
        if not is_image(image):
            continue

        if len(image.parts) < 2 or image.parts[0] != IMAGE_ROOT.name:
            errors.append(
                f"Image stored outside images/:\n"
                f"  {image}"
            )

        recipe = find_recipe_for_image(image, candidate_recipes)
        if recipe is None:
            errors.append(
                f"Image naming mismatch:\n"
                f"  Image: {image}\n"
                "  Expected the image filename to match a recipe filename."
            )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", help="Base Git commit for a PR diff")
    parser.add_argument("--head", help="Head Git commit for a PR diff")
    args = parser.parse_args()

    try:
        paths = changed_files(args.base, args.head)
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        print(f"❌ Unable to determine changed files: {exc}", file=sys.stderr)
        return 2

    errors: list[str] = []
    recipes = []
    for raw_path in run_git("ls-files"):
        recipe_path = Path(raw_path)
        if (
            recipe_path.parts[:1] == (RECIPE_ROOT.name,)
            and recipe_path.suffix.lower() == ".md"
            and len(recipe_path.parts) == 3
        ):
            recipes.append(recipe_path)

    changed_recipe_files = [p for p in paths if is_recipe(p)]

    # Validate every changed recipe, including a recipe moved into an invalid
    # category. Invalid locations are reported before content checks.
    for path in changed_recipe_files:
        validate_recipe(path, errors)

    validate_unsupported_files(paths, errors)
    validate_changed_images(paths, recipes, changed_recipe_files, errors)

    # Catch images referenced by changed recipes even when the image itself was
    # not part of the PR diff.
    for recipe in changed_recipe_files:
        if recipe.exists():
            for ref in recipe_image_paths(recipe):
                resolved = resolve_recipe_image(recipe, ref)
                try:
                    relative = resolved.relative_to(Path.cwd().resolve())
                except ValueError:
                    continue
                if relative.parts[:1] == (IMAGE_ROOT.name,) and is_image(relative):
                    if relative.stem.lower() != recipe.stem.lower():
                        # validate_recipe already reports this; avoid duplicates.
                        pass

    if errors:
        print("❌ Contribution validation failed\n")
        for index, error in enumerate(errors, 1):
            print(f"{index}. {error}\n")
        return 1

    print(f"✅ Contribution validation passed ({len(paths)} changed file(s) checked)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
