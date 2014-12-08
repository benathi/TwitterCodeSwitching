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
    level = 0.001
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
    
    print 'Betas (Most Positive)'
    for ii in range(100):
        tup = list_significantIndex[ii]
        NGRAMINDEX = 0
        ngram = dict_indexToNgram[tup[NGRAMINDEX]]
        print 'Beta=%f\tN-Gram = %s' % (tup[1],  ngram)
    
    print 'Betas (Most Negative)'
    for ii in range(1,100):
        tup = list_significantIndex[-ii]
        NGRAMINDEX = 0
        ngram = dict_indexToNgram[tup[NGRAMINDEX]]
        print 'Beta=%f\tN-Gram = %s' % (tup[1],  ngram)
    
    return (dict_indexToNgram, list_significantIndex)

def main():
    pass
    
if __name__ == "__main__":
    analyzeSignificantNgrams()