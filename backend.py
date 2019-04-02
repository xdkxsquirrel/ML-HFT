

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
        number_to_buy = buy = 0
        buy = self.company_weight * self.company_data + self.four_weight * self.four_data + self.moving_weight * self.moving_data + self.profit_weight * self.profit_data + self.twitter_weight * self.twitter_data 
        if buy < 40:
            number_to_buy = 0
            return "40", number_to_buy
        elif buy < 60:
            number_to_buy = 0
            return "sell", number_to_buy
        elif buy < 80:
            number_to_buy = 1
            return "sell", number_to_buy
        else:
            number_to_buy = 5
            return "sell", number_to_buy

    def learn(self):
        pass

        
