# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 10:22:13 2023

@author: aksha
"""

import pandas as pd
from datetime import datetime
import yfinance as yf
import os
import json

def transform_dataframe(dataframe):
    
    dataframe = dataframe.T
    dataframe.columns = dataframe.iloc[0]
    dataframe = dataframe.iloc[1:]
    dataframe['Date'] = pd.to_datetime(dataframe.index)
    dataframe.reset_index(drop=True, inplace=True)
    
    return dataframe

def get_price_timeseries(stock_ticker, exchange, period):
    # Valid periods = '1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'
    
    if exchange == 'NSE':
        symbol = stock_ticker + '.' + 'NS'
        
    elif exchange == 'BSE':
        symbol = stock_ticker + '.' + 'BO'
        
    stox = yf.Ticker(symbol)
    #print(stox)
    prices = stox.history(period)
    #print(prices)
    prices = pd.DataFrame(prices)
    prices.reset_index(inplace=True)
    print(prices)
    prices['Date'] = prices['Date'].dt.date
    #print(prices.columns)
    
    return prices

def income_statement_data(stock_ticker, exchange):
    
    if exchange == 'NSE':
        symbol = stock_ticker + '.' + 'NS'
        
    elif exchange == 'BSE':
        symbol = stock_ticker + '.' + 'BO'
    
    stox = yf.Ticker(symbol)
    stmt = stox.quarterly_income_stmt
    stmt.reset_index(inplace=True)
    stmt = transform_dataframe(stmt)
    #print(stmt.columns)
    
    return stmt

def balance_sheet_data(stock_ticker, exchange):
    
    if exchange == 'NSE':
        symbol = stock_ticker + '.' + 'NS'
        
    elif exchange == 'BSE':
        symbol = stock_ticker + '.' + 'BO'
    
    stox = yf.Ticker(symbol)
    bsht = stox.quarterly_balance_sheet
    bsht.reset_index(inplace=True)
    bsht = transform_dataframe(bsht)
    #print(bsht.columns)
    
    return bsht

def cash_flow_data(stock_ticker, exchange):
    
    if exchange == 'NSE':
        symbol = stock_ticker + '.' + 'NS'
        
    elif exchange == 'BSE':
        symbol = stock_ticker + '.' + 'BO'
    
    stox = yf.Ticker(symbol)
    cfwl = stox.quarterly_cashflow
    cfwl.reset_index(inplace=True)
    cfwl = transform_dataframe(cfwl)
    #print(cfwl.columns)
    
    return cfwl
    
def share_holder_division(stock_ticker, exchange):
    
    if exchange == 'NSE':
        symbol = stock_ticker + '.' + 'NS'
        
    elif exchange == 'BSE':
        symbol = stock_ticker + '.' + 'BO'
        
    stox = yf.Ticker(symbol)
    
    holders = stox.major_holders
    holders = pd.DataFrame(holders)
    holders.columns = ['Percentage Holdings', 'Legend']
    # Add a new column for the current date
    holders['Date'] = datetime.now().date()
    
    return holders

def get_company_description_summary(stock_ticker, exchange):
    
    file_path = os.getcwd() + '/stock_company_details/company_summary_fields.txt'
    
    if exchange == 'NSE':
        symbol = stock_ticker + '.' + 'NS'
        
    elif exchange == 'BSE':
        symbol = stock_ticker + '.' + 'BO'
        
    stox = yf.Ticker(symbol)
    #print(stox.info)
    
    with open(file_path, 'r') as file:
        data = file.read()
    
    #print(data)
    data_dict = json.loads(data)
    
    company_description = data_dict.get("company_description", [])
    valuation_ratios = data_dict.get("valuation_ratios", [])
    dividend_info = data_dict.get("dividend_info", [])
    key_ratios = data_dict.get("key_ratios", [])
    growth_metrics = data_dict.get("growth_metrics", [])
    #print(growth_metrics)
    
    info_dict = dict(stox.info)
    current_date_time = datetime.now()
    
    #print(info_dict)
    stock_summary = pd.DataFrame({key: [info_dict.get(key)] for key in company_description}) # Data refresh on update
    stock_summary['symbol'] = stock_ticker

    valuation = pd.DataFrame({key: [info_dict.get(key)] for key in valuation_ratios}) # Updated everyweek, appending new row 
    valuation['symbol'] = stock_ticker
    valuation['Date'] = current_date_time.date()
    
    dividend_inf = pd.DataFrame({key: [info_dict.get(key)] for key in dividend_info}) # Updated everyweek, appending new row
    dividend_inf['symbol'] = stock_ticker
    dividend_inf['lastDividendDate'] = pd.to_datetime(dividend_inf['lastDividendDate'], unit='s').dt.date
    
    key_ratio = pd.DataFrame({key: [info_dict.get(key)] for key in key_ratios}) # Updated everyweek, appending new row
    key_ratio['symbol'] = stock_ticker
    key_ratio['Date'] = current_date_time.date()
    
    growth_metrics = pd.DataFrame({key: [info_dict.get(key)] for key in growth_metrics}) # Updated everyweek, appending new row
    growth_metrics['symbol'] = stock_ticker
    growth_metrics['Date'] = current_date_time.date()
    
    return stock_summary, valuation, dividend_inf, key_ratio, growth_metrics
    
    

# Test function

#prices = get_price_timeseries('ICEMAKE', 'NSE', 'max')
#print(metadata)
#print(' ')
#print(prices)



#fundamentals = cash_flow_data('JGCHEM', 'BSE')
#print(fundamentals)

'''
holdings = share_holder_division('ABFRL', 'BSE')
print(holdings)
'''

#stock_summary, valuation, dividend_inf, key_ratio, growth_metrics = get_company_description_summary('JGCHEM', 'BSE')
#print(stock_summary)
#print(valuation)
#print(dividend_inf)
#print(key_ratio)
#print(growth_metrics)


