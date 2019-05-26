#!/usr/bin/env python3
from binance.client import Client
from binance.enums import *
import time
from decimal import Decimal

# Global Variable initialization/ declaration

api_key = 'yPDhNNsZTLrcJu1dNOzPU2zYmIBXnC9C6qkfzQH3YKVXLXGqa0DF3kFFVZZjy2Hy'
api_secret = '4DNM7yrmWsCnAStjC92ml9fQAKoabS2x1jdpVEd8xXGsvg9SGorYcrYv8xbglmru'
recv_window = 6000000

pair = "EOSUSDT"

profit = float(0.2/100) # profit 0.2%
sold_price = float(0)
bought_price = float(6.3150)

selling_price = float(0)
buying_price = float(0)

quantity = round(Decimal(1.68), 2)

placed_buy_order = True

ordered_id = 0

lowest_profit = float(0.5/100)

'''
# get market depth
#depth = client.get_order_book(symbol=pair)
#print (depth)

#info = client.get_symbol_info(pair)
#print (info)

# trades = client.get_recent_trades(symbol=pair)
# print (len(trades))
# print (trades)


# trades = client.get_historical_trades(symbol=pair)
# print (len(trades))
# print (trades)

#agg_trades = client.aggregate_trade_iter(symbol=pair, start_str='30 minutes ago UTC')
'''

# Function definition
def buy_limit_order(_symbol, _quantity, _price):
    global placed_buy_order
    global bought_price

    str_price = str(_price)

    order = client.order_limit_buy(
    symbol=_symbol,
    quantity=_quantity,
    price=str_price)

    placed_buy_order = True
    bought_price = float(_price)

    return order['orderId']

def sell_limit_order(_symbol, _quantity, _price):
    global placed_buy_order
    global sold_price

    str_price = str(_price)

    order = client.order_limit_sell(
    symbol=_symbol,
    quantity=_quantity,
    price=str_price)

    placed_buy_order = False
    sold_price = float(_price)

    return order['orderId']
# End of Function definition


# this would result in verify: False and timeout: 5 for the get_all_orders call
client = Client(api_key, api_secret, {"verify": True, "timeout": 20})

while True:
    # Check there is open order or not
    orders = client.get_open_orders(symbol=pair)
    print ("Current opened orders: ", len(orders))

    #opened_order_counter = 0
    while (len(orders) > 0):
        # orders = client.get_open_orders(symbol=pair)
        # time.sleep(30)
        # opened_order_counter = opened_order_counter + 1
        # if opened_order_counter == 3:
        #     opened_order_counter = 0
        #     client.cancel_order(
        #         symbol=pair,
        #         orderId=str(ordered_id))
        #     time.sleep(30)
        #     break;
        orders = client.get_open_orders(symbol=pair)
        time.sleep(30)

    curr_price_dict = client.get_symbol_ticker(symbol=pair)
    current_price = float(curr_price_dict['price'])
    print ("Last matched price: ", current_price)

    print ("placed_buy_order: ", placed_buy_order)

    if placed_buy_order:
        selling_price = float(bought_price * (1 + profit))
        if selling_price <= current_price:
            ordered_id = sell_limit_order(pair, quantity, current_price)
            print ("Latest best selling order: ", str(ordered_id))
        # elif (selling_price - current_price * (1 + best_profit)) <= 0:
        #     print ("Selling price: ", str(selling_price))
        #     ordered_id = sell_limit_order(pair, quantity, selling_price)
        #     print ("Latest best profit selling order: ", str(ordered_id))
        # elif current_price <= MAX and current_price >= MIN:
        #     ordered_id = sell_limit_order(pair, quantity, current_price)
        #     print ("Latest selling order: ", str(ordered_id))
    else:
        buying_price = float(sold_price * (1 - profit))
        lowest_price_bid = float(sold_price * (1 - lowest_profit))
        highest_price_bid = float(sold_price * (1 + lowest_profit))
        if buying_price >= current_price:
            ordered_id = buy_limit_order(pair, quantity, current_price)
            print ("Latest best buying order: ", str(ordered_id))
        elif current_price <= highest_price_bid and current_price >= lowest_price_bid:
            ordered_id = buy_limit_order(pair, quantity, current_price)
            print ("Latest alternative buying order: ", str(ordered_id))


    time.sleep(60)







