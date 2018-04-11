from dimacs.parser import Parser
from formulation.colorassignment.color_assignment import ColorAssignment
from formulation.representative.representative import Representative

import argparse as arg

if __name__ == '__main__':
    arg_parser = arg.ArgumentParser()

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
        '-t', '--problem-file-type',
        help='Flavor of problem to write',
        choices=['ip', 'lr'],
        default='ip'
    )

    args = arg_parser.parse_args()

    print 'Reading graph from %s...' % args.graph
    graph = Parser().parse(args.graph)
    print '...done.'

    formulation = {
        'rep': Representative,
        'assign': ColorAssignment
    }[args.formulation](graph)

    formulation.emit_to(args.problem_file, args.problem_file_type)

    problem = formulation.problem_from_file(args.problem_file)
    solution = problem.solve()

    print 'Objective value:', solution.objective_value()
    for n, v in solution.values().iteritems():
        print 'Value of variable %s: %f' % (n, v)
