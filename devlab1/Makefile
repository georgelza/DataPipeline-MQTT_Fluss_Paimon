
.DEFAULT_GOAL := help
include .env

define HELP

Available commands:

- buildapp: Just build the docker app image.

- run: This will call core.

- deploy: This will create all the catalogs, databases. Flink/Fluss tables etc.

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


run: 
	docker compose -p pipeline up -d \
		postgres metastore hiveserver2 \
		jobmanager taskmanager \
		zookeeper coordinator-server tablet-server-0 tablet-server-1 tablet-server-2 \
		 --remove-orphans 

#		minio mc
 
deploy: createcat
 
createcat:
	docker compose exec jobmanager /opt/flink/bin/sql-client.sh -f /sql/1.creCat.sql

source:
	docker compose exec jobmanager /opt/flink/bin/sql-client.sh -f /sql/2.creSource.sql

target:
	docker compose exec jobmanager /opt/flink/bin/sql-client.sh -f /sql/3.creTarget.sql


stop:
	docker compose stop

start:
	docker compose start

down:	
	docker compose down
	cd data/postgres; rm -rf *
	cd data/flink; rm -rf checkpoints logs rocksdb
	cd data/fluss; rm -rf *
	cd data/paimon; rm -rf *
	cd data/hdfs; rm -rf *

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