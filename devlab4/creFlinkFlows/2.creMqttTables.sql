
/*
    Full IoT Payload

    {
        "ts" : 1729312551000,
        "metadata" : {
            "siteId" : 1009,
            "deviceId" : 1042,
            "sensorId" : 10180,
            "unit" : "Psi",
            "ts_human" : "2024-10-02T00:00:00.869Z",
            "location": {
                "latitude": -26.195246, 
                "longitude": 28.034088
            },
            "deviceType" : "Oil Pump",
        },
        "measurement" : 1013.3997
    }

*/

--- Create source Flink Table's sourced via Flink source connector

SET 'pipeline.name' = 'Factory_iot 101 Source';

CREATE OR REPLACE TABLE hive_catalog.iot.factory_iot_101 (
    ts bigint,
    metadata array<row<
        siteId INTEGER, 
        deviceId INTEGER, 
        sensorId INTEGER, 
        unit STRING, 
        ts_human STRING, 
        location array<row<
            latitude DOUBLE, 
            longitude DOUBLE>>,  
        deviceType STRING>>,
    measurement DOUBLE,
    ts_WM as TO_TIMESTAMP(FROM_UNIXTIME(CAST(`ts` AS BIGINT) / 1000)),
    WATERMARK FOR ts_WM AS ts_WM
) WITH (
    'connector'     = 'mqtt',
    'server'        = 'broker_north',
    'port'          = '1883',
    'topic'         = 'factory_iot/north/101',
    'username'      = 'mqtt_dev',
    'password'      = 'abfr24'
);

SET 'pipeline.name' = 'Factory_iot 102 Source';

CREATE OR REPLACE TABLE hive_catalog.iot.factory_iot_102 (
    ts bigint,
    metadata array<row<
        siteId INTEGER, 
        deviceId INTEGER, 
        sensorId INTEGER, 
        unit STRING, 
        ts_human STRING, 
        location array<row<
            latitude DOUBLE, 
            longitude DOUBLE>>,  
        deviceType STRING>>,
    measurement DOUBLE,
    ts_WM as TO_TIMESTAMP(FROM_UNIXTIME(CAST(`ts` AS BIGINT) / 1000)),
    WATERMARK FOR ts_WM AS ts_WM
) WITH (
    'connector'     = 'mqtt',
    'server'        = 'broker_north',
    'port'          = '1883',
    'topic'         = 'factory_iot/north/102',
    'username'      = 'mqtt_dev',
    'password'      = 'abfr24'
);

SET 'pipeline.name' = 'Factory_iot 103 Source';

CREATE OR REPLACE TABLE hive_catalog.iot.factory_iot_103 (
    ts bigint,
    metadata array<row<
        siteId INTEGER, 
        deviceId INTEGER, 
        sensorId INTEGER, 
        unit STRING, 
        ts_human STRING, 
        location array<row<
            latitude DOUBLE, 
            longitude DOUBLE>>,  
        deviceType STRING>>,
    measurement DOUBLE,
    ts_WM as TO_TIMESTAMP(FROM_UNIXTIME(CAST(`ts` AS BIGINT) / 1000)),
    WATERMARK FOR ts_WM AS ts_WM
) WITH (
    'connector'     = 'mqtt',
    'server'        = 'broker_south',
    'port'          = '1884',
    'topic'         = 'factory_iot/south/103',
    'username'      = 'mqtt_dev',
    'password'      = 'abfr24'
);

SET 'pipeline.name' = 'Factory_iot 104 Source';

CREATE OR REPLACE TABLE hive_catalog.iot.factory_iot_104 (
    ts bigint,
    metadata array<row<
        siteId INTEGER, 
        deviceId INTEGER, 
        sensorId INTEGER, 
        unit STRING, 
        ts_human STRING, 
        location array<row<
            latitude DOUBLE, 
            longitude DOUBLE>>,  
        deviceType STRING>>,
    measurement DOUBLE,
    ts_WM as TO_TIMESTAMP(FROM_UNIXTIME(CAST(`ts` AS BIGINT) / 1000)),
    WATERMARK FOR ts_WM AS ts_WM
) WITH (
    'connector'     = 'mqtt',
    'server'        = 'broker_south',
    'port'          = '1884',
    'topic'         = 'factory_iot/south/104',
    'username'      = 'mqtt_dev',
    'password'      = 'abfr24'
);

