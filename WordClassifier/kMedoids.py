'''
Created on Oct 27, 2014

@author: Ben Athiwaratkun (pa338)

'''
#from __future__ import division
import numpy as np
import random
from nltk.corpus import wordnet as wn


def distanceMetric(mem1, mem2):
    print "Distance Metric Call"
    
    # Needs the same part of speech to compare path similarity
    syns1 = wn.synsets(mem1, pos=wn.ADJ)
    syns2 = wn.synsets(mem2, pos=wn.ADJ)
    print "Word = %r. Synsets = %r" %(mem1, syns1)
    print "Word = %r. Synsets = %r" %(mem2, syns2)
    
    return 1 - wn.path_similarity(syns1[0], syns2[0])


def kMedoids(K, X, distance):
    m = len(X)
    # 1. Initializing Medoids
    # randomize mu to be a list of distinct indices (from 0 to m-1)
    # - This is equivalent to assigning random members to be medoids
    mu = random.sample(xrange(m), K)
    
    
    # 2. initiate cluster_idx which indicates which cluster each observation belongs to
    cluster_idx = np.empty(m, int)
    
    # clusterSize : size of each cluster
    clusterSize = np.empty(K, int)
    epsilon = 0.001 # 0.1 percent
    
    numIterations = 50
    distortions = np.zeros((numIterations))
    
    # new
    
    
    for it in range(numIterations):
        # 1. assign each observation to a cluster based on distance
        # calculate the resulting cost as well
        cost = 0
        
        # clear the assignment
        assignmentDictionary = {}    
        for k in range(K):
            assignmentDictionary[k] = []
        
        for ob in range(m):
            distance_list = np.empty((K))
            for cluster in range(K):
                distance_list[cluster] = distance(X[mu[cluster]], X[ob])
            _clusterNumber = np.argmin(distance_list)
            cluster_idx[ob] = _clusterNumber
            assignmentDictionary[_clusterNumber].append(ob)
            cost += _clusterNumber
        
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
                    #sum_distance_list.append(  (index, sum(np.array([ distance(X[index], X[_other]) 
                    #                                        if cluster_idx[_other] == cluster else 0 
                    #                                        for _other in xrange(m) ]))  )  )
                _sum = sum(np.array([ distance(X[index], X[_other]) for _other in assignmentDictionary[cluster] ]))
                if _sum < minSum:
                    minSum = _sum
                    minIndex = index
            mu[cluster] = minIndex
    
        
    # make sure the distortion function decreases for every iteration
    print(distortions)



def main():
    kMedoids(2, ['simple','elegant','super','chic','fashion','upset','moody','feeling'], distanceMetric)
    
if __name__ == "__main__":
    main()