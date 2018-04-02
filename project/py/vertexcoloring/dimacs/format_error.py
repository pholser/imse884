class FormatError(Exception):
    def __init__(self, input, line_number, message):
        self.input = input
        self.line_number = line_number
        self.message = message

    def __str__(self):
        return "Format error at line %d on input '%s': %s" % (
            self.line_number,
            self.input,
            self.message
        )
