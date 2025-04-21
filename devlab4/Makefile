
.DEFAULT_GOAL := help
include .env

define HELP

Available commands:

- buildapp: Just build the docker app image.

- run: This will call core.

- deploy: This will create all the catalogs, databases. Flink/Fluss tables etc.

- rp#: Run workload creator/the Python app -> Post onto MQTT Broker Topic
- sp#: Stop Python app

- stop: Stop the project.
- start: Start a stopped project.
- down: Tear down the project, clean directories.
- ps: Show all running containers.

- logs: Show/tail logs.
- logsf: Stream logs.
- watch: Watch logs.

- fsql: Open Flink Jobmanager and start sql-client.
- jm: Open a bash terminal inside Jobmanager.
- cs: Open a bash terminal inside Coordinator Server.

endef

export HELP
help:
	@echo "$$HELP"
.PHONY: help



buildapp:
	cd ../app_mqttiot1; make build

#	docker rmi $(docker images -q --filter "dangling=true")

run: 
	docker compose -p pipeline up -d \
		postgres metastore hiveserver2 \
		jobmanager taskmanager \
		minio mc \
		zookeeper coordinator-server tablet-server-0 tablet-server-1 tablet-server-2 \
		mqtt_broker_north mqtt_broker_south mqtt_broker_east \
		 --remove-orphans 

#		minio mc
 
deploy: createcat
 
createcat:
	docker compose exec jobmanager /opt/flink/bin/sql-client.sh -f /sql/1.creCat.sql

source:
	docker compose exec jobmanager /opt/flink/bin/sql-client.sh -f /sql/2.creSource.sql

target:
	docker compose exec jobmanager /opt/flink/bin/sql-client.sh -f /sql/3.creTarget.sql

lakehouse:
	docker compose exec coordinator-server /bin/bash -f /shell/4.runLakehouse.bsh


# Run Python app  101,104
rp1:
	docker compose -p pipeline up -d iot1_mqtt

# Stop Python app
sp1:
	docker compose stop iot1_mqtt

# Run Python app  102,105
rp2:
	docker compose -p pipeline up -d iot2_mqtt

# Stop Python app
sp2:
	docker compose stop iot2_mqtt

# Run Python app  103,106
rp3:
	docker compose -p pipeline up -d iot3_mqtt

# Stop Python app
sp3:
	docker compose stop iot3_mqtt

stop:
	docker compose stop

start:
	docker compose start

down:	
	docker compose down
	cd data/minio; rm -rf .minio.sys
	cd data/minio; rm -rf * 
	cd data/postgres; rm -rf *
	cd data/flink; rm -rf checkpoints logs rocksdb
	cd data/fluss; rm -rf *
	cd data/paimon; rm -rf *
	cd data/mqtt/north/data; rm * 
	cd data/mqtt/south/data; rm * 
	cd data/mqtt/east/data; rm * 
	cd data/mqtt/north/log; rm * 
	cd data/mqtt/south/log; rm * 
	cd data/mqtt/east/log; rm * 
ps:
	docker compose ps

logs:
	docker compose logs

logsf:
	docker compose logs -f

watch:
	watch docker compose ps

fsql:
	docker compose exec jobmanager /opt/flink/bin/sql-client.sh

jm:
	docker compose exec jobmanager /bin/bash

cs:
	docker compose exec coordinator-server /bin/bash

#```shell  -> fluss coordinator-server
# ./bin/lakehouse.sh -D flink.rest.address=jobmanager -D flink.rest.port=8081 -D flink.execution.checkpointing.interval=30s -D flink.parallelism.default=2
#```