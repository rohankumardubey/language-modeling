# CS 4740 Project 1 Part 2
# 9/25/2015
# qw79, jrl336

from __future__ import division
import nltk, re, pprint
import random
import sys
import pickle
import math

children_bigrams_dict = pickle.load( open( "good_turing_children_bigrams2.p", "rb" ) )
children_unigrams_dict = pickle.load( open( "good_turing_children_unigrams2.p", "rb" ) )
crime_bigrams_dict = pickle.load( open( "good_turing_crime_bigrams2.p", "rb" ) )
crime_unigrams_dict = pickle.load( open( "good_turing_crime_unigrams2.p", "rb" ) )
history_bigrams_dict = pickle.load( open( "good_turing_history_bigrams2.p", "rb" ) )
history_unigrams_dict = pickle.load( open( "good_turing_history_unigrams2.p", "rb" ) )

#Calculate perpleixty using method 2 where unseen words are differentiated from unknown words
def get_perplexity(train_bigrams_dict, train_unigrams_dict, test_corpus):
    f = open(test_corpus)
    raw = f.read()
    mid_raw = unicode(raw, errors='replace')
    new_raw = mid_raw.encode('ascii','ignore')
    tokens = nltk.word_tokenize(new_raw)

    #Computer probability of unseen bigrams
    total = 0
    for bi in train_bigrams_dict:
        total += train_bigrams_dict[bi]
    prob_unseen_bigram = train_bigrams_dict.get(('unseen', 'unseen')) / total
    
    prob = 0
    for i in range(0, len(tokens)-1):
        count_tokeni = 0
        if(not train_unigrams_dict.has_key(tokens[i])):
            tokens[i] = 'unk'
        if(not train_unigrams_dict.has_key(tokens[i+1])):
            tokens[i+1] = 'unk'
        if ((tokens[i], tokens[i+1]) in train_bigrams_dict):
            bigram_count = train_bigrams_dict.get((tokens[i], tokens[i+1]))
            count_tokeni = train_unigrams_dict.get(tokens[i])
            prob = prob - math.log((bigram_count / count_tokeni))
        elif ((train_unigrams_dict.has_key(tokens[i]) and train_unigrams_dict.has_key(tokens[i+1])) and
            (train_unigrams_dict.has_key(tokens[i]) and tokens[i+1]=='unk') and
            train_unigrams_dict.has_key(tokens[i+1]) and tokens[i]=='unk'):
            prob = prob - math.log((prob_unseen_bigram))
        
    return math.exp(1/len(tokens) * prob) #not doing exp to avoid exlopsion

#Calculate perpleixty using method 1 where unseen words are considered the same as unknown words
def get_perplexity2(train_bigrams_dict, train_unigrams_dict, test_corpus):
    f = open(test_corpus)
    raw = f.read()
    mid_raw = unicode(raw, errors='replace')
    new_raw = mid_raw.encode('ascii','ignore')
    tokens = nltk.word_tokenize(new_raw)

    prob = 0
    for i in range(0, len(tokens)-1):
        count_tokeni = 0
        if ((tokens[i], tokens[i+1]) in train_bigrams_dict):
            bigram_count = train_bigrams_dict.get((tokens[i], tokens[i+1]))
            count_tokeni = train_unigrams_dict.get(tokens[i])
        else:
            bigram_count = train_bigrams_dict.get(('unk', 'unk'))
            count_tokeni = train_unigrams_dict.get('unk')
        prob = prob - math.log((bigram_count / count_tokeni))
    return math.exp(1/len(tokens) * prob) #not doing exp to avoid exlopsion


#Use perplexity calculated using method 2 to do genre classification
def genre_classification():
    per_children = get_perplexity(children_bigrams_dict, children_unigrams_dict, 'books/test_books/history/bacon.txt')
    per_crime = get_perplexity(crime_bigrams_dict, crime_unigrams_dict, 'books/test_books/history/bacon.txt')
    per_history = get_perplexity(history_bigrams_dict, history_unigrams_dict, 'books/test_books/history/bacon.txt')
    best_perplexity = min(per_children, per_crime, per_history)
    if (best_perplexity == per_children): print 'children'
    if (best_perplexity == per_crime): print 'crime'
    if (best_perplexity == per_history): print 'history'
    
    print per_children
    print per_crime
    print per_history
    
genre_classification()
