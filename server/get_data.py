__author__ = 'mt'
# -*- coding: utf-8 -*-
from pymongo import DESCENDING
import json
from dbs.mongodb import db


def get_content_as_json(data):
    try:
        return db.content.find_one({'_id': data})['content']
    except Exception as err:
        return '无法获取文章'+str(err)


def get_article_list_as_json(user, time):
    return json.dumps(list(db.article.find({"time": {"$lt": time}}).sort("time", DESCENDING).limit(15)))


if __name__ == '__main__':
    print get_article_list_as_json('dsada', '1111111111110')