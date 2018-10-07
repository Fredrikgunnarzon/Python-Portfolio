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

#stocks = pd.DataFrame({'Tickers': ["SAND.ST","SEB-A.ST","TELIA.ST","HEXA-B.ST","INVE-B.ST","GETI-B.ST","ARJO-B.ST"]
#	, 'Amount':[250,200,150,15,50,28,28]})
def printMoney(Net):
	print("\n\nYour Net Worth is:", Net,"\n\n")
	return 0


def Stock_Data(stocks,start,end):

	Portfolio=DataFrame()
	symbols=[]
	i=0

	for ticker in stocks.Tickers:
		stock = web.DataReader(ticker, "yahoo", start, end)
		if start != datetime.date.today():
			stock=stock.iloc[1:]
		Portfolio['Adj Close: '+ ticker] = stock['Adj Close']
		Portfolio['Worth: '+ ticker] = stocks.Amount[i]*stock["Adj Close"]
		i = i + 1
	return Portfolio

def Cash_Data(Portfolio,_init_cash):
	i = 0
	for ticker in _init_cash.Tickers:
		Portfolio['Worth: '+ ticker] = np.ones(len(Portfolio))*_init_cash.Amount.iloc[i]
		i = i + 1
	return Portfolio

def Crypto_Data(Portfolio,_init_Portfolio,start,end):
	i=0
	for ticker in _init_Portfolio.Tickers:
		df = quandl.get(ticker, returns="pandas")
		Portfolio["Adj Close: "+ticker] = df["Weighted Price"].tail(len(Portfolio)+1)
		Portfolio.iloc[-1,Portfolio.columns.get_loc("Adj Close: "+ticker)] = df["Weighted Price"].iloc[-1]
		Portfolio["Worth: "+ticker] = df["Weighted Price"].tail(len(Portfolio)+1)*_init_Portfolio.Amount.iloc[i]
		Portfolio.iloc[-1,Portfolio.columns.get_loc("Worth: "+ticker)] = df["Weighted Price"].iloc[-1]*_init_Portfolio.Amount.iloc[i]
		i=i+1
	return Portfolio


def Data(_init_Portfolio):
	f = open("Stock_Data.csv", "a")
	csvfile = pd.read_csv('Stock_Data.csv', encoding='utf-8',parse_dates=True)
	EndDate = datetime.datetime.strptime(csvfile.Date.iloc[-1],'%Y-%m-%d').date()
	if (EndDate != datetime.date.today()):
		start = EndDate + datetime.timedelta(days=1)
		end = datetime.date.today()
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









