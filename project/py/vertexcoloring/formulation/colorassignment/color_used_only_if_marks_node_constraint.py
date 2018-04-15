class ColorUsedOnlyIfMarksNodeConstraint(object):
    def __init__(self, problem, k):
        self.problem = problem
        self.k = k

    def name(self):
        return 's1_%d' % self.k

    def terms(self):
        return [
            [self.problem.node_color_var(n, self.k) for n in self.problem.nodes]
            + [self.problem.color_used_var(self.k)],
            [1.0] * len(self.problem.nodes) + [-1.0]
        ]

    def rhs(self):
        return 0.0

    def sense(self):
        return 'G'
