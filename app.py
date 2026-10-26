import json
from urllib.parse import quote_plus
import os
import requests
GROQ_API_KEY = "your_actual_groq_api_key"


import streamlit as st
import streamlit.components.v1 as components

try:
    from backend.recipe_service import (
        get_substitution_advice,
        find_recipe_substitutes,
        get_recipes_in_language,
    )
except Exception:
    get_substitution_advice = None
    find_recipe_substitutes = None
    get_recipes_in_language = None



st.set_page_config(
    page_title="FlavorMate | Global Cooking Assistant",
    page_icon="🍲",
    layout="wide",
)

st.markdown(
    """
    <style>
    .main-title {
        font-size: 42px;
        font-weight: 800;
        color: #D97706;
        text-align: center;
    }
    .subtitle {
        text-align: center;
        font-size: 17px;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


LANGUAGES = {
    "English": "en",
    "हिन्दी — Hindi": "hi",
    "অসমীয়া — Assamese": "as",
    "বাংলা — Bengali": "bn",
    "बोडो — Bodo": "brx",
    "डोगरी — Dogri": "doi",
    "ગુજરાતી — Gujarati": "gu",
    "ಕನ್ನಡ — Kannada": "kn",
    "कोंकणी — Konkani": "kok",
    "मैथिली — Maithili": "mai",
    "മലയാളം — Malayalam": "ml",
    "মণিপুরী — Manipuri": "mni",
    "मराठी — Marathi": "mr",
    "नेपाली — Nepali": "ne",
    "ଓଡ଼ିଆ — Odia": "or",
    "ਪੰਜਾਬੀ — Punjabi": "pa",
    "संस्कृतम् — Sanskrit": "sa",
    "سنڌي — Sindhi": "sd",
    "தமிழ் — Tamil": "ta",
    "తెలుగు — Telugu": "te",
    "اردو — Urdu": "ur",
    "संथाली — Santali": "sat",
    "کٲشُر — Kashmiri": "ks",
}

UI_TRANSLATIONS = {
    "English": {
        "welcome": "Your international cooking companion",
        "search": "Search recipes",
        "upload": "Upload a recipe",
    },
    "हिन्दी — Hindi": {
        "welcome": "आपका अंतरराष्ट्रीय खाना बनाने का साथी",
        "search": "रेसिपी खोजें",
        "upload": "रेसिपी अपलोड करें",
    },
    "मराठी — Marathi": {
        "welcome": "तुमचा आंतरराष्ट्रीय स्वयंपाक सोबती",
        "search": "पाककृती शोधा",
        "upload": "पाककृती अपलोड करा",
    },
    "ગુજરાતી — Gujarati": {
        "welcome": "તમારો આંતરરાષ્ટ્રીય રસોઈ સહાયક",
        "search": "વાનગીઓ શોધો",
        "upload": "વાનગી અપલોડ કરો",
    },
    "தமிழ் — Tamil": {
        "welcome": "உங்கள் சர்வதேச சமையல் துணை",
        "search": "சமையல் குறிப்புகளைத் தேடுங்கள்",
        "upload": "சமையல் குறிப்பைப் பதிவேற்றவும்",
    },
    "తెలుగు — Telugu": {
        "welcome": "మీ అంతర్జాతీయ వంట సహాయకుడు",
        "search": "వంటకాలను వెతకండి",
        "upload": "వంటకాన్ని అప్‌లోడ్ చేయండి",
    },
    "বাংলা — Bengali": {
        "welcome": "আপনার আন্তর্জাতিক রান্নার সহকারী",
        "search": "রেসিপি খুঁজুন",
        "upload": "রেসিপি আপলোড করুন",
    },
    "ಕನ್ನಡ — Kannada": {
        "welcome": "ನಿಮ್ಮ ಅಂತರರಾಷ್ಟ್ರೀಯ ಅಡುಗೆ ಸಹಾಯಕ",
        "search": "ಪಾಕವಿಧಾನಗಳನ್ನು ಹುಡುಕಿ",
        "upload": "ಪಾಕವಿಧಾನವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ",
    },
    "മലയാളം — Malayalam": {
        "welcome": "നിങ്ങളുടെ അന്താരാഷ്ട്ര പാചക സഹായി",
        "search": "പാചകക്കുറിപ്പുകൾ തിരയുക",
        "upload": "പാചകക്കുറിപ്പ് അപ്‌ലോഡ് ചെയ്യുക",
    },
    "ਪੰਜਾਬੀ — Punjabi": {
        "welcome": "ਤੁਹਾਡਾ ਅੰਤਰਰਾਸ਼ਟਰੀ ਖਾਣਾ ਬਣਾਉਣ ਵਾਲਾ ਸਹਾਇਕ",
        "search": "ਪਕਵਾਨ ਖੋਜੋ",
        "upload": "ਪਕਵਾਨ ਅੱਪਲੋਡ ਕਰੋ",
    },
    "ଓଡ଼ିଆ — Odia": {
        "welcome": "ଆପଣଙ୍କର ଆନ୍ତର୍ଜାତୀୟ ରନ୍ଧନ ସହାୟକ",
        "search": "ରେସିପି ଖୋଜନ୍ତୁ",
        "upload": "ରେସିପି ଅପଲୋଡ୍ କରନ୍ତୁ",
    },
    "অসমীয়া — Assamese": {
        "welcome": "আপোনাৰ আন্তঃৰাষ্ট্ৰীয় ৰন্ধন সহায়ক",
        "search": "ৰেচিপি বিচাৰক",
        "upload": "ৰেচিপি আপলোড কৰক",
    },
}


STARTER_RECIPES = [
    {
        "name": "Vegetable Poha",
        "cuisine": "Indian",
        "region": "Maharashtra, India",
        "category": "Everyday",
        "time": 20,
        "ingredients": [
            "Flattened rice (poha)", "Onion", "Potato",
            "Peanuts", "Mustard seeds", "Turmeric", "Lemon",
        ],
        "instructions": [
            "Rinse the poha gently and drain it.",
            "Heat oil and temper mustard seeds.",
            "Add onion, potato, peanuts and turmeric; cook until tender.",
            "Mix in poha and salt. Heat gently.",
            "Finish with lemon juice and serve.",
        ],
        "description": "A popular Indian breakfast.",
        "video": "",
        "rare": False,
    },
    {
        "name": "Margherita Pizza",
        "cuisine": "Italian",
        "region": "Naples, Italy",
        "category": "Main course",
        "time": 30,
        "ingredients": [
            "Pizza dough", "Tomato", "Mozzarella",
            "Basil", "Olive oil",
        ],
        "instructions": [
            "Preheat the oven according to your dough recipe.",
            "Spread tomato sauce over the dough.",
            "Add mozzarella and basil.",
            "Bake until the crust is cooked and the cheese melts.",
        ],
        "description": "A classic Neapolitan pizza.",
        "video": "",
        "rare": False,
    },
    {
        "name": "Vegetable Fried Rice",
        "cuisine": "Chinese-inspired",
        "region": "East Asia",
        "category": "Main course",
        "time": 25,
        "ingredients": [
            "Cooked rice", "Carrot", "Beans", "Capsicum",
            "Spring onion", "Soy sauce",
        ],
        "instructions": [
            "Prepare and chop the vegetables.",
            "Stir-fry the vegetables in a hot pan.",
            "Add cooked rice and soy sauce.",
            "Toss thoroughly and serve hot.",
        ],
        "description": "A quick vegetable rice dish.",
        "video": "",
        "rare": False,
    },
    {
        "name": "Pad Thai",
        "cuisine": "Thai",
        "region": "Thailand",
        "category": "Main course",
        "time": 35,
        "ingredients": [
            "Rice noodles", "Tofu", "Bean sprouts", "Egg",
            "Tamarind", "Peanuts", "Lime",
        ],
        "instructions": [
            "Soak the rice noodles according to the package directions.",
            "Prepare a sauce using tamarind and suitable seasonings.",
            "Cook tofu and egg, if using.",
            "Add noodles and sauce; toss until tender.",
            "Serve with bean sprouts, peanuts and lime.",
        ],
        "description": "A well-known Thai noodle dish.",
        "video": "",
        "rare": False,
    },
    {
        "name": "Shakshuka",
        "cuisine": "North African / Middle Eastern",
        "region": "North Africa",
        "category": "Breakfast",
        "time": 30,
        "ingredients": [
            "Eggs", "Tomatoes", "Onion", "Capsicum",
            "Garlic", "Paprika",
        ],
        "instructions": [
            "Cook onion, capsicum and garlic in a pan.",
            "Add chopped tomatoes and spices.",
            "Simmer until the sauce thickens.",
            "Make small wells and add eggs.",
            "Cover and cook until the eggs reach your preferred doneness.",
        ],
        "description": "Eggs cooked in a spiced tomato sauce.",
        "video": "",
        "rare": False,
    },
    {
        "name": "Okonomiyaki",
        "cuisine": "Japanese",
        "region": "Japan",
        "category": "Street food",
        "time": 35,
        "ingredients": [
            "Cabbage", "Flour", "Eggs", "Water",
            "Spring onion", "Optional toppings",
        ],
        "instructions": [
            "Finely shred the cabbage.",
            "Mix cabbage with flour, egg and enough water to form a batter.",
            "Cook portions on a lightly oiled pan.",
            "Flip and cook until both sides are done.",
            "Add your preferred toppings.",
        ],
        "description": "A savoury Japanese cabbage pancake.",
        "video": "",
        "rare": False,
    },
    {
        "name": "Undhiyu",
        "cuisine": "Gujarati",
        "region": "Gujarat, India",
        "category": "Regional",
        "time": 60,
        "ingredients": [
            "Seasonal vegetables", "Surti papdi",
            "Potato", "Eggplant", "Coriander", "Spices",
        ],
        "instructions": [
            "Wash and prepare the seasonal vegetables.",
            "Prepare a coriander-based spice mixture.",
            "Combine the vegetables with the mixture.",
            "Cook covered on low heat until the vegetables are tender.",
            "Check seasoning and serve.",
        ],
        "description": "A traditional mixed-vegetable Gujarati dish.",
        "video": "",
        "rare": False,
    },
    {
        "name": "Fesenjan",
        "cuisine": "Persian",
        "region": "Iran",
        "category": "Traditional",
        "time": 90,
        "ingredients": [
            "Walnuts", "Pomegranate molasses",
            "Onion", "Water or stock", "Chicken or vegetables",
        ],
        "instructions": [
            "Grind the walnuts finely.",
            "Cook onion until softened.",
            "Add walnuts and water or stock.",
            "Stir in pomegranate molasses and your chosen main ingredient.",
            "Simmer gently until rich and thick, checking the seasoning.",
        ],
        "description": "A rich Persian stew with walnut and pomegranate.",
        "video": "",
        "rare": True,
    },
    {
        "name": "Karelian Pies",
        "cuisine": "Finnish",
        "region": "Karelia, Finland",
        "category": "Traditional",
        "time": 75,
        "ingredients": [
            "Rye flour", "Water", "Rice", "Milk", "Salt",
        ],
        "instructions": [
            "Cook rice into a thick porridge using milk and water.",
            "Mix rye flour, water and salt to make a dough.",
            "Roll the dough into thin oval shapes.",
            "Place filling in the centre and fold the edges.",
            "Bake until the crust is cooked through.",
        ],
        "description": "Traditional Finnish pastries with rice porridge filling.",
        "video": "",
        "rare": True,
    },
    {
        "name": "Mujaddara",
        "cuisine": "Levantine",
        "region": "Levant",
        "category": "Traditional",
        "time": 45,
        "ingredients": [
            "Lentils", "Rice", "Onions", "Cumin", "Olive oil",
        ],
        "instructions": [
            "Rinse lentils and simmer until partly tender.",
            "Add rice, water and seasoning.",
            "Cook until both lentils and rice are tender.",
            "Slowly caramelise sliced onions separately.",
            "Serve the lentil-rice mixture topped with onions.",
        ],
        "description": "A comforting lentil and rice dish.",
        "video": "",
        "rare": False,
    },
    {
        "name": "Pakhala Bhata",
        "cuisine": "Odia",
        "region": "Odisha, India",
        "category": "Regional",
        "time": 20,
        "ingredients": [
            "Cooked rice", "Water", "Curd (optional)",
            "Salt", "Green chilli (optional)",
        ],
        "instructions": [
            "Prepare cooked rice and allow it to cool safely.",
            "Add clean drinking water and optional curd.",
            "Season to taste.",
            "Serve with suitable sides.",
        ],
        "description": "A traditional Odisha rice preparation. Fermented versions need appropriate food-safety care.",
        "video": "",
        "rare": False,
    },
    {
        "name": "Hákarl",
        "cuisine": "Icelandic",
        "region": "Iceland",
        "category": "Unusual traditional food",
        "time": 0,
        "ingredients": [
            "Traditionally prepared Greenland shark",
        ],
        "instructions": [
            "This is a traditional fermented food requiring specialised preparation.",
            "Use a reputable, food-safe source rather than attempting to prepare it at home.",
        ],
        "description": "A historically significant Icelandic fermented food, included for cultural discovery rather than beginner cooking.",
        "video": "",
        "rare": True,
    },
]


def normalise_recipe(recipe):
    if not isinstance(recipe, dict):
        return None

    name = recipe.get("name") or recipe.get("recipe_name")
    if not name:
        return None

    ingredients = recipe.get("ingredients", [])
    instructions = recipe.get("instructions", recipe.get("steps", []))

    if isinstance(ingredients, str):
        ingredients = [
            line.strip(" -•")
            for line in ingredients.replace(";", "\n").splitlines()
            if line.strip()
        ]

    if isinstance(instructions, str):
        instructions = [
            line.strip(" -•0123456789.")
            for line in instructions.splitlines()
            if line.strip()
        ]

    if not isinstance(ingredients, list):
        ingredients = []
    if not isinstance(instructions, list):
        instructions = []

    return {
        "name": str(name),
        "cuisine": str(recipe.get("cuisine", "Other")),
        "region": str(recipe.get("region", "Not specified")),
        "category": str(recipe.get("category", "Community")),
        "time": recipe.get("time", recipe.get("cooking_time", 0)),
        "ingredients": [str(x) for x in ingredients],
        "instructions": [str(x) for x in instructions],
        "description": str(recipe.get("description", "")),
        "video": str(recipe.get("video", recipe.get("video_url", ""))),
        "rare": bool(recipe.get("rare", False)),
    }


def load_backend_recipes(language_code):
    if get_recipes_in_language is None:
        return []

    try:
        data = get_recipes_in_language(language_code)
        if not isinstance(data, list):
            return []
        return [
            item for item in
            (normalise_recipe(recipe) for recipe in data)
            if item is not None
        ]
    except Exception:
        return []


def recipe_key(recipe):
    return recipe["name"].strip().casefold()


def get_all_recipes(language_code):
    combined = {}
    for recipe in STARTER_RECIPES + load_backend_recipes(language_code):
        item = normalise_recipe(recipe)
        if item:
            combined[recipe_key(item)] = item

    for recipe in st.session_state.get("uploaded_recipes", []):
        item = normalise_recipe(recipe)
        if item:
            combined[recipe_key(item)] = item

    return list(combined.values())


st.markdown('<div class="main-title">🍲 FlavorMate</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Discover the world, one recipe at a time.</div>',
    unsafe_allow_html=True,
)

language = st.selectbox(
    "🌐 Choose your preferred language",
    list(LANGUAGES.keys()),
    key="language_selector",
)
language_code = LANGUAGES[language]
labels = UI_TRANSLATIONS.get(
    language,
    {
        "welcome": "Your international cooking companion",
        "search": "Search recipes",
        "upload": "Upload a recipe",
    },
)

st.subheader(labels["welcome"])
st.caption(
    f"Interface language: {language}. "
    "Full recipe translation requires a translation service or translated recipe data."
)

st.info(
    "Voice narration uses your browser's speech support. "
    "Available voices and languages depend on your device."
)

st.divider()

recipes = get_all_recipes(language_code)

st.header("🌍 Explore the world's cuisines")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Recipes available", len(recipes))
with col2:
    st.metric(
        "Cuisines",
        len(set(r["cuisine"] for r in recipes)),
    )
with col3:
    st.metric(
        "Rare and traditional",
        sum(bool(r["rare"]) for r in recipes),
    )

query = st.text_input(
    labels["search"],
    placeholder="Try pizza, Persian, lentils, Gujarati, or walnuts",
    key="main_recipe_query",
)

cuisines = ["All"] + sorted(set(r["cuisine"] for r in recipes))
selected_cuisine = st.selectbox("Filter by cuisine", cuisines)

show_rare = st.checkbox("✨ Show only rare or traditional discovery recipes")

def matches_query(recipe, search_term):
    if not search_term:
        return True

    haystack = " ".join(
        [
            recipe["name"],
            recipe["cuisine"],
            recipe["region"],
            recipe["category"],
            recipe["description"],
            " ".join(recipe["ingredients"]),
        ]
    ).casefold()

    return search_term.casefold() in haystack


filtered_recipes = [
    recipe for recipe in recipes
    if matches_query(recipe, query.strip())
    and (
        selected_cuisine == "All"
        or recipe["cuisine"] == selected_cuisine
    )
    and (not show_rare or recipe["rare"])
]

if filtered_recipes:
    st.caption(f"Showing {len(filtered_recipes)} recipe(s).")

    for recipe in filtered_recipes:
        with st.expander(
            f"{'✨ ' if recipe['rare'] else '🍽️ '}{recipe['name']}"
            f" — {recipe['cuisine']}"
        ):
            st.write("**Origin:**", recipe["region"])
            st.write("**Category:**", recipe["category"])

            if recipe["time"]:
                st.write("**Estimated time:**", f"{recipe['time']} minutes")

            if recipe["description"]:
                st.write(recipe["description"])

            st.markdown("#### Ingredients")
            if recipe["ingredients"]:
                for ingredient in recipe["ingredients"]:
                    st.write(f"- {ingredient}")
            else:
                st.info("Ingredients have not been added yet.")

            st.markdown("#### Step-by-step instructions")
            if recipe["instructions"]:
                for index, step in enumerate(recipe["instructions"], start=1):
                    st.write(f"{index}. {step}")
            else:
                st.info("Instructions have not been added yet.")

            narration = (
                f"{recipe['name']}. Ingredients: "
                + ", ".join(recipe["ingredients"])
                + ". Instructions: "
                + ". ".join(recipe["instructions"])
            )

            if st.button(
                f"🔊 Read recipe aloud: {recipe['name']}",
                key=f"voice_{recipe_key(recipe)}",
            ):
                safe_text = json.dumps(narration, ensure_ascii=False)
                components.html(
                    f"""
                    <button onclick="speakRecipe()"
                        style="padding:10px 16px;border-radius:8px;
                        border:1px solid #888;cursor:pointer;">
                        ▶ Play narration
                    </button>
                    <button onclick="window.speechSynthesis.cancel()"
                        style="padding:10px 16px;border-radius:8px;
                        border:1px solid #888;cursor:pointer;">
                        ■ Stop
                    </button>
                    <script>
                    const recipeText = {safe_text};
                    function speakRecipe() {{
                        if (!('speechSynthesis' in window)) {{
                            alert('Speech is not supported by this browser.');
                            return;
                        }}
                        window.speechSynthesis.cancel();
                        const message = new SpeechSynthesisUtterance(recipeText);
                        window.speechSynthesis.speak(message);
                    }}
                    </script>
                    """,
                    height=75,
                )

            video_url = recipe["video"].strip()
            if video_url.startswith(("https://", "http://")):
                st.video(video_url)
            else:
                search_url = (
                    "https://www.youtube.com/results?search_query="
                    + quote_plus(recipe["name"] + " authentic recipe")
                )
                st.markdown(
                    f"[🎥 Search cooking videos for {recipe['name']}]"
                    f"({search_url})"
                )
                st.caption(
                    "This opens a video search, not a verified or embedded recipe video."
                )
else:
    st.warning(
        "No matching recipes were found. Try another name, ingredient, "
        "region, or cuisine."
    )


st.divider()
st.header("🥗 Smart Ingredient Substitute Finder")
st.write(
    "Enter an unavailable ingredient to check the substitution database."
)

missing_ingredient = st.text_input(
    "Ingredient you cannot find",
    placeholder="Example: pine nuts, buttermilk, or mozzarella",
    key="missing_ingredient",
)

if st.button("Find Ingredient Substitutes", key="find_substitutes"):
    if not missing_ingredient.strip():
        st.warning("Please enter an ingredient.")
    elif get_substitution_advice is None:
        st.error("The substitution backend is unavailable.")
    else:
        try:
            result = get_substitution_advice(missing_ingredient.strip())
            st.write(result.get("message", "Substitution results"))

            for item in result.get("substitutes", []):
                st.markdown(f"**{item.get('ingredient', 'Alternative')}**")
                st.write("Quantity ratio:", item.get("ratio", "Not specified"))
                st.write("Why it may work:", item.get("reason", "Not specified"))
                st.write(
                    "Taste or texture difference:",
                    item.get("difference", "Not specified"),
                )

            if not result.get("substitutes"):
                st.info(
                    "No match was found in the current database. "
                    "Try another ingredient name."
                )
        except Exception as error:
            st.error(f"Substitution search failed: {error}")


st.subheader("🍲 Recipe-specific substitutes")

recipe_options = ["Pesto", "Pizza", "Pancakes"]
chosen_recipe = st.selectbox(
    "Which dish are you preparing?",
    recipe_options,
    key="substitution_recipe",
)

missing_for_recipe = st.text_input(
    "Which ingredient is missing?",
    placeholder="Example: pine nuts",
    key="recipe_missing_ingredient",
)

if st.button("Find Dish-Specific Substitutes", key="recipe_substitutes"):
    if not missing_for_recipe.strip():
        st.warning("Please enter the missing ingredient.")
    elif find_recipe_substitutes is None:
        st.error("The recipe substitution backend is unavailable.")
    else:
        try:
            result = find_recipe_substitutes(
                chosen_recipe,
                missing_for_recipe.strip(),
            )
            st.write(result.get("message", "Substitution results"))

            for item in result.get("substitutes", []):
                st.markdown(f"**{item.get('ingredient', 'Alternative')}**")
                st.write("Quantity ratio:", item.get("ratio", "Not specified"))
                st.write("Why it works:", item.get("reason", "Not specified"))
                st.write(
                    "Expected difference:",
                    item.get("difference", "Not specified"),
                )

            if not result.get("substitutes"):
                st.info("No matching substitute was found.")
        except Exception as error:
            st.error(f"Recipe-specific search failed: {error}")


st.divider()
st.header("📤 Share Your Own Recipe")
st.write(
    "Contribute family recipes, regional dishes, international discoveries, "
    "and rare traditional food."
)

with st.form("upload_recipe_form", clear_on_submit=True):
    upload_name = st.text_input("Recipe name")
    upload_cuisine = st.text_input("Cuisine")
    upload_region = st.text_input("Region or country")
    upload_category = st.selectbox(
        "Recipe category",
        ["Everyday", "Traditional", "Regional", "Dessert", "Snack",
         "Main course", "Breakfast", "Rare discovery", "Other"],
    )
    upload_time = st.number_input(
        "Preparation/cooking time in minutes",
        min_value=0,
        max_value=1440,
        value=30,
    )
    upload_ingredients = st.text_area(
        "Ingredients (one per line)",
        placeholder="Rice\nOnion\nSpices",
    )
    upload_steps = st.text_area(
        "Cooking instructions (one step per line)",
        placeholder="Wash the rice.\nCook until tender.",
    )
    upload_description = st.text_area("Story or description")
    upload_video = st.text_input("Optional video URL (https://...)")
    upload_rare = st.checkbox("Mark as a rare or traditional discovery")
    submitted = st.form_submit_button("Add Recipe")

if submitted:
    if not upload_name.strip():
        st.warning("Recipe name is required.")
    elif not upload_ingredients.strip() or not upload_steps.strip():
        st.warning("Please add ingredients and cooking instructions.")
    elif upload_video.strip() and not upload_video.strip().startswith(
        ("https://", "http://")
    ):
        st.warning("Video links must begin with http:// or https://.")
    else:
        new_recipe = {
            "name": upload_name.strip(),
            "cuisine": upload_cuisine.strip() or "Community",
            "region": upload_region.strip() or "Not specified",
            "category": upload_category,
            "time": int(upload_time),
            "ingredients": [
                line.strip()
                for line in upload_ingredients.splitlines()
                if line.strip()
            ],
            "instructions": [
                line.strip()
                for line in upload_steps.splitlines()
                if line.strip()
            ],
            "description": upload_description.strip(),
            "video": upload_video.strip(),
            "rare": upload_rare,
        }

        if "uploaded_recipes" not in st.session_state:
            st.session_state["uploaded_recipes"] = []

        if any(
            recipe["name"].casefold() == new_recipe["name"].casefold()
            for recipe in st.session_state["uploaded_recipes"]
        ):
            st.warning("You have already uploaded a recipe with that name.")
        else:
            st.session_state["uploaded_recipes"].append(new_recipe)
            st.success(
                "Recipe added for this session. "
                "Permanent community publishing needs persistent storage."
            )
            st.rerun()


st.subheader("📚 Import a recipe collection")
st.caption(
    "Upload JSON or CSV containing recipes. Only validated recipe fields "
    "are used. This import is session-only."
)

uploaded_file = st.file_uploader(
    "Choose a recipe file",
    type=["json", "csv"],
    key="recipe_file_upload",
)

if uploaded_file is not None:
    try:
        if uploaded_file.name.lower().endswith(".json"):
            data = json.load(uploaded_file)
            if isinstance(data, dict):
                data = data.get("recipes", [data])
        else:
            import pandas as pd
            data = pd.read_csv(uploaded_file).fillna("").to_dict("records")

        if not isinstance(data, list):
            st.error("The JSON file must contain a list of recipes.")
        else:
            imported = [
                item for item in
                (normalise_recipe(recipe) for recipe in data)
                if item is not None
            ]

            if st.button("Import Valid Recipes", key="confirm_import"):
                if "uploaded_recipes" not in st.session_state:
                    st.session_state["uploaded_recipes"] = []

                existing = {
                    recipe["name"].casefold()
                    for recipe in st.session_state["uploaded_recipes"]
                }

                added = 0
                for recipe in imported:
                    if recipe["name"].casefold() not in existing:
                        st.session_state["uploaded_recipes"].append(recipe)
                        existing.add(recipe["name"].casefold())
                        added += 1

                st.success(f"Imported {added} new recipe(s) for this session.")
                st.rerun()

    except Exception as error:
        st.error(f"Could not read the recipe file: {error}")

st.divider()
st.caption(
    "FlavorMate | Global cuisines • Local discovery • "
    "Ingredient alternatives • Community recipes"
)
st.caption(
    "Food safety: verify unfamiliar ingredients, allergies, "
    "and preparation methods before cooking."
)
