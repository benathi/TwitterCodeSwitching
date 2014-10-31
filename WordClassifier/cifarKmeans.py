## Ben Athiwaratkun (c) 2014
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

print(n);
print(m);


# The number of clusters is specified by the first argument
K = int(sys.argv[1]);

print("Starting");
# initiate mu (matrix of K by n)
# each row indicates the location of a cluster's centroid
# random pick of K points (0 - m-1)
mu = empty(shape=(K,n));
r = random.sample(range(m), K);
for i in range(K): mu[i] = X[r[i]];
# initiate cluster_idx
# indicates which cluster each observation belongs to
cluster_idx = empty(m, int);

# muSize : size of each cluster
muSize = empty(K, int);
epsilon = 0.001; # 0.1 percent
distortions = array([]);

for it in range(50):
	# 1. assign each observation to a cluster based on distance
	# calculate the resulting cost as well
	cost = 0;
	for ob in range(m):
		ds = array([]);
		for c in range(K):
			diff = X[ob] - mu[c];
			ds = append(ds, dot(diff,diff))
		ind_min = indexMin(ds);
		cluster_idx[ob] = ind_min;
		cost += ds[ind_min]
	
	distortions = append(distortions, cost);
	lastIndex = distortions.size - 1;
	percent = (distortions[lastIndex - 1] - distortions[lastIndex])/distortions[lastIndex - 1];
	if( it > 5 and percent < epsilon): break;
	print("Iteration " + str(it) + ".The cost is decreasing by " + str(percent*100) + "%");

	# 2. compute the centroid of each cluster
	# 2.1 accumulate mu[k] with the points that belong to that cluster
	mu *= 0;
	muSize *= 0;
	for ob in range(m):
		k = cluster_idx[ob];
		mu[k] += X[ob];
		muSize[k] += 1;

	# 2.2 average
	for c in range(K):
		if(muSize[c] != 0):
			mu[c] = mu[c]/muSize[c];

	
# make sure the distortion function decreases for every iteration
print(distortions)
#plt.plot(range(ds.size), ds);

#print(mu[0])
# below is the rgb version
print("Below is the reshaped version");

# change to range of K
for k in range(K):
    #print(mu[k]);
    _mu = cast['uint8'](mu[k]).reshape(3,1024);
    #.reshape(32, 32, 3);
    _mu = _mu.transpose();
    #print(_mu);
    _mu = _mu.reshape(32,32,3);
    #print(_mu);
    result = Image.fromarray(_mu, 'RGB');
    name = "Keq" + str(K) + "center" + str(k+1) + ".png";
    result.save(name);
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
            result.save(name);
#result.show();
















