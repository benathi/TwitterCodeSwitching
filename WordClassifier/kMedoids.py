'''
Created on Oct 27, 2014

@author: Ben Athiwaratkun (pa338)

'''
#from __future__ import division
import numpy as np
import random
from nltk.corpus import wordnet as wn
import math

'''def wordNetPathSimilarity(mem1, mem2):
    print "Distance Metric Call"
    
    # Needs the same part of speech to compare path similarity
    syns1 = wn.synsets(mem1, pos=wn.ADJ)
    syns2 = wn.synsets(mem2, pos=wn.ADJ)
    print "Word = %r. Synsets = %r" %(mem1, syns1)
    print "Word = %r. Synsets = %r" %(mem2, syns2)
    
    return 1 - wn.path_similarity(syns1[0], syns2[0])'''


''' TODO - Filter only exact word?'''
def wordNetPathSimilarity(word1, word2, pos='v'):
    #print "Distance Metric Call for (%r, %r)" % (word1, word2)
    #print "Using Path Similarity"
    # Needs the same part of speech to compare path similarity
    syns1 = wn.synsets(word1, pos)
    syns2 = wn.synsets(word2, pos)
    list_sim = [0]
    for syn1 in syns1:
        for syn2 in syns2:
            #if syn1.pos() == syn2.pos():
            #print "Word = %r. Synset = %r" %(word1, syn1)
            #print "Word = %r. Synset = %r" %(word2, syn2)
            _sim = wn.path_similarity(syn1, syn2)
            if not _sim  == None:
                #print "Path Similarity for (%r, %r) is %f" % (syn1, syn2, _sim)
                list_sim.append(_sim)
    #print list_sim
    #print "The Average Similarity is %f" % np.mean(list_sim)
    #print "The Maximum Similarity is %f" % np.max(list_sim)
    
    return (1-np.mean(list_sim))
    #return math.sqrt(1-np.max(list_sim))


def kMedoids(K, X, distanceFunction):
    m = len(X)
    # 1. Initializing Medoids
    # randomize mu to be a list of distinct indices (from 0 to m-1)
    # - This is equivalent to assigning random members to be medoids
    #mu = random.sample(xrange(m), K)
    mu = [None]*K
    # 1.1 An option is to do KMeans++ to help with initialization
    print 'Starting KMeans'
    for k in range(K):
        if k==0:
            mu[k] = random.randint(0,K-1)
        else:
            distanceList = [None]*m
            forbiddenList = mu[:k]
            for el in range(m):
                if not el in forbiddenList:
                    #print mu[k-1]
                    #print el
                    distanceList[el] = distanceFunction(X[mu[k-1]], X[el])
                else:
                    distanceList[el] = -1
            pickIndex = np.argmax(distanceList)
            mu[k] = pickIndex
        print 'k=%d. Medoid=%s' % (k, X[mu[k]])
    print 'Done with KMeans Initialization'
    
    
    
    
    
    
    
    
    
    
    
    
    # 2. initiate cluster_idx which indicates which cluster each observation belongs to
    cluster_idx = np.zeros(m, int)
    epsilon = 0.1
    numIterations = 50
    distortions = np.zeros((numIterations))
    #format: key=cluster number. value= [index of elements belonging to the cluster]
    assignmentDictionary = {}    
    
    for it in range(numIterations):
        # 1. assign each observation to a cluster based on distanceFunction
        # calculate the resulting cost as well
        cost = 0
        
        # clear the assignment
        assignmentDictionary = {}    
        for k in range(K):
            assignmentDictionary[k] = []
        
        print 'mu =', mu
        print 'Medoids are'
        print [X[i] for i in mu]
        print 'Phase1: Assign Cluster'
        for ob in range(m):
            print 'Word = ',  X[ob]
            distance_list = np.empty((K))
            for cluster in range(K):
                distance_list[cluster] = distanceFunction(X[mu[cluster]], X[ob])
            print distance_list
            _clusterNumber = np.argmin(distance_list)
            print 'Picking Cluster ' % _clusterNumber
            cluster_idx[ob] = _clusterNumber
            assignmentDictionary[_clusterNumber].append(ob)
            cost += distance_list[_clusterNumber]
        distortions[it] = cost
        
        #listIndex = it
        if it > 0:
            percent = (distortions[it - 1] - distortions[it])/distortions[it - 1];
            print("Iteration " + str(it) + ".The cost is decreasing by " + str(percent*100) + "%");
        if( it > 5 and percent < epsilon): 
            break;
            
    
        # 2. compute the medoid of each cluster
        # 2.1 accumulate mu[k] with the points that belong to that cluster
        for cluster in range(K):
            print "Computing Medoid for Cluster %d", cluster
            sum_distance_list = []
            minIndex = -1
            minSum = 2 << 31
            for index in assignmentDictionary[cluster]:
            #for index in xrange(m):
                print "\tCluster %d Index %d" % (cluster, index)
                #if cluster_idx[index] == cluster:
                    #sum_distance_list.append(  (index, sum(np.array([ distanceFunction(X[index], X[_other]) 
                    #                                        if cluster_idx[_other] == cluster else 0 
                    #                                        for _other in xrange(m) ]))  )  )
                _sum = sum(np.array([ distanceFunction(X[index], X[_other]) for _other in assignmentDictionary[cluster] ]))
                if _sum < minSum:
                    minSum = _sum
                    minIndex = index
            mu[cluster] = minIndex


        
        #print "Iteration %d"  % it
        #print assignmentDictionary
        
    # make sure the distortion function decreases for every iteration
    print distortions
    print "Done with K Medoid"
    for cluster in assignmentDictionary:
        members = [X[index] for index in assignmentDictionary[cluster]]
        print "Cluster %d. Medoid=%s" % (cluster, X[mu[cluster]])
        print members




def main():
    pass
    ## Need to change part of speech
    #kMedoids(2, ['simple','elegant','super','chic','fashion','upset','moody','feeling'], wordNetPathSimilarity)
    #kMedoids(2, ['simple','elegant','super','chic','fashion','upset','moody','feeling'], wordNetPathSimilarity)
    #kMedoids(3, ['eat','walk','drink','travel','roam','sleep','cook','shower','mad'], wordNetPathSimilarity)
    theList = ['represent', 'revoke', 'forget', 'pardon', 'skip',
                'focus', 'unblock', 'go', 'follow', 'hate', 'sung', 
                'consider', 'graves', 'tweet', 'send', 'dissatisfied',
                'preserved', 'recycle', 'smile', 'dislike', 'pleasing',
                'restock', 'sent', 'uploaded']
    kMedoids(5, theList, wordNetPathSimilarity)
    
if __name__ == "__main__":
    main()