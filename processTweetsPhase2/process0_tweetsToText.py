# -*- coding: utf-8 -*-
'''
Created on Nov 27, 2014

@author: Ben Athiwaratkun (pa338)

Process 0: Added because python on ubuntu could not handle regular expression for emoji

Note: Down arrow not include in reg exp for emoji. Maybe filter by Thai character and English character?
'''
#from __future__ import division
#import numpy as np

import os
import json
import re

# Default folder is ThaiBatch1
def convertTweetToSegmentedText(listFileNames):
    segmentedWordsPath = '../Data/process0/'
    numTweets = 0
    numTweets_RT = 0
    for fname in listFileNames:
        if not '.txt' in fname:
            continue
        
        fout_name_m = re.search(r'[/]([\w]*).txt',fname)
        fout_name =  fout_name_m.group(1)
        fout_name_full = os.path.join(segmentedWordsPath, fout_name + '_mini.txt')
        fout = open(fout_name_full,'wb')
        
        print 'Processing File %s. Writing Result to %s' % (fname, fout_name_full)
        
        tweetsFile = open(fname)
        for line in tweetsFile:
            _d = {}
            print "Processing Tweet %d" % numTweets
            try:
                tweet = json.loads(line)
                numTweets += 1
            except ValueError:
                #print 'Warning: Invalid/Incomplete Tweet Encountered. Skipping to Next Tweet'
                #print line
                # skip the rest of the for loop and continue
                continue
            if tweet.has_key('text') and tweet.has_key('id_str') and tweet.has_key('retweeted'):
                _d['text'] = tweet['text']
                _d['id_str'] = tweet['id_str']
                # Note: the retweeted tag from the original json is ALWAYS false for some reason
                #_d['retweeted'] = tweet['retweeted']
                _d['retweeted'] = isRT(_d['text'])
                if _d['retweeted']:
                    numTweets_RT += 1
                #_text = tweet['text']#.decode('utf-8')
                #print type(_text)
                #text_noEmoji = removeEmoji(_text)
                #print text_noEmoji
                # the following function takes a unicode string a outputs a list of segmented (Thai) words
                #segmentedList = textToSegmentedList(text_noEmoji)
                #tabJoinedWords = ('\t'.join(segmentedList))
                #fout.write( tabJoinedWords.encode('utf-8') + '\n')
                #print _text
                #print text_noEmoji
                #fout.write(text_noEmoji.encode('utf-8') +'\n')
                fout.write(json.dumps(_d))
                fout.write("\n")
        numTweets += 1
    print 'The number of Total Tweets = %d', numTweets
    print 'The number of RT = %d', numTweets_RT
'''
Note: as of Dec 7, 2014 (Final Data Set)
The number of Total Tweets = %d 2583847
The number of RT = %d 1808427
'''


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
    new_text_00 = re.sub(u'[\uD800-\uDBFF][\uDC00-\uDFFF]',' ',text)
    new_text_01 = re.sub(u'[\u2600-\u27BF]',' ',new_text_00)
    new_text_02 = re.sub(u'[\uD83C][\uDF00-\uDFFF]',' ',new_text_01)
    new_text_03 = re.sub(u'[\uD83D][\uDC00-\uDE4F]',' ',new_text_02)
    new_text_04 = re.sub(u'[\uD83D][\uDE80-\uDEFF]',' ',new_text_03)
    
    new_text = new_text_04
    
    return re.sub(u'\s',' ',new_text)


''' The tag 'retweeted' in json does not truly indicate retweet for some reason'''
def testRetweetManual():
    s = u'RT @kongkangpcy: ยังคงรักเธอ ยังเฝ้ารออยู่เหมือนอย่างเคย'
    isRT(s)
    s2 = u'no retweet'
    isRT(s2)

def isRT(s):
    m = re.match(r'RT @[\w]+:', s)
    #print m
    return m != None
    

def main():
    all_listFiles = ( getListTweetFiles('../Data/ThaiBatch1') +
                     getListTweetFiles('../Data/ThaiBatch2') + 
                      getListTweetFiles('../Data/ThaiBatch3') + 
                      getListTweetFiles('../Data/ThaiBatch4') )
    
    #all_listFiles = ( getListTweetFiles('../Data/ThaiBatch1') )
    convertTweetToSegmentedText(all_listFiles)
    # Then do the same for ThaiBatch1 + ThaiBatch2 + ThaiBatch3

    
if __name__ == "__main__":
    main()