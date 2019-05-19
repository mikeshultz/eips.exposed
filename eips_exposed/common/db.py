from contextlib import contextmanager
from sqlalchemy import (
    create_engine,
    Table,
    ForeignKey,
    Column,
    Integer,
    String,
    Enum,
    DateTime,
    Text,
)
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import ARRAY
from eips_exposed.common import CONFIG
from eips_exposed.processor.objects import EIPType, EIPStatus, EIPCategory

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

    commits = relationship('Commit', secondary=EIPCommit)

    def __repr__(self):
        return '<EIP (eip_id={})>'.format(self.eip_id)


class Commit(Base):
    __tablename__ = 'commit'

    commit_hash = Column(String(40), primary_key=True)
    committer = Column(String(), nullable=False)
    committed_date = Column(DateTime(), nullable=False)
    message = Column(Text())

    eips = relationship('EIP', secondary=EIPCommit)

    def __repr__(self):
        return '<Commit (commit_hash={})>'.format(self.commit_hash)


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
