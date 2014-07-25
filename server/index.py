__author__ = 'mt'
# -*- coding: utf-8 -*-
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

# from tornado.options import define, options
# define("port", default=8080, help="run on the given port", type=int)


from handle_url import *


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application([
        (r"/list*", ListHandler),
        (r"/article*", ArticleHandler),
        (r"/collect*", CollectHandler),
        (r"/user*", UserHandler),
        (r"/like*", LikeHandler)
    ]
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8080)
    tornado.ioloop.IOLoop.instance().start()