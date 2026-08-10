# Contribution Guide

Thank you for contributing to the Recipe Book! This guide explains how to add recipes and submit changes while keeping the project organized and consistent.

## 1. Where to Add Recipes

All recipes should be added to the appropriate recipe category directory in the repository.

If the required category does not exist, create a suitable category directory before adding the recipe.

Use lowercase names with hyphens for recipe filenames.

Example:

```text
recipes/
├── beverages/
│   ├── cold-coffee.md
│   └── mango-lassi.md
├── desserts/
│   └── chocolate-cake.md
└── snacks/
    └── garlic-bread.md
```

## 2. Recipe Format

Every recipe should follow the standardized structure provided in the [Recipe Template](recipe-template.md).

Each recipe should contain:

* Recipe title
* Description
* Ingredients
* Preparation steps
* Cooking time
* Difficulty
* Servings
* Image
* Author

Keep the information clear, accurate, and easy to follow.

When adding a new recipe, copy the recipe template and replace the placeholder content with the actual recipe information.

## 3. Image Location and Naming Convention

All recipe images must be stored directly in the repository-level `images/` directory.

Valid:

```text
images/
└── cold-coffee.jpg
```

Invalid:

```text
recipes/beverages/cold-coffee.jpg
recipes/beverages/images/cold-coffee.jpg
recipes/images/cold-coffee.jpg
```

The image filename must match the recipe filename, excluding the `.md` extension. Lowercase letters, numbers, and hyphens are expected.

For:

```text
recipes/beverages/cold-coffee.md
```

use:

```text
images/cold-coffee.jpg
```

Avoid:

```text
Cold Coffee Final Image.jpg
IMG_2026.jpg
cold-coffee-final.jpg
```

The recipe should reference the repository-level image with a relative Markdown path:

```md
![Cold Coffee](../../images/cold-coffee.jpg)
```

Supported image formats are `.jpg`, `.jpeg`, `.png`, `.webp`, and `.gif`.

## 4. Automated Contribution Checks

Pull Requests are automatically checked for the repository conventions described in this guide.

The checker enforces:

* Recipe files are inside `recipes/appetizers/`, `recipes/mains/`, `recipes/desserts/`, or `recipes/beverages/`.
* Recipe filenames are lowercase, use hyphens, and end in `.md`.
* Recipe images are stored only in `images/`.
* An image filename matches its recipe filename.
* Recipes contain the required sections: Title, Description, Ingredients, Preparation, Cooking Time, Difficulty, Servings, Image, and Author.
* Unsupported non-Markdown files are not added inside recipe category directories.

The check runs automatically on Pull Requests. A failed check must be fixed before the contribution can be considered ready for merge.

## 5. Branch Naming Convention

Do not make changes directly on the `main` branch.

Create a separate feature branch for every contribution.

For a new recipe, use:

```text
recipe/<recipe-name>
```

Example:

```text
recipe/mango-lassi
```

For documentation changes, use:

```text
docs/<change-name>
```

Example:

```text
docs/recipe-contribution-guide
```

For other improvements, use an appropriate descriptive prefix such as:

```text
fix/<issue-name>
update/<change-name>
```

Branch names should be lowercase and use hyphens instead of spaces.

## 6. Commit Message Convention

Write short, clear, and descriptive commit messages.

For adding a recipe:

```text
Add <recipe-name> recipe
```

Example:

```text
Add mango lassi recipe
```

For documentation changes:

```text
Update contribution guide
```

For fixes:

```text
Fix recipe image path
```

Avoid vague commit messages such as:

```text
changes
update
final
stuff
asdf
```

Future contributors should be able to understand what a commit did without performing archaeological research.

## 7. Pull Request Requirements

All contributions should be submitted through a Pull Request.

Before opening a Pull Request, make sure that:

* The changes are made on a separate feature branch.
* The recipe follows the standard template.
* The recipe is placed in the correct category.
* Images follow the naming convention.
* Markdown links and formatting work correctly.
* Commit messages are clear and descriptive.
* No unrelated files or changes are included.

### Pull Request Title

Use a short and descriptive title.

For example:

```text
Add Mango Lassi recipe
```

For documentation changes:

```text
Add recipe contribution guide
```

### Pull Request Description

The description should briefly explain what was changed.

Example:

```md
## Summary

- Added Mango Lassi recipe
- Added recipe image
- Followed the standard recipe template

## Checklist

- [x] Recipe follows the required format
- [x] Image naming convention followed
- [x] Changes are on a separate branch
- [x] Markdown formatting checked
- [x] No unrelated changes included
```

## 8. Review and Merge

After opening the Pull Request:

1. Wait for the contribution to be reviewed.
2. Address any requested changes.
3. Push additional commits to the same branch if necessary.
4. Once approved, the Pull Request can be merged into `main`.

Do not merge your own Pull Request unless the repository's contribution policy explicitly allows it.

## 9. Quick Contribution Workflow

```bash
git checkout main
git pull origin main

git checkout -b recipe/<recipe-name>

# Add or modify the recipe

git add .
git commit -m "Add <recipe-name> recipe"

git push -u origin recipe/<recipe-name>
```

Then open a Pull Request on GitHub and wait for review.

## 10. Contribution Checklist

Before submitting your Pull Request, verify:

* [ ] Recipe is in the correct directory
* [ ] Recipe follows the standard template
* [ ] All required sections are present
* [ ] Image follows the naming convention
* [ ] Branch follows the naming convention
* [ ] Commit message is descriptive
* [ ] Markdown renders correctly
* [ ] No unrelated changes are included
* [ ] Pull Request has a clear title and description
* [ ] Changes are ready for review
