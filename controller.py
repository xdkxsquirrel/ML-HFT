import time
import backend
import datetime
import requests
import numpy as np
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob

## Final Version For Raspberry Pi Python 3.5.3

#***************************TWITTER*************************************************************#
# this class will be used to gather sentiment on stock trades via twitter
class TwitterClient(object):

    def __init__(self):
        consumer_key = '9TxQyYHvAujwVOGNW5Di97lsL'
        consumer_secret = '3TX9wmny6Rt1KQ5zwfCbta7X1L1Zw7rJJiuV44rngVarupdQAt'
        access_token = '1103715647127613441-h28XoZXcKIOSxP18U2vnqlJNGqPNao'
        access_token_secret = 'dNtpJ5825K070HBSFOCnD3CayTgm5DmvZmHrWZw2DgYkS'

        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret)

            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(self.auth)

        except:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):

        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count):

        tweets = []

        try:
            # call twitter api to get tweets
            fetched_tweets = self.api.search(q=query, count=count)

            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}

                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

                # append parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

                    # return parsed tweets
            return tweets

        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))

        except:
              print("Unknown Error in Twitter")
#*********************************************************************************************************#

class Api():
    def __init__(self, url, headers, key):
        self.url = url 
        self.headers = headers
        self.key = key

    def get(self, request_url, payload, querystring):
        full_url = self.url + request_url
        headers = self.headers
        response = requests.request("GET", full_url, data=payload, headers=headers, params=querystring)
        return response.json()

    def post(self, request_url, payload, querystring):
        full_url = self.url + request_url
        headers = self.headers
        response = requests.request("POST", full_url, data=payload, headers=headers, params=querystring)
        return response.json()

    def postIndico(self, payload):
        headers = {
            'X-ApiKey': 'd6bb482f0d1165b6912b2816246b8ffb',
            }
        data = '{"data": "' + payload + '"}'
        response = requests.post('https://apiv2.indico.io/sentiment', headers=headers, data=data)
        return(response.json())

