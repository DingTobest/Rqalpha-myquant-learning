from rqalpha.api import *

import talib
import copy
import numpy as np


def init(context):
    context.szzs = "000001.XSHG"
    context.hs300 = "000300.XSHG"
    context.cybz = "399006.XSHE"

    context.LLTD = 30

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
    plot("llt", context.LLTArray[-1])
    plot("Close", prices[-1])

    if context.LLTArray[-1] - context.LLTArray[-2] < 0:
        curPosition = context.portfolio.positions[context.algoInfo].quantity
        if curPosition > 0:
            order_target_value(context.algoInfo, 0)
    elif context.LLTArray[-1] - context.LLTArray[-2] > 0:
        curPosition = context.portfolio.positions[context.algoInfo].quantity
        if curPosition == 0:
            order_target_percent(context.algoInfo, 1)

