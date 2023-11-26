# -*- coding: utf-8 -*-
"""
Created on Sat Sep 23 10:57:54 2023

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

def get_income_statement(symbol):
    # Doesn't work for Indian markets
    # reports latest data for earnings and financials released by the company
    
    url = 'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol='+symbol+'&apikey='+alpha_vantage_key
    r = requests.get(url)
    data = dict(r.json())
    
    data = pd.DataFrame(data['annualReports'])
    
    return data

def get_balance_sheet(symbol):
    # Doesn't work for Indian markets
    # reports latest data for earnings and financials released by the company
    
    url = 'https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol='+symbol+'&apikey='+alpha_vantage_key
    r = requests.get(url)
    data = dict(r.json())
    
    data = pd.DataFrame(data['annualReports'])
    
    return data

def get_cash_flow(symbol):
    # Doesn't work for Indian markets
    # reports latest data for earnings and financials released by the company
    
    url = 'https://www.alphavantage.co/query?function=CASH_FLOW&symbol='+symbol+'&apikey='+alpha_vantage_key
    r = requests.get(url)
    data = dict(r.json())
    
    data = pd.DataFrame(data['annualReports'])
    
    return data

def get_earnings(symbol):
    # Doesn't work for Indian markets
    # reports latest data for earnings and financials released by the company
    
    url = 'https://www.alphavantage.co/query?function=EARNINGS&symbol='+symbol+'&apikey='+alpha_vantage_key
    r = requests.get(url)
    data = dict(r.json())
    #print(data.keys())
    
    data_annual = pd.DataFrame(data['annualEarnings'])
    data_quarterly = pd.DataFrame(data['quarterlyEarnings'])
    
    return data_annual, data_quarterly

# Test Functions
#income_statement = get_income_statement('AAPL')
#print(income_statement)

#balance_sheet = get_balance_sheet('AAPL')
#print(balance_sheet)

#cash_flow = get_cash_flow('AAPL')
#print(cash_flow)

#annual_earnings, quarterly_earnings = get_earnings('ABFRL.BSE')
#print(quarterly_earnings)