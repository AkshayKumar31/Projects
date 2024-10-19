# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 10:48:46 2024

@author: aksha
"""

# MRMD - Max Return, Min Standard Deviation

import os 
import numpy as np
import pandas as pd


# Create a function to find the closest Stock Issued value
def find_closest_stock_issued(row, balance_df):
    symbol = row['Symbol']
    date = row['Date']
    
    # Filter df_balance for the given symbol
    filtered_balance = balance_df[balance_df['Symbol'] == symbol]
    
    if not filtered_balance.empty:
        # Find the closest date
        closest_date_idx = (filtered_balance['Date'] - date).abs().idxmin()
        return filtered_balance.loc[closest_date_idx, 'Share Issued']
    else:
        return None  # or some default value if no match is found


def top_stocks_return_std(exchange, return_window=252, std_div_window=252):
    
    current_dir = os.getcwd()
    data_path = current_dir + '/stock_timeseries/' + exchange
    
    files = os.listdir(data_path)
    
    stock_mrmd = pd.DataFrame(columns=['Symbol', 'Date', 'Close', 'Previous_Close', 'Daily_Return', 'N_Day_Return', 'Return_STD'])

    # Loop through each file to read data
    for file in files:
        if file.endswith('.csv'):
            print(file)
            # Read the CSV file
            file_path = os.path.join(data_path, file)
            df = pd.read_csv(file_path, usecols=['Date', 'Close'], parse_dates=['Date'])
            
            # Ensure the DataFrame is sorted by date
            df.sort_values('Date', inplace=True)
            
            df['Symbol'] = file.split('.')[0]
            
            # Create a column for previous close
            df['Previous_Close'] = df['Close'].shift(1)
            
            # Calculate daily returns as a percentage
            df['Daily_Return'] = ((df['Close'] - df['Previous_Close']) / df['Previous_Close']) * 100

            # Calculate the 10-day return as a percentage
            df['N_Day_Return'] = ((df['Close'] - df['Close'].shift(return_window)) / df['Close'].shift(return_window)) * 100
            
            # Calculate the mean normalized moving standard deviation for the default aprox. one year (252 trading days)
            # Calculate rolling standard deviation
            df['Return_STD'] = df['Daily_Return'].rolling(window=std_div_window).std()

            # Calculate the mean of the daily returns over the same window
            #df['Return_Mean'] = df['Daily_Return'].rolling(window=std_div_window).mean()

            # Normalize the standard deviation
            #df['Normalized_STD'] = df['Return_STD'] / df['Return_Mean']
            
            stock_mrmd = stock_mrmd._append(df)

    
    stock_mrmd.to_csv(current_dir + '/strategy_data/mrmd_data/' + 'stock_mrmd_summary.csv', index=False)
    
    capitalization_data = current_dir + '/stock_fundamentals/' + exchange
    
    balance_files = os.listdir(capitalization_data)
    balance_files = [f for f in balance_files if "balance_sheet" in f]
    
    stock_balance = pd.DataFrame(columns=['Symbol', 'Date', 'Share Issued'])
    
    for bfiles in balance_files:
        file_path = os.path.join(capitalization_data, bfiles)
        
        try:
            df = pd.read_csv(file_path, usecols=['Date', 'Share Issued'], parse_dates=['Date'])
        
            # Ensure the DataFrame is sorted by date
            df.sort_values('Date', inplace=True)
            
            print(bfiles.split('.')[0].split('_')[0])
        
            df['Symbol'] = bfiles.split('.')[0].split('_')[0]
        
            stock_balance = stock_balance._append(df)
        except:
            continue
    
    stock_balance.to_csv(current_dir + '/strategy_data/mrmd_data/' + 'stock_balance_summary.csv', index=False)
    
    return 0


def get_dated_mrmd_summary(n_years, mode = 'quarterly'):
    
    #top_stocks_return_std(exchange, return_window, std_div_window)
    
    current_dir = os.getcwd()
    
    data_path = current_dir + '/strategy_data/mrmd_data/' + 'stock_mrmd_summary.csv'
    balance_path = current_dir + '/strategy_data/mrmd_data/' + 'stock_balance_summary.csv'
    
    df = pd.read_csv(data_path)
    
    df_balance = pd.read_csv(balance_path)
    
    # Convert Date columns, handling potential format issues
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce', format=None)  # You can specify a format if known
    df_balance['Date'] = pd.to_datetime(df_balance['Date'], errors='coerce', format=None)
    
    # Check for NaT values
    if df['Date'].isnull().any() or df_balance['Date'].isnull().any():
        print("Warning: Some dates could not be parsed.")
    
    # Calculate the start date for filtering
    current_year = pd.to_datetime("now").year
    start_date = pd.Timestamp(f"{current_year - n_years}-01-01")
    print(start_date)

    # Filter the DataFrame
    filtered_df = df[df['Date'] > start_date]

    if mode == 'quarterly':
        # Get the last date of each quarter
        last_quarter_dates = pd.date_range(start=filtered_df['Date'].min(), 
                                            end=filtered_df['Date'].max(), 
                                            freq='QE')

        # For each symbol, find the closest date to the last date of each quarter
        result = []
        for symbol in filtered_df['Symbol'].unique():
            symbol_data = filtered_df[filtered_df['Symbol'] == symbol]
            for q_date in last_quarter_dates:
                closest_date = symbol_data.iloc[(symbol_data['Date'] - q_date).abs().argsort()[:1]]
                closest_date['Date'] = q_date  # Set the Date column to q_date
                result.append(closest_date)

        # Combine results into a final DataFrame
        final_df = pd.concat(result).drop_duplicates()
        
        # Ensure both DataFrames are sorted by date
        final_df = final_df.sort_values(by=['Symbol', 'Date'])
        df_balance = df_balance.sort_values(by=['Symbol', 'Date'])
        
        # Apply the function to each row in df
        final_df['Share Issued'] = final_df.apply(find_closest_stock_issued, axis=1, balance_df=df_balance)
        
        final_df.to_csv(current_dir + '/strategy_data/mrmd_data/' + 'quarterly_mrmd_summary.csv', index=False)

    elif mode == 'weekly':
        # Get the last day of each week from the filtered DataFrame
        filtered_df['Week'] = filtered_df['Date'].dt.isocalendar().week
        filtered_df['Year'] = filtered_df['Date'].dt.isocalendar().year

        # Find the last entry for each week for each symbol, retaining all columns
        final_df = (filtered_df.sort_values('Date')
                     .groupby(['Symbol', 'Year', 'Week'], as_index=False)
                     .agg(lambda x: x.iloc[-1])  # Get the last entry for each group
                     .reset_index(drop=True))
    
        # Calculate the last date of the week for each entry
        final_df['Date'] = final_df.apply(
            lambda x: pd.Timestamp(x['Year'], 1, 1) + pd.DateOffset(weeks=x['Week'] - 1, days=6),
            axis=1
        )

        # Ensure both DataFrames are sorted by date
        final_df = final_df.sort_values(by=['Symbol', 'Date'])
        df_balance = df_balance.sort_values(by=['Symbol', 'Date'])
    
        # Apply the function to each row in df
        final_df['Share Issued'] = final_df.apply(find_closest_stock_issued, axis=1, balance_df=df_balance)
        
        final_df.to_csv(current_dir + '/strategy_data/mrmd_data/' + 'weekly_mrmd_summary.csv', index=False)

    else:
        raise ValueError("Mode must be either 'Quarterly' or 'Weekly'")
    
    return 0


def mrmd_strategy_return(exchange, n_years, cap_cutoff, n_return, n_std_div, trading_mode = 'reinvestement', regenerate = 'true', mode = 'quarterly', return_window = 252, std_div_window = 252):
    
    if regenerate == 'true':
        
        top_stocks_return_std(exchange, return_window, std_div_window)
        get_dated_mrmd_summary(n_years, mode)
    
    current_dir = os.getcwd()
    
    if mode == 'quarterly':
        
        df = pd.read_csv(current_dir + '/strategy_data/mrmd_data/' + 'quarterly_mrmd_summary.csv')
        
    
    elif mode == 'weekly':
        # issue in weekly  - replace the dates with each week last date 
        
        df = pd.read_csv(current_dir + '/strategy_data/mrmd_data/' + 'weekly_mrmd_summary.csv')
    
    # Sort the data by date
    df['Date'] = pd.to_datetime(df['Date'])
    df.sort_values(by='Date', inplace=True)
    # Convert specified columns to float
    df['Close'] = df['Close'].astype(float)
    df['Daily_Return'] = df['Daily_Return'].astype(float)
    df['N_Day_Return'] = df['N_Day_Return'].astype(float)
    df['Return_STD'] = df['Return_STD'].astype(float)
    df['Share Issued'] = df['Share Issued'].astype(float)

    total_profit = 0
    total_invested = 0  # Total investment amount
    invested_stocks = {}  # Track stocks and their purchase prices

    # Get the unique dates
    unique_dates = df['Date'].unique()
    print(unique_dates )
    
    # Iterate over each unique date
    for i, date in enumerate(unique_dates):
        daily_data = df[df['Date'] == date]

        # Calculate market capitalization
        daily_data['Market_Cap'] = daily_data['Share Issued'] * daily_data['Close']

        # Filter stocks with market cap > 500 crore
        filtered_stocks = daily_data[daily_data['Market_Cap'] > cap_cutoff]  # 500 crore = 500e7

        # Pick top 300 stocks by N_Day_Return
        top_stocks = filtered_stocks.nlargest(n_return, 'N_Day_Return')

        # Pick top 20 stocks with the lowest Return_STD
        selected_stocks = top_stocks.nsmallest(n_std_div, 'Return_STD')
        
        #print(top_stocks)

        # On the first date, buy all selected stocks at their close price
        
        if i == 0:
            for stock in selected_stocks['Symbol']:
                stock_data = daily_data[daily_data['Symbol'] == stock]
                #print(stock_data['Close'].iloc[0])
                invested_stocks[stock] = stock_data['Close'].iloc[0]  # Store purchase price
                total_profit -= stock_data['Close'].iloc[0]  # Initial investment
                total_invested += stock_data['Close'].iloc[0]  # Track total invested amount
                #print(total_profit)

        else:  # Not the first date
            # Track stocks to sell
            stocks_to_sell = set(invested_stocks.keys()) - set(selected_stocks['Symbol'])

            # Sell stocks that are not in the new selection
            for stock in stocks_to_sell:
                stock_data = daily_data[daily_data['Symbol'] == stock]
                total_profit += stock_data['Close'].iloc[0]  # Sell at current Close price
                #print(total_profit)
                del invested_stocks[stock]  # Remove from invested stocks

            # Update invested stocks
            for stock in selected_stocks['Symbol']:
                if stock not in invested_stocks:  # If it's a new stock
                    stock_data = daily_data[daily_data['Symbol'] == stock]
                    invested_stocks[stock] = stock_data['Close'].iloc[0]  # Store purchase price
                    if trading_mode == 'reinvestement':
                        if total_profit < stock_data['Close'].iloc[0]:
                            total_invested += stock_data['Close'].iloc[0]  # Update total invested amount
                        else:
                            total_invested += 0
                    else:
                        total_invested += stock_data['Close'].iloc[0]
                    total_profit -= stock_data['Close'].iloc[0]  # Investment cost
                    #print(total_profit)

        # Calculate profit for stocks still held
        for stock, purchase_price in invested_stocks.items():
            stock_data = daily_data[daily_data['Symbol'] == stock]
            total_profit += stock_data['Close'].iloc[0] - purchase_price  # Calculate profit
            #print(total_profit)

    # Total returns calculation (profit or loss)
    total_returns = total_profit  # Total returns based on profit
    total_return_percentage = (total_returns / total_invested) * 100   # Return percentage

    # Return the results
    return total_profit, total_invested, total_return_percentage
    
    