__author__ = 'mt'
# -*- coding: utf-8 -*-
import hashlib


def create_id(seed):
    md5 = hashlib.md5()
    md5.update(seed)
    return md5.hexdigest()


if __name__ == '__main__':
    print create_id('mt')