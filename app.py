
import streamlit as st

from backend.recipe_service import (
    get_substitution_advice,
    find_recipe_substitutes,
    get_recipes_in_language,
)

# --------------------------------------------------
# PAGE SETTINGS
# --------------------------------------------------

st.set_page_config(
    page_title="FlavorMate",
    page_icon="🍲",
    layout="wide",
)

# --------------------------------------------------
# LANGUAGE SETTINGS
# --------------------------------------------------

INDIAN_LANGUAGES = [
    "English",
    "हिन्दी — Hindi",
    "অসমীয়া — Assamese",
    "বাংলা — Bengali",
    "बोडो — Bodo",
    "डोगरी — Dogri",
    "ગુજરાતી — Gujarati",
    "ಕನ್ನಡ — Kannada",
    "कोंकणी — Konkani",
    "मैथिली — Maithili",
    "മലയാളം — Malayalam",
    "মণিপুরী — Manipuri (Meitei)",
    "मराठी — Marathi",
    "नेपाली — Nepali",
    "ଓଡ଼ିଆ — Odia",
    "ਪੰਜਾਬੀ — Punjabi",
    "संस्कृतम् — Sanskrit",
    "سنڌي — Sindhi",
    "தமிழ் — Tamil",
    "తెలుగు — Telugu",
    "اردو — Urdu",
    "संथाली — Santali",
    "کٲشُر — Kashmiri",
]

LANGUAGE_CODES = {
    "English": "en",
    "हिन्दी — Hindi": "hi",
    "मराठी — Marathi": "mr",
    "தமிழ் — Tamil": "ta",
    "తెలుగు — Telugu": "te",
}

UI_TEXT = {
    "English": {
        "welcome": "Your international cooking assistant",
        "recipe": "Choose your recipe",
        "ingredient": "Enter the missing ingredient",
        "find": "Find Substitutes",
    },
    "हिन्दी — Hindi": {
        "welcome": "आपका अंतरराष्ट्रीय खाना बनाने वाला सहायक",
        "recipe": "अपनी रेसिपी चुनें",
        "ingredient": "अनुपलब्ध सामग्री का नाम लिखें",
        "find": "विकल्प खोजें",
    },
    "मराठी — Marathi": {
        "welcome": "तुमचा आंतरराष्ट्रीय स्वयंपाक सहाय्यक",
        "recipe": "तुमची पाककृती निवडा",
        "ingredient": "उपलब्ध नसलेल्या घटकाचे नाव लिहा",
        "find": "पर्याय शोधा",
    },
    "தமிழ் — Tamil": {
        "welcome": "உங்கள் சர்வதேச சமையல் உதவியாளர்",
        "recipe": "உங்கள் உணவைத் தேர்ந்தெடுக்கவும்",
        "ingredient": "கிடைக்காத பொருளை உள்ளிடவும்",
        "find": "மாற்றுப் பொருட்களைக் கண்டறியவும்",
    },
    "తెలుగు — Telugu": {
        "welcome": "మీ అంతర్జాతీయ వంట సహాయకుడు",
        "recipe": "మీ వంటకాన్ని ఎంచుకోండి",
        "ingredient": "లేని పదార్థాన్ని నమోదు చేయండి",
        "find": "ప్రత్యామ్నాయాలను కనుగొనండి",
    },
}

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🍲 FlavorMate")
st.subheader("Discover the world, one recipe at a time!")

st.write(
    "Welcome to FlavorMate — your personal companion "
    "for discovering delicious recipes from around the world."
)

st.divider()

st.header("🌍 Choose Your Language")

language = st.selectbox(
    "Select your preferred language",
    INDIAN_LANGUAGES,
    key="language_selector",
)

selected_language_code = LANGUAGE_CODES.get(language, "en")

default_text = {
    "welcome": "Your international cooking assistant",
    "recipe": "Choose your recipe",
    "ingredient": "Enter the missing ingredient",
    "find": "Find Substitutes",
}

text_labels = UI_TEXT.get(language, default_text)

st.subheader(text_labels["welcome"])
st.caption(f"Selected language: {language}")

st.info(
    "Recipe translations depend on the translations available "
    "in the database. Languages without implemented translations "
    "currently use English recipe content."
)

st.divider()

# --------------------------------------------------
# GLOBAL RECIPE CARDS
# --------------------------------------------------

st.header("🌎 Explore Global Recipes")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🥗 Vegetable Poha")
    st.write("Cuisine: Indian")
    st.write("⏱️ 20 minutes")

    if st.button("View Poha Recipe", key="view_poha"):
        st.session_state["selected_recipe"] = "poha"

with col2:
    st.markdown("### 🍕 Margherita Pizza")
    st.write("Cuisine: Italian")
    st.write("⏱️ 30 minutes")

    if st.button("View Pizza Recipe", key="view_pizza"):
        st.session_state["selected_recipe"] = "pizza"

with col3:
    st.markdown("### 🍚 Vegetable Fried Rice")
    st.write("Cuisine: Chinese")
    st.write("⏱️ 25 minutes")

    if st.button("View Fried Rice Recipe", key="view_rice"):
        st.session_state["selected_recipe"] = "rice"

selected = st.session_state.get("selected_recipe")

