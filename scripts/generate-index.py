from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
RECIPES_DIR = ROOT / "recipes"
INDEX_FILE = RECIPES_DIR / "INDEX.md"

REQUIRED_FIELDS = {
    "title",
    "category",
    "difficulty",
    "time",
    "servings",
    "author",
    "tags",
}

ALLOWED_DIFFICULTIES = {"easy", "medium", "hard"}


def parse_front_matter(file_path):
    text = file_path.read_text(encoding="utf-8")

    match = re.match(
        r"\A---\s*\n(.*?)\n---\s*(?:\n|$)",
        text,
        re.DOTALL,
    )

    if not match:
        raise ValueError("Missing YAML front matter")

    lines = match.group(1).splitlines()

    data = {}
    tags = []
    reading_tags = False

    for line in lines:
        if not line.strip():
            continue

        # Read tag list
        if reading_tags and line.strip().startswith("-"):
            tags.append(line.strip()[1:].strip())
            continue

        match = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$", line)

        if not match:
            raise ValueError(f"Invalid metadata line: {line}")

        key, value = match.groups()

        if key == "tags":
            reading_tags = True
            continue

        reading_tags = False
        data[key] = value.strip().strip('"').strip("'")

    data["tags"] = tags

    return data


def validate_metadata(file_path, data):
    errors = []

    missing = REQUIRED_FIELDS - set(data.keys())

    if missing:
        errors.append(
            "Missing required metadata: "
            + ", ".join(sorted(missing))
        )

    difficulty = data.get("difficulty")

    if difficulty and difficulty not in ALLOWED_DIFFICULTIES:
        errors.append(
            f"Invalid difficulty: {difficulty}\n"
            "Expected: easy, medium, hard"
        )

    for field in ["time", "servings"]:
        if field in data:
            try:
                value = int(data[field])

                if value < 0:
                    raise ValueError

            except ValueError:
                errors.append(
                    f"Invalid {field}: {data[field]} "
                    "(expected a non-negative integer)"
                )

    if "tags" in data and not data["tags"]:
        errors.append("Tags must contain at least one tag")

    return errors


def main():
    recipe_files = sorted(
        file
        for file in RECIPES_DIR.rglob("*.md")
        if file.name != "INDEX.md"
    )

    recipes = []
    errors = []

    for file_path in recipe_files:

        try:
            metadata = parse_front_matter(file_path)

            validation_errors = validate_metadata(
                file_path,
                metadata,
            )

            if validation_errors:
                errors.append(
                    (file_path, validation_errors)
                )
            else:
                recipes.append(
                    (file_path, metadata)
                )

        except Exception as error:
            errors.append(
                (file_path, [str(error)])
            )

    # Show errors
    if errors:
        print("❌ Recipe metadata validation failed:\n")

        for file_path, messages in errors:
            relative_path = file_path.relative_to(RECIPES_DIR)

            print(f"❌ {relative_path}")

            for message in messages:
                for line in message.splitlines():
                    print(f"   {line}")

            print()

        return 1

    # Group recipes by category
    categories = {}

    for file_path, metadata in recipes:
        category = metadata["category"]

        if category not in categories:
            categories[category] = []

        categories[category].append(
            (file_path, metadata)
        )

    # Generate INDEX.md
    lines = [
        "# Recipe Index",
        "",
    ]

    for category in sorted(categories):

        display_category = category.replace(
            "-",
            " "
        ).title()

        lines.extend([
            f"## {display_category}",
            "",
            "| Recipe | Difficulty | Time | Servings |",
            "|--------|------------|------|----------|",
        ])

        # Sort recipes alphabetically
        recipes_in_category = sorted(
            categories[category],
            key=lambda item: item[1]["title"].lower()
        )

        for file_path, metadata in recipes_in_category:

            relative_path = file_path.relative_to(
                RECIPES_DIR
            ).as_posix()

            link = f"./{relative_path}"

            lines.append(
                f"| [{metadata['title']}]({link}) "
                f"| {metadata['difficulty'].capitalize()} "
                f"| {metadata['time']} min "
                f"| {metadata['servings']} |"
            )

        lines.append("")

    INDEX_FILE.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print(
        f"✅ Generated recipes/INDEX.md "
        f"from {len(recipes)} recipes."
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())