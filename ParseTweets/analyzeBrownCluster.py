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

def prepareInputBrownCluster():
    
    #_, dict_cs_byPOS = AnalyzeCSPhrases()
    dict_cs_byPOS_LW = pickle.load(open('../preprocessedData/dict_cs_byTags_LW.p','rb'))
    dict_eng_byPOS = pickle.load( open('../preprocessedData/brownWords_dict_byPOS.p','rb'))
    
    # Use only Noun, Verb, Adjective
    combinedDict = {}
    for pos in ['V','N','A']:
        for word in dict_cs_byPOS_LW[pos]:
            if not word in combinedDict:
                combinedDict[word] = 0
        for word in dict_eng_byPOS[pos]:
            if not word in combinedDict:
                combinedDict[word] = 0
    #####
    fname = '../preprocessedData/combinedBrownCS.txt'
    f = open(fname,'wb')
    for word in combinedDict:
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
    folder = 'combinedBrownCS-c10-p1.out'
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

def generateParallelDistribution():
    dict_cs_byPOS_LW = pickle.load(open('../preprocessedData/dict_cs_byTags_LW.p','rb'))
    dict_eng_byPOS = pickle.load( open('../preprocessedData/brownWords_dict_byPOS.p','rb'))
    dict_cs = dict(  dict_cs_byPOS_LW['V'].items() + 
                     dict_cs_byPOS_LW['A'].items() +
                     dict_cs_byPOS_LW['N'].items() )
    dict_eng = dict( dict_eng_byPOS['V'].items() +
                     dict_eng_byPOS['A'].items() +
                     dict_eng_byPOS['N'].items())
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
    print 'Number of CS Words = %d' % cs_numWords
    print 'Number of Eng Words = %d' % eng_numWords
    print cs_list
    print eng_list
    
    #### Print sample
    #format {'cl1':['word1':freq1, 'word2':freq2 ], ['cl2':[]}
    dict_cluster_listWords = {}
    for cl in clusters:
        dict_cluster_listWords[cl] = []
    for word in dict_cluster:
        sumFreq = 0
        if word in dict_cs:
            sumFreq += dict_cs[word]
        #if word in dict_eng:
        #    sumFreq += dict_eng[word]
        cluster = dict_cluster[word]
        dict_cluster_listWords[cluster].append((word,sumFreq))
    for key in dict_cluster_listWords:
        dict_cluster_listWords[key].sort(key=lambda x: x[1], reverse=True)
    
    for key in dict_cluster_listWords:
        _l = dict_cluster_listWords[key]
        print "Sample Words for Cluster %s" % key
        numWords = len(_l)
        print _l[0:min(len,25)]
    
    #### Plot
    Legend = ['Code-Switching']*len(clusters) + ['English-Tweets']*len(clusters)
    aggregate_list = cs_list + eng_list
    ag_clusters = clusters + clusters
    
    df = pd.DataFrame({'Cluster':ag_clusters,'Density':aggregate_list, 'Legend':Legend})
    p = (ggplot(aes(x='Cluster',y='Density',fill='Legend'), data=df) +
     #geom_bar(stat='identity', fill='#729EAB') +
     geom_bar(stat='identity', position='Legend') +
      labs(title='Distribution of Cluster for Code-Switching Words and English-Tweet Words') )
    print p
    
    
    
    return dict_cluster_listWords
    

if __name__ == "__main__":
    pass
    #prepareEngDictByPOS() # done: saved to pickle
    #dict_cs_byPOS_LW, dict_eng_byPOS, inputFileName_toCluster = prepareInputBrownCluster()
    #runBrownCluster('/Users/ben/Development/CS6742TwitterProject/preprocessedData/combinedBrownCS.txt', K=10)
    _d = generateParallelDistribution()
    