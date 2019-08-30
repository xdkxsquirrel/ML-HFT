import requests
import config

class Profitloss(object):
      def __init__(self):
            pass

      def get_profit_loss(self, symbol):
            try:                  
                  url = "https://cloud.iexapis.com/beta/stock/" + symbol + "/income?period=quarterly&last=3&token=" + config.IEX_api_secret_key
                  response = requests.request("GET", url, data=None, headers=None, params=None)
                  data = response.json()
            except:
                  print(" !!IEX is down right now")
                  return 0

            if "income" not in data:
                  return 0

            try:
                  current = float(data[u'income'][0]['totalRevenue'])
                  twoQtrAgo = float(data[u'income'][1]['totalRevenue'])
                  threeQtrAgo = float(data[u'income'][2]['totalRevenue'])
            except:
                  print(" !!IEX conversion error")
                  return 0

            if current > twoQtrAgo and twoQtrAgo > threeQtrAgo:
                  return 1
            else:
                  return 0