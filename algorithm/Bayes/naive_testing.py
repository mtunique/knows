__author__ = 'mxunique'
# coding: utf-8


from bayes_text import NaiveBayesClassifier
from basic_analyse import *
from std_settings import *


def train():
    nbc = NaiveBayesClassifier()
    nbc.set_tags_list()
    nbc.set_classes_dict()

    nbc.all_in_one_train(src_training_dirpath)


def predict():
    nbc = NaiveBayesClassifier()
    nbc.easy_init()
    for file in get_file_list(src_testing_dirpath):
        print "now predicting %s" % file
        filepath = src_testing_dirpath + "/" + file
        nbc.bayes_classify(doc=filepath)
        print "======================="

def test():
    nbc = NaiveBayesClassifier()
    nbc.easy_init()
    nbc.bayes_classify(string="", screen=True)


if __name__ == '__main__':
    test()
    pass