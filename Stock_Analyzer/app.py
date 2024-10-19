# -*- coding: utf-8 -*-
"""
Created on Sun Sep 24 10:25:51 2023

@author: aksha
"""

from flask import request, Flask, render_template, url_for, flash, redirect, send_from_directory
import metadata_handler as m
import reference_data_handeler as r
import core_stock_data as c
import stock_data_basic_analytics as dq
import pandas as pd
import utility as u
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import csv
import datetime 

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
        elif action == "manage_portfolio":
            return redirect(url_for('manage_portfolio'))
        elif stock_data_to_change == 'stock_BSE' and action == 'add_stock_data':
            return redirect(url_for('stock_data_load_bse'))
        elif stock_data_to_change == 'stock_NSE' and action == 'add_stock_data':
            return redirect(url_for('stock_data_load_nse'))
        elif stock_data_to_change == 'stock_BSE' and action == 'update_stock_data':
            return redirect(url_for('stock_data_update_bse'))
        elif stock_data_to_change == 'stock_NSE' and action == 'update_stock_data':
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
    symbols['added_date'] = pd.to_datetime(symbols['added_date'],format='%Y-%m-%d')
    # Sort DataFrame based on 'added_date' column in descending order
    symbols = symbols.sort_values(by='added_date', ascending=False)
    symbols = symbols[symbols['mic_code'] == 'XBOM']
    symbols = symbols[symbols['deleted_date'].isnull()]
    symbols = symbols['symbol'].tolist()
    
    timeseries = []
    income = []
    balance = []
    stock_summ = []
    valuation = []
    dividend_infor = []
    key_ratios = []
    growth_metrics = []
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
        
        if os.path.exists('E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/BSE' + '/' + val + '_stock_summary' + '.csv'):
            stock_summ.append('Yes')
        else:
            stock_summ.append('No')
            
        if os.path.exists('E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/BSE' + '/' + val + '_valuation' + '.csv'):
            valuation.append('Yes')
        else:
            valuation.append('No')
            
        if os.path.exists('E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/BSE' + '/' + val + '_dividend' + '.csv'):
            dividend_infor.append('Yes')
        else:
            dividend_infor.append('No')
            
        if os.path.exists('E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/BSE' + '/' + val + '_key_ratio' + '.csv'):
            key_ratios.append('Yes')
        else:
            key_ratios.append('No')
            
        if os.path.exists('E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/BSE' + '/' + val + '_growth_metrics' + '.csv'):
            growth_metrics.append('Yes')
        else:
            growth_metrics.append('No')
    
    headers = ['Name', 'Time Series', 'Income Statement', 'Balance Sheet', 'Stock Summary', 'Valuation', 'Dividend Info', 'key Ratios', 'Growth Metrics']

    # Creating a DataFrame
    stock_details = pd.DataFrame(list(zip(symbols, timeseries, income, balance, stock_summ, valuation, dividend_infor, key_ratios, growth_metrics)), columns=headers)
    
    if request.method == "POST":
        # Get the selected metadata value from the form
        action = request.form.get("action")
        
        if action == 'home_page':
            return redirect(url_for('index'))
        
        elif "update" in action: 
            symbol = action.split('_')[1]
            #symbol_call = symbol + '.BSE'
            #try:
            data = c.get_price_timeseries(symbol, 'BSE', 'max')
            data.to_csv('E:/Programming/Python/Stocks/Stock_Analyzer/stock_timeseries/BSE' + '/' + symbol + '.csv', index=False)
            income_statement = c.income_statement_data(symbol, 'BSE')
            income_statement.to_csv('E:/Programming/Python/Stocks/Stock_Analyzer/stock_fundamentals/BSE' + '/' + symbol + '_income_statement' + '.csv', index=False)
            balance_sheet = c.balance_sheet_data(symbol, 'BSE')
            balance_sheet.to_csv('E:/Programming/Python/Stocks/Stock_Analyzer/stock_fundamentals/BSE' + '/' + symbol + '_balance_sheet' + '.csv', index=False)
            stock_summary, valuation_info, dividend_inf, keys, growth = c.get_company_description_summary(symbol, 'BSE')
            stock_summary.to_csv('E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/BSE' + '/' + symbol + '_stock_summary' + '.csv', index=False)
            valuation_info.to_csv('E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/BSE' + '/' + symbol + '_valuation' + '.csv', index=False)
            dividend_inf.to_csv('E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/BSE' + '/' + symbol + '_dividend' + '.csv', index=False)
            keys.to_csv('E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/BSE' + '/' + symbol + '_key_ratio' + '.csv', index=False)
            growth.to_csv('E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/BSE' + '/' + symbol + '_growth_metrics' + '.csv', index=False)
            return redirect(url_for('stock_data_load_bse'))
            #except Exception as e:
                #with open('error.txt', 'w') as file:
                    #file.write(str(e))
                #return redirect(url_for('stock_data_load_bse'))
        
        elif "delete" in action: 
            symbol = action.split('_')[1]
            try:
                os.remove('E:/Programming/Python/Stocks/Stock_Analyzer/stock_timeseries/BSE' + '/' + symbol + '.csv')
                os.remove('E:/Programming/Python/Stocks/Stock_Analyzer/stock_fundamentals/BSE' + '/' + symbol + '_income_statement' + '.csv')
                os.remove('E:/Programming/Python/Stocks/Stock_Analyzer/stock_fundamentals/BSE' + '/' + symbol + '_balance_sheet' + '.csv')
                os.remove('E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/BSE' + '/' + symbol + '_stock_summary' + '.csv')
                os.remove('E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/BSE' + '/' + symbol + '_valuation' + '.csv')
                os.remove('E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/BSE' + '/' + symbol + '_dividend' + '.csv')
                os.remove('E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/BSE' + '/' + symbol + '_key_ratio' + '.csv')
                os.remove('E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/BSE' + '/' + symbol + '_growth_metrics' + '.csv')
                return redirect(url_for('stock_data_load_bse'))
            except Exception as e:
                return redirect(url_for('stock_data_load_bse'))
        
        elif 'add' in action:
            symbols_to_update = stock_details.loc[stock_details['Time Series'] == 'No', 'Name'].tolist()
            for val in symbols_to_update:
                try:
                    data = c.get_price_timeseries(val, 'BSE', 'max')
                    data.to_csv('E:/Programming/Python/Stocks/Stock_Analyzer/stock_timeseries/BSE' + '/' + val + '.csv', index=False)
                    income_statement = c.income_statement_data(val, 'BSE')
                    income_statement.to_csv('E:/Programming/Python/Stocks/Stock_Analyzer/stock_fundamentals/BSE' + '/' + val + '_income_statement' + '.csv', index=False)
                    balance_sheet = c.balance_sheet_data(val, 'BSE')
                    balance_sheet.to_csv('E:/Programming/Python/Stocks/Stock_Analyzer/stock_fundamentals/BSE' + '/' + val + '_balance_sheet' + '.csv', index=False)
                    stock_summary, valuation_info, dividend_inf, keys, growth = c.get_company_description_summary(val, 'BSE')
                    stock_summary.to_csv('E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/BSE' + '/' + val + '_stock_summary' + '.csv', index=False)
                    valuation_info.to_csv('E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/BSE' + '/' + val + '_valuation' + '.csv', index=False)
                    dividend_inf.to_csv('E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/BSE' + '/' + val + '_dividend' + '.csv', index=False)
                    keys.to_csv('E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/BSE' + '/' + val + '_key_ratio' + '.csv', index=False)
                    growth.to_csv('E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/BSE' + '/' + val + '_growth_metrics' + '.csv', index=False)
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
                    os.remove('E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/BSE' + '/' + val + '_stock_summary' + '.csv')
                    os.remove('E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/BSE' + '/' + val + '_valuation' + '.csv')
                    os.remove('E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/BSE' + '/' + val + '_dividend' + '.csv')
                    os.remove('E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/BSE' + '/' + val + '_key_ratio' + '.csv')
                    os.remove('E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/BSE' + '/' + val + '_growth_metrics' + '.csv')
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
    symbols['added_date'] = pd.to_datetime(symbols['added_date'],format='%Y-%m-%d')
    # Sort DataFrame based on 'added_date' column in descending order
    symbols = symbols.sort_values(by='added_date', ascending=False)
    symbols = symbols[symbols['deleted_date'].isnull()]
    symbols = symbols['symbol'].tolist()
    
    
    timeseries = []
    income = []
    balance = []
    stock_summ = []
    valuation = []
    dividend_infor = []
    key_ratios = []
    growth_metrics = []
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
            
        if os.path.exists('E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/NSE' + '/' + val + '_stock_summary' + '.csv'):
            stock_summ.append('Yes')
        else:
            stock_summ.append('No')
            
        if os.path.exists('E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/NSE' + '/' + val + '_valuation' + '.csv'):
            valuation.append('Yes')
        else:
            valuation.append('No')
            
        if os.path.exists('E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/NSE' + '/' + val + '_dividend' + '.csv'):
            dividend_infor.append('Yes')
        else:
            dividend_infor.append('No')
            
        if os.path.exists('E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/NSE' + '/' + val + '_key_ratio' + '.csv'):
            key_ratios.append('Yes')
        else:
            key_ratios.append('No')
            
        if os.path.exists('E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/NSE' + '/' + val + '_growth_metrics' + '.csv'):
            growth_metrics.append('Yes')
        else:
            growth_metrics.append('No')
    
    headers = ['Name', 'Time Series', 'Income Statement', 'Balance Sheet', 'Stock Summary', 'Valuation', 'Dividend Info', 'Key Ratios', 'Growth Metrics']

    # Creating a DataFrame
    stock_details = pd.DataFrame(list(zip(symbols, timeseries, income, balance, stock_summ, valuation, dividend_infor, key_ratios, growth_metrics)), columns=headers)
    
    if request.method == "POST":
        # Get the selected metadata value from the form
        action = request.form.get("action")
        
        if action == 'home_page':
            return redirect(url_for('index'))
        
        elif "update" in action:  
            symbol = action.split('_')[1]
            #symbol_call = symbol + '.NSE'
            try:
                data = c.get_price_timeseries(symbol, 'NSE', 'max')
                data.to_csv('E:/Programming/Python/Stocks/Stock_Analyzer/stock_timeseries/NSE' + '/' + symbol + '.csv', index=False)
                income_statement = c.income_statement_data(symbol, 'NSE')
                income_statement.to_csv('E:/Programming/Python/Stocks/Stock_Analyzer/stock_fundamentals/NSE' + '/' + symbol + '_income_statement' + '.csv', index=False)
                balance_sheet = c.balance_sheet_data(symbol, 'NSE')
                balance_sheet.to_csv('E:/Programming/Python/Stocks/Stock_Analyzer/stock_fundamentals/NSE' + '/' + symbol + '_balance_sheet' + '.csv', index=False)
                stock_summary, valuation_info, dividend_inf, keys, growth = c.get_company_description_summary(symbol, 'NSE')
                stock_summary.to_csv('E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/NSE' + '/' + symbol + '_stock_summary' + '.csv', index=False)
                valuation_info.to_csv('E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/NSE' + '/' + symbol + '_valuation' + '.csv', index=False)
                dividend_inf.to_csv('E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/NSE' + '/' + symbol + '_dividend' + '.csv', index=False)
                keys.to_csv('E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/NSE' + '/' + symbol + '_key_ratio' + '.csv', index=False)
                growth.to_csv('E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/NSE' + '/' + symbol + '_growth_metrics' + '.csv', index=False)
                return redirect(url_for('stock_data_load_nse'))
            except Exception as e:
                return redirect(url_for('stock_data_load_nse'))
            
        elif "delete" in action: 
            symbol = action.split('_')[1]
            try:
                os.remove('E:/Programming/Python/Stocks/Stock_Analyzer/stock_timeseries/NSE' + '/' + symbol + '.csv')
                os.remove('E:/Programming/Python/Stocks/Stock_Analyzer/stock_fundamentals/NSE' + '/' + symbol + '_income_statement' + '.csv')
                os.remove('E:/Programming/Python/Stocks/Stock_Analyzer/stock_fundamentals/NSE' + '/' + symbol + '_balance_sheet' + '.csv')
                os.remove('E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/NSE' + '/' + symbol + '_stock_summary' + '.csv')
                os.remove('E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/NSE' + '/' + symbol + '_valuation' + '.csv')
                os.remove('E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/NSE' + '/' + symbol + '_dividend' + '.csv')
                os.remove('E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/NSE' + '/' + symbol + '_key_ratio' + '.csv')
                os.remove('E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/NSE' + '/' + symbol + '_growth_metrics' + '.csv')
                return redirect(url_for('stock_data_load_nse'))
            except Exception as e:
                return redirect(url_for('stock_data_load_nse'))
        
        elif 'add' in action:
            symbols_to_update = stock_details.loc[stock_details['Time Series'] == 'No', 'Name'].tolist()
            for val in symbols_to_update:
                try:
                    data = c.get_price_timeseries(val, 'NSE', 'max')
                    data.to_csv('E:/Programming/Python/Stocks/Stock_Analyzer/stock_timeseries/NSE' + '/' + val + '.csv', index=False)
                    income_statement = c.income_statement_data(val, 'NSE')
                    income_statement.to_csv('E:/Programming/Python/Stocks/Stock_Analyzer/stock_fundamentals/NSE' + '/' + val + '_income_statement' + '.csv', index=False)
                    balance_sheet = c.balance_sheet_data(val, 'NSE')
                    balance_sheet.to_csv('E:/Programming/Python/Stocks/Stock_Analyzer/stock_fundamentals/NSE' + '/' + val + '_balance_sheet' + '.csv', index=False)
                    stock_summary, valuation_info, dividend_inf, keys, growth = c.get_company_description_summary(val, 'NSE')
                    stock_summary.to_csv('E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/NSE' + '/' + val + '_stock_summary' + '.csv', index=False)
                    valuation_info.to_csv('E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/NSE' + '/' + val + '_valuation' + '.csv', index=False)
                    dividend_inf.to_csv('E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/NSE' + '/' + val + '_dividend' + '.csv', index=False)
                    keys.to_csv('E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/NSE' + '/' + val + '_key_ratio' + '.csv', index=False)
                    growth.to_csv('E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/NSE' + '/' + val + '_growth_metrics' + '.csv', index=False)
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
                    os.remove('E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/NSE' + '/' + val + '_stock_summary' + '.csv')
                    os.remove('E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/NSE' + '/' + val + '_valuation' + '.csv')
                    os.remove('E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/NSE' + '/' + val + '_dividend' + '.csv')
                    os.remove('E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/NSE' + '/' + val + '_key_ratio' + '.csv')
                    os.remove('E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/NSE' + '/' + val + '_growth_metrics' + '.csv')
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
        # Convert 'max date' column to datetime
        data_quality_summary['max_date'] = pd.to_datetime(data_quality_summary['max_date'])
        # Sorting by 'max date' column in descending order
        data_quality_summary = data_quality_summary.sort_values(by='max_date', ascending=False)
        if data_quality_summary.empty:
            data_quality_summary = pd.DataFrame(columns=['symbol', 'min_date', 'max_date', 'missing_dates_per', 'latest_closing_price', 'growth_per_30', 'avg_vol_30', 'growth_per_7', 'avg_vol_7', 'latest_signal','latest_trend','signal_start_date','signal_duration', 'trend_start_date', 'trend_duration'])
            data_quality_summary.loc[0] = [pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA]
    else:
        data_quality_summary = pd.DataFrame(columns=['symbol', 'min_date', 'max_date', 'missing_dates_per', 'latest_closing_price', 'growth_per_30', 'avg_vol_30', 'growth_per_7', 'avg_vol_7', 'latest_signal','latest_trend','signal_start_date','signal_duration', 'trend_start_date', 'trend_duration'])
        data_quality_summary.loc[0] = [pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA]
    
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
            try:
                data = c.get_price_timeseries(symbol, 'BSE', '1mo')
                u.update_csv(data, 'E:/Programming/Python/Stocks/Stock_Analyzer/stock_timeseries/BSE' + '/' + symbol + '.csv', 'Date')
                income_statement = c.income_statement_data(symbol, 'BSE')
                u.update_csv(income_statement, 'E:/Programming/Python/Stocks/Stock_Analyzer/stock_fundamentals/BSE' + '/' + symbol + '_income_statement' + '.csv', 'Date')
                balance_sheet = c.balance_sheet_data(symbol, 'BSE')
                u.update_csv(balance_sheet, 'E:/Programming/Python/Stocks/Stock_Analyzer/stock_fundamentals/BSE' + '/' + symbol + '_balance_sheet' + '.csv', 'Date')
                stock_summary, valuation_info, dividend_inf, keys, growth = c.get_company_description_summary(symbol, 'BSE')
                stock_summary.to_csv('E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/BSE' + '/' + symbol + '_stock_summary' + '.csv', index=False)
                u.update_csv(valuation_info, 'E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/BSE' + '/' + symbol + '_valuation' + '.csv', 'Date')
                u.update_csv(dividend_inf, 'E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/BSE' + '/' + symbol + '_dividend' + '.csv', 'lastDividendDate')
                u.update_csv(keys, 'E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/BSE' + '/' + symbol + '_key_ratio' + '.csv', 'Date')
                u.update_csv(growth, 'E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/BSE' + '/' + symbol + '_growth_metrics' + '.csv', 'Date')
                summary = dq.stock_summary('E:/Programming/Python/Stocks/Stock_Analyzer/stock_timeseries', 'BSE')
                summary.to_csv(path)
                return redirect(url_for('stock_data_update_bse'))
            except Exception as e:
                return redirect(url_for('stock_data_update_bse'))
        elif 'fill' in action:
            for val in data_quality_summary['symbol']:
                try:
                    data = c.get_price_timeseries(val, 'BSE', '1mo')
                    u.update_csv(data, 'E:/Programming/Python/Stocks/Stock_Analyzer/stock_timeseries/BSE' + '/' + val + '.csv', 'Date')
                    income_statement = c.income_statement_data(val, 'BSE')
                    u.update_csv(income_statement, 'E:/Programming/Python/Stocks/Stock_Analyzer/stock_fundamentals/BSE' + '/' + val + '_income_statement' + '.csv', 'Date')
                    balance_sheet = c.balance_sheet_data(val, 'BSE')
                    u.update_csv(balance_sheet, 'E:/Programming/Python/Stocks/Stock_Analyzer/stock_fundamentals/BSE' + '/' + val + '_balance_sheet' + '.csv', 'Date')
                    stock_summary, valuation_info, dividend_inf, keys, growth = c.get_company_description_summary(val, 'BSE')
                    stock_summary.to_csv('E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/BSE' + '/' + val + '_stock_summary' + '.csv', index=False)
                    u.update_csv(valuation_info, 'E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/BSE' + '/' + val + '_valuation' + '.csv', 'Date')
                    u.update_csv(dividend_inf, 'E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/BSE' + '/' + val + '_dividend' + '.csv', 'lastDividendDate')
                    u.update_csv(keys, 'E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/BSE' + '/' + val + '_key_ratio' + '.csv', 'Date')
                    u.update_csv(growth, 'E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/BSE' + '/' + val + '_growth_metrics' + '.csv', 'Date')
                except Exception as e:
                    continue
            summary = dq.stock_summary('E:/Programming/Python/Stocks/Stock_Analyzer/stock_timeseries', 'BSE')
            summary.to_csv(path)
            return redirect(url_for('stock_data_update_bse'))
        elif 'charts' in action:
            return redirect(url_for('charts_view_bse'))
            
    return render_template('summarystock.html', data = data_quality_summary, title='Stocks_BSE')
    
