from vertexcoloring.formulation.colorassignment.solution import Solution


class LPFormat(object):
    def __init__(self, graph):
        self.nodes = sorted(graph.nodes)
        self.edges = sorted(map(sorted, graph.edges()))
        self.colors = self.nodes

    def emit(self):
        lines = []

        self.emit_objective(lines)
        self.emit_constraints(lines)
        self.emit_bounds(lines)
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

    def emit_bounds(self, lines):
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
               + ' + '.join([self.node_color_var(n, k) for k in self.colors]) \
               + ' = 1'

    def node_getting_color_constraint_name(self, n):
        return 'n' + n

    def adjacent_nodes_colored_differently_constraint(self, e, k):
        return self.adjacent_nodes_colored_differently_constraint_name(e, k) \
               + ': ' \
               + self.node_color_var(e[0], k) \
               + ' + ' \
               + self.node_color_var(e[1], k) \
               + ' - ' + self.color_used_var(k) \
               + ' <= 0'

    def adjacent_nodes_colored_differently_constraint_name(self, e, k):
        return 'e' + e[0] + ',' + e[1] + '_' + k

    def color_used_vars(self):
        return [self.color_used_var(k) for k in self.colors]

    def color_used_var(self, color):
        return 'w' + color

    def node_color_var(self, n, k):
        return 'x' + n + ',' + k

    def solution(self, cplex_solution):
        return Solution(self, cplex_solution)
