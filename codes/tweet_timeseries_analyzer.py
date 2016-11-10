import pandas as pd
import json
import matplotlib.pyplot as plt

with open( "timeseries.json", "r" ) as ts:
    data = json.load( ts )

date_arr = [ ]
sentiment_arr = [ ]    
for key, value in data.items():
    date_arr.append( key )
    sum = 0
    for i in range(0, len( value )):
        if( value[i] == "positive" ):
            sum += 1.0
    sentiment_arr.append( sum/len( value ) )

print( date_arr )
print( sentiment_arr )    
ts_data = { 'date' : date_arr, 'sentiment' : sentiment_arr }
df = pd.DataFrame( ts_data, columns = ['date', 'sentiment'] )
df["date"] = pd.to_datetime( df["date"] )
df.index = df["date"]
del df["date"]
print( df )         
df.plot()
plt.show()