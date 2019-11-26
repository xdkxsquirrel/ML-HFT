import requests
import config
import math
from pyti.bollinger_bands import upper_bollinger_band
from pyti.bollinger_bands import lower_bollinger_band


def bollinger(symbol):
	URL = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + symbol + "&apikey=" + config.alphaadvantage_api_key_id
	r = requests.get(url = URL)
	data = r.json()
	days = data["Time Series (Daily)"]
	closingPrices = []
	for day in days:
		closingPrices.append(float(days[day]['4. close']))


	cleanedData = []
	period = 2


	upperbands = upper_bollinger_band(closingPrices, 20)
	lowerBands = lower_bollinger_band(closingPrices, 20)

	ub = []
	lb = []

	for upper in upperbands:
		if(math.isnan(upper) == False ):
			ub.append(upper)

	for lower in lowerBands:
		if(math.isnan(lower) == False ):
			lb.append(lower)



	# if current price is greater than upper bound sell
	if(closingPrices[0] >= ub[0]):
			return (1)

	# if current price is lower than lower bound buy
	if(closingPrices[0] <= lb[0]):
			return 1

	# if within 2% of upperband band then sell
	if( (1 - (closingPrices[0] / ub[0]))*100 <= 2 ):
		return 0

	# if within 2% of lower band buy
	if( (1 - (lb[0] / closingPrices[0]))*100 <= 2  ):
		return 0

	# if inside middle range look for trajectory up or down
	if(closingPrices[0] > closingPrices[2]):
		return 1
	else:
		return 0
	# if down, sell, if up buy



