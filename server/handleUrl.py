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
        self.write(getAricleListJson(self.request.arguments['user'][0], self.request.arguments['time'][0]))


class ArticleHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(getConnetAsJson(self.request.arguments['hash'][0]))