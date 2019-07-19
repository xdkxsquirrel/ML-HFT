
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
