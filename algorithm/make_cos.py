__author__ = 'mt'
# -*- coding: utf-8 -*-
from std_functions import *
from dbs import mongodb


class Vector(object):

    def __init__(self, l):
        self.res = l
        self.dimension = len(l)

    def __getitem__(self, item):
        return self.res[item]

    def __len__(self):
        return self.dimension

    def length(self):
        ans = 0.
        for i in range(self.dimension):
            ans += self.res[i] * self.res[i]
        ans = math.sqrt(ans)
        return ans


def main(article):
    vectors = list(mongodb.db.vector.find({}))
    ans = {}
    for vector in vectors:
        ans.setdefault(vector['_id'], cos(list(vector['v']), article))
    return [ans[str(i)] for i in range(len(ans))]

if __name__ == '__main__':
    main()