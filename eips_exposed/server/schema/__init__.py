from graphene import (
    Schema,
    ObjectType,
    Field,
    ID,
    List,
    String,
    Int,
)
from eips_exposed.common.db import (
    get_session,
    EIP as DBEIP
)


class EIP(ObjectType):
    eip_id = ID()
    title = String()


class Query(ObjectType):
    eip = Field(EIP, eip_id=ID(required=True))
    eips = List(EIP, limit=Int(default_value=100), offset=Int(default_value=0))

    def resolve_eip(_, info, eip_id):
        sess = get_session()
        return sess.query(DBEIP.eip_id, DBEIP.title).filter(DBEIP.eip_id == eip_id).one_or_none()

    def resolve_eips(_, info, limit, offset):
        sess = get_session()
        return sess.query(DBEIP).order_by(DBEIP.eip_id).limit(limit).offset(offset).all()


schema = Schema(query=Query)
