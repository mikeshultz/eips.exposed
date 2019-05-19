from typing import Optional, List
from enum import Enum
from datetime import datetime
from git.objects.commit import Commit

from eips_exposed.common import EIPParseError, getLogger, list_of_int_or_none, datetime_or_none
from eips_exposed.processor.parser import pluck_headers

log = getLogger(__name__)


class EIPStatus(Enum):
    DRAFT = 'Draft'
    LAST_CALL = 'Last Call'
    ACCEPTED = 'Accepted'
    FINAL = 'Final'
    ACTIVE = 'Active'
    DEFERRED = 'Deferred'
    REJECTED = 'Rejected'
    SUPERSEDED = 'Superseded'

    @classmethod
    def get_by_val(cls, v):
        if not v:
            return None
        for attr in list(cls):
            str_attr = str(attr).split('.')[1]
            attr_v = getattr(cls, str_attr).value
            if attr_v == v or v in attr_v:
                return cls[str_attr]
        return None


class EIPType(Enum):
    STANDARDS = 'Standards Track (Core, Networking, Interface, ERC)'
    INFORMATIONAL = 'Informational'
    META = 'Meta'

    @classmethod
    def get_by_val(cls, v):
        if not v:
            return None
        for attr in list(cls):
            str_attr = str(attr).split('.')[1]
            attr_v = getattr(cls, str_attr).value
            if attr_v == v or v in attr_v:
                return cls[str_attr]
        return None


class EIPCategory(Enum):
    CORE = 'Core'
    NETWORKING = 'Networking'
    INTERFACE = 'Interface'
    ERC = 'ERC'

    @classmethod
    def get_by_val(cls, v):
        if not v:
            return None
        for attr in list(cls):
            str_attr = str(attr).split('.')[1]
            attr_v = getattr(cls, str_attr).value
            if attr_v == v or v in attr_v:
                return cls[str_attr]
        return None


class EIPCommit:
    """ Represents a commit on an EIP file """

    def __init__(self, commit: Commit):
        self.parse_git_commit(commit)

    def __repr__(self):
        return '<EIPCommit (hash={})>'.format(self.hash)

    def __str__(self):
        return '{} by {} on {}'.format(self.short_hash, self.committer, self.date)

    def parse_git_commit(self, commit: Commit):
        """ Process a GitPython Commit object """
        self.hash: str = commit.hexsha
        self.short_hash: str = commit.hexsha[:8]
        self.committer: str = commit.committer.name
        self.date: datetime = commit.committed_datetime
        self.message: str = commit.message


class EIP:
    """ An object representation of an EIP """

    def __init__(self, raw):
        self.raw: str = raw
        headers, body = pluck_headers(raw)
        self.parse_headers(headers)
        self.full_text: str = body

    def __repr__(self):
        return '<EIP (eip={})>'.format(self.eip_id)

    def parse_headers(self, headers):
        try:
            self.eip_id: int = int(headers['eip'])
            self.eip_type: EIPType = EIPType.get_by_val(headers['type'])
            self.title: str = headers['title']
            self.author: str = headers['author']
            self.status: EIPStatus = EIPStatus.get_by_val(headers['status'])
            self.created: datetime = datetime_or_none(headers['created'])

            # Check the get_by_val attrs since they could return None
            assert self.eip_type is not None, 'Failed to resolve type: {}'.format(headers['type'])
            assert self.status is not None, 'Failed to resolve status: {}'.format(headers['status'])
            assert self.created is not None, 'Failed to resolve created: {}'.format(
                headers['created']
            )
        except (KeyError, AssertionError) as err:
            log.debug(headers)
            raise EIPParseError('EIP missing header {}'.format(err))

        self.updated: Optional[str] = headers.get('updated')
        self.discussions_to: Optional[str] = headers.get('discussions-to')
        self.review_period_end: Optional[str] = headers.get('review-period-end')
        self.category: Optional[EIPCategory] = EIPCategory.get_by_val(headers.get('category'))
        self.requires: Optional[List[int]] = list_of_int_or_none(headers.get('requires'))
        self.replaces: Optional[List[int]] = list_of_int_or_none(headers.get('replaces'))
        self.superseded_by: Optional[List[int]] = list_of_int_or_none(headers.get('superseded-by'))
        self.resolution: Optional[str] = headers.get('resolution')
