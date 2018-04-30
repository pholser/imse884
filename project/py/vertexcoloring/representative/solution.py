from ..is_close import isclose
from ..vertex_coloring_solution import VertexColoringSolution


class Solution(VertexColoringSolution):
    def __init__(self, problem, cplex_solution, running_time):
        super(Solution, self).__init__(problem, cplex_solution, running_time)

        self.problem = problem
        self.cplex_solution = cplex_solution
        self.running_time = running_time

    def used_colors(self):
        represents_own_color_class_vars = \
            self.problem.represents_own_color_class_vars()

        return map(
            self.problem.color_class_for_representative_var,
            {
                k for k, v in filter(
                    lambda e:
                        e[0] in represents_own_color_class_vars
                        and isclose(e[1], 1.0),
                    self.values().iteritems()
                )
            }
        )

    def colors_by_node(self):
        color_classes = self.used_colors()

        representative_vars = {
            k for k, v in filter(
                lambda e:
                    self.problem.color_class_for_representative_var(e[0]) in color_classes
                    and isclose(e[1], 1.0),
                self.values().iteritems()
            )
        }
        return dict(
            map(
                self.problem.representative_pairing_for_var,
                representative_vars
            )
        )
