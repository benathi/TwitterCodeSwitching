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


def CV_determineOptimalLambda():
    X,Y = loadSparseInputMatrix()
    for penalty in ['l1','l2']:
        for regParam in [np.exp(i) for i in [-4,-3,-2,-1,0,1,2,3,4]]:
            print 'Penalty', penalty
            print 'Regularization Parameter = %e' % regParam
            logreg = linear_model.LogisticRegression(penalty=penalty,C=(1.0/(1.0*regParam)))
            scores = cross_validation.cross_val_score(logreg, X, Y, cv=5)
            print np.mean(scores)
            print np.std(scores)
        print '----------------------'

def performRegression():
    X,Y = loadSparseInputMatrix()
    logreg = linear_model.LogisticRegression(penalty='l1',C=(1.0/(np.exp(1.0)))) # can change to l1
    reg_result = logreg.fit(X,Y)
    print 'Done with Regression'
    coef = reg_result.coef_[0]
    #for i in range(len(coef)):
    #    if abs(coef[i]) > 0.000000000001:
    #        print 'Feature Index %d. Beta = %f' % (i,coef[i])
    pickle.dump(reg_result, open('../Data/process5/regressionResult.p', 'wb'))
    print 'The number of Features is ', len(coef)
    
def loadRegressionResult_allData():
    reg_result = pickle.load(open('../Data/process5/regressionResult.p', 'rb'))
    print 'Done Loading Regression Result - [All Data]'
    return reg_result


def analyzeRegressionSignificance():
    reg_result = loadRegressionResult_allData()
    print 'The Regression Intercept is' , reg_result.intercept_
    X,Y = loadSparseInputMatrix()
    
    numFeatures = np.shape(X)[1]
    print 'Number of features = ', numFeatures
    
    coefs = reg_result.coef_[0]
    results = sklearn.feature_selection.univariate_selection.f_regression(X, Y, center=False)
    F_values, p_values =  results
    #level = 0.01/numFeatures
    level = 0.001
    numSignificant = 0
    numTotal = 0
    numSignificant_pos = 0
    
    print 'Testing at Level %e' % level
    #for p_val in p_values:
    for i in range(len(coefs)):
        coef_val = coefs[i]
        p_val = p_values[i]
        numTotal += 1
        if p_val < level:
            numSignificant += 1
            '''print p_val'''
            if coef_val > 0:
                numSignificant_pos += 1
    
    
    print 'The number of cs in labels = %d', sum(Y)
    print 'baseline predictor accuracy = %f', (1-sum(Y)/(1.0*len(Y)))
    
    
    print 'Shape of X'
    print np.shape(X)
    print 'Out of %d Features, %d are significant at %e level' % (numTotal, numSignificant, level)
    print 'The number of positive betas that are significant = %d' % numSignificant_pos


def performRegressionSliced(numFold=5):
    X,Y = loadSparseInputMatrix()
    logreg = linear_model.LogisticRegression(penalty='l1',C=(1.0/(np.exp(-1.0)))) # can change to l1
    m = len(Y)
    m_regress = m - int(m/numFold)
    newX = X[:m_regress]
    newY = Y[:m_regress]
    print 'Done Slicing X,Y'
    reg_result = logreg.fit(X,Y)
    print 'Done with Regression'
    pickle.dump(reg_result, open('../Data/process5/regressionResultCV5fold.p', 'wb'))

def analyzeRegressionPredicintingStatistics(numFold=5):
    reg_result = pickle.load(open('../Data/process5/regressionResultCV5fold.p', 'rb'))
    XX,YY = loadSparseInputMatrix()
    m = len(YY)
    m_regress = m-int(m/numFold)
    Xtest = XX[m_regress:]
    Ytest = YY[m_regress:]
    
    print '-----------------------------------'
    predict_Y = reg_result.predict(Xtest)
    ac_scores = sklearn.metrics.accuracy_score(Ytest, predict_Y)
    print 'The Fraction of Correctly Classified Samples = %f' % ac_scores
    print 'Performance of Flat Predictor (0 for all) = %f' % (1.0 - (sum(Ytest)/(1.0*len(Ytest))))
    ## got 0.991494 - no way -- this is too high!
    
    print 'Number of Samples = %d' % len(Ytest)
    print 'Number of Code-Switching Instances = %d' % sum(Ytest)
    print 'Number of Predicting Code-Switching = %d' % sum(predict_Y)

     
    
    _fResults = sklearn.metrics.precision_recall_fscore_support(Ytest, predict_Y)
    _precision, _recall, _fbeta_score, _support = _fResults
    
    print 'Precision =', _precision
    print 'Recall =', _recall
    print 'Fbeta Score =', _fbeta_score
    print 'Support', _support



#################################################################################
#################################################################################
#################################################################################
#################################################################################
### OLD CODE ###
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
    #CV_determineOptimalLambda()
    pass
    #performRegression()
    #analyzeRegressionSignificance()
    ''' CV '''
    print 'Test----------------------'
    performRegressionSliced()
    analyzeRegressionPredicintingStatistics()
    
if __name__ == "__main__":
    main()
    #results = analyzeRegressionSignificance()