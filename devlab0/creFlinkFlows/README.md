
# Data Flows

1. 1.creCat.sql

    Will create the Hive & Fluss catalog.

    - hive_catalog
    - faker database inside hive_catalog
    - fluss_catalog

2. 2.creSource.sql

    Create source flink tables, to be populated by datagen connector.

3. 3.creTarget.sql

    Create target fluss tables, to be populated by data from step #2 tables.

4. 4.runLakehouse.bsh

   Initiate ./bin/lakehouse.sh sync script, this is the job that moves our data from Fluss tables on the tablet servers down to the configured lakehouse persistent storage.

5. 5.creSelect.sql

    Various select statements to run.

