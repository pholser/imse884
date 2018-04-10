class Solution(object):
    def __init__(self, format, cplex_solution):
        self.format = format
        self.cplex_solution = cplex_solution

    def nodes(self):
        return self.format.nodes

    def colors(self):
        return self.format.colors

    def objective_value(self):
        return self.cplex_solution.get_objective_value()

    def color_used(self, k):
        return self.cplex_solution.get_values(
            self.format.color_used_var(k)
        )

    def node_colored_as(self, n, k):
        return self.cplex_solution.get_values(
            self.format.node_color_var(n, k)
        )