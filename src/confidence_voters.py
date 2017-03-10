"""Algorithms to calculate confidence voters"""

from change import Change
import math
import git_tree
import os
from collections import deque


diameter_cache = {}
co_change_cache = {}


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


def _bfs(src, target, graph):
    """
    Calculates the shortest path from src to target using BFS.
    :param src: The source node.
    :type src: str
    :param target: The target node.
    :type target: str
    :param graph: The graph to search.
    :type graph: dict[str, list[str]]
    :returns: The shortest path between the two nodes.
    :rtype: int
    """

    curr = src
    queue = deque()
    distances = {src: 0}

    if src == target:
        return 0

    while queue:
        for neighbour in graph[curr]:
            if neighbour not in distances:
                distances[neighbour] = distances[curr] + 1

                if neighbour == target:
                    return distances[neighbour]
                else:
                    queue.append(neighbour)

    # There is no path between the two nodes.
    return -1


def calculate_call_graph_distance(static_call_graph, method_index, change_a, change_b):
    """
    Calcualates the distance between two changes in the call graph.
    This value is defined as 1 divided by the number of edges between the two nodes.
    :param static_call_graph: The static call graph to traverse.
    :type static_call_graph: dict[str, list[str]]
    :param method_index: An index of all the methods and line numbers they occupy.
    :type method_index: dict[str, dict[str, str | int]]
    :param change_a: The first change to consider.
    :type change_a: change.Change
    :param change_b: The second change to consider.
    :type change_b: change.Change
    """

    ln_a = change_a.line_number
    ln_b = change_b.line_number

    method_a = None
    method_b = None

    for line_range, method_name in method_index[change_a.source_file_snapshot.file_path].items():
        lines = [int(l) for l in line_range.split('-')]

        if ln_a >= lines[0] and ln_a <= lines[1]:
            method_a = method_name
            break

    for line_range, method_name in method_index[change_b.source_file_snapshot.file_path].items():
        lines = [int(l) for l in line_range.split('-')]

        if ln_b >= lines[0] and ln_b <= lines[1]:
            method_b = method_name
            break

    if not method_a or not method_b:
        # This means that one of the changes isn't in a method.
        return -1

    # Now we have the keys in the static call graph, we can now look for the distance.
    return _bfs(method_a, method_b, static_call_graph)


def calculate_co_change_frequency(repo, change_a, change_b):
    """
    Calculates the frequency at which two files are changed together.
    :param repo: The repository.
    :type repo: git.Repo
    :param change_a: The first change to consider.
    :type change_a: change.Change
    :param change_b: The second change to consider.
    :type change_b: change.Change
    """

    git = repo.git
    file_a = change_a.source_file_snapshot.file_path
    file_b = change_b.source_file_snapshot.file_path

    key = frozenset([file_a, file_b])

    if key not in co_change_cache:
        file_a_commits = set([repo.commit(x.split()[0]) for x in git.log('--oneline', '--follow', file_a).split('\n')])
        file_b_commits = set([repo.commit(x.split()[0]) for x in git.log('--oneline', '--follow', file_b).split('\n')])

        all_commits = file_a_commits.union(file_b_commits)
        common_commits = file_a_commits.intersection(file_b_commits)

        co_change_frequency = float(len(common_commits)) / float(len(all_commits))

        co_change_cache[key] = co_change_frequency
    else:
        co_change_frequency = co_change_cache[key]

    return co_change_frequency
