class Change(object):
	
	def __init__(self, operation, line, line_number, file_path):
		"""
		:param operation: The operation of this change.
		:type operation: str
		:param line: The contents of the line.
		:type line: str
		:param line_number: The line number of this change.
		:type line_number: int
		:param file_path: The path to the file containing this change.
		:type file_path: str
		"""

		self.operation = operation
		self.line = line
		self.line_number = line_number
		self.file_path = file_path

	def __str__(self):
		return f'({self.operation}, {self.line}, {self.line_number}, {self.file_path})'

	def __repr__(self):
		return str(self)


def collect_changes(commit):
	"""
	Collects all the individual line level changes of a commit.
	:param commit: The commit to breakdown.
	:type commit: git.objects.commit.Commit
	:returns: The individual line level changes.
	:rtype: list[Change]
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
					changes.append(Change('del', change[1:], old_line_number, d.a_path))
					old_line_number += 1
				elif change.startswith('+'):
					changes.append(Change('add', change[1:], new_line_number, d.b_path))
					new_line_number += 1
				elif change == '\\ No newline at end of file':
					continue
				else:
					old_line_number += 1
					new_line_number += 1

	return changes
