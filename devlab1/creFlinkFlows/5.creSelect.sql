USE CATALOG fluss_catalog;

SET 'sql-client.execution.result-mode' = 'tableau';
SET 'parallelism.default' = '2';
SET 'sql-client.verbose' = 'true';
SET 'execution.runtime-mode' = 'batch';
SET 'table.display.max-column-width' = '100';

SELECT * FROM top3_leaderboard_enriched ORDER BY game_id, ranking LIMIT 20;

SELECT * FROM games LIMIT 10;

SELECT * FROM games WHERE game_id='GM00011';

UPDATE games SET `genre` = 'Simulation' WHERE game_id='GM00011';

SELECT * FROM player_profiles LIMIT 10;

SELECT * FROM player_profiles WHERE player_id='PL00002';

DELETE FROM player_profiles WHERE player_id='PL00002';

SET 'execution.runtime-mode' = 'streaming';

