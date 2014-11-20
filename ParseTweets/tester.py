# -*- coding: utf-8 -*-
'''
This file contains script to test libraries for sanity check

Created on Nov 15, 2014

@author: Ben Athiwaratkun (pa338)

'''
#from __future__ import division
#import numpy as np
import enchant
import re
import langid
#import subprocess
from subprocess import Popen, PIPE, call

#### PyEnchant is a dictionary based on enchant C library
#### Can look up if words exist in the dictionary. (Case Sensitive)
#### It also handles word suggestion
def testPyEnchant():
    d_enchant = enchant.Dict('en_US')
    print d_enchant.check('Hellao')     # False
    print d_enchant.check('He')         # True
    print d_enchant.check('He does')    # False
    print d_enchant.check('iphone')     # False
    print d_enchant.check('iPhone')     # True
    print d_enchant.check('bangkok')    # False
    print d_enchant.check('Bangkok')    # True
    print d_enchant.suggest('Hellao')  # gives out a long list
    print d_enchant.check('7')          # true
    print d_enchant.check('www')        # false
    print d_enchant.check('OnDemand')   # false
    print d_enchant.suggest('OnDemand') #On-Demand is the first word
    print d_enchant.check('lt')         # false
    print d_enchant.suggest('lt')       #Lt,Lat,Lot,lat,let,lit,..


def testRegExp():
    w = '7wba'
    result = re.search(r"[a-zA-Z]+", w)
    
    if not result == None:
        print result.group()
        print type(result.group())
    else:
        print None
        
        
def testLanguageDetection():
    japEng = '''baby I'm so lucky
僕たちが出会えた偶然は
神様がくれたプレゼント
ただ一つ僕の宝物
GOT7, IGOT7僕らはみんな一つさ
baby I'm so lucky
僕たちが出会えた偶然は
神様がくれたプレゼント
ただ一つ僕の宝物
GOT7, IGOT7僕らはみんな一つさ'''
    print japEng
    print langid.classify(japEng)
    
    thaiEng1 = '''I'm at มหาวิทยาลัยศรีนครินทรวิโรฒ (Srinakharinwirot University) in Vadhana, Bangkok w/'''
    thaiEng2 = '''แฟนอาร์ตจาก pico ค่ะ รักนางอ่ะ ว่าแล้วนางต้องวาดรูปนี้ 5555 คือวาดหน้าตาเซฮุนกวนตีน 5555 #รักเขามาก '''
    thaiEng3 = 'สวัสดีค่าคุณยิปโซ อายเปนบริษัทoganizeค่า จะติดต่องาน ขอเบอร์ติดต่อได้ไหมคะ'
    print thaiEng1
    print langid.classify(thaiEng1)
    print thaiEng2
    print langid.classify(thaiEng2)
    print thaiEng3
    print langid.classify(thaiEng3)
    
    
    thai1 = ' 55555555555555555555555555555555555555555555555555ขอบคุนน้าจูเนี้ยะ เดี๋ยวเอาเปาไปไห้แหลกแบบรีฟิล วันอังคาร ล้างท้องรอเลยจุบุ'
    print thai1
    print langid.classify(thai1)
    
    Eng1 = 'IM SO EMOTIONAL RIGHT NOW UGHHHHH 😭'    
    Eng2 = 'I think maybe I will go to cinema for watching The Maze Runner~~ '
    Eng3 = 'IM SO EMOTIONAL RIGHT NOW UGHHHHH' 
    print Eng1
    print langid.classify(Eng1)
    print Eng2
    print langid.classify(Eng2)
    print Eng3
    print langid.classify(Eng3) # only 0.352 English (strange)

def testCodeSwitchingIdentification():
    thaiEng1 = '''I'm at มหาวิทยาลัยศรีนครินทรวิโรฒ (Srinakharinwirot University) in Vadhana, Bangkok w/'''
    Eng1 = 'IM SO EMOTIONAL RIGHT NOW UGHHHHH 😭'
    from Parser import  tweetToCodeSwitchingPhrases
    tweetToCodeSwitchingPhrases(thaiEng1, verbose=True)
    
    tweetToCodeSwitchingPhrases(Eng1, verbose=True)

def testListDir():
    import os
    for fname in os.listdir('../Data/'):
        if '.txt' in fname: 
            print 'Tweet File' , fname
    
def tagTweets():
    exit_code = call(['bash',
               'ark-tweet-nlp-0.3.2/runTagger.sh',
               '--output-format' ,
               'pretsv',
               '--no-confidence',
               'ark-tweet-nlp-0.3.2/examples/casual.txt',
               '>>', 
               '../preprocessedData/phrasesTagged.txt'])
    '''p = Popen(['bash',
               'ark-tweet-nlp-0.3.2/runTagger.sh',
               '--output-format' ,
               'pretsv',
               '--no-confidence',
               'ark-tweet-nlp-0.3.2/examples/casual.txt'], stdin=PIPE, stdout=PIPE, stderr=PIPE)'''
    ''''p = Popen(['bash', 'ark-tweet-nlp-0.3.2/runTagger.sh',
               'ark-tweet-nlp-0.3.2/examples/casual.txt'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    rc = p.returncode
    print 'Return Code is %d' % rc
    print 'Output is %s' % output
    print rc
    print type(output)'''
    return exit_code
    
def testTweetTagger():
    pass

def main():
    pass
    #testPyEnchant()    # works
    #testRegExp()
    #testLanguageDetection()
    #testCodeSwitchingIdentification()
    #testListDir()
    #tagTweets()
    
if __name__ == "__main__":
    main()