import time
import requests
import config
import FPGA
from Strategies.movingaverage import Average
from Strategies.companydata import Company
from Strategies.fourcandle import Fourcandle
from Strategies.profitloss import Profitloss
from Strategies.twitter import Twitter

# For Raspberry Pi and Python 3.5.3

class Stock():
      def __init__(self, symbol, name):
            self.symbol = symbol
            self.name = name
            self.price = 0
            self.week52Low = 0
            self.mla = FPGA.MLA()

      def get_stock_data(self):
            url = "https://cloud.iexapis.com/beta/stock/" + self.symbol + "/quote?token=" + config.IEX_api_secret_key
            response = requests.request("GET", url, data=None, headers=None, params=None)
            return response.json()

      def buy(self):
            try:
                  kind = "market"
                  time_in_force = "gtc"
                  qty = "1"
                  payload = "{\n\t\"symbol\": \"" + self.symbol + "\",\n\t\"qty\": " + qty +\
                                    ",\n\t\"side\": \"buy\",\n\t\"type\": \"" + kind +\
                                    "\",\n\t\"time_in_force\": \"" + time_in_force + "\"\n}"
                  querystring = {"status":"all","direction":"desc"}
                  url = "https://paper-api.alpaca.markets/v2/orders"
                  headers = {'content-type': "application/json", 'apca-api-secret-key': config.alpaca_api_secret_key, 'apca-api-key-id': config.alpaca_api_key_id}
                  response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
            except: 
                  print("Failed to buy " + self.name)

      def sell(self):
            try:
                  url = "https://paper-api.alpaca.markets/v2/positions/" + self.symbol
                  headers = {'content-type': "application/json", 'apca-api-secret-key': config.alpaca_api_secret_key, 'apca-api-key-id': config.alpaca_api_key_id}
                  response = requests.request("GET", url, data=None, headers=headers, params=None)
                  positions = response.json()
            except:
                  print("Failed getting open positions for " + self.name)
            if 'qty' in positions:
                  try:
                        kind = "market"
                        time_in_force = "gtc"
                        qty = positions['qty']
                        payload = "{\n\t\"symbol\": \"" + self.symbol + "\",\n\t\"qty\": " + qty +\
                                          ",\n\t\"side\": \"sell\",\n\t\"type\": \"" + kind +\
                                          "\",\n\t\"time_in_force\": \"" + time_in_force + "\"\n}"
                        querystring = {"status":"all","direction":"desc"}
                        url = "https://paper-api.alpaca.markets/v2/orders"
                        headers = {'content-type': "application/json", 'apca-api-secret-key': config.alpaca_api_secret_key, 'apca-api-key-id': config.alpaca_api_key_id}
                        response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
                  except: 
                        print("Failed to sell " + self.name)
            else:
                  print("!!No Positions")

def init_stocks():
      Tesla = Stock("TSLA", "Telsa")
      Apple = Stock("AAPL", "Apple")
      Walmart = Stock("WMT", "Walmart")
      JNJ = Stock("JNJ", "Johnson & Johnson")
      Google = Stock("GOOG", "Google")
      Exxon = Stock("XOM", "Exxon")
      Microsoft = Stock("MSFT", "Microsoft")
      GE = Stock("GE", "General Electric")
      JPMorgan = Stock("JPM", "JPMorgan Chase")
      IBM = Stock("IBM", "IBM")
      Amazon = Stock("AMZN", "Amazon")
      return [Tesla, Apple, Walmart, JNJ, Google, Exxon, Microsoft, GE, JPMorgan, IBM, Amazon]

def markets_are_open():
      url = "https://paper-api.alpaca.markets/v2/clock"
      headers = {'content-type': "application/json", 'apca-api-secret-key': config.alpaca_api_secret_key, 'apca-api-key-id': config.alpaca_api_key_id}
      response = requests.request("GET", url, data=None, headers=headers, params=None)
      if response.json()['is_open']:
          return True
      else:
          return False

