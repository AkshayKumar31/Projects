# -*- coding: utf-8 -*-
"""
Created on Sun Sep 24 10:25:51 2023

@author: aksha
"""

from flask import request, Flask, render_template, url_for, flash, redirect, session
import metadata_handler as m
import reference_data_handeler as r
import core_stock_data as c
import stock_data_basic_analytics as dq
import pandas as pd
import utility as u
import os

app = Flask(__name__)
app.secret_key = "stocks"

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        action = request.form.get("action")
        stock_data_to_change = request.form.get("stock_data_to_chnage")
        
        if action == "update_metadata":
            return redirect(url_for('metadata'))
        elif action == "update_reference_data":
            return redirect(url_for('reference_data'))
        elif stock_data_to_change == 'stock_BSE' and action == 'add_stock_data':
            return redirect(url_for('stock_data_load_bse'))
        elif stock_data_to_change == 'stock_NSE' and action == 'add_stock_data':
            return redirect(url_for('stock_data_load_nse'))
        elif stock_data_to_change == 'stock_BSE' and action == 'analyse_stock_data':
            return redirect(url_for('stock_data_update_bse'))
        elif stock_data_to_change == 'stock_NSE' and action == 'analyse_stock_data':
            return redirect(url_for('stock_data_update_nse'))

    return render_template('index.html')

@app.route("/update_metadata", methods=["GET", "POST"])
def metadata():
    if request.method == "POST":
        # Get the selected metadata value from the form
        folder = 'E:/Programming/Python/Stocks/Stock_Analyzer/meta_data'
        selected_metadata = request.form.get("metadata_to_update")
        action = request.form.get("action")
        
        if selected_metadata == 'exchanges' and action == 'update_metadata':
            metadata_to_update = '1'
            # Call the update_metadata function with the selected value
            m.update_metadata(metadata_to_update)
            csv_file_path = os.path.join(folder, 'exchanges.csv')
            table_name = 'Exchanges'
            
        elif selected_metadata == 'crypto_exchanges' and action == 'update_metadata':
            metadata_to_update = '2'
            # Call the update_metadata function with the selected value
            m.update_metadata(metadata_to_update)
            csv_file_path = os.path.join(folder, 'crypto_exchanges.csv')
            table_name = 'Crypto Exchanges'
            
        elif selected_metadata == 'technical_indicator' and action == 'update_metadata':
            metadata_to_update = '3'
            # Call the update_metadata function with the selected value
            m.update_metadata(metadata_to_update)
            csv_file_path = os.path.join(folder, 'technical_indicators.csv')
            table_name = 'Technical Indicators'
            
        elif selected_metadata == 'exchanges' and action == 'show_data':
            csv_file_path = os.path.join(folder, 'exchanges.csv')
            table_name = 'Exchanges'
            
        elif selected_metadata == 'crypto_exchanges' and action == 'show_data':
            csv_file_path = os.path.join(folder, 'crypto_exchanges.csv')
            table_name = 'Crypto Exchanges'
            
        elif selected_metadata == 'technical_indicator' and action == 'show_data':
            csv_file_path = os.path.join(folder, 'technical_indicators.csv')
            table_name = 'Technical Indicators'
        
        elif action == 'home_page':
            return redirect(url_for('index'))

        df = pd.read_csv(csv_file_path)
        # After processing the form, display the DataFrame as a table
        table_html = df.to_html(classes='table table-bordered table-striped', escape=False, index=False)

        flash(f"Updated metadata: {selected_metadata}")

        return render_template('metadata.html', table=table_html, table_name=table_name)
    return render_template('metadata.html', table=None, table_name=None)

