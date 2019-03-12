import api
import indicoio
import datetime
import numpy as np

indicoio.config.api_key = 'df08c40de1d01d2b3c8c3fc75f21ab81'
news = api.Api("https://newsapi.org/v2/", None, "36fc08386f85499c93487f0c03efba50")
now = datetime.datetime.now()
if(now.day!=1):
    yesterday = str(now.year) + '-' + str(now.month) + '-' + str(now.day-1)
else:
    yesterday = str(now.year) + '-' + str(now.month-1) + '-0'

class sentiment():
    def __init__(self, ticker, name):
        self.ticker = ticker 
        self.name = name
        self.current = 0

    def set_current_sentiment(self, number_of_articles):
        j = 0
        sentiment_list = list()
        newsfeed = news.get("everything?q=" + self.name + "&from=" + yesterday + "&to=" + yesterday + "&sortBy=popularity&language=en&apiKey=" + news.key, None, None)
        for i in newsfeed['articles']:
            #Put URL into webscraper API then put into sentiment.
            #print(i['content'])
            if(i['content']!=None):
                sentiment = indicoio.sentiment(i['content'])
                sentiment_list.append(float(sentiment))
                j = 1 + j
                if( j > number_of_articles):
                    return sentiment_list
        self.current = np.average(sentiment_list)