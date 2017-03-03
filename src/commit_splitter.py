from change import Change
from source_file import SourceFileSnapshot


def collect_changes(repo, commit):
	"""
	Collects all the individual line level changes of a commit.
	:param repo: The repository being mined.
	:type repo: git.Repo
	:param commit: The commit to breakdown.
	:type commit: git.objects.commit.Commit
	:returns: The individual line level changes.
	:rtype: list[change.Change]
	"""

	changes = []

	"""
	What's going on here is that I am iterating
	through the differences with all parents to the current
	commit.

	I am then parsing the diff. by using the header,
	I can determine line number info. - means a side, + means
	b side. a is old, b is new.
	I am collecting the op type, add/delete, the line number
	and the file path.
	"""

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
					changes.append(Change('del', change[1:], old_line_number, SourceFileSnapshot(d.a_path, repo, commit)))
					old_line_number += 1
				elif change.startswith('+'):
					changes.append(Change('add', change[1:], new_line_number, SourceFileSnapshot(d.b_path, repo, commit)))
					new_line_number += 1
				elif change == '\\ No newline at end of file':
					continue
				else:
					old_line_number += 1
					new_line_number += 1

	return changes
