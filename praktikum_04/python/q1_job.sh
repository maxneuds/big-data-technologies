#!/bin/bash

hadoop fs -rmdir /user/istmnneud/praktikum4/q1_output
hadoop jar /opt/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.7.5.jar \
-files /home/ldapusers/istmnneud/bdt/praktikum4/q1_mapper.py,/home/ldapusers/istmnneud/bdt/praktikum4/q1_reducer.py \
-mapper "python3 /home/ldapusers/istmnneud/bdt/praktikum4/q1_mapper.py" \
-reducer "python3 /home/ldapusers/istmnneud/bdt/praktikum4/q1_reducer.py" \
-input /user/istmnneud/praktikum4/movies_1m.json \
-output /user/istmnneud/praktikum4/q1_output
