class DistinctRepresentativeForNeighborsConstraint(object):
    def __init__(self, problem, n, v, w):
        self.problem = problem
        self.n = n
        self.v = v
        self.w = w

    def name(self):
        return 'uqrep%d_%d,%d' % (self.n, self.v, self.w)

    def terms(self):
        vars = [
            self.problem.represents_color_class_of_var(self.n, self.v),
            self.problem.represents_color_class_of_var(self.n, self.w),
            self.problem.represents_color_class_of_var(self.n, self.n)
        ]
        return [
            vars,
            [1.0, 1.0, -1.0]
        ]

    def rhs(self):
        return 0.0

    def sense(self):
        return 'L'
