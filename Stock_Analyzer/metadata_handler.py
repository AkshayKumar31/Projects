# -*- coding: utf-8 -*-
"""
Created on Sun Aug  6 18:52:23 2023

@author: aksha
"""

import os 
import pandas as pd
import meta_data as m
from datetime import datetime

        
def update_metadata(metadata_to_update):
    
    folder = 'E:/Programming/Python/Stocks/Stock_Analyzer/meta_data'
    added_date = datetime.today().strftime('%Y-%m-%d')
    
    if metadata_to_update == '1':
        csv_file_path = os.path.join(folder, 'exchanges.csv')
        meta = m.get_exchanges_list()
        meta = pd.DataFrame(meta['data'])
        symbol = 'name'
            
    elif metadata_to_update == '2':
        csv_file_path = os.path.join(folder, 'crypto_exchanges.csv')
        meta = m.get_crypto_exchanges_list()
        meta = pd.DataFrame(meta['data'])
        symbol = 'name'
        
    elif metadata_to_update == '3':
        csv_file_path = os.path.join(folder, 'technical_indicators.csv')
        meta = m.get_technical_indicator_list()
        meta = meta['data']
        meta = [{'indicator': key, **value} for key, value in meta.items()]
        meta = pd.DataFrame(meta)
        symbol = 'indicator'
    
    else: 
        print('Please enter a valid choice from provided list')
        
    meta['added_date'] = added_date
    meta['deleted_date'] = ''
        
    if os.path.exists(csv_file_path):
        existing_data = pd.read_csv(csv_file_path)
            
        # Identify deleted rows
        deleted_rows = existing_data[~existing_data[symbol].isin(meta[symbol])]
        if not deleted_rows.empty:
            deleted_rows['deleted_date'] = added_date
            existing_data.update(deleted_rows)
            
        # Identify reappeared rows with non-null deleted_date and update their added_date
        # So reappeared rows will have added date > deleted date
        reappeared_rows = existing_data[
                     existing_data[symbol].isin(meta[symbol]) &
                     ~existing_data['deleted_date'].isnull()
                  ]
        if not reappeared_rows.empty:
            existing_data.loc[existing_data[symbol].isin(reappeared_rows[symbol]), 'added_date'] = added_date
        
        # Identify new rows
        new_rows = meta[~meta[symbol].isin(existing_data[symbol])]
        if not new_rows.empty:
            existing_data = pd.concat([existing_data, new_rows], ignore_index=True).drop_duplicates()
        existing_data.to_csv(csv_file_path, index=False)
    else:
        meta.to_csv(csv_file_path, index=False)


#metadata_to_update = input('Enter the metadata to be updated [exchanges -1, crypto exchanges - 2, technical indicator - 3]: ')

#update_metadata(metadata_to_update)