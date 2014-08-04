__author__ = 'mxunique'
# coding: utf-8

CLASSES_SET = {
    'cloud': 0.18,
    'develop': 0.20,
    'prolang': 0.25,
    'systemsecure': 0.15,
    'pm': 0.14,
    'hardware': 0.068,
    'news': 0.157
}

# vector of source and trained
vector_filepath = 'Bayes/source_text/tags_real.txt'
tgt_vector_filepath = 'Bayes/source_text/trained_vector.json'


# ============== DEBUG ONLY =================
#
# training file path, in fact they are list
src_training_dirpath = 'training_file'
# testing classify file dir path, used to get the file list automatically
src_testing_dirpath = 'testing_file'


if __name__ == '__main__':
    pass
