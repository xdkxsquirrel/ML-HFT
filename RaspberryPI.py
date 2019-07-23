import time

class Stock():
    def __init__(self, symbol, name, price, week52Low):
        self.symbol = symbol
        self.name = name
        self.price = price
        self.week52Low = week52Low

def init_stocks():
      return [0,0,0,0,0,0,0,0]
'''
    try:
      IEX = 

      response = IEX.get("stock/TSLA/quote?token=" + IEX.key, None, None)
      Tesla = Stock("TSLA", "Telsa", float(response['latestPrice']), float(response['week52Low']))
      response = IEX.get("stock/AAPL/quote?token=" + IEX.key, None, None)
      Apple = Stock("AAPL", "Apple", float(response['latestPrice']), float(response['week52Low']))
      response = IEX.get("stock/WMT/quote?token=" + IEX.key, None, None)
      Walmart = Stock("WMT", "Walmart", float(response['latestPrice']), float(response['week52Low']))
      response = IEX.get("stock/JNJ/quote?token=" + IEX.key, None, None)
      JNJ = Stock("JNJ", "Johnson & Johnson", float(response['latestPrice']), float(response['week52Low']))
      response = IEX.get("stock/GOOG/quote?token=" + IEX.key, None, None)
      Google = Stock("GOOG", "Google", float(response['latestPrice']), float(response['week52Low']))
      response = IEX.get("stock/XOM/quote?token=" + IEX.key, None, None)
      Exxon = Stock("XOM", "Exxon", float(response['latestPrice']), float(response['week52Low']))
      response = IEX.get("stock/MSFT/quote?token=" + IEX.key, None, None)
      Microsoft = Stock("MSFT", "Microsoft", float(response['latestPrice']), float(response['week52Low']))
      response = IEX.get("stock/GE/quote?token=" + IEX.key, None, None)
      GE = Stock("GE", "General Electric", float(response['latestPrice']), float(response['week52Low']))
      response = IEX.get("stock/JPM/quote?token=" + IEX.key, None, None)
      JPMorgan = Stock("JPM", "JPMorgan Chase", float(response['latestPrice']), float(response['week52Low']))
      response = IEX.get("stock/IBM/quote?token=" + IEX.key, None, None)
      IBM = Stock("IBM", "IBM", float(response['latestPrice']), float(response['week52Low']))
      response = IEX.get("stock/AMZN/quote?token=" + IEX.key, None, None)
      Amazon = Stock("AMZN", "Amazon", float(response['latestPrice']), float(response['week52Low']))
      return [Tesla, Apple, Walmart, JNJ, Google, Exxon, Microsoft, GE, JPMorgan, IBM, Amazon]

    except:
            print("Error in init stocks")
'''

def main():
      stock_list = init_stocks()
      new_day = True
      while(1):            
            while new_day:
                  # Check if Markets are open
                  for stock in stock_list:
                        pass

# Gather Stock Data
# Get News Sentiment
# Get Four Candles
# Get Profit and Loss
# Get Twitter Sentiment
# Get Moving Average
# Send Data to MLA

# Delay for 5 minutes

# Adjust Weights

# Sell All Held Stocks
