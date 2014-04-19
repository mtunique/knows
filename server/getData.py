__author__ = 'mt'
# -*- coding: utf-8 -*-
import pymongo
import json
from dbs.mongodb import db


def getConnetAsJson(data):
    try:
        return db.content.find_one({'_id': data})['content']
    except:
        return '无法获取文章'


def getAricleListJson(user, time):
    return json.dumps(list(db.article.find({"time": {"$lt": time}}).limit(15)))


if __name__ == '__main__':
    print getAricleListJson('dsada','0A7A67B60F28FD80415511EFB6FFD54A')
