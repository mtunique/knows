__author__ = 'mt'
# -*- coding: utf-8 -*-

import numpy, sys
from dbs import mongodb
from pymongo import DESCENDING
import online_ldavb


def main():
    # The number of documents to analyze each iteration
    batch_size = 64
    # The total number of documents in mongodb
    D = mongodb.db.s_content.count()
    # The number of topics
    K = 100

    # How many documents to look at
    if len(sys.argv) < 2:
        documents_size = int(D/batch_size)
    else:
        documents_size = int(sys.argv[1])

    # Our vocabulary
    vocab = file('./dict_nostops.txt').readlines()
    W = len(vocab)

    # Initialize the algorithm with alpha=1/K, eta=1/K, tau_0=1024, kappa=0.7
    old_a = online_ldavb.OnlineLDA(vocab, K, D, 1./K, 1./K, 1024., 0.7)
    # Run until we've seen D documents. (Feel free to interrupt *much*
    # sooner than this.)
    flag = "91111111110"
    for iteration in range(0, documents_size):
        # Download some articles
        l = list(mongodb.db.article.find({"time": {"$lt": flag}}).sort("time", DESCENDING).limit(batch_size))
        if len(l) < batch_size:
            break
        flag = l[-1]['time']

        doc_set = []
        for a in l:
            try:
                doc_set.append(mongodb.db.s_content.find_one({"_id": a['_id']})['s'])
            except Exception as err:
                print a, err.args

        if not doc_set:
            break
        # Give them to online LDA
        (gamma, bound) = old_a.update_lambda(doc_set)
        # Compute an estimate of held-out perplexity
        (word_ids, word_counts) = online_ldavb.parse_doc_list(doc_set, old_a._vocab)
        perwordbound = bound * len(doc_set) / (D * sum(map(sum, word_counts)))
        print '%d:  rho_t = %f,  held-out perplexity estimate = %f' % \
            (iteration, old_a._rhot, numpy.exp(-perwordbound))

        # Save lambda, the parameters to the variational distributions
        # over topics, and gamma, the parameters to the variational
        # distributions over topic weights for the articles analyzed in
        # the last iteration.
        if iteration % 10 == 0:
            numpy.savetxt('lambda-%d.dat' % iteration, old_a._lambda)
            numpy.savetxt('gamma-%d.dat' % iteration, gamma)

    for num in range(len(old_a._lambda)):
        mongodb.db.vector.update({'_id': str(num)}, {'_id': str(num), 'v': list(old_a._lambda[num])}, upsert=True)

if __name__ == '__main__':
    main()