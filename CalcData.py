###################################################################
# Version 1.0 30 October 2018
# Author: Fredrik Gunnarsson, fredrikgunnarsson@outlook.com
###################################################################
# Calculates metrics for the portfolio program
###################################################################

# Debugging with: 	import pdb; pdb.set_trace()
# c=cont; s=step; r=return; l=list; n=next; b=break; args= arguments


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
# Data = csv file:		 with portfolio data
# _vec_derivative: 		 vector with tickers and information
# ticker: 				 single ticker for a stock or derivative


#Calculates net worth of portfolio
def Net(Data,_vec_derivative):
	Net_Worth = 0
	for ticker in _vec_derivative.Tickers:
		Net_Worth = Net_Worth + Data['Worth: '+ ticker].iloc[-1]
	return Net_Worth

#Calculates moving average and check if it's below 
def Moving_Average(Data,_vec_derivative):
	global Average
	Moving_ = 0;
	Enter = False;
	Legends = pd.DataFrame({'Tickers':[]})
	i=0
	for ticker in _vec_derivative.Tickers:
		Moving_ = np.round(Data['Adj Close: '+ticker].rolling(window = Average,center = False).mean(),2)
		
		if (Moving_.iloc[-1] > Data['Adj Close: '+ticker].iloc[-1]):
			portfolio_plot.plot_stock(Data,_vec_derivative.iloc[i])
			Enter = True
		i=i+1

	if Enter == False:
		print("\n NOTHING TO DO, ALL ABOVE MA"+str(Average)+"\n")

#Computes RSI data
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

# computes the volatility 
def computeVol(Data,x):
    log_returns = np.log(Data) - np.log(Data.shift(1))
    vol = log_returns.rolling(window = x,center=False).std() * np.sqrt(x)
    return vol

# Calculates risk for single derivative, VaR and std
def ComputeRisk(Data_i):
	global VaR_Parameter
	Return = Data_i.pct_change()
	Deviation = Return.std()
	Percentile = np.percentile(Return.dropna(), VaR_Parameter)
	return Deviation, Percentile

# Calculates and tabulates riskiest derivative and returns risk data  
def Portfolio_RiskStats(Data,_vec_derivative):
	Data_Risk = pd.DataFrame()
	for i in range(0,len(_vec_derivative)):
		std,VaR  = ComputeRisk(Data['Adj Close: '+ _vec_derivative.Tickers.iloc[i]])
		Data_Risk.at[_vec_derivative.Tickers.iloc[i],'VaR']=VaR
		Data_Risk.at[_vec_derivative.Tickers.iloc[i],'std']=std
	return Data_Risk

#Calculates the Portfolio risk as a variance with covariance and variance
def Portfolio_Risk(Data,_vec_derivative):
	Net_Worth = Net(Data,_vec_derivative)
	weights = []
	Stock_Beta = []

	log_returns = pd.DataFrame()
	Index_Return =pd.DataFrame()
	#Beta Calculation
	Index_Data = GetData.Index_Data()
	Index_Return = np.log(Index_Data / Index_Data.shift(1))
	Index_Variance = Index_Return.var()[0]
	
	# Perform Bootstrap to get the variance of the risk???
	for ticker in _vec_derivative["Tickers"]:
		log_returns[ticker] = np.log(Data['Adj Close: '+ticker] / Data['Adj Close: '+ticker].shift(1))
		weights.append(Data['Worth: '+ticker].iloc[-1]/Net_Worth)
		Index_Return=Index_Return.fillna(0)
		log_returns=log_returns.fillna(0)
		X = np.stack((Index_Return['Adj Close: ^OMX'],log_returns[ticker]), axis=0)
		Stock_Beta.append(np.cov(X)[0][1]/Index_Variance)

	Cov_Data = log_returns.cov()
	Risk = np.dot(weights,np.dot(Cov_Data,weights))	
	Beta = np.dot(Stock_Beta,weights)

	return (Risk, Beta)











