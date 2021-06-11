#!/usr/bin/python3

print( 'Content-Type: text/plain\n' )

import numpy as np
import pandas as pd
from pandas_datareader import DataReader
from datetime import datetime

now = datetime.now()
start = datetime( now.year - 3, now.month, now.day )
end = datetime( now.year, now.month, now.day - 1 )

stock = DataReader( '^N225','yahoo', start, end )

ts = stock.loc[:, ['Adj Close']].reset_index().rename( columns={'Adj Close': 'y', 'Date': 'ds'} )

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

import logging
from fbprophet import Prophet

logging.getLogger( 'fbprophet' ).setLevel( logging.WARNING )

model = Prophet()
with suppress_stdout_stderr():
    model.fit( ts )

future = model.make_future_dataframe( periods = 365 )
forecast = model.predict( future )

print( forecast )