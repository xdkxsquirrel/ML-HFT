class MLA():
    def __init__(self):
        self.company_weight = 50
        self.four_weight = 50
        self.profit_weight = 50
        self.twitter_weight = 50
        self.moving_weight = 50

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

    def remember(self):
            # When a trade is decided to be made, it should keep track so that in a minutes time we can come back and see if the trade was fruitful.
            # If the trade went up in value, add to the weights of the classifiers that suggested a buy.
            # If the trade went down in value, subtract from the weights of the classifiers that suggested a buy.
            pass

    def learn(self):
        pass
        
