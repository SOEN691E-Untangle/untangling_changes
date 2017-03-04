class Change(object):
    """
    Represents a single line level change.
    """
    
    def __init__(self, operation, line, line_number, source_file_snapshot):
        """
        :param operation: The operation of this change.
        :type operation: str
        :param line: The contents of the line.
        :type line: str
        :param line_number: The line number of this change.
        :type line_number: int
        :param source_file_snapshot: Snapshot of the file at the time of this change.
        :type source_file_snapshot: source_file.SourceFileSnapshot
        """

        self.operation = operation
        self.line = line
        self.line_number = line_number
        self.source_file_snapshot = source_file_snapshot

    def __str__(self):
        return f'({self.operation}, {self.line}, {self.line_number}, {self.source_file_snapshot.file_path})'

    def __repr__(self):
        return str(self)
