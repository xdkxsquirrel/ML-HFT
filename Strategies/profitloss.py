import requests

class Profitloss(object):
      def __init__(self):
            pass

       # not profit or loss for now, but seeing if revenue is increasing
      # which is a sign of a stable company
      def get_profit_loss(self, symbol):
            try:
                  URLPE = "https://api.iextrading.com/1.0/stock/" + symbol + "/financials"
                  rPE = requests.get(url = URLPE)
                  data = rPE.json()
            except:
                  print(" !!IEX is down right now")
                  return 0

            if "financials" not in data:
                  return 0

            current = float(data[u'financials'][0]['totalRevenue'])
            twoQtrAgo = float(data[u'financials'][1]['totalRevenue'])
            threeQtrAgo = float(data[u'financials'][2]['totalRevenue'])

            if current > twoQtrAgo and twoQtrAgo > threeQtrAgo:
                  return 1
            else:
                  return 0