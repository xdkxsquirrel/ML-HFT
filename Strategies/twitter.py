#import numpy as np
import re
import config
import tweepy
from tweepy import OAuthHandler
import requests
import datetime
from textblob import TextBlob

class TwitterClient(object):

    def __init__(self):
        consumer_key = config.tweepy_consumer_key
        consumer_secret = config.tweepy_consumer_secret
        access_token = config.tweepy_access_token
        access_token_secret = config.tweepy_access_token_secret
        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret)

            # set access token/password from config file
            self.auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(self.auth)

        except:
            print("Error: Twitter Sign In Failed")

        # Save the tweet to the database with the name and sentiment value.

    # Save to our database for possible future use - As of now, no need
    def Save_To_Database(self, tweet, sentimentValue, name):
        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d") + "T00:00:00.000Z"
        name = "Test"

        query = '''mutation insertTweet($tweet:String!, $rating:Float!, $date:Date!, $company:String!)
          { insertTweet(record: { tweet:$tweet rating:$rating date:$date company:$company}) {
          recordId
        }}'''

        if sentimentValue == "positive":
            rating = 1
        else:
            rating = 0

        variables = {'tweet': tweet, 'rating': rating, 'date': date, 'company': name}
        request = requests.post(
            'https://seniorprojectu.herokuapp.com/graphql', json={'query': query, 'variables': variables})
        if request.status_code != 200:
            raise Exception("Query failed to run by returning code of {}. {}".format(
                request.status_code, query))

    def regex(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split())

    def run_sentiment_analysis(self, tweet, name):
        cleanedTweet = self.regex(tweet)
        analysis = TextBlob(cleanedTweet)
        sentimentPolarityNumber = analysis.sentiment.polarity

        if sentimentPolarityNumber > 0:
            sentimentPolarity = 'positive'
        elif sentimentPolarityNumber < 1:
            sentimentPolarity = 'negative'
        else:
            sentimentPolarity = 'null'

        # call database to save
        self.Save_To_Database(cleanedTweet, sentimentPolarity, name)
        return sentimentPolarity

    def get_tweets(self, query, count):

        tweets = []

        try:
            # call twitter api with query for tweets
            fetched_tweets = self.api.search(q=query, count=count)

            # parse tweets one by one
            for tweet in fetched_tweets:

                # get sentiment
                sentiment = self.run_sentiment_analysis(tweet.text, query)

                # This creates an empty directory and then parses the tweets
                tweet_dir = {'text': tweet.text, 'sentiment': sentiment}

                # avoid having multiple tweets in our directory
                if tweet.retweet_count > 0:
                    if tweet_dir not in tweets:
                        tweets.append(tweet_dir)
                else:
                    tweets.append(tweet_dir)

                    # return tweets
            return tweets

        except tweepy.TweepError as error:
            # error
            print("Error : " + str(error))

        except:
              print("Unknown Error in Twitter")

class Twitter(object):

      def __init__(self):
            pass

      def  get_twitter_sentiment(self, name, criteria):
            twitterClient = TwitterClient()
            # Get 100 tweets of "Name"
            tweets = twitterClient.get_tweets(query=name, count=100)

            # Below is used for the machine learning
            # Get the number of Positive tweets
            positiveTweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
            percentPositive = 100 * len(positiveTweets) / len(tweets)

            # Return a 1 or a 0 for the machine learning to take and use
            if percentPositive > criteria:
                  return 1
            else:
                  return 0


