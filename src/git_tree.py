"""Functions for dealing with git file trees."""

from git.objects.tree import Tree
import itertools
from source_file import SourceFileSnapshot


def calculate_distance(tree, file_a, file_b):
    """
    Calculates the shortest path between two files in the file
    tree.

    The implememented algorithm calculates the sum of the distances
    from the root to each file minus 2 times the distance from the
    root to the lowest common ancestor node.

    :param tree: The tree containing the files.
    :type tree: git.objects.tree.Tree
    :param file_a: The first file to compare.
    :type file_a: source_file.SourceFileSnapshot
    :param file_b: The second file to compare.
    :type file_b: source_file.SourceFileSnapshot
    :rtype: int
    """
    
    # Dist(x, y) = Dist(root, x) + Dist(root, y) - 2*Dist(root, lowest common ancestor)
    pass


def find_level_of_file(tree, file, current_level=0):
    """
    Finds the level of the file in the file tree.
    :param tree: The tree to look in.
    :type tree: git.objects.tree.Tree
    :param file: The file to look for.
    :type file: source_file.SourceFileSnapshot
    :param current_level: The current level of traversal. If the node is not found, None is returned.
    :type current_level: int
    """

    if tree.hexsha == file.sha:
        return current_level
    elif type(tree) == Tree:
        # if all are none, the node isn't in the tree.
        # otherwise, there should be only one non-none value.
        search_results = [find_level_of_file(st, file, current_level + 1) for st in tree]
        return [r for r in search_results if r][0] if any(search_results) else None
    else:
        return None


def calculate_diameter(tree):
    """
    Calculates the diameter of the tree.
    The diameter is defined as the maximal length between two nodes.

    :param tree: The tree to measure.
    :type tree: git.objects.tree.Tree
    :rtype: int
    """

    if type(tree) is Tree:
        subtree_heights = [calculate_height(st) for st in tree]
        subtree_diameters = [calculate_diameter(st) for st in tree]

        if len(subtree_heights) > 1:
            largest_height_pair = max([h1 + h2 for h1, h2 in itertools.combinations(subtree_heights, 2)])
        else:
            largest_height_pair = subtree_heights[0]

        return max([largest_height_pair + 1] + subtree_diameters)  
    else:
        return 0


def calculate_height(tree):
    """
    Calculates the height of the tree.

    :param tree: The tree to measure.
    :type tree: git.objects.tree.Tree
    :rtype: int
    """

    if type(tree) is Tree:
        subtree_heights = [calculate_height(st) for st in tree]
        
        return 1 + max(subtree_heights)
    else:
        return 0
