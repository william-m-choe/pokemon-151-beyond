import json
import os

from dotenv import load_dotenv
from openai import OpenAI
from sqlalchemy import create_engine, text


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgres://", "postgresql+psycopg://", 1
    )
elif DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgresql://", "postgresql+psycopg://", 1
    )

engine = create_engine(DATABASE_URL)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


SYSTEM_INSTRUCTIONS = (
    "You are the AI analyst for the Pokémon 151 & Beyond project. "
    "Use the project's data when answering Pokémon analytics questions. "
    "In this project, 'strongest' means highest total base stats, "
    "calculated as HP + Attack + Defense + Special Attack + "
    "Special Defense + Speed. "
    "Do not claim that base-stat strength represents competitive "
    "battle performance or Pokémon GO performance. "

    "When data is provided by a tool, base your answer only on that data. "
    "Do not add Pokémon, forms, statistics, rankings, or facts that were not "
    "returned by the available tools. "
    "Only offer analyses that can be performed using the available tools. "

    "When rank and population data are available, add useful analytical "
    "context such as 'top 0.3% overall' or 'top 0.7% of Gen 1'. "
    "Use the percentages provided by the data rather than inventing or "
    "estimating percentages yourself. "

    "Make answers engaging and conversational while remaining analytical. "
    "When the data supports a strong finding, use light personality and "
    "Pokémon-themed language such as 'a force to be reckoned with', "
    "'heavy hitter', 'stands out', or 'punches above its generation'. "
    "Do not overdo the humor, and do not imply competitive battle performance "
    "unless the data specifically supports such a conclusion. "

    "Lead with the most interesting finding when possible. "
    "For specific Pokémon, prioritize total base stats, overall rank, "
    "generation rank, top-percent context, and notable individual stats. "
    "For generation comparisons, highlight meaningful differences and trends "
    "rather than simply listing numbers. "

    "Use concise, readable paragraphs and bullet points. "
    "Do not use Markdown tables. "
    "Do not mention internal tool names or explain how you called the tools. "

    "When comparing generations or statistics, only describe a value as highest, "
    "lowest, or a record if it is directly supported by comparing all relevant "
    "data returned by the tool. Do not make unsupported comparative claims."
)


def get_top_pokemon(limit: int):
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


def get_pokemon(name: str):
    query = text("""
        WITH ranked AS (
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
                total_stats,
                RANK() OVER (
                    ORDER BY total_stats DESC
                ) AS overall_rank,
                RANK() OVER (
                    PARTITION BY generation
                    ORDER BY total_stats DESC
                ) AS generation_rank,
                COUNT(*) OVER () AS total_pokemon,
                COUNT(*) OVER (
                    PARTITION BY generation
                ) AS generation_count
            FROM pokemon
        )
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
            total_stats,
            overall_rank,
            generation_rank,
            total_pokemon,
            generation_count
        FROM ranked
        WHERE LOWER(name) = LOWER(:name)
    """)

    with engine.connect() as connection:
        result = connection.execute(
            query,
            {"name": name}
        ).mappings().first()

    if result is None:
        return {
            "error": f"Pokémon '{name}' not found"
        }

    result = dict(result)

    result["overall_top_percent"] = round(
        result["overall_rank"] / result["total_pokemon"] * 100,
        1
    )

    result["generation_top_percent"] = round(
        result["generation_rank"] / result["generation_count"] * 100,
        1
    )

    return result


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


tools = [
    {
        "type": "function",
        "name": "get_top_pokemon",
        "description": "Get the strongest Pokémon ranked by total base stats.",
        "parameters": {
            "type": "object",
            "properties": {
                "limit": {
                    "type": "integer",
                    "description": "Number of Pokémon to return.",
                    "minimum": 1,
                    "maximum": 100,
                }
            },
            "required": ["limit"],
        },
    },
    {
        "type": "function",
        "name": "get_pokemon_by_generation",
        "description": "Get Pokémon from a specific generation ranked by total base stats.",
        "parameters": {
            "type": "object",
            "properties": {
                "generation": {
                    "type": "string",
                    "description": "Pokémon generation, such as Gen 1, Gen 2, or Gen 9.",
                }
            },
            "required": ["generation"],
        },
    },
    {
        "type": "function",
        "name": "get_pokemon",
        "description": "Get the detailed base stats and information for a specific Pokémon.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name of the Pokémon to look up.",
                }
            },
            "required": ["name"],
        },
    },
    {
        "type": "function",
        "name": "get_generation_stats",
        "description": "Get average and maximum total base stats for each Pokémon generation.",
        "parameters": {
            "type": "object",
            "properties": {},
        },
    },
]


def ask_ai(question: str) -> str:

    response = client.responses.create(
        model="gpt-5.6-luna",
        instructions=SYSTEM_INSTRUCTIONS,
        input=question,
        tools=tools,
    )

    while True:

        function_calls = [
            item
            for item in response.output
            if item.type == "function_call"
        ]

        if not function_calls:
            return response.output_text

        tool_outputs = []

        for item in function_calls:

            arguments = json.loads(item.arguments)

            if item.name == "get_top_pokemon":
                results = get_top_pokemon(arguments["limit"])

            elif item.name == "get_pokemon_by_generation":
                results = get_pokemon_by_generation(
                    arguments["generation"]
                )

            elif item.name == "get_pokemon":
                results = get_pokemon(
                    arguments["name"]
                )

            elif item.name == "get_generation_stats":
                results = get_generation_stats()

            else:
                continue

            tool_outputs.append(
                {
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": json.dumps(results, default=str),
                }
            )

        response = client.responses.create(
            model="gpt-5.6-luna",
            instructions=SYSTEM_INSTRUCTIONS,
            input=[
                {
                    "role": "user",
                    "content": question,
                },
                *response.output,
                *tool_outputs,
            ],
            tools=tools,
        )


if __name__ == "__main__":

    question = "Which Pokémon generation is strongest on average?"

    answer = ask_ai(question)

    print("\nAI Analyst:")
    print(answer)