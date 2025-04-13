# Building a IoT Source via MQTT Broker to Apache Flink/Fluss Pipeline for IoT based payload.

## Overview

We will Publish IoT structured payload for 6 factories onto 3 seperate MQTT Brokers (North, South and East), 2 factories per broker.

The data will be sourced from **MQTT Brokers** using **Apache Flink** source connector written in Java, followed by pushing th payload into our **Apache Flink** environment and onwards into **Apache Fluss** which will in turn deep store it in our **Apache Paimon** Open Table format based table, to be stored in **Apache Parquet** file format, stored on S3 object store, osted on a **MinIO S3** container.

We're still using our **Apache Hive Metastore** as catalog with a PostgreSQL database for backend storage.


### Modules and Versions

- Apache Flink 1.19.1-scala_2.12-java11 on Hadoop version: 3.3.4
- Flink CDC 3.2   - required by Flink 1.19.x
- Apache Paimon 0.9.0
- MQTT Broker
- Ubuntu 24.04 LTS
- Hive Metastore 3.1.3 on Hadoop 3.3.5
- PostgreSQL 12
- Python 3.13


## Configuring MQTT Authentification

[Authentication methods](https://mosquitto.org/documentation/authentication-methods/)

I decided to behave an enable authentification on the MQTT Broker, to accomplish this we need a password file with a username and password contained. To prepare for this follow the following steps.

Start by executing <root>/devlab/make run

This will start the stack, now execute the below.

Now execute
    docker compose exec mqtt_broker_north /bin/sh

Followby by executing inside the container.

    mosquitto_passwd -c /mosquitto/config/password_file mqtt_dev

    I used `abfr24` as password, this will match the .pws in <root>/app_iot1/.pws

First make sure the <root>/devlab/data/mqtt/<east/north and south>/config/mosquitto.conf contain the below

North
```
    persistence true
    listener 1883
    persistence_location /mosquitto/data
    log_dest file /mosquitto/log/mosquitto.log
    password_file /mosquitto/config/password_file
```

South
```
    persistence true
    listener 1884
    persistence_location /mosquitto/data
    log_dest file /mosquitto/log/mosquitto.log
    password_file /mosquitto/config/password_file
```

East
```
    persistence true
    listener 1885
    persistence_location /mosquitto/data
    log_dest file /mosquitto/log/mosquitto.log
    password_file /mosquitto/config/password_file
```

Now execute make down, once the stack is stopped execute the below.

    Copy the files located in <root>/devlab/data/mqtt/north/config to ../south/config and ../east/config


I use both MQTT Explorer and MQTT.fx to see whats happening on MQTT Brokers.


## IoT Payload

Below is a list of the various pauloads that can be created.

### Basic min IoT Payload

```json5
{
    "ts" : 123421452622,
    "metadata" : {
        "siteId" : 1009,
        "deviceId" : 1042,
        "sensorId" : 10180,
        "unit" : "Psi"
    },
    "measurement" : 1013.3997
}
```

### Basic min IoT Payload, with a human readable time stamp

```json5
{
    "ts" : 123421452622,
    "metadata" : {
        "siteId" : 1009,
        "deviceId" : 1042,
        "sensorId" : 10180,
        "unit" : "Psi",
        "ts_human" : "2024-10-02T00:00:00.869Z",

    },
    "measurement" : 1013.3997
}
```

### Modified IoT Payload -> schema evolution, we add location tag.

```json5
{
    "ts" : 123421452622,
    "metadata" : {
        "siteId" : 1009,
        "deviceId" : 1042,
        "sensorId" : 10180,
        "unit" : "Psi",
        "ts_human" : "2024-10-02T00:00:00.869Z",
        "location": {
            "latitude": -26.195246, 
            "longitude": 28.034088
        }
    },
    "measurement" : 1013.3997
}
```

### Modified IoT Payload -> schema evolution, here we further add deviceType tag.

```json5
{
    "timestamp" : "2024-10-02T00:00:00.869Z",
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
```

## Apache Flink Consumer Example

[Apache Flink Consumer](https://gist.github.com/Ugbot/7340025ff225283f56c3a8445f50348e)


## Apache Fluss

[Apache Fluss]()



## To run the project.


### See various configuration settings and passwords in:

0. devlab/docker_compose.yml

1. .pwd in app_iot1 in siteX.sh

2. devlab/.env

3. devlab/conf/hive.env

4. devlab/conf/hive-site.xml

### Download containers and libraries

1. cd infrastructure

2. make pullall

3. make buildall


### Build various containers

1. cd devlab

2. ./getlibs.sh

3. make build

4. Now, to run it please stay in devlab and refer to README.md in there...



## Projects / Components

- [One-Click Database Synchronization from Kafka Topic to Paimon Using Flink CDC](https://paimon.apache.org/docs/0.9/), navigate to Engine Flink and then down into CDC Ingestion.

- [Apache Flink](https://flink.apache.org)

- [Ververica](https://www.ververica.com)

- [Apache Paimon](https://paimon.apache.org)

- [Apache Parquet File format](https://parquet.apache.org)



## Misc Notes

### Flink Libraries

As I was travelling while writing this blog and did not want to pull the libraries on every build I decided to downlaod them once into the below directory and then copy them on build into container. Just a different way less bandwidth and also slightly faster.

The `devlab/data/flink/lib` directories will house our Java libraries required by our Flink stack. 

Normally I'd include these in the Dockerfile as part of the image build, but during development it's easier if we place them here and then mount the directories into the containers at run time via our `docker-compose.yml` file inside the volume specification for the flink-* services.

This makes it simpler to add/remove libraries as we simply have to restart the flink container and not rebuild it.

Additionally, as the `flink-jobmanager`, `flink-taskmanager` use the same libraries doing it tis way allows us to use this one set, thus also reducing the disk space and the container image size.

The various files are downloaded by executing the `getlibs.sh` file located in the `devlab/` directory.


### Flink base container images

    
docker pull arm64v8/flink:1.19-scala_2.12-java11


- https://flink.apache.org/downloads/#apache-flink-jdbc-connector-320
- https://flink.apache.org/downloads/#apache-flink-kafka-connector-330
- https://flink.apache.org/downloads/#apache-flink-mongodb-connector-120


### Flink source connector

- https://nightlies.apache.org/flink/flink-cdc-docs-release-3.2/docs/connectors/flink-sources/mongodb-cdc/


## Manual pull of all source containers images from `hub.docker.com`


## Uncategorized notes

Some misc notes:

[Apache Flink FLUSS](https://www.linkedin.com/posts/polyzos_fluss-is-now-open-source-activity-7268144336930832384-ds87?utm_source=share&utm_medium=member_desktop)

[Apache Flink Deployment](https://nightlies.apache.org/flink/flink-docs-release-1.19/docs/deployment/resource-providers/standalone/docker/)    
    
[Apache Flink SQL Connector](https://repo1.maven.org/maven2/org/apache/flink/flink-sql-connector-kafka/)

[Troubleshooting Apache Flink SQL S3 problems](https://www.decodable.co/blog/troubleshooting-flink-sql-s3-problems)

### Flink Cluster

[how-to-set-up-a-local-flink-cluster-using-docker](https://medium.com/marionete/how-to-set-up-a-local-flink-cluster-using-docker-0a0a741504f6)

### RocksDB

[Using RocksDB State Backend in Apache Flink: When and How](https://flink.apache.org/2021/01/18/using-rocksdb-state-backend-in-apache-flink-when-and-how/)


### DuckDB

[Can hashtag#duckdb revolutionize the data lake experience?](https://www.linkedin.com/posts/mehd-io_duckdb-activity-7265743807625723905-_OO4/?utm_source=share&utm_medium=member_desktop)

[Youtube: Can DuckDB revolutionize the data lake experience?](https://www.youtube.com/watch?v=CDzqDpCNjiY&feature=youtu.be)


### Log4J Logging levels

[Log4J Logging Levels](https://logging.apache.org/log4j/2.x/manual/customloglevels.html)
    
- The Flink jobmanager and taskmanager log levels can be modified by editing the various `devlab/conf/*.properties` files.


### Great quick reference for docker compose

[A Deep dive into Docker Compose by Alex Merced](https://dev.to/alexmercedcoder/a-deep-dive-into-docker-compose-27h5)


### Consider using secrets for sensitive information

[How to use sectrets with Docker Compose](https://docs.docker.com/compose/how-tos/use-secrets/)


### Enabling Prometheus monitoring on Minio with grafana dashboard

[Enabling Prometheus Scraping of Minio](https://min.io/docs/minio/linux/operations/monitoring/metrics-and-alerts.html)

[Grafana Dashboards](https://min.io/docs/minio/linux/operations/monitoring/grafana.html#minio-server-grafana-metrics)


### By:

George

[georgelza@gmail.com](georgelza@gmail.com)

[https://www.linkedin.com/in/george-leonard-945b502/](https://www.linkedin.com/in/george-leonard-945b502/)