def get_dict(wordlist, trigram_to_freq):
    worddict = {word: wordlist.index(word) for word in wordlist}

    trigram_to_freq_sorted = [(trigram, freq) for trigram, freq in
                              double_sorted(trigram_to_freq.items(),
                                            key=lambda x: x[1],
                                            reverse=True) if
                              freq >= min_context_count]

    word_context_dict = dict()
    for trigram, freq in trigram_to_freq:
        word1, word2, word3 = trigram

        left_context  = ('_', word2, word3)
        mid_context   = (word1, '_', word3)
        right_context = (word1, word2, '_')
        
        word_context_dict[word1] = left_context
        word_context_dict[word2] = mid_context
        word_context_dict[word3] = right_context

