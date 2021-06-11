# coding: utf-8

import json
import datetime
from pandas_datareader import DataReader

now = datetime.datetime.now()
end = datetime.datetime( now.year, now.month, now.day )
start = end + datetime.timedelta( days = -1 )

stock = DataReader( '^N225', 'yahoo', start, end )
ts = stock['Adj Close'].round( 2 )

diff_amount = ( ts[1] - ts[0] ).round( 2 )
diff_ratio = ( diff_amount / ts[0] * 100 ).round( 2 )

print( diff_amount, diff_ratio )