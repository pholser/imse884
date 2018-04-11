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

    args = arg_parser.parse_args()

    print 'Reading graph from %s...' % (args.graph)
    graph = Parser().parse(args.graph)
    print '...done.'

    formulation = {
        'rep' : Representative,
        'assign' : ColorAssignment
    }[args.formulation](graph)

    formulation.emit_ip_to(args.problem_file)

    # TODO: delegate the cplex machinery to the formulation
    # TODO: get formulation to extract right var values, obj, ...

    problem = formulation.problem_from_lpsolve(args.problem_file)
    solution = problem.solve()

    print 'Objective value:', solution.objective_value()
    for k in solution.colors():
        if solution.color_used(k) > 0:
            print 'Color', k, 'used:', solution.color_used(k)
    for n in solution.nodes():
        for k in solution.colors():
            if solution.node_colored_as(n, k) > 0:
                print 'Node', n, 'colored as', k, ':', \
                    solution.node_colored_as(n, k)
