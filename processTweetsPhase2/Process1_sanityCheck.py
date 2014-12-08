'''
Created on Dec 7, 2014

@author: Ben Athiwaratkun (pa338)

'''
#from __future__ import division
#import numpy as np
import json

def sanityCheck1():
    fin = '../Data/process1/output1_mini_textList.txt'
    for line in open(fin,'rb'):
        tweet = json.loads(line)
        for text, indic in zip( tweet['text'], tweet['th-indicator']):
            print text
            print indic
    

def main():
    sanityCheck1()
    
if __name__ == "__main__":
    main()