import cplex

from distinct_representatives_for_neighbors_constraint \
    import DistinctRepresentativeForNeighborsConstraint
from lp_format import LPFormat
from representative_constraint import RepresentativeConstraint


class Problem(object):
    def __init__(self, graph, solve_as):
        self.format = LPFormat(graph)
        self.graph = graph
        self.solve_as = solve_as
        self.cx = cplex.Cplex()
        self.cx.objective.set_sense(self.cx.objective.sense.minimize)
        self.var_names = self.format.all_vars()
        self.reps_own_color_var_names = self.format.represents_own_color_class_vars()
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
            RepresentativeConstraint(self.format, n)
            for n in self.format.nodes
        ]
        constraints.extend(
            [DistinctRepresentativeForNeighborsConstraint(
                self.format, n, v, w
            ) for n in self.format.nodes
              for v, w in self.graph.subgraph(
                self.format.antigraph.neighbors(n)
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
        return self.format.solution(self.cx.solution)

    def emit_to(self, path):
        self.cx.write(path, 'lp')
