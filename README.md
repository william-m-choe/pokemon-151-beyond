# Pokémon 151 & Beyond

An end-to-end analytics application exploring how Pokémon base stats have changed across generations and whether the original 151 Pokémon still rank among the strongest today.

## Live Demo

[View the deployed application](https://pokemon-151-beyond.onrender.com/app)

## Project Question

I grew up with the original 151 Pokémon and wanted to answer:

> What does the Pokémon world look like now, and which Pokémon are actually the strongest?

For this project, "strongest" is defined using total base stats across six core attributes:

- HP
- Attack
- Defense
- Special Attack
- Special Defense
- Speed

## Data Source

Data is sourced from https://pokeapi.co/.

The project analyzes 1,025 Pokémon species across Generations 1–9.

## Architecture

PokéAPI
   ↓
Python + Requests
   ↓
Pandas cleaning & transformation
   ↓
CSV dataset
   ↓
PostgreSQL
   ↓
SQL analytics
   ↓
FastAPI REST API
   ↓
OpenAI-powered AI Analyst
   ↓
Web Frontend

Tableau Public
   ↓
Interactive Analytics Dashboard

## Technologies

- Python
- Pandas
- Requests
- PostgreSQL
- SQL
- SQLAlchemy
- FastAPI
- OpenAI API
- HTML / CSS / JavaScript
- Tableau

## Data Pipeline

The Python pipeline retrieves Pokémon species data from PokéAPI and transforms it into an analytics-ready dataset.

The pipeline includes:

1. Pokémon species and generation information
2. Base stats
3. Pokémon types
4. Physical attributes
5. Type combinations
6. Total base stats
7. Overall ranking based on total base stats

The resulting dataset is loaded programmatically into PostgreSQL for analysis.

## SQL Analytics

The SQL analytics layer examines:

1. Average and maximum base stats by generation
2. Generation rankings by average total base stats
3. Original Gen 1 Pokémon ranked against the full dataset
4. Gen 1 representation within the overall top 10%
5. Average total base stats by primary Pokémon type

## AI Analyst

The project includes an AI-powered analyst that allows users to ask natural-language questions about the Pokémon dataset.

Example questions include:

- Which Gen 1 Pokémon are still among the strongest today?
- What are the 5 strongest Pokémon?
- How strong is Mewtwo?
- Which Pokémon generation is strongest on average?

The AI analyst uses the OpenAI API with function calling to determine which project data should be retrieved. The analyst queries PostgreSQL through SQLAlchemy and returns the relevant data to the model for interpretation.

The analyst is explicitly grounded in the project's dataset and defines "strongest" using total base stats.

## Web Application

A lightweight HTML, CSS, and JavaScript frontend provides an interface for interacting with the AI analyst and viewing the Tableau dashboard.

The application connects:

Web Frontend
     ↓
FastAPI
     ↓
AI Analyst
     ↓
OpenAI API
     ↓
SQLAlchemy
     ↓
PostgreSQL

The web application is deployed publicly using Render.

## Tableau Dashboard

The interactive Tableau dashboard includes:

### Average Total Base Stats by Generation

Compares average total base stats across Generations 1–9.

### Top 10 Gen 1 Pokémon by Total Base Stats

Highlights the 10 strongest Gen 1 Pokémon by total base stats.

### Top 100 Pokémon by Total Base Stats — Gen 1 Highlighted

Ranks the strongest Pokémon across all generations while highlighting Gen 1 Pokémon in red.

This visualization directly addresses the project's original question of whether the original 151 still hold up against newer generations.

### Average Total Base Stats by Primary Type

Compares average total base stats across primary Pokémon types.

### Tableau Public

View the interactive Tableau dashboard:

https://public.tableau.com/app/profile/william.choe4079/viz/Pokmon151Beyond/Pokmon151Beyond?publish=yes

## Key Findings

- Gen 9 has the highest average total base stats at 457.4.
- Gen 1 ranks 7th of 9 generations by average total base stats at 407.6.
- Mewtwo is the highest-ranked Gen 1 Pokémon, with 680 total base stats, ranking #3 overall.
- Six Gen 1 Pokémon appear within the overall top 10% under the project's rank-based methodology.
- Dragon has the highest average total base stats among primary types with at least 10 Pokémon, at 490.2.

## Project Status

Complete — Deployed Application

- [x] Extract Pokémon data from PokéAPI
- [x] Clean and transform data with Python/Pandas
- [x] Load data into PostgreSQL programmatically
- [x] Build SQL analytics layer
- [x] Build FastAPI REST endpoints
- [x] Build AI-powered analyst using the OpenAI API
- [x] Create interactive Tableau dashboard
- [x] Build web frontend
- [x] Integrate frontend with FastAPI and AI analyst
- [x] Publish Tableau dashboard to Tableau Public
- [x] Deploy web application publicly
- [ ] Expand analysis and document additional insights

## Methodology Note

This project measures base-stat strength, not competitive battle performance or Pokémon GO performance.

The analysis uses one default Pokémon form per species and calculates total base stats by summing:

HP + Attack + Defense + Special Attack + Special Defense + Speed

The project uses rank-based comparisons when evaluating Gen 1 Pokémon against the full dataset. Ties receive the same rank.
