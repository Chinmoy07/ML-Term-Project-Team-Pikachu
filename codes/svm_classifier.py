from sklearn import svm
import matplotlib.pyplot as plt
import json
import numpy as np

training_length = 0.60

with open("features.json", "r") as features_file:
    data = json.load( features_file )

X = []
Y = []

#stock_feat = data["Stock Features"]
index_feat = data["Index Features"]

features_key = [
                "Moving Average", 
                "Price Momentum Oscillator", 
                "Relative Strength Index", 
                "On Balance Volume", 
                "Stochastic Oscillator",
                "Sentiment Strength"
               ]

for i in range( 0, len( index_feat ) ):
    temp_arr = []
    
    for j in range( 0, len( features_key ) ):
        temp_arr.append( index_feat[i][ features_key[j] ] )
    #    temp_arr.append( index_feat[i][ features_key[j] ] )
    
    X.append( temp_arr )
    Y.append( index_feat[i]["Target"] )
    #Y.append( index_feat[i]["Target"] )
    
X =  np.array( X )
Y =  np.array( Y )  
X_train = X[ : int( training_length*len( X ) ) ]
Y_train = Y[ : int( training_length*len( Y ) ) ]
X_test = X[ int( training_length*len( X ) ) : ]
Y_test = Y[ int( training_length*len( Y ) ) : ]

clf = svm.SVC( kernel='rbf' )
clf.fit( X_train, Y_train )
Y_pred = clf.predict( X_test ) 
print( Y_pred )

cnt = 0
print( Y_test )
for i in range( 0, len( Y_pred ) ):
    if( Y_pred[i] != Y_test[i] ):
        cnt+=1
print( ( len( Y_pred ) - cnt )/( len( Y_pred ) ) )
