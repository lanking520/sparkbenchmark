#!/usr/bin/env bash

cd java/
./gradlew clean shadowJar
cd ..
time ../spark/bin/spark-submit --files players.csv java/build/libs/java-1.0-SNAPSHOT-all.jar
# --conf 'spark.executor.extraJavaOptions=-Dai.djl.pytorch.num_threads=1' \
# --conf 'spark.driver.extraJavaOptions=-Dai.djl.pytorch.num_threads=1' \
