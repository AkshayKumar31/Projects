# -*- coding: utf-8 -*-
"""
Created on Sat Nov 25 10:13:56 2023

@author: aksha
"""

import pandas as pd

def calculate_super_trend(timeseries_data, n = 14, multiplier=1.5, time_aggegration = 'daily', window_len = 5):
    
    # Convert the "date" column to datetime format if it's not already
    timeseries_data['Date'] = pd.to_datetime(timeseries_data['Date'])
    
    if time_aggegration == 'weekly':
        # Set the 'Date' column as the index
        timeseries_data.set_index('Date', inplace=True)
        print(timeseries_data)

        # Resample the data to weekly frequency (ending on Friday)
        weekly_data = timeseries_data.resample('W-Fri').agg({
                        'Open': 'first',
                        'High': 'max',
                        'Low': 'min',
                        'Close': 'last',
                })

        # Reset the index to have 'Date' as a column
        weekly_data.reset_index(inplace=True)
        
        timeseries_data = weekly_data

    # Sort the DataFrame based on the "date" column in descending order
    df_sorted = timeseries_data.sort_values(by='Date', ascending=True)
    
    # Initialize the 'Trend' column
    df_sorted.loc[0, 'trend'] = 'uptrend'
    # Iterate through the DataFrame to set the 'Trend' value
    for i in range(1, len(df_sorted)):
        if df_sorted.loc[i, 'Close'] > df_sorted.loc[i - 1, 'Close']:
            df_sorted.loc[i, 'trend'] = 'uptrend'
        elif df_sorted.loc[i, 'Close'] < df_sorted.loc[i - 1, 'Close']:
            df_sorted.loc[i, 'trend'] = 'downtrend'
        else:
            df_sorted.loc[i, 'trend'] = df_sorted.loc[i - 1, 'trend']
    
    dates = df_sorted ['Date'].to_list()
    high = df_sorted ['High'].to_list()
    low = df_sorted ['Low'].to_list()
    close = [0] + df_sorted['Close'].tolist()[:-1]
    df_sorted['Prev Close'] = close
    
    # Calculate True Range (TR)
    tr = [max(high[i] - low[i], abs(high[i] - close[i]), abs(low[i] - close[i])) for i in range(len(dates))]

    # Add the calculated TR to the DataFrame
    df_sorted['TrueRange'] = tr
    
    # Calculate Wilder's ATR
    atr = [0] * n  # Initialize the first n values with 0
    for i in range(n, len(tr)):
        atr_value = (atr[-1] * (n - 1) + tr[i]) / n
        atr.append(atr_value)

    # Add the calculated ATR to the DataFrame
    df_sorted['WilderATR'] = atr
    
    # Calculate SuperTrend
    df_sorted['UpperBand'] = 0.5*(df_sorted['Open'] + df_sorted['Close']) + multiplier * df_sorted['WilderATR']
    df_sorted['UpperBand'] = df_sorted['UpperBand'].rolling(window=window_len, min_periods=1).mean()
    df_sorted['LowerBand'] = 0.5*(df_sorted['Open'] + df_sorted['Close']) - multiplier * df_sorted['WilderATR']
    df_sorted['LowerBand'] = df_sorted['LowerBand'].rolling(window=window_len, min_periods=1).mean()

    # Initialize SuperTrend and trend direction
    df_sorted['SuperTrend'] = 0.0
    df_sorted['in_uptrend'] = True
    
    # Initialize buy and sell points
    df_sorted['BuySignal'] = 0
    df_sorted['SellSignal'] = 0

    for i in range(1, len(df_sorted)):
        if df_sorted.at[i - 1, 'in_uptrend'] and df_sorted.at[i, 'Close'] <= df_sorted.at[i - 1, 'LowerBand']:
            df_sorted.at[i, 'in_uptrend'] = False
            df_sorted.at[i, 'SuperTrend'] = df_sorted.at[i, 'UpperBand']
            df_sorted.at[i, 'SellSignal'] = df_sorted.at[i, 'Close']
        elif not df_sorted.at[i - 1, 'in_uptrend'] and df_sorted.at[i, 'Close'] >= df_sorted.at[i - 1, 'UpperBand']:
            df_sorted.at[i, 'in_uptrend'] = True
            df_sorted.at[i, 'SuperTrend'] = df_sorted.at[i, 'LowerBand']
            df_sorted.at[i, 'BuySignal'] = df_sorted.at[i, 'Close']
        else:
            df_sorted.at[i, 'in_uptrend'] = df_sorted.at[i - 1, 'in_uptrend']
            df_sorted.at[i, 'SuperTrend'] = df_sorted.at[i - 1, 'LowerBand'] if df_sorted.at[i - 1, 'in_uptrend'] else df_sorted.at[i - 1, 'UpperBand']
            df_sorted.at[i, 'SellSignal'] = df_sorted.at[i-1, 'SellSignal']
            df_sorted.at[i, 'BuySignal'] = df_sorted.at[i-1, 'BuySignal']
    
    # Calculate average super trend for non-overlapping periods
    #df_sorted['AverageSuperTrend'] = df_sorted['SuperTrend'].rolling(window=window_len, min_periods=1).mean()
    
    df_sorted = df_sorted.reset_index(drop=True)
    
    # Drop the first row
    df_sorted = df_sorted.drop(df_sorted.index[0])
    
    # Check if the last row has a non-zero BuySignal
    if df_sorted.iloc[-1]['BuySignal'] != 0:
        latest_signal = 'Buy'
        signal_start_date = df_sorted.loc[df_sorted['SellSignal'] != 0]['Date'].max()
        #print(signal_start_date)
        signal_duration = (df_sorted.iloc[-1]['Date'].date() - signal_start_date.date()).days
    # Check if the last row has a non-zero SellSignal
    elif df_sorted.iloc[-1]['SellSignal'] != 0:
        latest_signal = 'Sell'
        signal_start_date = df_sorted.loc[df_sorted['BuySignal'] != 0]['Date'].max()
        signal_duration = (df_sorted.iloc[-1]['Date'].date() - signal_start_date.date()).days
    else:
        latest_signal = 'Undetermined'
        signal_start_date = df_sorted.iloc[-1]['Date']
        
    '''   
    if df_sorted.iloc[-1]['in_uptrend'] == True:
        latest_trend = 1
    elif df_sorted.iloc[-1]['in_uptrend'] == False:
        latest_trend = -1
    else:
        latest_trend = 0
    '''
        
    # Determine the latest trend
    if df_sorted.iloc[-1]['trend'] == 'uptrend':
        latest_trend = 1
        # Find the latest date since the uptrend started
        trend_start_date = df_sorted.loc[df_sorted['trend'] == 'downtrend']['Date'].max()
    elif df_sorted.iloc[-1]['trend'] == 'downtrend':
        latest_trend = -1
        # Find the latest date since the downtrend started
        trend_start_date = df_sorted.loc[df_sorted['trend'] == 'uptrend']['Date'].max()
    else:
        latest_trend = 0
        trend_start_date = None  # No trend start date for undetermined trend

    # Calculate the duration of the current trend
    if trend_start_date is not None:
        trend_duration = (df_sorted.iloc[-1]['Date'].date() - trend_start_date.date()).days
    else:
        trend_duration = 0  # No duration for undetermined trend
    
    #print(df_sorted)
    #print(latest_signal)
    #print(signal_duration)
    signal_duration = int(str(signal_duration).split(' ')[0])
    trend_duration = int(str(trend_duration).split(' ')[0])

    return latest_signal, latest_trend, signal_start_date, signal_duration, trend_start_date, trend_duration, df_sorted[['Date', 'High', 'Low', 'Close', 'Prev Close', 'TrueRange', 'WilderATR', 'UpperBand', 'LowerBand', 'SuperTrend', 'in_uptrend', 'BuySignal', 'SellSignal', 'trend']]
    
    
