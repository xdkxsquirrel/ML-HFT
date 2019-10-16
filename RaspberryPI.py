import time as tm
import requests
import config
import FPGA
import datetime as dt
from Strategies.movingaverage import Average
from Strategies.companydata import Company
from Strategies.fourcandle import Fourcandle
from Strategies.profitloss import Profitloss
from Strategies.twitter import Twitter

# For Raspberry Pi and Python 3.5.3

class Stock():
      def __init__(self, symbol, name, weights):
            self.symbol = symbol
            self.name = name
            self.price = 0
            self.week52Low = 0
            self.mla = FPGA.MLA(weights[0], weights[1], weights[2], weights[3], weights[4])
            self.currentQtr = 0
            self.twoQtrAgo = 0
            self.threeQtrAgo = 0

      def get_stock_data(self):
            try:
                  url = "https://cloud.iexapis.com/beta/stock/" + self.symbol + "/quote?token=" + config.IEX_api_secret_key
                  response = requests.request("GET", url, data=None, headers=None, params=None)
                  return response.json()
            except:
                  print("Failed getting stock data for " + self.name)

      def buy(self):
            try:
                  kind = "market"
                  time_in_force = "gtc"
                  qty = "25"
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

def get_weights(ticker):
      try:
            query = "query{\n  MostRecentWeight(ticker: \"" + ticker + "\") {\n    twitterWeight\n    movingWeight\n fourWeight\n    profitWeight\n    companyWeight\n    date\n  }\n}"
            result = run_query(query)
            twitterWeight = int(result['data']['MostRecentWeight']['twitterWeight'])
            movingWeight = int(result['data']['MostRecentWeight']['movingWeight'])
            fourWeight = int(result['data']['MostRecentWeight']['fourWeight'])
            profitWeight = int(result['data']['MostRecentWeight']['profitWeight'])
            companyWeight = int(result['data']['MostRecentWeight']['companyWeight'])
            print("Weights: " + str(twitterWeight) + " " + str(movingWeight) + " " + str(fourWeight) + " " + str(profitWeight) + " " + str(companyWeight))
            return [companyWeight, fourWeight, profitWeight, twitterWeight, movingWeight]
      except: 
            print("!!Failed to load Weights")
            return None


def init_stocks():
      Tesla = Stock("TSLA", "Telsa", get_weights("TSLA"))
      Apple = Stock("AAPL", "Apple", get_weights("AAPL"))
      Walmart = Stock("WMT", "Walmart", get_weights("WMT"))
      JNJ = Stock("JNJ", "Johnson & Johnson", get_weights("JNJ"))
      Google = Stock("GOOG", "Google", get_weights("GOOG"))
      Exxon = Stock("XOM", "Exxon", get_weights("XOM"))
      Microsoft = Stock("MSFT", "Microsoft", get_weights("MSFT"))
      GE = Stock("GE", "General Electric", get_weights("GE"))
      JPMorgan = Stock("JPM", "JPMorgan Chase", get_weights("JPM"))
      IBM = Stock("IBM", "IBM", get_weights("IBM"))
      Amazon = Stock("AMZN", "Amazon", get_weights("AMZN"))
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
                  tm.sleep(120)

      except:
            print("!!Finding Open Orders Failed")
      try:
            url = "https://paper-api.alpaca.markets/v2/positions"
            headers = {'content-type': "application/json", 'apca-api-secret-key': config.alpaca_api_secret_key, 'apca-api-key-id': config.alpaca_api_key_id}
            response = requests.request("GET", url, data=None, headers=headers, params=None)
            positions = response.json()
            for position in positions:
                  kind = "market"
                  time_in_force = "gtc"
                  qty = position['qty']
                  payload = "{\n\t\"symbol\": \"" + position['symbol'] + "\",\n\t\"qty\": " + qty +\
                                          ",\n\t\"side\": \"sell\",\n\t\"type\": \"" + kind +\
                                          "\",\n\t\"time_in_force\": \"" + time_in_force + "\"\n}"
                  querystring = {"status":"all","direction":"desc"}
                  url = "https://paper-api.alpaca.markets/v2/orders"
                  headers = {'content-type': "application/json", 'apca-api-secret-key': config.alpaca_api_secret_key, 'apca-api-key-id': config.alpaca_api_key_id}
                  response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
      except:
            print("!!Failed Selling all shares")


