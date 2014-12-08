'''
Created on Nov 25, 2014

@author: Ben Athiwaratkun (pa338)

We model the occurrences of words as multinomial distribution:
    - Find words that occur more often compared to the English cluster
'''
#from __future__ import division
#import numpy as np
import pickle
import enchant
import pandas as pd
from ggplot import *
import math
'''
Input: CS Dictionary and Eng Dictionary. Also take part of speech as input.
Input Format: CS Dictionary and Eng Dictionary are POS Dict

Output: Words that occurs relatively often.
'''

def analyzeWordFrequency(pos_list=[], verbose=False):
    dict_cs_byPOS_LW = pickle.load(open('../preprocessedData/dict_cs_byTags_LW.p','rb'))
    dict_eng_byPOS = pickle.load( open('../preprocessedData/brownWords_dict_byPOS.p','rb'))
    
    # Consider words that occur in both
    dict_combined = {}
    totalNumCS = 0
    totalNumEng = 0
    for pos in pos_list:
        if verbose: print 'Consider POS', pos
        for word in dict_cs_byPOS_LW[pos]:
            if verbose: print '\tWord=', word
            word_lower = word.lower()
            if word_lower in dict_eng_byPOS[pos]:
                if verbose: print '\tIn Both'
                if not word_lower in dict_combined:
                    dict_combined[word_lower] = {'cs':0,'eng':0}
                dict_combined[word_lower]['cs'] += dict_cs_byPOS_LW[pos][word]
                totalNumCS += dict_cs_byPOS_LW[pos][word]
                dict_combined[word_lower]['eng'] += dict_eng_byPOS[pos][word_lower]
                totalNumEng += dict_eng_byPOS[pos][word_lower]
    print 'The number of distinct words considered = %d' % len(dict_combined.keys())
    print 'Total Number of Non-Distinct Words: CS=\t' , totalNumCS
    print 'Total Number of Non-Distinct Words: Eng=\t' , totalNumEng
    
    ### Calculate frequency
    for word in dict_combined:
        dict_combined[word]['cs-density'] = dict_combined[word]['cs']/(1.0*totalNumCS)
        dict_combined[word]['eng-density'] = dict_combined[word]['eng']/(1.0*totalNumEng)
        dict_combined[word]['ratio-density'] = dict_combined[word]['cs-density']/dict_combined[word]['eng-density']
        ## What other metric can we do
    
    d_enchant = enchant.Dict('en_US')
    list_words_extremeFrequency = []
    for word in dict_combined:
        # If the count is non-trivial
        if dict_combined[word]['cs'] >= 10:
            if dict_combined[word]['ratio-density'] >= 5 or dict_combined[word]['ratio-density'] <= 0.2:
                #print 'Word:%s\tDensity Ratio:%f' % (word, dict_combined[word]['ratio-density'])
                list_words_extremeFrequency.append( (word, 
                                                     dict_combined[word]['cs'],
                                                     dict_combined[word]['eng'],
                                                     dict_combined[word]['ratio-density']))
    ########### Print Sample Words
    RATIO_DENSITY = 3
    list_words_extremeFrequency.sort(key=lambda x: x[RATIO_DENSITY], reverse=True)
    for tuple in list_words_extremeFrequency:
        if d_enchant.check(tuple[0]):
            print tuple
    
    ########### Scatter Plot
    x = []
    y = []
    word_list = []
    log_ratioDensity = []
    
    for word in dict_combined:
        print 'word=', word
        # This number can be controlled for significance
        # Possible to use other metric
        if dict_combined[word]['cs'] >= 50: 
            if dict_combined[word]['ratio-density'] >= 4 or dict_combined[word]['ratio-density'] <= 0.25:
                if d_enchant.check(word):
                    word_list.append(word)
                    x.append(math.log(dict_combined[word]['eng-density']))
                    y.append(math.log(dict_combined[word]['cs-density']))
                    log_ratioDensity.append( 1+ math.pow(dict_combined[word]['ratio-density'], 0.25))
    print log_ratioDensity
    FACTOR=1000
    nn = len(x)*FACTOR
    controlLine = [math.log(i/(1.0*nn)) for i in xrange(1,nn+1,FACTOR)]
    print controlLine
    df2 = pd.DataFrame({'ControlLine':controlLine})
    df = pd.DataFrame({'x':x,'y':y, 'Word':word_list,
                       'Size':log_ratioDensity, 'ControlLine':controlLine})
    p = (ggplot(aes(x='x',y='y'), data=df) +
     #geom_bar(stat='identity', fill='#729EAB') +
     #geom_point() +
    geom_text( aes(size=10,label='Word'), color='#88aa55') + 
    geom_line(aes(x='ControlLine',y='ControlLine', color='#552255'), size=3, alpha=0.5) + 
    labs(title='Density of English Words and Code-Switching Words')  + 
      xlab("Log Probability of English Word") +
      ylab("Log Probability of Code-Switching Word")
      )
    print p
    
    return dict_combined
    
    

    
if __name__ == "__main__":
    pos_list = ['&','A','O','N','P','R','T','V']
    dict_combined = analyzeWordFrequency(pos_list)