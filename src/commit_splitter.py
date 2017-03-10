"""Splits a commit into individual line level changes."""

from change import Change
from source_file import SourceFileSnapshot


def collect_changes(repo, commit, repo_path):
    """
    Collects all the individual line level changes of a commit.

    The strategy used here is to generate a patch for the diff
    between the chosen commit and all of its parents.
    The diff is then parsed to find the line number of each change.

    This post is helpful for understanding unified diffs for
    extracting line numbers of changes:
    http://stackoverflow.com/questions/24455377/git-diff-with-line-numbers-git-log-with-line-numbers

    :param repo: The repository being mined.
    :type repo: git.Repo
    :param commit: The commit to breakdown.
    :type commit: git.objects.commit.Commit
    :param repo_path: The path to the repository root.
    :type repo_path: str
    :returns: The individual line level changes.
    :rtype: list[change.Change]
    """

    changes = []

    for parent in commit.parents:
        for d in parent.diff(commit, create_patch=True):
            diff = d.diff.decode('utf-8')

            for change in diff.split('\n'):
                if change.startswith('@@'):
                    info = [x for x in change.split() if x != '@@']
                    # Parse the beginning line numbers of the unified diff.
                    old_line_number = int(info[0][1:].split(',')[0])
                    new_line_number = int(info[1][1:].split(',')[0])
                elif change.startswith('-'):
                    changes.append(Change('del', change[1:], old_line_number, SourceFileSnapshot(d.a_path, repo, commit, repo_path)))
                    old_line_number += 1
                elif change.startswith('+'):
                    changes.append(Change('add', change[1:], new_line_number, SourceFileSnapshot(d.b_path, repo, commit, repo_path)))
                    new_line_number += 1
                elif change == '\\ No newline at end of file':
                    continue
                else:
                    old_line_number += 1
                    new_line_number += 1

    return changes
