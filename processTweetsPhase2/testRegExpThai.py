# -*- coding: utf-8 -*-
'''
Created on Dec 7, 2014

@author: Ben Athiwaratkun (pa338)

'''
#from __future__ import division
#import numpy as np
import re
from process01_prePyThai import tokenizeMixedLanguage


def testThaiUnicode():
    print u'\u0E00'
    print u'\u0E01'
    print u'\u0E02'
    print u'\u0E03'
    print u'\u0E04'
    print u'\u0E05'
    print u'\u0E06'
    
def testRegExpThai():
    th1 = u'ยังคงรักเธอ'
    s = u'RT @kongkangpcy: ยังคงรักเธอ ยังเฝ้ารออยู่alwaysเหมือนอย่างเคย'
    print th1
    m = re.search(u'[\u0E00-\u0E7F]+',th1)
    print 'match=', m.group()
    
    
if __name__ == "__main__":
    testRegExpThai()
    s = u'RT @kongkangpcy: ยังคงรักเธอ ยังเฝ้ารออยู่alwaysเหมือนอย่างเคย'
    tokenizeMixedLanguage(s)