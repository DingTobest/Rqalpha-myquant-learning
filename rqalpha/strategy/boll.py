from rqalpha.api import *

import talib

def init(context):
    context.hs300 = "000300.XSHG"

    context.algoInfo = context.hs300

    context.SHORTPERIOD = 20

def handle_bar(context, bar_dict):
    prices = history_bars(context.algoInfo, context.SHORTPERIOD+1, '1d', 'close')
    max_price = max(prices)
    min_price = min(prices)

    print(type(prices))

    print(str(max_price) + ":" + str(min_price))

    upperband, middleband, lowerband = talib.BBANDS(prices, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)

    # plot("upperband", upperband[-1])
    # plot("middleband", middleband[-1])
    # plot("lowerband", lowerband[-1])
    # plot("close", prices[-1])

    cha = (max_price - min_price) / (upperband[-1] - lowerband[-1])
    plot("cha", cha)

    # cur_position = context.portfolio.positions[context.algoInfo].quantity
    #
    # shares = context.portfolio.cash/bar_dict[context.algoInfo].close
    #
    # if short_avg[-1] > prices[-1] and short_avg[-2] < prices[-2] and cur_position > 0:
    #     order_target_value(context.algoInfo, 0)
    #
    # if short_avg[-1] < prices[-1] > 0 and short_avg[-2] > prices[-2]:
    #     order_shares(context.algoInfo, shares)
