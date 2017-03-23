import change

def merge(change_matrix, threshold):
    """
    Merges changes with values below the threshold.
    :param change_matrix: Matrix of changes with convidence voter values.
    :type change_matrix: dict[change.Change, dict[change.Change, double]]
    :param threshold: The threshold to discriminate whether a change pair should
    be merged or not.
    :type threshold: double
    :return: The updated change matrix.
    :rtype: dict[change.Change, dict[change.Change, double]]
    """

    while True:
        changes = []

        # SELECT 2 changes with a confidence value < threshold.
        for row in change_matrix.keys():
            for column, confidence_vote in change_matrix[row].items():
                if confidence_vote < threshold:
                    # collect the minimal votes.
                    changes = [row, column]
                    break

            if changes:
                break

        if not changes:
            # changes is empty and thus no acceptable changes were found.
            break

        # Find the minimal votes for all related cells.
        minimal_votes = {}

        for row in change_matrix.keys():
            for column, confidence_vote in change_matrix[row].items():
                if row in changes or column in changes:
                    old_vote = minimal_votes.get(column)

                    if not old_vote or confidence_vote < old_vote:
                        minimal_votes[column] = confidence_vote

        # Update Matrix
        # Remove rows and columns representing removed changes.
        change_matrix = {r: c for r,c in change_matrix.items() if r not in changes}

        for row in change_matrix.keys():
            change_matrix[row] = {c: cv for c, cv in change_matrix[row].items() if c not in changes}

        new_change = change.merge(changes[0], changes[1])

        # Fill in the new column. The corresponding row will be all empty (triangle matrix)
        if len(change_matrix.keys()) > 0:
            for row in change_matrix.keys():
                change_matrix[row][new_change] = minimal_votes[row]
        else:
            change_matrix[new_change] = {}
            change_matrix[new_change][new_change] = 0
            break

    return change_matrix