if selected == "poha":
    st.header("🥗 Vegetable Poha")
    st.write(
        "**Ingredients:** poha, onion, potato, peanuts, turmeric"
    )
    st.write("1. Wash the poha gently.")
    st.write("2. Cook onion and potato in a pan.")
    st.write("3. Add turmeric, salt and poha.")
    st.write("4. Mix well and serve hot.")

elif selected == "pizza":
    st.header("🍕 Margherita Pizza")
    st.write(
        "**Ingredients:** pizza base, tomato sauce, mozzarella, basil"
    )
    st.write("1. Spread tomato sauce on the base.")
    st.write("2. Add cheese and basil.")
    st.write("3. Bake until the cheese melts.")

elif selected == "rice":
    st.header("🍚 Vegetable Fried Rice")
    st.write(
        "**Ingredients:** cooked rice, carrot, beans, "
        "capsicum, soy sauce"
    )
    st.write("1. Chop the vegetables.")
    st.write("2. Stir-fry the vegetables.")
    st.write("3. Add rice and soy sauce.")
    st.write("4. Mix well and serve.")

st.divider()

# --------------------------------------------------
# INGREDIENT SUBSTITUTE FINDER
# --------------------------------------------------

st.header("🥗 Ingredient Substitute Finder")
st.write("Missing an ingredient? Find a possible alternative.")

missing_ingredient = st.text_input(
    text_labels["ingredient"],
    placeholder="Example: pine nuts",
    key="missing_ingredient",
)

if st.button(text_labels["find"], key="find_substitutes"):
    if not missing_ingredient.strip():
        st.warning("Please enter an ingredient first.")
    else:
        try:
            result = get_substitution_advice(
                missing_ingredient.strip()
            )

            st.write(result["message"])

            if result["substitutes"]:
                for item in result["substitutes"]:
                    st.subheader(item["ingredient"].title())
                    st.write(
                        "**Suggested quantity ratio:**",
                        item["ratio"],
                    )
                    st.write("**Why it may work:**", item["reason"])
                    st.write(
                        "**Taste or texture difference:**",
                        item["difference"],
                    )
            else:
                st.info(
                    "This ingredient is not in our starter "
                    "database yet."
                )

        except Exception as error:
            st.error(f"Substitution search failed: {error}")

st.divider()

# --------------------------------------------------
# RECIPE-SPECIFIC SUBSTITUTE FINDER
# --------------------------------------------------

st.header("🍲 Recipe-Specific Substitute Finder")
st.write("Find alternatives suited to the dish you're preparing.")

recipe_name = st.selectbox(
    text_labels["recipe"],
    ["Pesto", "Pizza", "Pancakes"],
    key="substitution_recipe",
)

ingredient_name = st.text_input(
    "Enter the missing ingredient",
    placeholder="Example: pine nuts",
    key="recipe_missing_ingredient",
)

if st.button(
    "Find Recipe-Specific Substitutes",
    key="recipe_substitutes",
):
    if not ingredient_name.strip():
        st.warning("Please enter the missing ingredient.")
    else:
        try:
            result = find_recipe_substitutes(
                recipe_name,
                ingredient_name.strip(),
            )

            st.write(result["message"])

            if result["substitutes"]:
                for item in result["substitutes"]:
                    st.subheader(item["ingredient"].title())
                    st.write("**Quantity ratio:**", item["ratio"])
                    st.write("**Why it works:**", item["reason"])
                    st.write(
                        "**Expected difference:**",
                        item["difference"],
                    )
            else:
                st.info("Try another ingredient or recipe.")

        except Exception as error:
            st.error(
                f"Recipe-specific substitution search failed: {error}"
            )

st.divider()

# --------------------------------------------------
# DATABASE-POWERED RECIPE FINDER
# --------------------------------------------------

st.header("🍽️ FlavorMate Recipe Finder")
st.write("Search for recipes by name, cuisine, or ingredient.")

recipe_query = st.text_input(
    "What would you like to cook?",
    placeholder="Try pizza, pasta, pancakes, or mozzarella",
    key="recipe_search_query",
)

if st.button("Search Recipes", key="search_recipes_button"):
    if not recipe_query.strip():
        st.warning("Please enter a recipe name or ingredient.")
    else:
        try:
            all_recipes = get_recipes_in_language(
                selected_language_code
            )

            query = recipe_query.strip().casefold()

            recipes = [
                recipe
                for recipe in all_recipes
                if query in str(recipe.get("name", "")).casefold()
                or query in str(recipe.get("cuisine", "")).casefold()
                or any(
                    query in str(ingredient).casefold()
                    for ingredient in recipe.get("ingredients", [])
                )
            ]

            if recipes:
                st.success(f"Found {len(recipes)} recipe(s)!")

                for recipe in recipes:
                    with st.expander(recipe["name"]):
                        st.write("**Cuisine:**", recipe["cuisine"])

                        st.write("**Ingredients:**")
                        for ingredient in recipe["ingredients"]:
                            st.write(f"- {ingredient}")

                        st.write("**Instructions:**")
                        for number, step in enumerate(
                            recipe["instructions"], start=1
                        ):
                            st.write(f"{number}. {step}")
            else:
                st.warning(
                    "No recipes found. Try pizza, pasta, pancakes, "
                    "or an ingredient such as mozzarella."
                )

        except Exception as error:
            st.error(f"Could not load recipes: {error}")

st.divider()
st.caption("FlavorMate | Made with ❤️ and Streamlit")
