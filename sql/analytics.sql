-- ============================================
-- Pokémon 151 & Beyond
-- SQL Analytics
-- ============================================


-- ============================================
-- Ranking view
-- ============================================

CREATE OR REPLACE VIEW pokemon_rankings AS
SELECT
    id,
    name,
    generation,
    type_1,
    type_2,
    type_combination,
    hp,
    attack,
    defense,
    special_attack,
    special_defense,
    speed,
    total_stats,
    RANK() OVER (ORDER BY total_stats DESC) AS overall_rank
FROM pokemon;


-- 1. Generation-level statistics
-- Compare average and maximum base stats across generations.

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
ORDER BY generation;


-- 2. Rank generations by average total stats

SELECT
    generation,
    ROUND(AVG(total_stats), 1) AS avg_total_stats,
    RANK() OVER (ORDER BY AVG(total_stats) DESC) AS strength_rank
FROM pokemon
GROUP BY generation
ORDER BY strength_rank;


-- 3. Rank Gen 1 Pokémon against the entire dataset

SELECT
    name,
    generation,
    type_combination,
    total_stats,
    overall_rank
FROM (
    SELECT
        name,
        generation,
        type_combination,
        total_stats,
        RANK() OVER (ORDER BY total_stats DESC) AS overall_rank
    FROM pokemon
) ranked
WHERE generation = 'Gen 1'
ORDER BY overall_rank;


-- 4. Gen 1 Pokémon in the top 10% by overall rank

SELECT
    name,
    type_combination,
    total_stats,
    overall_rank
FROM pokemon_rankings
WHERE generation = 'Gen 1'
  AND overall_rank <= (
      SELECT COUNT(*) * 0.10
      FROM pokemon
  )
ORDER BY overall_rank;


-- 5. Average stats by primary Pokémon type
-- Only include types with at least 10 Pokémon.

SELECT
    type_1,
    COUNT(*) AS pokemon_count,
    ROUND(AVG(total_stats), 1) AS avg_total_stats,
    MAX(total_stats) AS max_total_stats
FROM pokemon
GROUP BY type_1
HAVING COUNT(*) >= 10
ORDER BY avg_total_stats DESC;