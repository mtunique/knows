__author__ = 'mt'
# -*- coding: utf-8 -*-
import tornado.web
from get_data import *
import time
from handle_user import *


def handle_err(func):
    def real(self):
        try:
            func(self)
        except Exception as err:
            print '参数错误  %s' % str(err.message)
    return real


class ListHandler(tornado.web.RequestHandler):
    @handle_err
    def get(self):
        if self.request.arguments['time'][0] == '0':
            self.request.arguments['time'][0] = str(int(time.time()*10000))
        self.write(get_article_list_as_json(self.request.arguments['user'][0], self.request.arguments['time'][0]))


class ArticleHandler(tornado.web.RequestHandler):
    @handle_err
    def get(self):
        self.write(get_content_as_json(self.request.arguments['hash'][0]))


class CollectHandler(tornado.web.RedirectHandler):
    @handle_err
    def get(self):
        self.write(get_collect_list(self.request.arguments['uid'][0]))


class LikeHandler(tornado.web.RedirectHandler):
    @handle_err
    def get(self):
        mongodb.db.like.update(
            {'_id':self.request.arguments['uid']},
            {'$push':{'hash': self.request.arguments['hash']}},
            upsert=True)