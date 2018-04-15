class NodeGettingColorConstraint(object):
    def __init__(self, format, n):
        self.format = format
        self.n = n

    def name(self):
        return 'n%d' % self.n

    def terms(self):
        return [
            [self.format.node_color_var(self.n, k) for k in self.format.colors],
            [1.0] * len(self.format.colors)
        ]

    def rhs(self):
        return 1.0

    def sense(self):
        return 'E'
