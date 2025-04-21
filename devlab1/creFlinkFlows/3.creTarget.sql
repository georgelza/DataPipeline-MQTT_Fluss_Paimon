USE CATALOG fluss_catalog;

SET 'sql-client.execution.result-mode' = 'tableau';
SET 'parallelism.default' = '2';
SET 'sql-client.verbose' = 'true';

CREATE TABLE player_profiles (
    player_id STRING,
    username STRING,
    email STRING,
    signup_date TIMESTAMP(3),
    country STRING,
    PRIMARY KEY (player_id) NOT ENFORCED
) WITH ('bucket.num' = '3', 'table.datalake.enabled' = 'true');

INSERT INTO player_profiles SELECT * FROM hive_catalog.faker.player_profiles;

CREATE TABLE games (
    game_id STRING,
    title STRING,
    genre STRING,
    release_date TIMESTAMP(3),
    developer STRING,
    PRIMARY KEY (game_id) NOT ENFORCED
) WITH ('bucket.num' = '3', 'table.datalake.enabled' = 'true');

INSERT INTO games SELECT * FROM hive_catalog.faker.games;

CREATE TABLE gameplay_events (
    event_id STRING,
    player_id STRING,
    game_id STRING,
    score INT,
    proc_time AS PROCTIME(),
    event_time TIMESTAMP(3),
    event_type STRING,
       WATERMARK FOR event_time AS event_time - INTERVAL '5' SECOND
) WITH ('bucket.num' = '3', 'bucket.key' = 'player_id', 'table.datalake.enabled' = 'true');

INSERT INTO gameplay_events SELECT * FROM hive_catalog.faker.gameplay_events;

CREATE TABLE top3_leaderboard (
    ranking BIGINT,
    game_id STRING,
    player_id STRING,
    max_score BIGINT,
    proc_time AS PROCTIME(),
    PRIMARY KEY (ranking, game_id) NOT ENFORCED
) WITH ('bucket.num' = '3', 'table.datalake.enabled' = 'true');


INSERT INTO top3_leaderboard
WITH aggregated_scores AS (SELECT player_id,
                                  game_id,
                                  MAX(score)                                      AS max_score, 
                                  TUMBLE_START(event_time, INTERVAL '60' SECONDS) AS window_start
                           FROM gameplay_events
                           GROUP BY TUMBLE(event_time, INTERVAL '60' SECONDS ),
                                    player_id,
                                    game_id)
SELECT *
FROM (
    SELECT  
        ROW_NUMBER() OVER (PARTITION BY game_id ORDER BY max_score DESC) AS ranking,
        game_id,
        player_id,
        max_score
    FROM aggregated_scores)
WHERE ranking <= 3;


CREATE TABLE top3_leaderboard_enriched (
    game_id STRING,
    ranking BIGINT,
    player_id STRING,
    max_score BIGINT,
    username STRING,
    email STRING,
    title STRING,
    genre STRING,
    PRIMARY KEY (game_id, ranking) NOT ENFORCED
) WITH ('bucket.num' = '3', 'table.datalake.enabled' = 'true');

INSERT INTO top3_leaderboard_enriched
SELECT
    tl.game_id,
    tl.ranking,
    tl.player_id,
    tl.max_score,
    pp.username,
    pp.email,
    g.title,
    g.genre
FROM top3_leaderboard tl
 JOIN player_profiles FOR SYSTEM_TIME AS OF tl.proc_time AS pp
    ON tl.player_id = pp.player_id
 JOIN games FOR SYSTEM_TIME AS OF tl.proc_time AS g
    ON tl.game_id = g.game_id;
