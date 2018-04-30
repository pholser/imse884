from ..is_close import isclose
from ..vertex_coloring_solution import VertexColoringSolution


class Solution(VertexColoringSolution):
    def __init__(self, problem, cplex_solution, running_time):
        super(Solution, self).__init__(problem, cplex_solution, running_time)

        self.problem = problem
        self.cplex_solution = cplex_solution
        self.running_time = running_time

    def used_colors(self):
        return sorted(
            map(
                self.problem.color_for_used_var,
                {
                    k for k, v in filter(
                        lambda e:
                            e[0] in self.problem.color_used_vars()
                            and isclose(e[1], 1.0),
                        self.values().iteritems()
                    )
                }
            )
        )

    def colors_by_node(self):
        all_node_color_vars = set(self.problem.all_node_color_vars())

        node_color_vars = {
            k for k, v in filter(
                lambda e:
                    e[0] in all_node_color_vars
                    and isclose(e[1], 1.0),
                self.values().iteritems()
            )
        }
        return dict(
            map(
                self.problem.node_color_pairing_for_var,
                node_color_vars
            )
        )
