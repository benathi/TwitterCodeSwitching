'''
This script handles preliminary analysis for code-switching
Created on Nov 13, 2014

@author: Ben Athiwaratkun (pa338)

'''
#from __future__ import division
import numpy as np
import pickle
import matplotlib.pyplot as plt
import plotly.plotly as py
#from plotly.graph_objs import *
#from ggplot.geoms.geom_histogram import geom_histogram
from ggplot import *
import pandas as pd
from subprocess import Popen, call, PIPE
from nltk.tag.stanford import NERTagger
from mercurial.phases import listphases
import os
import sys
#POS_KEYS = ['!', '$', '&', ',', 'A', 'E', 'D', 'G', 'L', 'O', 'N', 'P', 'S', 'R', 'U', 'T', 'V', 'Y', 'X', 'Z', '^', '~']
POS_KEYS = ['!', '#', '$', '&', ',', 'A', 'E', 'D', 'G', 'L', 'O', 'N', 'P', 'S', 'R', 'U', 'T', 'V', 'Y', 'X', 'Z', '^', '~']
# @, M
#POS_KEYS = ['!', '#', '$', '&', ',', 'A', '@', 'E', 'D', 'G', 'M', 'L', 'O', 'N', 'P', 'S', 'R', 'U', 'T', 'V', 'Y', 'X', 'Z', '^', '~']


def loadCodeSwitchPhrases():
    return pickle.load(open('../preprocessedData/list_codeSwitchPhrases.p','rb'))

def loadEngPhrases():
    return pickle.load(open('../preprocessedData/list_engPhrases_eng_nov17.p'))

# Preprocessing
# Filter out unwanted phrases
def csList(option='All'):
    # 1. This is the minimal version - only selecting non-empty
    cs_dict = loadCodeSwitchPhrases()
    newList_cs = []
    numTweets = 0 # put the number in here
    numCSTweets = 0
    ###############
    if option=='All':
        for el in cs_dict:
            #numTweets += 1
            if 'cs' in el:
                numCSTweets += 1
                newList_cs.append(el['cs'])
    ###############
    return (numTweets, numCSTweets, newList_cs)

def histogram_numberOfcs():
    # This generates a histogram length of code-switching instances
    numTweets, numCSTweets, listCS = csList()
    # make a histogram
    listNumCS = np.array([ len(el)  for el in listCS])
    plt.hist(listNumCS)
    plt.show()

def histogram_CSLength():
    # This generates a histogram length of code-switching instances
    numTweets, numCSTweets, listCS = csList()
    # make a histogram
    print 'Number of Total Tweets=\t%d' % numTweets
    print 'Number of Code-Switching Tweets=\t%d' % numCSTweets 
    list_lengthCS = []
    for el in listCS:
        for el2  in el:
            # look at the number of words in a string
            list_lengthCS.append(len(el2.split()))
    #data = Data([Histogram(x=list_lengthCS)])
    #plot_url = py.plot(data, filename='../Results/histogram_Length_CS')

    df = pd.DataFrame(list_lengthCS, columns=['length_cs'])
    p = ggplot(aes(x='length_cs'), data=df)+ geom_histogram(binwidth=1,fill='#FF9999')
    print p
    return p

def listMostFrequent():
    # This will list the most frequent phrases 
    _dp = {} # dict for phrases
    _dw = {} # dict for words
    _,_, listCS = csList()
    for list_phrase in listCS:
        for phrase in list_phrase:
            if phrase  in _dp:
                _dp[phrase] += 1
            else:
                _dp[phrase] = 1
    
            for word in phrase.split():
                if word in _dw:
                    _dw[word] += 1
                else:
                    _dw[word] = 1
    
    print 'Listing Popular Words'
    listWords = [None]*len(_dw.keys())
    i=0
    for key in _dw:
        listWords[i] = (key, _dw[key]) 
        i += 1
    listWords.sort(key=lambda x: x[1], reverse=True) # sort descending
    #listWords = sorted(listWords, key=lambda x: x[1])
    for i in range(100):
        print listWords[i]
    
    print 'Listing Popular Phrases'
    listPhrases = [None]*len(_dp.keys())
    i=0
    for key in _dp:
        listPhrases[i] = (key, _dp[key]) 
        i += 1
    listPhrases.sort(key=lambda x: x[1], reverse=True) # sort descending
    #listWords = sorted(listWords, key=lambda x: x[1])
    for i in range(100):
        print listPhrases[i]
        
    # Note: listWords and listPhrases are nearly identical because the number of len-1 phrases dominate
    # Format [] of tuples (key, freq)
    pickle.dump(listWords, open('../preprocessedData/list_cs_words.p','wb'))
    pickle.dump(listPhrases, open('../preprocessedData/list_cs_phrases.p','wb'))
    
    # also write list of phrases into files [required as input for runTagger.sh]
    # one line for one tweet text
    #listPhrases = pickle.load(open('../preprocessedData/list_cs_phrases.p','rb'))
    f = open('../preprocessedData/list_cs_phrasesNoFreq.txt','wb')
    for phrasePair in listPhrases:
        f.write(phrasePair[0] + '\n')
    f.close()
    return (listWords, listPhrases)


