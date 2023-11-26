# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 10:22:13 2023

@author: aksha
"""

import pandas as pd
from datetime import datetime
import yfinance as yf

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
    prices = stox.history(period)
    print(prices)
    prices = pd.DataFrame(prices)
    prices.reset_index(inplace=True)
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
    
    

# Test function

#prices = get_price_timeseries('ABFRL', 'NSE', '5d')
#print(metadata)
#print(' ')
#print(prices)


'''
fundamentals = cash_flow_data('ABFRL', 'BSE')
print(fundamentals)
'''
'''
holdings = share_holder_division('ABFRL', 'BSE')
print(holdings)
'''