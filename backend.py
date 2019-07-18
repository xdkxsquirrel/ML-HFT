class MLA():
    def __init__(self, company_weight, four_weight, profit_weight, twitter_weight, moving_weight):
        self.company_weight = company_weight
        self.four_weight = four_weight
        self.profit_weight = profit_weight
        self.twitter_weight = twitter_weight
        self.moving_weight = moving_weight

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
            return 2
        elif (self.company_data * self.company_weight + \
            self.moving_data * self.moving_weight + \
                self.profit_data * self.profit_weight + \
                    self.twitter_data * self.twitter_weight) > 55:
            return 1
        else:
            return 0

    def remember(self):
            # When a trade is decided to be made, it should keep track so that in a minutes time we can come back and see if the trade was fruitful.
            # If the trade went up in value, add to the weights of the classifiers that suggested a buy.
            # If the trade went down in value, subtract from the weights of the classifiers that suggested a buy.
            pass

    def learn(self):
        pass
        
