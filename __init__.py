#program to extract tweets using Twitter API
#recent 100 tweets that has 'finance' keyword in it

import json
import nltk
import tweepy
import sys
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

ACCESS_TOKEN = "777019915546918912-FIMAXL5BkX64ICZH2NNCG8y5jwJpNlm"
ACCESS_SECRET = "bYEI0EZQdUDZDEYnEJ7Dt2Lc39J08EEi4b0Yz3JzSM9zm"
CONSUMER_TOKEN = "1Qx2jufOi4yGVT4NQwcWq8soh"
CONSUMER_SECRET = "DaYisjxi7AcLjLTIH7kMX2sJCXxb7Q1xCnJ0wHbEONtR4gH4ei"
f = open("tweets.json", "w")

oauth = OAuthHandler(CONSUMER_TOKEN , CONSUMER_SECRET)
oauth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

tweet_list = []        
        
class listener(StreamListener):
    count = 100
    def on_data(self, data):
        obj = json.loads(data)
        if listener.count > 0 :
            try:
                tweet_obj = {}
                tweet_obj["text"] = obj["text"]
                tweet_obj["date"] = obj["created_at"]
                if( "finance" in tweet_obj["text"]):
                    listener.count -= 1
                    tweet_list.append( tweet_obj )
                    print( str(listener.count) + "done")
            except:
                print(str(listener.count) + "not found")
        else:
            tweet_dict = {}
            tweet_dict["tweets"] = tweet_list
            f.write(json.dumps(tweet_dict))
            f.close()
            sys.exit()
        return(True)

    def on_error(self, status):
        print(status)


twitter_stream = Stream(oauth, listener())
twitter_stream.filter(track=["finance"])
f.close()

