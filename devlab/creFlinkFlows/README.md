
# Data Flows

1. creCat.sql

Will create the 2 cataloges and their containing databases

- c_hive and DB: hive

- c_paimon and DB: iot

2. creCdcTopic.bsh

Here we will create the process that will sink the data from the source Kafka topic into the Paimon table using the Flink paimon action framework.    

Our data will be pushed into `c_paimin.iot.factory_iot` table.

- The Flink source document that will help us here is: [Kafka CDC](https://paimon.apache.org/docs/0.9/flink/cdc-ingestion/kafka-cdc/).




