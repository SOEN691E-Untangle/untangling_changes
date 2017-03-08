import subprocess
import tempfile
import os
import understand


def _generate_understand_db(git, commit_hash, repo_path):
    """
    Generates the database file for Understand.
    :param git: Reference to the git api access.
    :param commit_hash: The hash of the commit to generate
    a call graph for.
    :type commit_hash: str
    :param repo_path: The path of the repository on the file system.
    :type repo_path: str
    :returns: The path to the understand db.
    :rtype: str
    """

    # Checkout the files for the commit.
    git.checkout(commit_hash)
    
    db_path = os.path.join(tempfile.gettempdir(), f'{commit_hash}.udb')

    # TODO: Handle the case where understand is not installed,
    # repo is missing, or we can't write to db_path
    subprocess.run([
        'und',
        'create',
        '-languages',
        'java',
        'add',
        repo_path,
        'analyze',
        '-all',
        db_path
    ], stdout=subprocess.DEVNULL)

    # Restore the repo to HEAD.
    git.checkout('HEAD')

    return db_path


def generate_call_graph(git, commit_hash, repo_path):
    """
    Generates a static call graph.
    :param git: Reference to the git api access.
    :param commit_hash: The hash of the commit to generate
    a call graph for.
    :type commit_hash: str
    :param repo_path: The path of the repository on the file system.
    :type repo_path: str
    :returns: The call graph at this commit. This is represented
    as a dictionary of methods in the full canonical form mapped
    to a list of methods called by that method in the same format.
    :rtype: dict[str, list[str]]
    """

    call_graph = {}
    udb_path = _generate_understand_db(git, commit_hash, repo_path)

    db = understand.open(udb_path)

    # Generate a mapping of method names in the form
    # CLASS.METHOD_NAME to a list of methods that it calls.
    for fn in db.ents('function, method, procedure'):                                         
        function_name = fn.longname()
        call_graph[function_name] = [called_fn.ent().longname() for called_fn in fn.refs('Java Call')]

    db.close()

    # Clean up the temp file when done with it.
    os.remove(udb_path)

    return call_graph
