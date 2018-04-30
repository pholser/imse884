import networkx as nx

from format_error import FormatError
from graph_assertion_error import GraphAssertionError


class Parser(object):
    def parse(self, file_path):
        graph = nx.Graph()

        problem_line_seen = False
        line_number = 0
        expected_number_of_nodes = 0
        expected_number_of_edges = 0

        with open(file_path) as f:
            for line in f:
                line_number += 1
                if not line.strip():
                    continue     # skip blank lines

                pieces = line.split()
                indicator = pieces[0]
                if 'c' == indicator:
                    continue     # skip comment lines

                if len(pieces) < 2:
                    raise FormatError(
                        pieces,
                        line_number,
                        'Need at least two pieces on the line'
                    )
                args = pieces[1:]

                if 'p' == indicator:
                    if problem_line_seen:
                        raise FormatError(
                            pieces,
                            line_number,
                            'Already seen a problem line'
                        )
                    if len(args) != 3:
                        raise FormatError(
                            args,
                            line_number,
                            'Expecting "edge", |V|, |E|'
                        )
                    if args[0] != 'edge':
                        raise FormatError(
                            args,
                            line_number,
                            'Expecting "edge" indicator'
                        )

                    problem_line_seen = True
                    expected_number_of_nodes, expected_number_of_edges = \
                        int(args[1]), int(args[2])
                elif 'e' == indicator:
                    if not problem_line_seen:
                        raise FormatError(
                            pieces,
                            line_number,
                            'Edge line without preceding problem line'
                        )
                    if len(args) != 2:
                        raise FormatError(
                            args,
                            line_number,
                            'Expecting edge line with two endpoints'
                        )
                    graph.add_edge(int(args[0]), int(args[1]))

        if graph.number_of_nodes() != expected_number_of_nodes:
            min_node = min(graph.nodes()) if len(graph.nodes()) > 0 else 0
            node_range = set(range(min_node, min_node + expected_number_of_nodes))
            for n in node_range - set(graph.nodes()):
                graph.add_node(n)

            if graph.number_of_nodes() != expected_number_of_nodes:
                raise GraphAssertionError(
                    'Expected graph with %d nodes, got %d' % (
                        expected_number_of_nodes,
                        graph.number_of_nodes()
                    )
                )
        if graph.number_of_edges() != expected_number_of_edges \
                and graph.number_of_edges() != expected_number_of_edges / 2:
            raise GraphAssertionError(
                'Expected graph with %d edges, got %d' % (
                    expected_number_of_edges,
                    graph.number_of_edges()
                )
            )

        return graph
