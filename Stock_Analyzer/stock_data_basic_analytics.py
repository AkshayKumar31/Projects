# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 10:49:34 2023

@author: aksha
"""

import pandas as pd
import numpy as np
import os 
import strategy.super_trend as s
from datetime import datetime

def missing_dates_list(file):
    data = pd.read_csv(file)
    data['Date'] = pd.to_datetime(data['Date'])
    minimum_date = min(data['Date'])
    maximum_date = max(data['Date'])
    date_range = pd.date_range(start=minimum_date, end=maximum_date, freq='B')  # 'B' for business days (excludes weekends)
    missing_date = date_range[~date_range.isin(data['Date'])]
    missing_date_per = round((len(date_range[~date_range.isin(data['Date'])])/len(data['Date']))*100,2)
    
    return missing_date, missing_date_per

def growth_metric(days, file):
    
    data = pd.read_csv(file)
    data['Date'] = pd.to_datetime(data['Date'])
    maximum_date = max(data['Date'])
    lower_date = maximum_date - pd.Timedelta(days, unit='D')
    # Filter the DataFrame using boolean indexing
    data = data[(data['Date'] >= lower_date) & (data['Date'] <= maximum_date)]
    max_analysis_date = max(data['Date'])
    min_analysis_date = min(data['Date'])
    #print(file)
    # Calculate the average of 'open', 'high', 'low', and 'close' for the latest date
    latest_date_data = data[data['Date'] == max_analysis_date]
    earliest_date_data = data[data['Date'] == min_analysis_date]

    latest_avg = (latest_date_data['Open'] + latest_date_data['High'] + latest_date_data['Low'] + latest_date_data['Close'])/4
    earliest_avg = (earliest_date_data['Open'] + earliest_date_data['High'] + earliest_date_data['Low'] + earliest_date_data['Close'])/4
    #print(str(list(latest_avg)[0]) + ' ' + str(list(earliest_avg)[0]))
    
    growth_per = round(((list(latest_avg)[0] - list(earliest_avg)[0])/list(earliest_avg)[0])*100,2)
    avg_volume = int(np.mean(list(data['Volume'])))
    
    return growth_per, avg_volume
    

def stock_summary(folder, exchange, n_duration = 14, multiplier = 1.5, time_aggegration = 'daily', window_len = 1):
    
    path = folder + '/' + exchange
    
    files = os.listdir(path)
    
    data_list = [] 
    
    for file in files:
        symbol = file.split('.')[0]
        with open('stocks.txt', 'w') as filesto:
            filesto.write(symbol)
        data = pd.read_csv(path + '/' + file)
        data['Date'] = pd.to_datetime(data['Date'])
        minimum_date = min(data['Date'])
        maximum_date = max(data['Date'])
        
        missing_dates, missing_date_per = missing_dates_list(path + '/' + file)
        
        growth_per_30, avg_vol_30 = growth_metric(30, path + '/' + file)
        growth_per_7, avg_vol_7 = growth_metric(7, path + '/' + file)
        
        try:
            latest_signal, latest_trend, signal_start_date, signal_duration, trend_start_date, trend_duration, TR_data = s.calculate_super_trend(data, n_duration, multiplier, time_aggegration, window_len)
            TR_data.to_csv('E:/Programming/Python/Stocks/Stock_Analyzer/strategy_data/supertrend_data'+ '/' + exchange + '/' + symbol + '.csv')
        except:
            latest_signal, latest_trend, signal_start_date, signal_duration, trend_start_date, trend_duration = 'Null', 0, 'Null', '0', 'Null', '0'
        
        latest_closing_price = round(TR_data['Close'].iloc[-1], 2)
        data_list.append([symbol, minimum_date, maximum_date, missing_date_per, latest_closing_price, growth_per_30, avg_vol_30, growth_per_7, avg_vol_7, latest_signal, latest_trend, signal_start_date, signal_duration, trend_start_date, trend_duration])
        
    
    df = pd.DataFrame(data_list, columns=['symbol', 'min_date', 'max_date', 'missing_dates_per', 'latest_closing_price', 'growth_per_30', 'avg_vol_30', 'growth_per_7', 'avg_vol_7', 'latest_signal', 'latest_trend', 'signal_start_date', 'signal_duration', 'trend_start_date', 'trend_duration'])
    
    return df

def portfolio_analysis_summary(user, exchange):
    
    portfolio_ledger = os.getcwd() + '/portfolio_data/ledger.csv'
    
    ledger = pd.read_csv(portfolio_ledger)
    ledger = ledger[ledger['user']==user]
    ledger['action_date'] = pd.to_datetime(ledger['action_date'], errors='coerce')
    ledger['added_date'] = pd.to_datetime(ledger['added_date'], errors='coerce')
    #print(ledger['action_date'])
    
    # Create a new column for effective date
    ledger['effective_date'] = ledger['action_date'].fillna(ledger['added_date'])
    #print(ledger)
    # Group by 'symbol' and get rows with max effective_date and non-null 'action'
    #result = ledger.loc[ledger.groupby('symbol')['effective_date'].idxmax()]
    #result = result[['symbol', 'action', 'price', 'quantity', 'effective_date']]
    # Calculate price per share
    #result['price_per_share'] = result['price'] / result['quantity']
    #print(result)
    
    symbols = ledger['symbol'].unique().tolist()
    
    stock_latest = pd.DataFrame(columns=['symbol', 'exchange', 'latest_date', 'closing_price', 'last_action', 'last_action_date', 'current_principle', 'current_quantity', 'current_buy_price_avg', 'total_PL', 'unrealized_PL'])
    for stock in symbols:
        #print(stock)
        if os.path.exists(os.getcwd() + '/stock_timeseries/' + exchange + '/' + stock + '.csv'):
            stock_data = pd.read_csv(os.getcwd() + '/stock_timeseries/' + exchange + '/' + stock + '.csv')
            stock_data['Date'] = pd.to_datetime(stock_data['Date'], errors='coerce')
        
            latest_data = stock_data.loc[stock_data['Date'].idxmax()]
        
            ledger_symbol = ledger[ledger['symbol']==stock].reset_index(drop=True)
            ledger_symbol = ledger_symbol.sort_values(by=['effective_date', 'action_number'], ascending=[True, True])
            result = ledger_symbol.loc[ledger_symbol['effective_date'].idxmax()]
        
            cur_principle = 0
            cur_quant = 0
            total_real_pl = 0
            unreal_pl = 0
            average_buy_price = 0
            for index, row in ledger_symbol.iterrows():
                if row['action'] == 'Buy':
                    cur_principle = cur_principle + row['price']
                    cur_quant = cur_quant + row['quantity']
                    total_real_pl = total_real_pl
                    if cur_quant != 0:
                        average_buy_price = cur_principle/cur_quant
                    else:
                        average_buy_price = 0.0
                    if latest_data['Date']>result['effective_date']:
                        unreal_pl = ((latest_data['Close'] * cur_quant) - cur_principle) 
                    else:
                        unreal_pl = -0.00
                elif row['action'] == 'Sell':
                    cur_principle = cur_principle - (row['quantity'] * average_buy_price)
                    cur_quant = cur_quant - row['quantity']
                    total_real_pl = total_real_pl + (row['price'] - (row['quantity'] * average_buy_price))
                    if cur_quant != 0:
                        average_buy_price = cur_principle/cur_quant
                    else:
                        average_buy_price = 0.0
                    if latest_data['Date']>result['effective_date']:
                        unreal_pl = latest_data['Close'] * cur_quant - cur_principle 
                    else:
                        unreal_pl = -0.00
                elif row['action'] == 'Split':
                    cur_principle = cur_principle
                    cur_quant = cur_quant*row['split ratio']
                    total_real_pl = total_real_pl
                    if cur_quant != 0:
                        average_buy_price = cur_principle/cur_quant
                    else:
                        average_buy_price = 0.0
                    if latest_data['Date']>result['effective_date']:
                        unreal_pl = ((latest_data['Close'] * cur_quant) - cur_principle) 
                    else:
                        unreal_pl = -0.00
                
            # Append latest data to stock_latest DataFrame
            stock_latest = stock_latest._append({
                       'symbol': stock,
                       'exchange': exchange,
                       'user_name': user,
                       'latest_date': latest_data['Date'],
                       'closing_price': round(latest_data['Close'],2),
                       'last_action': result['action'],
                       'last_action_date': result['effective_date'],
                       'current_principle': round(cur_principle,2),
                       'current_quantity': cur_quant,
                       'current_buy_price_avg': round(average_buy_price,2),
                       'total_PL': round(total_real_pl,2),
                       'unrealized_PL': round(unreal_pl,2)
                       }, ignore_index=True)
        else:
            # Append latest data to stock_latest DataFrame
            stock_latest = stock_latest._append({
                       'symbol': stock,
                       'exchange': 'N/A',
                       'user_name': user,
                       'latest_date': '1900-01-01',
                       'closing_price': 0.00,
                       'last_action': 'N/A',
                       'last_action_date': '1900-01-01',
                       'current_principle': 0.00,
                       'current_quantity': 0.00,
                       'current_buy_price_avg': 0.00,
                       'total_PL': 0.00,
                       'unrealized_PL': 0.00
                       }, ignore_index=True)
        
    stock_latest.to_csv(os.getcwd() + '/portfolio_data/' + user + '_' + exchange +'_portfolio_summary.csv', index=False)
    
    return 0

# Test functions 
#folder = 'E:/Programming/Python/Stocks/Stock_Analyzer/stock_timeseries'
#exchange = 'BSE'
#df = stock_summary(folder, exchange)

#print(df)

#portfolio_analysis_summary('Anant', 'NSE')
