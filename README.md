# Pokémon 151 & Beyond

An end-to-end data analytics project exploring how Pokémon base stats have changed across generations and whether the original 151 Pokémon still rank among the strongest today.

## Project Question

I grew up with the original 151 Pokémon and wanted to answer:

> What does the Pokémon world look like now, and which Pokémon are actually the strongest?

For this project, "strongest" is defined using **total base stats** across six core attributes:

- HP
- Attack
- Defense
- Special Attack
- Special Defense
- Speed

## Data Source

Data is sourced from [PokéAPI](https://pokeapi.co/).

The project currently analyzes **1,025 Pokémon species** across Generations 1–9.

## Data Pipeline

```text
PokéAPI
   ↓
Python + Requests
   ↓
Pandas cleaning & transformation
   ↓
CSV dataset
   ↓
SQLAlchemy
   ↓
PostgreSQL
   ↓
SQL analytics
```

## Technologies

- Python
- Pandas
- Requests
- PostgreSQL
- SQL
- SQLAlchemy

## Current Analysis

The SQL analytics layer currently examines:

1. Average and maximum base stats by generation
2. Generation rankings by average total stats
3. Original Gen 1 Pokémon ranked against the full dataset
4. Gen 1 representation within the overall top 10%
5. Average total stats by primary Pokémon type

## Early Findings

- **Gen 9** has the highest average total base stats at **457.4**.
- **Gen 1** ranks **7th of 9 generations** by average total base stats at **407.6**.
- **Mewtwo** is the highest-ranked Gen 1 Pokémon, with **680 total base stats**, ranking **#3 overall**.
- Six Gen 1 Pokémon appear within the overall top 10% under the project's rank-based methodology.
- **Dragon** has the highest average total base stats among primary types with at least 10 Pokémon, at **490.2**.

## Project Status

**In Progress**

Current focus:

- [x] Extract Pokémon data from PokéAPI
- [x] Clean and transform data with Python/Pandas
- [x] Load data into PostgreSQL programmatically
- [x] Build SQL analytics layer
- [ ] Build FastAPI endpoints
- [ ] Build AI-powered analyst using the OpenAI API
- [ ] Create interactive Tableau dashboard
- [ ] Expand analysis and document final insights

## Methodology Note

This project measures **base-stat strength**, not competitive battle performance or Pokémon GO performance.

The analysis uses one default Pokémon form per species and calculates total base stats by summing HP, Attack, Defense, Special Attack, Special Defense, and Speed.