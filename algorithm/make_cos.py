__author__ = 'mt'
# -*- coding: utf-8 -*-


class Vector(object):
    def __init__(self, l):
        self.l = l



def cos(x, y):
    if len(x) == len(y):
        ans = 0

        for i in range(len(x)):
            ans += x[i] * y[i]
    else:
        print "Vectors' lengths are different"
        return


def main():
    pass

if __name__ == '__main__':
    main()