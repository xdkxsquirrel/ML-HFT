import requests
import config
import math
from pyti.stochrsi import stochrsi

# based on closing prices so need to clean data for closing price

def rsi(symbol):
	URL = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + symbol + "&apikey=" + config.alphaadvantage_api_key_id
	r = requests.get(url = URL)
	data = r.json()
	days = data["Time Series (Daily)"]
	closingPrices = []
	for day in days:
		closingPrices.append(float(days[day]['4. close']))


	cleanedData = []
	# print (closingPrices)
	srsi = stochrsi(closingPrices, 28)
	for dataPoint in srsi:
		if(math.isnan(dataPoint) == False ):
			cleanedData.append(dataPoint)



	#above 70 buy no matter what
	if (cleanedData[0] > 60):
	 	return 1

	if(cleanedData[0] <= 40):
		return 0

	#above 30 buy if on upward trend for last 3
	if (cleanedData[0] > 40):
		if(cleanedData[0] > cleanedData[1]):
			return 1

	# if its not in buy range or above sell range and on upper trajectory we should sell

	return 0