@app.route("/update_reference_data", methods=["GET", "POST"])
def reference_data():
    if request.method == "POST":
        # Get the selected metadata value from the form
        folder = 'E:/Programming/Python/Stocks/Stock_Analyzer/reference_data'
        reference_data = request.form.get("reference_data_to_update")
        action = request.form.get("action")
        
        if reference_data == 'stock_BSE' and action == 'update_reference_data':
            csv_file_path = os.path.join(folder, 'stocks_BSE.csv')
            r.update_reference_data(reference_data)
            table_name = 'Stocks_BSE'
        
        elif reference_data == 'stock_NSE' and action == 'update_reference_data':
            csv_file_path = os.path.join(folder, 'stocks_NSE.csv')
            r.update_reference_data(reference_data)
            table_name = 'Stocks_NSE'
        
        elif reference_data == 'forex' and action == 'update_reference_data':
            csv_file_path = os.path.join(folder, 'forex_pairs.csv')
            r.update_reference_data(reference_data)
            table_name = 'Forex Pairs'
            
        elif reference_data == 'crypto' and action == 'update_reference_data':
            csv_file_path = os.path.join(folder, 'crypto_pairs.csv')
            r.update_reference_data(reference_data)
            table_name = 'Crypto Pairs'
            
        elif reference_data == 'etf_BSE' and action == 'update_reference_data':
            csv_file_path = os.path.join(folder, 'etfs_BSE.csv')
            r.update_reference_data(reference_data)
            table_name = 'ETFs_BSE'
        
        elif reference_data == 'etf_NSE' and action == 'update_reference_data':
            csv_file_path = os.path.join(folder, 'etfs_NSE.csv')
            r.update_reference_data(reference_data)
            table_name = 'ETFs_NSE'
            
        elif reference_data == 'indices_BSE' and action == 'update_reference_data':
            csv_file_path = os.path.join(folder, 'indices_BSE.csv')
            r.update_reference_data(reference_data)
            table_name = 'Indices_BSE'
        
        elif reference_data == 'indices_NSE' and action == 'update_reference_data':
            csv_file_path = os.path.join(folder, 'indices_NSE.csv')
            r.update_reference_data(reference_data)
            table_name = 'Indices_NSE'
            
        elif reference_data == 'stock_BSE' and action == 'show_data':
            csv_file_path = os.path.join(folder, 'stocks_BSE.csv')
            table_name = 'Stocks_BSE'
        
        elif reference_data == 'stock_NSE' and action == 'show_data':
            csv_file_path = os.path.join(folder, 'stocks_NSE.csv')
            table_name = 'Stocks_NSE'
            
        elif reference_data == 'forex' and action == 'show_data':
            csv_file_path = os.path.join(folder, 'forex_pairs.csv')
            table_name = 'Forex Pairs'
            
        elif reference_data == 'crypto' and action == 'show_data':
            csv_file_path = os.path.join(folder, 'crypto_pairs.csv')
            table_name = 'Crypto Pairs'
            
        elif reference_data == 'etf_BSE' and action == 'show_data':
            csv_file_path = os.path.join(folder, 'etfs_BSE.csv')
            table_name = 'ETFs_BSE'
        
        elif reference_data == 'etf_NSE' and action == 'show_data':
            csv_file_path = os.path.join(folder, 'etfs_NSE.csv')
            table_name = 'ETFs_NSE'
            
        elif reference_data == 'indices_BSE' and action == 'show_data':
            csv_file_path = os.path.join(folder, 'indices_BSE.csv')
            table_name = 'Indices_BSE'
        
        elif reference_data == 'indices_NSE' and action == 'show_data':
            csv_file_path = os.path.join(folder, 'indices_NSE.csv')
            table_name = 'Indices_NSE'
        
        elif action == 'home_page':
            return redirect(url_for('index'))
        
        
        df = pd.read_csv(csv_file_path)
        # After processing the form, display the DataFrame as a table
        table_html = df.to_html(classes='table table-bordered table-striped', escape=False, index=False)

        flash(f"Updated reference data: {reference_data}")
        return render_template('referencedata.html', table=table_html, table_name=table_name)
    return render_template('referencedata.html', table=None, table_name=None)

