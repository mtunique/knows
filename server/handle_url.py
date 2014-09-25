__author__ = 'mt'
# -*- coding: utf-8 -*-
import time
import sys
import os
import tornado.web
from get_data import *
from handle_user import *
import knows_users as k_user

sys.path.append(os.path.join(os.path.abspath('..'), 'algorithm'))
from std_functions import cos

TAG_VECTOR = mongodb.db.tag_vector.find_one({}, {'_id': 0})


def handle_err(func):
    def real(self):
        # try:
        #
        # except Exception as err:
        #     print '参数错误  %s' % str(err.message)
        #TODO write errors into logs
        func(self)
    return real


def type_json(func):
    def real(self):
        self.set_header('Content-Type', 'application/json')
        func(self)
    return real


class ListHandler(tornado.web.RequestHandler):
    @handle_err
    @type_json
    def get(self):
        if self.request.arguments['time'][0] == '0':
            self.request.arguments['time'][0] = str(int(time.time()*10000))
        self.write(json.dumps(get_list_from_uid(self.request.arguments['user'][0], self.request.arguments['time'][0])))


class ArticleHandler(tornado.web.RequestHandler):
    @handle_err
    def get(self):
        user_like(self.request.arguments['user'][0], self.request.arguments['hash'][0])
        self.write(get_content(self.request.arguments['hash'][0]))


class CollectHandler(tornado.web.RequestHandler):
    @handle_err
    @type_json
    def get(self):
        if self.request.arguments['time'][0] == '0':
            self.request.arguments['time'][0] = str(int(time.time()*10000))
            self.write(json.dumps(get_collect_list(self.request.arguments['uid'][0],
                                                   self.request.arguments['time'][0])))


class LikeHandler(tornado.web.RequestHandler):
    @handle_err
    def get(self):
        user_collect(self.request.arguments['uid'][0], self.request.arguments['hash'][0])
        tp = ''
        if self.request.arguments['type'][0] == '1':
            tp = '$addToSet'
        elif self.request.arguments['type'][0] == '0':
            tp = '$pull'
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
    @type_json
    def get(self):
        db_info = mongodb.db.merger_info.find_one({'way': self.request.arguments['way'][0],
                                                   'uid': self.request.arguments['uid'][0]})
        if db_info:
            main_id = db_info['main_id']
            vector = db_info['vector']
        else:
            main_id = k_user.create_id(self.request.arguments['way'][0]+self.request.arguments['uid'][0])
            vector = [0] * 20

        info = {'way': self.request.arguments['way'][0],
                'uid': self.request.arguments['uid'][0],
                'name': self.request.arguments['name'][0],
                'token': self.request.arguments['token'][0],
                'main_id': main_id,
                'vector': vector}

        mongodb.db.merger_info.update({'way': self.request.arguments['way'][0],
                                       'uid': self.request.arguments['uid'][0]},
                                      {'$set': info},
                                      upsert=True)
        self.write(json.dumps({'_id': info['uid'],
                               'isregister': str(not db_info == None)}))

    @handle_err
    def post(self):
        self.get(self)


class TagHandler(tornado.web.RequestHandler):
    @handle_err
    @type_json
    def get(self):
        if self.request.arguments['time'][0] == '0':
            self.request.arguments['time'][0] = str(int(time.time()*10000))
        self.write(get_list_from_tag(self.request.arguments['tag'][0], self.request.arguments['time'][0]))


class DelHandler(tornado.web.RequestHandler):
    @handle_err
    def get(self):
        user_dislike(self.request.arguments['uid'][0], self.request.arguments['hash'][0])


class FirstInfoHandler(tornado.web.RequestHandler):
    @handle_err
    @type_json
    def post(self):
        info = json.loads(self.request.body)

        data = mongodb.db.merger_info.find_one({'uid': info['uid']})
        vector = data['vector']

        global TAG_VECTOR
        TAG_VECTOR = dict(TAG_VECTOR)

        for tag in info['what']:
            if tag in TAG_VECTOR:
                vector = [vector[i] + TAG_VECTOR[tag][i] for i in range(20)]
        vector = [vector[i] / len(info['what']) for i in range(20)]

        tot_cos = 0.
        for tag_vec in TAG_VECTOR.values():
            tot_cos += cos(vector, tag_vec)

        mongodb.db.merger_info.update({'_id': data['_id']},
                                      {'$set': {'vector': vector, 'thr': tot_cos / len(TAG_VECTOR)}}, upsert=True)

        self.write('1')


class VerHandler(tornado.web.RequestHandler):
    @handle_err
    def get(self):
        self.write("{'version_code':1,'version':'1.0','address':'http://knows.mtunique.com/knows.apk'}")