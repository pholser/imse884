import cplex
import re

from distinct_representatives_for_neighbors_constraint \
    import DistinctRepresentativeForNeighborsConstraint
from itertools import chain
from networkx.algorithms.operators.unary import complement
from representative_constraint import RepresentativeConstraint
from solution import Solution


class Problem(object):
    def __init__(self, graph, solve_as):
        self.graph = graph
        self.antigraph = complement(graph)
        self.nodes = sorted(graph.nodes())
        self.solve_as = solve_as
        self.cx = cplex.Cplex()
        self.cx.objective.set_sense(self.cx.objective.sense.minimize)
        self.var_names = self.all_vars()
        self.reps_own_color_var_names = self.represents_own_color_class_vars()
        self.objective = [
            1.0 if v in self.reps_own_color_var_names else 0.0
            for v in self.var_names]

        if 'ip' == solve_as:
            self.cx.variables.add(
                obj=self.objective,
                types=[self.cx.variables.type.binary] * len(self.var_names),
                names=self.var_names
            )
        else:
            self.cx.variables.add(
                obj=self.objective,
                ub=[1.0] * len(self.var_names),
                names=self.var_names
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
        self.cx.linear_constraints.add(
            lin_expr=map(lambda c: c.terms(), constraints),
            senses=map(lambda c: c.sense(), constraints),
            rhs=map(lambda c: c.rhs(), constraints),
            names=map(lambda c: c.name(), constraints)
        )

    def solve(self):
        self.cx.solve()
        return Solution(self, self.cx.solution)

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
