# -*- coding: utf-8 -*-
"""
Created on Sat Jul 29 21:23:39 2023

@author: aksha
"""

import os 
import requests
from dotenv import load_dotenv

load_dotenv()

X_RapidAPI_Key = os.environ.get('X-RapidAPI-Key_TwelveData')
X_RapidAPI_Host = os.environ.get('X-RapidAPI-Host_TwelveData')
base_currency = os.environ.get('base_currency')
base_crypto = os.environ.get('base_crypto')

# Define the function to make API call and get list of stocks
def get_stock_list(exchange):
     
    stock_url = 'https://twelve-data1.p.rapidapi.com/stocks'
    querystring = {"exchange":exchange,"format":"json"}
    headers = {
	"X-RapidAPI-Key": X_RapidAPI_Key,
	"X-RapidAPI-Host": X_RapidAPI_Host
    }

    response = requests.get(stock_url, headers=headers, params=querystring)

    return response.json()

# Define the function to make API call and get list of forex pairs
def get_forex_pairs(base_currency = base_currency):
    
    forex_url = 'https://twelve-data1.p.rapidapi.com/forex_pairs'
    querystring = {"currency_base":base_currency,"format":"json"}
    headers = {
	"X-RapidAPI-Key": X_RapidAPI_Key,
	"X-RapidAPI-Host": X_RapidAPI_Host
    }

    response = requests.get(forex_url, headers=headers, params=querystring)

    return response.json()

# Define the function to make API call and get list of crypto currencies
def get_crypto_list(base_currency = base_crypto):
    
    crypto_url = 'https://twelve-data1.p.rapidapi.com/cryptocurrencies'
    querystring = {"currency_base":base_currency,"format":"json"}
    headers = {
	"X-RapidAPI-Key": X_RapidAPI_Key,
	"X-RapidAPI-Host": X_RapidAPI_Host
    }

    response = requests.get(crypto_url, headers=headers, params=querystring)

    return response.json()

# Define the function to make API call and get list of ETFs
def get_etf_list(exchange):
    
    etf_url = 'https://twelve-data1.p.rapidapi.com/etf'
    querystring = {"exchange":exchange,"format":"json"}
    headers = {
	"X-RapidAPI-Key": X_RapidAPI_Key,
	"X-RapidAPI-Host": X_RapidAPI_Host
    }

    response = requests.get(etf_url, headers=headers, params=querystring)

    return response.json()

# Define the function to make API call and get list of Indices
def get_indices_list(exchange):
    
    indices_url = 'https://twelve-data1.p.rapidapi.com/indices'
    querystring = {"exchange":exchange,"format":"json"}
    headers = {
	"X-RapidAPI-Key": X_RapidAPI_Key,
	"X-RapidAPI-Host": X_RapidAPI_Host
    }

    response = requests.get(indices_url, headers=headers, params=querystring)

    return response.json()

# Test the functions
#stocks = get_stock_list('BSE')
#print(stocks)