def run_query(query): 
      try:
            request = requests.post('https://seniorprojectu.herokuapp.com/graphql', json={'query': query}, headers=None)
            if request.status_code == 200:
                  return request.json()
            else:
                  print("!Weights Capture failed to run by returning code of {}. {}".format(request.status_code, query))
      except: 
            print("!Weights Capture failed to run by returning code of {}. {}".format(request.status_code, query))

def main():
      #graphQL_headers = {"Authorization": "Bearer " + config.GraphQL_api_key}
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

                        # Get News Sentiment
                        if new_day:
                              temp = Company()
                              stock.mla.company_data = temp.get_news_sentiment(20, stock.name)

                        # Get Four Candles 
                        try:
                              temp = Fourcandle()
                              stock.mla.four_data = temp.get_four_candle_hammer(stock.symbol)
                              print("Four Candle: " + str(stock.mla.four_data))

                        except Exception as e:
                              print("!!Four Candle Hammer Failed for " + stock.name + " because " + str(e))

                        # Get Profit and Loss 
                        if new_day:
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
                        if buy:
                              try:
                                    while have_open_orders():
                                          print("  Currently have open orders")
                                          tm.sleep(120)
                              except:
                                    print("!!Finding Open Orders Failed")

                              stock.buy()
                              purchases.append({ "Stock" : stock, "Price" : stock.price, "News" : stock.mla.company_data, "Candles" : stock.mla.four_data, "P&L" : stock.mla.profit_data, "Twitter" : stock.mla.twitter_data, "Moving" : stock.mla.moving_data})
                              print("     Bought " + stock.name + " " + str(stock.mla.company_data) + str(stock.mla.four_data) + str(stock.mla.profit_data) + str(stock.mla.twitter_data) + str(stock.mla.moving_data))
                        else: 
                              print("     Did Not Buy " + stock.name + " " + str(stock.mla.company_data) + str(stock.mla.four_data) + str(stock.mla.profit_data) + str(stock.mla.twitter_data) + str(stock.mla.moving_data))
                        print()      
                              
                  # Delay for 5 minutes
                  tm.sleep(300)

                  print("     Adjusting MLA Weights")#############################################
                  for purchase in purchases:
                        try:
                              news = purchase["News"]
                              candles = purchase["Candles"]
                              twitter = purchase["P&L"]
                              moving = purchase["Twitter"]
                              pandl = purchase["Moving"]
                              response = purchase["Stock"].get_stock_data()
                              current_price = float(response['latestPrice'])
                              if current_price < float(purchase["Price"]):                                    
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
                              
                              cw, fw, pw, tw, mw = purchase["Stock"].mla.learn(news, candles, pandl, twitter, moving)
                              time = dt.datetime.utcnow()
                              query = "mutation { insertWeight(record:{ ticker: \"" + str(purchase["Stock"].symbol) +\
                                    "\", twitterWeight:" + str(tw) + ", fourWeight:" + str(fw) + ", movingWeight:" + str(mw) +\
                                    ", companyWeight:" + str(cw) + ", profitWeight:" + str(pw) + ", date: \"" +\
                                    time.strftime("%Y-%m-%dT%H:%M:%S.000Z") + "\" }){ record { date } } } "
                              result = run_query(query)

                        except Exception as e:
                              print(e)
                              print("!!Failure Adjusting Weights for " + purchase["Stock"].name)

                  print("     Selling All Stocks Previously Purchased")#################################
                  print( )
                  sell_all_shares()
                  purchases = list()
                  tm.sleep(60)
                  new_day = False
                  
            
            print(" Markets are closed")
            # Delay for 15 minutes
            tm.sleep(900)
            new_day = True

main()