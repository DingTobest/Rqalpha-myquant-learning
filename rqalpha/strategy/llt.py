from rqalpha.api import *

import talib
import copy
import numpy as np
import math


def init(context):
    context.szzs = "000001.XSHG"
    context.hs300 = "000300.XSHG"
    context.cybz = "399006.XSHE"
    context.shenzzs = "399001.XSHE"

    context.LLTD = 60

    context.algoInfo = context.szzs

    context.LLTArray = []

def llt(context, closePrice):
    cp = copy.deepcopy(closePrice)

    if len(context.LLTArray) == 0:
        context.LLTArray.append(closePrice[-3])

    if len(context.LLTArray) == 1:
        context.LLTArray.append(closePrice[-2])

    a = 2.0/(context.LLTD +1.0)
    lltResult = (a-(a*a)/4)*cp[-1]+((a*a)/2)*cp[-2]-(a-3*(a*a)/4)*cp[-3]+2*(1-a)*context.LLTArray[-1]-(1-a)*(1-a)*context.LLTArray[-2]
    context.LLTArray.append(lltResult)

def handle_bar(context, bar_dict):
    prices = history_bars(context.algoInfo, 4, '1d', 'close')
    llt(context, prices)

    plot("close", prices[-1])
    plot("llt", context.LLTArray[-1])

    k = math.atan(context.LLTArray[-1] / context.LLTArray[-2] - 1) * 100
    # k = context.LLTArray[-1] - context.LLTArray[-2]
    print(str(k))

    if k < 0:
        curPosition = context.portfolio.positions[context.algoInfo].quantity
        if curPosition > 0:
            order_target_value(context.algoInfo, 0)
    elif k > 0:
        curPosition = context.portfolio.positions[context.algoInfo].quantity
        if curPosition == 0:
            order_target_percent(context.algoInfo, 1)


    #
    # if context.LLTArray[-1] > prices[-1] and context.LLTArray[-2] < prices[-2] or context.LLTArray[-1] < context.LLTArray[-2]:
    #    curPosition = context.portfolio.positions[context.algoInfo].quantity
    #    if curPosition > 0:
    #        print("-----------------------")
    #        print("Sell[LLTArray],", context.LLTArray[-1])
    #        print("Sell[prices],", prices[-1])
    #        order_target_value(context.algoInfo, 0)
    #        print("-----------------------")
    # elif context.LLTArray[-1] < prices[-1] and context.LLTArray[-2] > prices[-2] and context.LLTArray[-1] > context.LLTArray[-2]:
    #    curPosition = context.portfolio.positions[context.algoInfo].quantity
    #    if curPosition == 0:
    #        print("-----------------------")
    #        print("Buy[LLTArray],", context.LLTArray[-1])
    #        print("Buy[prices],", prices[-1])
    #        order_target_percent(context.algoInfo, 1)
    #        print("-----------------------")

