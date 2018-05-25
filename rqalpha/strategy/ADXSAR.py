# -*- coding: utf-8 -*-
# @Time    : 2018-05-09 16:28
# @Author  : Dingzh.tobest
# 文件描述  ：

# 可以自己import我们平台支持的第三方python模块，比如pandas、numpy等。
import talib as ta
import numpy as np


# 在这个方法中编写任何的初始化逻辑。context对象将会在你的算法策略的任何方法之间做传递。
def init(context):
    # context内引入全局变量:沪深主力连续合约（偷懒直接用米筐主力了。。。）
    context.s1 = "IF88"

    context.window = 80

    context.selOpen_Flag = False
    context.buyOpen_Flag = False

    # 据说SAR的使用需要根据势头改变大小哈，
    context.acceleration = 0.05

    # 初始化时订阅合约行情。订阅之后的合约行情会在handle_bar中进行更新。
    subscribe(context.s1)

    # 判断指标（搓键盘方便，无实际意义）
    context.JQ_selOpen = False
    context.JW_selOpen = False
    context.JE_selOpen = False
    context.JR_selOpen = False
    context.JQ_buyOpen = False
    context.JW_buyOpen = False
    context.JE_buyOpen = False
    context.JR_buyOpen = False
    context.JQ_selClos = False
    context.JW_selClos = False
    context.JE_selClos = False
    context.JR_selClos = False
    context.JQ_buyClos = False
    context.JW_buyClos = False
    context.JE_buyClos = False
    context.JR_buyClos = False

    scheduler.run_weekly(ADX, weekday=5)


def ADX(context, bar_dict):
    context.JQ_selOpen = (context.ADX[-1] >= 20) & (context.ADX[-2] >= 20) & (context.ADX[-1] <= 30) & (
    context.ADX[-2] <= 30)
    context.JQ_buyOpen = context.JQ_selOpen


# before_trading此函数会在每天策略交易开始前被调用，当天只会被调用一次
def before_trading(context):
    prices = history_bars(context.s1, context.window, '1d', fields=['high', 'low', 'close', 'open'])
    highP = prices['high']
    lowP = prices['low']
    closeP = prices['close']
    openP = prices['open']

    context.ADX = ta.ADXR(highP, lowP, closeP, timeperiod=14)
    context.Pdi = ta.PLUS_DI(highP, lowP, closeP, timeperiod=14)
    context.Ndi = ta.MINUS_DI(highP, lowP, closeP, timeperiod=14)

    context.MA_tw = ta.MA(closeP, timeperiod=20)[-5:]
    context.MA_fi = ta.MA(closeP, timeperiod=50)[-5:]
    context.MA_fork = context.MA_tw > context.MA_fi

    context.SAR = ta.SAR(highP, lowP, acceleration=context.acceleration, maximum=0.2)

    # context.JQ_selOpen = (context.ADX[-1]>=20) #& (context.ADX[-2]>=20) & (context.ADX[-1]<=30) & (context.ADX[-2]<=30)
    context.JW_selOpen = (context.Pdi[-1] <= context.Ndi[-1]) & (context.Pdi[-2] >= context.Ndi[-2])
    context.JE_selOpen = (context.MA_fork[-1]) & (context.MA_fork[-2]) & (not context.MA_fork[-3])
    context.JR_selOpen = (context.SAR[-1] >= 0.95 * openP[-1]) & (context.SAR[-2] <= 1.05 * closeP[-2])
    context.J_selOpen = context.JQ_selOpen & context.JW_selOpen & context.JE_selOpen & context.JR_selOpen

    # context.JQ_buyOpen = context.JQ_selOpen
    context.JW_buyOpen = (context.Pdi[-1] >= context.Ndi[-1]) & (context.Pdi[-2] <= context.Ndi[-2])
    context.JE_buyOpen = (not context.MA_fork[-1]) & (not context.MA_fork[-2]) & (not context.MA_fork[-3])
    context.JR_buyOpen = (context.SAR[-2] >= 0.95 * openP[-2]) & (context.SAR[-1] <= 1.05 * closeP[-1])
    context.J_buyOpen = context.JQ_buyOpen & context.JW_buyOpen & context.JE_buyOpen & context.JR_buyOpen


# 你选择的期货数据更新将会触发此段逻辑，例如日线或分钟线更新
def handle_bar(context, bar_dict):
    # 开始编写你的主要的算法逻辑
    # bar_dict[order_book_id] 可以获取到当前期货合约的bar信息
    # context.portfolio 可以获取到当前投资组合信息

    # plot('A',context.JQ_buyOpen)
    # plot('B',context.JW_buyOpen)
    # plot('C',context.JE_buyOpen)
    # plot('D',context.JR_buyOpen)

    sq = context.portfolio.positions[context.s1].sell_quantity
    bq = context.portfolio.positions[context.s1].buy_quantity

    if context.J_selOpen:
        sell_open(context.s1, 1)
        print([sq, bq])

    if context.J_buyOpen:
        buy_open(context.s1, 1)
        print([sq, bq])

    if sq & context.J_buyOpen:
        buy_close(context.s1, sq)

    if bq & context.J_selOpen:
        sell_close(context.s1, bq)


# after_trading函数会在每天交易结束后被调用，当天只会被调用一次
def after_trading(context):
    prices = history_bars(context.s1, 2, '1d', fields='high')

    accMax = context.acceleration <= 0.2

    if accMax & (prices[-2] < prices[-1]):
        context.acceleration = context.acceleration + 0.02

    sq = context.portfolio.positions[context.s1].sell_quantity
    bq = context.portfolio.positions[context.s1].buy_quantity

    if (sq == 0) & (bq == 0):
        context.acceleration = 0.05