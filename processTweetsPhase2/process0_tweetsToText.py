'''
Created on Nov 27, 2014

@author: Ben Athiwaratkun (pa338)

Process 0: Added because python on ubuntu could not handle regular expression for emoji

'''
#from __future__ import division
#import numpy as np

import os
import json
import re

# Default folder is ThaiBatch1
def convertTweetToSegmentedText(listFileNames):
    segmentedWordsPath = '../Data/pre_SegmentedTweets/'
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
                text_noEmoji = removeEmoji(_text)
                #print text_noEmoji
                # the following function takes a unicode string a outputs a list of segmented (Thai) words
                #segmentedList = textToSegmentedList(text_noEmoji)
                #tabJoinedWords = ('\t'.join(segmentedList))
                #fout.write( tabJoinedWords.encode('utf-8') + '\n')
                #print _text
                #print text_noEmoji
                fout.write(text_noEmoji.encode('utf-8') +'\n')
        numTweets += 1




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
    new_text1 = re.sub(u'[\uD800-\uDBFF][\uDC00-\uDFFF]',' ',text)
    return re.sub(u'\s',' ',new_text1)

def main():
    pass
    #print getListTweetFiles()
    #testFoutName()
    #convertTweetToSegmentedText(['../Data/ThaiBatch1/output1.txt']) # TEST
    all_listFiles = ( getListTweetFiles('../Data/ThaiBatch2') + 
                      getListTweetFiles('../Data/ThaiBatch3') )
    #print all_listFiles
    #convertTweetToSegmentedText(getListTweetFiles('../Data/ThaiBatch1'))
    convertTweetToSegmentedText(all_listFiles)
    # Then do the same for ThaiBatch1 + ThaiBatch2 + ThaiBatch3
    

    
if __name__ == "__main__":
    main()