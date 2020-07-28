#!/usr/bin/env bash

cd java/
./gradlew clean shadowJar
cd ..
time ../spark/bin/spark-submit --files players.csv --jars java/build/libs/java-1.0-SNAPSHOT-all.jar
