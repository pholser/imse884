from dimacs.parser import Parser
from networkx.algorithms.clique import find_cliques
from networkx.algorithms.operators.unary import complement


class Solver:
    pass


import argparse as arg

if __name__ == '__main__':
    arg_parser = arg.ArgumentParser()

    arg_parser.add_argument(
        '-g', '--graph',
        help='Path to graph description for graph to color (DIMACS format)',
        required=True
    )

    args = arg_parser.parse_args()

    print 'Reading graph from %s...' % (args.graph)
    graph = Parser().parse(args.graph)
    print '...done.'

    for q in filter(lambda k: len(k) > 2, find_cliques(graph)):
        print q
#     for i in find_cliques(complement(graph)):
#        print i