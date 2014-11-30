'''
Created on Nov 27, 2014

@author: Ben Athiwaratkun (pa338)

This files creates a dictionary of n-gram (1-,2-,3- grams) that 
occur in code-switching versus non-code switching instance.

1. Count the number of instances the n-gram occurs in CS
2. Count the number of instances the n-gram occurs in non-CS
Format:

key=n-gram, value={cs:10, non-cs:25}

Then filter out only n-gram that are frequent enough.

Save result to pickle file.
'''
#from __future__ import division
#import numpy as np
#import enchant
import langid
import pickle
#import regex as re
import re
import os
import json

def buildNgramDict(listFileNames):
    # Format: key = n-gram
    # value = {freq-cs: , freq-non-cs:}
    dict_cs = {}
    dict_ngram = {}
    numLine = -1
    fout = open('../Data/process3/process3.txt','wb')
    for fname in listFileNames:
        f = open(fname, 'rb')
        for line in f:
            numLine += 1
            print 'Process Line %d' % numLine
            _d = json.loads(line) # key: cs-word-list and text-list
            ''' 1. add cs to dict_cs '''
            if len(_d['cs-word-list']) > 0:
                for word in _d['cs-word-list']:
                    if word in dict_cs:
                        dict_cs[word] += 1
                    else:
                        dict_cs[word] = 1
            ''' 2. add n-gram to dict_ngram. Choose 1-,2-,3- grams'''
            text_list = _d['text-list']
            # Exclude anything English. have to be careful about symbols
            # Regular expression for Thai?
            lang_list = [langid.classify(word)[0] for word in text_list]
            #####for text,lang in zip(text_list, lang_list):
            #####    print 'Text:%s \tLang:%s' % (text, lang)
            
            new_text_list = [] # This is a list of list
            index_tList = 0
            new_text_list.append([])
            for i in range(len(text_list)):
                if lang_list[i] == 'th':
                    new_text_list[index_tList].append(text_list[i])
                else:
                    index_tList += 1
                    new_text_list.append([])
            
            #print new_text_list
            new_text_list_nonEmpty = [list for list in new_text_list if len(list) > 0]
            #print new_text_list_nonEmpty
            #print new_text_list_nonEmpty
            listNgrams = getListNgrams(new_text_list_nonEmpty)
            #print listNgrams
            
            isCS = len(_d['cs-word-list']) > 0
            for ngram in listNgrams:
                if not ngram in dict_ngram:
                    dict_ngram[ngram] = {'cs':0,'non-cs':0}
                # Record if it's CS or not
                if isCS:
                    dict_ngram[ngram]['cs'] += 1
                else:
                    dict_ngram[ngram]['non-cs'] += 1
            _d['lang-list'] = lang_list
            _d['ngram-list'] = listNgrams
            fout.write(json.dumps(_d))
            fout.write('\n')
            
            ''' DEBUG '''
            #if numLine > 1000:
            #    break
    print 'The number of Distinct CS=\t%r' % len(dict_cs.keys())
    print 'The Number of Distinct N-Gram=\t%r' % len(dict_ngram.keys())
    pickle.dump(dict_cs, open('../Data/process3/dict_cs.p', 'wb'))
    pickle.dump(dict_ngram, open('../Data/process3/dict_ngram.p', 'wb'))
    '''Next: filter out only keys that are frequent enough '''

def getListNgrams(list_thai_words, n=2):
    
    listNgrams = []
    for sub_list in list_thai_words:
        for index in range(len(sub_list) - n + 1): 
            listNgrams.append(' '.join(sub_list[index:index+n]))
    return listNgrams
    

def regExpAlphaNumeric(text):
    re.search(r'[a-zA-Z0-9_]*',text)

def getListInputFiles(dir='../Data/process2/'):
    _listFiles = os.listdir(dir)
    for i in range(len(_listFiles)):
        _listFiles[i] = os.path.join(dir, _listFiles[i])
    return _listFiles

def testRegExpThai(text):
    re.search(u'\p{Thai}+', text)

def testRegExpNonEnglish():
    re.search(u'[^\x00-\x7F]+')

def main():
    list_inputFiles = ['../Data/process2/process2_part2.txt']
    buildNgramDict(list_inputFiles)
    
if __name__ == "__main__":
    main()