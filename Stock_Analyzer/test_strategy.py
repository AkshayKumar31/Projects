# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 11:13:33 2024

@author: aksha
"""

import strategy.mrmd as mrmd

# Test functions 
total_profit, total_invested, total_return_percentage = mrmd.mrmd_strategy_return('NSE', 3, 5000000000, 100, 15, 'reinvestement', 'false', 'quarterly', 252, 252)
print("Total Profit: " + str(round(total_profit,2)))
print("Total Investment Required: " + str(round(total_invested,2)))
print("Percentage Return: " + str(round(total_return_percentage,2)) + " %")