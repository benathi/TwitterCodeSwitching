'''
Created on Nov 23, 2014

@author: Ben Athiwaratkun (pa338)

This file is to analyze Word Net Cluster
'''
#from __future__ import division
#import numpy as np
from histogramAnalysis import AnalyzeCSPhrases
import enchant
import nltk
import pickle
from WordClassifier.kMedoids import kMedoids, wordNetPathSimilarity

#########################
d_enchant = enchant.Dict('en_US')

'''def writeLoneCStokens():
    dict_cs_phrase, dict_cs_tags = AnalyzeCSPhrases()
    pickle.dump(dict_cs_tags, open('../preprocessedData/dict_lone_CS.p','wb'))'''
def loadCSloneWords(tag=None):
    dict_cs =  pickle.load(open('../preprocessedData/dict_cs_byTags_LW.p', 'rb'))
    if tag == None:
        return dict_cs
    else:
        return dict_cs[tag]


### Sanity Check
''' As of now: only words in the dictionary
TODO: Remove any word with number
'''
def testVocabWordNet(pos='V'):
    dict_cs_lone = loadCSloneWords()
    ''' Look at Only Verbs'''
    list_words = [key for key in dict_cs_lone[pos]]
    new_cs_dict = {}
    
    numInDict = 0
    for word in list_words:
        print '----------------------------'
        print word
        inDict = d_enchant.check(word)
        numInDict += inDict
        print "In Dictionary?", d_enchant.check(word)
        if inDict:
            #if word[1:].islower():
            print 'Adding this word'
            word_low = word.lower()
            if word_low in new_cs_dict:
                new_cs_dict[word_low] += dict_cs_lone[pos][word]
            else:
                new_cs_dict[word_low] = dict_cs_lone[pos][word]
        else:
            suggested_word = d_enchant.suggest(word)
            print "Suggested Word", suggested_word
            #if len(suggested_word) != 0:
                #if suggested_word[0] in word:
                #    print 'Adding This Word'
                #    list_words_new.append(suggested_word[0])
            
    #numInDict /= 1.0*len(list_words)
    #print 'Proportion of Words in Dictionary = %f. Out of %d' % (numInDict, len(list_words))
    print 'Number of All Words = %d' % len(list_words)
    #print 'Number of Words in Dictionary = %d', numInDict
    print 'Number of Words in Final List = %d' % len(new_cs_dict.keys())
    return new_cs_dict


def clusterWords():
    pos = 'V'
    dictVerb = testVocabWordNet(pos=pos)
    list_verbs = dictVerb.keys()
    print 'Starting K-Medoid Cluster'
    kMedoids(30, list_verbs, wordNetPathSimilarity)

#########################

def main():
    pass

if __name__ == "__main__":
    #new_cs_dict = testVocabWordNet('V')
    #print new_cs_dict.keys()
    clusterWords()