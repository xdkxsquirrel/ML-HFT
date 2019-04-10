import time
import backend
import indicoio
import datetime
import requests
import numpy as np
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob


#***************************TWITTER SHIT*************************************************************#
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

    def set_news_sentiment(self, number_of_articles):
        indicoio.config.api_key = 'df08c40de1d01d2b3c8c3fc75f21ab81'
        news = Api("https://newsapi.org/v2/", None, "36fc08386f85499c93487f0c03efba50")
        sentiment_list = list()
        now = datetime.datetime.now()
        if (now.day != 1):
            yesterday = str(now.year) + '-' + str(now.month) + '-' + str(now.day - 1)
        else:
            yesterday = str(now.year) + '-' + str(now.month - 1) + '-0'
        newsfeed = news.get(
            "everything?q=" + self.name + "&from=" + yesterday + "&to=" + yesterday + "&sortBy=popularity&language=en&apiKey=" + news.key,
            None, None)
        for i in newsfeed['articles']:
            # Put URL into webscraper API then put into sentiment.
            # print(i['content'])
            if (i['content'] != None):
                sentiment = indicoio.sentiment(i['content'])
                sentiment_list.append(float(sentiment))
                self.news_sentiment = np.average(sentiment_list)
                if (newsfeed['articles'].index(i) > number_of_articles):
                    break

    def set_four_candle(self):
        pass

    def set_profit_loss(self):
        pass

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
        neutral = 100 * (len(tweets) - len(ntweets) - len(ptweets)) / len(tweets);

        if (positive + neutral >= 80):
            print("1")
        else:
            print("0")

    def set_moving_avg(self):
        pass

def init_stocks():
    IEX = Api("https://cloud.iexapis.com/beta/", None,
              "pk_11551eefe1bf4f0b81121b498c6a7651")  # secret = sk_8df6ccfac04742f194e71f6140cf6944
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


def buy(alpaca, symbol):
    qty = "300"
    kind = "market"
    time_in_force = "gtc"
    payload = "{\n\t\"symbol\": \"" + symbol + "\",\n\t\"qty\": " + qty + \
              ",\n\t\"side\": \"buy\",\n\t\"type\": \"" + kind + \
              "\",\n\t\"time_in_force\": \"" + time_in_force + "\"\n}"
    querystring = {"status": "all", "direction": "desc"}
    return alpaca.post("orders", payload, querystring)


def sell(alpaca, symbol):
    qty = "299"
    kind = "market"
    time_in_force = "gtc"
    payload = "{\n\t\"symbol\": \"" + symbol + "\",\n\t\"qty\": " + qty + \
              ",\n\t\"side\": \"sell\",\n\t\"type\": \"" + kind + \
              "\",\n\t\"time_in_force\": \"" + time_in_force + "\"\n}"
    querystring = {"status": "all", "direction": "desc"}
    return alpaca.post("orders", payload, querystring)


def get_current_price(stock):
    IEX = Api("https://cloud.iexapis.com/beta/", None, "pk_11551eefe1bf4f0b81121b498c6a7651")
    response = IEX.get("stock/" + stock.symbol + "/quote?token=" + IEX.key, None, None)
    stock.price = float(response['latestPrice'])
    return stock.price


def perform_trades():
    pass


def main():
    alpaca = Api("https://paper-api.alpaca.markets/v1/", {
        'content-type': "application/json",
        'apca-api-secret-key': "fRPyMcc4OootRhgez/W0HLPAv1IXbD/E6OaAzJTo",
        'apca-api-key-id': "PK6WI3ROFW19GXBRAQ4O"
    }, "fRPyMcc4OootRhgez/W0HLPAv1IXbD/E6OaAzJTo")

    stock_list = init_stocks()
    for stock in stock_list:
        stock.set_news_sentiment(10)

    while True:
        clock = alpaca.get("clock", None, None)
        if clock['is_open']:

            for stock in stock_list:
                print(f'Current Price of ' + stock.name + ' is ' + str(stock.price) + ' with 52 week low of ' + str(
                    stock.week52Low) + ' and sentiment of ' + str(stock.news_sentiment))
                print(f'Sentiment is ' + stock.news_sentiment)
                if ((stock.news_sentiment > .6) & ((stock.price - stock.week52Low) < (stock.price / 10))):
                    # buy(alpaca, stock.symbol)
                    print(f'Bought ' + stock.name + ' for ' + str(stock.price))
                print('')
            time.sleep(60)

        else:
            print('Markets are closed')
            time.sleep(60)


def other():
    alpaca = Api("https://paper-api.alpaca.markets/v1/", {
        'content-type': "application/json",
        'apca-api-secret-key': "fRPyMcc4OootRhgez/W0HLPAv1IXbD/E6OaAzJTo",
        'apca-api-key-id': "PK6WI3ROFW19GXBRAQ4O"
    }, "fRPyMcc4OootRhgez/W0HLPAv1IXbD/E6OaAzJTo")

    Tesla = Stock("TSLA", "Telsa", 0, 0)

    while (1):
        clock = alpaca.get("clock", None, None)
        if clock['is_open']:

            if (get_current_price(Tesla) > 283):
                sell(alpaca, "TSLA")
                print('Sold Tesla')
                exit()
            else:
                print(Tesla.price)
            time.sleep(60)

        else:
            print('Markets are closed')
            time.sleep(60)


main()
