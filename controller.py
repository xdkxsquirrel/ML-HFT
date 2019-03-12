import time
import api
import paralleldots

paralleldots.set_api_key("7bb52o7adoBzZjmxaG6Wwgy7wfYvg9txNLnZHKh89E4")

stock_list = [
    "TSLA","AAPL","WMT","JNJ","GOOG","XOM","MSFT","GE","JPM","IBM","AMZN"
    ]
name_list = [
    "Tesla","Apple","Walmart","Johnson & Johnson","Google","Exxon","Microsoft","General Electric","JPMorgan Chase","IBM","Amazon"
    ]

alpaca = api.Api("https://paper-api.alpaca.markets/v1/", {
    'content-type': "application/json",
    'apca-api-secret-key': "fRPyMcc4OootRhgez/W0HLPAv1IXbD/E6OaAzJTo",
    'apca-api-key-id': "PK6WI3ROFW19GXBRAQ4O"
    }, "fRPyMcc4OootRhgez/W0HLPAv1IXbD/E6OaAzJTo")

news = api.Api("https://newsapi.org/v2/", None, "36fc08386f85499c93487f0c03efba50")

#########################################################################################
############                        MAIN METHOD                       ################### 
def main():
    global account_info
    
    while True:

        current_positions = alpaca.get("positions", None, None)
        current_list = list()
        open_orders = alpaca.get("orders", None, {"status":"open","direction":"desc"})

        for i in range(len(current_positions)):
            current_list.insert(i, current_positions[i]['symbol']) 
        clock = alpaca.get("clock", None, None)
        account_info = alpaca.get("account", None, None)
        if clock['is_open']:
            
            if len(open_orders) == 0 :
                for i in current_positions:
                    print(i['symbol'])
                    time.sleep(10)

                for i in stock_list :
                    if i not in current_list :
                        print(i)
                        time.sleep(10)


            else :
                print(f'{len(open_orders)} orders pending.')
                time.sleep(30)

        else:
            print('Markets are closed')
            time.sleep(60)

main()