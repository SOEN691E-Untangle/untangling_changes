from git import Repo
import pprint
import commit_splitter
import confidence_voters
import itertools


if __name__ == '__main__':
	repo = Repo('..\\..\\git')

	head = repo.head.commit

	changes = commit_splitter.collect_changes(repo, head)

	# pprint.pprint(changes)

	for change_pair in itertools.product(changes, repeat=2):
		file_distance = confidence_voters.calculate_file_distance(*change_pair)
		if file_distance not in [0, 1]:
			print(f'{change_pair[0]} vs {change_pair[1]}')
			print(f'{file_distance}')