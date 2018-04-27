import cplex
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
        self.graph = graph
        self.antigraph = complement(graph)
        self.nodes = sorted(graph.nodes())
        self.solve_as = solve_as
        self.cx = self.init_cplex()

    def init_cplex(self):
        cx = cplex.Cplex()

        cx.objective.set_sense(cx.objective.sense.minimize)
        var_names = self.all_vars()
        reps_own_color_var_names = self.represents_own_color_class_vars()
        objective = [
            1.0 if v in reps_own_color_var_names else 0.0
            for v in var_names]

        if 'ip' == self.solve_as:
            cx.variables.add(
                obj=objective,
                types=[cx.variables.type.binary] * len(var_names),
                names=var_names
            )
        else:
            cx.variables.add(
                obj=objective,
                ub=[1.0] * len(var_names),
                names=var_names
            )

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
        cx.linear_constraints.add(
            lin_expr=map(lambda c: c.terms(), constraints),
            senses=map(lambda c: c.sense(), constraints),
            rhs=map(lambda c: c.rhs(), constraints),
            names=map(lambda c: c.name(), constraints)
        )

        return cx

    def suppress_output(self):
        self.cx.set_log_stream(None)
        self.cx.set_error_stream(None)
        self.cx.set_warning_stream(None)
        self.cx.set_results_stream(None)

    def solve(self):
        start = self.cx.get_dettime()
        self.cx.solve()
        end = self.cx.get_dettime()
        return Solution(self, self.cx.solution, end - start)

    def add_cuts(self, cuts):
        for cut in cuts:
            self.cx.linear_constraints.add(
                lin_expr=[cut.terms()],
                senses=[cut.sense()],
                rhs=[cut.rhs()],
                names=[cut.name()]
            )

    def clique_cuts(self):
        i = 0
        for u in self.nodes:
            for q in filter(
                lambda cl: len(cl) > 2,
                find_cliques(self.graph.subgraph(self.antigraph.neighbors(u)))
            ):
                i += 1
                yield CliqueCut(self, u, q, i)

    def emit_to(self, path):
        self.cx.write(path, 'lp')

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
