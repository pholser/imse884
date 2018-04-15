import cplex
import re

from adjacent_node_color_constraint import AdjacentNodeColorConstraint
from color_used_only_if_marks_node_constraint import ColorUsedOnlyIfMarksNodeConstraint
from node_getting_color_constraint import NodeGettingColorConstraint
from solution import Solution
from use_lower_numbered_color_first_constraint import UseLowerNumberedColorFirstConstraint


class Problem(object):
    def __init__(self, graph, solve_as):
        self.graph = graph
        self.nodes = sorted(graph.nodes)
        self.edges = sorted(map(sorted, graph.edges()))
        self.colors = self.nodes
        self.solve_as = solve_as
        self.cx = cplex.Cplex()
        self.cx.objective.set_sense(self.cx.objective.sense.minimize)
        self.var_names = self.all_node_color_vars() + self.color_used_vars()
        self.objective = [0.0] * len(self.all_node_color_vars()) \
            + [1.0] * len(self.color_used_vars())

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
        self.cx.linear_constraints.add(
            lin_expr=map(lambda c: c.terms(), constraints),
            senses=map(lambda c: c.sense(), constraints),
            rhs=map(lambda c: c.rhs(), constraints),
            names=map(lambda c: c.name(), constraints)
        )

    def suppress_output(self):
        self.cx.set_log_stream(None)
        self.cx.set_error_stream(None)
        self.cx.set_warning_stream(None)
        self.cx.set_results_stream(None)

    def solve(self):
        self.cx.solve()
        return Solution(self, self.cx.solution)

    def emit_to(self, path):
        self.cx.write(path, 'lp')

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
