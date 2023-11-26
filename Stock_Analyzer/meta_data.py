# -*- coding: utf-8 -*-
"""
Created on Sun Aug  6 18:43:20 2023

@author: aksha
"""

import os 
import requests
from dotenv import load_dotenv

load_dotenv()

X_RapidAPI_Key = os.environ.get('X-RapidAPI-Key_TwelveData')
X_RapidAPI_Host = os.environ.get('X-RapidAPI-Host_TwelveData')

# Define the function to make API call and get list of available exchanges in Twelve data
def get_exchanges_list():
     
    exchange_url = 'https://twelve-data1.p.rapidapi.com/exchanges'
    querystring = {"format":"json"}
    headers = {
	"X-RapidAPI-Key": X_RapidAPI_Key,
	"X-RapidAPI-Host": X_RapidAPI_Host
    }

    response = requests.get(exchange_url, headers=headers, params=querystring)

    return response.json()

# Define the function to make API call and get list of available crypto exchanges in Twelve data
def get_crypto_exchanges_list():
     
    crypto_exchange_url = 'https://twelve-data1.p.rapidapi.com/cryptocurrency_exchanges'
    querystring = {"format":"json"}
    headers = {
	"X-RapidAPI-Key": X_RapidAPI_Key,
	"X-RapidAPI-Host": X_RapidAPI_Host
    }

    response = requests.get(crypto_exchange_url, headers=headers, params=querystring)

    return response.json()

# Define the function to make API call and get list of available technical indicators in Twelve data
def get_technical_indicator_list():
     
    indicators_url = 'https://twelve-data1.p.rapidapi.com/technical_indicators'
    querystring = {"format":"json"}
    headers = {
	"X-RapidAPI-Key": X_RapidAPI_Key,
	"X-RapidAPI-Host": X_RapidAPI_Host
    }

    response = requests.get(indicators_url, headers=headers, params=querystring)

    return response.json()

# Test the functions
#stocks = get_country_symbol_list()
#print(stocks)