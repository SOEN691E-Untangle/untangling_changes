"""Untangles commits from a Git repository."""

from git import Repo
import commit_splitter
import confidence_voters
import itertools
import argparse
import call_graph


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

    for change_pair in itertools.combinations(changes, 2):
    #     file_distance = confidence_voters.calculate_file_distance(*change_pair)
    #     if file_distance not in [0, 1]:
    #         # print(f'{change_pair[0]} vs {change_pair[1]}')
    #         # print(file_distance)
    #         pass

    #     package_distance = confidence_voters.calculate_package_distance(commit.tree, *change_pair)
        
    #     if package_distance not in [0, 1]:
    #         print(f'{change_pair[0].source_file_snapshot.file_path} vs {change_pair[1].source_file_snapshot.file_path}')
    #         print(package_distance)

    #     print(confidence_voters.calculate_call_graph_distance(static_call_graph, method_index, *change_pair))
    #     print(confidence_voters.calculate_co_change_frequency(repo, *change_pair))


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
