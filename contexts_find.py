# import codecs
# import os
import re
import sys
# import string
import operator
# mywords=dict()
# from math import sqrt
# from  collections import defaultdict 
# import numpy 
# from numpy import *

if len(sys.argv) != 2:
    print("Incorrect number of inputs...")

# reads in file and converts to a properly formatted list
input_corpus = open(sys.argv[1], 'r')
corpus_string = input_corpus.read()
corpus_tokenized = re.findall(r"[\w']+|[.,!?;\n]", corpus_string)
corpus_into_words_case_sensitive = list(filter(lambda word: word != '\n', corpus_tokenized))
corpus_into_words = [word.lower() for word in corpus_into_words_case_sensitive]
del corpus_tokenized
del corpus_string

word_dict = dict()
context_dict = dict()
contexts_to_words = dict()
words_to_contexts = dict()

# inputs first two words into word dictionary for ease of coding
word_dict[corpus_into_words[0]] = 1
if corpus_into_words[1] in word_dict:
    word_dict[corpus_into_words[1]] += 1
else:
    word_dict[corpus_into_words[1]] = 1

for ind in range(2, len(corpus_into_words)):
    left_word, mid_word, right_word = corpus_into_words[ind - 2], corpus_into_words[ind - 1], corpus_into_words[ind]
    # building a dictionary of all the words in the corpus -- first two words already inputted
    if right_word in word_dict:
        word_dict[right_word] += 1
    else:
        word_dict[right_word] = 1
    # finds left, middle, and right trigrams
    left_context = '_', mid_word, right_word
    mid_context = left_word, '_', right_word
    right_context = left_word, mid_word, '_'
    if left_context in context_dict:
        context_dict[left_context] += 1
    else:
        context_dict[left_context] = 1

    if mid_context in context_dict:
        context_dict[mid_context] += 1
    else:
        context_dict[mid_context] = 1
    
    if right_context in context_dict:
        context_dict[right_context] += 1
    else: 
        context_dict[right_context] = 1

    key_word = [(left_context, left_word), (mid_context, mid_word), (right_context,right_word)]
    # inputs contexts into dict and for each context stores dict of words present
    for key, word in key_word:
        if key in contexts_to_words:
            words_in_context = contexts_to_words.get(key)
            if word in words_in_context:
                words_in_context[word] += 1
            else:
                words_in_context[word] = 1
        else:
            contexts_to_words[key] = dict()
            contexts_to_words[key].update({word : 1})
    # inputs words into dict and for each word stores dict of contexts present
    for key, word in key_word:
        if word in words_to_contexts:
            contexts_in_word = words_to_contexts.get(word)
            if key in contexts_in_word:
                contexts_in_word[key] += 1
            else:
                contexts_in_word[key] = 1
        else:
            words_to_contexts[word] = dict()
            words_to_contexts[word].update({key : 1})


# print functions useful for displaying dictionaries above
# for word in words_to_contexts:
#     print(word)
#     for contexts in words_to_contexts[word]:
#         print(contexts, ':', words_to_contexts[word][contexts])
#     print('\n')

# print('\n\n\n')
# for context in contexts_to_words:
#     print(context)
#     for words in contexts_to_words[context]:
#         print(words, ':', contexts_to_words[context][words])
#     print('\n')

# for word in word_dict:
#     print(word, ':', word_dict[word])

top_words = dict()
top_contexts = dict()
focus_word_dict = dict(sorted(word_dict.items(), key=operator.itemgetter(1), reverse=True)[:10])
focus_context_dict = dict(sorted(context_dict.items(), key=operator.itemgetter(1), reverse=True)[:10])
for word in focus_word_dict:
    top_contexts = dict(sorted(words_to_contexts[word].items(), key=operator.itemgetter(1), reverse=True)[:10])
    print(word)
    print(top_contexts)
print('\n')
for context in focus_context_dict:
    top_words = dict(sorted(contexts_to_words[context].items(), key=operator.itemgetter(1), reverse=True)[:10])
    print(context)
    print(top_words)

def find_neighbors(word_dict, context_dict, contexts_to_words, words_to_contexts):
    # temp_word_dict = word_dict()
    focus_word_dict = dict(sorted(word_dict.items(), key=operator.itemgetter(1), reverse=True)[:10])
    focus_context_dict = dict(sorted(context_dict.items(), key=operator.itemgetter(1), reverse=True)[:10])
    words_to_neighbors = dict()
    contexts_to_neighbors = dict()
    word_neighbor_nums = dict()
    context_neighbor_nums = dict()
    for word in focus_word_dict:
        temp_contexts = words_to_contexts[word]
        neighbor_count = 0
        word_neighbor_nums[word] = dict()
        for other_word in words_to_contexts:
            if other_word != word:
                for context in words_to_contexts[other_word]:
                    if context in temp_contexts:
                        neighbor_count += words_to_contexts[other_word][context]
                        word_neighbor_nums[word][other_word] = neighbor_count
                        neighbor_count = 0
                
    
    for context in focus_context_dict:
        temp_words = contexts_to_words[context]
        neighbor_count = 0
        context_neighbor_nums[context] = dict()
        for other_context in contexts_to_words:
            if other_context != context:
                for word in contexts_to_words[other_context]:
                    if word in temp_contexts:
                        neighbor_count += contexts_to_words[other_context][word]
                        context_neighbor_nums[context][other_context] = neighbor_count
                        neighbor_count = 0
    # frequent_word_neighbors = dict(sorted(word_neighbor_nums.items(), key=operator.itemgetter(1), reverse=True)[:10])
    # frequent_context_neighbors = dict(sorted(context_neighbor_nums.items(), key=operator.itemgetter(1), reverse=True)[:10])
    frequent_word_neighbors = dict()
    frequent_context_neighbors = dict()
    for word in focus_word_dict:
        frequent_word_neighbors[word] = dict()
        frequent_word_neighbors[word] = dict(sorted(word_neighbor_nums[word].items(), key=operator.itemgetter(1), reverse=True)[:10])
    for context in focus_context_dict:
        frequent_context_neighbors[context] = dict()
        frequent_context_neighbors[context] = dict(sorted(context_neighbor_nums[context].items(), key=operator.itemgetter(1), reverse=True)[:10])
    return frequent_word_neighbors, frequent_context_neighbors

# frequent_word_neighbors, frequent_context_neighbors = find_neighbors(word_dict, context_dict, contexts_to_words, words_to_contexts)
# for word in frequent_word_neighbors:
#     print(word)
#     for other_word in frequent_word_neighbors[word]:
#         print(other_word, ':', frequent_word_neighbors[word][other_word])
#     print('\n')
