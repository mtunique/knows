__author__ = 'mt'
# -*- coding: utf-8 -*-
import threading
import time
import subprocess
from settings import SPIDER_INTERVAL as sp


def exec_spider(name, interval):
    while True:
        try:
            script = 'cd ../knows/knows/\nscrapy crawl %s' % name
            output = subprocess.check_output(script, shell=True)
            print output
        except subprocess.CalledProcessError as err:
            print err
        time.sleep(interval)


spiders = {}
for i in sp:
    spider = threading.Thread(target=exec_spider, args=(i, sp[i]))
    spiders.setdefault(i, spider)
    spider.start()
