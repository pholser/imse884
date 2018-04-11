from itertools import chain
from networkx.algorithms.operators.unary import complement
from vertexcoloring.formulation.representative.solution import Solution


class LPFormat(object):
    def __init__(self, graph):
        self.graph = graph
        self.antigraph = complement(graph)
        self.nodes = sorted(graph.nodes())

    def emit_ip(self):
        lines = []

        self.emit_objective(lines)
        self.emit_constraints(lines)
        self.emit_ip_bounds(lines)
        self.emit_end(lines)

        return "\n".join(lines)

    def emit_lr(self):
        lines = []

        self.emit_objective(lines)
        self.emit_constraints(lines)
        self.emit_lr_bounds(lines)
        self.emit_end(lines)

        return "\n".join(lines)

    def emit_objective(self, lines):
        lines.append('Minimize')
        lines.append(
            'color_reps: ' + ' + '.join(self.represents_own_color_class_vars())
        )

    def emit_constraints(self, lines):
        lines.append('Subject To')
        for n in self.nodes:
            lines.append(self.representative_constraint(n))
        for n in self.nodes:
            for v, w in self.graph.subgraph(self.antigraph.neighbors(n)).edges():
                lines.append(
                    self.distinct_representatives_for_neighbors_constraint(n, v, w)
                )

    def emit_ip_bounds(self, lines):
        lines.append('Binary')
        for n in self.nodes:
            lines.append(
                ' '.join(self.represents_color_class_of_vars(n)))

    def all_vars(self):
        return [vs for n in self.nodes for vs in self.represents_color_class_of_vars(n)]

    def represents_color_class_of_vars(self, n):
        return [
            self.represents_color_class_of_var(n, v)
            for v in sorted(chain({n}, self.antigraph.neighbors(n)))
        ]

    def emit_lr_bounds(self, lines):
        lines.append('Bounds')
        for n in self.nodes:
            for v in sorted(chain({n}, self.antigraph.neighbors(n))):
                lines.append('0 <= ' + self.represents_color_class_of_var(n, v) + ' <= 1')

    def emit_end(self, lines):
        lines.append('End')

    def solution(self, cplex_solution):
        return Solution(self, cplex_solution)

    def represents_own_color_class_vars(self):
        return [
            self.represents_color_class_of_var(n, n) for n in self.nodes
        ]

    def represents_color_class_of_var(self, representative, other):
        return 'x' + representative + ',' + other

    def representative_constraint(self, n):
        return self.representative_constraint_name(n) \
               + ': ' \
               + ' + '.join([
                   self.represents_color_class_of_var(u, n)
                   for u in chain({n}, self.antigraph.neighbors(n))
               ]) \
               + ' >= 1'

    def representative_constraint_name(self, n):
        return 'rep' + n

    def distinct_representatives_for_neighbors_constraint(self, n, v, w):
        return self.distinct_representatives_for_neighbors_constraint_name(n, v, w) \
               + ': ' \
               + ' + '.join([
                   self.represents_color_class_of_var(n, v),
                   self.represents_color_class_of_var(n, w)
               ]) \
               + ' - ' \
               + self.represents_color_class_of_var(n, n) \
               + ' <= 0'

    def distinct_representatives_for_neighbors_constraint_name(self, n, v, w):
        return 'uqrep' + n + '_' + v + ',' + w
