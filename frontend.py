#import alpaca_trade_api as tradeapi
import time
import requests

base_url = "https://paper-api.alpaca.markets/v1/"
headers = {
    'content-type': "application/json",
    'apca-api-secret-key': "fRPyMcc4OootRhgez/W0HLPAv1IXbD/E6OaAzJTo",
    'apca-api-key-id': "PK6WI3ROFW19GXBRAQ4O"
    }
account_info = None
stock_list = [
    "TSLA","AAPL","WMT","IBN","GS","T","DE","JNJ","O","GOOG","XOM","MSFT","TTM","GE","STM","XLNX",
    "PFE","GPRO","INTC","JPM","IBM","UIS",
    ]


def get_account_info():
    url = base_url + "account"
    payload = ""
    response = requests.request("GET", url, data=payload, headers=headers)
    return response.json()


##########################################################################################
############                        ORDERS                             ###################
def list_all_orders():
    url = base_url + "orders"
    querystring = {"status":"all","direction":"desc"}
    payload = ""
    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    return response.json()


def list_all_open_orders():
    url = base_url + "orders"
    querystring = {"status":"open","direction":"desc"}
    payload = ""
    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    return response.json()


def place_buy_order(symbol, qty, type, time_in_force):
    url = base_url + "orders"
    querystring = {"status":"all","direction":"desc"}
    payload = "{\n\t\"symbol\": \"" + symbol + "\",\n\t\"qty\": " + qty +\
        ",\n\t\"side\": \"buy\",\n\t\"type\": \"" + type +\
        "\",\n\t\"time_in_force\": \"" + time_in_force + "\"\n}"
    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
    return response.json()


def place_sell_order(symbol, qty, type, time_in_force):
    url = base_url + "orders"
    querystring = {"status":"all","direction":"desc"}
    payload = "{\n\t\"symbol\": \"" + symbol + "\",\n\t\"qty\": " + qty +\
        ",\n\t\"side\": \"sell\",\n\t\"type\": \"" + type +\
        "\",\n\t\"time_in_force\": \"" + time_in_force + "\"\n}"
    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
    return response.json()


def get_an_order():
    return 'Get an Order'


def cancel_an_order():
    return 'Cancel an Order'


##########################################################################################
############                        POSITIONS                          ###################
def get_all_open_positions():
    url = base_url + "positions"
    payload = ""
    response = requests.request("GET", url, data=payload, headers=headers)
    current_positions = response.json()
    # 200 print (response.status_code)
    # Json print (response.headers['content-type'])
    return current_positions


def get_an_open_position(symbol):
    url = base_url + "positions/" + symbol
    payload = ""
    response = requests.request("GET", url, data=payload, headers=headers)
    return response.json()


##########################################################################################
############                        ASSETS                             ###################
def get_all_assets():
    print('All Assets')


def get_an_asset():
    print('Asset')


##########################################################################################
############                        CALENDAR and CLOCK                 ###################    
def get_the_calendar():
    print('Calendar')


def get_the_clock():
    url = base_url + "clock"
    payload = ""
    response = requests.request("GET", url, data=payload, headers=headers)
    return response.json()

##########################################################################################
############                        MARKET DATA                        ###################    
def get_one_day_bar(symbol):
    url = "https://data.alpaca.markets/v1/bars/1D"
    querystring = {"symbols":symbol,"limit":"1","start":"","end":"","after":"","until":""}
    payload = ""
    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    return response.json()


def get_fifteen_minute_bar(symbol):
    url = "https://data.alpaca.markets/v1/bars/15Min"
    querystring = {"symbols":symbol,"limit":"1","start":"","end":"","after":"","until":""}
    payload = ""
    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    return response.json()


##########################################################################################
############                        TRADE ALGORITHMS                   ################### 
def trade_currently_held_stocks(symbol):
    open_position = (get_an_open_position(symbol))
    one_day_bar = get_one_day_bar(symbol)

    if float(open_position['market_value']) < (float(account_info['portfolio_value'])/40) :
        if (float(one_day_bar[symbol][0]['l']) - float(open_position['current_price'])) < (float(one_day_bar[symbol][0]['l'])/50) :
            if float(open_position['current_price']) < (float(account_info['buying_power']) + 10) :
                print(f'BUY ONE {symbol}')
                place_buy_order(symbol, "1", "market", "gtc")
    else :
        if (float(open_position['current_price']) - float(open_position['avg_entry_price'])) > (float(open_position['current_price'])/100) :
            print(f'SELL ALL {symbol}')
            place_sell_order(symbol, open_position['qty'], "market", "gtc")
        else : 
            print(f'STAY ALL {symbol}')


def buy_new_stock(symbol):
    one_day_bar = get_one_day_bar(symbol)
    if (float(one_day_bar[symbol][0]['c']) - float(one_day_bar[symbol][0]['l'])) < (float(one_day_bar[symbol][0]['l'])/100) :
        if float(one_day_bar[symbol][0]['c']) < (float(account_info['buying_power']) + 10) :
            print(f'BUYING {symbol} from stock list')
            place_buy_order(symbol, "1", "market", "gtc")


##########################################################################################
############                        MAIN METHOD                        ################### 
def main():
    global account_info
    while True:
        current_positions = get_all_open_positions()
        current_list = list()
        open_orders = list_all_open_orders()
        for i in range(len(current_positions)):
            current_list.insert(i, current_positions[i]['symbol']) 
        clock = get_the_clock()
        account_info = get_account_info()
        if clock['is_open']:
            
            if len(open_orders) == 0 :
                for i in current_positions:
                    trade_currently_held_stocks(i['symbol'])
                    time.sleep(10)

                for i in stock_list :
                    if i not in current_list :
                        buy_new_stock(i)
                        time.sleep(10)


            else :
                print(f'{len(open_orders)} orders pending.')
                time.sleep(30)

        else:
            print('Markets are closed')
            time.sleep(60)

main()
