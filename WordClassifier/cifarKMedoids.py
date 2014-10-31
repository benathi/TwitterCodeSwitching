## Ben Athiwaratkun (cluster) 2014
## Practical 1 Warm Up : E-181
## K-means

from numpy import *
import cPickle
import random
import sys
from PIL import Image
# make sure matplotlib is installed
#import matplotlib.image as img
#import matplotlib.pyplot as plt
import numpy as np

# load the data
def unpickle(f):
	fo = open(f,'rb')
	dict = cPickle.load(fo);
	fo.close();
	return dict;

def indexMin(vec):
	min_d = float('inf');
	idx = -1;
	for i in range(vec.size):
		if(vec[i] < min_d):
			min_d = vec[i];
			idx = i;
	return idx;


def distance(mem1, mem2):
	diff = mem1 - mem2
	return np.dot(diff,diff)

''' main() '''

dict = unpickle("cifar-10-batches-py/data_batch_1");
X = dict.get("data");
# int32 can hold 255*255*1024*3
X = cast['int32'](X)
m = X.shape[0];
n = X.shape[1];
# the length of each row is 1024*3
# first 1024 elements is R component in row-major
# next 1024 G and B

print 'dimension for each point = %d'% n
print 'The number of Points = %d'% m


# The number of clusters is specified by the first argument
K = int(sys.argv[1]);

print("Starting");


# 1. Initializing Medoids
# randomize mu to be a list of distinct indices (from 0 to m-1)
# - This is equivalent to assigning random members to be medoids
mu = random.sample(xrange(m), K)


# 2. initiate cluster_idx which indicates which cluster each observation belongs to
cluster_idx = empty(m, int)

# clusterSize : size of each cluster
clusterSize = empty(K, int)
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
				#										if cluster_idx[_other] == cluster else 0 
				#										for _other in xrange(m) ]))  )  )
			_sum = sum(np.array([ distance(X[index], X[_other]) for _other in assignmentDictionary[cluster] ]))
			if _sum < minSum:
				minSum = _sum
				minIndex = index
		mu[cluster] = minIndex

	
# make sure the distortion function decreases for every iteration
print(distortions)
#plt.plot(range(distance_list.size), distance_list);

#print(mu[0])
# below is the rgb version
print("Below is the reshaped version");

# change to range of K
for k in range(K):
    #print(mu[k]);
    _mu = cast['uint8'](X[mu[k]]).reshape(3,1024);
    #.reshape(32, 32, 3);
    _mu = _mu.transpose();
    #print(_mu);
    _mu = _mu.reshape(32,32,3);
    #print(_mu);
    result = Image.fromarray(_mu, 'RGB');
    name = "Keq" + str(K) + "center" + str(k+1) + ".png";
    result.save('TestData/Clusters/' +name);
#result.show();



for k in range(K):
## saves 9 images that belong to each cluster
    count = 0;
    for i in range(m):
        if(count == 9):
            break;
        elif (cluster_idx[i] == k):
            count += 1;
            print(X[i])
            _im = cast['uint8'](X[i]).reshape(3,1024);
            _im = _im.transpose();
            _im = _im.reshape(32,32,3);
            result = Image.fromarray(_im, 'RGB');
            name = "Keq" + str(K) + "cluster" + str(k+1) + "sample" + str(count+1) + ".png";
            result.save('TestData/ClusterSamples' + name);
#result.show();
