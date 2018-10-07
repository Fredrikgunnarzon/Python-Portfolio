import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np
import matplotlib as mpl
import matplotlib.dates as mdates
import CalcData

pd.set_option('display.height', 1000)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
mpl.style.use('seaborn')

def plot_stocks(Data,stocks):
	fig, (ax1, ax2,ax3) = plt.subplots(3,1,figsize=(15, 8), gridspec_kw = {'height_ratios':[1, 1,3]})
	Portfolio=pd.DataFrame()
	Portfolio['Date'] = pd.to_datetime(Data.Date, format='%Y-%m-%d')
	dates = mdates.date2num(Portfolio['Date'])
	Portfolio['Net'] = 0
	Amount=[]
	Tickers_Daily =stocks[(stocks['Type']==('Stock'))|(stocks['Type']==('Crypto'))]
	for ticker in stocks["Tickers"]:
		Portfolio['Net'] += Data['Worth: '+ticker]
		if(any(Tickers_Daily.Tickers == ticker)):
			ax3.plot_date(dates, Data['Adj Close: '+ticker]/Data['Adj Close: '+ticker][1],label=[ticker],fmt='-')		
		Amount.append(Data['Worth: '+ticker][30])
	x = np.arange(len(Amount))
	ax1.bar(x,height=Amount)
	plt.sca(ax1)
	plt.xticks(x, stocks.Tickers)
	ax3.legend(loc='upper right',shadow=True, fontsize='medium')
	ax2.plot_date(dates,Portfolio['Net'],fmt='-')
	ax2.legend(loc='upper right', shadow=True, fontsize='medium')
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
	Moving_ = 0;
	Legends = pd.DataFrame({'Tickers':[]})
	Average1= 10
	Average2= 20
	Moving_10 = np.round(pd.rolling_mean(Data['Adj Close: '+ stock.Tickers],window=Average1),10)
	Moving_20 = np.round(pd.rolling_mean(Data['Adj Close: '+ stock.Tickers],window=Average2),20)
	dates2 = pd.to_datetime(Data.Date, format='%Y-%m-%d')
	dates = mdates.date2num(dates2)
	left, width = 0.1, 0.8
	axescolor = '#f6f6f6'

	fig, (ax1, ax2) = plt.subplots(2,1,figsize=(15, 8), gridspec_kw = {'height_ratios':[1, 3]},sharex=True)

	rsi = CalcData.rsi(Data["Adj Close: "+stock.Tickers])
	ax2.plot_date(dates,Moving_10,fmt='--')
	ax2.plot_date(dates,Moving_20,fmt='--')
	ax2.plot_date(dates,Data['Adj Close: '+stock.Tickers],fmt='-')


	ax1.plot_date(dates,rsi,fmt='-')
	ax1.axhline(70, color='salmon',linestyle='--')
	ax1.axhline(30, color='green',linestyle='--')
	ax1.text(0.6, 0.9, '>70 = overbought', va='top', transform=ax1.transAxes, fontsize=9)
	ax1.text(0.6, 0.1, '<30 = oversold', transform=ax1.transAxes, fontsize=9)
	ax1.set_ylim(0, 100)
	ax1.set_yticks([30, 70])
	ax1.text(0.025, 0.95, 'RSI (14)', va='top', transform=ax1.transAxes, fontsize=9)
	ax1.set_title('%s daily' % stock.Tickers)
	Legends.loc[len(Legends)] = stock.Tickers+": MA"+str(Average1)
	Legends.loc[len(Legends)] = stock.Tickers+": MA"+str(Average2)
	Legends.loc[len(Legends)] = stock.Tickers
	ax2.legend(Legends.Tickers)

	fig.autofmt_xdate()
	plt.show()




