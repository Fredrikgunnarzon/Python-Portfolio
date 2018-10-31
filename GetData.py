###################################################################
# Version 1.0, 30 October 2018
# Author: Fredrik Gunnarsson, fredrikgunnarsson@outlook.com
###################################################################
# Updates the Data storage for the Portfolio program
###################################################################

import pandas as pd 
import pandas_datareader as web
import datetime
import numpy as np
from pandas import DataFrame
import quandl

pd.set_option('display.height', 1000)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

#Index settings
start 	= datetime.datetime.strptime('2018-08-03','%Y-%m-%d').date()
end 	= datetime.date.today()
Index   = '^OMX'  

def printMoney(Net):
	print("\n\nYour Net Worth is:", Net,"\n\n")
	return 0


def Stock_Data(_vec_derivative,start,end):

	Data 	= DataFrame()
	symbols	= []
	i 		= 0

	for ticker in _vec_derivative.Tickers:
		stock = web.DataReader(ticker, "yahoo", start, end)
		if start != datetime.date.today():
			stock=stock.iloc[1:]
		Data['Adj Close: '+ ticker] = stock['Adj Close']
		Data['Worth: '+ ticker] = _vec_derivative.Amount[i]*stock["Adj Close"]
		i = i + 1
	return Data

def Cash_Data(Data,_init_cash):
	i = 0
	for ticker in _init_cash.Tickers:
		Data['Adj Close: '+ ticker] = np.ones(len(Data))
		Data['Worth: '+ ticker] = np.ones(len(Data))*_init_cash.Amount.iloc[i]
		i = i + 1
	return Data

def Crypto_Data(Data,_init_Portfolio,start,end):
	i=0
	for ticker in _init_Portfolio.Tickers:
		df = quandl.get(ticker, returns="pandas")
		Data["Adj Close: "+ticker] = df["Weighted Price"]
		Data.iloc[-1,Data.columns.get_loc("Adj Close: "+ticker)] = df["Weighted Price"].iloc[-1]
		Data["Worth: "+ticker] = df["Weighted Price"]*_init_Portfolio.Amount.iloc[i]
		Data.iloc[-1,Data.columns.get_loc("Worth: "+ticker)] = df["Weighted Price"].iloc[-1]*_init_Portfolio.Amount.iloc[i]
		i=i+1
	return Data


def Load_Data(_init_Portfolio):
	f = open("Stock_Data.csv", "a")
	csvfile = pd.read_csv('Stock_Data.csv', encoding='utf-8',parse_dates=True)
	EndDate = datetime.datetime.strptime(csvfile.Date.iloc[-1],'%Y-%m-%d').date()
	if (EndDate	!= datetime.date.today()):
		start 	= EndDate + datetime.timedelta(days=1)
		end 	= datetime.date.today()
		print("Retrieving data for: \n",_init_Portfolio[(_init_Portfolio['Type']=='Stock')],"\n")
		Portfolio = Stock_Data(_init_Portfolio[(_init_Portfolio['Type']=='Stock')],start,end)


		print("Retrieving data for: \n",_init_Portfolio[(_init_Portfolio['Type']=='Cash')],"\n")
		Portfolio = Cash_Data(Portfolio,_init_Portfolio[(_init_Portfolio['Type']=='Cash')])


		print("Retrieving data for: \n",_init_Portfolio[(_init_Portfolio['Type']=='Crypto')],"\n")
		Portfolio = Crypto_Data(Portfolio,_init_Portfolio[(_init_Portfolio['Type']=='Crypto')],start,end)
		print(Portfolio)
		f.write('\n')
		Portfolio.to_csv(f,sep=',',header=False)
		print('\nStock data is now updated\n')
	else:
		print('Data is already up to date')
	f.close()


def Index_Data():
	global start, end, Index
	Data 	= DataFrame()
	symbols	= []
	stock = web.DataReader(Index, "yahoo", start, end)
	Data['Adj Close: '+ Index] = stock['Adj Close'][1:]
	return Data





