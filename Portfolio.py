###################################################################
# Version 1.0:  30 October 2018
# Author: Fredrik Gunnarsson, fredrikgunnarsson@outlook.com
###################################################################
# Portfolio Manager: Helps to identify risk, correlation etc
# 					f or your portfolio
###################################################################
# Need csv file with stock data
# Need _init_portfolio that contains all info about portfolio
###################################################################


import pandas as pd 
from pandas import DataFrame
import GetData
import CalcData
import portfolio_plot
pd.set_option('display.height', 1000)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


# Data = File with all derivative data
class _init_():
	Portfolio = pd.DataFrame({'Tickers': ["SAND.ST","SEB-A.ST","SEK","EUR","BTC-USD"],'Amount':[250,200,50000,10000,0.5]})
	stocks = pd.DataFrame({'Tickers': ["SAND.ST","SEB-A.ST"], 'Amount':[250,200]})
	cash   = pd.DataFrame({'Tickers': ["SEK","EUR"], 'Amount':[50000,10000]})
	crypto = pd.DataFrame({'Tickers': ["BTC-USD"], 'Amount':[1]})


def main():
	_init_Portfolio = pd.DataFrame({'Tickers': ["SAND.ST","SEB-A.ST","SEK","EUR","BCHARTS/KRAKENUSD"],'Amount':[250,200,50000,10000,1] ,'Type':["Stock","Stock","Cash","Cash","Crypto"]})
	output = 1 

	while (output != "0"):
		print("\n\nWELCOME TO YOUR PORTFOLIO MANAGER!\n")
		print ("Choose one of the following, exit with 0:")
		print ("1. Update stock-data in csv file")
		print("2. Calculate Net Worth \n3. Plot propagation of Stocks\n4. Plot propagation of portfolio\n5. Check stocks below MA200\n6. Look at single stock")
		output = input()

		if (output == "6"):
			print("Choose one of")
			print(_init_Portfolio) 
			output2 = input()
		
		if (output == "1"): 
			File = GetData.Load_Data(_init_Portfolio)
		elif output == "2": 
			Data = pd.read_csv('Stock_Data.csv', encoding='utf-8',parse_dates=True)
			Net_Worth = CalcData.Net(Data,_init_Portfolio)
			GetData.printMoney(Net_Worth)
		elif output == "3":
			Data = pd.read_csv('Stock_Data.csv', encoding='utf-8',parse_dates=True)
			portfolio_plot.plot_stocks(Data,_init_Portfolio[(_init_Portfolio['Type']=='Stock')])
		elif output == "4":
			Data = pd.read_csv('Stock_Data.csv', encoding='utf-8',parse_dates=True)
			portfolio_plot.plot_stocks(Data,_init_Portfolio)
		elif output == "5":
			Data = pd.read_csv('Stock_Data.csv', encoding='utf-8',parse_dates=True)
			CalcData.Moving_Average(Data,_init_Portfolio[(_init_Portfolio['Type']=='Stock')])
		elif output == "6":
			Data = pd.read_csv('Stock_Data.csv', encoding='utf-8',parse_dates=True)
			portfolio_plot.plot_stock(Data, _init_Portfolio,int(output2))
			CalcData.computeRisk(Data,_init_Portfolio,int(output2))

if __name__== "__main__":
  main()













