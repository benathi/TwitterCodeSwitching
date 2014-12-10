'''
Created on Dec 8, 2014

@author: Ben Athiwaratkun (pa338)

'''
#from __future__ import division
#import numpy as np
import json



def sanityCheckNgram():
    numLine = 0
    fin = open('../Data/process3/process3.txt','rb')
    for line in fin:
        numLine += 1
        print 'Process Line %d--------------------------------------------' % numLine
        _d = json.loads(line) # key: cs-word-list and text-list
        for ph in _d['original-text-list']:
            print ph
        print '##### Ngrams ######'
        for ngram in _d['ngram-list']:
            print ngram
        ## looks good!
    
        ### 
        if numLine >= 100:
            return


def main():
    sanityCheckNgram()
    
if __name__ == "__main__":
    main()