@app.route("/analyse_stock_data_nse", methods=["GET", "POST"])
def stock_data_update_nse():
    
    folder = 'E:/Programming/Python/Stocks/Stock_Analyzer/basic_analytics'
    file = 'nse_stock_data_summary.csv'
    
    path = folder + '/' + file
    
    if os.path.exists(path):
        data_quality_summary = pd.read_csv(path)
        # Convert 'max date' column to datetime
        data_quality_summary['max_date'] = pd.to_datetime(data_quality_summary['max_date'])
        # Sorting by 'max date' column in descending order
        data_quality_summary = data_quality_summary.sort_values(by='max_date', ascending=False)
        if data_quality_summary.empty:
            data_quality_summary = pd.DataFrame(columns=['symbol', 'min_date', 'max_date', 'missing_dates_per', 'latest_closing_price', 'growth_per_30', 'avg_vol_30', 'growth_per_7', 'avg_vol_7', 'latest_signal','latest_trend','signal_start_date','signal_duration', 'trend_start_date', 'trend_duration'])
            data_quality_summary.loc[0] = [pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA]
    else:
        data_quality_summary = pd.DataFrame(columns=['symbol', 'min_date', 'max_date', 'missing_dates_per', 'latest_closing_price', 'growth_per_30', 'avg_vol_30', 'growth_per_7', 'avg_vol_7', 'latest_signal','latest_trend','signal_start_date','signal_duration', 'trend_start_date', 'trend_duration'])
        data_quality_summary.loc[0] = [pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA]
    
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
            try:
                data = c.get_price_timeseries(symbol, 'NSE', '1mo')
                u.update_csv(data, 'E:/Programming/Python/Stocks/Stock_Analyzer/stock_timeseries/NSE' + '/' + symbol + '.csv', 'Date')
                income_statement = c.income_statement_data(symbol, 'NSE')
                u.update_csv(income_statement, 'E:/Programming/Python/Stocks/Stock_Analyzer/stock_fundamentals/NSE' + '/' + symbol + '_income_statement' + '.csv', 'Date')
                balance_sheet = c.balance_sheet_data(symbol, 'NSE')
                u.update_csv(balance_sheet, 'E:/Programming/Python/Stocks/Stock_Analyzer/stock_fundamentals/NSE' + '/' + symbol + '_balance_sheet' + '.csv', 'Date')
                stock_summary, valuation_info, dividend_inf, keys, growth = c.get_company_description_summary(symbol, 'NSE')
                stock_summary.to_csv('E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/NSE' + '/' + symbol + '_stock_summary' + '.csv', index=False)
                u.update_csv(valuation_info, 'E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/NSE' + '/' + symbol + '_valuation' + '.csv', 'Date')
                u.update_csv(dividend_inf, 'E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/NSE' + '/' + symbol + '_dividend' + '.csv', 'lastDividendDate')
                u.update_csv(keys, 'E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/NSE' + '/' + symbol + '_key_ratio' + '.csv', 'Date')
                u.update_csv(growth, 'E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/NSE' + '/' + symbol + '_growth_metrics' + '.csv', 'Date')
                summary = dq.stock_summary('E:/Programming/Python/Stocks/Stock_Analyzer/stock_timeseries', 'NSE')
                summary.to_csv(path)
                return redirect(url_for('stock_data_update_nse'))
            except Exception as e:
                return redirect(url_for('stock_data_update_nse'))
        elif 'fill' in action:
            for val in data_quality_summary['symbol']:
                try:
                    data = c.get_price_timeseries(val, 'NSE', '1mo')
                    u.update_csv(data, 'E:/Programming/Python/Stocks/Stock_Analyzer/stock_timeseries/NSE' + '/' + val + '.csv', 'Date')
                    income_statement = c.income_statement_data(val, 'NSE')
                    u.update_csv(income_statement, 'E:/Programming/Python/Stocks/Stock_Analyzer/stock_fundamentals/NSE' + '/' + val + '_income_statement' + '.csv', 'Date')
                    balance_sheet = c.balance_sheet_data(val, 'NSE')
                    u.update_csv(balance_sheet, 'E:/Programming/Python/Stocks/Stock_Analyzer/stock_fundamentals/NSE' + '/' + val + '_balance_sheet' + '.csv', 'Date')
                    stock_summary, valuation_info, dividend_inf, keys, growth = c.get_company_description_summary(val, 'NSE')
                    stock_summary.to_csv('E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/NSE' + '/' + val + '_stock_summary' + '.csv', index=False)
                    u.update_csv(valuation_info, 'E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/NSE' + '/' + val + '_valuation' + '.csv', 'Date')
                    u.update_csv(dividend_inf, 'E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/NSE' + '/' + val + '_dividend' + '.csv', 'lastDividendDate')
                    u.update_csv(keys, 'E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/NSE' + '/' + val + '_key_ratio' + '.csv', 'Date')
                    u.update_csv(growth, 'E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/NSE' + '/' + val + '_growth_metrics' + '.csv', 'Date')
                except Exception as e:
                    continue
            summary = dq.stock_summary('E:/Programming/Python/Stocks/Stock_Analyzer/stock_timeseries', 'NSE')
            summary.to_csv(path)
            return redirect(url_for('stock_data_update_nse'))
        elif 'charts' in action:
            return redirect(url_for('charts_view_nse'))
            
    return render_template('summarystock.html', data = data_quality_summary, title='Stocks_NSE')

