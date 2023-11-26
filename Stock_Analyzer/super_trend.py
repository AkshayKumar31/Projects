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
    
    # Drop the last row
    df_sorted = df_sorted.drop(df_sorted.index[0])

    return df_sorted[['Date', 'High', 'Low', 'Close', 'Prev Close', 'TrueRange', 'WilderATR', 'UpperBand', 'LowerBand', 'SuperTrend', 'in_uptrend', 'BuySignal', 'SellSignal']]
    
    
'''
# test function 

data = pd.read_csv('E:/Programming/Python/Stocks/Stock_Analyzer/stock_timeseries/NSE/VBL.csv')

TR_data = calculate_super_trend(data, 14, 1.5, 'daily', 5)
print(TR_data)

# Extract the last 30 values for plotting
last_30_values = TR_data.tail(200)

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