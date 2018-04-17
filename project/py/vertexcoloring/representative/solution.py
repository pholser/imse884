import sys

from collections import defaultdict

from ..is_close import isclose


class Solution(object):
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

    def value_of(self, *vars):
        return self.cplex_solution.get_values(*vars)

    def is_integer(self):
        return all(isclose(val, abs(val)) for val in self.values().itervalues())

    def used_colors(self):
        represents_own_color_class_vars = \
            self.problem.represents_own_color_class_vars()

        return map(
            self.problem.color_class_for_representative_var,
            {
                k for k, v in filter(
                    lambda e:
                        e[0] in represents_own_color_class_vars
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
                self.problem.color_class_for_representative_var(e[0]) in color_classes
                and e[1] >= 0.999,
                self.values().iteritems()
            )
        }
        return dict(
            map(
                self.problem.representative_pairing_for_var,
                representative_vars
            )
        )

    def nodes_by_color(self):
        by_color = defaultdict(list)
        for n, k in self.colors_by_node().iteritems():
            by_color[k].append(n)
        return by_color