@app.route("/image/<path:filename>")
def get_image(filename):
    # Assuming your images are stored in 'summary_charts' folder
    return send_from_directory("E:/Programming/Python/Stocks/Stock_Analyzer/basic_analytics/summary_charts", filename)


@app.route("/analyse_charts_bse", methods=["GET", "POST"])
def charts_view_bse():
    
    folder = 'E:/Programming/Python/Stocks/Stock_Analyzer/basic_analytics'
    file = 'bse_stock_data_summary.csv'
    chart_summary = 'chart_summary_settings_bse.csv'
    
    path = folder + '/' + file
    chart_summary_path = folder + '/' + chart_summary
    
    if os.path.exists(path):
        data_quality_summary = pd.read_csv(path)
        # Convert 'max date' column to datetime
        data_quality_summary['max_date'] = pd.to_datetime(data_quality_summary['max_date'])
        # Sorting by 'max date' column in descending order
        data_quality_summary = data_quality_summary.sort_values(by='max_date', ascending=False)
        # Get the maximum value of the 'max_date' column
        max_date_value = data_quality_summary['max_date'].max()
        data_quality_summary = data_quality_summary[data_quality_summary['max_date'] >= max_date_value - pd.Timedelta(days=7)]
        
        #Select columns of interest
        columns_of_interest = ['latest_closing_price', 'growth_per_30', 'avg_vol_30', 'growth_per_7', 'avg_vol_7', 'latest_signal', 'signal_duration', 'trend_duration']
        
        absolute_max = []
        absolute_min = []
        for column in columns_of_interest:
            if column != 'latest_signal':
                absolute_max.append(max(data_quality_summary[column]))
                absolute_min.append(min(data_quality_summary[column]))
            elif column == 'latest_signal':
                absolute_max.append(1)
                absolute_min.append(0)
        
        if os.path.exists(chart_summary_path):
            filtered_cols = pd.read_csv(chart_summary_path)
            # Loop over each row in filtered_cols
            for index, row in filtered_cols.iterrows():
                # Get the title, min, and max values from the current row
                title = row['title']
                min_val = row['min']
                max_val = row['max']
                
        
                # Filter rows where the values fall within the specified range
                if title != 'latest_signal':
                    data_quality_summary = data_quality_summary[(data_quality_summary[title] >= min_val) & (data_quality_summary[title] <= max_val)]
                elif title == 'latest_signal':
                    if min_val == 1 and max_val == 0:
                        data_quality_summary = data_quality_summary[(data_quality_summary[title] == 'Buy')]
                    elif min_val == 0 and max_val == 1:
                        data_quality_summary = data_quality_summary[(data_quality_summary[title] == 'Sell')]
                    

        # Plotting the distribution of selected columns
        image_paths = []
        titles = []
        curr_max = []
        curr_min = []
        for column in columns_of_interest:
            plt.figure(figsize=(8, 8))
            plt.hist(data_quality_summary[column], bins=100, color='skyblue', edgecolor='black')
            plt.title(f'Distribution of {column}', fontsize=12)
            plt.xlabel(column, fontsize=12)
            plt.ylabel('Frequency', fontsize=12)
            plt.xticks(rotation=20)  # Rotate x-axis labels by 45 degrees
            plt.tick_params(axis='both', which='major', labelsize=15)  # Set tick size
            # Make ticks sparser
            plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(nbins=10))
            #plt.grid(True)
            plt.savefig(os.getcwd() + '/basic_analytics/summary_charts/' + f'summary_distributions_{column}.png')
            image_paths.append(f'summary_distributions_{column}.png')
            titles.append(column)
            
            if column != 'latest_signal':
                curr_max.append(max(data_quality_summary[column]))
                curr_min.append(min(data_quality_summary[column]))
            elif column == 'latest_signal':
                curr_max.append(1)
                curr_min.append(0)
        
        if data_quality_summary.empty:
            return redirect(url_for('stock_data_update_bse'))
    else:
        return redirect(url_for('stock_data_update_bse'))
    
    # Pre-zip images and titles
    chart_data = zip(image_paths, titles, absolute_max, absolute_min, curr_min, curr_max)

    if request.method == "POST":
        # Get the selected metadata value from the form
        action = request.form.get("action")
        
        data_string = request.form.get('data')
        if data_string:
            # Process the received data
            data_list = data_string.split(' ')
            with open(os.getcwd() + '/basic_analytics/chart_summary_settings_bse.csv', 'w', newline='') as csvfile:
                fieldnames = ['title', 'min', 'max']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for item in data_list:
                    item_data = item.split(':')
                    if len(item_data) == 3:  
                        # Ensure that each item has all three parts: title, min, and max
                        writer.writerow({'title': item_data[0], 'min': item_data[1], 'max': item_data[2]})
        
        if action == 'analysis_page':
            return redirect(url_for('stock_data_update_bse'))
        elif action == 'home_page':
            return redirect(url_for('index'))
        elif action == 'clear':
            os.remove(chart_summary_path)
            return redirect(url_for('charts_view_bse'))
        elif 'analyze' in action:
            symbol = action.split('_')[1]
            return redirect(url_for('stock_view', symbol=symbol, exchange='BSE', user='NA'))
    
    return render_template('charts.html', title='Stock Distribution Charts BSE', chart_data=chart_data, data = data_quality_summary)


