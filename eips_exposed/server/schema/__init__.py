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
)
from eips_exposed.common.db import (
    get_session,
    EIP as DBEIP,
    get_total_eips,
    get_total_commits,
    get_total_committers,
    get_eip_tags,
    get_all_tags,
)
from eips_exposed.processor.objects import EIPType, EIPStatus, EIPCategory


class EIP(ObjectType):
    eip_id = ID()
    eip_type = Field(type=Enum.from_enum(EIPType))
    title = String()
    author = String()
    status = Field(type=Enum.from_enum(EIPStatus))
    created = Date()
    updated = String()
    discussions_to = String()
    review_period_end = String()
    category = Field(type=Enum.from_enum(EIPCategory))
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
    issues = Int()


class Tag(ObjectType):
    tag_name = String()
    active = Boolean()
    eips_count = Int()


class Query(ObjectType):
    stats = Field(Stats)
    eip = Field(EIP, eip_id=ID(required=True))
    eips = List(EIP, limit=Int(default_value=100), offset=Int(default_value=0), tag=String())
    tags = List(Tag, eip_id=ID())

    def resolve_eip(_, info, eip_id):
        sess = get_session()
        return sess.query(DBEIP).filter(DBEIP.eip_id == eip_id).one_or_none()

    def resolve_eips(_, info, limit, offset, tag=None):
        sess = get_session()
        if tag:
            return sess.query(DBEIP).filter(
                DBEIP.tags.any(tag_name=tag)
            ).order_by(DBEIP.eip_id).limit(limit).offset(offset).all()
        else:
            return sess.query(DBEIP).order_by(DBEIP.eip_id).limit(limit).offset(offset).all()

    def resolve_stats(_, info):
        return AttrDict({
            'eips': get_total_eips(),
            'commits': get_total_commits(),
            'contributors': get_total_committers(),
            'issues': -1,
        })

    def resolve_tags(_, info, eip_id=None):
        if eip_id:
            return get_eip_tags(eip_id)
        else:
            return get_all_tags()


schema = Schema(query=Query)
