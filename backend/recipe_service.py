
# backend/recipe_service.py

# Starter ingredient-substitution knowledge base.
# Suggestions depend on the role of the ingredient in the dish.

SUBSTITUTIONS = {
    "pine nuts": [
        {
            "ingredient": "cashews",
            "ratio": 1.0,
            "reason": "Creamy texture and mild nutty flavour; useful in pesto.",
            "difference": "Slightly sweeter and less resinous.",
        },
        {
            "ingredient": "walnuts",
            "ratio": 1.0,
            "reason": "Nutty flavour and a similar role in pesto.",
            "difference": "More earthy and can taste slightly bitter.",
        },
    ],
    "buttermilk": [
        {
            "ingredient": "milk + lemon juice",
            "ratio": 1.0,
            "reason": "Acidified milk can provide similar acidity in many baked recipes.",
            "difference": "Thinner than cultured buttermilk.",
        },
    ],
    "sour cream": [
        {
            "ingredient": "plain unsweetened yogurt",
            "ratio": 1.0,
            "reason": "Provides tanginess and moisture in many dips and sauces.",
            "difference": "Usually less rich; strained yogurt is thicker.",
        },
    ],
    "heavy cream": [
        {
            "ingredient": "evaporated milk",
            "ratio": 1.0,
            "reason": "Can add creaminess to some soups and sauces.",
            "difference": "Less fatty; it will not whip like heavy cream.",
        },
    ],
    "parmesan": [
        {
            "ingredient": "vegetarian hard cheese",
            "ratio": 1.0,
            "reason": "Can provide a salty, savoury topping.",
            "difference": "Flavour varies by cheese; check the label if vegetarian.",
        },
    ],
    "soy sauce": [
        {
            "ingredient": "tamari",
            "ratio": 1.0,
            "reason": "A similar savoury, umami-rich seasoning.",
            "difference": "Check gluten content and saltiness on the label.",
        },
    ],
    "cornstarch": [
        {
            "ingredient": "potato starch",
            "ratio": 1.0,
            "reason": "Useful for thickening many sauces and gravies.",
            "difference": "Can behave differently at high temperatures; add carefully.",
        },
    ],
}


def find_substitutes(ingredient):
    """Return known alternatives for an unavailable ingredient."""
    key = ingredient.strip().lower()

    if not key:
        return []

    return SUBSTITUTIONS.get(key, [])


def get_substitution_advice(ingredient):
    """Provide readable advice for a missing ingredient."""
    suggestions = find_substitutes(ingredient)

    if not suggestions:
        return {
            "ingredient": ingredient,
            "message": (
                "No verified suggestion is available yet. "
                "Check the recipe's function before choosing an alternative."
            ),
            "substitutes": [],
        }

    return {
        "ingredient": ingredient,
        "message": (
            "These are possible alternatives. The best choice depends "
            "on the recipe and the ingredient's role."
        ),
        "substitutes": suggestions,
    }


# Recipe-specific substitution guidance

RECIPE_SUBSTITUTIONS = {
    "pesto": {
        "pine nuts": [
            {
                "ingredient": "cashews",
                "ratio": 1.0,
                "reason": "Their creamy texture and mild flavour work well in pesto.",
                "difference": "The result may taste sweeter and less traditionally pine-nut-like.",
            },
            {
                "ingredient": "walnuts",
                "ratio": 1.0,
                "reason": "They provide a similar nutty quality in pesto.",
                "difference": "The flavour is earthier and may be slightly bitter.",
            },
        ]
    },
    "pizza": {
        "mozzarella": [
            {
                "ingredient": "pizza cheese",
                "ratio": 1.0,
                "reason": "It can provide a similar melting function on pizza.",
                "difference": "Stretchiness and flavour vary by brand.",
            }
        ]
    },
    "pancakes": {
        "buttermilk": [
            {
                "ingredient": "milk + lemon juice",
                "ratio": 1.0,
                "reason": "Acidified milk can provide acidity and moisture.",
                "difference": "The texture may be thinner than buttermilk.",
            }
        ]
    },
}


