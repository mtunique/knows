__author__ = 'mt'
# -*- coding: utf-8 -*-
import sys
import threading
import time
import subprocess
from settings import SPIDER_INTERVAL as sp


def exec_spider(name, interval):
    while True:
        try:
            script = 'cd ../knows/knows/\nscrapy crawl %s' % name
            output = subprocess.check_output(script, shell=True, stderr=subprocess.STDOUT)
            print output
        except subprocess.CalledProcessError as err:
            print err
        time.sleep(interval)


def main():
    spiders = {}
    for i in sp:
        spider = threading.Thread(target=exec_spider, args=(i, sp[i]))
        spiders.setdefault(i, spider)
        spider.start()

if __name__ == '__main__':
    outfile = open('control.log', 'w')
    sys.stdout = outfile
    sys.stderr = outfile
    main()
