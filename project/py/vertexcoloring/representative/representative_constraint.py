from ..constraint import Constraint
from itertools import chain


class RepresentativeConstraint(Constraint):
    def __init__(self, problem, n):
        self.problem = problem
        self.n = n

    def name(self):
        return 'rep%d' % self.n

    def terms(self):
        vars = [
            self.problem.represents_color_class_of_var(u, self.n)
            for u in chain(
                {self.n},
                sorted(self.problem.antigraph.neighbors(self.n))
            )
        ]
        return [
            vars,
            [1.0] * len(vars)
        ]

    def rhs(self):
        return 1.0

    def sense(self):
        return 'G'
