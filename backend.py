

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
        if(self.company_data > 50):
            print("Company Data Bullish")
        else:
            print("Comapny Data Bearish")
        
        if(self.four_data > 50):
            print("Four Candle Hammer Bullish")
        else:
            print("Four Candle Hammer Bearish")

        if(self.profit_data > 50):
            print("Profit and Loss Statement Bullish")
        else: 
            print("Profit and Loss Statement Bearish")

        if(self.twitter_data > 50):
            print("Twitter Bullish")
        else:
            print("Twitter Bearish")

        if(self.moving_data > 50):
            print("200 Moving Day Average Bullish")
        else:
            print("200 Moving Day Average Bearish")

        
