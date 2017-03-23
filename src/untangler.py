"""Untangles commits from a Git repository."""

from git import Repo
import commit_splitter
import confidence_voters
import itertools
import argparse
import call_graph
import os
import merger


def main(repo_path, commit_hash):
    """
    :param repo_path: The path to the repository to mine.
    :type repo_path: str
    :param commit_hash: The commit hash of the commit to untangle.
    :type commit_hash: str
    """

    repo = Repo(args.repo_path)
    git = repo.git

    commit = repo.commit(commit_hash)

    changes = commit_splitter.collect_changes(repo, commit, repo_path)

    static_call_graph = call_graph.generate_call_graph(git, commit_hash, args.repo_path)

    method_index = call_graph.generate_method_index(args.repo_path)

    change_matrix = {}

    for change_pair in itertools.combinations(changes, 2):
        # 0 means changes are close, 1 means they are far
        file_distance = confidence_voters.calculate_file_distance(*change_pair)
        package_distance = confidence_voters.calculate_package_distance(commit.tree, *change_pair)
        call_graph_distance = confidence_voters.calculate_call_graph_distance(static_call_graph, method_index, *change_pair)
        co_change_frequency = confidence_voters.calculate_co_change_frequency(repo, *change_pair)

        voters = [file_distance, package_distance, call_graph_distance, co_change_frequency]
        voters = [v for v in voters if v >= 0 and v <= 1]

        sum = 0

        for v in voters:
            sum += v

        score = sum / len(voters)

        if not change_matrix.get(change_pair[0]):
            change_matrix[change_pair[0]] = {}

        change_matrix[change_pair[0]][change_pair[1]] = score


    final_matrix = merger.merge(change_matrix, 0.4)

    for change in final_matrix.keys():
        print(str(change))
 
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Untangles commits from a Git repository.'
    )

    parser.add_argument(
        'repo_path',
        help='The path to the repository to mine.'
    )

    parser.add_argument(
        'commit_hash',
        help='The commit hash of the commit to untangle.'
    )

    args = parser.parse_args()

    main(args.repo_path, args.commit_hash)
