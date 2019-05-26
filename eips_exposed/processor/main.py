import sys
import time
from typing import List
from pathlib import Path

from eips_exposed.common import CONFIG, getLogger
from eips_exposed.common.db import (
    get_session,
    get_latest_commit,
    EIP as DBEIP,
    Commit as DBCommit,
)
from eips_exposed.common.exceptions import EIPParseError
from eips_exposed.processor import parse_eip
from eips_exposed.processor.git import latest_commit_hash, get_eip_repo, all_commits, file_history
from eips_exposed.processor.objects import EIP

log = getLogger(__name__)

PROCESS_WAIT = 10
IGNORE_FILES = ['eip-20-token-standard.md']
IGNORE_EIP_ATTRS = ['raw']
IGNORE_EIP_ATTR_TYPES = ["<class 'function'>", "<class 'method'>"]


def list_eip_files() -> List[Path]:
    """ Return a list of the available EIPs files """
    if not CONFIG['EIPS_DIR'].is_dir():
        raise FileNotFoundError('Expected local EIPs repo missing!')
    return [f for f in CONFIG['EIPS_DIR'].iterdir() if f.is_file()]


def get_public_attrs(obj) -> List[str]:
    public_attrs = set()

    for attr in dir(obj):

        if not attr.startswith('_') \
          and attr not in IGNORE_EIP_ATTRS \
          and str(type(getattr(obj, attr))) not in IGNORE_EIP_ATTR_TYPES:

            public_attrs.add(attr)

    return public_attrs


def create_eip_model_instance(eip: EIP) -> DBEIP:
    """ Create a model instance from an EIP object """
    kwargs = {k: getattr(eip, k) for k in get_public_attrs(eip)}
    return DBEIP(**kwargs)


def process() -> None:
    """ Run through all commits and EIPs and add them to the DB """

    commit_count = 0
    eip_count = 0
    eip_error_count = 0
    eip_skipped_count = 0
    repo = get_eip_repo()
    db_session = get_session()

    if repo.bare:
        log.error('EIP Repo clone failure')
        sys.exit(1)

    # Check and make sure we actually need to update
    latest_commit = latest_commit_hash()
    latest_db_commit = get_latest_commit()

    if latest_db_commit and latest_commit == latest_db_commit.commit_hash:
        log.info('Up to date!  Commit: {}'.format(latest_commit[:7]))
        return

    commits = all_commits()
    db_commits = {}

    for commit in commits:

        commit_count += 1

        commit_inst = DBCommit(
            commit_hash=commit.hexsha,
            committer=commit.committer.name,
            committed_date=commit.committed_datetime,
            message=commit.message
        )

        log.debug('Adding commit {}'.format(commit.hexsha))

        db_commit = db_session.merge(commit_inst)
        db_commits[db_commit.commit_hash] = db_commit

    eip_files = list_eip_files()

    for fil in eip_files:

        if fil.name in IGNORE_FILES:
            eip_skipped_count += 1
            continue

        eip: EIP

        log.info('Processing EIP file {}...'.format(fil))

        try:
            eip = parse_eip(fil.read_text())
        except EIPParseError:
            log.exception('Parsing of EIP file failed ({})'.format(fil))
            eip_error_count += 1
        else:
            log.info('Successfully parsed EIP {}'.format(eip))
            eip_count += 1

            # Upsert into the DB
            eip_db_obj = create_eip_model_instance(eip)

            history = file_history(fil)

            for comm_hash in history:
                eip_db_obj.commits.append(db_commits[comm_hash])

            db_session.merge(eip_db_obj)

    log.debug('Comitting changes to database...')
    db_session.commit()

    log.debug('Total EIP Files: {}'.format(len(eip_files)))
    log.debug('Skipped {} EIP files'.format(eip_skipped_count))
    log.info('Successfully parsed {} EIPs'.format(eip_count))
    log.warning('Failed parsing {} EIPs'.format(eip_error_count))


def main() -> None:
    """ Kick of the process of processing EIPs into the DB """

    try:
        while True:
            process()
            time.sleep(PROCESS_WAIT)
    except KeyboardInterrupt:
        log.warning('Process interrupted by user')
        sys.exit(0)
