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
        output = '********\n'
        output += f'({self.operation}, {self.source_file_snapshot.file_path}, {self.line_number})\n'
        output += '********\n'

        return output


class CompoundChange(object):
    """
    Represents a compound change (multiple lines).
    """

    def __init__(self, *changes_to_merge):
        """
        :param changes_to_merge: The changes to merge.
        """

        self.changes = []

        for change in changes_to_merge:
            if type(change) == Change:
                self.changes.append(change)
            elif type(change) == CompoundChange:
                self.changes += change.changes

    def __str__(self):
        output = '+++++++\n'

        for change in self.changes:
            output += f'{change}\n'

        output += '+++++++++++\n'

        return output


def merge(change_1, change_2):
    """
    Merges two changes.
    :param change_1: The first change.
    :type change_1: Change
    :param change_2: The other change.
    :type change_2: Change
    :returns: The merged change.
    :rtype: CompoundChange
    """

    return CompoundChange(change_1, change_2)