class Stock():
    def __init__(self, symbol, name, price, week52Low):
        self.symbol = symbol
        self.name = name
        self.price = price
        self.week52Low = week52Low
        self.news_sentiment = 0
        self.four_candle = 0
        self.profit_loss = 0
        self.twitter_sentiment = 0
        self.moving_avg = 0
        self.MLA = backend.MLA(25, 0, 25, 25, 25)
        self.sell = 0

    def set_news_sentiment(self, number_of_articles):
        try:
            indico = Api(None, None, None)
            news = Api("https://newsapi.org/v2/", None, "36fc08386f85499c93487f0c03efba50")
            sentiment_list = list()
            now = datetime.datetime.now()
            if(now.day!=1):
                  yesterday = str(now.year) + '-' + str(now.month) + '-' + str(now.day-1)
            else:
                  yesterday = str(now.year) + '-' + str(now.month-1) + '-0'
            newsfeed = news.get("everything?q=" + self.name + "&from=" + yesterday + "&to=" + yesterday + "&sortBy=popularity&language=en&apiKey=" + news.key, None, None)
            for i in newsfeed['articles']:
                  #Put URL into webscraper API then put into sentiment.
                  if(i['content']!=None):
                        data = re.sub('[^A-Za-z0-9 ]+', '', i['content'])
                        sentiment = indico.postIndico(data)
                        sentiment_list.append(float(sentiment['results']))
                  if np.average(sentiment_list) > .55:
                        self.news_sentiment = 1
                        self.MLA.company_data = 1
                  else:
                        self.news_sentiment = 0
                        self.MLA.company_data = 0
                  if( newsfeed['articles'].index(i) > number_of_articles):
                        break
        except:
            print("Error in News Sentiment")

    def set_four_candle(self):
        pass

    # not profit or loss for now, but seeing if revenue is increasing
    # which is a sign of a stable company
    def set_profit_loss(self):
        try:
            URLPE = "https://api.iextrading.com/1.0/stock/" + self.symbol + "/financials"
            rPE = requests.get(url = URLPE)
            data = rPE.json()
        except:
            print("IEX is down right now")
            self.profit_loss = 0
            self.MLA.profit_data = 0
            return

        if "financials" not in data:
            self.profit_loss = 0
            self.MLA.profit_data = 0
            return
        current = float(data[u'financials'][0]['totalRevenue'])
        twoQtrAgo = float(data[u'financials'][1]['totalRevenue'])
        threeQtrAgo = float(data[u'financials'][2]['totalRevenue'])

        if current > twoQtrAgo and twoQtrAgo > threeQtrAgo:
            self.profit_loss = 1
            self.MLA.profit_data = 1
        else:
            self.profit_loss = 0
            self.MLA.profit_data = 0

    def set_twitter_sentiment(self):
        api = TwitterClient()
        # Get 100 tweets of "__"
        tweets = api.get_tweets(query="exx", count=100)
        # positive tweets
        ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
        positive = 100 * len(ptweets) / len(tweets)
        # negative tweets
        ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
        negative = 100 * len(ptweets) / len(tweets)
        # neutral tweets
        neutral = 100 * (len(tweets) - len(ntweets) - len(ptweets)) / len(tweets)

        if (positive + neutral >= 80):
            self.twitter_sentiment = 1
            self.MLA.twitter_data = 1
        else:
            self.twitter_sentiment = 0
            self.MLA.twitter_data = 0

    def set_moving_avg(self):
        URL = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + self.symbol + "&apikey=WRV0ICYRFLQOX96V"
        r = requests.get(url = URL)
        data = r.json()
        count = total = 0
        if "Time Series (Daily)" not in data:
            self.moving_avg = 0
            self.MLA.moving_data = 0
            return
        for a in data["Time Series (Daily)"]:
            count = count + 1
            total = float(data["Time Series (Daily)"][a]["4. close"]) + total
        #print count, float(data["Time Series (Daily)"][a]["4. close"]),total
        movingAvg = total / 100
        dates = sorted(data["Time Series (Daily)"].keys(),  reverse=True)
        currentDate = dates[0]
        currnetPrice = float(data["Time Series (Daily)"][currentDate]["4. close"])
        tenDayTotal = 0
        for y in range(10):
            tenDayTotal= tenDayTotal + float(data["Time Series (Daily)"][dates[y]]["4. close"])
        tenDayAvg = tenDayTotal / 10
        fiveDayOldPrice = float(data["Time Series (Daily)"][dates[4]]["4. close"])

        if (currnetPrice < fiveDayOldPrice):
            # slope is moving down
            # we want to buy
            # TODO  we should actually see if the slope is down and we are within a small %
            # of touching the long term moving average
            if currnetPrice > movingAvg:
                self.moving_avg = 1
                self.MLA.moving_data = 1
        else:
            # slope is moving up
            # if slope is moving up and we already have bought it
            # lets hold it
            # if slope is moving up lets look for slope of last few days, if its comming down
            # lets sell it
            threeDayOldPrice = float(data["Time Series (Daily)"][dates[2]]["4. close"])
            if(currnetPrice < threeDayOldPrice):
                #sell it
                self.sell = 1
                self.moving_avg = 0
                self.MLA.moving_data = 0
            else:
                self.moving_avg = 0
                self.MLA.moving_data = 0

            # eventually we want to see if the the slope of the 10 day average is comming down
            # and the current price is within a few % of the long term moving average
            # that means we are buying on the way back down to the moving average which should be
            # acting as support line and possibly buying around lowest price in the cycle
            # the other side we'll want to keep track that it doesnt go too far below the long term avg
            # if it does then we will want to sell until we start averaging above again
            # if currnetPrice > movingAvg and tenDayAvg > movingAvg:
            #     print "buy it"

def init_stocks():
    try:
      IEX = Api("https://cloud.iexapis.com/beta/", None, "pk_11551eefe1bf4f0b81121b498c6a7651") #secret = sk_8df6ccfac04742f194e71f6140cf6944

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

