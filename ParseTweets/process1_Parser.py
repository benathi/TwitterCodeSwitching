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
import pickle
import langid
import os

''' Input    : Tweet as a text
    Output   : A list of English Phrases (retain the contiguousness)
    Example  : ----- HAve a nice day --- oh my god ----
            The output is ['Have a nice day', 'oh my god']
'''
d_enchant = enchant.Dict('en_US')

def isEnglishWord(_text):
    if _text == '':
        return False
    else:
        return d_enchant.check(_text)
        
###### This method break phrase into multiple phrases
###### For Example: a phrase 'I want &gt chicken'
###### Actually we should simply remove the non-identifiable word
def breakPhrase(phrase):
    phrase = phrase.lower()
    _l = phrase.split(' ')
    new_list = []
    currentPhrase = ''
    for w in _l:
        if isEnglishWord(w):
            currentPhrase += ' ' +  w
        else:
            if currentPhrase.strip() != '':
                new_list.append(currentPhrase.strip())
                currentPhrase = ''
    if currentPhrase.strip() != '':
        new_list.append(currentPhrase.strip())
    return new_list


''' Input: Tweet
    Output: List of English Phrases
    Specification:
        Remove hashtag
        Remove username
        TODO : For proper noun, put them in another key
    '''
def tweetToCodeSwitchingPhrases(tweetText, verbose=False, filterThaiCS=True):
    # there's an option to filter Thai Code-Switch instance or not
    # Input: Tweet (text)
    # Output: List of Phrases
    
    # 1. Removing Hashtag #xxx or username @xxx or http:xxxx or https:xxx
    #tweetText = re.sub(r'[@#]\w+',r'REPLACING USERNAME/HASHTAG', tweetText) # - tested - passed
    tweetText = re.sub(r'[@#]\w+',r'', tweetText)
    #tweetText = re.sub(r'http://.*', r'REPLACING HTTP', tweetText) # tested/passed
    tweetText = re.sub(r'http://.*', r'', tweetText)
    tweetText = re.sub(r'https://.*', r'', tweetText)
    if verbose: print tweetText
    
    
    #list_words = re.findall(r"[a-zA-Z0-9_\-()' ]*", tweetText)
    list_words = re.findall(u"[^\u0E00-\u0E7F]*", tweetText)
    
    #list_words = re.findall(r"[a-zA-Z0-9?><;,{}[\]\-_+=!@#$%\^&*|']*$", tweetText)
    new_list_words = []
    
    
    # Check 3 conditions
    # 1. Remove empty string
    # 2. Filter out phrases that contain only numbers or symbols
    # 3. Filter out phrases that are not surrounded by Thai (no Thai before or no Thai after)
    for w in list_words:
        # 1.
        if not len(w.strip()) == 0:   
            # 2. make sure it contains some word character not just numbers of symbols
            containSomeW = re.search(r"[a-zA-Z]+", w)
            if not containSomeW == None and len(containSomeW.group().strip()) > 0:
                # 3.
                position_start = tweetText.find(w)
                position_end = position_start + len(w)
                thaiBefore = langid.classify(tweetText[:position_start])
                thaiAfter = langid.classify(tweetText[position_end:])
                if verbose:
                    #print 'Location' , position_start
                    print 'Testing if Phrases before are Thai'
                    print thaiBefore
                    print 'Testing if Phrases after are Thai'
                    print thaiAfter
                
                # If the option is not to filter Thai CodeSwitch : always add
                if (not filterThaiCS) or ((thaiBefore[0] == 'th' and thaiBefore[1] >= 0.75) or 
                    (thaiAfter[0] == 'th' and thaiAfter[1] >= 0.75)):
                    new_list_words.append(w.strip())
    
    # what should we do if the words are not actual English words
    # Minimal processing: don't break phrases for now
    '''new_list_words2 = []
    for i in range(len(new_list_words)):
        _list1 = breakPhrase(new_list_words[i])
        print "List 1 =" 
        print _list1
        new_list_words2 += _list1'''
    
    if verbose and not new_list_words == []:
        print tweetText
        print new_list_words
    if verbose: print '-----------------------------------------------------'
    #print '.'
    return new_list_words

# This extracts a list of code-switching English phrases
# Output: a list of dictionaries. Required field: 1. id 2. a list of code-switching instances. 
# For example
def extractCodeSwitchingInstances(listFileNames, filterThaiCS=True, tag=''):
    listCodeSwitching = []
    numTweets = 1
    numDuplicateStr = 0
    for fname in listFileNames:
        if not '.txt' in fname: 
            continue
        dict_id_str = {}
        print 'Processing File %s' % fname
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
            _d = {}
            if tweet.has_key('id') and tweet.has_key('text'):
                if isRT(tweet['text']):
                    print 'RT'
                    continue
                #print 'Non RT'
                
                if tweet['id_str'] in dict_id_str:
                    print 'Found Duplicate ID STR'
                    numDuplicateStr += 1
                    continue
                else:
                    dict_id_str[tweet['id_str']] = True
                
                _listPhrases = tweetToCodeSwitchingPhrases(tweet['text'], filterThaiCS=filterThaiCS)
                
                #print tweet['text']
                #print _listPhrases
                
                # Before: save id regardless
                # After: save id and cs only when there's a CS instance (roughl determination)
                if not _listPhrases == []: # saves the list only if there's a code switching instance
                    _d['id'] = tweet['id']
                    _d['cs'] = _listPhrases # cs stands for code-switching
                listCodeSwitching.append(_d)
            else:
                print 'This Tweet has no ID or no Text'
    print 'Number of Duplicate ID_STR = %d' % numDuplicateStr
    if filterThaiCS:
        pickle.dump(listCodeSwitching, open('../preprocessedData/list_codeSwitchPhrases.p','wb'))
    else:
        pickle.dump(listCodeSwitching, open('../preprocessedData/list_engPhrases_' + tag + '.p', 'wb'))
    return listCodeSwitching

def isRT(s):
    m = re.match(r'RT @[\w]+:', s)
    #print m
    return m != None

def sanityCheck():
    inputFileName = '../Data/output1.txt'
    extractCodeSwitchingInstances([inputFileName])

# Default folder is ThaiBatch1
def getListTweetFiles(dir='../Data/ThaiBatch1'):
    _listFiles = os.listdir(dir)
    for i in range(len(_listFiles)):
        _listFiles[i] = os.path.join(dir, _listFiles[i])
    return _listFiles

def test():
    print breakPhrase('water melon bfdaeff new word')
    print getListTweetFiles()

def main():
    pass
    #inputFileName = '../Data/output1.txt'
    listFiles = ( getListTweetFiles('../Data/ThaiBatch1') + getListTweetFiles('../Data/ThaiBatch2') +
            getListTweetFiles('../Data/ThaiBatch3') + getListTweetFiles('../Data/ThaiBatch4') )
    #listFiles = ['../Data/ThaiBatch1/output1.txt']
    extractCodeSwitchingInstances(listFiles)
    
    
    # English (get only English)
    #extractCodeSwitchingInstances(['../Data/EngTweets/tweets_eng_nov17.txt'], filterThaiCS=False, tag='eng_nov17')
    
if __name__ == "__main__":
    main()