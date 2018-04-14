class UseLowerNumberedColorFirstConstraint(object):
    def __init__(self, format, k):
        self.format = format
        self.k = k

    def name(self):
        return 's2_%d' % self.k

    def terms(self):
        return [
            [self.format.color_used_var(self.k),
             self.format.color_used_var(self.k + 1)],
            [1.0, -1.0]
        ]

    def rhs(self):
        return 0.0

    def sense(self):
        return 'G'
