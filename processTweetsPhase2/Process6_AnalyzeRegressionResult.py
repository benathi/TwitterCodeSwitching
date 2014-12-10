# -*- coding: utf-8 -*-
'''
Created on Dec 3, 2014

@author: Ben Athiwaratkun (pa338)

This module is to analyze the Thai n-grams that are significant

'''
import numpy as np
#this dict does not have the index
#from Process4_formatTweetsToSparseMatrix import loadThaiNgram
from Process5_Regression import loadRegressionResult_allData
import sklearn.feature_selection
from Process5_Regression import loadSparseInputMatrix
from Process4_formatTweetsToSparseMatrix import loadSmallNgramDict
import json

def analyzeSignificantNgrams():
    dict_ThaiNgram = loadSmallNgramDict()
    dict_indexToNgram = {}
    for key in dict_ThaiNgram:
        index = dict_ThaiNgram[key]
        #thaiNgram_miniDict = dict_ThaiNgram[key]
        #print thaiNgram_miniDict
        #index = thaiNgram_miniDict['n-gram']
        dict_indexToNgram[index] = key
    print 'Done Processing Inverse Dictionary'
    reg_result = loadRegressionResult_allData()
    X,Y = loadSparseInputMatrix()
    
    coefs = reg_result.coef_[0]
    results = sklearn.feature_selection.univariate_selection.f_regression(X, Y, center=False)
    F_values, p_values =  results
    level = 0.00001
    numSignificant = 0
    numTotal = 0
    numSignificant_pos = 0
    
    list_significantIndex = []
    for i in range(len(coefs)):
        coef_val = coefs[i]
        p_val = p_values[i]
        numTotal += 1
        if p_val < level:
            numSignificant += 1
            tup = (i, coef_val, p_val)
            list_significantIndex.append(tup)
            if coef_val > 0:
                numSignificant_pos += 1
    
    print 'Shape of X'
    print np.shape(X)
    print 'Out of %d Features, %d are significant at %f level' % (numTotal, numSignificant, level)
    print 'The number of positive betas that are significant = %d' % numSignificant_pos
    
    
    ''' Sort by Betas '''
    list_significantIndex.sort(key = lambda x: x[1], reverse=True)
    
    NGRAMINDEX = 0

    print 'Next: Example of Tweets Associated with Positive Significant Betas'    
    print 'Constructing Dict of Significant Positive Ngram'
    dict_sigPosNgram = {}
    for ii in range(100):
        tup = list_significantIndex[ii]
        ngram = dict_indexToNgram[tup[NGRAMINDEX]]
        dict_sigPosNgram[ngram] = {'beta':tup[1],'pval':tup[2],'sampleTweets':[]}
    print 'Done'
    
    
    print 'Constructing Dict of Significant Negative Ngram'
    dict_sigNegNgram = {}
    for ii in range(1,100):
        tup = list_significantIndex[-ii]
        ngram = dict_indexToNgram[tup[NGRAMINDEX]]
        dict_sigNegNgram[ngram] = {'beta':tup[1],'pval':tup[2],'sampleTweets':[]}
    print 'Done'
    
    ftweets = open('../Data/process3/process3.txt','rb')
    numLine = 0
    for line in ftweets:
        #print 'Reading Line %d' % numLine
        numLine += 1
        tweet = json.loads(line)
        ngram_list = tweet['ngram-list']
        for ng in ngram_list:
            if ng in dict_sigPosNgram:
                #print 'n-gram=%s found in Tweet' % ng
                #print tweet['cs-word-list']
                #print 'original text = '
                #print ' '.join(tweet['original-text-list'])
                dict_sigPosNgram[ng]['sampleTweets'].append(( tweet['cs-word-list'] ,' '.join(tweet['original-text-list'])  ))
            if ng in dict_sigNegNgram:
                #print 'n-gram=%s found in Tweet' % ng
                #print tweet['cs-word-list']
                #print 'original text = '
                #print ' '.join(tweet['original-text-list'])
                dict_sigNegNgram[ng]['sampleTweets'].append(( tweet['cs-word-list'] ,' '.join(tweet['original-text-list'])  ))
    print 'Done collecting sample tweets'
    
    
    print 'Betas (Most Positive)'
    for ii in range(100):
        tup = list_significantIndex[ii]
        ngram = dict_indexToNgram[tup[NGRAMINDEX]]
        print 'Beta=%f\tN-Gram = %s\t\tp-val=%e' % (tup[1],  ngram, tup[2])
        print 'Number of Occurrences =', len(dict_sigPosNgram[ngram]['sampleTweets'])
    
    print 'Betas (Most Negative)'
    for ii in range(1,100):
        tup = list_significantIndex[-ii]
        ngram = dict_indexToNgram[tup[NGRAMINDEX]]
        print 'Beta=%f\tN-Gram = %s\t\tp-val=%e' % (tup[1],  ngram, tup[2])
        print 'Number of Occurrences =', len(dict_sigNegNgram[ngram]['sampleTweets'])
    
    
    
    print ''
    for ngram in dict_sigPosNgram.keys()[:20]:
        print '--------------------------------'
        printSampleTweets(ngram, dict_sigPosNgram)
        
    
    return (dict_indexToNgram, list_significantIndex, dict_sigPosNgram)

def printSampleTweets(ngram, dict_sigPosNgram):
    numSamples = len(dict_sigPosNgram[ngram]['sampleTweets'])
    print 'Ngram=%s \t | Beta=%f.p=value=%e. Num samples %d' % (ngram, dict_sigPosNgram[ngram]['beta'], dict_sigPosNgram[ngram]['pval'], numSamples)
    sampleTweetNum = 0
    
    if numSamples < 100:
        print 'Skip.'
        return
    
    for sampleTweet in  dict_sigPosNgram[ngram]['sampleTweets']:
        if len(sampleTweet[0]) > 0:
                
            print 'Sample Tweet No %d. Ngram=%s' % (sampleTweetNum, ngram)
            print sampleTweet[0]
            print sampleTweet[1]
        sampleTweetNum += 1

def main():
    pass
    
if __name__ == "__main__":
    (dict_indexToNgram, list_significantIndex, dict_sigPosNgram) = analyzeSignificantNgrams()