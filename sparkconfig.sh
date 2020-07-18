#!/usr/bin/env bash

apt-get install openjdk-8-jdk python3-dev python3-pip
curl -O http://mirror.cogentco.com/pub/apache/spark/spark-2.4.6/spark-2.4.6-bin-hadoop2.7.tgz
tar zxvf spark-2.4.6-bin-hadoop2.7.tgz
mv spark-2.4.6-bin-hadoop2.7/ spark
export SPARK_MASTER_HOST=localhost
export SPARK_WORKER_INSTANCES=$(nproc)
export PYSPARK_DRIVER_PYTHON=python3
export PYSPARK_PYTHON=python3
./spark/sbin/start-master.sh
./spark/sbin/start-slave.sh spark://localhost:7077 -m 1g -c 1
