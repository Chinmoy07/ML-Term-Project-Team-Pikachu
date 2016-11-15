import csv
import json
import sys

timeframe = 10

def minimum(a, b):
    return a < b

def maximum(a, b):
    return a > b

def get_sentiment_strength( sentiment_array ):
    sum = 0.0
    cnt = 0
    for item in sentiment_array:
        if( item == "positive" ):
            sum += 1.0
    return sum / len( sentiment_array )

def read_csv_calculate_feature( filename, target_reqd ):
    flag = False
    close_price = []
    volume = []
    date = []
    
    with open("../Output-files/timeseries.json", "r") as senti_file:
        sentiments = json.load( senti_file )
    
    
    with open( filename, "r" ) as csv_file:
        data = csv.reader( csv_file ) 
        for row in data:
            if( flag ):
                close_price.append( float( row[6] ) )
                volume.append( int( row[5] ) )
                date.append( row[0] )
            else:
                flag = True
    
    flag = False    
    on_balance_volume = 0
    moving_average = 0
    prev_moving_avg = 0
    exp_moving_avg = 0
    prev_exp_moving_avg = 0
    
    for i in range(1, timeframe):
        moving_average += ( close_price[ i ] / timeframe )
    
    features = []                
    for i in range( timeframe, len( close_price ) - 1 ):
        
        obj = {}
        '''
            SIMPLE MOVING AVERAGE CALCULATION
        '''
        moving_average += ( close_price[ i ]/timeframe )
        if(flag):
            if( prev_moving_avg > moving_average ):
                obj["Moving Average"] = -1
            else:
                obj["Moving Average"] = 1
        prev_moving_avg = moving_average
        moving_average -= ( close_price[ i-timeframe+1 ]/timeframe )
        
            
        '''
            PRICE MOMENTUM OSCILLATOR CALCULATION
        '''
        
        price_momentum_oscillator = close_price[i] - close_price[i-timeframe+1]
        obj["Price Momentum Oscillator"] = price_momentum_oscillator
        
        '''
            STOCHASTIC OSCILLATOR CALCULATION
        '''
        
        lowest_low = 100000
        highest_high = -1 
        for j in range( i - timeframe + 1, i ):
            lowest_low = minimum(lowest_low, close_price[j])
            highest_high = maximum(highest_high, close_price[j])
        stochastic_oscillator =  ( close_price[i] - lowest_low )/( highest_high - lowest_low )   
        obj["Stochastic Oscillator"] = stochastic_oscillator
        
        '''
            RELATIVE STRENGTH INDEX CALCULATION
        '''
        up_close = 0
        down_close = 0
        for j in range( i - timeframe + 2, i ):
            if( close_price[j-1] > close_price[j] ):
                down_close += ( close_price[j-1] - close_price[j] )              
            else:
                up_close += ( close_price[j] - close_price[j-1] )
        relative_strength_index = up_close / ( up_close + down_close )        
        obj["Relative Strength Index"] = relative_strength_index
        
        '''
            ON BALANCE VOLUME CALCULATOR
        '''        
        if( close_price[i-1] > close_price[i] ):
            #on_balance_volume -= volume[i]
            on_balance_volume = -1
        else:
            #on_balance_volume += volume[i]
            on_balance_volume = 1
        obj["On Balance Volume"] = on_balance_volume 
        
        '''
            SENTIMENT STRENGTH
        '''
        sentiment_strength = get_sentiment_strength( sentiments[ date[i] ] )
        obj["Sentiment Strength"] = sentiment_strength
        
        '''
            TARGET
        '''
        if( target_reqd ): 
            if( close_price[i+1] > close_price[i] ):
                target = 1
            else:
                target = -1
            obj["Target"] =  target
        if( flag ):
            features.append( obj )
        else:
            flag = True
    return features            
            
index_features = read_csv_calculate_feature( "../Input-files/sp-index.csv", True )
features_dict = {}
features_dict["Index Features"] = index_features
f = open("../Output-files/features.json", "w")
f.write( json.dumps( features_dict ) )
print("Features calculated and saved to Output-files/features.json")