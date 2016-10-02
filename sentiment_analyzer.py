import nltk

pos_tweets = [('I love this car', 'positive'),
              ('This view is amazing', 'positive'),
              ('I feel great this morning', 'positive'),
              ('I am so excited about the concert', 'positive'),
              ('He is my best friend', 'positive')]

neg_tweets = [('I do not like this car', 'negative'),
              ('This view is horrible', 'negative'),
              ('I feel tired this morning', 'negative'),
              ('I am not looking forward for the concert', 'negative'),
              ('He is my enemy', 'negative')]

tweets = []

def get_all_words(tweets):
    all_words = []
    for (word, sentiment) in tweets :
        all_words.extend( word )
    return all_words    
 
def get_word_features( all_words ):
    wordlist = nltk.FreqDist( all_words )
    print( wordlist )
    word_features = wordlist.keys()
    return word_features

def feature_extractor( test_tweet ):
    tweet_words_set = set( test_tweet )
    features = {}
    for word in word_features:
        features[ 'contains(%s)' % word ] = ( word in tweet_words_set )
    return features
 

 
for (line, sentiment) in pos_tweets + neg_tweets:
    words_filtered = [e.lower() for e in line.split() if len(e) > 2]
    tweets.append( ( words_filtered, sentiment ) )
    
#print(tweets)   
word_features = get_word_features( get_all_words(tweets) )

training_set = nltk.classify.apply_features( feature_extractor, tweets )
#print(training_set)
classifier = nltk.NaiveBayesClassifier.train( training_set )

#print( classifier.show_most_informative_features(32) )

tweet = 'The movie is not looking'
print(classifier.classify( feature_extractor(tweet) ))

#print( feature_extractor(tweet) )




