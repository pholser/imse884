class AdjacentNodeColorConstraint(object):
    def __init__(self, format, n1, n2, k):
        self.format = format
        self.n1 = n1
        self.n2 = n2
        self.k = k

    def name(self):
        return 'e%d,%d_%d' % (self.n1, self.n2, self.k)

    def terms(self):
        return [
            [self.format.node_color_var(self.n1, self.k),
             self.format.node_color_var(self.n2, self.k),
             self.format.color_used_var(self.k)
            ],
            [1.0, 1.0, -1.0]
        ]

    def rhs(self):
        return 0.0

    def sense(self):
        return 'L'