@app.route("/add_stock_data_bse", methods=["GET", "POST"])
def stock_data_load_bse():
    folder = 'E:/Programming/Python/Stocks/Stock_Analyzer/reference_data'
        
    csv_file_path = os.path.join(folder, 'stocks_BSE.csv')
    data_files = os.listdir('E:/Programming/Python/Stocks/Stock_Analyzer/stock_timeseries/BSE')
        
    symbols = pd.read_csv(csv_file_path)
    symbols = symbols[symbols['mic_code'] == 'XBOM']
    symbols = symbols[symbols['deleted_date'].isnull()]
    symbols = symbols['symbol'].tolist()
    
    timeseries = []
    income = []
    balance = []
    for val in symbols:
        if os.path.exists('E:/Programming/Python/Stocks/Stock_Analyzer/stock_timeseries/BSE' + '/' + val + '.csv'):
            timeseries.append('Yes')
        else:
            timeseries.append('No')
        
        if os.path.exists('E:/Programming/Python/Stocks/Stock_Analyzer/stock_fundamentals/BSE' + '/' + val + '_income_statement' + '.csv'):
            income.append('Yes')
        else:
            income.append('No')
        
        if os.path.exists('E:/Programming/Python/Stocks/Stock_Analyzer/stock_fundamentals/BSE' + '/' + val + '_balance_sheet' + '.csv'):
            balance.append('Yes')
        else:
            balance.append('No')
    
    headers = ['Name', 'Time Series', 'Income Statement', 'Balance Sheet']

    # Creating a DataFrame
    stock_details = pd.DataFrame(list(zip(symbols, timeseries, income, balance)), columns=headers)
    
    if request.method == "POST":
        # Get the selected metadata value from the form
        action = request.form.get("action")
        
        if action == 'home_page':
            return redirect(url_for('index'))
        
        elif "update" in action: 
            symbol = action.split('_')[1]
            #symbol_call = symbol + '.BSE'
            try:
                data = c.get_price_timeseries(symbol, 'BSE', '2y')
                data.to_csv('E:/Programming/Python/Stocks/Stock_Analyzer/stock_timeseries/BSE' + '/' + symbol + '.csv', index=False)
                income_statement = c.income_statement_data(symbol, 'BSE')
                income_statement.to_csv('E:/Programming/Python/Stocks/Stock_Analyzer/stock_fundamentals/BSE' + '/' + symbol + '_income_statement' + '.csv', index=False)
                balance_sheet = c.balance_sheet_data(symbol, 'BSE')
                balance_sheet.to_csv('E:/Programming/Python/Stocks/Stock_Analyzer/stock_fundamentals/BSE' + '/' + symbol + '_balance_sheet' + '.csv', index=False)
                return redirect(url_for('stock_data_load_bse'))
            except Exception as e:
                return redirect(url_for('stock_data_load_bse'))
        
        elif "delete" in action: 
            symbol = action.split('_')[1]
            try:
                os.remove('E:/Programming/Python/Stocks/Stock_Analyzer/stock_timeseries/BSE' + '/' + symbol + '.csv')
                os.remove('E:/Programming/Python/Stocks/Stock_Analyzer/stock_fundamentals/BSE' + '/' + symbol + '_income_statement' + '.csv')
                os.remove('E:/Programming/Python/Stocks/Stock_Analyzer/stock_fundamentals/BSE' + '/' + symbol + '_balance_sheet' + '.csv')
                return redirect(url_for('stock_data_load_bse'))
            except Exception as e:
                return redirect(url_for('stock_data_load_bse'))
        
        elif 'add' in action:
            symbols_to_update = stock_details.loc[stock_details['Time Series'] == 'No', 'Name'].tolist()
            for val in symbols_to_update:
                try:
                    data = c.get_price_timeseries(val, 'BSE', '2y')
                    data.to_csv('E:/Programming/Python/Stocks/Stock_Analyzer/stock_timeseries/BSE' + '/' + val + '.csv', index=False)
                    income_statement = c.income_statement_data(val, 'BSE')
                    income_statement.to_csv('E:/Programming/Python/Stocks/Stock_Analyzer/stock_fundamentals/BSE' + '/' + val + '_income_statement' + '.csv', index=False)
                    balance_sheet = c.balance_sheet_data(val, 'BSE')
                    balance_sheet.to_csv('E:/Programming/Python/Stocks/Stock_Analyzer/stock_fundamentals/BSE' + '/' + val + '_balance_sheet' + '.csv', index=False)
                except Exception as e:
                    continue
            return redirect(url_for('stock_data_load_bse'))
                
        elif 'remove' in action:
            symbols_to_remove = stock_details.loc[stock_details['Time Series'] == 'Yes', 'Name'].tolist()
            for val in symbols_to_remove:
                try:
                    os.remove('E:/Programming/Python/Stocks/Stock_Analyzer/stock_timeseries/BSE' + '/' + val + '.csv')
                    os.remove('E:/Programming/Python/Stocks/Stock_Analyzer/stock_fundamentals/BSE' + '/' + val + '_income_statement' + '.csv')
                    os.remove('E:/Programming/Python/Stocks/Stock_Analyzer/stock_fundamentals/BSE' + '/' + val + '_balance_sheet' + '.csv')
                except Exception as e:
                    continue
            return redirect(url_for('stock_data_load_bse'))
        
    return render_template('addstock.html', data_stocks=stock_details, title='Stocks_BSE')

