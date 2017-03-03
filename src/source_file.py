class SourceFileSnapshot(object):
	"""
	Represents a source file at a given point in history.
	"""

	def __init__(self, file_path):
		self.file_path = file_path

	def __str__(self):
		return f'{self.file_path}'

	def __repr__(self):
		return str(self)