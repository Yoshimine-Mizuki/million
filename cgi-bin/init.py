#!/usr/bin/python3

import cgi

print( 'Content-Type: text/plain\n' )

# データ取得
import numpy as np
import pandas as pd
from pandas_datareader import DataReader
import datetime

form = cgi.FieldStorage()
stock_id = form.getvalue( 'id' )

now = datetime.datetime.now()
end = datetime.datetime( now.year, now.month, now.day )

# 学習(SARIMA)
import statsmodels.api as sm

Y_pred, D_pred = [], []

result = sm.load( 'pickle/' + stock_id + '.pickle' )

Y_pred = result.predict( end , end + datetime.timedelta( days = 30 ) )

for i in range( 31 ):
    D_pred.append( ( end + datetime.timedelta( days = i ) ).strftime( '%Y-%m-%d' ) )

# 出力
comma = ','

print( '[' )

print( '{ "id": "' + stock_id + '" },' )

for i in range( len( Y_pred ) ):
    if ( i == ( len( Y_pred ) - 1 ) ): comma = ''
    print( '{ "x": "' + D_pred[i] + '", "y":' , Y_pred[i], '}' + comma )

print( ']' )
