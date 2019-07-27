MAXWEIGHT = 100
MINWEIGHT = 0

class MLA():
      def __init__(self):
            self.company_weight = MAXWEIGHT/2
            self.four_weight = MAXWEIGHT/2
            self.profit_weight = MAXWEIGHT/2
            self.twitter_weight = MAXWEIGHT/2
            self.moving_weight = MAXWEIGHT/2

            self.company_data = 0
            self.four_data = 0
            self.profit_data = 0
            self.twitter_data = 0
            self.moving_data = 0

      def decide_trade(self):
            if(self.company_data * self.company_weight + \
                        self.moving_data * self.moving_weight + \
                        self.profit_data * self.profit_weight + \
                        self.twitter_data * self.twitter_weight) > 76:
                  return True
            elif (self.company_data * self.company_weight + \
                        self.moving_data * self.moving_weight + \
                        self.profit_data * self.profit_weight + \
                        self.twitter_data * self.twitter_weight) > 55:
                  return True
            else:
                  return False

      def learn(self, company_weight, four_weight, profit_weight, twitter_weight, moving_weight):
            if self.company_weight > MINWEIGHT & self.company_weight < MAXWEIGHT:
                  self.company_weight += company_weight

            if self.four_weight > MINWEIGHT & self.four_weight < MAXWEIGHT:
                  self.four_weight += four_weight

            if self.profit_weight > MINWEIGHT & self.profit_weight < MAXWEIGHT:
                  self.profit_weight += profit_weight

            if self.twitter_weight > MINWEIGHT & self.twitter_weight < MAXWEIGHT:
                  self.twitter_weight += twitter_weight

            if self.moving_weight > MINWEIGHT & self.moving_weight < MAXWEIGHT:
                  self.moving_weight += moving_weight

            return str(company_weight) + str(four_weight) + str(profit_weight) + str(twitter_weight) + str(moving_weight) 
