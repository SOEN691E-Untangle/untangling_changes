"""Algorithms to calculate confidence voters"""

from change import Change
import math
import git_tree

diameter_cache = {}


def calculate_file_distance(change_a, change_b):
    """
    Calculates the file distance between two changes.
    The file distance is defined as the number of lines
    between the two change operations, divided by the length
    of the source file in lines at the time of this change.

    If the two changes are not in the same file, the file
    distance will be the maximum value, 1.

    :param change_a: The first change to consider.
    :type change_a: change.Change
    :param change_b: The second change to consider.
    :type change_b: change.Change
    """

    if change_a.source_file_snapshot.file_path == change_b.source_file_snapshot.file_path:
        return math.fabs(change_a.line_number - change_b.line_number) / change_a.source_file_snapshot.line_length
    else:
        return 1


def calculate_package_distance(tree, change_a, change_b):
    """
    Calculates the package distance between two changes.
    The package distance is defined as the distance in the
    package tree between the location of the two changes divided
    by the largest possible distance in the package tree, that is
    the diameter of the tree at the time of this change.

    If the two changes are in the same file, the file
    distance will be the minimum value, 0.

    :param tree: The file tree.
    :type tree: git.objects.tree.Tree
    :param change_a: The first change to consider.
    :type change_a: change.Change
    :param change_b: The second change to consider.
    :type change_b: change.Change
    """

    if change_a.source_file_snapshot.file_path == change_b.source_file_snapshot.file_path:
        return 0
    else:
        diameter = diameter_cache.get(tree)

        if not diameter:
            # Cache the diameter so we don't recalculate each time.
            diameter = git_tree.calculate_diameter(tree)
            diameter_cache[tree] = diameter

        distance = git_tree.calculate_distance(tree, change_a.source_file_snapshot, change_b.source_file_snapshot)

        return float(distance) / float(diameter)
