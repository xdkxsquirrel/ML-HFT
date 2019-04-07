

class MLA():
    def __init__(self, company_weight, four_weight, profit_weight, twitter_weight, moving_weight):
        self.company_weight = company_weight
        self.four_weight = four_weight
        self.profit_weight = profit_weight
        self.twitter_weight = twitter_weight
        self.moving_weight = moving_weight

        self.trades_history = list()

        self.company_data = 0
        self.four_data = 0
        self.profit_data = 0
        self.twitter_data = 0
        self.moving_data = 0

    def decide_trade(self):
        if(self.company_data * self.company_weight) > 1:
            return 1
        else:
            return 0

    def learn(self):
        pass

        
