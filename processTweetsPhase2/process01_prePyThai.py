'''
Created on Dec 7, 2014

@author: Ben Athiwaratkun (pa338)

'''
#from __future__ import division
#import numpy as np
import os
import json
import re
RT = 'retweeted'
TH_INDICATOR = 'th-indicator'
TEXT = 'text'

def tweetTextToDisjointedList(listFileNames, sanityCheck=False):
    outputPath = '../Data/process01/'
    numTweets = 0
    numTweets_written = 0
    for fname in listFileNames:
        if not '.txt' in fname:
            continue
        
        fout_name_m = re.search(r'[/]([\w]*).txt',fname)
        fout_name =  fout_name_m.group(1)
        fout_name_full = os.path.join(outputPath, fout_name + '_textList.txt')
        fout = open(fout_name_full,'wb')
        
        print 'Processing File %s. Writing Result to %s' % (fname, fout_name_full)
        
        tweetsFile = open(fname)
        for line in tweetsFile:
            try:
                tweet = json.loads(line)
                numTweets += 1
            except ValueError:
                print 'Warning: Invalid/Incomplete Tweet Encountered. Skipping to Next Tweet'
                #print line
                # skip the rest of the for loop and continue
                continue
            if tweet[RT]:
                #print 'Skipping RT'
                continue
            print "Processing Tweet %d------------------------" % numTweets
            tweetText = tweet[TEXT]
            textList, textListIndicator = tokenizeMixedLanguage(tweetText)
            
            ''' Sanity Check'''
            if sanityCheck:
                if numTweets_written >= 1000:
                    return
                print tweetText
                print textList
                print textListIndicator
            
            tweet[TEXT] = textList
            tweet[TH_INDICATOR] = textListIndicator
            fout.write(json.dumps(tweet))
            fout.write('\n')
            numTweets_written += 1
    print 'Done with tweetTextToDisjointedList'
    print 'Number of Tweets = %d' % numTweets
    print 'Number of Tweets Written (Non-RT) = %d' % numTweets_written
'''
Note: as of Dec 7, 2014

Number of Tweets = 2583827
Number of Tweets Written (Non-RT) = 775400
'''

thaiRegExp = re.compile(u'[\u0E00-\u0E7F]+')

def tokenizeMixedLanguage(s):
    regList = [thaiRegExp.match(c) != None for c in s]
    indexToBreak = []
    for i in range(1,len(regList)):
        if regList[i-1] != regList[i]:
            indexToBreak.append(i)
    
    textListIndicator = []
    textList = []
    phrase = ""
    for i in range(len(s)):
        c = s[i]
        if i in indexToBreak:
            textList.append(phrase)
            # for i = 0, it won't get here
            textListIndicator.append(regList[i-1])
            phrase = c
        else:
            phrase += c
    textList.append(phrase)
    textListIndicator.append(regList[len(s)-1])
    #for word,isThai in zip(textList,textListIndicator):
    #    print word
    #    print "is Thai?", isThai
    return textList,textListIndicator

def getListTweetFiles(dir='../Data/ThaiBatch1'):
    _listFiles = os.listdir(dir)
    for i in range(len(_listFiles)):
        _listFiles[i] = os.path.join(dir, _listFiles[i])
    return _listFiles

def test():
    tweetTextToDisjointedList(['../Data/process0/tweetsoct212014_mini.txt']) # TEST

def main():
    all_listFiles = ( getListTweetFiles('../Data/process0/') )
    tweetTextToDisjointedList(all_listFiles)
    
    
if __name__ == "__main__":
    main()