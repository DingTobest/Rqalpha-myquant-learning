from rqalpha.api import *

import talib
import copy
import numpy as np


def init(context):
    # 回测参数部分
    context.szzs = "000001.XSHG"
    context.hs300 = "000300.XSHG"
    context.cybz = "399006.XSHE"
    context.shenzzs = "399001.XSHE"

    context.algoInfo = context.hs300

    # 策略参数部分，对此部分进行调整可用于参数优化
    context.n1 = 4  # 买入启动和卖出启动形态形成的价格比较滞后期数
    context.n2 = 4  # 买入启动和卖出启动形态形成的价格关系向连续个数
    context.n3 = 4  # 模型计数阶段最终信号发出所需的计数值

    # 策略中间变量
    context.pCount = 0              # 用于价格计数与n2进行比较
    context.startBuyFlag = False    # 买入启动开始标志
    context.startSellFalg = False   # 卖出启动开始标志

    context.buyCount = 0    # 买入计数
    context.sellCount = 0   # 卖出计数

    context.minPrice = 0    # 买入计数过程中最高价
    context.maxPrice = 0    # 卖出计数过程中最低价

def td(context, close, high, low):
    if close[-1] > close[-2] and close[-2] > close[-3]:
        context.pCount += 1
    elif close[-1] < close[-2] and close[-2] < close[-3]:
           context.pCount -= 1
    elif close[-1] == close[-2]:
        context.pCount = context.pCount
    else:
        context.pCount = 0

    if context.pCount == context.n2:
        context.startBuyFlag = True
        context.pCount = 0
        context.buyCount = 0
        return 1
    elif context.pCount == -context.n2:
        context.startSellFlag = True
        context.pCount = 0
        context.sellCount = 0
        return -1

    if close[-1] < context.minPrice and context.minPrice != 0:
        context.pCount = 0
        context.sellCount = 0
        context.minPrice = 0
        return -1
    elif close[-1] > context.maxPrice and context.maxPrice != 0:
        context.pCount = 0
        context.buyCount = 0
        context.maxPrice = 0
        return 1

    if context.startBuyFlag:
        if close[-1] >= high[1] and close[-1] >= high[2]:
            context.buyCount += 1
        if high[-1] > high[1]:
            context.buyCount += 1
        if close[-1] > close[1]:
            context.buyCount += 1

        if context.minPrice < low[-1] or context.minPrice == 0:
            context.minPrice = low[-1]

        if context.buyCount >= context.n3:
            context.startBuyFlag = False
            context.buyCount = 0
            context.maxPrice = 0
            return 1
        else:
            return 0
    elif context.startSellFalg:
        if close[-1] <= low[1] and close[-1] <= low[2]:
            context.sellCount += 1
        if low[-1] < low[1]:
            context.sellCount += 1
        if close[-1] < close[1]:
            context.sellCount += 1

        if context.maxPrice > high[-1] or context.minPrice == 0:
            context.maxPrice = high[-1]

        if context.sellCount >= context.n3:
            context.startSellFlag = False
            context.sellCount = 0
            context.minPrice = 0
            return -1
        else:
            return 0

def handle_bar(context, bar_dict):
    close = history_bars(context.algoInfo, context.n1, '1d', 'close')
    high = history_bars(context.algoInfo, context.n1, '1d', 'high')
    low = history_bars(context.algoInfo, context.n1, '1d', 'low')

    tradeFlag = td(context, close, high, low)

    if tradeFlag == 1:
        curPosition = context.portfolio.positions[context.algoInfo].quantity
        if curPosition == 0:
            order_target_percent(context.algoInfo, 1)
    elif tradeFlag == -1:
        curPosition = context.portfolio.positions[context.algoInfo].quantity
        if curPosition > 0:
            order_target_value(context.algoInfo, 0)
