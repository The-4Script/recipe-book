# Recipe Index

Welcome to the Recipe Index! Browse through our collection of recipes categorized by course.

---

## Navigation
* [Appetizers](#appetizers)
* [Main Course](#main-course)
* [Desserts](#desserts)
* [Beverages](#beverages)

---

## Appetizers

| Recipe | Category | Difficulty | Cooking Time |
| :--- | :--- | :--- | :--- |
| [Spring Rolls](./appetizers/spring-rolls.md) | Appetizer | Medium | 35 |

---

## Main Course

| Recipe | Category | Difficulty | Cooking Time |
| :--- | :--- | :--- | :--- |
| [Paneer Butter Masala](./mains/paneer-butter-masala.md) | Main Course | Medium | 25 min |

---

## Desserts

| Recipe | Category | Difficulty | Cooking Time |
| :--- | :--- | :--- | :--- |
| *(No recipes available yet)* | Dessert | — | — |

---

## Beverages

| Recipe | Category | Difficulty | Cooking Time |
| :--- | :--- | :--- | :--- |
| [Mango Lassi](./beverages/mango-lassi.md) | Beverage | Easy | 10 min |
| [Cold Coffee](./beverages/cold-coffee.md) | Beverage | Easy | 10 min |

*(Note: Add existing recipes present in your repository under their respective category tables using relative links like `./beverages/cold-coffee.md`.)*
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