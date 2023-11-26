# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 11:41:25 2023

@author: aksha
"""

import pandas as pd
from datetime import datetime
import yfinance as yf

def get_news(stock_ticker, exchange):
    
    if exchange == 'NSE':
        symbol = stock_ticker + '.' + 'NS'
        
    elif exchange == 'BSE':
        symbol = stock_ticker + '.' + 'BO'
        
    stox = yf.Ticker(symbol)
    
    news_data = pd.DataFrame(stox.news)
    print(news_data.columns)
    
    return news_data
    

# Test functions 

news = get_news('PNB', 'NSE')
print(news[['title', 'providerPublishTime']])