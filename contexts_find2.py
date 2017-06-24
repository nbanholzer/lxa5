import re
import sys
from collections import *
import operator



if len(sys.argv) != 2:
    print("Incorrect number of inputs...")

input_corpus = open(sys.argv[1])


def trigram_split(ind, trigram):
    left, middle, right = trigram
    if ind == 0:
        return left, ('_', middle, right)
    elif ind == 1:
        return middle, (left, '_', right)
    else:
        return right, (left, middle, '_')

def fix_punctuations(line):
    line = line.replace('.', ' . ')
    line = line.replace(',', ' , ')
    line = line.replace(';', ' ; ')
    line = line.replace('!', ' ! ')
    line = line.replace('?', ' ? ')
    line = line.replace(':', ' : ')
    line = line.replace(')', ' ) ')
    line = line.replace('(', ' ( ')
    return re.sub('\s', ' ', line)

def run(input_corpus):

    word_dict = Counter()
    trigrams_counter = Counter()

    current_word_token_count = 0

    for line in input_corpus:
        line = fix_punctuations(line).strip()
        line = line.lower()

        words = line.split()
        if not words:
            continue

        current_word_token_count += len(words)

        words_on_line = words
        trigrams_of_line = zip(*[words[i:] for i in range(3)])

        word_dict.update(words_on_line)
        trigrams_counter.update(trigrams_of_line)

    return dict(word_dict), dict(trigrams_counter)

word_dict, trigrams_counter = run(input_corpus)
word_dict = {word: count for word, count in word_dict.items() if count > 5}
trigrams_counter = {trigram: count for trigram, count in trigrams_counter.items() if count > 5}
# print(trigrams_counter)

context_dict = dict()
words_to_contexts = dict()
contexts_to_words = dict()
# maxim = max(trigrams_counter, key=trigrams_counter.get)
# print(maxim, trigrams_counter[maxim])
for trigram, count in trigrams_counter.items():
    left_word, left_context = trigram_split(0, trigram)
    mid_word, mid_context = trigram_split(1, trigram)
    right_word, right_context = trigram_split(2, trigram)

    if left_context in context_dict:
        context_dict[left_context] += count
    else:
        context_dict[left_context] = count

    if mid_context in context_dict:
        context_dict[mid_context] += count
    else:
        context_dict[mid_context] = count
    
    if right_context in context_dict:
        context_dict[right_context] += count
    else: 
        context_dict[right_context] = count

    key_word = [(left_context, left_word), (mid_context, mid_word), (right_context,right_word)]
    # inputs contexts into dict and for each context stores dict of words present
    for key, word in key_word:
        if key in contexts_to_words:
            words_in_context = contexts_to_words.get(key)
            if word in words_in_context:
                words_in_context[word] += count
            else:
                words_in_context[word] = count
        else:
            contexts_to_words[key] = dict()
            contexts_to_words[key].update({word : count})
    # inputs words into dict and for each word stores dict of contexts present
    for key, word in key_word:
        if word in words_to_contexts:
            contexts_in_word = words_to_contexts.get(word)
            if key in contexts_in_word:
                contexts_in_word[key] += count
            else:
                contexts_in_word[key] = count
        else:
            words_to_contexts[word] = dict()
            words_to_contexts[word].update({key : count})


top_words = dict()
top_contexts = dict()
# focus_word_dict = dict(sorted(word_dict.items(), key=operator.itemgetter(1), reverse=True)[:10])
# print(focus_word_dict)
# focus_context_dict = dict(sorted(context_dict.items(), key=operator.itemgetter(1), reverse=True)[:10])
# print(focus_context_dict)
# for word in focus_word_dict:
#     top_contexts = dict(sorted(words_to_contexts[word].items(), key=operator.itemgetter(1), reverse=True)[:10])
#     print(word)
#     print(top_contexts)
# print('\n')
# for context in focus_context_dict:
#     top_words = dict(sorted(contexts_to_words[context].items(), key=operator.itemgetter(1), reverse=True)[:10])
#     print(context)
#     print(top_words)

# maxim = max(words_to_contexts['the'], key=words_to_contexts['the'].get)
# print(maxim, words_to_contexts['the'][maxim])

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
    # return word_neighbor_nums, context_neighbor_nums

frequent_word_neighbors, frequent_context_neighbors = find_neighbors(word_dict, context_dict, contexts_to_words, words_to_contexts)
# maxim = max(frequent_word_neighbors['the'], key=frequent_word_neighbors['the'].get)
# print(maxim, frequent_word_neighbors['the'][maxim])
for word in frequent_word_neighbors:
    print(word.upper())
    for other_word in frequent_word_neighbors[word]:
        print(other_word, ':', frequent_word_neighbors[word][other_word])
    print('\n')
# print(frequent_word_neighbors)
# print(frequent_context_neighbors)