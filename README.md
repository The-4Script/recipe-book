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

---

## Validating Recipes

Before opening a pull request, run the validator to make sure your recipe(s) follow the required structure:

```bash
python scripts/validate-recipes.py
```

The script recursively scans every `.md` file under `recipes/` and checks each one for:

* A recipe title (`# Recipe Name`)
* All required sections: `Description`, `Ingredients`, `Preparation`, `Cooking Time`, `Difficulty`, `Servings`, `Author`
* Non-empty content under each section
* A valid local image reference (broken or missing image paths are reported)
* Correct file location — recipes must live directly inside one of `recipes/appetizers/`, `recipes/mains/`, `recipes/desserts/`, or `recipes/beverages/`

**Example output — success:**