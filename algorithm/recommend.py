__author__ = 'mt'
import traceback
import threading
from dbs import redisdb, mongodb
from std_functions import cos

TAGS = ['cloud', 'develop', 'prolang', 'systemsecure', 'pm',
        'hardware', 'news', 'viewdesign,', 'uidesign', 'appanalyze']


def main():
    global users
    import random
    while True:
        tmp, content_hash = redisdb.db.brpop('s_content')
        if random.randint(1, 5) == 1:
            redisdb.db.lpush('base_list', content_hash)
            redisdb.db.ltrim('base_list', 0, 199)
        try:
            data = mongodb.db.v_content.find_one({'_id': content_hash}, {'t': 1})

            for user in users:
                if user['thr'] > cos(data['t'], user['vector']) or random.randint(1, 5) == 1:
                    redisdb.db.lpush(user['uid'], content_hash)
                    redisdb.db.ltrim(user['uid'], 0, 199)

        except Exception as err:
            print '[%s]:%s' % (content_hash, str(err.message))
            traceback.print_exc()
            redisdb.db.lpush('recommend_error', content_hash)


def update_users():
    global users
    import time
    while 1:
        users = list(mongodb.db.merger_info.find({}, {'main_id': 1, 'vector': 1, 'thr': 1}))
        time.sleep(600)


if __name__ == '__main__':
    import sys
    outfile = open('recommend.log', 'w')
    sys.stderr = outfile
    sys.stdout = outfile
    users = list(mongodb.db.merger_info.find({}, {'main_id': 1, 'vector': 1, 'thr': 1}))
    thread = threading.Thread(target=update_users)
    thread.start()
    main()