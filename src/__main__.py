from git import Repo
import pprint
import commit_splitter


if __name__ == '__main__':
	repo = Repo('..\\..\\git')

	head = repo.head.commit

	changes = commit_splitter.collect_changes(repo, head)

	pprint.pprint(changes)
