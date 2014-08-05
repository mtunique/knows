"""
Bayes classification and training core

"""
from __future__ import division

__author__ = 'mxunique'
# coding: utf-8

from std_settings import *
from basic_analyse import *
import json
import codecs
import time


class NaiveBayesClassifier():
    def __init__(self, classes_dict=CLASSES_SET):
        """
        input param:
        tags_list is the vocabulary bag, list of string, no duplicated
        classes_dict is a dict like ==> {'cloud':0.46, 'mobile':0.13, ...}

        attributes:
        freq_dict = {'class1':{'pole':0.25, '': ...}, 'class2':{'pole':0.25, '': ...} ...}
        """

        self.vector_dim = None
        self.vector_list = None
        #store the classes priority probabilities
        self.classes = classes_dict
        self.freq_dict = {}

    def easy_init(self):
        """
        easy simple way to init using default set, for KNOWS only
        """
        self.set_classes_dict()
        self.set_tags_list()
        self.load_from_file()

    def set_classes_dict(self, class_dict=CLASSES_SET):
        """
        input param:
        class_dict is the class set you want to use in the current classification
        initialize with a default SET
        """
        self.vector_list = class_dict

    def set_tags_list(self, tags_list_file=vector_filepath):
        """
        input param:
        tags_list_file is the file path to the items of terms
        initialize with a default file
        """
        self.vector_list = get_tag_list(tags_list_file)
        self.vector_dim = len(self.vector_list)

    def standard_train(self, doc, class_name):
        """
        :param doc: the documents you want to train

        :return: save a dict like ==> {'make':0.34, 'pole':0.25 ...}
        """
        words_list = get_words_list(doc)
        words_dim = len(words_list)

        count_list = {}
        freq_list = {}

        # initialize the counting board with 1 -> Laplace smoothing
        for tag in self.vector_list:
            count_list[tag] = 1

        # start counting the word appeared in the training set
        for wordid in words_list:
            if wordid in count_list.keys():
                count_list[wordid] += 1

        # calculate the P(w|c) = (tf(w,c) + 1) / (|c| + |V|)
        sum_of_all = 0
        for (word, count_num) in count_list.items():
            freq_list[word] = count_num / (self.vector_dim + words_dim)
            sum_of_all += freq_list[word]
        # make the freq to percentage
        for (word, freq) in freq_list.items():
            freq_list[word] = (freq / sum_of_all) * 1000

        try:
            self.freq_dict[class_name] = freq_list
        except Exception, err:
            print "no class_name in the previous settings" + str(err)

    def all_in_one_train(self, dirpath=src_training_dirpath):
        """

        :param dirpath: the directory path your training files lie in
        default as src_training_dirpath
        :return: writing to file
        """

        for classid in self.classes.keys():
            print "now training %s..." % classid
            start = time.clock()
            trainpath = dirpath + '/%s.txt' % classid
            self.standard_train(doc=trainpath, class_name=classid)
            end = time.clock()
            total = end - start
            print "training complete, time costing: " + str(total)
            print "============== COMPLETE ONE =============="

        print "all training complete, now writing to file"
        self._persistance_to_file(self, persis_filepath=tgt_vector_filepath)
        # TODO make graph oh shit!!

    def bayes_classify(self, string=None, doc=None, screen=False):
        """
        classify the docs or strings into a correct class

        :param doc: the file path to the document you want to predict
        :param string: the string you want to predict
        Attention! If string has a value, then the doc value will be ignored
        :param screen: whether to print the result on screen, default is False

        :return: the best match class
        """
        if string is None:
            words_list = get_words_list(doc)
            words_dim = len(words_list)
        else:
            words_list = get_words_list_from_string(string)
            words_dim = len(words_list)

        probability_each_class = {}

        for (class_name, freq_list) in self.freq_dict.items():
            probability_multi = 1

            # experiment
            hit_words_list = []

            for wordid in words_list:
                if wordid in freq_list.keys():
                    probability_multi *= freq_list[wordid]
                    hit_words_list.append(wordid)
                else:
                    # TODO note down the missing word for analyse
                    pass
            probability_each_class[class_name] = probability_multi * self.classes[class_name]

        sort_dict = sorted(probability_each_class.items(), key=lambda x: x[1])
        best_match = sort_dict[sort_dict.__len__() - 1][0]

        if screen:
            print "best match class is => " + best_match
            print "all the probabilities listed as follows:"
            print sort_dict

        return best_match

    def load_from_file(self, load_filepath=tgt_vector_filepath):
        """
        input param:
        tgt_vector_filepath is the trained model file
        """
        self.freq_dict = get_trained_vector_dict(load_filepath)

    @staticmethod
    def _persistance_to_file(self, persis_filepath):
        fd_newfile = codecs.open(persis_filepath, 'w', encoding='utf-8')
        json.dump(self.freq_dict, fd_newfile, indent=4)
        fd_newfile.close()

    @staticmethod
    def trained_number(self):
        print "Trained classes number is: %d  As follows:" % self.freq_dict.__len__()
        print self.freq_dict.keys()


if __name__ == '__main__':
    bayes = NaiveBayesClassifier()
    bayes.load_from_file('source_text/trained_vector.json')
    from dbs.mongodb import db
    from bs4 import BeautifulSoup

    def to_string(content, strip=True):
        return BeautifulSoup(content).html.body.get_text('\n', strip=strip)

    for i in db.article.find({'tag': {'$nin': ['cloud', 'develop', 'prolang', 'systemsecure', 'pm',
                                                     'hardware', 'news', 'viewdesign', 'uidesign', 'appanalyze']}}):
        s_content = db.s_content.find_one({'_id': i['_id']})
        try:
            s_content = s_content['s']
        except Exception:
            s = to_string(db.content.find_one({'_id': i['_id']})['content'])
            db.s_content.update({'_id': i['_id']}, {'$set': {'s': s}}, upsert=True)
            s_content = s
        print 'pre tag', i['_id']
        try:
            print i['tag']
            print type(i['tag'])
            print len(i['tag'])
            print i['tag'] in ['cloud', 'develop', 'prolang', 'systemsecure', 'pm',
                                                     'hardware', 'news', 'viewdesign,', 'uidesign', 'appanalyze']
        except KeyError:
            pass

        tmp = bayes.bayes_classify(s_content.encode('utf-8'))
        print tmp
        print type(tmp)
        db.article.update({'_id': i['_id']},
                                  {'$set': {'tag': tmp}},
                                  )
        print 'now tag', db.article.find_one({'_id': i['_id']})['tag'],'\n'