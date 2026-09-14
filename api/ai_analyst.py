import json
import os

import requests
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

API_BASE_URL = "http://127.0.0.1:8000"

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
    "Use concise, readable paragraphs and bullet points. "
    "Do not use Markdown tables. "
    "Do not mention internal tool names or explain how you called the tools."
)

def get_top_pokemon(limit: int):
    response = requests.get(
        f"{API_BASE_URL}/pokemon/top/{limit}"
    )

    response.raise_for_status()

    return response.json()

def get_pokemon_by_generation(generation: str):
    response = requests.get(
        f"{API_BASE_URL}/pokemon/generation/{generation}"
    )

    response.raise_for_status()

    return response.json()

def get_pokemon(name: str):
    response = requests.get(
        f"{API_BASE_URL}/pokemon/{name}"
    )

    response.raise_for_status()

    return response.json()

def get_generation_stats():
    response = requests.get(
        f"{API_BASE_URL}/generations"
    )

    response.raise_for_status()

    return response.json()

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
                    "output": json.dumps(results),
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