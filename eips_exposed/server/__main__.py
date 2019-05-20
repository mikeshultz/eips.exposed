from tornado.ioloop import IOLoop
from eips_exposed.common.config import CONFIG
from eips_exposed.server.app import app
from eips_exposed.common import getLogger

log = getLogger(__name__)

if __name__ == '__main__':
    log.info('Starting server on port {}'.format(CONFIG['SERVER_PORT']))
    app.listen(CONFIG['SERVER_PORT'])
    IOLoop.instance().start()
