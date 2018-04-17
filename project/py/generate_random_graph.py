#!/usr/bin/env python

import argparse as arg
import networkx as nx

from vertexcoloring.dimacs.formatter import Formatter


class Probability(object):
    def __eq__(self, other):
        return 0.0 <= other <= 1.0

    def __repr__(self):
        return '0...1'


if __name__ == '__main__':
    arg_parser = arg.ArgumentParser(
        formatter_class=arg.ArgumentDefaultsHelpFormatter
    )

    arg_parser.add_argument(
        '-n', '--number-of-nodes',
        help='Desired number of nodes in the graph',
        type=int,
        required=True
    )
    arg_parser.add_argument(
        '-p', '--probability-of-edge-creation',
        help='Probability of an edge between any two nodes',
        type=float,
        choices=[Probability()],
        default=0.5,
    )
    arg_parser.add_argument(
        '-s', '--seed',
        help='Seed for the random number generator',
        type=int
    )

    args = arg_parser.parse_args()

    graph = nx.fast_gnp_random_graph(
        args.number_of_nodes,
        args.probability_of_edge_creation,
        args.seed
    )

    print Formatter().format(graph)