def buy(alpaca, symbol, qty):
    kind = "market"
    time_in_force = "gtc"
    payload = "{\n\t\"symbol\": \"" + symbol + "\",\n\t\"qty\": " + qty +\
            ",\n\t\"side\": \"buy\",\n\t\"type\": \"" + kind +\
            "\",\n\t\"time_in_force\": \"" + time_in_force + "\"\n}"
    querystring = {"status":"all","direction":"desc"}
    return alpaca.post("orders", payload, querystring)

def sell(alpaca, symbol, qty):
    kind = "market"
    time_in_force = "gtc"
    payload = "{\n\t\"symbol\": \"" + symbol + "\",\n\t\"qty\": " + qty +\
            ",\n\t\"side\": \"sell\",\n\t\"type\": \"" + kind +\
            "\",\n\t\"time_in_force\": \"" + time_in_force + "\"\n}"
    querystring = {"status":"all","direction":"desc"}
    return alpaca.post("orders", payload, querystring)

def list_all_open_orders(alpaca):
    querystring = {"status":"open","direction":"desc"}
    payload = ""
    return alpaca.get("orders", payload, querystring)

def get_current_price(stock):
    IEX = Api("https://cloud.iexapis.com/beta/", None, "pk_11551eefe1bf4f0b81121b498c6a7651")
    response = IEX.get("stock/" + stock.symbol + "/quote?token=" + IEX.key, None, None)
    stock.price = float(response['latestPrice'])
    return stock.price

def get_an_open_position(alpaca, symbol):
    payload = ""
    querystring = ""
    return alpaca.get("positions/" + symbol, payload, querystring)

def main():
    new_day = True
    alpaca = Api("https://paper-api.alpaca.markets/v1/", {
    'content-type': "application/json",
    'apca-api-secret-key': "fRPyMcc4OootRhgez/W0HLPAv1IXbD/E6OaAzJTo",
    'apca-api-key-id': "PK6WI3ROFW19GXBRAQ4O"
    }, "fRPyMcc4OootRhgez/W0HLPAv1IXbD/E6OaAzJTo")

    stock_list = init_stocks()

    while True:
        clock = alpaca.get("clock", None, None)
        if clock['is_open']:
            for stock in stock_list:
                  print("Processing: {}".format(stock.name))
                  if new_day:
                        print("News Sentiment")
                        stock.set_news_sentiment(10)
                  print("Setting Moving Average")
                  stock.set_moving_avg()
                  print("Setting Profit Loss")
                  stock.set_profit_loss()
                  print("Twitter Sentiment")
                  stock.set_twitter_sentiment()
                  time.sleep(60)
            if new_day:
                  new_day = False
                  
            open_orders = list_all_open_orders(alpaca)
            if len(open_orders) == 0 :     
                for stock in stock_list:
                    position = get_an_open_position(alpaca, stock.symbol)                    
                    trade = stock.MLA.decide_trade()
                    if trade > 1:
                        buy(alpaca, stock.symbol, "10")
                        print("Bought {} for {} at qty: 10".format(stock.name, str(stock.price)))
                    elif trade == 1:
                        buy(alpaca, stock.symbol, "1")
                        print("Bought {} for {} at qty: 1".format(stock.name, str(stock.price)))
                    else:
                        print("Do not buy {}".format(stock.name))
                    print('')
                    time.sleep(10)
                time.sleep(60)
                
                open_orders = list_all_open_orders(alpaca)
                print("")
                print("Sell Stuff")
                while len(open_orders) is not 0 : 
                    open_orders = list_all_open_orders(alpaca)
                    print('waiting....')
                    time.sleep(10)
                for stock in stock_list:
                    position = get_an_open_position(alpaca, stock.symbol)
                    if 'qty' in position:
                        if stock.sell == 1 or (float(position['current_price']) - float(position['avg_entry_price']) > 2.5):
                            print("Sold all {} for {}".format(stock.name, str(position['current_price'])))
                            sell(alpaca, stock.symbol, position['qty'])
                        else:
                            print("Do not Sell: {}".format(stock.name))
                    else:
                        print('No positions')
                
                time.sleep(60)

        else:
            print('Markets are closed')
            new_day = True
            time.sleep(60)


main()