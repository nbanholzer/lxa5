import codecs
import os
import sys
import string
import operator
mywords=dict()
from math import sqrt
from  collections import defaultdict 
import numpy
from numpy import *


linecount       = 0
contexts        = dict()
analyzedwordlist    = list()
analyzedworddict    = dict()

LatexFlag = True
unicodeFlag = False
FileEncoding =  "ascii"
 
NumberOfWordsForContext     = 1000 # 40000
NumberOfWordsForAnalysis    = 500 #4000
NumberOfNeighbors       = 9

shortfilename       = "french"
outshortfilename    = "french"
languagename        = "french"
  
datafilelocation =  "../../data/"
  
wordfolder    = datafilelocation + languagename + "/dx1_files/"
trigramfolder = datafilelocation + languagename + "/trig/"
infileTrigramsname = "linguistica/datasets/lxa_outputs/word_trigrams.txt"
outfolder     = datafilelocation + languagename + "/neighbors/"
outfilenameNeighbors    = outfolder + outshortfilename + "_PoS_closest" + "_" + str(NumberOfNeighbors ) + "_neighbors.txt"
outfilenameLatex    = outfolder + outshortfilename + "_latex.tex"
outfilenameContexts     = outfolder + outshortfilename + "_contexts.txt"
 


if unicodeFlag:
    trigramfile         =codecs.open(infileTrigramsname, encoding = FileEncoding)
    wordfile            =codecs.open(infileWordsname, encoding = FileEncoding)
    outfileNeighbors    = codecs.open (outfileneighborsname, "w",encoding = FileEncoding)
     
else:
    outfileNeighbors    = open (outfilenameNeighbors, "w")
    outfileLatex        = open (outfilenameLatex, "w")
    outfileContexts     = open (outfilenameContexts, "w")
 
    wordfile            = open(infileWordsname)
    trigramfile         = open(infileTrigramsname)
 
print ("Language is", languagename, ". File name:", shortfilename, ". Number of words", NumberOfWordsForContext, ".")
 

from_word_to_context = dict()
if 1==1:
    for line in wordfile:
        pieces = line.split()
        print(pieces[0]) 
        if pieces[0] == "#":
            continue
        mywords[pieces[0]] = int(pieces[1])      
    print ("1. Word file is ", infileWordsname )      
    wordfile.close()
    analyzedwordlist = sorted(mywords,key=mywords.__getitem__,reverse=True)
    analyzedwordlist[NumberOfWordsForAnalysis:] = []
    for i in range(NumberOfWordsForAnalysis):
        analyzedworddict[analyzedwordlist[i]] = i
        #from_word_to_context[analyzedwordlist[i]] = dict()
        
      
    print ("2. Reading in trigram file.")
    for line in trigramfile:
        linecount += 1
        line = line.split()
        if line[0] == "#":
            continue
        thesewords = line[0].split("_")
        #print thesewords
 
        focus_word = thesewords[1]
        if focus_word in analyzedworddict:
            context = thesewords[0] + "_" +  thesewords[2]
            if not context in contexts:
                contexts[context] = dict()
            contexts[context][focus_word] = 1
            if not focus_word  in from_word_to_context:
                from_word_to_context[focus_word] = list()
            from_word_to_context[focus_word].append(context)
 
        #Left trigrams
        focus_word = thesewords[0]
        if focus_word in analyzedworddict:
            context = "_" + thesewords[1] + "+" + thesewords[2]
            if not context in contexts:
                contexts[context] = dict()
            contexts[context][focus_word] = 1
            if focus_word not in from_word_to_context:
                from_word_to_context[focus_word] = list()
            from_word_to_context[focus_word].append(context)
 
 
        #Right trigrams
        focus_word = thesewords[2]
        if focus_word in analyzedworddict:  
            context = thesewords[0]  + "+" + thesewords[1] + "_"
            if not context in contexts:
                contexts[context] = dict()
            contexts[context][focus_word] = 1
            if focus_word not in from_word_to_context:
                from_word_to_context[focus_word] = list()
            from_word_to_context[focus_word].append(context)
  
 
contextlist = contexts.keys() 
  
print ("%-50s %3d = number of contexts" % ("3. End of words and counts.", len(contextlist) ) )
 






































def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def get_parameters(filename):
    f = open(filename, "r")
    params = f.read().split("\n")
    return params

def make_array():
    params = get_parameters("param.txt")
    pair_freq = [[0 for i in range(int(float(params[0])))] for j in range(int(float(params[0])))]
    count = 0
    for i in range(len(pair_freq)):
        for j in range(len(pair_freq[0])):
            count += 1
            pair_freq[i][j] = params[count]
    return pair_freq

def read_dict(array, filename):
    word_list = get_parameters(filename)
    for i in range(len(word_list)):
        for j in range(len(word_list)):
            output = '{:10}{:10}{:>30}'.format(word_list[i] + "--", word_list[j] + ":", str(array[i][j]))
            print(output)
    return

# def find_closest(array, input_val, closest_inds):
#     temp_arr = map(filter((lambda x: x not = input_val), array))
    

            

context_array = make_array()
print_array(context_array, "example_words.txt")