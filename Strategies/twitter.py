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

    # Sanatize the tweet. ie remove all images and #s and other junk
    def regex(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|", " ", tweet).split())

    def get_analysis(self, tweet):
        return TextBlob(cleaned_tweet)

    def run_sentiment_analysis(self, tweet):
        analysis = get_analysis(self.regex(tweet))

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

                # avoid having multiple same tweets in our directory
                # since we could save multiple retweets.
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

    def __init__(self):
            pass

    # Sanatize the tweet. ie remove all images and #s and other junk
    def regex(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|", " ", tweet).split())

    # these are the universe for the stocks that we are buying/selling thus, these are all we need
    def Get_Stocks(self):
        return ["Tesla", "Apple", "Walmart", "JNJ", "Google", "Exxon", "Microsoft", "GE", "JPMorgan", "IBM", "Amazon"]

    # Save the tweet to the database with the name and sentiment value.
    def Save_To_Database(self, tweet, sentimentValue, name):
        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d") + "T00:00:00.000Z"
        payload = 'Payload{insertTweet(record: {' + self.regex(tweet) + ', rating:' + sentimentValue + '' \
                  'date: ' + date + ',company: ' + name + '})}'
        request = requests.post(
            'https://seniorprojectu.herokuapp.com/graphql', json={'payload': payload})
        if request.status_code != 200:
            raise Exception("Query failed to run by returning code of {}. {}".format(
                request.status_code, payload))

    # this is the main method the twitter analysis.
    def get_twitter_sentiment(self):
        api = TwitterClient()
        # get all names for the company data
        CompanyNames = self.Get_Stocks()

        # Loop through each company name
        for name in CompanyNames:
            # Get 100 tweets of "name"
            tweets = api.get_tweets(query=name, count=100)
            # Save the positive tweets
            for tweet in tweets:
                if tweet['sentiment'] == 'positive':
                    positive_tweets = tweet

            # Find the percentage of positive tweets using the length of the arrays of tweets
            positive = 100 * len(positive_tweets) / len(tweets)
            # Get the number of Positive tweets
            if positive > 50:
                  sentimentValue = 1
            else:
                  sentimentValue = 0
            #
            for tweet in tweets:
                self.Save_To_Database(tweet, tweet['sentiment'], name)

            # we need to bable to save to the database just company sentiment and all the tweets