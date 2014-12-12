'''
Created on Nov 19, 2014

@author: Ben Athiwaratkun (pa338)

'''
#from __future__ import division
import numpy as np
from histogramAnalysis import runPOSTagger, AnalyzeCSPhrases,\
    produceEnglishPOSHistogram, POS_KEYS
import pickle
from histogramAnalysis import produce50mpaths2POSHistogram
from subprocess import Popen, PIPE
import os
import pandas as pd
from ggplot import *

def prepareEngDictByPOS():
    filename = '../Data/BrownClustering/50mpaths2_onlyWords.txt'
    output =  runPOSTagger(filename)
    weights = pickle.load( open('../preprocessedData/brownWords_Weights.p','rb'))
    # key: pos tag
    # value: {V:{'eat':5, 'drink':6} , {N:{'home':10, 'house':11}} }
    dict_eng_by_POS = {}
    for pos in POS_KEYS:
        dict_eng_by_POS[pos] = {}
    
    numLines = 0
    numWords_moreThanOneToken = 0
    for line in output.splitlines():
        weight = weights[numLines]
        numLines += 1
        result = line.split('\t')
        pos = result[1]
        word = result[0]
        #print line
        #print result
        
        # Explicitly ignoring words that are ambiguous (have more than one token)
        if len(pos.split(' ')) > 1:
            numWords_moreThanOneToken += 1
            continue
        
        # Add tag if it doesn't exist
        if not pos in dict_eng_by_POS:
            print "Warning: New Tag Found: %s" % pos
            dict_eng_by_POS[pos] = {}
        if word in dict_eng_by_POS[pos]:
            dict_eng_by_POS[pos][word] += weight
        else:
            dict_eng_by_POS[pos][word] = weight
    
    if numLines != len(weights):
        print 'Error: The number of lines %d and Length of Weights %d Do Not Match' % (numLines,len(weights))
    # tested - correct weight
    pickle.dump(dict_eng_by_POS, open('../preprocessedData/brownWords_dict_byPOS.p','wb'))

# First Version: Only Both(either or)
# New Version: 
def prepareInputBrownCluster(pos_list = ['V','N','A'], either=False):
    if either:
        return prepareInputBrownCluster_EitherOr(pos_list)
    else:
        print 'Preparing Input for Brown Cluster: Both in Dict'
        return prepareInputBrownCluster_Both(pos_list)
    
def prepareInputBrownCluster_Both(pos_list):
    #_, dict_cs_byPOS = AnalyzeCSPhrases()
    dict_cs_byPOS_LW = pickle.load(open('../preprocessedData/dict_cs_byTags_LW.p','rb'))
    dict_eng_byPOS = pickle.load( open('../preprocessedData/brownWords_dict_byPOS.p','rb'))
    
    # Use only the part of speech specified
    combinedDict = {}
    for pos in pos_list: # pos_list = ['V', 'N', 'A'] by default
        for word in dict_cs_byPOS_LW[pos]:
            if not word in combinedDict:
                combinedDict[word] = 0
        for word in dict_eng_byPOS[pos]:
            if not word in combinedDict:
                combinedDict[word] = 0
    #####
    list_words = []
    list_words_notInEng = []
    numWordsCS_Considered_distinct = 0
    numWordsInBoth_distinct = 0
    numWordsCS_Considered = 0
    numWordsInBoth = 0
    
    for pos in pos_list:
        for word in dict_cs_byPOS_LW[pos]:
            numWordsCS_Considered_distinct += 1
            numWordsCS_Considered += dict_cs_byPOS_LW[pos][word]
            # Add to the common list only if 
            # the word in cs is in the Eng Dict
            # note:revert
            word_lower = word.lower() ##### NOTE: This is a quick fix (see it we should change the dict permanently)
            if word_lower in dict_eng_byPOS[pos]:
                numWordsInBoth_distinct += 1
                numWordsInBoth +=  dict_cs_byPOS_LW[pos][word]
                numWordsInBoth +=  dict_eng_byPOS[pos][word_lower]
                list_words.append(word_lower)
            else:
                list_words_notInEng.append(word_lower)
    print 'The Number of Distinct CS Words Considered = %d' % numWordsCS_Considered_distinct
    print 'The Number of Distinct Words in Both CS and Eng Dict = %d' % numWordsInBoth_distinct
    
    print 'The Number of Total CS Words Considerd = %d' % numWordsCS_Considered
    print 'The Number of Words in Both CS/Eng = %d' % numWordsInBoth
    
    print 'List of words that are not in Eng Dict'
    print list_words_notInEng
    
    fname = '../preprocessedData/combinedBrownCS.txt'
    f = open(fname,'wb')
    for word in list_words:
        f.write(word + '\n')
    return (dict_cs_byPOS_LW, dict_eng_byPOS, fname)


