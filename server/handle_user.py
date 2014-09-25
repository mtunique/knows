__author__ = 'mt'
# -*- coding: utf-8 -*-
from dbs import mongodb
import sys
import os
import time

sys.path.append(os.path.join(os.path.abspath('..'), 'algorithm'))
from std_functions import cos


def user_like(user, article_hash):
    article_data = mongodb.db.v_content.find_one({'_id': article_hash}, {'t': 1})
    user_data = mongodb.db.merger_info.find_one({'uid': user}, {'vector': 1})
    user_data['vector'] = [(user_data['vector'][i] + article_data['t'][i]*0.1) / 2 for i in range(20)]
    mongodb.db.merger_info.update({'uid': user}, {'$set': {'vector': user_data['vector']}}, upsert=True)


def user_dislike(user, article_hash):
    article_data = mongodb.db.v_content.find_one({'_id': article_hash}, {'t': 1})
    user_data = mongodb.db.merger_info.find_one({'uid': user}, {'vector': 1})
    user_data['vector'] = [(user_data['vector'][i] - article_data['t'][i]*0.1) / 2 for i in range(20)]
    mongodb.db.merger_info.update({'uid': user}, {'$set': {'vector': user_data['vector']}}, upsert=True)
    mongodb.db.dislike.update({'uid': user, 'hash': article_hash},
                              {'uid': user, 'hash': article_hash, 'time': str(int(time.time()*10000))}, upsert=True)


def user_collect(user, article_hash):
    article_data = mongodb.db.v_content.find_one({'_id': article_hash}, {'t': 1})
    user_data = mongodb.db.merger_info.find_one({'uid': user}, {'vector': 1})
    user_data['vector'] = [(user_data['vector'][i] + article_data['t'][i]) / 2 for i in range(20)]
    mongodb.db.merger_info.update({'uid': user}, {'$set': {'vector': user_data['vector']}}, upsert=True)

