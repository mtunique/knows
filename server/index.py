__author__ = 'mt'
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import tornado.wsgi
import tornado.ioloop
import tornado.web
import tornado.httpserver
import os

from handle_url import *

settings = {
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        }

if __name__ == '__main__':
    app = tornado.wsgi.WSGIApplication([
        (r"/list*", ListHandler),
        (r"/article*", ArticleHandler),
        (r"/collect*", CollectHandler),
        (r"/user*", UserHandler),
        (r"/like*", LikeHandler),
        ],
        **settings)

    app.listen(8080)
    tornado.ioloop.IOLoop.instance().start()