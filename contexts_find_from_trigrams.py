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
# word_dict = dict(filter(lambda word: word[1] < 5, word_dict.items()))    
# i = 0
# for trig in trigram_dict:
#     left, mid, right = trig
#     if left == 'the' and right == 'of':
#         print(trig, '\t', trigram_dict[trig])
#         i+=1
#     if i > 100:
#         break

contexts_to_words = dict()
words_to_contexts = dict()
context_dict = dict()

# 
for trigram in trigram_dict:
    left_word, mid_word, right_word = trigram[0], trigram[1], trigram[2]
    left_context = '_', mid_word, right_word
    mid_context = left_word, '_', right_word
    right_context = left_word, mid_word, '_'
    temp_context_word_pairs = [(left_context, left_word), (mid_context, mid_word), (right_context, right_word)]
    for context, word in temp_context_word_pairs:
        # if left_word == 'of' and mid_word == 'the':
        #     print(temp_context_word_pairs)
        if context in contexts_to_words:
            if word in contexts_to_words[context]:
                contexts_to_words[context][word] += 1
            else:
                contexts_to_words[context][word] = 1
        else:
            contexts_to_words[context] = dict()
            contexts_to_words[context][word] = 1
        
        if word in words_to_contexts:
            if context in words_to_contexts[word]:
                words_to_contexts[word][context] += 1
                print(word, context, words_to_contexts[word][context])
            else:
                words_to_contexts[word][context] = 1
        else:
            words_to_contexts[word] = dict()
            words_to_contexts[word][context] = 1
        
        if context in context_dict:
            context_dict[context] += 1
        else:
            context_dict[context] = 1

