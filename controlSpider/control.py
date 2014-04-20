__author__ = 'mt'
# -*- coding: utf-8 -*-
import threading
import time


def spider1():
    time.sleep(10)
    print '1'
    print time.time()


def spider2():
    time.sleep(20)
    print '2'
    print time.time()


t1 = threading.Thread(target=spider1)
t2 = threading.Thread(target=spider2)

print time.time()
t1.start()
t2.start()

