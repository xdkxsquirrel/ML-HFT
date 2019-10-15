# 1. Identify a market trend... 20-day high.
# 2. Identify a pullback (that moves against this trend), such as a 4 day pullback.
# 3. Observe the trend resuming, the 5th day closing price is above the 4th day closing price.
# 4. Buy at the opening of the 6th day.
# 5. Place a stop loss 10 pips below the 5th day low.
# 6. Aim for a risk/reward ratio of 1:3 by taking a profit 3 times the distance between your entry price.

# Call API
# query{
#  fourCandleHammer(date:"2019-04-28T00:00:00.000Z", ticker:"JNJ")
# }

import requests
import datetime


class Fourcandle(object):
    def __init__(self):
        pass

    def get_four_candle_hammer(self, symbol):
        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d") + "T00:00:00.000Z"
        query = 'query{ fourCandleHammer(date:"' + \
            date + '", ticker:"' + symbol + '") }'
        request = requests.post(
            'https://seniorprojectu.herokuapp.com/graphql', json={'query': query})
        if request.status_code != 200:
            raise Exception("Query failed to run by returning code of {}. {}".format(
                request.status_code, query))
        response = request.json()
        if response['data']['fourCandleHammer'] == True:
            return 1
        return 0