'''
# test function 

data = pd.read_csv('E:/Programming/Python/Stocks/Stock_Analyzer/stock_timeseries/NSE/PCJEWELLER.csv')

latest_signal, latest_trend, signal_start_date, signal_duration, trend_start_date, trend_duration, TR_data = calculate_super_trend(data, 14, 1.5, 'daily', 1)
#print(signal_duration)
#print(str(latest_signal) + ':' + str(latest_trend) + ':' + str(signal_start_date) + ':' + str(signal_duration))
print(TR_data)

# Extract the last 30 values for plotting
last_30_values = TR_data.tail(100)

import matplotlib.pyplot as plt

# Filter rows where BuySignal or SellSignal is not zero
buy_signals = last_30_values[last_30_values['BuySignal'] != 0]
sell_signals = last_30_values[last_30_values['SellSignal'] != 0]

# Plotting the SuperTrend
plt.figure(figsize=(10, 6))
#plt.plot(last_30_values['Date'], last_30_values['AverageSuperTrend'], label='Avg SuperTrend', color='blue')
plt.plot(last_30_values['Date'], last_30_values['SuperTrend'], label='SuperTrend', color='k')
#plt.plot(last_30_values['Date'], last_30_values['UpperBand'], label='Upper Band', linestyle='--', color='green')
#plt.plot(last_30_values['Date'], last_30_values['LowerBand'], label='Lower Band', linestyle='--', color='red')
plt.scatter(buy_signals['Date'], buy_signals['BuySignal'], marker='*', color='green', label='Buy Signal')
plt.scatter(sell_signals['Date'], sell_signals['SellSignal'], marker='*', color='red', label='Sell Signal')
plt.plot(last_30_values['Date'], last_30_values['Close'], label='Close', color='red')#, marker='o')
plt.title('SuperTrend Plot (Last 30 Values)')
plt.xlabel('Date')
plt.ylabel('Price')
plt.xticks(rotation=45)
plt.legend()
plt.show()
'''