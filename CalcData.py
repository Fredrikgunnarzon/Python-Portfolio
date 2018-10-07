import pandas as pd 
import numpy as np
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

def Moving_Average(Stock_Data,stocks):
	Moving_ = 0;
	Average=14
	Enter=False;
	Legends = pd.DataFrame({'Tickers':[]})
	i=0
	for ticker in stocks.Tickers:
		Moving_ = np.round(pd.rolling_mean(Stock_Data['Adj Close: '+ticker],window=Average),2)
		if (Moving_.iloc[-1] > Stock_Data['Adj Close: '+ticker].iloc[-1]):
			portfolio_plot.plot_stock(Stock_Data,stocks.iloc[i])
			Enter = True
		i=i+1

	if Enter == False:
		print("\n NOTHING TO DO, ALL ABOVE MA"+str(Average)+"\n")

def rsi(prices, n = 14):

    deltas = np.diff(prices)
    seed = deltas[:n+1]
    up = seed[seed >= 0].sum()/n
    down = -seed[seed < 0].sum()/n
    rs = up/down
    rsi = np.zeros_like(prices)
    rsi[:n] = 100. - 100./(1. + rs)

    for i in range(n, len(prices)):
        delta = deltas[i - 1]  # cause the diff is 1 shorter

        if delta > 0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta

        up = (up*(n - 1) + upval)/n
        down = (down*(n - 1) + downval)/n

        rs = up/down
        rsi[i] = 100. - 100./(1. + rs)

    return rsi

def movingaverage(values,window):
    weigths = np.repeat(1.0, window)/window
    smas = np.convolve(values, weigths, 'valid')
    return smas


def ExpMovingAverage(values, window):
    weights = np.exp(np.linspace(-1., 0., window))
    weights /= weights.sum()
    a =  np.convolve(values, weights, mode='full')[:len(values)]
    a[:window] = a[window]
    return a


def computeMACD(x, slow = 26, fast = 12):
    emaslow = ExpMovingAverage(x, slow)
    emafast = ExpMovingAverage(x, fast)
    return emaslow, emafast, emafast - emaslow