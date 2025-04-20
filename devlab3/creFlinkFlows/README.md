
# Data Flows

1. 1.creCat.sql

    Will create the Fluss catalog.

    - fluss_catalog

2. 2.creMqttTables.sql

    Create Flink source Tables that will consume from the MQTT broker topic, persisting the data into Apache Fluss and down to apache Paimon as apache Parquet files persisted to a local HDFS cluster.



