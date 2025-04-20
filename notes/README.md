## Mosquito Configuration.

For those that dont want to use authenfitication on the Mosquito / MQTT broker, copy the `mosquitto.conf` file into the `<root>/devlab#/conf/mqtt/<region>` directory. You can also delete the password file.

If you don't want to create the password file simply copy the `password_file` from this directory into the above mentioned config directory.

You can direct all the payloads via a single broker by changing the `export MQTT_BROKER_PORT=188X` port number in the 3 x `siteX.sh` files located in `<root>/app_mqttiot1/`, `<root>/app_mqttiot2/` & `<root>/app_mqttiot3/` to all be `export MQTT_BROKER_PORT=1883`.

Note: you will also need to change the `<root>/devlab#/creFlinkFlows/2.creMqttTables.sql` to reference the relevant broker/port.


## MQTT Source and Sink connectors Notes

### Flink Project Docs

https://nightlies.apache.org/flink/flink-docs-master/docs/dev/table/sourcessinks/
https://nightlies.apache.org/flink/flink-docs-master/docs/dev/datastream/sources/


### MQTT Connectors

[davidfantasy](https://github.com/davidfantasy/flink-connector-mqtt)
[davidfantasy](https://gitee.com/davidfantasy/flink-connector-mqtt)
[Jar File](https://repo1.maven.org/maven2/com/github/davidfantasy/flink-connector-mqtt/1.1.0/flink-connector-mqtt-1.1.0.jar)

[BG shared](https://gist.github.com/Ugbot/7340025ff225283f56c3a8445f50348e)

[Git repo](https://github.com/kevin4936/kevin-flink-connector-mqtt3)
[Jar File](https://repo1.maven.org/maven2/io/github/kevin4936/kevin-flink-connector-mqtt3_2.12/1.14.4.1/kevin-flink-connector-mqtt3_2.12-1.14.4.1.jar)



## Fluss SQL examples 

### Primary key and log based tables, manual and auto partitioned.

Notes re Primary Key and Log based tables, partitioned and not, using auto or manual partition adding.

-- Basic PK Table
```sql
CREATE TABLE my_pk_table (
  shop_id BIGINT,
  user_id BIGINT,
  num_orders INT,
  total_amount INT,
  PRIMARY KEY (shop_id, user_id) NOT ENFORCED
) WITH (
  'bucket.num' = '4'
);

-- Partitioned PK Table
CREATE TABLE my_part_pk_table (
  dt STRING,
  shop_id BIGINT,
  user_id BIGINT,
  num_orders INT,
  total_amount INT,
  PRIMARY KEY (dt, shop_id, user_id) NOT ENFORCED
) PARTITIONED BY (dt);

-- Add Partitions, or
ALTER TABLE my_part_pk_table ADD PARTITION (dt = '2025-03-05');


-- Auto Partitioned PK Table
CREATE TABLE my_auto_part_pk_table (
  dt STRING,
  shop_id BIGINT,
  user_id BIGINT,
  num_orders INT,
  total_amount INT,
  PRIMARY KEY (dt, shop_id, user_id) NOT ENFORCED
) PARTITIONED BY (dt) WITH (
  'bucket.num' = '4',
  'table.auto-partition.enabled' = 'true',
  'table.auto-partition.time-unit' = 'day'
);

-- Basic Log Table
CREATE TABLE my_log_table (
  order_id BIGINT,
  item_id BIGINT,
  amount INT,
  address STRING
) WITH (
  'bucket.num' = '8'
);

-- Partitioned Log table
CREATE TABLE my_part_log_table (
  order_id BIGINT,
  item_id BIGINT,
  amount INT,
  address STRING,
  dt STRING
) PARTITIONED BY (dt);

-- Add Partitions, or
ALTER TABLE my_part_log_table ADD PARTITION (dt = '2025-03-05');

-- Auto Partitioned Log Table
CREATE TABLE my_auto_part_log_table (
  order_id BIGINT,
  item_id BIGINT,
  amount INT,
  address STRING,
  dt STRING
) PARTITIONED BY (dt) WITH (
  'bucket.num' = '8',
  'table.auto-partition.enabled' = 'true',
  'table.auto-partition.time-unit' = 'hour'
);

-- Show/Display partitions for a table
SHOW PARTITIONS my_part_pk_table;
SHOW PARTITIONS my_auto_part_pk_table;
SHOW PARTITIONS my_part_log_table;
SHOW PARTITIONS my_auto_part_log_table;


-- to pipeline the data to lakehouse add the following to the create table.ABORT
'table.datalake.enabled' = 'true'
```


## Fluss <==> Flink Lakehouse sync command.

The below shell command will sync all tables created with `table.datalake.enabled ` set to `True` to Fluss down onto the lakehouse storage tier configured. To be executed in cooridnator-server shell.

```shell

./bin/lakehouse.sh -D flink.rest.address=jobmanager -D flink.rest.port=8081 -D flink.execution.checkpointing.interval=30s -D flink.parallelism.default=2

```