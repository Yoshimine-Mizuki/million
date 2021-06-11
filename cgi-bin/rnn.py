#!/usr/bin/python3

print( 'Content-Type: text/plain\n' )

import numpy as np
import pandas as pd
from datetime import datetime
from pandas_datareader import DataReader

now = datetime.now()
start = datetime( now.year - 3, now.month, now.day )
end = datetime( now.year, now.month, now.day )

def load_data( data, n_prev = 50 ):

    docX, docY = [], []
    for i in range(len(data)-n_prev):
        docX.append( data.iloc[i:i+n_prev].values )
        docY.append( data.iloc[i+n_prev].values )
    alsX = np.array( docX )
    alsY = np.array( docY )

    return alsX, alsY

def train_test_split( df, test_size=0.1, n_prev = 50 ):
    ntrn = round( len( df ) * .8 )
    ntrn = int( ntrn )
    X_train, y_train = load_data( df.iloc[0:ntrn], n_prev )
    X_test, y_test = load_data( df.iloc[ntrn:], n_prev )

    return ( X_train, y_train ), ( X_test, y_test )

from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.layers.recurrent import LSTM, GRU

def create_model( model_option = 'lstm', in_out_neurons = 1, hidden_neurons = 300, length_of_sequences = 50, activation = 'linear' ):
    model = Sequential()

    if model_option == 'lstm':
        h = LSTM( hidden_neurons, batch_input_shape = ( None, length_of_sequences, in_out_neurons ), return_sequences = False )
    elif model_option == 'gru':
        h = GRU( hidden_neurons, batch_input_shape = ( None, length_of_sequences, in_out_neurons ), return_sequences = False )
    elif model_option == 'qrnn':
        from qrnn import QRNN
        h = QRNN( 64, window_size = 12, dropout = 0 )

    model.add( h )
    model.add( Dense( in_out_neurons ) )
    model.add( Activation( activation ) )

    return model

import json

json_file = open( 'all.json', 'r' )
json_object = json.load( json_file )

for i in range( len(json_object) ):
    symbol = json_object[i]['symbol']

    stock = DataReader( symbol,'yahoo', start, end )

    ts = stock[['Adj Close']].resample('D').interpolate('time').ffill().bfill() / stock['Adj Close'][0]

    length_of_sequences = 50
    X_train, Y_train = load_data( ts.iloc[0:len(ts)-1], length_of_sequences )
    X_test, Y_test = load_data( ts.iloc[len(ts) - length_of_sequences - 1:len(ts)], length_of_sequences )

    model = create_model( 'gru' )

    model.compile( loss = 'mean_absolute_error', optimizer = 'adam' )
    history = model.fit( X_train, Y_train, batch_size = 128, epochs = 100, validation_split = 0.2 )

    model.save( '/var/www/cgi-bin/h5/' + symbol + '.h5' )