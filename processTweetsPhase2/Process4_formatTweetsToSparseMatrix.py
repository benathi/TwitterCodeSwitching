'''
Created on Nov 29, 2014

@author: Ben Athiwaratkun (pa338)

'''
#from __future__ import division
import numpy as np
import pickle
import pandas as pd
from ggplot import *
#import sklearn.linear_model.LogisticRegression
from scipy import sparse
import random
NUM_LINES = 1892532
import json

def loadThaiNgram():
    dict_ngram = pickle.load(open('../Data/process3/dict_ngram.p','rb'))
    print 'Done Loading N-Gram Dict'
    return dict_ngram

def loadCSdict():
    return pickle.load(open('../Data/process3/dict_cs.p','rb'))

def analyzeThaiNgram():
    dict_ngram = loadThaiNgram()
    totalNumOccur = 0
    totalNumGreater_ten = 0
    dict_histogram = {}
    #for i in range(1,100):
    #    dict_histogram[i] = 0
    
    for ngram in dict_ngram:
        cs = dict_ngram[ngram]['cs']
        non_cs = dict_ngram[ngram]['non-cs']
        sum = cs + non_cs
        #dict_histogram[sum] += 1
        if sum in dict_histogram:
            dict_histogram[sum] += 1
        else:
            dict_histogram[sum] = 1
            
        totalNumOccur += sum
        totalNumGreater_ten += 1 if sum >= 10 else 0
    print 'Total Number of Occurrences = %d' % totalNumOccur
    print 'The Number of n-gram occuring >= 10 = %d', totalNumGreater_ten
    print 'The Number of n-grams = %d', len(dict_ngram.keys()) 
    
    x = dict_histogram.keys()
    y = [dict_histogram[i] for i in x]
    
    df = pd.DataFrame({'x':x,'y':y})
    p = (ggplot(aes(x='x',y='y'), data=df) +
     #geom_bar(stat='identity', fill='#729EAB') +
     #geom_bar(stat='identity') +
     geom_histogram(stat='bar') +
      labs(title='Distribution of Cluster for Code-Switching Words and English-Tweet Words',
           x='Number of Occurrences of N-Gram in Tweets',
           y='Frequency') )
    
    
    print p
    
    '''
    Note: number of n-grams = 
    '''
    #################
    return (dict_ngram, dict_histogram)

def obtainNgramDict():
    ''' Cut off = 10 '''
    dict_ngram = loadThaiNgram()
    # format
    # key = n-gram. Value = feature id (which column of X matrix)
    dict_ngram_filtered = {}
    index = 0
    for ngram in dict_ngram:
        cs = dict_ngram[ngram]['cs']
        non_cs = dict_ngram[ngram]['non-cs']
        sum = cs + non_cs
        if sum >= 10:
            dict_ngram_filtered[ngram] = index
            index += 1
    pickle.dump(dict_ngram_filtered,open('../Data/process4/NgramDictAbove10.p','wb'))

def loadSmallNgramDict50():
    dict_ngram_filtered = pickle.load(open('../Data/process4/NgramDictAbove50.p','rb'))
    print 'Finished Loading Ngram'
    return dict_ngram_filtered    
    
def loadSmallNgramDict():
    dict_ngram_filtered = pickle.load(open('../Data/process4/NgramDictAbove10.p','rb'))
    print 'Finished Loading Ngram'
    return dict_ngram_filtered

def makeSparseFeatureMatrix():
    ''' This method read tweets generate a sparse matrix (to be used for regression)'''
    # also needs y vector (1 for code-switch, 0 for non code-switch)
    dict_ngram = loadSmallNgramDict()
    numFeatures = len(dict_ngram.keys())
    X = sparse.lil_matrix((NUM_LINES,numFeatures), dtype=np.bool)
    Y = sparse.lil_matrix((NUM_LINES,1), dtype=np.bool)
    
    fin = open('../Data/process3/process3.txt', 'rb')
    numRow = 0
    for line in fin:
        print 'Processing Line %d' % numRow
        tweet = json.loads(line)
        ngram_list = tweet['ngram-list']
        # record y
        Y[numRow,0] = (len(tweet['cs-word-list']) > 0)
        # record X
        for ngram in ngram_list:
            if ngram in dict_ngram:
                _feat_index = dict_ngram[ngram]
                X[numRow, _feat_index] = True
        numRow += 1
        #if numRow >= 1000:
        #    break
    print 'Finished Reading Lines'
    X = X.tocsr()
    Y = Y.tocsr()
    pickle.dump((X,Y), open('../Data/process4/sparseInputMatrix.p', 'wb'))


def testSparseMatrix():
    ''''x = np.zeros((1,100))
    print np.shape(x)
    for i in range(100):
        x[0,i] = (random.random() > 0.8)
    print x
    
    x_sparse = sparse(x)
    print x_sparse'''
    numLines = 3
    numFeatures = 10
    mtx = sparse.csr_matrix((numLines,numFeatures), dtype=np.bool)
    print mtx
    mtx[0,0] = True # got a warning saying this is inefficient. 
    # lil_matrix is more efficient for constructing sparse matrix incrementally
    print mtx.todense()
    
    mtl = sparse.lil_matrix((numLines,numFeatures), dtype=np.bool)
    mtl[0,0] = True
    print mtl.todense()
    
    
    mt_csr = mtl.tocsr()
    print mt_csr.todense()
    # consider copy lil_matrix format to another format when done?
    # Convert to CSR (converting is recommended by scipy specificication)

def test_analyzeSmallNgram():
    dict_ngramSmall = loadSmallNgramDict()
    print 'The number of keys = %d' % len(dict_ngramSmall.keys())

def main():
    pass
    
if __name__ == "__main__":
    (dict_ngram, dict_histogram) = analyzeThaiNgram()
    #obtainNgramDict()
    #testSparseMatrix()
    #makeSparseFeatureMatrix()
    