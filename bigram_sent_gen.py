# CS 4740 Project 1
# 9/10/2015
# qw79, jrl336

#USAGE: python part1.py [sentence seed]

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
all_counts = sum(all_pairs.values()) #total no. of seen bigrams

#generate a random start word
def generate_seed():
    rand = random.uniform(0, all_counts)
    counter = 0.0
    for i in all_pairs_sorted:
        if ( (rand <= counter + i[1] ) & (rand > counter) ):
            return i[0]
        counter += i[1]
    return ''

seed = generate_seed()

#Create hashtable of bigram and counts
def make_hashtable():
    hash_tokens = dict()
    for i in range(0, len(tokens) - 1):
        if ( hash_tokens.has_key( (tokens[i], tokens[i+1])) ):
            hash_tokens[ (tokens[i], tokens[i+1])] += 1
        else:
            hash_tokens[(tokens[i], tokens[i+1])] = 1
    return hash_tokens

#dicionary of all bigrams only with count >=1
bigrams_dict = make_hashtable()

#Generate next word based on bigrams
def generate_next(given_word):
    temp_list = []
    for key,value in bigrams_dict.iteritems():
        if (given_word == key[0]):
            temp_list.append((key[1], value))
    
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
    word = spliced_sentence[len(spliced_sentence) - 1] 
    prev_word = word
    for i in range(0, length):
        prev_word = generate_next(prev_word)
        given_sentence = given_sentence + ' ' + prev_word
    return given_sentence

#Generate sentence without given seed
def generate_sentence_without_seed(length):
    word = generate_seed()
    return generate_sentence_with_seed(word, length)
    
#Script starts
#print sentence with given seed to console

print("Sentence with given seed:")
print(generate_sentence_with_seed(sys.argv[1], 15))
 
#print sentence without seed to console
print("Sentence without seed:")
print(generate_sentence_without_seed(15))
