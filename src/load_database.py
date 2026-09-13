import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load environment variables from .env
load_dotenv()

database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise ValueError("DATABASE_URL was not found in the .env file.")

# Connect to PostgreSQL
engine = create_engine(database_url)

# Find the CSV relative to the project folder
project_root = Path(__file__).resolve().parent.parent
csv_path = project_root / "data" / "pokemon_clean.csv"

# Load cleaned Pokémon data
df = pd.read_csv(csv_path)

# Clear existing records while keeping the PostgreSQL table and view
with engine.begin() as connection:
    connection.execute(text("TRUNCATE TABLE pokemon;"))

# Load data into PostgreSQL
df.to_sql(
    "pokemon",
    engine,
    if_exists="append",
    index=False
)

print(f"Loaded {len(df)} Pokémon into PostgreSQL.")