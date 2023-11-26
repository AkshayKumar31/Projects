# -*- coding: utf-8 -*-
"""
Created on Sun Aug  6 18:52:44 2023

@author: aksha
"""

import os
from dotenv import load_dotenv
import reference_data as r
import pandas as pd
from datetime import datetime

# Replace these values with your actual database information

def update_reference_data(data_to_update):
    
    folder = 'E:/Programming/Python/Stocks/Stock_Analyzer/reference_data'
    added_date = datetime.today().strftime('%Y-%m-%d')
    
    if data_to_update == 'stock_BSE':
        csv_file_path = os.path.join(folder, 'stocks_BSE.csv')
        f_ins = r.get_stock_list('BSE')
        f_ins = pd.DataFrame(f_ins['data'])
        field = 'symbol'
    
    elif data_to_update == 'stock_NSE':
        csv_file_path = os.path.join(folder, 'stocks_NSE.csv')
        f_ins = r.get_stock_list('NSE')
        f_ins = pd.DataFrame(f_ins['data'])
        field = 'symbol'
        
    elif data_to_update == 'forex':
        csv_file_path = os.path.join(folder, 'forex_pairs.csv')
        f_ins = r.get_forex_pairs()
        f_ins = pd.DataFrame(f_ins['data'])
        field = 'symbol'
    
    elif data_to_update == 'crypto':
        csv_file_path = os.path.join(folder, 'crypto_pairs.csv')
        f_ins = r.get_crypto_list()
        f_ins = pd.DataFrame(f_ins['data'])
        field = 'symbol'
    
    elif data_to_update == 'etf_BSE':
        csv_file_path = os.path.join(folder, 'etfs_BSE.csv')
        f_ins = r.get_etf_list('BSE')
        f_ins = pd.DataFrame(f_ins['data'])
        field = 'symbol'
    
    elif data_to_update == 'etf_NSE':
        csv_file_path = os.path.join(folder, 'etfs_NSE.csv')
        f_ins = r.get_etf_list('NSE')
        f_ins = pd.DataFrame(f_ins['data'])
        field = 'symbol'
        
    elif data_to_update == 'indices_BSE':
        csv_file_path = os.path.join(folder, 'indices_BSE.csv')
        f_ins = r.get_indices_list('BSE')
        f_ins = pd.DataFrame(f_ins['data'])
        field = 'symbol'
    
    elif data_to_update == 'indices_NSE':
        csv_file_path = os.path.join(folder, 'indices_NSE.csv')
        f_ins = r.get_indices_list('NSE')
        f_ins = pd.DataFrame(f_ins['data'])
        field = 'symbol'
    
    else:
        print('Please choose one value from the provided list')
        
    f_ins['added_date'] = added_date
    f_ins['deleted_date'] = ''
    
    if os.path.exists(csv_file_path):
        existing_data = pd.read_csv(csv_file_path)
        
        # Identify deleted rows
        deleted_rows = existing_data[~existing_data[field].isin(f_ins[field])]
        if not deleted_rows.empty:
            deleted_rows['deleted_date'] = added_date
            existing_data.update(deleted_rows)
        
        # Identify reappeared rows with non-null deleted_date and update their added_date
        # So reappeared rows will have added date > deleted date
        reappeared_rows = existing_data[
                 existing_data[field].isin(f_ins[field]) &
                 ~existing_data['deleted_date'].isnull()
              ]
        if not reappeared_rows.empty:
            existing_data.loc[existing_data[field].isin(reappeared_rows[field]), 'added_date'] = added_date
    
        # Identify new rows
        new_rows = f_ins[~f_ins[field].isin(existing_data[field])]
        if not new_rows.empty:
            existing_data = pd.concat([existing_data, new_rows], ignore_index=True).drop_duplicates()
        existing_data.to_csv(csv_file_path, index=False)
    else:
        f_ins.to_csv(csv_file_path, index=False)
        

#reference_data_to_update = input('Enter the reference data to be updated [stock_BSE, stock_NSE, forex, crypto, etf_BSE, etf_NSE, indices_BSE, indices_NSE]: ')
#update_reference_data(reference_data_to_update)

# Transform the csv to have latest added at and first added at. Similarly latest deleted at and first deleted at