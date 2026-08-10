from pathlib import Path

required_sections = [
    "# ",
    "## Ingredients",
]

recipes_dir = Path("recipes")
errors = []

for recipe in recipes_dir.rglob("*.md"):
    content = recipe.read_text(encoding="utf-8")

    for section in required_sections:
        if section not in content:
            errors.append(f"{recipe}: missing {section}")
            
    if "## Preparation Steps" not in content and "## Instructions" not in content:
        errors.append(f"{recipe}: missing preparation/instructions section")        

if errors:
    print("Recipe validation failed:")
    for error in errors:
        print(error)
    raise SystemExit(1)

print("All recipes are valid!")