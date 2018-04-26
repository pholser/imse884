#!/usr/bin/env python

from __future__ import print_function
from itertools import chain, combinations
import argparse as arg
import numpy as np


def power_set(iterable):
    "Swiped from https://docs.python.org/2/library/itertools.html"
    s = list(iterable)
    return chain.from_iterable(
        combinations(s, r) for r in xrange(len(s) + 1)
    )


def positive_int(value):
    "Swiped from https://bit.ly/2r3hfEU"
    ivalue = int(value)
    if ivalue <= 0:
        raise arg.ArgumentTypeError("Need a positive integer, got %s" % value)
    return ivalue


def verbose(indicator, *objects):
    if indicator:
        print(*objects)

"""
Theorem: A is TUM iff for every Q subset-of M = {1, ..., m},
there exists a partition Q_1, Q_2 of Q
such that abs(sum[i in Q_1]( a_ij ) - sum[i in Q_2]( a_ij )) <= 1
for j in 1...n
"""

if __name__ == '__main__':
    arg_parser = arg.ArgumentParser(
        formatter_class=arg.ArgumentDefaultsHelpFormatter
    )
    arg_parser.add_argument(
        '-r', '--number-of-rows',
        help='Desired number of rows in the matrix',
        type=positive_int,
        default=3
    )
    arg_parser.add_argument(
        '-c', '--number-of-columns',
        help='Desired number of columns in the matrix',
        type=positive_int,
        default=3
    )
    arg_parser.add_argument(
        '-v', '--verbose',
        help='Whether to emit results of intermediate checks',
        action='store_true'
    )

    args = arg_parser.parse_args()

    chatty = args.verbose 
    A = np.random.random_integers(
        -1, 1, size=(args.number_of_rows, args.number_of_columns)
    )
    M = set(xrange(A.shape[0]))
    n = A.shape[1]

    counterexample_found = False

    print('Assessing the following matrix for TUM:')
    print(A)

    for Q in power_set(M):
        verbose(chatty, 'Q =', Q)

        found_suitable_partition = False

        for sub in power_set(Q):
            Q1 = set(sub)
            Q2 = set(Q) - Q1
            verbose(chatty, 'sub =', sub, 'Q1 =', Q1, 'Q2 =', Q2)

            if all(
                abs(sum(A[i, j] for i in Q1)
                    -
                    sum(A[i, j] for i in Q2)) <= 1
                for j in xrange(n)):
	
                verbose(chatty, 'Found a partition of Q =', Q, 'that suits:')
                verbose(chatty, 'Q1:', Q1, 'Q2:', Q2)
                verbose(chatty, 'Q1 rows:')
                verbose(chatty, A[sorted(list(Q1))])
                verbose(chatty, 'Q2 rows:')
                verbose(chatty, A[sorted(list(Q2))])
                found_suitable_partition = True
                break

        if not found_suitable_partition:
            print('Could not find suitable partition for Q =', Q)
            print(A[sorted(list(Q))])
            print('Therefore, the matrix is *not* totally unimodular.')
            counterexample_found = True
            break

    if not counterexample_found: 
        print(
            'Found suitable partitions for all subsets of rows of matrix.'
        )
        print('Therefore, the matrix *is* totally unimodular.')

