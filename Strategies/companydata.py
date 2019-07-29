import numpy
import datetime
import config
import requests
import re

class Company(object):
      def __init__(self):
            pass
      
      def get_news_sentiment(self, number_of_articles, name):
            try:
                  sentiment_list = list()
                  now = datetime.datetime.now()
                  if(now.day!=1):
                        yesterday = str(now.year) + '-' + str(now.month) + '-' + str(now.day-1)
                  else:
                        yesterday = str(now.year) + '-' + str(now.month-1) + '-0'
                  url = "https://newsapi.org/v2/everything?q=" + name + "&from=" + yesterday + "&to=" + yesterday + "&sortBy=popularity&language=en&apiKey=" + config.newsapi_api_key_id
                  response = requests.request("GET", url, data=None, headers=None, params=None)
                  newsfeed = response.json()
                  for i in newsfeed['articles']:
                        if(i['content']!=None):
                              data = re.sub('[^A-Za-z0-9 ]+', '', i['content'])
                              payload = {'data' : data} 
                              url = "https://apiv2.indico.io/sentiment"
                              headers = { 'X-ApiKey' : config.indico_api_key_id}
                              response = requests.request("GET", url, data=payload, headers=headers, params=None)
                              sentiment = response.json()
                              sentiment_list.append(float(sentiment['results']))

                        if( newsfeed['articles'].index(i) > number_of_articles):
                              break

                  if numpy.average(sentiment_list) > .55:
                        return 1
                  else:
                        return 0
            except:
                  print("Error in News Sentiment")