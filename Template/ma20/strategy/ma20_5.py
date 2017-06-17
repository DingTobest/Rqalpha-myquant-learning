from rqalpha.api import *

import talib

def init(context):
    context.szzs = "000001.XSHG"
    context.hs300 = "000300.XSHG"
    context.cybz = "399006.XSHE"

    context.algoInfo = context.hs300

    context.SHORTPERIOD = 5

def handle_bar(context, bar_dict):
    prices = history_bars(context.algoInfo, context.SHORTPERIOD+1, '1d', 'close')

    short_avg = talib.SMA(prices, context.SHORTPERIOD)

    plot("short avg", short_avg[-1])

    cur_position = context.portfolio.positions[context.algoInfo].quantity

    shares = context.portfolio.cash/bar_dict[context.algoInfo].close

    if short_avg[-1] > prices[-1] and short_avg[-2] < prices[-2] and cur_position > 0:
        order_target_value(context.algoInfo, 0)

    if short_avg[-1] < prices[-1] > 0 and short_avg[-2] > prices[-2]:
        order_shares(context.algoInfo, shares)
