import pandas as pd 
import numpy as np
import GetData
import portfolio_plot
pd.set_option('display.height', 1000)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
Average = 14
VaR_Parameter=95




# Data = csv file with portfolio data
#_vec_derivative = vector with tickers and information
def Net(Data,_vec_derivative):
	Net_Worth = 0
	for ticker in _vec_derivative.Tickers:
		Net_Worth = Net_Worth + Data['Worth: '+ ticker].iloc[-1]
	portfolio_plot.plot_net(_vec_derivative,Data)
	return Net_Worth

def Moving_Average(Data,_vec_derivative):
	global Average
	Moving_ = 0;
	Enter = False;
	Legends = pd.DataFrame({'Tickers':[]})
	i=0
	for ticker in _vec_derivative.Tickers:
		#Moving_ = np.round(pd.rolling_mean(Data['Adj Close: '+ticker],window=Average),2)
		Moving_ = np.round(Data['Adj Close: '+ticker].rolling(window = Average,center=False).mean(),2)
		
		if (Moving_.iloc[-1] > Data['Adj Close: '+ticker].iloc[-1]):
			portfolio_plot.plot_stock(Data,_vec_derivative.iloc[i])
			Enter = True
		i=i+1

	if Enter == False:
		print("\n NOTHING TO DO, ALL ABOVE MA"+str(Average)+"\n")


def rsi(Data_i, n = 14):
    deltas = np.diff(Data_i)
    seed = deltas[:n+1]
    up = seed[seed >= 0].sum()/n
    down = -seed[seed < 0].sum()/n
    rs = up/down
    rsi = np.zeros_like(Data_i)
    rsi[:n] = 100. - 100./(1. + rs)

    for i in range(n, len(Data_i)):
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

def movingaverage(Data_i,window):
    weigths = np.repeat(1.0, window)/window
    smas = np.convolve(Data_i, weigths, 'valid')
    return smas


def ExpMovingAverage(Data_i, window):
    weights = np.exp(np.linspace(-1., 0., window))
    weights /= weights.sum()
    a =  np.convolve(Data_i, weights, mode='full')[:len(Data_i)]
    a[:window] = a[window]
    return a

def computeMACD(Data_i, slow = 26, fast = 12):
    emaslow = ExpMovingAverage(Data_i, slow)
    emafast = ExpMovingAverage(Data_i, fast)
    return emaslow, emafast, emafast - emaslow


def computeVol(Data,x):
    log_returns = np.log(Data) - np.log(Data.shift(1))
    #vol = pd.rolling_std(log_returns, window=x) * np.sqrt(x)
    vol = log_returns.rolling(window = x,center=False).std() * np.sqrt(x)
    return vol

def computeRisk(Data,stock,i):
	global VaR_Parameter
	Data_i = Data['Adj Close: '+ stock.Tickers.iloc[i]]
	Return = Data_i.pct_change()
	Deviation = Return.std()
	percentile = np.percentile(Return.dropna(), VaR_Parameter)
	return Deviation, percentile 









