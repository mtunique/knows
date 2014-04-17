__author__ = 'mt'
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import tornado.wsgi
import tornado.ioloop
import tornado.web
import tornado.httpserver
import wsgiref.simple_server
import os

from handleUrl import *

settings = {
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        }

if __name__ == '__main__':
    app = tornado.wsgi.WSGIApplication([(r"/list/*", MainHandler),(r"/article*", MainHandler), ], **settings)

    server = wsgiref.simple_server.make_server('', 8080, app)
    server.serve_forever()
else:
    app = tornado.wsgi.WSGIApplication([(r"/", MainHandler), ], **settings)

    server = wsgiref.simple_server.make_server('', 8080, app)
    server.serve_forever()
