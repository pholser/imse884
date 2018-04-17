class CliqueCut(object):
    def __init__(self, problem, node, clique, id):
        self.problem = problem
        self.node = node
        self.clique = sorted(clique)
        self.id = id

    def name(self):
        return 'q%d' % self.id

    def terms(self):
        return [
            [self.problem.represents_color_class_of_var(self.node, v)
             for v in self.clique]
            + [self.problem.represents_color_class_of_var(self.node, self.node)],
            [1.0] * len(self.clique) + [-1.0]
        ]

    def rhs(self):
        return 0.0

    def sense(self):
        return 'L'

    def allows(self, solution):
        clique_rep_vars = [
            self.problem.represents_color_class_of_var(self.node, v)
            for v in self.clique
        ]
        own_rep_var = self.problem.represents_color_class_of_var(
            self.node,
            self.node
        )
        clique_rep_values = solution.value_of(clique_rep_vars)
        own_rep_value = solution.value_of(own_rep_var)
        return sum(clique_rep_values) - own_rep_value <= self.rhs()
