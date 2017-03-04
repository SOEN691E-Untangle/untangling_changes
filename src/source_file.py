class SourceFileSnapshot(object):
	"""
	Represents a source file at a given point in history.
	"""

	# Calculating the file length is expensive. We don't want to
	# repeat it over and over for the same files.
	file_length_cache = {}


	def __init__(self, file_path, repo, commit):
		"""
		:param file_path: The path to the source file.
		:type file_path: str
		:param repo: The repository the file belongs to.
		:type repo: git.Repo
		:param commit: The commit for this snapshot.
		:type commit: git.objects.commit.Commit
		"""

		self._repo = repo
		self._commit = commit

		self.file_path = file_path

		# This gets the length of the file at point in time of the commit.
		file_length_key = f'{commit}:{file_path}'
		length = self.file_length_cache.get(file_length_key)

		if not length:
			length = len(repo.git.show(file_length_key).split('\n'))
			self.file_length_cache[file_length_key] = length

		self.line_length = length

	def __str__(self):
		return f'{self.file_path}'

	def __repr__(self):
		return str(self)
