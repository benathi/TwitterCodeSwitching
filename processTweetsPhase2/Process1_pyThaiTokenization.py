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
from process01_prePyThai import TEXT, TH_INDICATOR

# Default folder is ThaiBatch1
def convertTextToSegmentedText(listFileNames):
    segmentedWordsPath = '../Data/process1/'
    numTweets = 0
    numError = 0
    for fname in listFileNames:
        if not '.txt' in fname: 
            continue
        
        fout_name_m = re.search(r'[/]([\w]*).txt',fname)
        fout_name =  fout_name_m.group(1)
        fout_name_full = os.path.join(segmentedWordsPath, fout_name + '_Thai.txt')
        fout = open(fout_name_full,'wb')
        
        print 'Processing File %s. Writing Result to %s' % (fname, fout_name_full)
        
        tweetsFile = open(fname)
        for _line in tweetsFile:
            print "Processing Tweet %d" % numTweets
            numTweets += 1
            tweet = json.loads(_line)
            textList = tweet[TEXT]
            textListIndicator = tweet[TH_INDICATOR]
            
            for i in range(len(textList)):
                if textListIndicator[i]:
                    text = textList[i]
                    try:
                        segmentedList = textToSegmentedList(text)
                    except:
                        numError += 1
                        print 'Error Occured During Text Segmentation. File %s.' %(fname)
                        print textList
                        segmentedList = []
                    # rewriting new value
                    textList[i] = '\t'.join(segmentedList)

            fout.write(json.dumps(tweet))
            fout.write('\n')
    print 'Number of Errors = %d' % numError


def textToSegmentedList(sentence):
    # change later
    #return sentence.split(u' ')
    return pythai.split(sentence)
    


def getListTweetFiles(dir='../Data/ThaiBatch1'):
    _listFiles = os.listdir(dir)
    for i in range(len(_listFiles)):
        _listFiles[i] = os.path.join(dir, _listFiles[i])
    return _listFiles


def test():
    convertTextToSegmentedText(['../Data/process01/output1_mini_textList.txt']) # TEST

def main():
    all_listFiles = ( getListTweetFiles('../Data/process01/') )
    convertTextToSegmentedText(all_listFiles)
    
if __name__ == "__main__":
    test()