@app.route("/analyse_charts_nse", methods=["GET", "POST"])
def charts_view_nse():
    
    folder = 'E:/Programming/Python/Stocks/Stock_Analyzer/basic_analytics'
    file = 'nse_stock_data_summary.csv'
    chart_summary = 'chart_summary_settings_nse.csv'
    
    path = folder + '/' + file
    chart_summary_path = folder + '/' + chart_summary
    
    if os.path.exists(path):
        data_quality_summary = pd.read_csv(path)
        # Convert 'max date' column to datetime
        data_quality_summary['max_date'] = pd.to_datetime(data_quality_summary['max_date'])
        # Sorting by 'max date' column in descending order
        data_quality_summary = data_quality_summary.sort_values(by='max_date', ascending=False)
        # Get the maximum value of the 'max_date' column
        max_date_value = data_quality_summary['max_date'].max()
        data_quality_summary = data_quality_summary[data_quality_summary['max_date'] >= max_date_value - pd.Timedelta(days=7)]
        
        #Select columns of interest
        columns_of_interest = ['latest_closing_price', 'growth_per_30', 'avg_vol_30', 'growth_per_7', 'avg_vol_7', 'latest_signal', 'signal_duration', 'trend_duration']
        
        absolute_max = []
        absolute_min = []
        for column in columns_of_interest:
            if column != 'latest_signal':
                absolute_max.append(max(data_quality_summary[column]))
                absolute_min.append(min(data_quality_summary[column]))
            elif column == 'latest_signal':
                absolute_max.append(1)
                absolute_min.append(0)
            
        
        if os.path.exists(chart_summary_path):
            filtered_cols = pd.read_csv(chart_summary_path)
            # Loop over each row in filtered_cols
            for index, row in filtered_cols.iterrows():
                # Get the title, min, and max values from the current row
                title = row['title']
                min_val = row['min']
                max_val = row['max']
        
                # Filter rows where the values fall within the specified range
                if title != 'latest_signal':
                    data_quality_summary = data_quality_summary[(data_quality_summary[title] >= min_val) & (data_quality_summary[title] <= max_val)]
                elif title == 'latest_signal':
                    if min_val == 1 and max_val == 0:
                        data_quality_summary = data_quality_summary[(data_quality_summary[title] == 'Buy')]
                    elif min_val == 0 and max_val == 1:
                        data_quality_summary = data_quality_summary[(data_quality_summary[title] == 'Sell')]
            

        # Plotting the distribution of selected columns
        image_paths = []
        titles = []
        curr_max = []
        curr_min = []
        for column in columns_of_interest:
            plt.figure(figsize=(8, 8))
            plt.hist(data_quality_summary[column], bins=100, color='skyblue', edgecolor='black')
            plt.title(f'Distribution of {column}', fontsize=12)
            plt.xlabel(column, fontsize=12)
            plt.ylabel('Frequency', fontsize=12)
            plt.xticks(rotation=20)  # Rotate x-axis labels by 45 degrees
            plt.tick_params(axis='both', which='major', labelsize=15)  # Set tick size
            # Make ticks sparser
            plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(nbins=10))
            #plt.grid(True)
            plt.savefig(os.getcwd() + '/basic_analytics/summary_charts/' + f'summary_distributions_{column}.png')
            image_paths.append(f'summary_distributions_{column}.png')
            titles.append(column)
            
            if column != 'latest_signal':
                curr_max.append(max(data_quality_summary[column]))
                curr_min.append(min(data_quality_summary[column]))
            elif column == 'latest_signal':
                curr_max.append(1)
                curr_min.append(0)
        
        if data_quality_summary.empty:
            return redirect(url_for('stock_data_update_nse'))
    else:
        return redirect(url_for('stock_data_update_nse'))
    
    # Pre-zip images and titles
    chart_data = zip(image_paths, titles, absolute_max, absolute_min, curr_min, curr_max)
    
    if request.method == "POST":
        # Get the selected metadata value from the form
        action = request.form.get("action")
        
        data_string = request.form.get('data')
        if data_string:
            # Process the received data
            data_list = data_string.split(' ')
            with open(os.getcwd() + '/basic_analytics/chart_summary_settings_nse.csv', 'w', newline='') as csvfile:
                fieldnames = ['title', 'min', 'max']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for item in data_list:
                    item_data = item.split(':')
                    if len(item_data) == 3:  
                        # Ensure that each item has all three parts: title, min, and max
                        writer.writerow({'title': item_data[0], 'min': item_data[1], 'max': item_data[2]})
        
        if action == 'analysis_page':
            return redirect(url_for('stock_data_update_nse'))
        elif action == 'home_page':
            return redirect(url_for('index'))
        elif action == 'clear':
            os.remove(chart_summary_path)
            return redirect(url_for('charts_view_nse')) 
        elif 'analyze' in action:
            symbol = action.split('_')[1]
            return redirect(url_for('stock_view', symbol=symbol, exchange='NSE', user='NA'))
        
    
    return render_template('charts.html', title='Stock Distribution Charts NSE', chart_data=chart_data, data = data_quality_summary)


