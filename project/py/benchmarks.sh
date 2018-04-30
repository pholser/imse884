#!/bin/bash

for n in 10 20 30 50 70; do
    for p in 0.2 0.4 0.6 0.8; do
        python ./generate_random_graph.py -n $n -p $p \
            > ./tests/data/benchmark/${n}_${p}.col
    done
done
