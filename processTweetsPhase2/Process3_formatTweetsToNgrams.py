'''
Created on Nov 27, 2014

@author: Ben Athiwaratkun (pa338)

This files creates a dictionary of n-gram (1-,2-,3- grams) that 
occur in code-switching versus non-code switching instance

'''
#from __future__ import division
#import numpy as np
import enchant
import langid
import pickle
import re
import os

def getNgrams(listFileNames):
    # Format: key = n-gram
    # value = {freq-cs: , freq-non-cs:}
    di = {}
    for fname in listFileNames:
        f = open(fname, 'rb')
        for line in f:
            listWords_original = line.split('\t')
            #for n in [1,2,3]:

def isCodeSwitching():
    ''' 1. For now, only consider lone word
        2. Use the POS Tagger for English Word
    '''
    
    pass

def getListInputFiles(dir='../Data/SegmentedTweets'):
    _listFiles = os.listdir(dir)
    for i in range(len(_listFiles)):
        _listFiles[i] = os.path.join(dir, _listFiles[i])
    return _listFiles

def main():
    list_inputFiles = getListInputFiles()
    
    
if __name__ == "__main__":
    main()