def tagTweets(fname='list_cs_phrasesNoFreq.txt'):
    # works
    #exit_code = call(['bash', 'ark-tweet-nlp-0.3.2/runTagger.sh', '--output-format', 'pretsv', '--no-confidence' ,'ark-tweet-nlp-0.3.2/examples/casual.txt'])
    
    p = Popen(['bash',
               'ark-tweet-nlp-0.3.2/runTagger.sh',
               '--output-format' ,
               'pretsv',
               '--no-confidence',
               '../preprocessedData/' + fname], stdin=PIPE, stdout=PIPE, stderr=PIPE)

    output, err = p.communicate()
    rc = p.returncode
    print 'Return Code is %d' % rc
    ### 
    listPhrases = pickle.load(open('../preprocessedData/list_cs_phrases.p', 'rb'))
    lineNum = 0
    for line in output.splitlines():
        result = line.split('\t')
        #tokens, tags = (result[0], result[1])
        list_tokens = result[0].split(' ')
        list_tags = result[1].split(' ')
        print 'Token List'
        print list_tokens
        
        print 'Tag List'
        print list_tags
        
        listPhrases[lineNum] = (listPhrases[lineNum][0], listPhrases[lineNum][1], list_tokens, list_tags)
        
        if not len(list_tags) == len(list_tokens):
            print 'Error! List of Tags and List of Tokens are Not of the Same Length'
            return -1
        lineNum += 1
    
    pickle.dump(listPhrases, open('../preprocessedData/list_cs_phrases_w_tags.p', 'wb'))
    
    ### print out top 1000
    for i in range(1000):
        print listPhrases[i]
    
    return rc

'''def getTags():
    # Tag and save to file (bash process)
    tagTweets()
    # Then load from file
    with open('../preprocessedData/phrasesTagged.txt') as f:
        for line in f:
            print line'''
    

def histogramPOS():
    # do a part of speech histogram
    listPhrases = pickle.load(open('../preprocessedData/list_cs_phrases_w_tags.p', 'rb'))
    dict_pos = {}
    for phrase in listPhrases:
        for tag in phrase[3]:
            if not tag in dict_pos:
                dict_pos[tag] = 1
            else:
                dict_pos[tag] += 1
    #print dict_pos.keys()
    #print [dict_pos[key] for key in dict_pos]
    
    tags = POS_KEYS
    listFreq = [None]*len(tags)
    sumTags = 0
    for i in range(len(tags)):
        if tags[i] in dict_pos:
            listFreq[i] = dict_pos[tags[i]]
        else:
            listFreq[i] = 0
        sumTags += listFreq[i]
    print 'Total number of tags(tokens) = %d' % sumTags
    for i in range(len(tags)):
        listFreq[i] /= sumTags*1.0
    
    df = pd.DataFrame({'POS':POS_KEYS, 'Density':listFreq})
    p = (ggplot(aes(x='POS',y='Density'), data=df) +
     geom_bar(stat='identity', fill='#FF9999') +
      labs(title='Distribution of Part for Speech of '+ str(sumTags) +' Words in Code-Switching Phrases') )
    print p

def histogramPOS_LoneCS():
    # do a part of speech histogram
    listPhrases = pickle.load(open('../preprocessedData/list_cs_phrases_w_tags.p', 'rb'))
    dict_pos = {}
    totalNum = 0
    numLoneCS = 0
    for phrase in listPhrases:
        totalNum += 1
        if len(phrase[3]) == 1:
            numLoneCS += 1
            tag = phrase[3][0]
            if not tag in dict_pos:
                dict_pos[tag] = 1
            else:
                dict_pos[tag] += 1
    
    tags = POS_KEYS
    listFreq = [None]*len(tags)
    sumTags = 0
    for i in range(len(tags)):
        if tags[i] in dict_pos:
            listFreq[i] = dict_pos[tags[i]]
        else:
            listFreq[i] = 0
        sumTags += listFreq[i]
    print 'Total number of tags(tokens) = %d' % sumTags
    for i in range(len(tags)):
        listFreq[i] /= sumTags*1.0
    
    print 'The number of CS phrases = %d' % totalNum
    print 'The number of CS phrases of length 1 = %d' % numLoneCS
    
    df = pd.DataFrame({'POS':POS_KEYS, 'Density':listFreq})
    p = ( ggplot(aes(x='POS',y='Density'), data=df) +
           geom_bar(stat='identity', fill='#FF9999') +
           labs(title='Distribution of Part of Speech of ' + str(sumTags) + ' Code-Switching Lone Words') )
    print p