@app.route('/stock_view/<symbol>/<exchange>/<user>', methods=["GET", "POST"])
def stock_view(symbol, exchange, user):
    # Render stock analysis page with the appropriate image for the symbol
    # You can use the symbol to dynamically load the image
    path_timeseries = os.getcwd() + '/stock_timeseries/' + exchange + '/' + symbol + '.csv'
    path_super_trend = os.getcwd() + '/strategy_data/supertrend_data/' + exchange + '/' + symbol + '.csv'
    if exchange == 'BSE':
        path_summary = 'E:/Programming/Python/Stocks/Stock_Analyzer/basic_analytics/' + 'bse_stock_data_summary.csv'
    elif exchange == 'NSE':
        path_summary = 'E:/Programming/Python/Stocks/Stock_Analyzer/basic_analytics/' + 'nse_stock_data_summary.csv'
    path_balance = os.getcwd() + '/stock_fundamentals/' + exchange + '/' + symbol + '_balance_sheet' + '.csv'
    path_income = os.getcwd() + '/stock_fundamentals/' + exchange + '/' + symbol + '_income_statement' + '.csv'
    path_stock_sum = 'E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/' + exchange + '/' + symbol + '_stock_summary' + '.csv'
    path_valuat = 'E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/' + exchange + '/' + symbol + '_valuation' + '.csv'
    path_div = 'E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/' + exchange + '/' + symbol + '_dividend' + '.csv'
    path_key = 'E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/' + exchange + '/' + symbol + '_key_ratio' + '.csv'
    path_grow = 'E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/' + exchange + '/' + symbol + '_growth_metrics' + '.csv'
    
    
    income_columns = ['Total Revenue', 'Cost Of Revenue', 'Gross Profit', 'Operating Expense', 'Operating Income', 'Depreciation And Amortization In Income Statement', 'EBITDA', 'Net Interest Income', 'Interest Expense', 'Net Income From Continuing Operation Net Minority Interest', 'Net Income', 'Basic EPS', 'Diluted EPS', 'Tax Provision', 'Normalized EBITDA', 'Total Unusual Items', 'Date']
    balance_columns = ['Total Assets', 'Current Assets', 'Cash And Cash Equivalents', 'Accounts Receivable', 'Allowance For Doubtful Accounts Receivable', 'Net PPE', 'Accumulated Depreciation', 'Total Liabilities Net Minority Interest', 'Current Liabilities', 'Accounts Payable', 'Long Term Debt', 'Net Debt', 'Stockholders Equity', 'Common Stock Equity', 'Retained Earnings', 'Total Equity Gross Minority Interest', 'Working Capital', 'Total Non Current Liabilities Net Minority Interest', 'Date']
    
    image_paths = []
    titles = []
    
    if os.path.exists(path_timeseries) and os.path.exists(path_super_trend) and os.path.exists(path_summary):
        data_timeseries = pd.read_csv(path_timeseries)
        
        data_timeseries['Date'] = pd.to_datetime(data_timeseries['Date'])
        data_timeseries = data_timeseries.sort_values(by='Date')
        
        # Filter data for the last 6 months
        six_months_ago = pd.Timestamp.now() - pd.DateOffset(months=6)
        df_last_6_months = data_timeseries[data_timeseries['Date'] >= six_months_ago]
        # Plotting
        plt.figure(figsize=(10, 6))
        plt.plot(df_last_6_months['Date'], df_last_6_months['Open'], label='Open', color='blue', marker='o')
        plt.plot(df_last_6_months['Date'], df_last_6_months['High'], label='High', color='green', marker='o')
        plt.plot(df_last_6_months['Date'], df_last_6_months['Low'], label='Low', color='red', marker='o')
        plt.plot(df_last_6_months['Date'], df_last_6_months['Close'], label='Close', color='orange', marker='o')

        plt.title('Last 6 Months Trend')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        plt.savefig(os.getcwd() + '/basic_analytics/summary_charts/' + f'timeseries_6mon.png')
        image_paths.append(f'timeseries_6mon.png')
        titles.append('Timeseries')

        # Plot super trend data
        data_supertrend = pd.read_csv(path_super_trend)
        
        data_supertrend['Date'] = pd.to_datetime(data_supertrend['Date'])
        data_supertrend = data_supertrend.sort_values(by='Date')
        data_supertrend = data_supertrend[data_supertrend['Date'] >= six_months_ago]
        # Filter rows where BuySignal or SellSignal is not zero
        buy_signals = data_supertrend[data_supertrend['BuySignal'] != 0]
        sell_signals = data_supertrend[data_supertrend['SellSignal'] != 0]
        
        plt.figure(figsize=(10, 6))
        plt.plot(data_supertrend['Date'], data_supertrend['SuperTrend'], label='SuperTrend', color='k')
        plt.scatter(buy_signals['Date'], buy_signals['BuySignal'], marker='*', color='green', label='Buy Signal')
        plt.scatter(sell_signals['Date'], sell_signals['SellSignal'], marker='*', color='red', label='Sell Signal')
        plt.plot(data_supertrend['Date'], data_supertrend['Close'], label='Close', color='red')
        plt.title('SuperTrend Plot (Last 6 Months)')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.xticks(rotation=45)
        plt.legend()
        plt.savefig(os.getcwd() + '/basic_analytics/summary_charts/' + f'supertrend_6mon.png')
        image_paths.append(f'supertrend_6mon.png')
        titles.append('Supertrend')
        
        # Pre-zip images and titles
        chart_data = zip(image_paths, titles)
        
        data_quality_summary = pd.read_csv(path_summary)
        data_quality_summary = data_quality_summary[data_quality_summary['symbol']==symbol]
        table_html = data_quality_summary.to_html(index=False)
        
        ava_col_b = pd.read_csv(path_balance, nrows=0).columns.tolist()
        balance_columns_to_use = [col for col in balance_columns if col in ava_col_b]
        data_balance = pd.read_csv(path_balance, usecols=balance_columns_to_use)
        div_b = [col for col in balance_columns_to_use if col not in ['Date']]
        data_balance[div_b] = data_balance[div_b].div(10000000)
        table_balance = data_balance.to_html(index=False)
        
        ava_col_in = pd.read_csv(path_income, nrows=0).columns.tolist()
        income_columns_to_use = [col for col in income_columns if col in ava_col_in]
        data_income = pd.read_csv(path_income, usecols=income_columns_to_use)
        div_i = [col for col in income_columns_to_use if col not in ['Date', 'Diluted EPS', 'Basic EPS']]
        data_income[div_i] = data_income[div_i].div(10000000)
        table_income = data_income.to_html(index=False)
        
        stock_sum = pd.read_csv(path_stock_sum)
        table_sum = stock_sum.to_html(index=False)
        
        stock_valuat = pd.read_csv(path_valuat)
        table_valuat = stock_valuat.to_html(index=False)
        
        stock_div = pd.read_csv(path_div)
        table_div = stock_div.to_html(index=False)
        
        stock_key = pd.read_csv(path_key)
        table_key = stock_key.to_html(index=False)
        
        stock_grow = pd.read_csv(path_grow)
        table_grow = stock_grow.to_html(index=False)
        
    else:
        if exchange == 'BSE':
            return redirect(url_for('charts_view_bse')) 
        if exchange == 'NSE':
            return redirect(url_for('charts_view_nse')) 
        
    
    return render_template('stock_view.html', title=f'Stock Analysis - {exchange}:{symbol}', chart_data=chart_data, table=table_html, balance=table_balance, income=table_income, description=table_sum, value=table_valuat, dividend=table_div, keys_p=table_key, st_grow=table_grow)


