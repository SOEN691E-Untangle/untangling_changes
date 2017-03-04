"""Functions for dealing with git file trees."""

from git.objects.tree import Tree
import itertools


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
