USE CATALOG hive_catalog;

SET 'sql-client.execution.result-mode' = 'tableau';
SET 'parallelism.default' = '2';
SET 'sql-client.verbose' = 'true';


CREATE TABLE  hive_catalog.faker.player_profiles (
    player_id STRING,
    username STRING,
    email STRING,
    signup_date TIMESTAMP(3),
    country STRING
) WITH (
    'connector' = 'faker',
    'fields.player_id.expression' = '#{regexify ''(PL)[0-9]{5}''}',
    'fields.username.expression' = '#{name.username}',
    'fields.email.expression' = '#{Internet.emailAddress}',
    'fields.signup_date.expression' = '#{date.past ''1000'',''DAYS''}',
    'fields.country.expression' = '#{Address.country}'
);



CREATE TABLE hive_catalog.faker.games (
                       game_id STRING,
                       title STRING,
                       genre STRING,
                       release_date TIMESTAMP(3),
                       developer STRING
) WITH (
      'connector' = 'faker',
      'fields.game_id.expression' = '#{regexify ''(GM)[0-9]{5}''}',
      'fields.title.expression' = '#{GameOfThrones.house}',
      'fields.genre.expression' = '#{regexify ''(Action|Adventure|Puzzle|Strategy|Simulation){1}''}',
      'fields.release_date.expression' = '#{date.past ''1000'',''DAYS''}',
      'fields.developer.expression' = '#{Company.name}'
      );


CREATE TABLE hive_catalog.faker.gameplay_events (
                                 event_id STRING,
                                 player_id STRING,
                                 game_id STRING,
                                 score INT,
                                 event_time TIMESTAMP(3),
                                 event_type STRING
) WITH (
      'connector' = 'faker',
      'fields.event_id.expression' = '#{Internet.uuid}',
      'fields.player_id.expression' = '#{regexify ''(PL)[0-9]{5}''}',
      'fields.game_id.expression' = '#{regexify ''(GM)[0-9]{5}''}',
      'fields.score.expression'     = '#{number.numberBetween ''0'',''5000''}',
      'fields.event_time.expression' = '#{date.past ''30'',''SECONDS''}',
      'fields.event_type.expression' = '#{regexify ''(start_session|end_session|achievement|level_up){1}''}'
      );




