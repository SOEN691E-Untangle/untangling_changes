"""Functions for dealing with git file trees."""

from git.objects.tree import Tree
import itertools
from source_file import SourceFileSnapshot


def find_lowest_common_ancestor_node(path_to_a, path_to_b):
    """
    Finds the lowed common ancestor node.
    :param path_to_a: The path to node a from root.
    :type path_to_a: list[git.objects.blob.Blob]
    :param path_to_b: The path to node b from root.
    :type path_to_b: list[git.object.blob.Blob]
    """

    for a in reversed(path_to_a):
        for b in reversed(path_to_b):
            if a == b:
                return a


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
    
    path_to_a = find_path_from_root(tree, file_a.sha)
    path_to_b = find_path_from_root(tree, file_b.sha)

    lowest_common_ancestor = find_lowest_common_ancestor_node(path_to_a, path_to_b)

    path_to_lca = find_path_from_root(tree, lowest_common_ancestor.hexsha)

    return calculate_path_length(path_to_a) + calculate_path_length(path_to_b) - 2 * calculate_path_length(path_to_lca)


def find_path_from_root(tree, file_sha, path=[]):
    """
    Determines the path from the root to the file.
    :param tree: The tree to look in.
    :type tree: git.objects.tree.Tree
    :param file_sha: The sha of the file to look for.
    :type file_sha: str
    :param path: The path from the root to the file.
    :type path: list[git.objects.blob.Blob]
    """

    if tree.hexsha == file_sha:
        return path + [tree]
    elif type(tree) == Tree:
        # if all are none, the node isn't in the tree.
        # otherwise, there should be only one non-none value.
        for st in tree:
            potential_path = find_path_from_root(st, file_sha, path + [tree])
            
            if potential_path:
                path = potential_path
                return path
    else:
        return []


def calculate_path_length(path):
    """
    Calculates the length of a path.
    :param path: The path to calculate the length of.
    :type path: list[git.objects.blob.Blob]
    :rtype: int
    """

    return len(path) - 1


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
