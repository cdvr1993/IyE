#!/usr/bin/env python

import os

from tornado import httpserver, ioloop, web, wsgi, websocket
from tornado.options import options, define, parse_command_line
from django.core.wsgi import get_wsgi_application
from django.conf import settings


define('port', type=int, default=8000)


class SocketHandler(websocket.WebSocketHandler):
    def open(self):
        pass

    def on_message(self, msg):
        self.write_message('Server reads ' + msg)

    def on_close(self):
        pass


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "IyE.settings")
    parse_command_line()
    wsgi_app = wsgi.WSGIContainer(get_wsgi_application())
    tornado_app = \
        web.Application([(r'/chat', SocketHandler),
                        (r'/static/(.*)', web.StaticFileHandler,
                         {'path': settings.STATICFILES_DIRS[0]}),
                        ('.*', web.FallbackHandler, dict(fallback=wsgi_app)), ])
    server = httpserver.HTTPServer(tornado_app)
    server.listen(options.port)
    ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()