"""Untangles commits from a Git repository."""

from git import Repo
import commit_splitter
import confidence_voters
import itertools
import argparse
import git_tree


def main(repo_path, commit_hash):
    """
    :param repo_path: The path to the repository to mine.
    :type repo_path: str
    :param commit_hash: The commit hash of the commit to untangle.
    :type commit_hash: str
    """

    repo = Repo(args.repo_path)
    commit = repo.commit(commit_hash)

    changes = commit_splitter.collect_changes(repo, commit)

    diameter = git_tree.calculate_diameter(commit.tree)

    # for change_pair in itertools.combinations(changes, 2):
    #     file_distance = confidence_voters.calculate_file_distance(*change_pair)
    #     if file_distance not in [0, 1]:
    #         print(f'{change_pair[0]} vs {change_pair[1]}')
    #         print(f'{file_distance}')


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