SET 'pipeline.name' = 'Factory_iot 105 Source';

CREATE OR REPLACE TABLE hive_catalog.iot.factory_iot_105 (
    ts bigint,
    metadata array<row<
        siteId INTEGER, 
        deviceId INTEGER, 
        sensorId INTEGER, 
        unit STRING, 
        ts_human STRING, 
        location array<row<
            latitude DOUBLE, 
            longitude DOUBLE>>,  
        deviceType STRING>>,
    measurement DOUBLE,
    ts_WM as TO_TIMESTAMP(FROM_UNIXTIME(CAST(`ts` AS BIGINT) / 1000)),
    WATERMARK FOR ts_WM AS ts_WM
) WITH (
    'connector'     = 'mqtt',
    'server'        = 'broker_east',
    'port'          = '1885',
    'topic'         = 'factory_iot/east/105',
    'username'      = 'mqtt_dev',
    'password'      = 'abfr24'
);

SET 'pipeline.name' = 'Factory_iot 104 Source';

CREATE OR REPLACE TABLE hive_catalog.iot.factory_iot_106 (
    ts bigint,
    metadata array<row<
        siteId INTEGER, 
        deviceId INTEGER, 
        sensorId INTEGER, 
        unit STRING, 
        ts_human STRING, 
        location array<row<
            latitude DOUBLE, 
            longitude DOUBLE>>,  
        deviceType STRING>>,
    measurement DOUBLE,
    ts_WM as TO_TIMESTAMP(FROM_UNIXTIME(CAST(`ts` AS BIGINT) / 1000)),
    WATERMARK FOR ts_WM AS ts_WM
) WITH (
    'connector'     = 'mqtt',
    'server'        = 'broker_east',
    'port'          = '1885',
    'topic'         = 'factory_iot/east/106',
    'username'      = 'mqtt_dev',
    'password'      = 'abfr24'
);


-- Unnested Tables

SET 'pipeline.name' = 'Factory_iot Unnested';

CREATE OR REPLACE TABLE hive_catalog.iot.factory_iot_unnested (
    ts bigint,
    siteId INTEGER, 
    deviceId INTEGER, 
    sensorId INTEGER, 
    unit STRING, 
    ts_human STRING, 
    latitude DOUBLE, 
    longitude DOUBLE,  
    deviceType STRING,
    measurement DOUBLE,
    ts_WM as TO_TIMESTAMP(FROM_UNIXTIME(CAST(`ts` AS BIGINT) / 1000)),
    WATERMARK FOR ts_WM AS ts_WM
) ;

--- Populate Unnested tables

SET 'pipeline.name' = 'Unnest payloads from factory_iot# into factory_iot_unnested';

INSERT INTO hive_catalog.iot.factory_iot_unnested
SELECT
    ts as ts,
    mt.siteId AS siteId,
    mt.deviceId AS deviceId,
    mt.sensorId AS sensorId,
    mt.unit AS unit,
    mt.ts_human as tshuman,
    mt.location.latitude as latitude,
    mt.location.longitude as longitude,
    mt.devicetype as devicetype,
    measurement as measurement
    FROM hive_catalog.iot.factory_iot_101
    CROSS JOIN UNNEST(`metadata`) AS mt;

-- and

INSERT INTO hive_catalog.iot.factory_iot_unnested
SELECT
    ts as ts,
    mt.siteId AS siteId,
    mt.deviceId AS deviceId,
    mt.sensorId AS sensorId,
    mt.unit AS unit,
    mt.ts_human as tshuman,
    mt.location.latitude as latitude,
    mt.location.longitude as longitude,
    mt.devicetype as devicetype,
    measurement as measurement
    FROM hive_catalog.iot.factory_iot_102
    CROSS JOIN UNNEST(`metadata`) AS mt;

--- Create Catalog


--- Create target Fluss Auto Partitioned table

