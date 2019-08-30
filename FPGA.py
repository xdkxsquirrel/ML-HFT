MAXWEIGHT = 100.0
MINWEIGHT = 0.0

class MLA():
      def __init__(self, cw, fw, pw, tw, mw):
            self.company_weight = cw
            self.four_weight = fw
            self.profit_weight = pw
            self.twitter_weight = tw
            self.moving_weight = mw

            self.company_data = 0
            self.four_data = 0
            self.profit_data = 0
            self.twitter_data = 0
            self.moving_data = 0

      def decide_trade(self):
            tipping_point = (self.company_weight +  self.four_weight + self.profit_weight + self.twitter_weight + self.moving_weight) / 5
            if(self.company_data * self.company_weight + \
                        self.moving_data * self.moving_weight + \
                        self.profit_data * self.profit_weight + \
                        self.twitter_data * self.twitter_weight) > tipping_point:
                  return True
            else:
                  return False

      def learn(self, company_data, four_data, profit_data, twitter_data, moving_data):
            if (self.company_weight > MINWEIGHT) & (self.company_weight < MAXWEIGHT):
                  self.company_weight += float(company_data)

            if (self.four_weight > MINWEIGHT) & (self.four_weight < MAXWEIGHT):
                  self.four_weight += float(four_data)

            if (self.profit_weight > MINWEIGHT) & (self.profit_weight < MAXWEIGHT):
                  self.profit_weight += float(profit_data)

            if (self.twitter_weight > MINWEIGHT) & (self.twitter_weight < MAXWEIGHT):
                  self.twitter_weight += float(twitter_data)

            if (self.moving_weight > MINWEIGHT) & (self.moving_weight < MAXWEIGHT):
                  self.moving_weight += float(moving_data)

            return self.company_weight, self.four_weight, self.profit_weight, self.twitter_weight, self.moving_weight 