def buildNERtagger():
    currentDir = os.getcwd()
    f1_path = os.path.join(currentDir, 'stanford-ner-2014-06-16/classifiers/english.all.3class.distsim.crf.ser.gz')
    f2_path = os.path.join(currentDir, 'stanford-ner-2014-06-16/stanford-ner.jar')
    st = NERTagger(f1_path, f2_path)
    return st

def NER_Tweets():
    st = buildNERtagger()
    listPhrases = pickle.load(open('../preprocessedData/list_cs_phrases_w_tags.p', 'rb'))
    #list_onlyPhrases = [ ' '.join(phrase[2]).encode('ascii') for phrase in listPhrases]
    list_onlyPhrases = ['']*len(listPhrases)
    for i in range(len(list_onlyPhrases)):
        phrase = ' '.join(listPhrases[i][2])
        for ch in phrase:
            if not ord(ch) < 128:
                print 'Error!'
                print phrase
                print ch
                break
        list_onlyPhrases[i] = phrase.encode('utf-8')
    
    print list_onlyPhrases[:10]
    ## TODO - Problem with encoding/decoding
    
    #print 'Exit'
    #sys.exit()
    print 'Start NER Tagging'
    ner_tags = st.tag(list_onlyPhrases)
    print 'Done NER Tagging'
    for i in range(len(listPhrases)):
        listPhrases[i] = (listPhrases[i][0], listPhrases[i][1], listPhrases[i][2], listPhrases[i][3] , ner_tags[i])
    print 'Showing Tags for Top 100'
    for i in range(500):
        print listPhrases[i]
    pickle.dump(listPhrases, open('../preprocessedData/list_cs_phrases_pos_ner.p', 'wb'))

def histogramStanfordNER():
    listPhrases = pickle.load(open('../preprocessedData/list_cs_phrases_pos_ner.p', 'rb'))
    # format: [] of (key, frequency)
    
    dict_ner = {}
    TUPLE_INDEX_NER = 4
    for phrase in listPhrases:
        for tag in phrase[TUPLE_INDEX_NER]:
            if not tag in dict_ner:
                dict_ner[tag] = 1
            else:
                dict_ner[tag] += 1
    freq = [dict_ner[key] for key in dict_ner]
    _sum = sum(freq)
    for i in range(len(freq)):
        freq[i] /= _sum*1.0
    
    df = pd.DataFrame({'NER Tagging':dict_ner.keys(), 'Density':freq})
    p = ggplot(aes(x='NER Tagging',y='Density'), data=df)+ geom_bar(stat='identity', fill='#FF9999')
    print p
    

def AnalyzeCSPhrases():
    listPhrases = pickle.load(open('../preprocessedData/list_cs_phrases_w_tags.p', 'rb'))
    #for p in listPhrases: print p
    # make a dictionary of list of phrases?
    dict_cs_byPhrase = {}
    for tup in listPhrases:
        phrase = tup[0]
        freq = tup[1]
        dict_cs_byPhrase[phrase] = {'freq':freq, 'tweet_tokens':tup[2], 'tweet_tags':tup[3]}
    

    ### Initialization
    dict_cs_byTags_LW = {}
    # key: pos tag
    # value: {V:{'eat':5, 'drink':6} , {N:{'home':10, 'house':11}} }
    for key in POS_KEYS:
        dict_cs_byTags_LW[key] = {}
    ### End Initialization
    
    ### Question: Should I include tokens in phrases? 
    
    for key in dict_cs_byPhrase:
        if len(dict_cs_byPhrase[key]['tweet_tokens']) == 1:
            pos = dict_cs_byPhrase[key]['tweet_tags'][0]
            token = dict_cs_byPhrase[key]['tweet_tokens'][0]
            
            if not pos in dict_cs_byTags_LW:
                dict_cs_byTags_LW[pos] = {}
            
            if not token in dict_cs_byTags_LW[pos]:
                dict_cs_byTags_LW[pos][token] = dict_cs_byPhrase[key]['freq']
            else:
                dict_cs_byTags_LW[pos][token] += dict_cs_byPhrase[key]['freq']
    
    fname = '../preprocessedData/Batch1And2_listCSbyPOS_LoneWords.tsv'
    #if not os.path.isfile(fname):
    f = open(fname,'wb')
    #Format for each line: POS \t Word \t frequency
    for pos in dict_cs_byTags_LW:
        list_this_pos = [ (word, dict_cs_byTags_LW[pos][word])  for word in dict_cs_byTags_LW[pos].keys()]
        list_this_pos.sort(key=lambda x: x[1], reverse=True)
        for it in list_this_pos:
            f.write(pos+'\t'+ str(it[0]) + '\t' + str(it[1]) +'\n')
    f.close()
    
    pickle.dump(dict_cs_byTags_LW, open('../preprocessedData/dict_cs_byTags_LW.p','wb'))
    
    return (dict_cs_byPhrase, dict_cs_byTags_LW)





