class ColorUsedOnlyIfMarksNodeConstraint(object):
    def __init__(self, format, k):
        self.format = format
        self.k = k

    def name(self):
        return 's1_%d' % self.k

    def terms(self):
        return [
            [self.format.node_color_var(n, self.k) for n in self.format.nodes]
            + [self.format.color_used_var(self.k)],
            [1.0 for n in self.format.nodes] + [-1.0]
        ]

    def rhs(self):
        return 0.0

    def sense(self):
        return 'G'
