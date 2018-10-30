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






def plot_stock(Data,stock,i):
	Legends 	= pd.DataFrame({'Tickers':[]})
	Average1 	= 10
	Average2 	= 20
	Moving_10 	= np.round(Data['Adj Close: '+stock.Tickers.iloc[i]].rolling(window = Average1,center=False).mean(),10)
	Moving_20 	= np.round(Data['Adj Close: '+stock.Tickers.iloc[i]].rolling(window = Average2,center=False).mean(),20)
	vol 		= CalcData.computeVol(Data["Adj Close: "+stock.Tickers.iloc[i]],10)
	log_returns = np.log(Data['Adj Close: '+stock.Tickers.iloc[i]] / Data['Adj Close: '+stock.Tickers.iloc[i]].shift(1))

	percentile = np.percentile(log_returns.dropna(), 95)
	rsi 		= CalcData.rsi(Data["Adj Close: "+stock.Tickers.iloc[i]])
	dates 		= mdates.date2num(pd.to_datetime(Data.Date, format='%Y-%m-%d'))

	fig, ((ax4, ax1),(ax5,ax2)) = plt.subplots(2,2,figsize=(15, 8), gridspec_kw = {'width_ratios':[1,2],'height_ratios':[1, 3]})

	ax2.plot_date(dates,Moving_10,fmt='--')
	ax2.plot_date(dates,Moving_20,fmt='--')
	ax2.plot_date(dates,Data['Adj Close: '+stock.Tickers.iloc[i]],fmt='-')
	ax2.set_ylabel('Price')

	ax3 = ax2.twinx()
	ax3.plot_date(dates,vol,fmt='-')
	ax3.legend('Volatility',loc='upper right')
	ax3.set_ylabel('Volatility')
	ax3.grid('False')
	ax3.xaxis.set_tick_params(rotation=45)
	Legends.loc[len(Legends)] = stock.Tickers.iloc[i]+": MA"+str(Average1)
	Legends.loc[len(Legends)] = stock.Tickers.iloc[i]+": MA"+str(Average2)
	Legends.loc[len(Legends)] = stock.Tickers.iloc[i]
	ax2.legend(Legends.Tickers)
	ax2.xaxis.set_tick_params(rotation=45)

	ax4.hist(log_returns.dropna(),30)
	ax4.legend(["VAR 95 quantile:"+str(round(percentile,3))])

	stock=stock[(stock['Type']=='Stock')]
	for ticker in stock.Tickers:
		mean5 = np.round(Data['Adj Close: '+ticker].rolling(window = 5,center=False).mean(),5)
		ax5.plot_date(dates, mean5/mean5.iloc[6],'-')
	ax5.legend(stock.Tickers)
	ax5.xaxis.set_tick_params(rotation=45)	


	ax1.plot_date(dates,rsi,fmt='-')
	ax1.axhline(70, color='salmon',linestyle='--')
	ax1.axhline(30, color='green',linestyle='--')
	ax1.text(0.6, 0.9, '>70 = overbought', va='top', transform=ax1.transAxes, fontsize=9)
	ax1.text(0.6, 0.1, '<30 = oversold', transform=ax1.transAxes, fontsize=9)
	ax1.set_ylim(0, 100)
	ax1.set_yticks([30, 70])
	ax1.text(0.025, 0.95, 'RSI (14)', va='top', transform=ax1.transAxes, fontsize=9)
	ax1.set_title('%s daily' % stock.Tickers.iloc[i])
	ax1.get_shared_x_axes().join(ax1, ax2)

	plt.show()




