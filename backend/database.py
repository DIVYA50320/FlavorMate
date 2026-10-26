
import sqlite3
from pathlib import Path

# Store the database in the main FlavorMate project folder.
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_DIR / "flavormate.db"


def get_connection():
    """Create a connection to the FlavorMate SQLite database."""
    connection = sqlite3.connect(str(DATABASE_PATH))
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    """Create the required tables if they do not already exist."""
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recipe_key TEXT UNIQUE NOT NULL,
                cuisine TEXT NOT NULL,
                prep_time_minutes INTEGER,
                category TEXT
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS recipe_translations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recipe_id INTEGER NOT NULL,
                language_code TEXT NOT NULL,
                recipe_name TEXT NOT NULL,
                description TEXT,
                FOREIGN KEY (recipe_id) REFERENCES recipes(id),
                UNIQUE (recipe_id, language_code)
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS ingredients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recipe_id INTEGER NOT NULL,
                ingredient_name TEXT NOT NULL,
                quantity TEXT,
                FOREIGN KEY (recipe_id) REFERENCES recipes(id)
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS instruction_translations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recipe_id INTEGER NOT NULL,
                language_code TEXT NOT NULL,
                step_number INTEGER NOT NULL,
                instruction TEXT NOT NULL,
                FOREIGN KEY (recipe_id) REFERENCES recipes(id),
                UNIQUE (recipe_id, language_code, step_number)
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS ingredient_translations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ingredient_id INTEGER NOT NULL,
                language_code TEXT NOT NULL,
                translated_name TEXT NOT NULL,
                FOREIGN KEY (ingredient_id) REFERENCES ingredients(id),
                UNIQUE (ingredient_id, language_code)
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS substitutions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ingredient_name TEXT NOT NULL,
                substitute_name TEXT NOT NULL,
                advice TEXT
            )
        """)


if __name__ == "__main__":
    initialize_database()
    print("FlavorMate database initialized successfully!")
    print(f"Database location: {DATABASE_PATH}")
