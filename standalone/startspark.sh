#!/usr/bin/env bash

export SPARK_MASTER_HOST=localhost
export SPARK_WORKER_INSTANCES=1
export PYSPARK_DRIVER_PYTHON=python3
export PYSPARK_PYTHON=python3
./spark/sbin/start-master.sh
./spark/sbin/start-slave.sh spark://localhost:7077
