# 可以自己import我们平台支持的第三方python模块，比如pandas、numpy等。
import math
import pandas
from pandas import Series
import numpy as np
import talib


# 在这个方法中编写任何的初始化逻辑。context对象将会在你的算法策略的任何方法之间做传递。
def init(context):
    # 实时打印日志
    # scheduler.run_monthly(judge, monthday=1)
    scheduler.run_weekly(judge, weekday=1)
    # scheduler.run_daily(judge)
    scheduler.run_daily(stoploss)
    context.stocks = ["511010.XSHG", "510300.XSHG", "510500.XSHG"]
    update_universe(context.stocks)
    context.marketval = 0
    context.positionIndex = -1
    context.trend = ""

def judge(context, bar_dict):
    GUO = history_bars(context.stocks[0], 120, "1d", "close")
    HS300 = history_bars(context.stocks[1], 120, "1d", "close")
    S500 = history_bars(context.stocks[2], 120, "1d", "close")

    mentguo = calMent(GUO)
    ment300 = calMent(HS300)
    ment500 = calMent(S500)

    # logger.info(str(ment300) + " "+ str(ment500) + " "+ str(mentguo))
    if mentguo > max(ment300, ment500):
        if context.stocks[1] in context.portfolio.positions:
            order_target_percent(context.stocks[1], 0)
        if context.stocks[2] in context.portfolio.positions:
            order_target_percent(context.stocks[2], 0)
        # if mentguo > 0:
        if context.stocks[0] not in context.portfolio.positions:
            # order_target_percent(context.stocks[0], 1)
            buyStocks(context, context.stocks[0], GUO)
            context.positionIndex = 0
            # logger.info("买入国债:" + str(context.portfolio.positions[context.stocks[0]].quantity))
    elif ment300 > max(mentguo, ment500):
        if context.stocks[0] in context.portfolio.positions:
            order_target_percent(context.stocks[0], 0)
        if context.stocks[2] in context.portfolio.positions:
            order_target_percent(context.stocks[2], 0)
        # if ment300 > 0:
        if context.stocks[1] not in context.portfolio.positions:
            # order_target_percent(context.stocks[1], 1)
            buyStocks(context, context.stocks[1], HS300)
            context.positionIndex = 1
            # logger.info("买入300:" + str(context.portfolio.positions[context.stocks[1]].quantity))
    elif ment500 > max(ment300, mentguo):
        if context.stocks[1] in context.portfolio.positions:
            order_target_percent(context.stocks[1], 0)
        if context.stocks[0] in context.portfolio.positions:
            order_target_percent(context.stocks[0], 0)
        # if ment500 > 0:
        if context.stocks[2] not in context.portfolio.positions:
            # order_target_percent(context.stocks[2], 1)
            buyStocks(context, context.stocks[2], S500)
            context.positionIndex = 2
            # logger.info("买入500:" + str(context.portfolio.positions[context.stocks[2]].quantity))
    context.marketval = context.portfolio.market_value


def calMent(close):
    # return (close[19] - close[0]) / close[0]
    return (close[-1] - close[-20]) / close[-20]

def timming(prices):
    short_avg = talib.SMA(prices, 20)
    long_avg = talib.SMA(prices, 120)

    timmingData = (short_avg[-1] / long_avg[-1]) - 1

    if timmingData > 0.01:
        return 'up'
    elif timmingData < -0.01:
        return 'down'
    else:
        return 'Shock'

def buyStocks(context, stock, prices):
    # order_target_percent(stock, 1)

    context.trend = timming(prices)
    if context.trend == 'up':
        order_target_percent(stock, 1)
    elif context.trend == 'Shock':
        order_target_percent(stock, 0.6)
    else:
        return

def stoploss(context, bar_dict):
    if context.trend != 'up':
        return

    if context.positionIndex == 1:
        prices = history_bars(context.stocks[1], 21, "1d", "close")
    elif context.positionIndex == 2:
        prices = history_bars(context.stocks[2], 21, "1d", "close")
    else:
        return

    short_avg = talib.SMA(prices, 20)

    if prices[-1] < short_avg[-1] and prices[-2] > short_avg[-2]:
        for stock in context.portfolio.positions:
            if bar_dict[stock].is_trading:
                order_target_percent(stock, 0)

