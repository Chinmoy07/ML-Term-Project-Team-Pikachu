from sklearn import svm
import matplotlib.pyplot as plt
import json
import numpy as np

training_length = 0.60

with open("../Output-files/features.json", "r") as features_file:
    data = json.load( features_file )

X = []
Y = []

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
    
    X.append( temp_arr )
    Y.append( index_feat[i]["Target"] )
    
X =  np.array( X )
Y =  np.array( Y )  
X_train = X[ : int( training_length*len( X ) ) ]
Y_train = Y[ : int( training_length*len( Y ) ) ]
X_test = X[ int( training_length*len( X ) ) : ]
Y_test = Y[ int( training_length*len( Y ) ) : ]

clf = svm.SVC( kernel='rbf' )
clf.fit( X_train, Y_train )
Y_pred = clf.predict( X_test ) 

cnt = 0
pred_file = open("../Output-files/Predictions.txt", "w")
pred_file.write("Actual    Predicted\n")
for i in range( 0, len( Y_pred ) ):
    pred_file.write( (' '+str(Y_test[i]))[-2:] + "       " + (' '+str(Y_pred[i]))[-2:] + "\n" )
    if( Y_pred[i] != Y_test[i] ):
        cnt+=1
print( "Prediction done with accuracy : " + str( ( len( Y_pred ) - cnt )/( len( Y_pred ) ) ) + " and predictions saved to Output-files/Predictions.txt")
