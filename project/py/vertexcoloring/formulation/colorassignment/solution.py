from collections import defaultdict


class Solution(object):
    def __init__(self, format, cplex_solution):
        self.format = format
        self.cplex_solution = cplex_solution

    def objective_value(self):
        return self.cplex_solution.get_objective_value()

    def values(self):
        return {
            v: self.cplex_solution.get_values(v)
            for v in self.format.all_vars()
        }

    def used_colors(self):
        return sorted(
            map(
                self.format.color_for_used_var,
                {
                    k for k, v in filter(
                        lambda e:
                            e[0] in self.format.color_used_vars()
                            and e[1] >= 0.999,
                        self.values().iteritems()
                    )
                }
            )
        )

    def colors_by_node(self):
        all_node_color_vars = set(self.format.all_node_color_vars())

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
                self.format.node_color_pairing_for_var,
                node_color_vars
            )
        )

    def nodes_by_color(self):
        by_color = defaultdict(list)
        for n, k in self.colors_by_node().iteritems():
            by_color[k].append(n)
        return by_color