@app.route("/add_stock_data_nse", methods=["GET", "POST"])
def stock_data_load_nse():
    folder = 'E:/Programming/Python/Stocks/Stock_Analyzer/reference_data'
        
    csv_file_path = os.path.join(folder, 'stocks_NSE.csv')
    #data_files = os.listdir('E:/Programming/Python/Stocks/Stock_Analyzer/stock_timeseries/NSE')
        
    symbols = pd.read_csv(csv_file_path)
    symbols = symbols[symbols['deleted_date'].isnull()]
    symbols = symbols['symbol'].tolist()
    
    timeseries = []
    income = []
    balance = []
    for val in symbols:
        if os.path.exists('E:/Programming/Python/Stocks/Stock_Analyzer/stock_timeseries/NSE' + '/' + val + '.csv'):
            timeseries.append('Yes')
        else:
            timeseries.append('No')
        
        if os.path.exists('E:/Programming/Python/Stocks/Stock_Analyzer/stock_fundamentals/NSE' + '/' + val + '_income_statement' + '.csv'):
            income.append('Yes')
        else:
            income.append('No')
        
        if os.path.exists('E:/Programming/Python/Stocks/Stock_Analyzer/stock_fundamentals/NSE' + '/' + val + '_balance_sheet' + '.csv'):
            balance.append('Yes')
        else:
            balance.append('No')
    
    headers = ['Name', 'Time Series', 'Income Statement', 'Balance Sheet']

    # Creating a DataFrame
    stock_details = pd.DataFrame(list(zip(symbols, timeseries, income, balance)), columns=headers)
    
    if request.method == "POST":
        # Get the selected metadata value from the form
        action = request.form.get("action")
        
        if action == 'home_page':
            return redirect(url_for('index'))
        
        elif "update" in action:  
            symbol = action.split('_')[1]
            #symbol_call = symbol + '.NSE'
            try:
                data = c.get_price_timeseries(symbol, 'NSE', '2y')
                data.to_csv('E:/Programming/Python/Stocks/Stock_Analyzer/stock_timeseries/NSE' + '/' + symbol + '.csv', index=False)
                income_statement = c.income_statement_data(symbol, 'NSE')
                income_statement.to_csv('E:/Programming/Python/Stocks/Stock_Analyzer/stock_fundamentals/NSE' + '/' + symbol + '_income_statement' + '.csv', index=False)
                balance_sheet = c.balance_sheet_data(symbol, 'NSE')
                balance_sheet.to_csv('E:/Programming/Python/Stocks/Stock_Analyzer/stock_fundamentals/NSE' + '/' + symbol + '_balance_sheet' + '.csv', index=False)
                return redirect(url_for('stock_data_load_nse'))
            except Exception as e:
                return redirect(url_for('stock_data_load_nse'))
            
        elif "delete" in action: 
            symbol = action.split('_')[1]
            try:
                os.remove('E:/Programming/Python/Stocks/Stock_Analyzer/stock_timeseries/NSE' + '/' + symbol + '.csv')
                os.remove('E:/Programming/Python/Stocks/Stock_Analyzer/stock_fundamentals/NSE' + '/' + symbol + '_income_statement' + '.csv')
                os.remove('E:/Programming/Python/Stocks/Stock_Analyzer/stock_fundamentals/NSE' + '/' + symbol + '_balance_sheet' + '.csv')
                return redirect(url_for('stock_data_load_nse'))
            except Exception as e:
                return redirect(url_for('stock_data_load_nse'))
        
        elif 'add' in action:
            symbols_to_update = stock_details.loc[stock_details['Time Series'] == 'No', 'Name'].tolist()
            for val in symbols_to_update:
                try:
                    data = c.get_price_timeseries(val, 'NSE', '2y')
                    data.to_csv('E:/Programming/Python/Stocks/Stock_Analyzer/stock_timeseries/NSE' + '/' + val + '.csv', index=False)
                    income_statement = c.income_statement_data(val, 'NSE')
                    income_statement.to_csv('E:/Programming/Python/Stocks/Stock_Analyzer/stock_fundamentals/NSE' + '/' + val + '_income_statement' + '.csv', index=False)
                    balance_sheet = c.balance_sheet_data(val, 'NSE')
                    balance_sheet.to_csv('E:/Programming/Python/Stocks/Stock_Analyzer/stock_fundamentals/NSE' + '/' + val + '_balance_sheet' + '.csv', index=False)
                except Exception as e:
                    continue
            return redirect(url_for('stock_data_load_nse'))
        
        elif 'remove' in action:
            symbols_to_remove = stock_details.loc[stock_details['Time Series'] == 'Yes', 'Name'].tolist()
            for val in symbols_to_remove:
                try:
                    os.remove('E:/Programming/Python/Stocks/Stock_Analyzer/stock_timeseries/NSE' + '/' + val + '.csv')
                    os.remove('E:/Programming/Python/Stocks/Stock_Analyzer/stock_fundamentals/NSE' + '/' + val + '_income_statement' + '.csv')
                    os.remove('E:/Programming/Python/Stocks/Stock_Analyzer/stock_fundamentals/NSE' + '/' + val + '_balance_sheet' + '.csv')
                except Exception as e:
                    continue
            return redirect(url_for('stock_data_load_nse'))
            
    return render_template('addstock.html', data_stocks=stock_details, title='Stocks_NSE')
        
    