#################### English
def produceEnglishPOSHistogram():
    engPhrasesList = loadEngPhrases()
    fname = '../preprocessedData/list_engPhrases.txt'
    f = open(fname,'wb')
    numTweets = len(engPhrasesList)
    for item in engPhrasesList:
        if not 'cs' in item:
            continue
        for phrase in item['cs']: # not exactly code-switch phrase
            if not phrase.strip() == '':
                f.write(phrase + '\n') 
    f.close()
    return producePOShistogram(fname, text_title = 'in ' + str(numTweets) + ' Tweets')


def produce50mpaths2POSHistogram():
    originalFileName = '../Data/BrownClustering/50mpaths2.txt'
    fin = open(originalFileName, 'rb')
    outFilename = '../Data/BrownClustering/50mpaths2_onlyWords.txt'
    fout = open(outFilename, 'wb')
    weights = []
    for line in fin:
        ll = line.split('\t')
        fout.write(ll[1]+'\n')
        weights.append(int(ll[2]))
    fin.close()
    fout.close()
    pickle.dump(weights, open('../preprocessedData/brownWords_Weights.p','wb'))
    print 'Done Generating Word File'
    
    # format: key=pos, val=frequency
    _dictPOS_Brown = producePOShistogram(outFilename, text_title = ' from Brown Cluster Words', weights=weights)
    return _dictPOS_Brown

def runPOSTagger(fname):
    p = Popen(['bash',
               'ark-tweet-nlp-0.3.2/runTagger.sh',
               '--output-format' ,
               'pretsv',
               '--no-confidence',
               fname], stdin=PIPE, stdout=PIPE, stderr=PIPE)

    output, err = p.communicate()
    rc = p.returncode
    print 'Done Tagging. Return Code is %d' % rc
    return output

def producePOShistogram(fname, text_title, weights = None):
    output = runPOSTagger(fname)
    ### 
    #listPhrases = pickle.load(open('../preprocessedData/list_cs_phrases.p', 'rb'))
    _dictPOS = {}
    lineNum = 0
    for line in output.splitlines():
        result = line.split('\t')
        #list_tokens = result[0].split(' ')
        list_tags = result[1].split(' ')
        # NOTE: Even though the input per line is one word, it can be interpreted as more than one token
        for tag in list_tags:
            if weights == None:
                increment = 1
            else:
                increment = weights[lineNum]
            if not tag in _dictPOS:
                _dictPOS[tag] = increment
            else:
                _dictPOS[tag] += increment
        lineNum += 1
    tags = POS_KEYS
    listFreq = [None]*len(tags)
    sumTags = 0
    for i in range(len(tags)):
        if tags[i] in _dictPOS:
            listFreq[i] = _dictPOS[tags[i]]
        else:
            listFreq[i] = 0
        sumTags += listFreq[i]
    print 'Total number of tags(tokens) = %d' % sumTags
    for i in range(len(tags)):
        listFreq[i] /= sumTags*1.0
    print listFreq
    print tags
    print type(tags[0])
    df = pd.DataFrame({'POS':tags, 'Density':listFreq})
    p = (ggplot(aes(x='POS',y='Density'), data=df) +
     geom_bar(stat='identity', fill='#729EAB') +
      labs(title='Distribution for Part of Speech of ' + str(sumTags) + ' English Words' + text_title) )
    print p
    return _dictPOS
    

def main():
    pass
    
if __name__ == "__main__":
    #p = histogram_CSLength()
    #(listWords, listPhrases) = listMostFrequent()
    # 1. Tag Tweets with CMU Tweet Tool
    #tagTweets()
    #histogramPOS()
    #histogramPOS_LoneCS()
    
    # 2. Use Stanford NER for Tagging too - (bug in NLTK possibly)
    #NER_Tweets()
    #histogramStanfordNER()
    
    # 3. Sanity Check
    #ob = AnalyzeCSPhrases()
    
    #produceEnglishPOSHistogram()
    produce50mpaths2POSHistogram()