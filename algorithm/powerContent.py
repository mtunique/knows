__author__ = 'mt'
# -*- coding: utf-8 -*-
import redis
from bs4 import BeautifulSoup


class PowerContent(object):
    def __init__(self, content):
        self.content = content
        self.html = BeautifulSoup(content).html

    def to_string(self, separator=u"", strip=True):
        self.html.get_text('\n', separator=separator, strip=strip)


#if __name__ == '__main__':