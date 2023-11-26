# -*- coding: utf-8 -*-
"""
Created on Sat Sep 23 10:02:16 2023

@author: aksha
"""

import os 
import requests
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime
import pytz

load_dotenv()

alpha_vantage_key = os.environ.get('alpha_vantage_api_key')

def get_intra_day_data(symbol, interval, adjusted, month, extended_hours):
    # Doesn't work for Indian Stocks
    
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol='+symbol+'&interval='+interval+'&month='+month+'&adjusted='+adjusted+'&extended_hours='+extended_hours+'&outputsize=full&apikey='+alpha_vantage_key
    r = requests.get(url)
    data = r.json()
    
    data = pd.DataFrame(data['Time Series ('+interval+')']).T
    data.reset_index(inplace=True)
    data.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volums']
 
    return data

def get_daily_data(symbol, output_size):
    # output size - full, compact
    
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+symbol+'&outputsize='+output_size+'&apikey='+alpha_vantage_key
    r = requests.get(url)
    data = r.json()
    print(data)
    
    data = pd.DataFrame(data['Time Series (Daily)']).T
    data.reset_index(inplace=True)
    data.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volums']
 
    return data

def get_weekly_data(symbol, adjusted):
    
    if adjusted == 'false':
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol='+symbol+'&outputsize=full&apikey='+alpha_vantage_key
        r = requests.get(url)
        data = r.json()
        data = pd.DataFrame(data['Weekly Time Series']).T
        data.reset_index(inplace=True)
        data.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volums']
    elif adjusted == 'true':
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol='+symbol+'&outputsize=full&apikey='+alpha_vantage_key
        r = requests.get(url)
        data = r.json()
        data = pd.DataFrame(data['Weekly Adjusted Time Series']).T
        data.reset_index(inplace=True)
        data.columns = ['timestamp', 'open', 'high', 'low', 'close', 'adjusted close', 'volums', 'dividend amount']
 
    return data

def get_monthly_data(symbol, adjusted):
    
    if adjusted == 'false':
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol='+symbol+'&outputsize=full&apikey='+alpha_vantage_key
        r = requests.get(url)
        data = r.json()
        data = pd.DataFrame(data['Monthly Time Series']).T
        data.reset_index(inplace=True)
        data.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volums']
    elif adjusted == 'true':
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol='+symbol+'&outputsize=full&apikey='+alpha_vantage_key
        r = requests.get(url)
        data = r.json()
        data = pd.DataFrame(data['Monthly Adjusted Time Series']).T
        data.reset_index(inplace=True)
        data.columns = ['timestamp', 'open', 'high', 'low', 'close', 'adjusted close', 'volums', 'dividend amount']
 
    return data

# Test Function
#stock_prices_intraday = get_intra_day_data('AAPL', '30min', 'false', '2023-08', 'true')
#print(stock_prices_intraday)

#stock_prices_daily = get_daily_data('AANCHALISP.BSE', 'full')
#print(stock_prices_daily)

#stock_prices_weekly = get_weekly_data('PNBHOUSING.BSE', 'true')
#print(stock_prices_weekly)

#stock_prices_monthly = get_monthly_data('PNBHOUSING.BSE', 'false')
#print(stock_prices_monthly)