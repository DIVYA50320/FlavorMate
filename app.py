
import streamlit as st
from backend.recipe_service import (
    get_substitution_advice,
    find_recipe_substitutes,
)
from backend.recipe_service import search_recipes
from backend.recipe_service import get_recipes_in_language
st.set_page_config(
    page_title="FlavorMate",
    page_icon="🍲",
    layout="wide"
)

st.title("🍲 FlavorMate")
st.subheader("Discover the world, one recipe at a time!")

st.write(
    "Welcome to FlavorMate — your personal companion "
    "for discovering delicious recipes from around the world."
)

st.divider()

st.header("🔎 Find Your Next Recipe")


st.divider()
st.header("🍽️ FlavorMate Recipe Finder")
st.write("Search for recipes by name, cuisine, or ingredient.")

recipe_query = st.text_input(
    "What would you like to cook?",
    placeholder="Try pizza, pasta, or pancakes",
    key="recipe_search_query"
)

if st.button("Search Recipes", key="search_recipes_button"):
    if recipe_query.strip():
        all_recipes = get_recipes_in_language(
            selected_language_code
        )

        query = recipe_query.strip().casefold()

        recipes = [
            recipe for recipe in all_recipes
            if query in recipe["name"].casefold()
            or query in recipe["cuisine"].casefold()
            or any(
                query in ingredient.casefold()
                for ingredient in recipe["ingredients"]
            )
        ]

        if recipes:
            st.success(f"Found {len(recipes)} recipe(s)!")

            for recipe in recipes:
                with st.expander(recipe["name"]):
                    st.write("**Cuisine:**", recipe["cuisine"])

                    st.write("**Ingredients:**")
                    for ingredient in recipe["ingredients"]:
                        st.write(f"- {ingredient.title()}")

                    st.write("**Instructions:**")
                    for step_number, step in enumerate(
                        recipe["instructions"], start=1
                    ):
                        st.write(f"{step_number}. {step}")
        else:
            st.warning(
                "No recipes found. Try pizza, pasta, pancakes, "
                "or an ingredient such as mozzarella."
            )
    else:
        st.warning("Please enter a recipe name or ingredient.")
