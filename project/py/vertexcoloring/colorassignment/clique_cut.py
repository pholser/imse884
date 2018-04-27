from ..constraint import Constraint


class CliqueCut(Constraint):
    def __init__(self, problem, clique, color, cut_id):
        self.problem = problem
        self.clique = sorted(clique)
        self.color = color
        self.id = cut_id

    def name(self):
        return 'q%d' % self.id

    def terms(self):
        return [
            [self.problem.node_color_var(n, self.color) for n in self.clique]
            + [self.problem.color_used_var(self.color)],
            [1.0] * len(self.clique) + [-1.0]
        ]

    def rhs(self):
        return 0.0

    def sense(self):
        return 'L'

    def allows(self, solution):
        clique_vars = [
            self.problem.node_color_var(n, self.color)
            for n in self.clique
        ]
        color_used_var = self.problem.color_used_var(self.color)
        clique_values = solution.value_of(clique_vars)
        color_used_value = solution.value_of(color_used_var)

        return sum(clique_values) - color_used_value <= self.rhs()
