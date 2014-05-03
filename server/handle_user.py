__author__ = 'mt'
# -*- coding: utf-8 -*-
from dbs import mongodb


def add_user(uid):
    pass


def merge_user(uid, merge_id, type):
    mongodb.db.user.update({'_id':uid}, {'$set':{merge_id:type}}, upsert=True)