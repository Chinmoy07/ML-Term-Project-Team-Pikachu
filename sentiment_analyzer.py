import nltk
import csv
from nltk.stem.porter import PorterStemmer

#pos_tweets = [('I love this car', 'positive'),
#              ('This view is amazing', 'positive'),
#              ('I feel great this morning', 'positive'),
#              ('I am so excited about the concert', 'positive'),
#              ('He is my best friend', 'positive')]

#neg_tweets = [('I do not like this car', 'negative'),
#              ('This view is horrible', 'negative'),
#              ('I feel tired this morning', 'negative'),
#              ('I am not looking forward for the concert', 'negative'),
#              ('He suffered losses', 'negative')]

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
    st = PorterStemmer()
    for word in word_features:
        features[ 'contains(%s)' % word ] =  ( word in  stemmed_words ) 
    return features
 
def trainer_example( ):
    pos_tweets = []
    neg_tweets = []
    with open("training_set.csv") as mycsv:
        data = csv.reader( mycsv, delimiter = ',' )
        for row in data:
            if( row[0] == "0" ):
                neg_tweets.append( ( row[1], "negative" ) )
            elif( row[0] == "4" ):
                pos_tweets.append( (row[1], "positive" ) )
    return ( pos_tweets, neg_tweets )

#### MAIN FUNCTION BEGINS

( pos_tweets, neg_tweets ) = trainer_example()
tweets = []
 
for (line, sentiment) in pos_tweets + neg_tweets:
    words_filtered = [e.lower() for e in line.split() if len(e) > 2]
    stemmed_words_list = list_stemmer( words_filtered )
    tweets.append( ( stemmed_words_list, sentiment ) )

#print(tweets)
#print(get_all_words(tweets))

word_features = get_word_features( get_all_words(tweets) )
#print(word_features)

training_set = nltk.classify.apply_features( feature_extractor, tweets )

classifier = nltk.NaiveBayesClassifier.train( training_set )

tweet = 'i won the match'
print(classifier.classify( feature_extractor(tweet.split()) ))

tweet = 'it was a loss'
print(classifier.classify( feature_extractor(tweet.split()) ))

tweet = 'it was a profit'
print(classifier.classify( feature_extractor(tweet.split()) ))
