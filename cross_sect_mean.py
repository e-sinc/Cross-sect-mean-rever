

from Backtest_struct import backtest,buy_all   # premade backtest structure

# intraday mean reversion strategy 
import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

entryZscore =1;
lookback = 25;
start_date = '2018-01-01'
end_date = '2020-07-01'
tickers = ["MMM", "ABT", "ABBV", "ABMD", "ACN", "ATVI", "ADBE", "AMD", "AAP", "AES", "AFL"]

def cross_mean_rev(df,ticker):

    df['avg_return'] = df.xs('s_return',level='type',axis=1).mean(axis=1)    
    df['denom'] = (df.xs('s_return',level='type',axis=1).sub(df['avg_return'],axis=0)).abs().sum(axis=1) 
 
    s_return_columns = df.xs('s_return', level='type', axis=1)
    
    # Subtract the 'avg_return' from each column by broadcasting 'avg_return' across columns
    adjusted_returns = s_return_columns.sub(df['avg_return'], axis=0)
    
    # Ensure 'denom' is aligned properly
    denom_series = df['denom']
    
    # Divide by 'denom'
    final_result = adjusted_returns.div(denom_series, axis=0)
    
    final_result.fillna(0,inplace=True)
    row_sums = final_result.abs().sum(axis=1)
    final_result = final_result.div(row_sums, axis=0)
    final_result.fillna(0,inplace=True)
    return final_result

val,w,df = backtest(cross_mean_rev,start_date,end_date,tickers)
