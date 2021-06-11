#!/usr/bin/python3

import cgi

print( 'Content-Type: text/plain\n' )

import os

class suppress_stdout_stderr( object ):
    def __init__( self ):
        self.null_fds = [os.open( os.devnull, os.O_RDWR ) for x in range( 2 )]
        self.save_fds = [os.dup( 1 ), os.dup( 2 )]

    def __enter__( self ):
        os.dup2( self.null_fds[0], 1 )
        os.dup2( self.null_fds[1], 2 )

    def __exit__( self, *_ ):
        os.dup2( self.save_fds[0], 1 )
        os.dup2( self.save_fds[1], 2 )
        for fd in self.null_fds + self.save_fds:
            os.close( fd )

# データ取得
import numpy as np
import pandas as pd
from pandas_datareader import DataReader
import datetime

form = cgi.FieldStorage()
stock_id = form.getvalue( 'id' )
selectType = form.getvalue( 'type' )

now = datetime.datetime.now()
end = datetime.datetime( now.year, now.month, now.day )
start = end + datetime.timedelta( days = -75 )

df = DataReader( stock_id, 'yahoo', start, end )
stock = df.loc[:, ['Adj Close']].resample('D').interpolate('time').ffill().bfill().reset_index().round( 2 )

term = 365

if selectType == 'rnn':

    import keras

    model = keras.models.load_model( 'h5/' + stock_id + '.h5', compile = False )

    ts = df[['Adj Close']].resample('D').interpolate('time').ffill().bfill() / stock['Adj Close'][0]

    X_test = ts.iloc[25:75].values[np.newaxis, :, :]
    Y_pred, D_pred = [], []

    for i in range( term ):
        predicted = model.predict( X_test )
        X_test = np.append( X_test[0,1:], predicted, axis = 0 )[np.newaxis, :, :]
        Y_pred.append( predicted[0, 0] * stock['Adj Close'][0] )
        D_pred.append( ( end + datetime.timedelta( days = i ) ).strftime( '%Y-%m-%d' ) )

if selectType == 'sarima':

    import statsmodels.api as sm

    Y_pred, D_pred = [], []

    result = sm.load( 'pickle/' + stock_id + '.pickle' )

    Y_pred = result.predict( end , end + datetime.timedelta( days = term ) )

    for i in range( term + 1 ):
        D_pred.append( ( end + datetime.timedelta( days = i ) ).strftime( '%Y-%m-%d' ) )

if selectType == 'prophet':

    import logging
    from fbprophet import Prophet

    past = -365

    end = datetime.datetime( now.year, now.month, now.day )
    start = end + datetime.timedelta( days = past )
    df = DataReader( '^N225','yahoo', start, end )

    ts = df.loc[:, ['Adj Close']].resample('D').interpolate('time').ffill().bfill().reset_index().rename( columns = {'Adj Close': 'y', 'Date': 'ds'} )

    logging.getLogger( 'fbprophet' ).setLevel( logging.WARNING )

    model = Prophet()
    with suppress_stdout_stderr():
        model.fit( ts )

    future = model.make_future_dataframe( periods = term )
    forecast = model.predict( future )


# 出力
stock['Date'] = stock['Date'].dt.strftime( '%Y-%m-%d' )

comma = ','

print( '[' )

if selectType in {'rnn', 'sarima'}:
    for i in range( len( stock ) ):
        print( '{ "x": "' + stock.values[i][0] + '", "y":' , stock.values[i][1], '},' )

    for i in range( len( Y_pred ) ):
        if ( i == ( len( Y_pred ) - 1 ) ): comma = ''
        print( '{ "x": "' + D_pred[i] + '", "y":' , Y_pred[i].round( 2 ), '}' + comma )

elif selectType == 'prophet':
    past += 75
    for i in range( len( forecast ) + past ):
        if ( i == ( len( forecast ) + past - 1 ) ): comma = ''
        print( '{ "x": "', forecast['ds'][i - past].strftime( '%Y-%m-%d' ), '", "y":' , forecast['yhat'][i - past].round( 2 ), '}' + comma )

print( ']' )