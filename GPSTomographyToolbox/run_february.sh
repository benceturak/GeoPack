#!/bin/bash

for day in {4..28}
do
    echo $day
    for hour in {0..23}
    do
        ./run.sh 2024 02 $day $hour
    done
done