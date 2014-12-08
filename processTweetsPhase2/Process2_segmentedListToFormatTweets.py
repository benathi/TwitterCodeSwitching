'''
Created on Nov 27, 2014

@author: Ben Athiwaratkun (pa338)

Input: from process 1:
Output: dictionary of tweets by id:
Format:
write it as json file
{
1:{text:'XXXXX XX', cs:None},
2:{text:'XXXXX Eat XX', cs:Eat},
}

'''
#from __future__ import division
#import numpy as np
import enchant
import langid
import pickle
import re
import os
import json
from subprocess import Popen, call, PIPE
#from ParseTweets.histogramAnalysis import runPOSTagger

# The list of accepted part of speech
accepted_pos = ['&','A','O','N','P','R','T','V']
d_enchant = enchant.Dict('en_US')


''' TODO 
To filter out:
semicolon, colon, 

Alternative: Filter out other character that are not Thai or Alpha Numeric? (Try this)
'''
def process2_part1(listFileNames, verbose=True):
    # Format: key = n-gram
    # value = {freq-cs: , freq-non-cs:}
    fout = open('../Data/process2/process2_part1.txt','wb')
    lineNum = -1
    numCSTweets = 0
    for fname in listFileNames:
        
        f = open(fname, 'rb')
        for _line in f:
            lineNum += 1
            print 'Processing Line %d' % lineNum
            tweet = json.loads(_line)
            tweetTextList = tweet['text']
            #textListIndicator = tweet['th-indicator']
            tweetText = '\t'.join(tweetTextList)
            
            #print line.strip()
            # Remove Tokens
            line_clean = removeNonCSTokens(tweetText)
            #print line_clean
            list_tagSep = line_clean.split('\t')
            #print list_tagSep
            list_tagSep2 = []
            for el in list_tagSep:
                if not len(el.strip()) == 0:
                    list_tagSep2.append(el.strip())
            list_lang = [langid.classify(el) for el in list_tagSep2]
            for i in range(len(list_tagSep2)):
                if isEmoji(list_tagSep2[i]):
                    list_lang[i] = 'emoji'
                
            # indicators for CS
            '''Filter 1. English Word (including French for word like Cafe with accent)
                         surrounded on the right or left by Thai'''
            list_cs_indicator1 = [False]*len(list_lang)
            max_len = len(list_tagSep2) - 1
            for i in range(len(list_tagSep2)):
                lang = list_lang[i]
                el = list_tagSep2[i]
                if lang[0] == 'en' or lang[0] == 'fr':
                    surroundedByThai = False
                    surroundedByEng = False
                    #if i == 0 or i == max_len:
                    
                    if i > 0:
                        lang_left = list_lang[i-1][0]
                        #print el
                        #print lang_left
                        if lang_left == 'th':
                            surroundedByThai = True
                        if lang_left == 'en' or lang_left == 'fr':
                            surroundedByEng = True    
                    if i < max_len:
                        lang_right = list_lang[i+1][0]
                        if lang_right == 'th':
                            surroundedByThai = True
                        if lang_right == 'en' or lang_right == 'fr':
                            surroundedByEng = True
                    #print 'Surrounded by Thai?%r Eng?%r' % (surroundedByThai, surroundedByEng)
                    if surroundedByThai and not surroundedByEng:
                        list_cs_indicator1[i] = True
            if sum(list_cs_indicator1) >= 1:
                numCSTweets += 1
            ## Write Result to file
            _d = {}
            cs_index = [i for i in range(len(list_cs_indicator1)) if list_cs_indicator1[i] ]
            _d['text'] = list_tagSep2
            _d['cs-index'] = cs_index
            # sanity check
            #print _d
            fout.write(json.dumps(_d))
            fout.write('\n')
            if not verbose:
                continue
            if sum(list_cs_indicator1) >= 1:
                print 'CS!!!!!-------------------------------------------'
                for el, lang, cs in zip(list_tagSep2, list_lang, list_cs_indicator1):
                    print 'Text:%s\tLang:%s.Is Potential CS?%s' % (el, lang, cs)
            else:
                print line_clean
            
    print 'Total Number of Tweets with CS %d' % (numCSTweets)


def isEmoji(text):
    # Replacing Emoji 
    # Surrogates for emoji are in the range [\uD800-\uDBFF][\uDC00-\uDFFF]
    m1 = re.match(u'[\uD800-\uDBFF][\uDC00-\uDFFF]',text)
    m2 = re.match(u'[\u2600-\u27BF]',text)
    m3 = re.match(u'[\uD83C][\uDF00-\uDFFF]',text)
    m4 = re.match(u'[\uD83D][\uDC00-\uDE4F]',text)
    m5 = re.match(u'[\uD83D][\uDE80-\uDEFF]',text)
    
    return (m1 != None or m2 != None or m3 != None or m4 != None or m5 != None)


