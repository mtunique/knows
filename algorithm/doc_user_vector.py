__author__ = 'mt'
# -*- coding: utf-8 -*-
import sys
from dbs import redisdb
from dbs import mongodb
from std_functions import cos
import counts


def _update(tmp_cos, content_hash, user):
    if tmp_cos >= user['min']:
        mongodb.db.push_list.update({'_id': user['_id']}, {'$set': {content_hash: tmp_cos}}, upsert=True)
        mongodb.db.push_list.update({'_id': user['_id']},
                                    {'$unset': {user['min_hash']: tmp_cos}}, upsert=True)

        d = mongodb.db.push_list.find_one({'_id': user['_id']}, {'_id': 0})
        mm, mh = min(d.items(), key=lambda x: x[1])
        mongodb.db.user.update({'_id': user['_id']}, {'$set': {'min': mm, 'min_hash': mh}}, upsert=True)
    else:
        mongodb.db.user.update({'_id': user['_id']}, {'$set': {'min': tmp_cos, 'min_hash': content_hash}}, upsert=True)
        mongodb.db.push_list.update({'_id': user['_id']}, {'$set': {content_hash: tmp_cos}}, upsert=True)


def main():
    while True:
        tmp, content_hash = redisdb.db.brpop('s_content')
        try:
            v_content = mongodb.db.v_content.find_one({'_id': content_hash})
            if not v_content:
                print 'can not find %s in mongo.v_content' % content_hash

            users = list(mongodb.db.user.find({}, {'_id': 1, 'vector': 1, 'min': 1, 'min_hash': 1}))
            for user in users:
                tmp_cos = cos(v_content, user['vector'])
                num = len(mongodb.db.push_list.find_one({'_id': user['_id']}))
                if num < counts.MAX_PUSH:
                    mongodb.db.push_list.update({'_id': user['_id']}, {'$set': {content_hash: tmp_cos}}, upsert=True)
                else:
                    _update(tmp_cos, content_hash, user)
        except Exception as err:
            print '[%s] %s' % (content_hash, err.message)

if __name__ == '__main__':
    sys.stdout = open('doc_user_vector.log', 'w')
    main()