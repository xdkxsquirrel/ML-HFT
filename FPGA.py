import time
import serial

MAXWEIGHT = 255.0
MINWEIGHT = 0.0
FPGA_IN_USE = True

ser = serial.Serial(            
     port='/dev/serial0',
     baudrate = 115200,
     parity=serial.PARITY_NONE,
     stopbits=serial.STOPBITS_ONE,
     bytesize=serial.EIGHTBITS,
     timeout=2000
 )


class MLA():
      def __init__(self, cw, fw, pw, tw, mw, ticker):
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
            
            self.ticker = ticker
            try:
                  if(FPGA_IN_USE):
                        bytes_to_send = 'A'
                        stock_case = { "TSLA": '1', "AAPL": '2', "WMT": '3', "JNJ": '4', "GOOG": '5', "XOM": '6', "MSFT": '7', "GE": '8', "JPM": '9', "IBM": 'A', "AMZN": 'B' }
                        bytes_to_send += stock_case[ticker]
                        bytes_to_send += "{:02x}".format(cw)
                        bytes_to_send += "{:02x}".format(fw)
                        bytes_to_send += "{:02x}".format(pw)
                        bytes_to_send += "{:02x}".format(tw)
                        bytes_to_send += "{:02x}".format(mw)
                        ser.write(bytes_to_send.encode())
                        bytes_received = ser.read(10)
                        answer = "CCCCCCCCCC"
                        if((bytes_received[0] == ord(answer[0]) ) and (bytes_received[1] == ord(answer[1]) ) and (bytes_received[2] == ord(answer[2])) and (bytes_received[3] == ord(answer[3])) and (bytes_received[4] == ord(answer[4])) and (bytes_received[5] == ord(answer[5])) and (bytes_received[6] == ord(answer[6])) and (bytes_received[7] == ord(answer[7])) and (bytes_received[8] == ord(answer[8])) and (bytes_received[9] == ord(answer[9])) ):
                             print("    Weights Set on FPGA")
                        else:
                             print(" !! FPGA Failed to save Weights as " + str(e))
            except Exception as e:
                  print(" !! FPGA Exception to save Weights as " + str(e))
                       
      
      def decide_trade_locally(self):
            tipping_point = (self.company_weight +  self.four_weight + self.profit_weight + self.twitter_weight + self.moving_weight) / 2
            print("TP: " + str(tipping_point) + " Calc: " + str(self.company_data * self.company_weight + \
                        self.moving_data * self.moving_weight + \
                        self.profit_data * self.profit_weight + \
                        self.twitter_data * self.twitter_weight + \
                        self.four_data * self.four_weight))
            if(self.company_data * self.company_weight + \
                        self.moving_data * self.moving_weight + \
                        self.profit_data * self.profit_weight + \
                        self.twitter_data * self.twitter_weight + \
                        self.four_data * self.four_weight) > tipping_point:
                  return True
            else:
                  return False

      def learn_from_failure_locally(self, company_data, four_data, profit_data, twitter_data, moving_data):
            if (self.company_weight > MINWEIGHT) & (self.company_weight < MAXWEIGHT):
                  self.company_weight -= float(company_data)

            if (self.four_weight > MINWEIGHT) & (self.four_weight < MAXWEIGHT):
                  self.four_weight -= float(four_data)

            if (self.profit_weight > MINWEIGHT) & (self.profit_weight < MAXWEIGHT):
                  self.profit_weight -= float(profit_data)

            if (self.twitter_weight > MINWEIGHT) & (self.twitter_weight < MAXWEIGHT):
                  self.twitter_weight -= float(twitter_data)

            if (self.moving_weight > MINWEIGHT) & (self.moving_weight < MAXWEIGHT):
                  self.moving_weight -= float(moving_data)

            return self.company_weight, self.four_weight, self.profit_weight, self.twitter_weight, self.moving_weight 
            
      def learn_from_success_locally(self, company_data, four_data, profit_data, twitter_data, moving_data):
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
            
      def decide_trade_on_FPGA(self):
            try:
                  bytes_to_send = 'C'
                  stock_case = { "TSLA": '1', "AAPL": '2', "WMT": '3', "JNJ": '4', "GOOG": '5', "XOM": '6', "MSFT": '7', "GE": '8', "JPM": '9', "IBM": 'A', "AMZN": 'B' }
                  bytes_to_send += stock_case[self.ticker]
                  bytes_to_send += '{:02d}'.format(self.company_data)
                  bytes_to_send += '{:02d}'.format(self.four_data)
                  bytes_to_send += '{:02d}'.format(self.profit_data)
                  bytes_to_send += '{:02d}'.format(self.twitter_data)
                  bytes_to_send += '{:02d}'.format(self.moving_data)
                  ser.write(bytes_to_send.encode())
                  bytes_received = ser.read(10)
                  
                  buy = "1111111111"
                  hold = "2222222222"
                  if((bytes_received[0] == ord(buy[0])) and (bytes_received[1] == ord(buy[1])) and (bytes_received[2] == ord(buy[2])) and (bytes_received[3] == ord(buy[3])) and (bytes_received[4] == ord(buy[4])) and (bytes_received[5] == ord(buy[5])) and (bytes_received[6] == ord(buy[6])) and (bytes_received[7] == ord(buy[7])) and (bytes_received[8] == ord(buy[8])) and (bytes_received[9] == ord(buy[9]))):
                     return True
                  elif((bytes_received[0] == ord(hold[0])) and (bytes_received[1] == ord(hold[1])) and (bytes_received[2] == ord(hold[2])) and (bytes_received[3] == ord(hold[3])) and (bytes_received[4] == ord(hold[4])) and (bytes_received[5] == ord(hold[5])) and (bytes_received[6] == ord(hold[6])) and (bytes_received[7] == ord(hold[7])) and (bytes_received[8] == ord(hold[8])) and (bytes_received[9] == ord(hold[9]))):
                     return False
                  else:
                     print("  FPGA decide trade FAILED")
                     return self.decide_trade_locally()
            except Exception as e:
                  print(" !! FPGA decide trade FAILED for " + e)
                  return self.decide_trade_locally()
            
      def learn_from_failure_on_FPGA(self, company_data, four_data, profit_data, twitter_data, moving_data):
            bytes_to_send = 'E'
            stock_case = { "TSLA": '1', "AAPL": '2', "WMT": '3', "JNJ": '4', "GOOG": '5', "XOM": '6', "MSFT": '7', "GE": '8', "JPM": '9', "IBM": 'A', "AMZN": 'B' }
            bytes_to_send += stock_case[self.ticker]
            if(company_data):
                  bytes_to_send += '01'
            else:
                  bytes_to_send += '00'
                  
            if(four_data):
                  bytes_to_send += '01'
            else:
                  bytes_to_send += '00'
                  
            if(profit_data):
                  bytes_to_send += '01'
            else:
                  bytes_to_send += '00'
                  
            if(twitter_data):
                  bytes_to_send += '01'
            else:
                  bytes_to_send += '00'
                  
            if(moving_data):
                  bytes_to_send += '01'
            else:
                  bytes_to_send += '00'
                  
            ser.write(bytes_to_send.encode())
            bytes_received = ser.read(10)
            
            if(bytes_received != 'CCCCCCCCCC'):
                  print("  FPGA Learn from failure FAILED")
                  
            return self.learn_from_failure_locally(company_data, four_data, profit_data, twitter_data, moving_data)
            
      def learn_from_success_on_FPGA(self, company_data, four_data, profit_data, twitter_data, moving_data):
            bytes_to_send = 'D'
            stock_case = { "TSLA": '1', "AAPL": '2', "WMT": '3', "JNJ": '4', "GOOG": '5', "XOM": '6', "MSFT": '7', "GE": '8', "JPM": '9', "IBM": 'A', "AMZN": 'B' }
            bytes_to_send += stock_case[self.ticker]
            if(company_data):
                  bytes_to_send += '01'
            else:
                  bytes_to_send += '00'
                  
            if(four_data):
                  bytes_to_send += '01'
            else:
                  bytes_to_send += '00'
                  
            if(profit_data):
                  bytes_to_send += '01'
            else:
                  bytes_to_send += '00'
                  
            if(twitter_data):
                  bytes_to_send += '01'
            else:
                  bytes_to_send += '00'
                  
            if(moving_data):
                  bytes_to_send += '01'
            else:
                  bytes_to_send += '00'
                  
            ser.write(bytes_to_send.encode())
            bytes_received = ser.read(10)
            
            if(bytes_received != 'CCCCCCCCCC'):
                  print("  FPGA Learn from success FAILED")
                  
            return self.learn_from_success_locally(company_data, four_data, profit_data, twitter_data, moving_data)
            
      def decide_trade(self):
            if(FPGA_IN_USE):
                  return self.decide_trade_on_FPGA()
            else:
                  return self.decide_trade_locally()
                  
      def learn_from_failure(self, company_data, four_data, profit_data, twitter_data, moving_data):
            if(FPGA_IN_USE):
                  return self.learn_from_failure_locally(company_data, four_data, profit_data, twitter_data, moving_data)
            else:
                  return self.learn_from_failure_on_FPGA(company_data, four_data, profit_data, twitter_data, moving_data)
                  
      def learn_from_success(self, company_data, four_data, profit_data, twitter_data, moving_data):
            if(FPGA_IN_USE):
                  return self.learn_from_success_locally(company_data, four_data, profit_data, twitter_data, moving_data)
            else:
                  return self.learn_from_success_on_FPGA(company_data, four_data, profit_data, twitter_data, moving_data)
