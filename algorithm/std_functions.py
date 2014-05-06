__author__ = 'mt'
# -*- coding: utf-8 -*-
import math
from counts import *


def _cos(x, y):
    ans = 0.
    for i in range(len(x)):
        ans += x[i] * y[i]
    ans = math.sqrt(ans)
    return ans


def cos(x, y):
    if len(x) == len(y):
        return _cos(x, y)
    else:
        print "Vectors' lengths are different"


def doc_vector(doc):
    ids, count = parse_doc_list(doc)
    temp_dict = {}
    for i, num in ids, count:
        temp_dict.setdefault(str(i), num)
    ans = []
    for i in range(VECTOR_LEN):
        try:
            ans.append(temp_dict[str(i)])
        except KeyError:
            ans.append(0.)
    return ans