@app.route("/analyse_stock_data_bse", methods=["GET", "POST"])
def stock_data_update_bse():
    
    folder = 'E:/Programming/Python/Stocks/Stock_Analyzer/basic_analytics'
    file = 'bse_stock_data_summary.csv'
    
    path = folder + '/' + file
    
    if os.path.exists(path):
        data_quality_summary = pd.read_csv(path)
        if data_quality_summary.empty:
            data_quality_summary = pd.DataFrame(columns=['symbol', 'min_date', 'max_date', 'missing_dates_per', 'growth_per_30', 'avg_vol_30', 'growth_per_7', 'avg_vol_7'])
            data_quality_summary.loc[0] = [pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA]
    else:
        data_quality_summary = pd.DataFrame(columns=['symbol', 'min_date', 'max_date', 'missing_dates_per', 'growth_per_30', 'avg_vol_30', 'growth_per_7', 'avg_vol_7'])
        data_quality_summary.loc[0] = [pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA]
    
    if request.method == "POST":
        # Get the selected metadata value from the form
        action = request.form.get("action")
        
        if action == 'home_page':
            return redirect(url_for('index'))
        elif action == 'generate_summary':
            summary = dq.stock_summary('E:/Programming/Python/Stocks/Stock_Analyzer/stock_timeseries', 'BSE')
            summary.to_csv(path)
            return redirect(url_for('stock_data_update_bse'))
        elif 'update' in action:
            symbol = action.split('_')[1]
            data = c.get_price_timeseries(symbol, 'BSE', '1mo')
            u.update_csv(data, 'E:/Programming/Python/Stocks/Stock_Analyzer/stock_timeseries/BSE' + '/' + symbol + '.csv', 'Date')
            income_statement = c.income_statement_data(symbol, 'BSE')
            u.update_csv(income_statement, 'E:/Programming/Python/Stocks/Stock_Analyzer/stock_fundamentals/BSE' + '/' + symbol + '_income_statement' + '.csv', 'Date')
            balance_sheet = c.balance_sheet_data(symbol, 'BSE')
            u.update_csv(balance_sheet, 'E:/Programming/Python/Stocks/Stock_Analyzer/stock_fundamentals/BSE' + '/' + symbol + '_balance_sheet' + '.csv', 'Date')
            summary = dq.stock_summary('E:/Programming/Python/Stocks/Stock_Analyzer/stock_timeseries', 'BSE')
            summary.to_csv(path)
            return redirect(url_for('stock_data_update_bse'))
        elif 'fill' in action:
            for val in data_quality_summary['symbol']:
                data = c.get_price_timeseries(val, 'BSE', '1mo')
                u.update_csv(data, 'E:/Programming/Python/Stocks/Stock_Analyzer/stock_timeseries/BSE' + '/' + val + '.csv', 'Date')
                income_statement = c.income_statement_data(val, 'BSE')
                u.update_csv(income_statement, 'E:/Programming/Python/Stocks/Stock_Analyzer/stock_fundamentals/BSE' + '/' + val + '_income_statement' + '.csv', 'Date')
                balance_sheet = c.balance_sheet_data(val, 'BSE')
                u.update_csv(balance_sheet, 'E:/Programming/Python/Stocks/Stock_Analyzer/stock_fundamentals/BSE' + '/' + val + '_balance_sheet' + '.csv', 'Date')
            summary = dq.stock_summary('E:/Programming/Python/Stocks/Stock_Analyzer/stock_timeseries', 'BSE')
            summary.to_csv(path)
            return redirect(url_for('stock_data_update_bse'))
            
    return render_template('summarystock.html', data = data_quality_summary, title='Stocks_BSE')
    
