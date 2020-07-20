#!/usr/bin/env bash

apt-get update
apt-get install openjdk-8-jdk python3-dev python3-pip
curl -O http://mirror.cogentco.com/pub/apache/spark/spark-2.4.6/spark-2.4.6-bin-hadoop2.7.tgz
tar zxvf spark-2.4.6-bin-hadoop2.7.tgz
mv spark-2.4.6-bin-hadoop2.7/ spark
