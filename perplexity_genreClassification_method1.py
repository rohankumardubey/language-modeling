# CS 4740 Project 1 Part 2
# 9/25/2015
# qw79, jrl336

from __future__ import division
import nltk, re, pprint
import random
import sys
import pickle
import math

children_bigrams_dict = pickle.load( open( "good_turing_children_bigrams.p", "rb" ) )
children_unigrams_dict = pickle.load( open( "good_turing_children_unigrams.p", "rb" ) )
crime_bigrams_dict = pickle.load( open( "good_turing_crime_bigrams.p", "rb" ) )
crime_unigrams_dict = pickle.load( open( "good_turing_crime_unigrams.p", "rb" ) )
history_bigrams_dict = pickle.load( open( "good_turing_history_bigrams.p", "rb" ) )
history_unigrams_dict = pickle.load( open( "good_turing_history_unigrams.p", "rb" ) )


def get_perplexity(train_bigrams_dict, train_unigrams_dict, test_corpus):
    f = open(test_corpus)
    raw = f.read()
    mid_raw = unicode(raw, errors='replace')
    new_raw = mid_raw.encode('ascii','ignore')
    tokens = nltk.word_tokenize(new_raw)
    
    total = 0
    for bi in train_bigrams_dict:
        total += train_bigrams_dict[bi]
    prob_unseen_bigram = train_bigrams_dict.get(('unk', 'unk')) / total

    prob = 0
    for i in range(0, len(tokens)-1):
        count_tokeni = 0
        if ((tokens[i], tokens[i+1]) in train_bigrams_dict):
            bigram_count = train_bigrams_dict.get((tokens[i], tokens[i+1]))
            count_tokeni = train_unigrams_dict.get(tokens[i])
            prob = prob - math.log((bigram_count / count_tokeni))
        else:
            prob = prob - math.log(prob_unseen_bigram)
    return math.exps(1/len(tokens) * prob)


def genre_classification():
    per_children = get_perplexity(children_bigrams_dict, children_unigrams_dict, 'books/test_books/children/the_magic_city.txt')
    per_crime = get_perplexity(crime_bigrams_dict, crime_unigrams_dict, 'books/test_books/children/the_magic_city.txt')
    per_history = get_perplexity(history_bigrams_dict, history_unigrams_dict, 'books/test_books/children/the_magic_city.txt')
    best_perplexity = min(per_children, per_crime, per_history)
    if (best_perplexity == per_children): print 'children'
    if (best_perplexity == per_crime): print 'crime'
    if (best_perplexity == per_history): print 'history'
    
    print per_children
    print per_crime
    print per_history
    
genre_classification()