def prepareInputBrownCluster_EitherOr(pos_list):
    #_, dict_cs_byPOS = AnalyzeCSPhrases()
    dict_cs_byPOS_LW = pickle.load(open('../preprocessedData/dict_cs_byTags_LW.p','rb'))
    dict_eng_byPOS = pickle.load( open('../preprocessedData/brownWords_dict_byPOS.p','rb'))
    
    # Use only Noun, Verb, Adjective
    combinedDict = {}
    for pos in pos_list: # pos_list = ['V', 'N', 'A'] by default
        for word in dict_cs_byPOS_LW[pos]:
            if not word in combinedDict:
                combinedDict[word] = 0
        for word in dict_eng_byPOS[pos]:
            if not word in combinedDict:
                combinedDict[word] = 0
    ####
    list_words = combinedDict.keys()
    
    fname = '../preprocessedData/combinedBrownCS.txt'
    f = open(fname,'wb')
    for word in list_words:
        f.write(word + '\n')
    return (dict_cs_byPOS_LW, dict_eng_byPOS, fname)






def runBrownCluster(inputFileName, K):
    wbrownFileName = '/Users/ben/Development/GitRepositories/brown-cluster/wcluster'
    p = Popen([wbrownFileName,
               '--text',
               inputFileName,
               '--c',
               str(K)], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    
    output, err = p.communicate()
    rc = p.returncode
    print 'Done Brown Clustering. Return Code is %d' % rc
    print output
    return output

def visualizeHtml():
    pass
    # Ran this command for visualization
    # /Users/ben/Development/GitRepositories/brown-cluster/cluster-viewer/build-viewer.sh 
    #   /Users/ben/Development/CS6742TwitterProject/ParseTweets/combinedBrownCS-c10-p1.out/paths    

def loadClusterResults():
    folder = 'combinedBrownCS-c100-p1.out'    #### CHANGE
    filename = os.path.join(folder, 'paths')
    # format:   key=word, value=cluster
    dict_cluster = {}
    f = open(filename, 'rb')
    for line in f:
        # format of each line:   clusterKey, word, frequency
        result = line.split('\t')
        cluster = result[0]
        word = result[1]
        if not word in dict_cluster:
            dict_cluster[word] = cluster
        else:
            print "Warning: Duplicate Word"
    return dict_cluster

def generateParallelDistribution(pos_list=['V','A','N']): # TODO : Use this POS list
    dict_cs_byPOS_LW = pickle.load(open('../preprocessedData/dict_cs_byTags_LW.p','rb'))
    dict_eng_byPOS = pickle.load( open('../preprocessedData/brownWords_dict_byPOS.p','rb'))
    
    dict_cs = {}
    dict_eng = {}
    for pos in pos_list:
        dict_cs = dict(dict_cs.items() + dict_cs_byPOS_LW[pos].items())
        dict_eng = dict(dict_eng.items() + dict_eng_byPOS[pos].items())
    #dict_cs = dict(  dict_cs_byPOS_LW['V'].items() + 
    #                 dict_cs_byPOS_LW['A'].items() +
    #                 dict_cs_byPOS_LW['N'].items() )
    #dict_eng = dict( dict_eng_byPOS['V'].items() +
    #                 dict_eng_byPOS['A'].items() +
    #                 dict_eng_byPOS['N'].items())
    cs_frequency = {}
    eng_frequency = {}
    dict_cluster = loadClusterResults()
    for word in dict_cluster:
        cluster = dict_cluster[word]
        if word in dict_cs:
            # make sure cluster is a key in cs_frequency
            if cluster not in cs_frequency:
                cs_frequency[cluster] = 0
            cs_frequency[cluster] += dict_cs[word]
        
        if word in dict_eng:
            # make sure cluster is a key in cs_frequency
            if cluster not in eng_frequency:
                eng_frequency[cluster] = 0
            eng_frequency[cluster] += dict_eng[word]
    
    if (len(eng_frequency.keys()) != len(cs_frequency.keys())):
        print 'Number of Clusters for Code-Switching Words and Normal English Tweets Words are not equal'
    
    clusters = eng_frequency.keys()
    
    cs_numWords = sum([cs_frequency[cl] for cl in cs_frequency])
    eng_numWords = sum([eng_frequency[cl] for cl in eng_frequency])
    cs_list = []
    eng_list = []
    for cl in clusters:
        cs_density = cs_frequency[cl]/(1.0*cs_numWords)
        cs_list.append(cs_density)
        
        eng_density = eng_frequency[cl]/(1.0*eng_numWords)
        eng_list.append(eng_density)
    print '[Non-Distinct]Number of CS Words = %d' % cs_numWords
    print '[Non-Distinct]Number of Eng Words = %d' % eng_numWords
    print cs_list
    print eng_list
    
    #### Print sample - Change here
    #format {'cl1':['word1':freq1, 'word2':freq2 ], ['cl2':[]}
    dict_to_consider = dict_cs
    print 'Listing Words in Cluster for CS'
    #print 'Listing Words in Cluster for Eng Dict'
    
    dict_cluster_listWords = {}
    for cl in clusters:
        dict_cluster_listWords[cl] = []
    for word in dict_cluster:
        sumFreq = 0
        if word in dict_to_consider:
            sumFreq += dict_to_consider[word]
        #if word in dict_eng:
        #    sumFreq += dict_eng[word]
        cluster = dict_cluster[word]
        dict_cluster_listWords[cluster].append((word,sumFreq))
    for key in dict_cluster_listWords:
        dict_cluster_listWords[key].sort(key=lambda x: x[1], reverse=True)
    
    
        
    
    
    #### Plot
    Legend = ['Code-Switching']*len(clusters) + ['English-Tweets']*len(clusters)
    aggregate_list = cs_list + eng_list
    ag_clusters = clusters + clusters
    
    
    #ag_clusters_num = [None]*len(ag_clusters)
    #for j in range(len(ag_clusters)):
    #    ag_clusters_num[j] = ag_clusters[j]
    
    ag_clusters_num = [str(i) for i in range(len(clusters))] + [str(i) for i in range(len(clusters))]
    
    
    df = pd.DataFrame({'Cluster':ag_clusters_num,'Density':aggregate_list, 'Legend':Legend})
    p = (ggplot(aes(x='Cluster',y='Density',fill='Legend'), data=df) +
     #geom_bar(stat='identity', fill='#729EAB') +
     geom_bar(stat='identity', position='dodged') +
      labs(title='Density of Cluster for Code-Switching Words and English-Tweet Words') )
    print p
    
    
    for j in range(len(clusters)):
        key = clusters[j]
        _l = dict_cluster_listWords[key]
        print "Sample Words for Cluster %d" % j
        numWords = len(_l)
        print _l[0:min(len,25)]
        
    
    return dict_cluster_listWords
    

if __name__ == "__main__":
    pos_list = ['&','A','O','N','P','R','T','V']
    #prepareEngDictByPOS() # done: saved to pickle
    #dict_cs_byPOS_LW, dict_eng_byPOS, inputFileName_toCluster = prepareInputBrownCluster(pos_list)
    runBrownCluster('/Users/ben/Development/CS6742TwitterProject/preprocessedData/combinedBrownCS.txt', K=100)
    _d = generateParallelDistribution(pos_list)
    