'''
Created on Nov 29, 2014

@author: Ben Athiwaratkun (pa338)

Sunday Nov 30th.
Did part of the analysis. The cross-validation score are super high. 
However, this might due to the disproportionately high non code-switch

Next:
Continue Analyzing Precision / Recall
'''
#from __future__ import division
import numpy as np
import pickle
from scipy import sparse
from sklearn import linear_model
import sklearn.feature_selection
import sklearn.metrics
from sklearn.svm.libsvm import cross_validation
from sklearn import cross_validation

def loadSparseInputMatrix():
    X,Y = pickle.load( open('../Data/process4/sparseInputMatrix.p', 'rb'))
    Y = np.asarray(Y.todense()).ravel()
    print 'Done Loading X,Y'
    return (X,Y)

def performRegression():
    X,Y = loadSparseInputMatrix()
    logreg = linear_model.LogisticRegression()
    reg_result = logreg.fit(X,Y)
    print 'Done with Regression'
    coef = reg_result.coef_[0]
    for i in range(len(coef)):
        if abs(coef[i]) > 0.000000000001:
            print 'Feature Index %d. Beta = %f' % (i,coef[i])
    pickle.dump(reg_result, open('../Data/process5/regressionResult.p', 'wb'))
    print 'The number of Features is ', len(coef)

def analyzeRegressionResult():
    reg_result = pickle.load(open('../Data/process5/regressionResult.p', 'rb'))
    print 'The Regression Intercept is' , reg_result.intercept_
    X,Y = loadSparseInputMatrix()
    #sse = np.sum( (reg_result.predict(X) - Y)**2, axis=0)/float(X.shape[0] - X.shape(1) - 1) # another -1 for parameter
    results = sklearn.feature_selection.univariate_selection.f_regression(X, Y, center=False)
    F_values, p_values =  results
    level = 0.001
    numSignificant = 0
    numTotal = 0
    for p_val in p_values:
        numTotal += 1
        if p_val < level:
            numSignificant += 1
            print p_val
    
    print 'Out of %d Features, %d are significant at %f level' % (numTotal, numSignificant, level)
    
    predict_Y = reg_result.predict(X)
    ac_scores = sklearn.metrics.accuracy_score(Y, predict_Y)
    print 'The Fraction of Correctly Classified Samples = %f' % ac_scores
    ## got 0.991494 - no way -- this is too high!
    
    print 'Number of Samples = %d' % len(Y)
    print 'Number of Code-Switching Instances = %d' % sum(Y)
    print 'Number of Predicting Code-Switching = %d' % sum(predict_Y)
    '''
    Number of Samples = 1892532
    Number of Code-Switching Instances = 35156
    Number of Predicting Code-Switching = 19418
    '''
    
    return results

def testCrossValidation():
    X,Y = loadSparseInputMatrix()
    ## Cross Validation
    print 'Start Performing Cross Validation'
    logreg = linear_model.LogisticRegression()
    scores = cross_validation.cross_val_score(logreg, X, Y, cv=2)
    print scores
    ''' Result
        [ 0.98871353  0.98851697]
    '''
    ## Might be high because it's almost always 0
    

def testRegression():
    X = sparse.lil_matrix((4,10), dtype=np.bool)
    Y = sparse.lil_matrix((4,1), dtype=np.bool)
    Y[0,0] = True
    Y[2,0] = True
    X[0,2] = True
    X[1,1] = True
    X[3,4] = True
    
    
    X = X.tocsr()
    Y = np.asarray(Y.todense()).ravel()
    print Y
    print np.unique(Y, return_inverse=True)
    
    logreg = linear_model.LogisticRegression()
    reg_result = logreg.fit(X,Y)
    print reg_result.get_params()
    print reg_result.coef_



    

def main():
    pass
    #testRegression()
    #performRegression()
    analyzeRegressionResult()
    #testCrossValidation()
    
if __name__ == "__main__":
    main()
    #results = analyzeRegressionResult()