def find_recipe_substitutes(recipe_name, ingredient):
    """Find substitutes based on both the recipe and missing ingredient."""
    recipe = recipe_name.strip().lower()
    missing = ingredient.strip().lower()

    recipe_data = RECIPE_SUBSTITUTIONS.get(recipe, {})
    suggestions = recipe_data.get(missing, [])

    if suggestions:
        return {
            "recipe": recipe_name,
            "ingredient": ingredient,
            "message": "These alternatives are selected for this recipe.",
            "substitutes": suggestions,
        }

    return {
        "recipe": recipe_name,
        "ingredient": ingredient,
        "message": (
            "No recipe-specific suggestion is available yet. "
            "Try the general Ingredient Substitute Finder."
        ),
        "substitutes": [],
    }


# Basic recipe catalogue for FlavorMate

RECIPES = [
    {
        "name": "Margherita Pizza",
        "aliases": ["pizza", "cheese pizza", "italian pizza"],
        "cuisine": "Italian",
        "ingredients": [
            "pizza dough", "tomato sauce", "mozzarella", "basil"
        ],
        "instructions": [
            "Preheat the oven to 220°C.",
            "Spread tomato sauce over the pizza dough.",
            "Add mozzarella cheese and basil.",
            "Bake until the crust is golden and the cheese melts."
        ],
    },
    {
        "name": "Vegetable Pizza",
        "aliases": ["veg pizza", "vegetarian pizza"],
        "cuisine": "Italian",
        "ingredients": [
            "pizza dough", "tomato sauce", "mozzarella",
            "onion", "capsicum", "tomato"
        ],
        "instructions": [
            "Preheat the oven to 220°C.",
            "Spread tomato sauce over the dough.",
            "Add cheese and chopped vegetables.",
            "Bake until the crust is golden and the vegetables are cooked."
        ],
    },
    {
        "name": "Pancakes",
        "aliases": ["pancake", "breakfast pancakes"],
        "cuisine": "International",
        "ingredients": ["flour", "milk", "egg", "sugar"],
        "instructions": [
            "Mix the flour, milk, egg and sugar.",
            "Heat a lightly greased pan.",
            "Pour in the batter and cook both sides until golden."
        ],
    },
    {
        "name": "Pesto Pasta",
        "aliases": ["pasta", "pesto"],
        "cuisine": "Italian",
        "ingredients": ["pasta", "pesto sauce", "parmesan"],
        "instructions": [
            "Boil the pasta until tender.",
            "Drain the pasta.",
            "Mix with pesto sauce and serve with cheese."
        ],
    },
]


def search_recipes(query):
    """Search recipes by name, alias, cuisine or ingredient."""
    query = query.strip().casefold()

    if not query:
        return []

    results = []

    for recipe in RECIPES:
        searchable_text = [
            recipe["name"],
            recipe["cuisine"],
            *recipe["aliases"],
            *recipe["ingredients"],
        ]

        if any(query in item.casefold() for item in searchable_text):
            results.append(recipe)

    return results


from backend.database import get_connection, initialize_database


def save_recipes_to_database():
    """Save the existing recipe catalogue into SQLite."""
    initialize_database()

    with get_connection() as connection:
        for recipe in RECIPES:
            cursor = connection.execute(
                """
                INSERT INTO recipes (recipe_key, cuisine)
                VALUES (?, ?)
                ON CONFLICT(recipe_key) DO UPDATE SET
                    cuisine = excluded.cuisine
                """,
                (
                    recipe["name"].strip().lower().replace(" ", "_"),
                    recipe["cuisine"],
                ),
            )

            recipe_key = recipe["name"].strip().lower().replace(" ", "_")
            row = connection.execute(
                "SELECT id FROM recipes WHERE recipe_key = ?",
                (recipe_key,),
            ).fetchone()

            recipe_id = row["id"]

            connection.execute(
                """
                INSERT INTO recipe_translations
                    (recipe_id, language_code, recipe_name, description)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(recipe_id, language_code) DO UPDATE SET
                    recipe_name = excluded.recipe_name
                """,
                (
                    recipe_id,
                    "en",
                    recipe["name"],
                    recipe.get("description", ""),
                ),
            )

            for step_number, instruction in enumerate(
                recipe.get("instructions", []), start=1
            ):
                connection.execute(
                    """
                    INSERT INTO instruction_translations
                        (recipe_id, language_code, step_number, instruction)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(recipe_id, language_code, step_number)
                    DO UPDATE SET instruction = excluded.instruction
                    """,
                    (recipe_id, "en", step_number, instruction),
                )

            # Add ingredients only when this recipe has none saved yet.
            existing = connection.execute(
                "SELECT COUNT(*) AS total FROM ingredients WHERE recipe_id = ?",
                (recipe_id,),
            ).fetchone()["total"]

            if existing == 0:
                for ingredient in recipe.get("ingredients", []):
                    connection.execute(
                        """
                        INSERT INTO ingredients (recipe_id, ingredient_name)
                        VALUES (?, ?)
                        """,
                        (recipe_id, ingredient),
                    )

    return len(RECIPES)


