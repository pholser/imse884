import re

from adjacent_node_color_constraint import AdjacentNodeColorConstraint
from clique_cut import CliqueCut
from color_used_only_if_marks_node_constraint import ColorUsedOnlyIfMarksNodeConstraint
from networkx.algorithms.clique import find_cliques
from node_getting_color_constraint import NodeGettingColorConstraint
from solution import Solution
from use_lower_numbered_color_first_constraint import UseLowerNumberedColorFirstConstraint
from ..vertex_coloring_problem import VertexColoringProblem


class Problem(VertexColoringProblem):
    def __init__(self, graph, solve_as):
        super(Problem, self).__init__(solve_as)

        self.graph = graph
        self.nodes = sorted(graph.nodes)
        self.edges = sorted(map(sorted, graph.edges()))
        self.colors = self.nodes
        self.init_cplex()

    def init_cplex(self):
        self.set_sense_minimize()

        var_names = self.all_node_color_vars() + self.color_used_vars()
        objective_coefficients = [0.0] * len(self.all_node_color_vars()) \
            + [1.0] * len(self.color_used_vars())

        self.set_objective(objective_coefficients, var_names)

        constraints = [
            NodeGettingColorConstraint(self, n)
            for n in self.nodes
        ]
        constraints.extend(
            [AdjacentNodeColorConstraint(self, e[0], e[1], k)
             for e in self.edges
             for k in self.colors]
        )
        constraints.extend(
            [ColorUsedOnlyIfMarksNodeConstraint(self, k) for k in self.colors]
        )
        constraints.extend(
            [UseLowerNumberedColorFirstConstraint(self, k)
             for k in self.colors[:-1]]
        )
        self.add_constraints(constraints)

    def solve(self):
        cplex_solution, solution_time = self.cplex_solve()
        return Solution(self, cplex_solution, solution_time)

    def clique_cuts(self):
        i = 0
        for q in filter(lambda cl: len(cl) > 2, find_cliques(self.graph)):
            for k in self.colors:
                i += 1
                yield CliqueCut(self, q, k, i)

    def all_vars(self):
        return self.all_node_color_vars() + self.color_used_vars()

    def all_node_color_vars(self):
        all = []
        for n in self.nodes:
            all.extend(self.node_color_vars(n))
        return all

    def node_color_vars(self, n):
        return [self.node_color_var(n, k) for k in self.colors]

    def node_color_var(self, n, k):
        return 'x%d,%d' % (n, k)

    def color_used_vars(self):
        return [self.color_used_var(k) for k in self.colors]

    def color_used_var(self, color):
        return 'w%d' % color

    def color_for_used_var(self, var):
        return int(re.match('^w(.*)$', var).group(1))

    def node_color_pairing_for_var(self, var):
        return map(int, re.match('^x(.*),(.*)$', var).group(1, 2))
