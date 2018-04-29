import re

from clique_cut import CliqueCut
from distinct_representatives_for_neighbors_constraint \
    import DistinctRepresentativeForNeighborsConstraint
from itertools import chain
from networkx.algorithms.clique import find_cliques
from networkx.algorithms.operators.unary import complement
from representative_constraint import RepresentativeConstraint
from solution import Solution
from ..vertex_coloring_problem import VertexColoringProblem


class Problem(VertexColoringProblem):
    def __init__(self, graph, solve_as):
        super(Problem, self).__init__(solve_as)

        self.graph = graph
        self.antigraph = complement(graph)
        self.nodes = sorted(graph.nodes())
        self.init_cplex()

    def init_cplex(self):
        self.set_sense_minimize()

        var_names = self.all_vars()
        reps_own_color_var_names = self.represents_own_color_class_vars()
        objective_coefficients = [
            1.0 if v in reps_own_color_var_names else 0.0
            for v in var_names]

        self.set_objective(objective_coefficients, var_names)

        constraints = [
            RepresentativeConstraint(self, n)
            for n in self.nodes
        ]
        constraints.extend(
            [DistinctRepresentativeForNeighborsConstraint(
                self, n, v, w
            ) for n in self.nodes
              for v, w in self.graph.subgraph(
                  self.antigraph.neighbors(n)
              ).edges()
            ]
        )
        self.add_constraints(constraints)

    def solve(self):
        cplex_solution, solution_time = self.cplex_solve()
        return Solution(self, cplex_solution, solution_time)

    def clique_cuts(self):
        i = 0
        for u in self.nodes:
            for q in filter(
                lambda cl: len(cl) > 2,
                find_cliques(self.graph.subgraph(self.antigraph.neighbors(u)))
            ):
                i += 1
                yield CliqueCut(self, u, q, i)

    def all_vars(self):
        return [vs for n in self.nodes for vs in self.represents_color_class_of_vars(n)]

    def represents_color_class_of_vars(self, n):
        return [
            self.represents_color_class_of_var(n, v)
            for v in sorted(chain({n}, self.antigraph.neighbors(n)))
        ]

    def represents_own_color_class_vars(self):
        return [
            self.represents_color_class_of_var(n, n) for n in self.nodes
        ]

    def represents_color_class_of_var(self, representative, other):
        return 'x%d,%d' % (representative, other)

    def color_class_for_representative_var(self, var):
        return int(re.match('^x(.*),(.*)$', var).group(1))

    def representative_pairing_for_var(self, var):
        match = re.match('^x(.*),(.*)$', var)
        return int(match.group(2)), int(match.group(1))
