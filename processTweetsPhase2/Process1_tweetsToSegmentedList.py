# -*- coding: utf-8 -*-
'''
Created on Nov 27, 2014

@author: Ben Athiwaratkun (pa338)

This file is part of a pre-process:
Input: Tweet in the form of json object per line (in many files and many folders)

Output: Text of tweet that are segmented, each token separated by tab


Note: This file needs 'pythai', a python library, and 'libthai' which is a C-library. 
This file is run on Ubuntu 13.01 (not compatible with 14.04 or OS X 10.10 for some mysterious reason)
'''

#from __future__ import division
#import numpy as np
import os
import pickle
import langid
import json
import re
import pythai

# Default folder is ThaiBatch1
def convertTweetToSegmentedText(listFileNames):
    segmentedWordsPath = '../Data/SegmentedTweets/'
    numTweets = 0
    for fname in listFileNames:
        if not '.txt' in fname: 
            continue
        
        fout_name_m = re.search(r'[/]([\w]*).txt',fname)
        fout_name =  fout_name_m.group(1)
        fout_name_full = os.path.join(segmentedWordsPath, fout_name + '_SEG.txt')
        fout = open(fout_name_full,'wb')
        
        print 'Processing File %s. Writing Result to %s' % (fname, fout_name_full)
        
        tweetsFile = open(fname)
        for line in tweetsFile:
            print "Processing Tweet %d" % numTweets
            try:
                tweet = json.loads(line)
                numTweets += 1
            except ValueError:
                #print 'Warning: Invalid/Incomplete Tweet Encountered. Skipping to Next Tweet'
                #print line
                # skip the rest of the for loop and continue
                continue
            if tweet.has_key('text'):
                _text = tweet['text']#.decode('utf-8')
                #print _text
                text_noEmji = removeEmoji(_text)
                #print text_noEmji
                # the following function takes a unicode string a outputs a list of segmented (Thai) words
                segmentedList = textToSegmentedList(_text)
                tabJoinedWords = ('\t'.join(segmentedList))
                fout.write( tabJoinedWords.encode('utf-8') + '\n')
        numTweets += 1


def textToSegmentedList(sentence):
    # change later
    #return sentence.split(' ')
    return pythai.split(sentence)


def getListTweetFiles(dir='../Data/ThaiBatch1'):
    _listFiles = os.listdir(dir)
    for i in range(len(_listFiles)):
        _listFiles[i] = os.path.join(dir, _listFiles[i])
    return _listFiles

def testFoutName():
    fname = '../Data/ThaiBatch1/output1.txt'
    fout_name_m = re.search(r'[/]([\w]*).txt',fname)
    print fout_name_m.group(1)

def removeEmoji(text):
    # Replacing Emoji 
    # Surrogates for emoji are in the range [\uD800-\uDBFF][\uDC00-\uDFFF]
    return re.sub(u'[\uD800-\uDBFF][\uDC00-\uDFFF]',' ',text)

def main():
    pass
    #print getListTweetFiles()
    #testFoutName()
    convertTweetToSegmentedText(['../Data/ThaiBatch1/output1.txt']) # TEST
    all_listFiles = ( getListTweetFiles('../Data/ThaiBatch1') + 
                      getListTweetFiles('../Data/ThaiBatch2') + 
                      getListTweetFiles('../Data/ThaiBatch3') )
    print all_listFiles
    #convertTweetToSegmentedText(getListTweetFiles('../Data/ThaiBatch1'))
    # Then do the same for ThaiBatch1 + ThaiBatch2 + ThaiBatch3
    
if __name__ == "__main__":
    main()