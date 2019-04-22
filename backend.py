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
        print(f'CD: ' + str(self.company_data) + 'CW: ' + str(self.company_weight) + \
            ' | MD: ' + str(self.moving_data) + 'MW: ' + str(self.moving_weight) + \
                ' | PD: ' + str(self.profit_data) + 'PW: ' + str(self.profit_weight) + \
                    ' | TD: ' + str(self.twitter_data) + 'TW: ' + str(self.twitter_weight))
        print(self.company_data * self.company_weight + \
            self.moving_data * self.moving_weight + \
                self.profit_data * self.profit_weight + \
                    self.twitter_data * self.twitter_weight)
                    
        if(self.company_data * self.company_weight + \
            self.moving_data * self.moving_weight + \
                self.profit_data * self.profit_weight + \
                    self.twitter_data * self.twitter_weight) > 70:
            return 2
        elif (self.company_data * self.company_weight + \
            self.moving_data * self.moving_weight + \
                self.profit_data * self.profit_weight + \
                    self.twitter_data * self.twitter_weight) > 20:
            return 1
        else:
            return 0

    def learn(self):
        pass

        
