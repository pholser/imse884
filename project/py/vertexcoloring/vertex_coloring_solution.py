import sys

from abc import ABCMeta, abstractmethod
from collections import defaultdict

from is_close import isclose


class VertexColoringSolution:
    __metaclass__ = ABCMeta

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

    def value_of(self, *variable_names):
        return self.cplex_solution.get_values(*variable_names)

    def show(self, to=sys.stdout):
        for n, v in sorted(self.values().iteritems()):
            print >> to, 'Value of variable %s: %f' % (n, v)

    def is_integer(self):
        return all(isclose(val, int(val)) for val in self.values().itervalues())

    @abstractmethod
    def used_colors(self):
        pass

    @abstractmethod
    def colors_by_node(self):
        pass

    def nodes_by_color(self):
        by_color = defaultdict(list)
        for n, k in self.colors_by_node().iteritems():
            by_color[k].append(n)
        return by_color
