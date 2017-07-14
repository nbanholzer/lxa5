import sys
import re
import operator
from time import gmtime, strftime

# initializes dictionaries
word_dict = dict()
trigram_dict = dict()
print("Program starting...", strftime("%Y-%m-%d %H:%M:%S", gmtime()))
# opens file for reading
with open(sys.argv[1], 'r') as f:
    start = True
    # initializes variables for end of line saves
    word_save_left = '_'
    word_save_mid = '_'
    # reads in first line
    for line in f:
        if line[0] == '#':
            continue
        # processes lines, tokenizes and converts to lower case
        line_tokenized = re.findall(r"[\w']+|[.,!?;\n]", line)
        line_case_sensitive = list(filter(lambda word: word != '\n', line_tokenized))
        del line_tokenized
        line_into_words = [word.lower() for word in line_case_sensitive]
        del line_case_sensitive
        # checks if it is the first line so it can initialize dictionaries with first words
        if start and len(line_into_words) > 2:
            try:
                word_dict[line_into_words[0]] += 1
            except:
                word_dict[line_into_words[0]] = 1
            if line_into_words[1] in word_dict:
                word_dict[line_into_words[1]] += 1
            else:
                word_dict[line_into_words[1]] = 1
            start = False
        
        line_len = len(line_into_words)
        # checks if any words were saved, only fails on first line
        if word_save_left != '_' and line_len > 2:
            left_word = word_save_left
            mid_word = word_save_mid
            right_word = line_into_words[0]
            trigram = left_word, mid_word, right_word
            if trigram in trigram_dict:
                trigram_dict[trigram] += 1
            else:
                trigram_dict[trigram] = 1
            if right_word in word_dict:
                word_dict[right_word] += 1
            else: 
                word_dict[right_word] = 1
            left_word = word_save_mid
            mid_word = line_into_words[0]
            right_word = line_into_words[1]
            trigram = left_word, mid_word, right_word
            if trigram in trigram_dict:
                trigram_dict[trigram] += 1
            else:
                trigram_dict[trigram] = 1
            if right_word in word_dict:
                word_dict[right_word] += 1
            else: 
                word_dict[right_word] = 1
        # reads in words and trigrams
        for ind in range(2, line_len):            
            left_word, mid_word, right_word = line_into_words[ind - 2], line_into_words[ind - 1], line_into_words[ind]
            trigram = left_word, mid_word, right_word
            if trigram in trigram_dict:
                trigram_dict[trigram] += 1
                # print('inc trig')
            else: 
                trigram_dict[trigram] = 1
            
            if right_word in word_dict:
                word_dict[right_word] += 1
            else:
                word_dict[right_word] = 1
        # saves words for next line
        word_save_left, word_save_mid = line_into_words[line_len - 2], line_into_words[line_len - 1]

print("Word and context dict created...")
print("Total length:", len(trigram_dict))
trigram_dict = dict(filter(lambda trig: trig[1] >= 2, trigram_dict.items()))
print("Filtered length:", len(trigram_dict))
print("Trigram dict filtered...", strftime("%Y-%m-%d %H:%M:%S", gmtime()))



# sanity check 1
# print('TRIGRAMS',dict(sorted(trigram_dict.items(), key=operator.itemgetter(1),reverse=True)[:10]))

contexts_to_words = dict()
words_to_contexts = dict()
context_dict = dict()

check_list = list()

for trigram in trigram_dict:
    left_word, mid_word, right_word = trigram[0], trigram[1], trigram[2]
    left_context = '_', mid_word, right_word
    mid_context = left_word, '_', right_word
    right_context = left_word, mid_word, '_'
    if (left_word == 'the' or left_word == 'a') and right_word == 'of':
        check_list.append((mid_word, left_word))
    temp_context_word_pairs = [(left_context, left_word), (mid_context, mid_word), (right_context, right_word)]
    for context, word in temp_context_word_pairs:
        if context in contexts_to_words:
            if word in contexts_to_words[context]:
                contexts_to_words[context][word] += trigram_dict[trigram]
            else:
                contexts_to_words[context][word] = trigram_dict[trigram]
        else:
            contexts_to_words[context] = dict()
            contexts_to_words[context][word] = trigram_dict[trigram]
        
        if word in words_to_contexts:
            if context in words_to_contexts[word]:
                words_to_contexts[word][context] += trigram_dict[trigram]
                # print(word, context, words_to_contexts[word][context])
            else:
                words_to_contexts[word][context] = trigram_dict[trigram]
        else:
            words_to_contexts[word] = dict()
            words_to_contexts[word][context] = trigram_dict[trigram]
        
        if context in context_dict:
            context_dict[context] += trigram_dict[trigram]
        else:
            context_dict[context] = trigram_dict[trigram]


