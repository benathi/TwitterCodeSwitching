'''
Created on Nov 25, 2014

@author: Ben Athiwaratkun (pa338)

'''
import oauth2 as oauth
import urllib2 as urllib
import re
# See assignment1.html instructions or README for how to get these credentials

api_key = "J7Bg9y5keCUlDu9mUWitrQheS"
api_secret = "lkVhMmQjD3on1nzvKYbdnhstQZAid7d9bMbzB4c72xYWjxO4C0"
access_token_key = "2613894511-Mn2nhK0Z1mGBlV1V4aSxjnANux7379wrO1xRSEc"
access_token_secret = "WmP0TIVkFanJMUbTTo9zjPu8iA7MxhJO4XiKP1FfLGQFI"

_debug = 0

oauth_token    = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=api_key, secret=api_secret)

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

http_method = "GET"


http_handler  = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)

'''
Construct, sign, and open a twitter request
using the hard-coded credentials above.
'''
def twitterreq(url, method, parameters):
  req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                             token=oauth_token,
                                             http_method=http_method,
                                             http_url=url, 
                                             parameters=parameters)

  req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)

  headers = req.to_header()

  if http_method == "POST":
    encoded_post_data = req.to_postdata()
  else:
    encoded_post_data = None
    url = req.to_url()

  opener = urllib.OpenerDirector()
  opener.add_handler(http_handler)
  opener.add_handler(https_handler)

  response = opener.open(url, encoded_post_data)

  return response

def fetchsamples():
    #url = "https://stream.twitter.com/1/statuses/sample.json?language=th"
    #https://twitter.com/search?q=lang%3Ath&src=typd
    
    url = "https://api.twitter.com/1.1/search/tweets.json?q=lang%3Ath&src=typd"
    url = "https://api.twitter.com/1.1/search/tweets.json?q=lang%3Ath"
    parameters = []
    response = twitterreq(url, "GET", parameters)
    for line in response:
        theLine = line.strip()
        #print theLine
        # .*? : non greedy option to get only the text and not other attributes
        # load it to json - http://mike.teczno.com/notes/streaming-data-from-twitter.html
        match = re.search(r'"text":"(.*?)","',theLine)
        if match:
            text = match.group(1)
            print "Text: %s" % text.encode('utf-8')
            #print "Test Unicode: %s" % unicode(text)
        else:
            print "No Text"
if __name__ == '__main__':
    fetchsamples()



def main():
    pass
    
if __name__ == "__main__":
    main()