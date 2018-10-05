import pandas as pd 
import pandas_datareader as web
import datetime
import numpy as np
from pandas import DataFrame
import csv
import matplotlib.pyplot as plt
import GetData
import portfolio_plot
pd.set_option('display.height', 1000)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


def 	Net(stocks,Stock_Data):
	Net_Worth = 0
	Net_Worth = 0
	
	
	
	for ticker in stocks.Tickers:
		Net_Worth = Net_Worth + Stock_Data['Worth: '+ ticker].iloc[-1]

	portfolio_plot.plot_net(stocks,Stock_Data)
	return Net_Worth

def Moving_Average(stocks,Stock_Data,Average):
	Moving_ = 0;
	Enter=False;
	Legends = pd.DataFrame({'Tickers':[]})

	for ticker in stocks.Tickers:
		Moving_ = np.round(pd.rolling_mean(Stock_Data['Adj Close: '+ticker],window=Average),2)
		if (Moving_.iloc[-1] > Stock_Data['Adj Close: '+ticker].iloc[-1]):
			Enter=True;
			Moving_.plot(grid=True)
			Stock_Data['Adj Close: '+ticker].plot(grid=True)
			Legends.loc[len(Legends)] = ticker+": MA"+str(Average)
			Legends.loc[len(Legends)] = ticker

	if Enter == True:
		plt.legend(Legends.Tickers)
		plt.show()
	else:
		print("\n NOTHING TO DO, ALL ABOVE MA"+str(Average)+"\n")