print("Association dicts created...", strftime("%Y-%m-%d %H:%M:%S", gmtime()))
# print("Context dict length:", len(context_dict))
# print("contexts_to_words length:", len(contexts_to_words))
# print("Size of contexts to words:", sys.getsizeof(contexts_to_words))
def find_word_neighbors(word_dict, context_dict, words_to_contexts, contexts_to_words):
    focus_word_key_list = sorted(word_dict.keys(), key = lambda x: word_dict[x], reverse=True)[:1000]
    # focus_word_list = dict(sorted(word_dict.items(), key=operator.itemgetter(1), reverse=True)[:1000])
    words_to_neighbors = dict()
    contexts_to_neighbors = dict()
    word_neighbor_nums = dict()
    context_neighbor_nums = dict()
    word_neighbor_contexts_dict = dict()
    context_neighbor_words_dict = dict()
    print("Neighbor dicts initialized...")
    
    for word in focus_word_key_list:
        temp_contexts = words_to_contexts[word]
        neighbor_count = 0
        word_neighbor_nums[word] = dict()
        word_neighbor_contexts_dict[word] = dict()
        for other_word in focus_word_key_list:
            # word_neighbor_nums[word][other_word] = 0
            if other_word != word:
                for context in words_to_contexts[other_word]:
                    if context in temp_contexts:
                        if other_word not in word_neighbor_nums[word]:
                            word_neighbor_nums[word][other_word] = 0
                        if other_word not in word_neighbor_contexts_dict[word]:
                            word_neighbor_contexts_dict[word][other_word] = dict()
                        neighbor_count += words_to_contexts[other_word][context]
                        word_neighbor_nums[word][other_word] += neighbor_count
                        if context in word_neighbor_contexts_dict[word][other_word]:
                            word_neighbor_contexts_dict[word][other_word][context] += words_to_contexts[other_word][context]
                        else:
                            word_neighbor_contexts_dict[word][other_word][context] = words_to_contexts[other_word][context]
                        neighbor_count = 0
    # for other_word in word_neighbor_nums['the']:
    #     # word_neighbor_nums['the'][other_word] /= float(word_dict['the']) * word_dict[other_word]
    #     print(other_word, file=open("output.txt", "a"))
    #     for context in word_neighbor_contexts_dict['the'][other_word]:
    #         print('\t',context, word_neighbor_contexts_dict['the'][other_word][context], file=open("output.txt", "a"))
    # word_neighbor_nums_list = sorted(word_neighbor_nums.keys(), key=lambda word: word_dict[word])
    print("Word neighbors found...", strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    

    # for contexts, instead of doing contexts_to_words twice, do contexts_to_words to temp_words in words_to_contexts

    # cleans words_to_contexts to free up space
    # del words_to_contexts
    # # temporary 
    # del word_neighbor_contexts_dict
    # for context in contexts_to_words:
    #     temp_words = contexts_to_words[context]
    #     neighbor_count = 0
    #     context_neighbor_nums[context] = dict()
    #     context_neighbor_words_dict[context] = dict()
    #     for other_context in contexts_to_words:
    #         if other_context != context:
    #             for word in contexts_to_words[other_context]:
    #                 if word in temp_words:
    #                     if other_context not in context_neighbor_nums[context]:
    #                         context_neighbor_nums[context][other_context] = 0
    #                     if other_context not in context_neighbor_words_dict[context]:
    #                         context_neighbor_words_dict[context][other_context] = dict()
    #                     neighbor_count += contexts_to_words[other_context][word]
    #                     context_neighbor_nums[context][other_context] += neighbor_count
    #                     if word in context_neighbor_words_dict[context][other_context]:
    #                         context_neighbor_words_dict[context][other_context][word] += 1
    #                     else:
    #                         context_neighbor_words_dict[context][other_context][word] = 1
    #                     neighbor_count = 0
    # print(i)
    # print("Context neighbors found... ", strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    focus_word_neighbor_list = list()
    for word in word_neighbor_nums:
        word_tuple = (word, dict(sorted(word_neighbor_nums[word].items(), key=operator.itemgetter(1), reverse=True)[:10]))
        focus_word_neighbor_list.append(word_tuple)
    focus_word_neighbor_list_sorted = list(sorted(focus_word_neighbor_list, key=lambda word: word_dict[word], reverse=True))[:1000]
    del focus_word_neighbor_list
    focus_context_neighbor_list = list()
    for context in context_neighbor_nums:
        temp_dict = {context : list(sorted(context_neighbor_nums[context].items(), key=operator.itemgetter(1), reverse=True))}
        focus_context_neighbor_list.append(temp_dict)
    focus_context_neighbor_list_sorted = list(sorted(focus_context_neighbor_list, key=lambda context: context_dict[context], reverse=True))[:1000]
    print("Output sorted...", strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    return focus_context_neighbor_list_sorted
    # return 1

# focus_word_neighbors = find_word_neighbors(word_dict, context_dict, words_to_contexts, contexts_to_words)
# focus_word_neighbors_sorted = sorted(focus_word_neighbors, key=lambda inner_tuple: word_dict[inner_tuple[0]], reverse=True)


printed_list = list()
for word, neighbor_dict in focus_word_neighbors_sorted:
    temp_dict = sorted(neighbor_dict.items(), key=lambda inner_tuple: neighbor_dict[inner_tuple[0]], reverse=True)
    printed_list.append((word, temp_dict))
# print(printed_list[0])
# focus_word_list = [word for word, neighbors in focus_word_neighbors]
# # focus_word_list = sorted(focus_word_list, key=lambda word: word_dict[word], reverse=True)
print("Printing to file...")
for word, neighbor_list in printed_list:
    print(word.upper(), file=open("output.txt", "a"))
    for inner_word, count in neighbor_list:
        print('\t','{0:30} {1:30}'.format(inner_word,str(count)), file=open("output.txt", "a"))

for left, mid, right in frequent_context_neighbors:
    upper_context = left.upper(), mid.upper(), right.upper()
    print(upper_context, file=open("output.txt", "a"))
    for other_context in frequent_context_neighbors[left, mid, right]:
        print('\t','{0:30} {1:30d}'.format(str(other_context),frequent_context_neighbors[left, mid, right][other_context]), file=open("output.txt", "a"))