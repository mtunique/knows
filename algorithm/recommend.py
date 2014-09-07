__author__ = 'mt'
import traceback
import threading
from dbs import redisdb, mongodb
from std_functions import cos

TAGS = ['cloud', 'develop', 'prolang', 'systemsecure', 'pm',
        'hardware', 'news', 'viewdesign,', 'uidesign', 'appanalyze']


def main():
    global users
    while True:
        tmp, content_hash = redisdb.db.brpop('s_content')
        try:
            data = mongodb.db.v_content.find_one({'_id': content_hash}, {'t': 1})
            for user in users:
                if user['thr'] > cos(data['t'], user['vector']):
                    redisdb.db.rpush(user['main_id'], content_hash)
                    redisdb.db.ltrim(user['main_id'], 0, 199)
        except Exception as err:
            print '[%s]:%s' % (content_hash, str(err.message))
            traceback.print_exc()
            redisdb.db.lpush('recommend_error', content_hash)


def update_users():
    global users
    import time
    while 1:
        users = list(mongodb.db.find({}, {'main_id': 1, 'vector': 1, 'thr': 1}))
        time.sleep(600)


if __name__ == '__main__':
    users = []
    thread = threading.Thread(target=update_users)
    main()