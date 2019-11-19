import datetime
import requests
import numpy as np
import re
import config
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob

 #Constants
Current_Company = " "
cleaned_tweet =""

class TwitterClient(object):

    def __init__(self):
        consumer_key = config.tweepy_consumer_key
        consumer_secret = config.tweepy_consumer_secret
        access_token = config.tweepy_access_token
        access_token_secret = config.tweepy_access_token_secret

        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret)

            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(self.auth)

        except:
            print("Error: Twitter Sign In Failed")

    def regex(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split())

    def run_sentiment_analysis(self, tweet):

        analysis = TextBlob(self.regex(tweet))

        # create TextBlob object of passed tweet text
        cleaned_tweet = self.clean_tweet(tweet)
        analysis = TextBlob(cleaned_tweet)

        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        else:
            return 'null'

    def get_tweets(self, query, count):

        tweets = []

        try:
            # call twitter api to get tweets
            fetched_tweets = self.api.search(q=query, count=count)

            # parsing tweets one by one
            for tweet in fetched_tweets:
                # This creates an empty directory and then parses the tweets
                tweet_dir = {'text': tweet.text, 'sentiment': self.run_sentiment_analysis(tweet.text)}

                # avoid having multiple tweets in our directory
                if tweet.retweet_count > 0:
                    if tweet_dir not in tweets:
                        tweets.append(tweet_dir)
                else:
                    tweets.append(tweet_dir)

                    # return tweets
            return tweets

        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))

        except:
              print("Unknown Error in Twitter")

class Twitter(object):

    def Get_Stocks(self):
        return ["Tesla", "Apple", "Walmart", "JNJ", "Google", "Exxon", "Microsoft", "GE", "JPMorgan", "IBM", "Amazon"]

    def __init__(self):
            pass

    def get_twitter_sentiment(self):
        api = TwitterClient()

        #get all names for the company data
        CompanyNames = self.Get_Stocks()
        for name in CompanyNames:
            # Get 100 tweets of "name"
            tweets = api.get_tweets(query=name, count=100)
            # positive tweets
            ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
            positive = 100 * len(ptweets) / len(tweets)
            # Get the number of Positive tweets
            if positive > 50:
                  SentValue = 1

            else:
                  SentValue = 0

            now = datetime.datetime.now()
            date = now.strftime("%Y-%m-%d") + "T00:00:00.000Z"
            payload = 'Payload{insertTweet(record: {'+cleaned_tweet+', rating:' + SentValue +'' \
                'date: '+date+',company: '+name+'})}'

            request = requests.post(
                'https://seniorprojectu.herokuapp.com/graphql', json={'query': payload})
            if request.status_code != 200:
                raise Exception("Query failed to run by returning code of {}. {}".format(
                    request.status_code, payload))







