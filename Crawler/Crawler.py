'''
Created on Nov 23, 2014

@author: Ben Athiwaratkun (pa338)

This file is to crawl Pantip.com Forum
'''
#from __future__ import division
#import numpy as np

#import requests
import urllib2
from bs4 import BeautifulSoup as bs

# The url format is www.pantip.com/forum/XXXX  where XXXX is the room's name
PANTIP_ROOMS = ['room','greenzone', 'camera', 'cartoon', 'gallery', 'klaibann', 'jatujak',
         'chalermkrung', 'chalermthai', 'family', 'home', 'siliconvalley', 'beauty', 'writer', 
         'blueplanet', 'tvshow', 'pantip', 'region', 'mbk', 'ratchada', 
         'rajdumnern', 'isolate', 'social', 'religious', 'supachalasai', 'siam', 'lumpini', 
         'sinthorn', 'silom' , 'wahkor', 'library' , 'art' ]
BASE_URL = 'http://www.pantip/com/forum/'
START_ID = 30000000
END_ID = 32800000

def writeUrlListToFile():
    for id in range(START_ID, END_ID):
        currentUrl = BASE_URL + str(id)
        #r = requests.get(currentUrl)
        urlf = urllib2.urlopen('http://pantip.com/topic/32881890')
        h =  urlf.read()
        bs_instance = bs(h)
        #print bs_instance
        post_title = bs_instance.findAll(True, {'class':'display-post-title'})
        post_story = bs_instance.findAll(True,{'class':'display-post-story'})
        tag_items = bs_instance.findAll(True,{'class':'tag-item'})
        #print post_title
        ### Use this to parse
        f = open('../Data/Pantip/' + str(id) + '.txt', 'wb')
        
        for item in post_title:
            f.write(item.get_text().encode('utf-8') + "\n")
        for item in post_story:
            f.write(item.get_text().encode('utf-8') + "\n")
            
        f2 = open('../Data/Pantip/' + str(id) + '_tags.txt', 'wb')
        for item in tag_items:
            f2.write(item.get_text().encode('utf-8') + "\n")

'''def main():
    pass'''
    
if __name__ == "__main__":
    writeUrlListToFile()