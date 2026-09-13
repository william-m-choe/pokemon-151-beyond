import requests
import pandas as pd

pokemon_data = []

# Get the total number of Pokémon species dynamically
species_count_url = "https://pokeapi.co/api/v2/pokemon-species?limit=1"
response = requests.get(species_count_url)
response.raise_for_status()

species_count = response.json()["count"]
print(f"Total Pokémon species found: {species_count}")

# Get the full list of Pokémon species
species_list_url = (
    f"https://pokeapi.co/api/v2/pokemon-species?limit={species_count}"
)
response = requests.get(species_list_url)
response.raise_for_status()

species_list = response.json()["results"]

# Collect data for every Pokémon species
for index, species in enumerate(species_list, start=1):

    # Get species information
    species_response = requests.get(species["url"])
    species_response.raise_for_status()
    species_data = species_response.json()

    # Find the default form for the species
    default_variety = next(
        variety
        for variety in species_data["varieties"]
        if variety["is_default"]
    )

    # Get Pokémon stats/details
    pokemon_response = requests.get(default_variety["pokemon"]["url"])
    pokemon_response.raise_for_status()
    pokemon = pokemon_response.json()

    # Extract base stats
    stats = {
        stat["stat"]["name"]: stat["base_stat"]
        for stat in pokemon["stats"]
    }

    # Extract types
    types = [
        pokemon_type["type"]["name"]
        for pokemon_type in pokemon["types"]
    ]

    # Extract generation
    generation = species_data["generation"]["name"]

    pokemon_data.append({
        "id": species_data["id"],
        "name": pokemon["name"],
        "generation": generation,
        "height": pokemon["height"],
        "weight": pokemon["weight"],
        "base_experience": pokemon["base_experience"],
        "hp": stats["hp"],
        "attack": stats["attack"],
        "defense": stats["defense"],
        "special_attack": stats["special-attack"],
        "special_defense": stats["special-defense"],
        "speed": stats["speed"],
        "type_1": types[0],
        "type_2": types[1] if len(types) > 1 else None,
    })

    print(f"[{index}/{species_count}] Collected: {pokemon['name']}")


# Create DataFrame
df = pd.DataFrame(pokemon_data)

# -----------------------------
# Data Quality Checks
# -----------------------------

print("\n--- Data Quality Checks ---")

# Check for duplicate Pokémon IDs
duplicate_ids = df["id"].duplicated().sum()
print("Duplicate IDs:", duplicate_ids)

# Check for missing values
print("\nMissing values:")
print(df.isnull().sum())

# Check that Pokémon IDs are unique
print("\nUnique Pokémon IDs:", df["id"].nunique())

# Check expected number of Pokémon
print("Number of Pokémon:", len(df))

# Check numeric fields for negative values
numeric_columns = [
    "height",
    "weight",
    "base_experience",
    "hp",
    "attack",
    "defense",
    "special_attack",
    "special_defense",
    "speed",
]

negative_values = (df[numeric_columns] < 0).sum()

print("\nNegative values:")
print(negative_values)

# -----------------------------
# Data Transformation
# -----------------------------

# Calculate total base stats
df["total_stats"] = (
    df["hp"]
    + df["attack"]
    + df["defense"]
    + df["special_attack"]
    + df["special_defense"]
    + df["speed"]
)

# Convert generation names into readable labels
generation_map = {
    "generation-i": "Gen 1",
    "generation-ii": "Gen 2",
    "generation-iii": "Gen 3",
    "generation-iv": "Gen 4",
    "generation-v": "Gen 5",
    "generation-vi": "Gen 6",
    "generation-vii": "Gen 7",
    "generation-viii": "Gen 8",
    "generation-ix": "Gen 9",
}

df["generation"] = df["generation"].map(generation_map)

# Convert API height from decimeters to meters
df["height_m"] = df["height"] / 10

# Convert API weight from hectograms to kilograms
df["weight_kg"] = df["weight"] / 10

# Create a readable type combination
df["type_combination"] = df["type_1"]

df.loc[df["type_2"].notna(), "type_combination"] = (
    df["type_1"] + " / " + df["type_2"]
)

print("\n--- Cleaned Data ---")
print(
    df[
        [
            "name",
            "generation",
            "height_m",
            "weight_kg",
            "type_combination",
            "total_stats",
        ]
    ].head()
)


print("\n--- DataFrame Info ---")
df.info()

print("\n--- First 5 Pokémon ---")
print(df.head())

print("\n--- Top 10 Pokémon by Total Stats ---")
print(
    df[["name", "type_1", "type_2", "total_stats"]]
    .sort_values("total_stats", ascending=False)
    .head(10)
)

# Save dataset
df.to_csv("data/pokemon_clean.csv", index=False)

print("\nSaved cleaned data to data/pokemon_clean.csv")

print("\n--- Top 10 Pokémon by Attack ---")

top_attack = (
    df[["name", "type_combination", "attack"]]
    .sort_values("attack", ascending=False)
    .head(10)
)

print(top_attack)