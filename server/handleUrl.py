__author__ = 'mt'
# -*- coding: utf-8 -*-
import tornado.web
from getData import *
import time
from handleUser import *


class ListHandler(tornado.web.RequestHandler):
    def get(self):
        if self.request.arguments['time'][0] == '0':
            self.request.arguments['time'][0] = str(int(time.time()*10000))
        self.write(get_article_list_as_json(self.request.arguments['user'][0], self.request.arguments['time'][0]))


class ArticleHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(get_content_as_json(self.request.arguments['hash'][0]))


class RegisterHandler(tornado.web.RequestHandler):
    def post(self):
        try:
            if self.request.arguments['what'][0] == 'register':
                add_user(self.request.arguments['main-uid'][0])
                self.write("{'ret':0}")
            if self.request.arguments['what'][0] == 'merge':
                merge_user(self.request.arguments['main-uid'][0], self.request.arguments['merge-uid'][0],
                           self.request.arguments['type'][0])
        except Exception as err:
            self.write('参数错误' + err.message)

    def get(self):
        try:
            if self.request.arguments['what'][0] == 'register':
                add_user(self.request.arguments['main-uid'][0])
                self.write("{'ret':0}")
            if self.request.arguments['what'][0] == 'merge':
                merge_user(self.request.arguments['main-uid'][0], self.request.arguments['merge-uid'][0],
                           self.request.arguments['type'][0])
        except Exception as err:
            self.write('参数错误' + err.message)