@app.route('/portfolio', methods=["GET", "POST"])
def manage_portfolio():
    
    portfolio_ledger = os.getcwd() + '/portfolio_data/ledger.csv'
    
    if os.path.exists(portfolio_ledger):
        ledger = pd.read_csv(portfolio_ledger)
    else:
        ledger = pd.DataFrame(columns=['timestamp', 'user', 'app', 'symbol', 'action', 'action_date', 'added_date', 'quantity', 'price', 'split ratio'])
        ledger.to_csv(portfolio_ledger, index=False)
        
    if request.method == "POST":
        # Get the selected metadata value from the form
        action = request.form.get("action")
        
        if action == 'home_page':
            return redirect(url_for('index'))
        
        elif action == 'submit_ledger':  
            current_datetime = datetime.datetime.now()
            timestamp = int(current_datetime.timestamp() * 1e6)
            user = request.form.get('user')
            app = request.form.get('app')
            symbol = request.form.get('symbol')
            action_value = request.form.get('action_value')
            action_date = request.form.get('action_date')
            added_date = datetime.date.today().isoformat()
            quantity = request.form.get('quantity')
            price = request.form.get('price')
            split = request.form.get('split_ratio')
            
            ledger = pd.read_csv(portfolio_ledger)
            
            # Append the new data to the existing DataFrame
            new_entry = {'timestamp': timestamp, 'user': user, 'app': app, 'symbol': symbol, 'action': action_value, 'action_date': action_date,
                         'added_date': added_date, 'quantity': quantity, 'price': price, 'split ratio':split}
            ledger = ledger._append(new_entry, ignore_index=True)

            # Save the updated DataFrame back to CSV
            ledger.to_csv(portfolio_ledger, index=False)
            
            return redirect(url_for('manage_portfolio'))
        
        elif 'delete' in action:  
            timestamp = action.split('_')[1]
            # Save the removed timestamp value to a text file
            #with open('removed_timestamp.txt', 'w') as file:
                #file.write(timestamp)
            ledger = pd.read_csv(portfolio_ledger)
            # Filter out the row where the 'timestamp' column matches the specified timestamp
            ledger = ledger[ledger['timestamp'] != int(timestamp)]
            # Save the updated DataFrame back to CSV
            ledger.to_csv(portfolio_ledger, index=False)
            
            return redirect(url_for('manage_portfolio'))
        
        elif action == 'portfolio_summary':

            return redirect(url_for('portfolio_summary'))
            
    
    return render_template('manage_portfolio.html', data=ledger)

