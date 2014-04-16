__author__ = 'mt'
# -*- coding: utf-8 -*-
import tornado.web
from getData import *
from tornado import template


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        if 'hash' in self.request.arguments:
            print self.write(getConnetAsJson(self.request.arguments['hash'][0]))
        else:
            self.write(getAricleListJson(self.request.arguments['user'][0], self.request.arguments['time'][0]))