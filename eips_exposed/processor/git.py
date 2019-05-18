import time
from typing import Optional, List
from pathlib import Path
from git import Repo
from git.objects.commit import Commit
from eips_exposed.common import CONFIG, getLogger

eip_git_repo: Optional[Repo] = None
log = getLogger(__name__)


def get_eip_repo() -> Repo:
    """ Return an intiialized git Repo instnace """
    global eip_git_repo

    if eip_git_repo is not None:
        return eip_git_repo

    repo_dir = CONFIG.get('EIPS_LOCAL_REPO')

    if repo_dir and repo_dir.is_dir():
        eip_git_repo = Repo(repo_dir)
    else:
        eip_git_repo = clone_eip_repo(repo_dir)

    return eip_git_repo


def clone_eip_repo(repo_dir: Path) -> Repo:
    """ Clone the repo if necessary """
    origin = None
    repo = None

    if not repo_dir.is_dir():
        repo = Repo.clone_from(CONFIG.get('EIPS_REMOTE_REPO'), repo_dir)

    if not repo:
        repo = get_eip_repo()

    if repo.bare:
        origin = repo.create_remote('origin', url=CONFIG.get('EIPS_REMOTE_REPO'))
        assert origin.exists(), 'Ethereum EIPs repo missing?  WTF'
        for fetch_info in origin.fetch():
            log.info("Updated %s to %s" % (fetch_info.ref, fetch_info.commit))
        master = repo.create_head('master', origin.refs.master)
        repo.head.set_reference(master)
    else:
        origin = repo.remote()
        for fetch_info in origin.fetch():
            log.info("Updated %s to %s" % (fetch_info.ref, fetch_info.commit))

    return repo


def latest_commit_hash() -> str:
    """ Get the latest commit hash for a repo """
    repo = get_eip_repo()
    return repo.refs.master.commit.hexsha


def file_history(fil: Path) -> List[str]:
    """ Get the Git history for a file """
    repo = get_eip_repo()
    commits = []
    for commit in repo.iter_commits('--all', paths=fil):
        commits.append(commit.hexsha)
    return commits


def all_commits() -> List[Commit]:
    repo = get_eip_repo()
    commits = []
    for commit in repo.iter_commits('--all'):
        commits.append(commit)
    return commits