CREATE TABLE fluss_catalog.iot.factory_iot (
    ts bigint,
    metadata array<row<
        siteId INTEGER, 
        deviceId INTEGER, 
        sensorId INTEGER, 
        unit STRING, 
        ts_human STRING, 
        location array<row<
            latitude DOUBLE, 
            longitude DOUBLE>>,  
        deviceType STRING>>,
    measurement DOUBLE,
) PARTITIONED BY (metadata.siteId, FROM_UNIXTIME(CAST(`ts` AS BIGINT) / 1000)) WITH (
    'bucket.num'                    = '3',
    'table.datalake.enabled'        = 'true'
    'table.auto-partition.enabled'  = 'true',
    'x'                             = 'y',
    'table.auto-partition.time-unit' = 'day'
);

--- Create target Fluss Manual Partitioned table

CREATE TABLE fluss_catalog.iot.factory_iot (
    ts bigint,
    metadata array<row<
        siteId INTEGER, 
        deviceId INTEGER, 
        sensorId INTEGER, 
        unit STRING, 
        ts_human STRING, 
        location array<row<
            latitude DOUBLE, 
            longitude DOUBLE>>,  
        deviceType STRING>>,
    measurement DOUBLE,
) PARTITIONED BY (metadata.siteId, FROM_UNIXTIME(CAST(`ts` AS BIGINT) / 1000)) WITH (
    'bucket.num'                = '3',
    'table.datalake.enabled'    = 'true',
    'x'                         = 'y',
);

-- Add Partitions, or
ALTER TABLE fluss_catalog.iot.factory_iot ADD PARTITION (ts = '2025-03');

SHOW PARTITIONS factory_iot;

--- Create target Fluss Auto Partitioned table

CREATE TABLE fluss_catalog.iot.factory_iot_unnested (
    ts bigint,
    siteId INTEGER, 
    deviceId INTEGER, 
    sensorId INTEGER, 
    unit STRING, 
    ts_human STRING, 
    latitude DOUBLE, 
    longitude DOUBLE>>,  
    deviceType STRING>>,
    measurement DOUBLE,
) PARTITIONED BY (siteId, FROM_UNIXTIME(CAST(`ts` AS BIGINT) / 1000)) WITH (
    'bucket.num'                    = '3',
    'table.datalake.enabled'        = 'true'
    'table.auto-partition.enabled'  = 'true',
    'x'                             = 'y',
    'table.auto-partition.time-unit' = 'day'
);

--- Create target Fluss Manual Partitioned table

CREATE TABLE fluss_catalog.iot.factory_iot_unnested (
    ts bigint,
    siteId INTEGER, 
    deviceId INTEGER, 
    sensorId INTEGER, 
    unit STRING, 
    ts_human STRING, 
    latitude DOUBLE, 
    longitude DOUBLE>>,  
    deviceType STRING>>,
    measurement DOUBLE,
) PARTITIONED BY (siteId, FROM_UNIXTIME(CAST(`ts` AS BIGINT) / 1000)) WITH (
    'bucket.num'                = '3',
    'table.datalake.enabled'    = 'true',
    'x'                         = 'y',
);


--- Populate target fluss table

SET 'pipeline.name' = 'Push Flink factory_iot_101 to consolidated Fluss factory_iot ';
INSERT INTO fluss_catalog.iot.factory_iot SELECT * FROM c_hive.iot.factory_iot_101;

SET 'pipeline.name' = 'Push Flink factory_iot_102 to consolidated Fluss factory_iot ';
INSERT INTO fluss_catalog.iot.factory_iot SELECT * FROM c_hive.iot.factory_iot_102;

SET 'pipeline.name' = 'Push Flink factory_iot_103 to consolidated Fluss factory_iot ';
INSERT INTO fluss_catalog.iot.factory_iot SELECT * FROM c_hive.iot.factory_iot_103;

SET 'pipeline.name' = 'Push Flink factory_iot_104 to consolidated Fluss factory_iot ';
INSERT INTO fluss_catalog.iot.factory_iot SELECT * FROM c_hive.iot.factory_iot_104;

SET 'pipeline.name' = 'Push Flink unnested factory_iot to Fluss factory_iot';
INSERT INTO fluss_catalog.iot.factory_iot_unnested SELECT * FROM hive_catalog.iot.factory_iot_unnested;


