# coding: utf-8

import json
from pandas_datareader import DataReader
from datetime import datetime

end = datetime.now()
start = datetime( end.year, end.month-1, end.day )

json_file = open( 'stock.json', 'r' )
json_object = json.load( json_file )

for i in range( len(json_object) ):
    symbol = json_object[i]['symbol']

    stock = DataReader( symbol, 'yahoo', start, end )

    print( symbol, stock['Adj Close'].tail(5) )
