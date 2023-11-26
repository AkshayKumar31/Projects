# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 09:52:10 2023

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

def get_market_status():
    
    # Get the current UTC time
    utc_now = datetime.utcnow()

    # Define the timezone for India (IST)
    india_timezone = pytz.timezone('Asia/Kolkata')

    # Convert the UTC time to India time
    india_time = utc_now.replace(tzinfo=pytz.utc).astimezone(india_timezone)

    # Format the time as a string
    india_time_str = india_time.strftime('%Y-%m-%d %H:%M:%S %Z%z')
    
    url = 'https://www.alphavantage.co/query?function=MARKET_STATUS&apikey='+alpha_vantage_key
    r = requests.get(url)
    data = r.json()
    
    data = pd.DataFrame(data['markets'])
    data = data[data['region']=='India']
    
    data['timestamp'] = india_time_str
    
    current_status = list(data['current_status'])[0]
    
    
    return data, current_status

def ticker_search(keyword = 'abfr'):
    
    url = 'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords='+keyword+'&apikey='+alpha_vantage_key
    r = requests.get(url)
    data = r.json()
    
    data = pd.DataFrame(data['bestMatches'])
    data = data[data['4. region']=='India/Bombay']
    
    return data

def update_csv(data, filepath, indexing_column):
    
    existing_data = pd.read_csv(filepath)
    
    new_rows = data[~data[indexing_column].isin(existing_data[indexing_column])]
    
    # Append new rows to the existing data
    updated_data = pd.concat([existing_data, new_rows], ignore_index=True).drop_duplicates()

    # Write the updated DataFrame back to the CSV file
    updated_data.to_csv(filepath, index=False)
    

# Test Function
#market_data, market_status = get_market_status()
#print(market_data)
#print(market_status)

#tickers = ticker_search('hdfc')
#print(tickers)