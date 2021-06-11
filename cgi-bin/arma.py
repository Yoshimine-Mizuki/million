#!/usr/bin/python3

print( 'Content-Type: text/plain\n' )

import numpy as np
import pandas as pd

import statsmodels.tsa.api as smt
import seaborn as sns
sns.set()

from pandas_datareader import DataReader
from datetime import datetime

now = datetime.now()
start = datetime( now.year - 5, now.month, now.day )
end = datetime( now.year, now.month, now.day )

term = 180

import json

json_file = open( 'all.json', 'r' )
json_object = json.load( json_file )

for i in range( len(json_object) ):
    symbol = json_object[i]['symbol']

    stock = DataReader( symbol,'yahoo', start, end ).round( 2 )

    ts = stock['Adj Close'].resample('D').interpolate('time').ffill().bfill()

    # sarimax_model = smt.SARIMAX( ts, order = ( 1, 1, 1 ), seasonal_order = ( 1, 1, 1, term ) )
    # result = sarimax_model.fit( method = 'bfgs' )

    arima_model = smt.arima.ARIMA( ts, order = ( 1, 1, 1 ), seasonal_order = ( 1, 1, 1, term ) )
    result = arima_model.fit( method = 'innovations_mle', low_memory = True, cov_type = 'none' )

    result.save( '/var/www/cgi-bin/pickle/' + symbol + '.pickle' )