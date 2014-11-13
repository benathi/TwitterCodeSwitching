'''
This script handles the conversion of input to output in the desired format.
Created on Nov 12, 2014

@author: Ben Athiwaratkun (pa338)

'''
#from __future__ import division
#import numpy as np
import json
import re
import enchant
from lib2to3.fixer_util import Newline

''' Input    : Tweet as a text
    Output   : A list of English Phrases (retain the contiguousness)
    Example  : ----- HAve a nice day --- oh my god ----
            The output is ['Have a nice day', 'oh my god']
'''
d_enchant = enchant.Dict('en_US')

def isEnglishWord(_text):
    return d_enchant.check(_text)
        
    
''' Input: Tweet
    Output: List of English Words
    Assumption: Agnostic about sentences. Only look at English **lone word** in the middle of Thai
    - Add a feature to include 2-gram, 3-gram, and more?
    '''
def tweetToCodeSwitching(tweetText):
    # Use regular expression to extract
    print tweetText
    # 1. Removing Hashtag #xxx or username @xxx or http:xxxx or https:xxx
    #tweetText = re.sub(r'[@#]\w+',r'REPLACING USERNAME/HASHTAG', tweetText) # - tested - passed
    tweetText = re.sub(r'[@#]\w+',r'', tweetText)
    #tweetText = re.sub(r'http://.*', r'REPLACING HTTP', tweetText) # tested/passed
    tweetText = re.sub(r'http://.*', r'', tweetText)
    tweetText = re.sub(r'https://.*', r'', tweetText)
    print tweetText
    
    
    list_words = re.findall(r"[a-zA-Z_' ]*", tweetText)
    #list_words = re.findall(r"[a-zA-Z0-9?><;,{}[\]\-_+=!@#$%\^&*|']*$", tweetText)
    new_list_words = []
    for w in list_words:
        if re.match(r'[a-zA-Z]', w):
            new_list_words.append(w)
    print new_list_words
    
    # 
    list_words = tweetText.split()
    check = True
    for i in range(len(list_words)):
        list_words[i].lower()
        isEnglishWord(list_words[i])
    
    print '-----------------------------------------------------'
    return new_list_words

# This extracts a list of code-switching English phrases
# Output: a list of dictionaries. Required field: 1. id 2. a list of code-switching instances. 
# For example
def extractCodeSwitchingInstances(fname):
    tweetsFile = open(fname)
    listCodeSwitching = []
    for line in tweetsFile:
        try:
            tweet = json.loads(line)
        except ValueError:
            print 'Warning: Invalid/Incomplete Tweet Encountered'
        _d = {}
        if tweet.has_key('id') and tweet.has_key('text'):
            _d['id'] = tweet['id']
            _listPhrases = tweetToCodeSwitching(tweet['text'])
            _d['code-switching-phrases'] = _listPhrases
            listCodeSwitching.append(_d)
        else:
            print 'This Tweet has no ID or no Text' 
        
    return listCodeSwitching
    print "Test: Done"

def testPyEnchant():
    print d_enchant.check('Hellao')     # False
    print d_enchant.check('He')         # True
    print d_enchant.check('He does')    # False
    print d_enchant.check('iphone')     # False
    print d_enchant.check('iPhone')     # True
    print d_enchant.check('bangkok')    # False
    print d_enchant.check('Bangkok')    # True
    print d_enchant.suggest('Hellao')  # gives out a long list
    print d_enchant.check('7')          # true
    print d_enchant.check('www')        # false
    print d_enchant.check('OnDemand')   # false
    print d_enchant.suggest('OnDemand') #On-Demand is the first word
    print d_enchant.check('lt')         # false
    print d_enchant.suggest('lt')       #Lt,Lat,Lot,lat,let,lit,..

def main():
    #testPyEnchant()    # works
    inputFileName = '../Data/output1.txt'
    print extractCodeSwitchingInstances(inputFileName)
    
    
if __name__ == "__main__":
    main()