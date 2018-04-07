class ColorAssignment(object):
    def __init__(self, graph):
        self.graph = graph

    def format_as_lpsolve(self):
        lines = []

        nodes = sorted(self.graph.nodes)
        colors = nodes

        lines.append('Minimize')
        lines.append(
            'colors_used: '
            + ' + '.join(['w' + k for k in colors]))

        lines.append('Subject To')
        for n in nodes:
            lines.append(
                'n' + n + ': '
                + ' + '.join(['x' + n + ',' + k for k in colors])
                + ' = 1')
        for e in sorted(map(sorted, self.graph.edges())):
            for k in colors:
                lines.append(
                    'e' + e[0] + ',' + e[1] + '_' + k + ': '
                    + 'x' + e[0] + ',' + k
                    + ' + '
                    + 'x' + e[1] + ',' + k
                    + ' - w' + k
                    + ' <= 0'
                )
        lines.append('Binary')
        for n in nodes:
            lines.append(
                ' '.join(['x' + n + ',' + k for k in colors])
            )
        lines.append(' '.join(['w' + k for k in colors]))

        lines.append('End')

        return "\n".join(lines)
