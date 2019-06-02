from contextlib import contextmanager
from datetime import datetime
from sqlalchemy import (
    create_engine,
    func,
    distinct,
    text,
    Table,
    ForeignKey,
    Index,
    Column,
    Integer,
    String,
    Enum,
    DateTime,
    Text,
    Boolean,
)
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy_utils.types.ts_vector import TSVectorType
from eips_exposed.common import CONFIG, getLogger
from eips_exposed.processor.objects import EIPType, EIPStatus, EIPCategory, ErrorType

log = getLogger(__name__)

Base = declarative_base()
engine = create_engine(CONFIG['EIPS_DB_URL'], echo=True)
Session = sessionmaker(bind=engine)


EIPCommit = Table(
    'eip_commit',
    Base.metadata,
    Column('eip_commit_id', Integer, primary_key=True),
    Column('commit_hash', Integer, ForeignKey('commit.commit_hash'), nullable=False),
    Column('eip_id', Integer, ForeignKey('eip.eip_id'), nullable=False),
)


EIPTag = Table(
    'eip_tag',
    Base.metadata,
    Column('eip_tag_id', Integer, primary_key=True),
    Column('tag_name', String, ForeignKey('tag.tag_name'), nullable=False),
    Column('eip_id', Integer, ForeignKey('eip.eip_id'), nullable=False),
)


class EIP(Base):
    __tablename__ = 'eip'

    eip_id = Column(Integer, primary_key=True)

    eip_type = Column(Enum(EIPType), nullable=False)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    status = Column(Enum(EIPStatus), nullable=False)
    created = Column(DateTime, nullable=False)

    updated = Column(String)
    discussions_to = Column(String)
    review_period_end = Column(String)
    category = Column(Enum(EIPCategory))
    requires = Column(ARRAY(Integer))
    replaces = Column(ARRAY(Integer))
    superseded_by = Column(ARRAY(Integer))
    resolution = Column(String)

    full_text = Column(Text)

    search_vector = Column(TSVectorType)

    commits = relationship('Commit', secondary=EIPCommit)
    tags = relationship('Tag', secondary=EIPTag)

    def __repr__(self):
        return '<EIP (eip_id={})>'.format(self.eip_id)

    @classmethod
    def search(cls, session, terms):
        return session.query(cls).filter(cls.search_vector.match(terms))


class Commit(Base):
    __tablename__ = 'commit'

    commit_hash = Column(String(40), primary_key=True)
    committer = Column(String(), nullable=False)
    author = Column(String(), nullable=False)
    committed_date = Column(DateTime(), nullable=False)
    message = Column(Text())

    search_vector = Column(TSVectorType)

    eips = relationship('EIP', secondary=EIPCommit)

    def __repr__(self):
        return '<Commit (commit_hash={})>'.format(self.commit_hash)

    @classmethod
    def search(cls, session, terms):
        return session.query(cls).filter(cls.search_vector.match(terms))


class Tag(Base):
    __tablename__ = 'tag'

    tag_name = Column(String(), primary_key=True)
    active = Column(Boolean(), default=False, nullable=False)

    eips = relationship('EIP', secondary=EIPTag)

    def __repr__(self):
        return '<Tag (tag_name={})>'.format(self.tag_name)

    def __str__(self):
        return self.tag_name


class Error(Base):
    __tablename__ = 'error'

    eip_id = Column('eip_id', Integer, ForeignKey('eip.eip_id'), primary_key=True)
    error_type = Column(Enum(ErrorType), nullable=False)
    when = Column(DateTime, server_default=func.current_timestamp())
    message = Column(String)

    def __repr__(self):
        return '<Error (error_id={})>'.format(self.error_id)

    def __str__(self):
        return self.message


def get_session():
    """ Return an SQLAlchemy session """
    return Session()


@contextmanager
def yield_session(commit=False):
    sess = get_session()
    yield sess
    if commit:
        sess.commit()


# Helpful little functions

def get_latest_commit():
    with yield_session() as sess:
        return sess.query(Commit).order_by(Commit.committed_date.desc()).first()


def get_total_eips():
    with yield_session() as sess:
        return sess.query(func.count(EIP.eip_id)).first()[0]


def get_total_commits():
    with yield_session() as sess:
        return sess.query(func.count(Commit.commit_hash)).first()[0]


def get_total_committers():
    with yield_session() as sess:
        return sess.query(func.count(distinct(Commit.committer))).first()[0]


def get_total_errors():
    with yield_session() as sess:
        return sess.query(func.count(Error.eip_id)).first()[0]


def get_all_tags():
    with yield_session() as sess:
        return sess.query(
            Tag.tag_name,
            Tag.active,
            func.count(EIP.eip_id).label('eips_count'))\
            .join(EIPTag, EIPTag.c.tag_name == Tag.tag_name)\
            .join(EIP, EIP.eip_id == EIPTag.c.eip_id)\
            .filter(Tag.active == True)\
            .group_by(Tag).order_by(Tag.tag_name).all()


def get_eip_tags(eip_id):
    with yield_session() as sess:
        return sess.query(Tag).filter(Tag.eips.any(eip_id=eip_id)).order_by(Tag.tag_name).all()


def set_error(session, eip_id, error_type, message):
    log.debug('set_error({}, {}, {})'.format(eip_id, error_type, message))
    err = Error(
        eip_id=eip_id,
        error_type=error_type,
        message=message,
        when=datetime.now(),
    )
    return session.merge(err)
