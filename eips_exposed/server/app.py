import tornado.web
from tornado.gen import coroutine, Return
from graphene_tornado.tornado_graphql_handler import TornadoGraphQLHandler

from eips_exposed.server.schema import schema
from eips_exposed.common import getLogger

log = getLogger(__name__)

ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'https://eips.exposed:80',
]


class GraphQLHandler(TornadoGraphQLHandler):
    """ Do some stuff that the graphene_tornado handler doesn't, like CORS """
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Headers", 'x-requested-with, content-type')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        if self.request.headers.get('Origin'):
            origin = self.request.headers['Origin']
            self.set_header("Access-Control-Allow-Origin", origin)

    def options(self):
        if self.request.headers.get('Origin') in ALLOWED_ORIGINS:
            self.set_status(204)
        self.finish()


class EIPSExposedApplication(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r'/graphql', GraphQLHandler, dict(graphiql=True, schema=schema)),
            (r'/graphql/batch', GraphQLHandler, dict(graphiql=True, schema=schema,
             batch=True)),
            (r'/graphql/graphiql', GraphQLHandler, dict(graphiql=True, schema=schema))
        ]
        tornado.web.Application.__init__(self, handlers)


app = EIPSExposedApplication()
