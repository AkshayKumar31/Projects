# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 10:49:34 2023

@author: aksha
"""

import pandas as pd
import numpy as np
import os 

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
    

def stock_summary(folder, exchange):
    
    path = folder + '/' + exchange
    
    files = os.listdir(path)
    
    data_list = [] 
    
    for file in files:
        symbol = file.split('.')[0]
        data = pd.read_csv(path + '/' + file)
        data['Date'] = pd.to_datetime(data['Date'])
        minimum_date = min(data['Date'])
        maximum_date = max(data['Date'])
        missing_dates, missing_date_per = missing_dates_list(path + '/' + file)
        growth_per_30, avg_vol_30 = growth_metric(30, path + '/' + file)
        growth_per_7, avg_vol_7 = growth_metric(7, path + '/' + file)
    
        data_list.append([symbol, minimum_date, maximum_date, missing_date_per, growth_per_30, avg_vol_30, growth_per_7, avg_vol_7])
    
    df = pd.DataFrame(data_list, columns=['symbol', 'min_date', 'max_date', 'missing_dates_per', 'growth_per_30', 'avg_vol_30', 'growth_per_7', 'avg_vol_7'])
    
    return df
    

# Test functions 
#folder = 'E:/Programming/Python/Stocks/Stock_Analyzer/stock_timeseries'
#exchange = 'BSE'
#df = stock_summary(folder, exchange)

#print(df)