# sanity check 2
print('CORINTHIAN')
print('\t', words_to_contexts['corinthian'])
# print('CONTEXTS',dict(sorted(context_dict.items(), key=operator.itemgetter(1),reverse=True)[:10]))
# print('WORDS',dict(sorted(word_dict.items(), key=operator.itemgetter(1),reverse=True)[:10]))
# print(words_to_contexts['the'])
# print(dict(sorted(words_to_contexts['there'].items(), key=operator.itemgetter(1), reverse=True)[:10]))
# print(dict(sorted(words_to_contexts['the'].items(), key=operator.itemgetter(1), reverse=True)[:10]))
# a_count = 0
# there_count = 0
# she_count = 0
# for context in words_to_contexts['the']:
#     if context in words_to_contexts['of']:
#         a_count += words_to_contexts['of'][context] + words_to_contexts['the'][context]
#     if context in words_to_contexts['there']:
#         there_count += words_to_contexts['there'][context] + words_to_contexts['the'][context]
#     if context in words_to_contexts['she']:
#         she_count += words_to_contexts['she'][context] + words_to_contexts['the'][context]
# print('OF', a_count, a_count / float(word_dict['of'] * word_dict['the']))
# print('SHE', she_count, she_count / float(word_dict['she'] * word_dict['the']))
# print('THERE', there_count, there_count / float(word_dict['there'] * word_dict['the']))

print("Association dicts created...", strftime("%Y-%m-%d %H:%M:%S", gmtime()))


def find_word_neighbors(word_dict, context_dict, words_to_contexts, contexts_to_words):
    focus_word_key_list = sorted(words_to_contexts.keys(), key = lambda x: word_dict[x], reverse=True)[:1000]
    words_to_neighbors = dict()
    contexts_to_neighbors = dict()
    word_neighbor_nums = dict()
    context_neighbor_nums = dict()

    print("Neighbor dicts initialized...")

    for word in focus_word_key_list:
        temp_contexts = words_to_contexts[word]
        word_neighbor_nums[word] = dict()
        for context in temp_contexts:
            temp_word_counts = contexts_to_words[context]
            for other_word in temp_word_counts:
                if other_word not in word_neighbor_nums:
                    if other_word != word:
                        word_count = contexts_to_words[context][word]
                        other_word_count = contexts_to_words[context][other_word]
                        word_neighbor_nums[word][other_word] = (word_count + other_word_count) #\
                            #/ float(word_dict[word] * word_dict[other_word])

    print("Word neighbors found...", strftime("%Y-%m-%d %H:%M:%S", gmtime()))

    # for context in contexts_to_words: 
    #     temp_words = contexts_to_words[context]
    #     context_neighbor_nums[context] = dict()
    #     for word in temp_words:
    #         temp_context_counts = words_to_contexts[word]
    #         for other_context in temp_context_counts:
    #             if other_context not in context_neighbor_nums:
    #                 if other_context != context:
    #                     context_count = words_to_contexts[word][context]
    #                     other_context_count = words_to_contexts[word][other_context]
    #                     context_neighbor_nums[context][other_context] = (context_count + other_context_count) #\
    #                         #/ float(context_dict[context] * context_dict[other_context])

    # print("Context neighbors found...", strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    # print()
    # focus_word_neighbor_list = list()
    for word in word_neighbor_nums:
        word_tuple = (word, dict(sorted(word_neighbor_nums[word].items(), key=operator.itemgetter(1), reverse=True)[:10]))
        if word == 'the':
            print(word_tuple)
    #     focus_word_neighbor_list.append(word_tuple)
    # focus_word_neighbor_list_sorted = focus_word_neighbor_list
    # del focus_word_neighbor_list

    # focus_context_neighbor_list = list()
    # for context in context_neighbor_nums:
    #     context_tuple = (context, dict(sorted(context_neighbor_nums.items(), key=operator.itemgetter(1), reverse=True)[:10]))
    #     focus_context_neighbor_list.append(context_tuple)
    # focus_context_neighbor_list_sorted = list(sorted(focus_context_neighbor_list, key=lambda context: context_dict[context]))
    # del focus_context_neighbor_list
    # print("Outputs sorted...", strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    # return focus_word_neighbor_list_sorted, focus_context_neighbor_list_sorted
    # return word_neighbor_nums, context_neighbor_nums
    return 1, 2

# word_neighbor_list, context_neighbor_list = find_word_neighbors(word_dict, context_dict, words_to_contexts, contexts_to_words)
# print(word_neighbor_list['the'])


# formatted_word_neighbors = list()
# for word, neighbor_dict in word_neighbor_list:
#     temp_dict = sorted(neighbor_dict.items(), key=lambda inner_tuple: neighbor_dict[inner_tuple[0]], reverse=True)
#     formatted_word_neighbors.append((word, temp_dict))

# del word_neighbor_list
# del words_to_contexts
# del word_dict

# formatted_context_neighbors = list()
# for context, neighbor_dict in context_neighbor_list:
#     temp_dict = sorted(neighbor_dict.items(), key=lambda inner_tuple: neighbor_dict[inner_tuple[0]], reverse=True)
#     formatted_context_neighbors.append((context, temp_dict))

# del context_neighbor_list
# del contexts_to_words
# del context_dict

# print("Printing to file...")

# for word, neighbor_list in formatted_word_neighbors:
#     print(word.upper(), file=open("output.txt", "a"))
#     for inner_word, count in neighbor_list:
#         print('\t','{0:30} {1:30}'.format(inner_word,str(count)), file=open("output.txt", "a"))

# for context, neighbor_list in formatted_context_neighbors:
#     print(map(str.upper, context), file=open("output.txt", "a"))
#     for inner_context, count in neighbor_list:
#         print('\t','{0:30} {1:30}'.format(inner_context, str(count)), file=open("output.txt", "a"))