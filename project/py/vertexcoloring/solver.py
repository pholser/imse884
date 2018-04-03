from dimacs.parser import Parser


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

    graph = Parser().parse(args.graph)
    print 'Number of nodes: %d\nNumber of edges: %d' % (
        len(graph.nodes),
        len(graph.edges)
    )