import numpy as np
import re
import config
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob

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

      def __init__(self):
            pass

      def  get_twitter_sentiment(self, name):
            api = TwitterClient()
            # Get 100 tweets of "Name"
            tweets = api.get_tweets(query=name, count=100)

            # Get the number of Positive tweets
            positive_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
            percent_positive = 100 * len(positive_tweets) / len(tweets)

            # Return a 1 or a 0 for the machine learning to take and use
            if percent_positive > 50:
                  return 1
            else:
                  return 0


