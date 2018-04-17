#!/usr/bin/env python

import argparse as arg
import networkx as nx
import matplotlib.pyplot as plt
import vertexcoloring.colorassignment.problem as assign
import vertexcoloring.representative.problem as rep

from vertexcoloring.dimacs.parser import Parser
from matplotlib import colors as mcolors
from operator import itemgetter


def plot(graph, solution):
    graph_pos = nx.shell_layout(graph)

    node_list = []
    color_list = []
    for n, k in solution.colors_by_node().iteritems():
        node_list.append(n)
        color_list.append(k)

    color_indices = map(lambda k: color_list.index(k), color_list)
    color_names = itemgetter(*color_indices)(mcolors.cnames.keys())

    nx.draw_networkx_nodes(
        graph,
        graph_pos,
        nodelist=node_list,
        node_color=color_names,
        alpha=0.3)
    nx.draw_networkx_edges(graph, graph_pos, edge_color='lightslategray')
    nx.draw_networkx_labels(graph, graph_pos, font_size=12, font_family='sans-serif')

    plt.show()


if __name__ == '__main__':
    arg_parser = arg.ArgumentParser(
        formatter_class=arg.ArgumentDefaultsHelpFormatter
    )

    arg_parser.add_argument(
        '-g', '--graph',
        help='Path to graph description for graph to color (DIMACS format)',
        required=True
    )
    arg_parser.add_argument(
        '-f', '--formulation',
        help='Desired formulation of vertex coloring',
        choices=['rep', 'assign'],
        default='assign'
    )
    arg_parser.add_argument(
        '-p', '--problem-file',
        help='Path to write CPLEX LP file for problem to',
        default='./vertexcoloring.lp'
    )
    arg_parser.add_argument(
        '-s', '--solve-as',
        help='Whether to solve as IP, or LR with cuts',
        choices=['ip', 'lr'],
        default='ip'
    )

    args = arg_parser.parse_args()

    print 'Reading graph from %s...' % args.graph
    graph = Parser().parse(args.graph)
    print '...done.'

    keep_cutting = True
    candidate_clique_cuts = {}
    new_clique_cuts = []
    problem = None
    solution = None

    while keep_cutting:
        if not problem:
            problem = {
                'rep': rep.Problem,
                'assign': assign.Problem
            }[args.formulation](graph, args.solve_as)
            candidate_clique_cuts = {
                q.id: q for q in problem.clique_cuts()
            }

        problem.add_cuts(new_clique_cuts)
        problem.suppress_output()

        if args.problem_file:
            problem.emit_to(args.problem_file)

        solution = problem.solve()
        print 'Linear relaxation solution time:', solution.running_time
        print 'Objective value:', solution.objective_value()

        new_clique_cuts = filter(
            lambda cut: not cut.allows(solution),
            candidate_clique_cuts.itervalues())
        for q in new_clique_cuts:
            del candidate_clique_cuts[q.id]

        keep_cutting = len(new_clique_cuts) > 0

    print 'Number of colors used:', solution.objective_value()
    for n, v in sorted(solution.values().iteritems()):
        print 'Value of variable %s: %f' % (n, v)

    if solution.is_integer():
        plot(graph, solution)
