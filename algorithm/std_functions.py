__author__ = 'mt'
# -*- coding: utf-8 -*-
import math
from counts import *
import jieba
import jieba.analyse
from bs4 import BeautifulSoup


def to_string(content, strip=True):
    return BeautifulSoup(content).html.body.get_text('\n', strip=strip)


def _cos(x, y):
    ans = 0.
    len_x = 0
    len_y = 0
    for i in range(len(x)):
        ans += x[i] * y[i]
        len_x += x[i] ** 2
        len_y += y[i] ** 2
    return math.sqrt(math.fabs(ans)) / math.sqrt(len_x) / math.sqrt(len_y)


def cos(x, y):
    if len(x) == len(y):
        return _cos(x, y)
    else:
        print "Vectors' lengths are different"


def parse_doc_list(docs, vocab):
    """
    @param docs: A List of documents. Each document must be a string
    @param vocab: No_stop_words vocabularies, that's to say only when the word is in this list will it not be ignored
    @return:
    Returns a pair of lists of lists.

    The first, wordids, says what vocabulary tokens are present in
    each document. wordids[i][j] gives the jth unique token present in
    document i. (Don't count on these tokens being in any particular
    order.)

    The second, wordcts, says how many times each vocabulary token is
    present. wordcts[i][j] is the number of times that the token given
    by wordids[i][j] appears in document i.
    """

    #jieba.initialize()

    D = len(docs)

    wordids = list()
    wordcts = list()
    for d in range(0, D):
        words = jieba.cut(docs[d])
        ddict = dict()
        for word in words:
            if word in vocab:
                wordtoken = vocab[word]
                if not wordtoken in ddict:
                    ddict[wordtoken] = 0
                ddict[wordtoken] += 1


        wordids.append([i-1 for i in ddict.keys()])
        wordcts.append(ddict.values())

    return wordids, wordcts


def doc_to_vector(doc, vocab):
    ids, count = parse_doc_list([doc], vocab)
    ids, count = ids[0], count[0]
    temp_dict = {}
    if len(ids):
        for index in range(len(ids)):
            temp_dict.setdefault(str(ids[index]), count[index])
    ans = []
    for tmp_id in range(VECTOR_LEN):
        try:
            ans.append(temp_dict[str(tmp_id)])
        except KeyError:
            ans.append(0.)
    return ans


def get_base_vectors(db=None):
    if not db:
        from dbs.mongodb import db
    return [db.vector.find_one({'_id': str(i)})['v'] for i in range(20)]


def vector_to_topic_vector(vector, base_vector):
    return [cos(vector, base_vector[i]) for i in range(20)]


if __name__ == '__main__':
    print cos([0.1, -0.1], [1.1, -0.9])