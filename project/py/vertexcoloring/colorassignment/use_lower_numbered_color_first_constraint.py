from ..constraint import Constraint


class UseLowerNumberedColorFirstConstraint(Constraint):
    def __init__(self, problem, k):
        self.problem = problem
        self.k = k

    def name(self):
        return 's2_%d' % self.k

    def terms(self):
        return [
            [self.problem.color_used_var(self.k),
             self.problem.color_used_var(self.k + 1)],
            [1.0, -1.0]
        ]

    def rhs(self):
        return 0.0

    def sense(self):
        return 'G'
