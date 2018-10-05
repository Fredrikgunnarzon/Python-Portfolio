import matplotlib.pyplot as plt
import pandas as pd 
import pandas_datareader as web
import datetime
import numpy as np
import matplotlib.cbook as cbook
import csv
import matplotlib.dates as mdates
pd.set_option('display.height', 1000)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

def plot_stocks(Data,stocks):
	ax1 = plt.subplot(221)
	ax2 = plt.subplot(222)
	ax3 = plt.subplot(212)

	Portfolio=pd.DataFrame()
	Portfolio['Date'] = pd.to_datetime(Data.Date)
	Portfolio['Net'] = 0
	Amount=[]
	Tickers_Daily =stocks[(stocks['Type']==('Stock'))|(stocks['Type']==('Crypto'))]
	for ticker in stocks["Tickers"]:
		Portfolio['Net'] += Data['Worth: '+ticker]
		if(any(Tickers_Daily.Tickers == ticker)):
			ax1.plot(pd.to_datetime(Data['Date']), Data['Adj Close: '+ticker]/Data['Adj Close: '+ticker][1],label=[ticker])		
		Amount.append(Data['Worth: '+ticker][30])
	print(Amount)
	x = np.arange(len(Amount))
	ax3.bar(x,height=Amount)
	plt.xticks(x, stocks.Tickers);


	legend = ax1.legend(loc='upper right',shadow=True, fontsize='medium')
	ax2.plot(Portfolio['Date'], Portfolio['Net'])
	plt.gcf().autofmt_xdate()
	legend = ax2.legend(loc='upper right', shadow=True, fontsize='medium')
	plt.show()



def plot_net(stocks,Data):
	Net = 0
	for ticker in  stocks.Tickers:
		Net += Data['Worth: '+ticker]
		plt.stackplot(Data['Date'], Data['Worth: '+ ticker])
		plt.gcf().autofmt_xdate()
	plt.legend(stocks.Tickers)
	plt.show()


def plot_stock(Data,stock):
	months = mdates.MonthLocator() 
	Moving_ = 0;
	Legends = pd.DataFrame({'Tickers':[]})
	Average1= 10
	Average2= 20

	Moving_10 = np.round(pd.rolling_mean(Data['Adj Close: '+ stock.Tickers],window=Average1),10)
	Moving_20 = np.round(pd.rolling_mean(Data['Adj Close: '+ stock.Tickers],window=Average2),20)
	#Moving_10.plot(grid=True)
	#Moving_20.plot(grid=True)
	plt.plot(Data.Date,Moving_10)
	plt.plot(Data.Date,Moving_20)
	Data['Adj Close: '+stock.Tickers].plot(grid=True)

	Legends.loc[len(Legends)] = stock.Tickers+": MA"+str(Average1)
	Legends.loc[len(Legends)] = stock.Tickers+": MA"+str(Average2)
	Legends.loc[len(Legends)] = stock.Tickers

	plt.legend(Legends.Tickers)
	#plt.gcf().autofmt_xdate()
	plt.xaxis.set_minor_locator(months)

	plt.show()





