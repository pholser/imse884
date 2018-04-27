from ..constraint import Constraint


class NodeGettingColorConstraint(Constraint):
    def __init__(self, problem, n):
        self.problem = problem
        self.n = n

    def name(self):
        return 'n%d' % self.n

    def terms(self):
        return [
            [self.problem.node_color_var(self.n, k) for k in self.problem.colors],
            [1.0] * len(self.problem.colors)
        ]

    def rhs(self):
        return 1.0

    def sense(self):
        return 'E'
