from change import Change

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

	pass