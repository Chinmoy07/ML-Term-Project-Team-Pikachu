#program to extract tweets using Twitter API

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

def get_proper_time( twitter_time, month_map ):
    time_segments = twitter_time.split()
    proper_time = time_segments[5]+'-'
    proper_time += month_map[time_segments[1]]+'-'
    proper_time += time_segments[2]+' '
    proper_time += time_segments[3]    
    return proper_time

def compare_date( ):
    return True        
        
class listener(StreamListener):
    flag = True
    count = 1000
    start_date = "2016-10-08 05:15:36"
    month_map = {
        "Jan": "01",
        "Feb": "02",
        "Mar": "03",
        "Apr": "04",
        "May": "05",
        "Jun": "06",
        "Jul": "07",
        "Aug": "08",
        "Sep": "09",
        "Oct": "10",
        "Nov": "11",
        "Dec": "12"
    }
    def on_data(self, data):
        obj = json.loads(data)
        if ( listener.count > 0 ):
            try:
                tweet_obj = {}
                tweet_obj["text"] = obj["text"]
                tweet_obj["date"] = get_proper_time(obj["created_at"], listener.month_map ) 
                tweet_list.append( tweet_obj )
                print(listener.count)
                listener.count = listener.count - 1
            except Exception as err :
                print(err)
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
twitter_stream.filter(track=["microsoft"], languages=["en"])
f.close()

