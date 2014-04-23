__author__ = 'mt'
# -*- coding: utf-8 -*-
from knows.mongodb import db
import hashlib


def judge_link(link):
    hash = hashlib.md5(link).hexdigest().upper()
    if db.content.find_one({'_id': hash}):
        return True
    else:
        return False


def process_links(links):
    result = []
    for link in links:
        if not judge_link(link.url):
            result.append(link)

    return result