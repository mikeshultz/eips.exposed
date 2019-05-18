from tornado.ioloop import IOLoop
from eips_exposed.common.config import CONFIG
from eips_exposed.server.app import app

if __name__ == '__main__':
    app.listen(CONFIG['SERVER_PORT'])
    IOLoop.instance().start()
