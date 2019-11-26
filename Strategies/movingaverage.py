import requests
import config

class Average(object):
      def __init__(self):
            pass

      def get_moving_avg(self, symbol):
            try:
                  URL = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + symbol + "&apikey=" + config.alphaadvantage_api_key_id
                  r = requests.get(url = URL)
                  data = r.json()
                  count = total = 0
                  if "Time Series (Daily)" not in data:
                        return 0
                  for a in data["Time Series (Daily)"]:
                        count = count + 1
                        total = float(data["Time Series (Daily)"][a]["4. close"]) + total
                  #print (float(data["Time Series (Daily)"][a]["4. close"]))
                  movingAvg = total / 100
                  dates = sorted(data["Time Series (Daily)"].keys(),  reverse=True)
                  currentDate = dates[0]
                  currnetPrice = float(data["Time Series (Daily)"][currentDate]["4. close"])
                  tenDayTotal = 0
                  for y in range(10):
                        tenDayTotal= tenDayTotal + float(data["Time Series (Daily)"][dates[y]]["4. close"])
                  tenDayAvg = tenDayTotal / 10
                  fiveDayOldPrice = float(data["Time Series (Daily)"][dates[4]]["4. close"])

                  if (currnetPrice < fiveDayOldPrice):
                  # slope is moving down
                  # we want to buy
                  # TODO  we should actually see if the slope is down and we are within a small %
                  # of touching the long term moving average
                        if currnetPrice > movingAvg:
                              return 1
                        else:
                              return 0
                  else:
                  # slope is moving up
                  # if slope is moving up and we already have bought it
                  # lets hold it
                  # if slope is moving up lets look for slope of last few days, if its comming down
                  # lets sell it
                        return 0

            # eventually we want to see if the the slope of the 10 day average is comming down
            # and the current price is within a few % of the long term moving average
            # that means we are buying on the way back down to the moving average which should be
            # acting as support line and possibly buying around lowest price in the cycle
            # the other side we'll want to keep track that it doesnt go too far below the long term avg
            # if it does then we will want to sell until we start averaging above again
            # if currnetPrice > movingAvg and tenDayAvg > movingAvg:
            #     print "buy it"

            except Exception as e:
                  print("!! Failure in movingAverage: " + str(e))
                  return 0