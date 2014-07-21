__author__ = 'mt'
# -*- coding: utf-8 -*-
import tornado.web
from get_data import *
import time
from handle_user import *
import knows_users as k_user


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
        self.write(get_article_list_as_json(self.request.arguments['user'][0],
                                            self.request.arguments['time'][0]))


class ArticleHandler(tornado.web.RequestHandler):
    @handle_err
    def get(self):
        self.write(get_content_as_json(self.request.arguments['hash'][0]))


class CollectHandler(tornado.web.RequestHandler):
    #@handle_err
    def get(self):
        if self.request.arguments['time'][0] == '0':
            self.request.arguments['time'][0] = str(int(time.time()*10000))
        self.write(json.dumps(get_collect_list(self.request.arguments['uid'][0], self.request.arguments['time'][0])))


class LikeHandler(tornado.web.RequestHandler):
    @handle_err
    def get(self):
        tp = ''
        if self.request.arguments['type'][0] == '1':
            tp = '$addToSet'
        elif self.request.arguments['type'][0] == '0':
            tp = 'pull'
        if tp:
            mongodb.db.like.update(
                {'_id':   self.request.arguments['uid'][0]},
                {tp: {'hash': self.request.arguments['hash'][0]}},
                upsert=True)
            self.write('1')
        else:
            self.write('0')


class UserHandler(tornado.web.RequestHandler):
    @handle_err
    def post(self):
        db_info = mongodb.db.merger_info.find_one({'way': self.request.arguments['way'][0],
                                                  'uid': self.request.arguments['uid'][0]})
        if db_info:
            main_id = db_info['main_id']
        else:
            main_id = k_user.create_id(self.request.arguments['way'][0]+self.request.arguments['uid'][0])
        info = {'way': self.request.arguments['way'][0],
                'uid': self.request.arguments['uid'][0],
                'name': self.request.arguments['name'][0],
                'token': self.request.arguments['token'][0],
                'main_id': main_id}
        mongodb.db.merger_info.update({'way': self.request.arguments['way'][0],
                                       'uid': self.request.arguments['uid'][0]},
                                      {'$set': info},
                                      upsert=True)
        self.write(json.dumps({'_id': main_id,
                    'merger_info':list(mongodb.db.merger_info.find({'way': self.request.arguments['way'][0],
                                                                    'uid': self.request.arguments['uid'][0]},
                                                                   {'_id': 0}))}))
    @handle_err
    def get(self):
        db_info = mongodb.db.merger_info.find_one({'way': self.request.arguments['way'][0],
                                                  'uid': self.request.arguments['uid'][0]})
        if db_info:
            main_id = db_info['main_id']
        else:
            main_id = k_user.create_id(self.request.arguments['way'][0]+self.request.arguments['uid'][0])
        info = {'way': self.request.arguments['way'][0],
                'uid': self.request.arguments['uid'][0],
                'name': self.request.arguments['name'][0],
                'token': self.request.arguments['token'][0],
                'main_id': main_id}
        mongodb.db.merger_info.update({'way': self.request.arguments['way'][0],
                                       'uid': self.request.arguments['uid'][0]},
                                      {'$set': info},
                                      upsert=True)
        self.write(json.dumps({'_id':main_id,
                    'merger_info':list(mongodb.db.merger_info.find({'way': self.request.arguments['way'][0],
                                                                    'uid': self.request.arguments['uid'][0]},
                                                                   {'_id': 0}))}))