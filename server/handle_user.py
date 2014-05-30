__author__ = 'mt'
# -*- coding: utf-8 -*-
from dbs import mongodb


def add_user(uid):
    pass


def merge_user(uid, merge_id, tp):
    mongodb.db.user.update({'_id':uid}, {'$set':{tp: merge_id}}, upsert=True)