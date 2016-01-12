# CS 4740 Project 1 Part 2
# 9/25/2015
# qw79, jrl336

#USAGE: Good Turing Smoothing

from __future__ import division
import nltk, re, pprint
import random
import sys
import pickle

#Preprocessing
f = open('books/train_books/history/aggregated_history_train.txt')
raw = f.read()
mid_raw = unicode(raw, errors='replace')
new_raw = mid_raw.encode('ascii','ignore')

#deliminated words in a list
tokens = nltk.word_tokenize(new_raw)
tokenUni = nltk.word_tokenize(new_raw)

def insertUnknowns():
    found = dict()
    for i in range(0,len(tokens)):
        if not found.has_key(tokens[i]):
            found[tokens[i]] = 1
            tokens[i] = 'unk'

insertUnknowns()

#Create hashtable of bigram and counts
def make_hashtable():
    hash_tokens = dict()
    for i in range(0, len(tokens) - 1):
        if ( hash_tokens.has_key( (tokens[i], tokens[i+1])) ):
            hash_tokens[(tokens[i], tokens[i+1])] += 1
        else:
            hash_tokens[(tokens[i], tokens[i+1])] = 1
    return hash_tokens
#dicionary of all bigrams only with count >=1
bigrams_dict = make_hashtable()
#print bigrams_dict


#Assume #seen once bigrams = #unseen bigrams
def get_no_of_seen_once_bigrams():
    counts = 0
    for bi in bigrams_dict:
        if(bigrams_dict.get(bi) == 1):
            counts = counts + 1
    return counts
#print get_no_of_seen_once_bigrams()


def get_no_of_unseen_bigrams():
    seen_bigrams = 0
    for bi in bigrams_dict:
        seen_bigrams += bigrams_dict[bi]
    unseen_bigrams = len(bigrams_dict) * len(bigrams_dict) - seen_bigrams
    return unseen_bigrams
#print get_no_of_unseen_bigrams()


#Compute revised Good-Turing counts for N_0 to N_5
def revise_counts():
    no_of_seen_once_bigrams = get_no_of_seen_once_bigrams()
    no_of_unseen_bigrams = get_no_of_unseen_bigrams()
    adjusted_unseen_bigrams = no_of_seen_once_bigrams / no_of_unseen_bigrams
    new_counts = [adjusted_unseen_bigrams]
    prev_count = no_of_seen_once_bigrams
    for i in range(2,7):
        count = 0
        for bi in bigrams_dict:
            if( bigrams_dict.get(bi) == i):
                count = count + 1
        good_turing_count = i * count / prev_count
        prev_count = count
        #print prev_count #original bigram counts
        new_counts.append(good_turing_count) 
    return new_counts
#print revise_counts()

#print (tokenUni)

#Modify bigrams_dict table with new counts from N_0 to N_5
# def good_turing_bigrams_dict_count():
#     new_counts = revise_counts()
#     for i in range (1,6):
#         for bi in bigrams_dict:
#             if (bigrams_dict.get(bi) == i):
#                 bigrams_dict[bi] = new_counts[i]
#     bigrams_dict[('unk', 'unk')] = new_counts[0]
#     return bigrams_dict
# good_turing_bigrams_dict_count()

def good_turing_bigrams_dict_count2():
    new_counts = revise_counts()
    for i in range (1,6):
        for bi in bigrams_dict:
            if (bigrams_dict.get(bi) == i):
                bigrams_dict[bi] = new_counts[i]
    bigrams_dict[('unseen', 'unseen')] = new_counts[0]
    #return bigrams_dict
good_turing_bigrams_dict_count2()


def make_unigram_table():
    unigram_dict = dict()
    for t in tokenUni:
        if (unigram_dict.has_key(t)):
            unigram_dict[t] = unigram_dict[t] + 1
        else:
            unigram_dict[t] = 1
    return unigram_dict

unigram_dict = make_unigram_table()


def get_seen_once_unigrams():
    count = 0
    for u in unigram_dict:
        if unigram_dict[u] == 1 :
            count += 1
    return count
#print get_seen_once_unigrams()
    
    
def revise_unigram_counts():
    no_of_seen_once_unigrams = get_seen_once_unigrams()
    new_counts = [no_of_seen_once_unigrams]
    prev_count = no_of_seen_once_unigrams
    for i in range(2,7):
        count = 0
        for u in unigram_dict:
            if( unigram_dict.get(u) == i):
                count = count + 1
        good_turing_count = i * count / prev_count
        prev_count = count
        #print prev_count #original bigram counts
        new_counts.append(good_turing_count) 
    return new_counts
#print revise_unigram_counts()


def smooth_unigram_table():
    new_counts = revise_unigram_counts()
    for i in range (1,6):
        for u in unigram_dict:
            if (unigram_dict.get(u) == i):
                unigram_dict[u] = new_counts[i]
    unigram_dict['unk'] = new_counts[0]
    return unigram_dict

unigram_smoothed = smooth_unigram_table()
#print(unigram_smoothed.get('unk'))

#Make pickle files for bigrams and unigrams dictionaries
#pickle.dump(bigrams_dict, open( "good_turing_children_bigrams.p", "wb" ) )
#pickle.dump(unigram_dict, open( "good_turing_children_unigrams.p", "wb" ) )
pickle.dump(bigrams_dict, open( "good_turing_history_bigrams2.p", "wb" ) )
pickle.dump(unigram_dict, open( "good_turing_history_unigrams2.p", "wb" ) )