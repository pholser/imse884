from itertools import chain

class Formatter(object):
    def format(self, graph):
        return "\n".join(
            chain(
                [self.problem_line(
                    len(graph),
                    graph.number_of_edges()
                )],
                self.edge_lines(graph.edges())))

    def problem_line(self, number_of_nodes, number_of_edges):
        return 'p edge %d %d' % (number_of_nodes, number_of_edges)

    def edge_lines(self, edges):
        return [
            'e %d %d' % (e[0], e[1])
            for e in sorted(map(sorted, edges))
        ]
