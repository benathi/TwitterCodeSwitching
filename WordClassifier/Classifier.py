'''
Created on Oct 26, 2014

@author: Ben Athiwaratkun (pa338)

'''
#from __future__ import division
import numpy as np
#from sklearn.cluster import KMeans
#from sklearn import linear_model as lm
#from sklearn import svm
#from scipy import stats

def classifierKMeans(k, data, **kwargs):
    # returns a function that takes a word (or list of words?) and predict which category it is in
    # needs a list of categories too
    pass
    # 1. What metric for distance?
    # 1.1 Try 1 - path_similarity
    
    # 2. Use Kmeans to classify
    #km = KMeans(init='k-means++', n_clusters=k)
    



def main():
    classifierKMeans(5, ['simple','elegant','iPhone','time lapse','super','chic','fashion','upset','mood','feeling'])
    
if __name__ == "__main__":
    main()