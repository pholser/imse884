#!/bin/bash

for n in 10 20 30 50; do
    for p in 0.2 0.4 0.6 0.8; do
        if [[ $(echo - | awk "{print $n * $p}") -lt 28 ]]; then
            problem="./tests/data/benchmark/${n}_${p}.col"

            echo Solving "${problem} as assignment IP"
            python ./solver.py \
                -g "${problem}" \
                -f assign \
                -d /tmp \
                -s ip \
                > "${problem}.assign.ip.out"

            echo Solving "${problem} as assignment LR, warm restart"
            python ./solver.py \
                -g "${problem}" \
                -f assign \
                -r warm \
                -d /tmp \
                -s lr \
                > "${problem}.assign.lr.warm.out"

            echo Solving "${problem} as assignment LR, cold restart"
            python ./solver.py \
                -g "${problem}" \
                -f assign \
                -r cold \
                -d /tmp \
                -s lr \
                > "${problem}.assign.lr.cold.out"

            echo Solving "${problem} as representative IP"
            python ./solver.py \
                -g "${problem}" \
                -f rep \
                -d /tmp \
                -s ip \
                > "${problem}.rep.ip.out"

            echo Solving "${problem} as representative LR, warm restart"
            python ./solver.py \
                -g "${problem}" \
                -f rep \
                -r warm \
                -d /tmp \
                -s lr \
                > "${problem}.rep.lr.warm.out"

            echo Solving "${problem} as representative LR, cold restart"
            python ./solver.py \
                -g "${problem}" \
                -f rep \
                -r cold \
                -d /tmp \
                -s lr \
                > "${problem}.rep.lr.cold.out"
        fi
    done
done
