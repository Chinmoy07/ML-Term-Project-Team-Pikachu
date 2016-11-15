import nltk
import csv
from nltk.stem.porter import PorterStemmer
import json

def list_stemmer( words_filtered ):
    st = PorterStemmer()
    stemmed_words_list = []
    for word in words_filtered:
        word = st.stem( word )
        stemmed_words_list.append( word )
    return stemmed_words_list

def get_all_words(tweets):
    all_words = []
    for (word, sentiment) in tweets :
        all_words.extend( word )
    return all_words    
 
def get_word_features( all_words ):
    wordlist = nltk.FreqDist( all_words )
    word_features = wordlist.keys()
    return word_features

def feature_extractor( test_tweet ):
    tweet_words_set = set( test_tweet )
    stemmed_words = list_stemmer( tweet_words_set ) 
    features = {}
    for word in word_features:
        features[ 'contains(%s)' % word ] =  ( word in  stemmed_words ) 
    return features
 
def trainer_example( ):
    pos_tweets = []
    neg_tweets = []
    with open("../Input-files/training_set.csv") as mycsv:
        data = csv.reader( mycsv, delimiter = ',' )
        for row in data:
            if( row[0] == "0" ):
                neg_tweets.append( ( row[1], "negative" ) )
            elif( row[0] == "4" ):
                pos_tweets.append( (row[1], "positive" ) )
    return ( pos_tweets, neg_tweets )

def predict( classifier, tweet ):
    return classifier.classify( feature_extractor( tweet.split() ) )

#### MAIN FUNCTION BEGINS

( pos_tweets, neg_tweets ) = trainer_example()
tweets = []

for (line, sentiment) in pos_tweets + neg_tweets:
    words_filtered = [e.lower() for e in line.split() if len(e) > 2]
    stemmed_words_list = list_stemmer( words_filtered )
    tweets.append( ( stemmed_words_list, sentiment ) )

word_features = get_word_features( get_all_words(tweets) )

training_set = nltk.classify.apply_features( feature_extractor, tweets )

classifier = nltk.NaiveBayesClassifier.train( training_set )

with open("../Input-files/tweets.json", "r") as tweets_file:
    data = json.load( tweets_file )

ts_file = open("../Output-files/timeseries.json", "w") 
ts_dict = {}
cnt = 1
for obj in data["tweets"]:
    pred = predict( classifier, obj["text"] )
    print( str(cnt) + pred )
    date = obj["date"].split(' ')[0]
    
    try:
        ts_dict[ date ].append( pred )
    except( Exception ):
        ts_dict[ date ] = [ pred ]
    cnt += 1
ts_file.write( json.dumps( ts_dict ) )
print("Classified all tweets and output written to Output-files/timeseries.json")