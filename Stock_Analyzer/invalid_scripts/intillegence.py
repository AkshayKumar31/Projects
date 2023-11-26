# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 10:22:21 2023

@author: aksha
"""

import os 
import requests
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime
import pytz

load_dotenv()

alpha_vantage_key = os.environ.get('alpha_vantage_api_key')

def get_company_overview(symbol):
    # Doesn't work for Indian markets
    # reports latest data for earnings and financials released by the company
    
    url = 'https://www.alphavantage.co/query?function=OVERVIEW&symbol='+symbol+'&apikey='+alpha_vantage_key
    r = requests.get(url)
    data = dict(r.json())
    
    return data

def get_current_quote(symbol = 'ABFRL.BSE'):
    
    url = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol='+symbol+'&apikey='+alpha_vantage_key
    r = requests.get(url)
    data = r.json()

    return data['Global Quote']

def get_sentiment_and_news(symbols, start_date, end_date, limit):
    # Doesn't work for Indian stock currently
    # symbols - 'COIN,CRYPTO:BTC,FOREX:USD'
    # start_date - '20230410T0130' (2023-04-10 01:30:00)
    # end_date - '20230510T0130' (2023-05-10 01:30:00)
    # limit - 1000 (number)
    
    url = 'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers='+symbols+'&time_from='+start_date+'&time_to='+end_date+'&limit='+str(limit)+'&apikey='+alpha_vantage_key
    print(url)
    r = requests.get(url)
    data = r.json()
    
    score_definition = 'Sentiment score definition: ' + data['sentiment_score_definition'] + '    ' + 'Relevence score definition: ' + data['relevance_score_definition']
    data = pd.DataFrame(data['feed'])

    return score_definition, data

def get_sentiment_and_news_by_topic(symbols, topics, start_date, end_date, limit):
    # Doesn't work for Indian stock currently
    # symbols - 'COIN,CRYPTO:BTC,FOREX:USD'
    # topics - technology
    # start_date - '20230410T0130' (2023-04-10 01:30:00)
    # end_date - '20230510T0130' (2023-05-10 01:30:00)
    # limit - 1000 (number)
    
    url = 'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers='+symbols+'&topics='+topics+'&time_from='+start_date+'&time_to='+end_date+'&limit='+str(limit)+'&apikey='+alpha_vantage_key
    print(url)
    r = requests.get(url)
    data = r.json()
    
    score_definition = 'Sentiment score definition: ' + data['sentiment_score_definition'] + '    ' + 'Relevence score definition: ' + data['relevance_score_definition']
    data = pd.DataFrame(data['feed'])

    return score_definition, data


# Test Function
#overview = get_company_overview('PNBHOUSING.BSE')
#print(overview)

#current_price = get_current_quote('TVSMOTOR.BSE')
#print(current_price)

#score_definition, news = get_sentiment_and_news('AAPL', '20230410T0130', '20230510T0130', '100')
#print(score_definition)
#print(news)

#score_definition, news = get_sentiment_and_news_by_topic('AAPL', 'technology', '20230410T0130', '20230510T0130', '100')
#print(score_definition)
#print(news)