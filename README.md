## Contributing

We welcome contributions to the Recipe Book!

Before adding or modifying a recipe, please read the [Contribution Guide](docs/contribution-guide.md) for the required recipe format, naming conventions, branch guidelines, commit conventions, and Pull Request requirements.

Use the [Recipe Template](docs/recipe-template.md) when creating a new recipe to keep all recipes consistent.

## Recipe Metadata

Every recipe must begin with YAML front matter.

### Metadata Format

```yaml
---
title: Cold Coffee
category: beverages
difficulty: easy
time: 10
servings: 2
author: Durvesh
tags:
  - coffee
  - beverage
  - cold
---
```

### Required Fields

The following fields are required for every recipe:

- `title` — Name of the recipe
- `category` — Category of the recipe
- `difficulty` — Difficulty level
- `time` — Total preparation/cooking time in minutes
- `servings` — Number of servings
- `author` — Name of the recipe author
- `tags` — List of relevant tags

### Allowed Difficulty Values

Only these difficulty values are allowed:

- `easy`
- `medium`
- `hard`

### Generate Recipe Index

The recipe index is generated automatically from the recipe metadata.

Run:

```bash
python scripts/generate-index.py
```

This command scans all recipe files and generates:

```text
recipes/INDEX.md
```

The generated index contains recipes grouped by category, along with their difficulty, time, and servings.

`recipes/INDEX.md` is a generated file. Contributors should not manually maintain the recipe table.