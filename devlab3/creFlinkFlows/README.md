
# Data Flows

1. 1.creCat.sql

    Will create the Hive & Fluss catalog.

    - hive_catalog
    - iot database inside hive_catalog
    - fluss_catalog

2. 2.creSource.sql

    Create Flink source Tables that will consume from the MQTT broker topic.
    
3.  3.creTarget.sql

    Create our Fluss Target tables
    Execute the insert jobs that will move the data from the Flink Tables into the Fluss tables, locally persisted on the tablet servers.

4. 4.runLakehouse.bsh

   Initiate ./bin/lakehouse.sh sync script, this is the job that moves our data from Fluss tables on the tablet servers down to the configured lakehouse persistent storage -> local HDFS service.