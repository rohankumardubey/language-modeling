# CS 4740 Project 1 Part 2
# 9/24/2015
# qw79, jrl336

#USAGE: trigram sentence generator

from __future__ import division
import nltk, re, pprint
from collections import Counter
import random
import sys

#Preprocessing
f = open('books/train_books/children/aggregated_children_train.txt')
raw = f.read()
mid_raw = unicode(raw, errors='replace')
new_raw = mid_raw.encode('ascii','ignore')

#deliminated words in a list
tokens = nltk.word_tokenize(new_raw)

#Count occurences of each unique work token
all_pairs = Counter(tokens) #Counter Object
all_pairs_sorted = all_pairs.most_common() #Convert Counter Obj to list
all_counts = sum(all_pairs.values()) #total no. of tokens in the corpus


#Create hashtable of trigram and counts
def make_trigram_hashtable():
    hash_tokens = dict()
    for i in range(0, len(tokens) - 2):
        if ( hash_tokens.has_key( (tokens[i], tokens[i+1], tokens[i+2])) ):
            hash_tokens[ (tokens[i], tokens[i+1], tokens[i+2])] += 1
        else:
            hash_tokens[(tokens[i], tokens[i+1], tokens[i+2])] = 1
    return hash_tokens

trigrams_dict = make_trigram_hashtable()


#Generate next word based on bigrams
def generate_next(given_bigram):
    temp_list = []
    for key,value in trigrams_dict.iteritems():
        if (given_bigram[0] == key[0]) & (given_bigram[1] == key[1]):
            temp_list.append((key[2], value))
    
    total = 0
    for i in temp_list:
        total += i[1]
    
    rand = random.uniform(0, total)
    counter = 0.0
    for j in temp_list:
        if ( (rand <= counter + j[1] ) & (rand > counter) ):
            return j[0]
        counter += j[1]
    return ''

#Generates sentence with given word sequence (given_sentence) of length (length)
def generate_sentence_with_seed(given_sentence, length):
    spliced_sentence = given_sentence.split()
    bigram = ( spliced_sentence[len(spliced_sentence) - 2], spliced_sentence[len(spliced_sentence) - 1] )
    prev_bigram = bigram
    for i in range(0, length):
        next_word = generate_next(prev_bigram)
        given_sentence = given_sentence + ' ' + next_word
        prev_bigram = (prev_bigram[1], next_word)
    return given_sentence

print generate_sentence_with_seed('Every sight he beheld in the heavens', 20)
