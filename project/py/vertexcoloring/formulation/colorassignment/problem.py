import cplex

from adjacent_node_color_constraint import AdjacentNodeColorConstraint
from color_used_only_if_marks_node_constraint import ColorUsedOnlyIfMarksNodeConstraint
from node_getting_color_constraint import NodeGettingColorConstraint
from use_lower_numbered_color_first_constraint import UseLowerNumberedColorFirstConstraint
from lp_format import LPFormat


class Problem(object):
    def __init__(self, graph, solve_as):
        self.format = LPFormat(graph)
        self.graph = graph
        self.solve_as = solve_as
        self.cx = cplex.Cplex()
        self.cx.objective.set_sense(self.cx.objective.sense.minimize)
        self.var_names = \
            self.format.all_node_color_vars() + self.format.color_used_vars()
        self.objective = [0.0] * len(self.format.all_node_color_vars()) \
            + [1.0] * len(self.format.color_used_vars())

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
            NodeGettingColorConstraint(self.format, n)
            for n in self.format.nodes
        ]
        constraints.extend(
            [AdjacentNodeColorConstraint(self.format, e[0], e[1], k)
             for e in self.format.edges
             for k in self.format.colors]
        )
        constraints.extend(
            [ColorUsedOnlyIfMarksNodeConstraint(
                self.format,
                k) for k in self.format.colors]
        )
        constraints.extend(
            [UseLowerNumberedColorFirstConstraint(
                self.format,
                k) for k in self.format.colors[:-1]]
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