def have_open_orders():
      querystring = {"status":"open","direction":"desc"}
      payload = ""
      url = "https://paper-api.alpaca.markets/v2/orders"
      headers = {'content-type': "application/json", 'apca-api-secret-key': config.alpaca_api_secret_key, 'apca-api-key-id': config.alpaca_api_key_id}
      response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
      return response.json()

def sell_all_shares():
      try:
            while have_open_orders():
                  print("  Currently have open orders")
                  time.sleep(120)
      except:
            print("!!Finding Open Orders Failed")
      try:
            pass
      except:
            print("!!Failed Selling all shares")

def main():
      new_day = True
      purchases = list()
      stocks = init_stocks()
      while(1):
            while markets_are_open():
                  for stock in stocks:
                        print("     Gathering Stock Data")  #############################################
                        try:
                              response = stock.get_stock_data()
                              stock.price = float(response['latestPrice'])
                              stock.week52Low = float(response['week52Low'])
                        except: 
                              print("!!Gather Stock Data Failed for " + stock.name)

                        # Get News Sentiment.
                        if new_day:
                              temp = Company()
                              stock.mla.company_data = temp.get_news_sentiment(20, stock.name)

                        # Get Four Candles 
                        temp = Fourcandle()
                        stock.mla.four_data = temp.get_four_candle_hammer()

                        # Get Profit and Loss 
                        temp = Profitloss()
                        stock.mla.profit_data = temp.get_profit_loss(stock.symbol)

                        # Get Twitter Sentiment
                        temp = Twitter()
                        stock.mla.twitter_data = temp.get_twitter_sentiment(stock.name)

                        # Get Moving Average
                        temp = Average()
                        stock.mla.moving_data = temp.get_moving_avg(stock.symbol)

                        print("     Sending Data to MLA")#############################################
                        buy = stock.mla.decide_trade()

                        print("     Buying Recomendataions from MLA")#################################
                        try:
                              while have_open_orders():
                                    print("  Currently have open orders")
                                    time.sleep(120)
                        except:
                              print("!!Finding Open Orders Failed")
                        if buy:
                              stock.buy()
                              purchases.append({ "Stock" : stock, "Price" : stock.price, "News" : stock.mla.company_data, "Candles" : stock.mla.four_data, "P&L" : stock.mla.profit_data, "Twitter" : stock.mla.twitter_data, "Moving" : stock.mla.moving_data})
                              print("     Bought " + stock.name)
                        else: 
                              print("     Did Not Buy " + stock.name)
                              
                  # Delay for 1 minute
                  time.sleep(60)

                  print("     Adjusting MLA Weights")#############################################
                  for purchase in purchases:
                        try:
                              response = purchase["Stock"].get_stock_data()
                              current_price = float(response['latestPrice'])
                              if current_price > purchase["Price"]:
                                    print("   " + purchase["Stock"].mla.learn(purchase["News"], purchase["Candles"], purchase["P&L"], purchase["Twitter"], purchase["Moving"]))
                              else:
                                    if  purchase["News"] == 1:
                                          news = -1
                                    if purchase["Candles"] == 1:
                                          candles = -1
                                    if purchase["P&L"] == 1:
                                          pandl = -1
                                    if purchase["Twitter"] == 1:
                                          twitter = -1
                                    if purchase["Moving"] == 1:
                                          moving = -1
                                    print("   " + purchase["Stock"].mla.learn(news, candles, pandl, twitter, moving))

                        except:
                              print("!!Failure Adjusting Weights for " + purchase["Stock"].name)

                  print("     Selling All Stocks Previously Purchased")#################################
                  sell_all_shares()
                  purchases = list()
                  exit()
                  time.sleep(60)
                  new_day = False
                  
            
            print(" Markets are closed")
            # Delay for 15 minutes
            time.sleep(900)
            new_day = True

#main()
'''
tesla = Stock("TSLA", "Tesla")
temp = Company()
tesla.mla.company_data = temp.get_news_sentiment(20, tesla.name)
'''
stocks = init_stocks()
for stock in stocks:
      temp = Company()
      stock.mla.company_data = temp.get_news_sentiment(20, stock.name)
      print(stock.mla.company_data)
      print()












