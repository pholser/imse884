import sys

from collections import defaultdict
from ..is_close import isclose
from ..vertex_coloring_solution import VertexColoringSolution


class Solution(VertexColoringSolution):
    def __init__(self, problem, cplex_solution, running_time):
        self.problem = problem
        self.cplex_solution = cplex_solution
        self.running_time = running_time

    def objective_value(self):
        return self.cplex_solution.get_objective_value()

    def values(self):
        return {
            v: self.cplex_solution.get_values(v)
            for v in self.problem.all_vars()
        }

    def show(self, to=sys.stdout):
        for n, v in sorted(self.values().iteritems()):
            print >> to, 'Value of variable %s: %f' % (n, v)

    def value_of(self, *variable_names):
        return self.cplex_solution.get_values(*variable_names)

    def is_integer(self):
        return all(isclose(val, int(val)) for val in self.values().itervalues())

    def used_colors(self):
        return sorted(
            map(
                self.problem.color_for_used_var,
                {
                    k for k, v in filter(
                        lambda e:
                            e[0] in self.problem.color_used_vars()
                            and e[1] >= 0.999,
                        self.values().iteritems()
                    )
                }
            )
        )

    def colors_by_node(self):
        all_node_color_vars = set(self.problem.all_node_color_vars())

        node_color_vars = {
            k for k, v in filter(
                lambda e:
                    e[0] in all_node_color_vars
                    and e[1] >= 0.999,
                self.values().iteritems()
            )
        }
        return dict(
            map(
                self.problem.node_color_pairing_for_var,
                node_color_vars
            )
        )

    def nodes_by_color(self):
        by_color = defaultdict(list)
        for n, k in self.colors_by_node().iteritems():
            by_color[k].append(n)
        return by_color
