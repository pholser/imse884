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
        return map(
            self.format.color_class_for_representative_var,
            {
                k for k, v in filter(
                    lambda e:
                        e[0] in self.format.represents_own_color_class_vars()
                        and e[1] >= 0.999,
                    self.values().iteritems()
                )
            }
        )

    def colors_by_node(self):
        color_classes = self.used_colors()

        representative_vars = {
            k for k, v in filter(
                lambda e:
                    self.format.color_class_for_representative_var(e[0]) in color_classes
                    and e[1] >= 0.999,
                self.values().iteritems()
            )
        }
        return dict(
            map(
                self.format.representative_pairing_for_var,
                representative_vars
            )
        )

    def nodes_by_color(self):
        by_color = defaultdict(list)
        for n, k in self.colors_by_node().iteritems():
            by_color[k].append(n)
        return by_color
