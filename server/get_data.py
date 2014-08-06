__author__ = 'mt'
# -*- coding: utf-8 -*-
from pymongo import DESCENDING
import json
from dbs.mongodb import db


def ids_list_to_article_list(ids, time, limit=15):
    return list(db.article.find({'_id': {'$in': ids}, "time": {"$lt": time}})
                .sort("time", DESCENDING).limit(limit))


def get_content(data):
    try:
        return '<!DOCTYPE html><html><head><link rel="stylesheet" ' \
            'href="file:///android_asset/mystyle.css"><meta ' \
            'charset="utf-8"><script src="file:///android_asset/my.js"></script' \
            '></head><body><div class="article_content" id="article_content">%s</div>' \
            '<script type="text/javascript" src="file:///android_asset/myscript.js">' \
            '</script></body></html>' % db.content.find_one({'_id': data})['content']
    except Exception as err:
        #TODO now it is duty
        return '无法获取文章'+str(err)


def get_list_from_uid(user, time, limit=15):
    #TODO use algorithm
    return json.dumps(list(db.article.find({"time": {"$lt": time}}).sort("time", DESCENDING).limit(limit)))


def get_collect_list(uid, time):
    try:
        l = db.like.find_one({"_id": uid})['hash']
    except Exception as err:
        #TODO send errors to logs
        print err.message
        return []
    return ids_list_to_article_list(l, time)


def get_list_from_tag(tag, time, limit=15):
    article_list = []
    try:
        article_list = list(db.article.find({"tag": tag, "time": {"$lt": time}})
                            .sort("time", DESCENDING).limit(limit))
    except Exception as err:
        #TODO send errors to logs
        print err.message
    return json.dumps(article_list)

if __name__ == '__main__':
    pass