def process2_part2():
    
    
    # 1. read file and write result to temp.txt for pos tagging
    fin = open('../Data/process2/process2_part1.txt','rb')
    pos_file = '../Data/process2/temp.txt'
    fpos = open(pos_file, 'wb')
    numLine = -1
    for line in fin:
        numLine += 1
        print 'To Temp File - Write Line %d' % numLine
        _d = json.loads(line)
        word_list = _d['text']
        index_cs = _d['cs-index']
        if len(index_cs) > 0:
            cs_words_list = []
            for index in index_cs:
                cs_words_list.append(word_list[index])
            cs_words = ' '.join(cs_words_list)
            #print type(cs_words)
            #print cs_words
            fpos.write(cs_words.encode('utf-8') + '\n')
    fpos.close()
    result = runPOSTagger(pos_file).split('\n')
    
    newFile = '../Data/process2/process2_part2.txt'
    fout = open(newFile, 'wb')
    resultLineNum = -1
    fin = open('../Data/process2/process2_part1.txt','rb')
    numSuccessfulCS = 0
    for line in fin:
        _d = json.loads(line)
        index_cs = _d['cs-index']
        new_cs_indicator = []
        if len(index_cs) > 0:
            resultLineNum += 1
            print 'CS #%d-------------------------------------------------' % resultLineNum
            result_all = result[resultLineNum].split('\t')
            list_tags = result_all[1].split(' ')
            if len(list_tags) > len(index_cs):
                print 'Warning!!!!!!!!!!!! Number of Tokens Mismatch'
                print result_all
                continue
            #print result_all
            #print list_tags
            #print _d['text']
            #print index_cs
            #_d['pos'] = list_tags
            for index,pos in zip(index_cs, list_tags):
                token = _d['text'][index]
                # If POS is in the accepted list and it's a dictionary word
                if pos in accepted_pos:
                    if d_enchant.check(token.lower()):
                        print '##############Yay########### CS=%s' % (token)
                        new_cs_indicator.append(index)
                        numSuccessfulCS += 1
        _newDict = {} # store only thai text, code-switching word, and position of code-switching words
        #textThai = _d['text']
        #for i in index_cs:
        #    textThai[i] = '\t'
        #textThaiString = '\t'.join(textThai)
        #_newDict['text-thai-list'] = textThaiString.split('\t')
        #_newDict['cs-word-list'] = [_d['text'][index] for index in new_cs_indicator]
        
        
        _newDict['text-list'] = _d['text']
        _newDict['cs-word-list'] = [_d['text'][index] for index in new_cs_indicator]
        if len(_newDict['cs-word-list']) > 0:
            print _newDict['text-list']
            print _newDict['cs-word-list']
        
        #for i in index_cs:
        #    if i not in new_cs_indicator:
        #        textThai[i] = ''
        #textThaiString = '\t'.join(textThai)
        #textThai2 = textThaiString.split('\t')        
        #indexCS_thaiText = [j for j in range(len(textThai2)) if textThai2[i] in _newDict['cs-word']]
        
        fout.write(json.dumps(_newDict))
        fout.write('\n')
    print 'Total Number of CS=%d' % numSuccessfulCS

def removeNonCSTokens(tweetText):
    tweetText = re.sub(r'[@#]\w+',r'\t', tweetText)
    tweetText = re.sub(r'[@#][\s]\w+',r'\t', tweetText)
    tweetText = re.sub(r'http://.*', r'\t', tweetText)
    tweetText = re.sub(r'https://.*', r'\t', tweetText)
    tweetText = re.sub(r'RT', r'\t', tweetText)
    tweetText = re.sub(r'\n', r'\t', tweetText)
    tweetText = re.sub(r'[@()&$+%]',r'\t',tweetText)
    tweetText = re.sub(r'[\d]+', r'\t', tweetText)
    tweetText = re.sub(r'T[_]*T', r'\t', tweetText)
    tweetText = re.sub(r'[\[\]\(\)\{\}]+', r'\t', tweetText)
    tweetText = re.sub(r'[\^~_]+', r'\t', tweetText)
    tweetText = re.sub(r'[#!:-]+', r'\t', tweetText)
    tweetText = re.sub(r'[\.]+', r'\t', tweetText)
    tweetText = re.sub(r'["\?\/;]+', r'\t', tweetText)
    #tweetText = re.sub(r'[\.^:;_\-\?\"!]+', r'\t', tweetText)
    tweetText = tweetText.strip()
    return tweetText

def tweetPartOfSpeech(el):
    temp_filename = 'temp/temp.txt'
    f = open(temp_filename, 'wb')
    f.write(el)
    f.close()
    output = runPOSTagger(temp_filename)
    # only one line
    result = output.split('\t')
    print result
    pos = result[1]
    return pos

def runPOSTagger(fname):
    p = Popen(['bash',
               '../ParseTweets/ark-tweet-nlp-0.3.2/runTagger.sh',
               '--output-format' ,
               'pretsv',
               '--no-confidence',
               fname], stdin=PIPE, stdout=PIPE, stderr=PIPE)

    output, err = p.communicate()
    rc = p.returncode
    print 'Done Tagging. Return Code is %d' % rc
    return output



def getListInputFiles(dir='../Data/SegmentedTweets'):
    _listFiles = os.listdir(dir)
    for i in range(len(_listFiles)):
        _listFiles[i] = os.path.join(dir, _listFiles[i])
    return _listFiles

def main():
    ''' Part 1 '''
    #list_inputFiles = getListInputFiles()
    list_inputFiles = ['../Data/process1/output1_mini_textList_Thai.txt']
    process2_part1(list_inputFiles)
    ''' Part 2 '''
    #process2_part2()
    
def test():
    print tweetPartOfSpeech('Ben goes to the mall.')
    print tweetPartOfSpeech('Benni\n \nI want\n \nNo\n')

def testWordInDict():
    # All these lone words are in dict
    print d_enchant.check('L')
    print d_enchant.check('D')
    print d_enchant.check('l')
    print d_enchant.check('d')

if __name__ == "__main__":
    main()
    #test()
    #testWordInDict()