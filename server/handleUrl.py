__author__ = 'mt'
# -*- coding: utf-8 -*-
import tornado.web
from getData import *
import time
from tornado import template


class ListHandler(tornado.web.RequestHandler):
    def get(self):
        if self.request.arguments['time'][0] == '0':
            self.request.arguments['time'][0] = str(int(time.time()*10000))
        self.write(get_article_list_as_json(self.request.arguments['user'][0], self.request.arguments['time'][0]))


class ArticleHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(get_content_as_json(self.request.arguments['hash'][0]))