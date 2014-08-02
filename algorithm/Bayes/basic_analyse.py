__author__ = 'mxunique'
# coding: utf-8

import jieba
import codecs
import os
import json


def get_tag_list(filepath):
    fd = codecs.open(filepath, 'r', encoding='utf-8')
    vector_list = [line.strip() for line in fd.readlines()]
    return vector_list


def get_words_list(filepath):
    fd = codecs.open(filepath, 'r', encoding='utf-8')
    raw_content = fd.read()
    return [word for word in jieba.cut(raw_content)]


def get_words_list_from_string(string):
    return [word for word in jieba.cut(string)]


def get_trained_vector_dict(filepath):
    fd = codecs.open(filepath, 'r', encoding='utf-8')
    vector_dict = json.loads(fd.read())
    fd.close()
    return vector_dict


def get_file_list(dirpath):
    """
    used only in debug
    """
    filelist = os.listdir(dirpath)
    return filelist


# TODO make graph , show the vector in histogram
def draw_vector_hist(vecotr_dict):
    pass


if __name__ == '__main__':
    pass