# Building a IoT Source via MQTT Broker to Apache Flink/Fluss Pipeline for IoT based payload.

Work in Progress... NOT COMPLETE.

## Overview

This originally started as a simple idea, create a IoT JSON packaged payload, publish it to a **MQTT Broker**, consume using a connector into Flink and then down to Fluss and down to the lakehouse configured Paimon storage onto the configured storage technology, which was originally planned as S3.

But we tripped and ended in the proverbial rabbit hole, again, nothing new.

The numbers below maps to the `<root>/devlab#` directories

0.  First is just to show how the stack fit together, this is a very simple Flink/Fluss example (as per Giannis video NEED his OK still... to be after he published his video), persisting both tablet server and Lakehouse data onto local disk via volume mounts.

1.  Second we're doing the same as above, but now persisted onto **HDFS**.

2.  Ok, now a back to our original plan, we will create the IoT specific payload as shown below, post it onto 3 x **MQTT Brokers**,consuming themessages using one of the following 2 source connectors.

- [davidfantasy - flink-connector-mqtt](https://github.com/davidfantasy/flink-connector-mqtt) (Preferred) or 

- [kevin-flink-connector-mqtt3](https://github.com/kevin4936/kevin-flink-connector-mqtt3)
  [Jar file](https://repo1.maven.org/maven2/io/github/kevin4936/kevin-flink-connector-mqtt3_2.12/1.14.4.1/kevin-flink-connector-mqtt3_2.12-1.14.4.1.jar)

from our **Apache Flink** cluster and ingest the data into our `hive_catalog.iot.factory_iot_#` tables. We will then insert the data into our `fluss_catalog.iot.*` selecting from the `hive_catalog.iot.*` tables.

1.  Same as #2, but persisted onto **HDFS**.

2.  Same as #2, but persisted onto **AWS S3** hosted on a **MinIO** Container, ye the actual original idea for this blog, or was that series, but def a Rabbbit hole.


### For sections devlab #2, 3 & 4

We will post the 6 factories onto 3 seperate **MQTT Brokers** based on the regional locatation/distribution, namely North, South and East.


### Flink Catalog


We're still using our **Apache Hive Metastore** as catalog with a **PostgreSQL** database for backend storage.
See below for version information.


## Modules and Versions

- Apache Flink 1.20.1

- Apache Fluss 0.6.0

- Apache Paimon 1.0.1

- Hadoop File System (HDFS) 3.3.5 build (OpenJDK11) on Ubuntu 20.04 LTS

- MQTT Broker - Latest

- Ubuntu 24.04 LTS

- Hive Metastore 3.1.3 on Hadoop 3.3.5 (OpenJDK8) on Ubuntu 24.04 LTS

- PostgreSQL 12

- Python 3.12

- Minio S3 


## Our various IoT Payloads formats.

### Basic min IoT Payload, produced by Factories 101 and 104

```json5
{
    "ts": 1729312551000, 
    "metadata": {
        "siteId": 101, 
        "deviceId": 1004, 
        "sensorId": 10034, 
        "unit": "BAR"
    }, 
    "measurement": 120
}
```

### Basic min IoT Payload, with a human readable time stamp & location added, produced by Factories 102 and 105

```json5
{
    "ts": 1713807946000, 
    "metadata": {
        "siteId": 102, 
        "deviceId": 1008, 
        "sensorId": 10073, 
        "unit": "Liter", 
        "ts_human": "2024-04-22T19:45:46.000000", 
        "location": {
            "latitude": -33.924869, 
            "longitude": 18.424055
        }
    }, 
    "measurement": 25
}
```

### Complete IoT Payload, with deviceType tag added, produced by Factories 103 and 106

```json5
{
    "ts": 1707882120000, 
    "metadata": {
        "siteId": 103, 
        "deviceId": 1014, 
        "sensorId": 10124, 
        "unit": "Amp", 
        "ts_human": "2024-02-14T05:42:00.000000", 
        "location": {
            "latitude": -33.9137, 
            "longitude": 25.5827
        }, 
        "deviceType": "Hoist_Motor"
    },
    "measurement": 24
}
```


## To run the project.

### See various configuration settings and passwords in:

0. devlab#/docker_compose.yml

1. .pwd in app_mqttiot# in siteX.sh

2. devlab#/.env

3. devlab#/conf/hive.env

4. devlab#/conf/hive-site.xml

### Download containers and libraries

1. cd infrastructure

2. make pullall

3. make buildall


### Build various containers

1. cd devlab#

2. ./getlibs.sh

3. make build

4. Slight Digress, At this stage we need to configure our Mosquito Brokers. See below.


### Mosquito Access control

[Authentication methods](https://mosquitto.org/documentation/authentication-methods/)

I decided to behave an enable authentification on the MQTT Broker, to accomplish this we need a password file with a username and password contained. To prepare for this follow the following steps.

Start by executing `<root>/devlab#/make run`

This will start the stack, now execute the below.

Now execute
    `docker compose exec mqtt_broker_north /bin/sh`

Followby by executing inside the container.

    `mosquitto_passwd -c /mosquitto/config/password_file mqtt_dev`

    I used `abfr24` as password, this will match the `.pws` in `<root>/app_mqttiot1/.pws`

First make sure the `<root>/devlab#/conf/mqtt/<east/north/south>/mosquitto.conf` contain the below

North
```shell
    persistence true
    listener 1883
    persistence_location /mosquitto/data
    log_dest file /mosquitto/log/mosquitto.log
    password_file /mosquitto/config/password_file
```

South
```shell
    persistence true
    listener 1884
    persistence_location /mosquitto/data
    log_dest file /mosquitto/log/mosquitto.log
    password_file /mosquitto/config/password_file
```

East
```shell
    persistence true
    listener 1885
    persistence_location /mosquitto/data
    log_dest file /mosquitto/log/mosquitto.log
    password_file /mosquitto/config/password_file
```

Now execute `make down`, once the stack is stopped execute the below.

    Copy the files located into the `<root>/devlab#/conf/mqtt/north/` to `../south/` & `../east/` directories.


I use both MQTT Explorer and MQTT.fx to see whats happening on MQTT Brokers.


4. Now, to run it please read README.md in `<root>/devlab#/README.md` file.


## Projects / Components

- [Apache Flink](https://flink.apache.org)

- [Ververica](https://www.ververica.com)

- [What is Fluss](https://alibaba.github.io/fluss-docs/)

- [Fluss Overview](https://alibaba.github.io/fluss-docs/docs/install-deploy/overview/)

- [What is Fluss docs](https://alibaba.github.io/fluss-docs/docs/intro/)

- [Fluss Project Git Repo](https://github.com/alibaba/fluss)

- [Introduction to Fluss](https://www.ververica.com/blog/introducing-fluss)

- [Apache Paimon](https://paimon.apache.org)

- [Apache Parquet File format](https://parquet.apache.org)


## Misc Notes

The various `REAMDE.md` utilises markdown syntax. You can refer to `https://markdownlivepreview.com` & `https://dillinger.io` for more information, examples.

To view a mardown file, `https://jumpshare.com/viewer/md` or if you using Visual Studio Code search for markdown as a module and try some of them.


### Flink Libraries

As I am always travelling while writing these blog's and did not want to pull the libraries on every build I decided to downlaod them once into the below directory and then mount them into container. Just a different way less bandwidth and also slightly faster builds.

The `devlab#/conf/flink/lib/*` directories will house our Java libraries required by our Flink stack. 

Normally I'd include these in the Dockerfile as part of the image build, but during development it's easier if we place them here and then mount the directories into the containers at run time via our `docker-compose.yml` file inside the volume specification for the flink-* services.

This makes it simpler to add/remove libraries as we simply have to restart the flink container and not rebuild it.

Additionally, as the `jobmanager`, `taskmanager` use the same libraries doing it tis way allows us to use this one set, thus also reducing the disk space and the container image size.

The various files are downloaded by executing the `getlibs.sh` file located in the `devlab#/` directory.


### Flink base container images for 1.20.1 (manual pull from `hub.docker.com`)

- docker pull arm64v8/flink:1.20.1-scala_2.12-java11


### Self Build Flink container

- [Master Flink download](https://flink.apache.org/downloads/#apache-flink-1201)

- [Flink 1.20.1 binaries](https://www.apache.org/dyn/closer.lua/flink/flink-1.20.1/flink-1.20.1-bin-scala_2.12.tgz)


## Manual pull of all source containers images from `hub.docker.com`

- to be completed !!!!
    mc
    minio
    postgresql 12
    ubuntu 24.04
    Python 3.12
    ...


## Uncategorized notes and Articles

- [Apache Flink FLUSS](https://www.linkedin.com/posts/polyzos_fluss-is-now-open-source-activity-7268144336930832384-ds87?utm_source=share&utm_medium=member_desktop)


- [Apache Flink Deployment](https://nightlies.apache.org/flink/flink-docs-release-1.19/docs/deployment/resource-providers/standalone/docker/)    
    

- [Troubleshooting Apache Flink SQL S3 problems](https://www.decodable.co/blog/troubleshooting-flink-sql-s3-problems)

### HDFS Cluster

- [Setting Up an HDFS Cluster with Docker Compose: A Step-by-Step Guide](https://bytemedirk.medium.com/setting-up-an-hdfs-cluster-with-docker-compose-a-step-by-step-guide-4541cd15b168)
- [Deploying Hadoop using Docker](https://medium.com/@garin.sanny07/hadoop-cluster-55477505d0ff)

- [Installing the Hadoop Stack using Docker](https://hackmd.io/@silicoflare/docker-hadoop)


### Flink Cluster

- [how-to-set-up-a-local-flink-cluster-using-docker](https://medium.com/marionete/how-to-set-up-a-local-flink-cluster-using-docker-0a0a741504f6)


### RocksDB

- [Using RocksDB State Backend in Apache Flink: When and How](https://flink.apache.org/2021/01/18/using-rocksdb-state-backend-in-apache-flink-when-and-how/)


### DuckDB

- [Can hashtag#duckdb revolutionize the data lake experience?](https://www.linkedin.com/posts/mehd-io_duckdb-activity-7265743807625723905-_OO4/?utm_source=share&utm_medium=member_desktop)


- [Youtube: Can DuckDB revolutionize the data lake experience?](https://www.youtube.com/watch?v=CDzqDpCNjiY&feature=youtu.be)


### Log4J Logging levels

- [Log4J Logging Levels](https://logging.apache.org/log4j/2.x/manual/customloglevels.html)
    

- The Flink jobmanager and taskmanager log levels can be modified by editing the various `devlab#/conf/*.properties` files. Remember to restart your Flink containers.


### Great quick reference for docker compose

- [A Deep dive into Docker Compose by Alex Merced](https://dev.to/alexmercedcoder/a-deep-dive-into-docker-compose-27h5)


### Consider using secrets for sensitive information

- [How to use sectrets with Docker Compose](https://docs.docker.com/compose/how-tos/use-secrets/)


### Enabling Prometheus monitoring on Minio with grafana dashboard

- [Enabling Prometheus Scraping of Minio](https://min.io/docs/minio/linux/operations/monitoring/metrics-and-alerts.html)


- [Grafana Dashboards](https://min.io/docs/minio/linux/operations/monitoring/grafana.html#minio-server-grafana-metrics)


### Credits:

This blog would not have been possible without the assistance of allot of people, 3 that I do need to mention by name being Ben Gamble, Jark Wu (the product owner of Fluss at Alibaba) & Giannis Polyzos from [Ververica](http://ververica.com).

    Ben Gamble,
        Field CTO @ [Ververica](http://ververica.com)
        Apache Kafka, Apache Flink, streaming and stuff (as he calls it)
        A good friend, thats always great to chat to... and we seldom stick to original topic.
        https://www.linkedin.com/in/bengamble7/
        https://confluentcommunity.slack.com/team/U03R0RG6CHZ

    Jark Wu
        Head of Fluss and Flink SQL at Alibaba Cloud (Ververica) | PMC member and Committer of Apache Flink
        https://www.linkedin.com/in/jarkwu/

    Giannis Polyzos
        Staff Streaming Architect | Fluss Lead @ [Ververica](http://ververica.com) | Apache Flink
        https://www.linkedin.com/in/polyzos/

### By:

George

[georgelza@gmail.com](georgelza@gmail.com)

[George on Linkedin](https://www.linkedin.com/in/george-leonard-945b502/)

[George on Medium](https://medium.com/@georgelza)

