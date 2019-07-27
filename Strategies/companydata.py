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
                  indico = Api(None, None, None)
                  news = Api("https://newsapi.org/v2/", None, config.newsapi_api_key_id)
                  sentiment_list = list()
                  now = datetime.datetime.now()
                  if(now.day!=1):
                        yesterday = str(now.year) + '-' + str(now.month) + '-' + str(now.day-1)
                  else:
                        yesterday = str(now.year) + '-' + str(now.month-1) + '-0'
                  newsfeed = news.get("everything?q=" + name + "&from=" + yesterday + "&to=" + yesterday + "&sortBy=popularity&language=en&apiKey=" + news.key, None, None)
                  for i in newsfeed['articles']:
                        #Put URL into webscraper API then put into sentiment.
                        if(i['content']!=None):
                              data = re.sub('[^A-Za-z0-9 ]+', '', i['content'])
                              sentiment = indico.postIndico(data)
                              sentiment_list.append(float(sentiment['results']))

                        if( newsfeed['articles'].index(i) > number_of_articles):
                              break

                  if numpy.average(sentiment_list) > .55:
                        return 1
                  else:
                        return 0
            except:
                  print("Error in News Sentiment")