@app.route("/analyse_stock_data_nse", methods=["GET", "POST"])
def stock_data_update_nse():
    
    folder = 'E:/Programming/Python/Stocks/Stock_Analyzer/basic_analytics'
    file = 'nse_stock_data_summary.csv'
    
    path = folder + '/' + file
    
    if os.path.exists(path):
        data_quality_summary = pd.read_csv(path)
        if data_quality_summary.empty:
            data_quality_summary = pd.DataFrame(columns=['symbol', 'min_date', 'max_date', 'missing_dates_per', 'growth_per_30', 'avg_vol_30', 'growth_per_7', 'avg_vol_7'])
            data_quality_summary.loc[0] = [pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA]
    else:
        data_quality_summary = pd.DataFrame(columns=['symbol', 'min_date', 'max_date', 'missing_dates_per', 'growth_per_30', 'avg_vol_30', 'growth_per_7', 'avg_vol_7'])
        data_quality_summary.loc[0] = [pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA]
    
    if request.method == "POST":
        # Get the selected metadata value from the form
        action = request.form.get("action")
        
        if action == 'home_page':
            return redirect(url_for('index'))
        elif action == 'generate_summary':
            summary = dq.stock_summary('E:/Programming/Python/Stocks/Stock_Analyzer/stock_timeseries', 'NSE')
            summary.to_csv(path)
            return redirect(url_for('stock_data_update_nse'))
        elif 'update' in action:
            symbol = action.split('_')[1]
            data = c.get_price_timeseries(symbol, 'NSE', '1mo')
            u.update_csv(data, 'E:/Programming/Python/Stocks/Stock_Analyzer/stock_timeseries/NSE' + '/' + symbol + '.csv', 'Date')
            income_statement = c.income_statement_data(symbol, 'NSE')
            u.update_csv(income_statement, 'E:/Programming/Python/Stocks/Stock_Analyzer/stock_fundamentals/NSE' + '/' + symbol + '_income_statement' + '.csv', 'Date')
            balance_sheet = c.balance_sheet_data(symbol, 'NSE')
            u.update_csv(balance_sheet, 'E:/Programming/Python/Stocks/Stock_Analyzer/stock_fundamentals/NSE' + '/' + symbol + '_balance_sheet' + '.csv', 'Date')
            summary = dq.stock_summary('E:/Programming/Python/Stocks/Stock_Analyzer/stock_timeseries', 'NSE')
            summary.to_csv(path)
            return redirect(url_for('stock_data_update_nse'))
        elif 'fill' in action:
            for val in data_quality_summary['symbol']:
                data = c.get_price_timeseries(val, 'NSE', '1mo')
                u.update_csv(data, 'E:/Programming/Python/Stocks/Stock_Analyzer/stock_timeseries/NSE' + '/' + val + '.csv', 'Date')
                income_statement = c.income_statement_data(val, 'NSE')
                u.update_csv(income_statement, 'E:/Programming/Python/Stocks/Stock_Analyzer/stock_fundamentals/NSE' + '/' + val + '_income_statement' + '.csv', 'Date')
                balance_sheet = c.balance_sheet_data(val, 'NSE')
                u.update_csv(balance_sheet, 'E:/Programming/Python/Stocks/Stock_Analyzer/stock_fundamentals/NSE' + '/' + val + '_balance_sheet' + '.csv', 'Date')
            summary = dq.stock_summary('E:/Programming/Python/Stocks/Stock_Analyzer/stock_timeseries', 'NSE')
            summary.to_csv(path)
            return redirect(url_for('stock_data_update_nse'))
            
            
    return render_template('summarystock.html', data = data_quality_summary, title='Stocks_NSE')
    

if __name__ == "__main__":
    app.run(debug=True)