import re

from solution import Solution


class LPFormat(object):
    def __init__(self, graph):
        self.nodes = sorted(graph.nodes)
        self.edges = sorted(map(sorted, graph.edges()))
        self.colors = self.nodes

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
        lines.append('colors_used: ' + ' + '.join(self.color_used_vars()))

    def emit_constraints(self, lines):
        lines.append('Subject To')
        for n in self.nodes:
            lines.append(self.nodes_getting_color_constraint(n))
        for e in self.edges:
            for k in self.colors:
                lines.append(
                    self.adjacent_nodes_colored_differently_constraint(e, k)
                )
        for k in self.colors:
            lines.append(
                self.color_used_only_if_color_marks_a_node_constraint(k)
            )
        for k in self.colors[:-1]:
            lines.append(
                self.use_lower_numbered_colors_first_constraint(k)
            )

    def emit_ip_bounds(self, lines):
        lines.append('Binary')
        for n in self.nodes:
            lines.append(' '.join(self.node_color_vars(n)))
        lines.append(' '.join(self.color_used_vars()))

    def emit_lr_bounds(self, lines):
        lines.append('Bounds')
        for n in self.nodes:
            for k in self.colors:
                lines.append('0 <= ' + self.node_color_var(n, k) + ' <= 1')
        for k in self.colors:
            lines.append('0 <= ' + self.color_used_var(k) + ' <= 1')

    def emit_end(self, lines):
        lines.append('End')

    def nodes_getting_color_constraint(self, n):
        return self.node_getting_color_constraint_name(n) + ': ' \
               + ' + '.join(self.node_color_vars(n)) \
               + ' = 1'

    def node_getting_color_constraint_name(self, n):
        return 'n%d' % n

    def adjacent_nodes_colored_differently_constraint(self, e, k):
        return self.adjacent_nodes_colored_differently_constraint_name(e, k) \
               + ': ' \
               + self.node_color_var(e[0], k) \
               + ' + ' \
               + self.node_color_var(e[1], k) \
               + ' - ' + self.color_used_var(k) \
               + ' <= 0'

    def adjacent_nodes_colored_differently_constraint_name(self, e, k):
        return 'e%d,%d_%d' % (e[0], e[1], k)

    def color_used_only_if_color_marks_a_node_constraint(self, k):
        return self.color_used_only_if_color_marks_a_node_constraint_name(k) \
            + ': ' \
            + ' + '.join([self.node_color_var(n, k) for n in self.nodes]) \
            + ' - ' + self.color_used_var(k) \
            + ' >= 0'

    def color_used_only_if_color_marks_a_node_constraint_name(self, k):
        return 's1_%d' % k

    def use_lower_numbered_colors_first_constraint(self, k):
        return self.use_lower_numbered_colors_first_constraint_name(k) \
            + ': ' \
            + self.color_used_var(k) + ' - ' + self.color_used_var(k + 1) \
            + ' >= 0'

    def use_lower_numbered_colors_first_constraint_name(self, k):
        return 's2_%d' % k

    def all_vars(self):
        return self.all_node_color_vars() + self.color_used_vars()

    def color_used_vars(self):
        return [self.color_used_var(k) for k in self.colors]

    def color_used_var(self, color):
        return 'w%d' % color

    def color_for_used_var(self, var):
        return int(re.match('^w(.*)$', var).group(1))

    def all_node_color_vars(self):
        all = []
        for n in self.nodes:
            all.extend(self.node_color_vars(n))
        return all

    def node_color_vars(self, n):
        return [self.node_color_var(n, k) for k in self.colors]

    def node_color_var(self, n, k):
        return 'x%d,%d' % (n, k)

    def node_color_pairing_for_var(self, var):
        return map(int, re.match('^x(.*),(.*)$', var).group(1, 2))

    def solution(self, cplex_solution):
        return Solution(self, cplex_solution)