from backend.database import get_connection


def get_recipes_in_language(language_code="en"):
    """Retrieve recipes and instructions in the selected language."""
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT
                r.id,
                r.cuisine,
                rt.recipe_name,
                rt.description
            FROM recipes AS r
            JOIN recipe_translations AS rt
                ON r.id = rt.recipe_id
            WHERE rt.language_code = ?
            ORDER BY rt.recipe_name
            """,
            (language_code,),
        ).fetchall()

        results = []

        for row in rows:
            recipe_id = row["id"]

            ingredients = connection.execute(
                """
                SELECT ingredient_name
                FROM ingredients
                WHERE recipe_id = ?
                """,
                (recipe_id,),
            ).fetchall()

            instructions = connection.execute(
                """
                SELECT instruction
                FROM instruction_translations
                WHERE recipe_id = ? AND language_code = ?
                ORDER BY step_number
                """,
                (recipe_id, language_code),
            ).fetchall()

            results.append({
                "id": recipe_id,
                "name": row["recipe_name"],
                "cuisine": row["cuisine"],
                "description": row["description"] or "",
                "ingredients": [item["ingredient_name"] for item in ingredients],
                "instructions": [item["instruction"] for item in instructions],
            })

        return results


def add_hindi_margherita_translation():
    """Add Hindi recipe name and cooking instructions."""
    from backend.database import get_connection

    with get_connection() as connection:
        recipe = connection.execute(
            """
            SELECT id FROM recipes
            WHERE recipe_key = 'margherita_pizza'
            """
        ).fetchone()

        if recipe is None:
            raise ValueError(
                "Margherita Pizza is missing from the database."
            )

        recipe_id = recipe["id"]

        connection.execute(
            """
            INSERT INTO recipe_translations
                (recipe_id, language_code, recipe_name, description)
            VALUES (?, 'hi', ?, ?)
            ON CONFLICT(recipe_id, language_code) DO UPDATE SET
                recipe_name = excluded.recipe_name,
                description = excluded.description
            """,
            (
                recipe_id,
                "मार्गरीटा पिज़्ज़ा",
                "टमाटर सॉस, मोज़रेला चीज़ और तुलसी से बना पिज़्ज़ा।",
            ),
        )

        hindi_steps = [
            "ओवन को 220°C पर पहले से गर्म करें।",
            "पिज़्ज़ा के आटे को गोल आकार में बेलें।",
            "ऊपर टमाटर सॉस और मोज़रेला चीज़ फैलाएँ।",
            "पिज़्ज़ा को सुनहरा होने तक लगभग 10–15 मिनट बेक करें।",
            "ऊपर ताज़ी तुलसी डालें और परोसें।",
        ]

        for step_number, instruction in enumerate(hindi_steps, start=1):
            connection.execute(
                """
                INSERT INTO instruction_translations
                    (recipe_id, language_code, step_number, instruction)
                VALUES (?, 'hi', ?, ?)
                ON CONFLICT(recipe_id, language_code, step_number)
                DO UPDATE SET instruction = excluded.instruction
                """,
                (recipe_id, step_number, instruction),
            )

    return "Hindi translation saved for Margherita Pizza."