@app.route('/portfolio_summary', methods=["GET", "POST"])
def portfolio_summary():
    
    stock_exchange = 'NA'
    user_name = 'NA'
    summary_data = pd.DataFrame(columns=['symbol','latest_date','closing_price','last_action','last_action_date','current_principle','current_quantity','current_buy_price_avg','total_PL','unrealized_PL'])
    summary_data.loc[0] = ['NA'] * len(summary_data.columns)
    invested_amount = 0.0
    realized_profit = 0.0
    unrealized_profit = 0.0
    
    if request.method == "POST":
        action = request.form.get("action")
        
        if action == "home_page":
            return redirect(url_for('index'))
        elif action == "manage_portfolio":
            return redirect(url_for('manage_portfolio'))
        elif action == 'update_port_summary':
            stock_exchange = request.form.get("exchange")
            stock_exchange = stock_exchange.split('_')[1]
            user_name = request.form.get("user")
            dq.portfolio_analysis_summary(user_name, stock_exchange)
            
            summary_data = pd.read_csv(os.getcwd() + '/portfolio_data/' + user_name + '_' + stock_exchange +'_portfolio_summary.csv')
            invested_amount = summary_data['current_principle'].sum()
            realized_profit = summary_data['total_PL'].sum()
            unrealized_profit = summary_data['unrealized_PL'].sum()
            
            return render_template('portfolio_summary.html', exchange=stock_exchange, user=user_name, data=summary_data, principle_amount=invested_amount, real_tot_profit=realized_profit, unreal_tot_profit=unrealized_profit)
        elif action == 'add_portfolio':
            stock_exchange = request.form.get("exchange")
            stock_exchange = stock_exchange.split('_')[1]
            user_name = request.form.get("user")
            summary_data = pd.read_csv(os.getcwd() + '/portfolio_data/' + user_name + '_' + stock_exchange +'_portfolio_summary.csv')
            symbols = summary_data['symbol'].unique()
            for val in symbols:
                if os.path.exists('E:/Programming/Python/Stocks/Stock_Analyzer/stock_timeseries/' + stock_exchange + '/' + val + '.csv'):
                    continue
                else:
                    try:
                        data = c.get_price_timeseries(val, stock_exchange, 'max')
                        data.to_csv('E:/Programming/Python/Stocks/Stock_Analyzer/stock_timeseries/' + stock_exchange + '/' + val + '.csv', index=False)
                        income_statement = c.income_statement_data(val, stock_exchange)
                        income_statement.to_csv('E:/Programming/Python/Stocks/Stock_Analyzer/stock_fundamentals/' + stock_exchange + '/' + val + '_income_statement' + '.csv', index=False)
                        balance_sheet = c.balance_sheet_data(val, stock_exchange)
                        balance_sheet.to_csv('E:/Programming/Python/Stocks/Stock_Analyzer/stock_fundamentals/' + stock_exchange + '/' + val + '_balance_sheet' + '.csv', index=False)
                        stock_summary, valuation_info, dividend_inf, keys, growth = c.get_company_description_summary(val, 'NSE')
                        stock_summary.to_csv('E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/' + stock_exchange + '/' + val + '_stock_summary' + '.csv', index=False)
                        valuation_info.to_csv('E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/' + stock_exchange + '/' + val + '_valuation' + '.csv', index=False)
                        dividend_inf.to_csv('E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/' + stock_exchange + '/' + val + '_dividend' + '.csv', index=False)
                        keys.to_csv('E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/' + stock_exchange + '/' + val + '_key_ratio' + '.csv', index=False)
                        growth.to_csv('E:/Programming/Python/Stocks/Stock_Analyzer/stock_company_details/' + stock_exchange + '/' + val + '_growth_metrics' + '.csv', index=False)
                    except Exception as e:
                        continue
            dq.portfolio_analysis_summary(user_name, stock_exchange)
            
            summary_data = pd.read_csv(os.getcwd() + '/portfolio_data/' + user_name + '_' + stock_exchange +'_portfolio_summary.csv')
            invested_amount = summary_data['current_principle'].sum()
            realized_profit = summary_data['total_PL'].sum()
            unrealized_profit = summary_data['unrealized_PL'].sum()
            
            return render_template('portfolio_summary.html', exchange=stock_exchange, user=user_name, data=summary_data, principle_amount=invested_amount, real_tot_profit=realized_profit, unreal_tot_profit=unrealized_profit)
        elif action == 'update_port_stocks':
            stock_exchange = request.form.get("exchange")
            stock_exchange = stock_exchange.split('_')[1]
            user_name = request.form.get("user")
            summary_data = pd.read_csv(os.getcwd() + '/portfolio_data/' + user_name + '_' + stock_exchange +'_portfolio_summary.csv')
            symbols = summary_data['symbol'].unique()
            for val in symbols:
                try:
                    data = c.get_price_timeseries(val, stock_exchange, '1mo')
                    u.update_csv(data, 'E:/Programming/Python/Stocks/Stock_Analyzer/stock_timeseries/' + stock_exchange + '/' + val + '.csv', 'Date')
                except Exception as e:
                    continue
            dq.portfolio_analysis_summary(user_name, stock_exchange)
            
            summary_data = pd.read_csv(os.getcwd() + '/portfolio_data/' + user_name + '_' + stock_exchange +'_portfolio_summary.csv')
            invested_amount = summary_data['current_principle'].sum()
            realized_profit = summary_data['total_PL'].sum()
            unrealized_profit = summary_data['unrealized_PL'].sum()
            
            return render_template('portfolio_summary.html', exchange=stock_exchange, user=user_name, data=summary_data, principle_amount=invested_amount, real_tot_profit=realized_profit, unreal_tot_profit=unrealized_profit)
        elif action == 'remove_data':
            stock_exchange = request.form.get("exchange")
            stock_exchange = stock_exchange.split('_')[1]
            user_name = request.form.get("user")
            summary_data = pd.read_csv(os.getcwd() + '/portfolio_data/' + user_name + '_' + stock_exchange +'_portfolio_summary.csv')
            symbols = summary_data['symbol'].unique()
            for val in symbols:
                if os.path.exists('E:/Programming/Python/Stocks/Stock_Analyzer/stock_timeseries/' + stock_exchange + '/' + val + '.csv'):
                    stock_data = pd.read_csv('E:/Programming/Python/Stocks/Stock_Analyzer/stock_timeseries/' + stock_exchange + '/' + val + '.csv')
                    #with open('stocks_del.txt', 'w') as file:
                        #file.write(val)
                    stock_data['Date'] = pd.to_datetime(stock_data['Date'])
                    stock_data.sort_values(by='Date', inplace=True)
                    #stock_data.to_csv('test.csv', index=False)
                    stock_data.drop(stock_data.tail(1).index, inplace=True)
                    stock_data = stock_data.drop_duplicates()
                    stock_data.to_csv('E:/Programming/Python/Stocks/Stock_Analyzer/stock_timeseries/' + stock_exchange + '/' + val + '.csv', index=False)
            dq.portfolio_analysis_summary(user_name, stock_exchange)
            
            summary_data = pd.read_csv(os.getcwd() + '/portfolio_data/' + user_name + '_' + stock_exchange +'_portfolio_summary.csv')
            invested_amount = summary_data['current_principle'].sum()
            realized_profit = summary_data['total_PL'].sum()
            unrealized_profit = summary_data['unrealized_PL'].sum()
            
            return render_template('portfolio_summary.html', exchange=stock_exchange, user=user_name, data=summary_data, principle_amount=invested_amount, real_tot_profit=realized_profit, unreal_tot_profit=unrealized_profit)
        elif 'view' in action:  
            symbol = action.split('_')[1]
            stock_exchange = action.split('_')[2]
            user = action.split('_')[3]
            with open('stocks.txt', 'w') as file:
                file.write(user)
            
            return redirect(url_for('stock_view', symbol=symbol, exchange=stock_exchange, user=user))
    
    return render_template('portfolio_summary.html', exchange=stock_exchange, user=user_name, data=summary_data, principle_amount=invested_amount, real_tot_profit=realized_profit, unreal_tot_profit=unrealized_profit)
    
    
    
if __name__ == "__main__":
    
    app.run()