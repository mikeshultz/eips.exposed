from attrdict import AttrDict
from graphene import (
    Schema,
    ObjectType,
    Field,
    ID,
    List,
    String,
    Int,
    Enum,
    Date,
    Boolean,
    DateTime,
)
from eips_exposed.common.db import (
    joinedload,
    yield_session,
    EIP as DBEIP,
    Error as DBError,
    Commit as DBCommit,
    get_total_eips,
    get_total_commits,
    get_total_committers,
    get_total_errors,
    get_eip_tags,
    get_all_tags,
    get_categories_with_totals,
    get_statuses_with_totals,
)
from eips_exposed.processor.objects import EIPType, EIPStatus, EIPCategory, ErrorType


EIPCategoryField = Field(type=Enum.from_enum(EIPCategory))
EIPStatusField = Field(type=Enum.from_enum(EIPStatus))


class EIP(ObjectType):
    eip_id = ID()
    eip_type = Field(type=Enum.from_enum(EIPType))
    title = String()
    author = String()
    status = EIPStatusField
    created = Date()
    updated = String()
    discussions_to = String()
    review_period_end = String()
    category = EIPCategoryField
    requires = List(Int)
    replaces = List(Int)
    superseded_by = List(Int)
    resolution = String()
    full_text = String()
    tags = List(String)


class Stats(ObjectType):
    eips = Int()
    commits = Int()
    contributors = Int()
    errors = Int()


class Tag(ObjectType):
    tag_name = String()
    active = Boolean()
    eips_count = Int()


class Error(ObjectType):
    eip_id = ID()
    error_type = Field(type=Enum.from_enum(ErrorType))
    when = DateTime()
    message = String()


class Commit(ObjectType):
    commit_hash = ID()
    author = String()
    committer = String()
    committed_date = DateTime()
    message = String()


class Category(ObjectType):
    category = EIPCategoryField
    eip_count = Int()


class Status(ObjectType):
    status = EIPStatusField
    eip_count = Int()


class Query(ObjectType):
    stats = Field(Stats)
    eip = Field(EIP, eip_id=ID(required=True))
    eips = List(
        EIP,
        limit=Int(default_value=100),
        offset=Int(default_value=0),
        tag=String(),
        category=String(),
        status=String(),
        search=String(),
    )
    commits = List(
        Commit,
        limit=Int(default_value=100),
        offset=Int(default_value=0),
        eip_id=Int(),
        search=String(),
    )
    errors = List(Error)
    tags = List(Tag, eip_id=ID())
    categories = List(Category)
    statuses = List(Status)

    def resolve_eip(_, info, eip_id):
        with yield_session() as sess:
            return sess.query(DBEIP).filter(DBEIP.eip_id == eip_id).options(
                joinedload('tags')
            ).one_or_none()

    def resolve_eips(_, info, limit, offset, tag=None, category=None, status=None, search=None):
        with yield_session() as sess:
            if tag:
                return sess.query(DBEIP).filter(
                    DBEIP.tags.any(tag_name=tag)
                ).order_by(DBEIP.eip_id).limit(limit).offset(offset).options(
                    joinedload('tags')
                ).all()
            elif category:
                return sess.query(DBEIP).filter(
                    DBEIP.category == category.upper()
                ).order_by(DBEIP.eip_id).limit(limit).offset(offset).options(
                    joinedload('tags')
                ).all()
            elif status:
                return sess.query(DBEIP).filter(
                    DBEIP.status == status.upper()
                ).order_by(DBEIP.eip_id).limit(limit).offset(offset).options(
                    joinedload('tags')
                ).all()
            else:
                if search:
                    return DBEIP.search(sess, search).order_by(DBEIP.eip_id).limit(limit).offset(offset).options(
                        joinedload('tags')
                    ).all()
                else:
                    return sess.query(DBEIP).order_by(DBEIP.eip_id).limit(limit).offset(offset).options(
                        joinedload('tags')
                    ).all()

    def resolve_commits(_, info, limit, offset, eip_id=None, search=None):
        with yield_session() as sess:
            if eip_id:
                # TODO: add search with eip_id
                return sess.query(
                    DBCommit
                ).filter(
                    DBCommit.eips.any(eip_id=eip_id)
                ).order_by(DBCommit.committed_date.desc()).limit(limit).offset(offset).all()
            else:
                if search:
                    return DBCommit.search(
                        sess,
                        search
                    ).order_by(DBCommit.committed_date.desc()).limit(limit).offset(offset).all()
                else:
                    return sess.query(
                        DBCommit
                    ).order_by(DBCommit.committed_date.desc()).limit(limit).offset(offset).all()

    def resolve_errors(_, info):
        with yield_session() as sess:
            return sess.query(DBError).all()

    def resolve_stats(_, info):
        return AttrDict({
            'eips': get_total_eips(),
            'commits': get_total_commits(),
            'contributors': get_total_committers(),
            'errors': get_total_errors(),
        })

    def resolve_tags(_, info, eip_id=None):
        if eip_id:
            return get_eip_tags(eip_id)
        else:
            return get_all_tags()

    def resolve_categories(_, info):
        return get_categories_with_totals()

    def resolve_statuses(_, info):
        return get_statuses_with_totals()


schema = Schema(query=Query)
