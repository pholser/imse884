from dimacs.parser import Parser
from formulation.colorassignment.color_assignment import ColorAssignment


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
    arg_parser.add_argument(
        '-p', '--problem-file',
        help='Path to write CPLEX LP file for problem to',
        default='./vertexcoloring.lp'
    )

    args = arg_parser.parse_args()

    print 'Reading graph from %s...' % (args.graph)
    graph = Parser().parse(args.graph)
    print '...done.'

    formulation = ColorAssignment(graph)
    formulation.emit_lpsolve_to(args.problem_file)

    # TODO: delegate the cplex machinery to the formulation
    # TODO: get formulation to extract right var values, obj, ...

    problem = formulation.problem_from_lpsolve(args.problem_file)
    solution = problem.solve()

    print 'Number of colors used: %d' % solution.objective_value
    print 'Color classes:'
    for k, nodes in solution.color_classes.iteritems():
        print 'Color', k, ':', nodes
