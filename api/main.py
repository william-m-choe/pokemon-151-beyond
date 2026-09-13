import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, text

load_dotenv()

database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise ValueError("DATABASE_URL was not found in the .env file.")

engine = create_engine(database_url)

app = FastAPI(
    title="Pokémon 151 & Beyond API",
    description="API for querying Pokémon analytics data",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "message": "Pokémon 151 & Beyond API is running"
    }


@app.get("/pokemon/{name}")
def get_pokemon(name: str):
    query = text("""
        SELECT
            name,
            generation,
            type_combination,
            hp,
            attack,
            defense,
            special_attack,
            special_defense,
            speed,
            total_stats
        FROM pokemon
        WHERE LOWER(name) = LOWER(:name)
    """)

    with engine.connect() as connection:
        result = connection.execute(
            query,
            {"name": name}
        ).mappings().first()

    if result is None:
        raise HTTPException(
            status_code=404,
            detail=f"Pokémon '{name}' not found"
        )

    return dict(result)


@app.get("/pokemon/top/{limit}")
def get_top_pokemon(limit: int):
    if limit < 1 or limit > 100:
        raise HTTPException(
            status_code=400,
            detail="Limit must be between 1 and 100"
        )

    query = text("""
        SELECT
            name,
            generation,
            type_combination,
            total_stats,
            overall_rank
        FROM pokemon_rankings
        ORDER BY overall_rank
        LIMIT :limit
    """)

    with engine.connect() as connection:
        results = connection.execute(
            query,
            {"limit": limit}
        ).mappings().all()

    return [dict(row) for row in results]


@app.get("/pokemon/generation/{generation}")
def get_pokemon_by_generation(generation: str):
    query = text("""
        SELECT
            name,
            generation,
            type_combination,
            total_stats,
            overall_rank
        FROM pokemon_rankings
        WHERE LOWER(generation) = LOWER(:generation)
        ORDER BY overall_rank
    """)

    with engine.connect() as connection:
        results = connection.execute(
            query,
            {"generation": generation}
        ).mappings().all()

    return [dict(row) for row in results]


@app.get("/generations")
def get_generation_stats():
    query = text("""
        SELECT
            generation,
            COUNT(*) AS pokemon_count,
            ROUND(AVG(total_stats), 1) AS avg_total_stats,
            MAX(total_stats) AS max_total_stats,
            ROUND(AVG(attack), 1) AS avg_attack,
            ROUND(AVG(defense), 1) AS avg_defense,
            ROUND(AVG(hp), 1) AS avg_hp
        FROM pokemon
        GROUP BY generation
        ORDER BY avg_total_stats DESC
    """)

    with engine.connect() as connection:
        results = connection.execute(query).mappings().all()

    return [dict(row) for row in results]