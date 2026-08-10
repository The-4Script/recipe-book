import re
import sys
from pathlib import Path

REQUIRED_SECTIONS = [
    "Description",
    "Ingredients",
    "Preparation",
    "Cooking Time",
    "Difficulty",
    "Servings",
    "Author",
]

VALID_CATEGORIES = {"appetizers", "mains", "desserts", "beverages"}

# Pattern for Markdown headings (e.g., "## Description")
SECTION_HEADER_PATTERN = re.compile(r"^##\s+(.+)$", re.MULTILINE)
# Pattern for Markdown images (e.g., ![alt](path))
IMAGE_PATTERN = re.compile(r"!\[[^\]]*\]\(([^)\s]+)\)")

recipes_dir = Path("recipes")

if not recipes_dir.exists():
    print("❌ Directory 'recipes/' not found.")
    sys.exit(1)

recipe_files = list(recipes_dir.rglob("*.md"))
if not recipe_files:
    print("❌ No recipe files found in 'recipes/'.")
    sys.exit(1)

total_errors = 0
failed_files = 0


def get_section_content(content: str, section_name: str) -> str | None:
    """Extract content under a specific '## Section' up to the next heading or EOF."""
    # Matches line starting exact with '## Section Name'
    match = re.search(rf"^##\s+{re.escape(section_name)}\s*$", content, re.MULTILINE)
    if not match:
        return None

    start = match.end()
    # Find next section heading or level-1 title heading
    next_heading = re.search(r"^#+\s+", content[start:], re.MULTILINE)
    end = start + next_heading.start() if next_heading else len(content)
    return content[start:end].strip()


for recipe in sorted(recipe_files):
    content = recipe.read_text(encoding="utf-8")
    problems = []

    # Verify category location relative to recipes/
    rel_path = recipe.relative_to(recipes_dir)
    if len(rel_path.parts) != 2 or rel_path.parts[0] not in VALID_CATEGORIES:
        category = rel_path.parts[0] if len(rel_path.parts) > 1 else "root"
        problems.append(
            f"invalid file location (expected inside {sorted(VALID_CATEGORIES)}, got '{category}')"
        )

    # Check for # Title
    if not re.search(r"^#\s+\S", content, re.MULTILINE):
        problems.append("missing title (# Recipe Name)")

    # Check required sections and content
    for section in REQUIRED_SECTIONS:
        body = get_section_content(content, section)
        if body is None:
            problems.append(f"missing section: ## {section}")
        elif not body:
            problems.append(f"empty section: ## {section}")

    # Check images
    images = IMAGE_PATTERN.findall(content)
    local_images = [img for img in images if not img.startswith(("http://", "https://"))]

    if not images:
        problems.append("missing image reference")
    else:
        for img in local_images:
            image_path = (recipe.parent / img).resolve()
            if not image_path.is_file():
                problems.append(f"broken image reference: {img}")

    # Report results
    if problems:
        failed_files += 1
        total_errors += len(problems)
        print(f"❌ {recipe}")
        for problem in problems:
            print(f"   - {problem}")
    else:
        print(f"✓ {recipe}")

print()
if failed_files:
    print("Recipe validation failed.")
    print(f"{total_errors} error(s) found in {failed_files} file(s).")
    sys.exit(1)

print("All recipes passed validation.")
sys.exit(0)