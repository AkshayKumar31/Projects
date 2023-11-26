# -*- coding: utf-8 -*-
"""
Created on Sat Sep 23 11:26:35 2023

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

def get_stock_sma():
    # Simple Moving Average
    
    url = 'https://www.alphavantage.co/query?function=SMA&symbol=ABFRL.BSE&interval=weekly&time_period=10&series_type=open&apikey='+alpha_vantage_key
    r = requests.get(url)
    data = r.json()

    
    

get_stock_sma()