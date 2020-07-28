#!/usr/bin/env bash

cd python/
pip3 install -r requirement.txt
cd ..
time ../spark/bin/spark-submit --files players.csv python/sparktest.py
