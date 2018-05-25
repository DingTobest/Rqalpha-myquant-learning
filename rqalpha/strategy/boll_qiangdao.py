# -*- coding: utf-8 -*-
# @Time    : 2018-04-06 16:43
# @Author  : Dingzh.tobest
# 文件描述  ：

import talib
import numpy as np


def init(context):
    # context内引入全局变量s1
    context.s1 = get_dominant_future('J')  # 自制主力连续
    # 初始化context.last_main_symbol
    context.last_main_symbol = context.s1
    # 将判断主力是否更新的flag初始设置为False
    context.main_changed = False
    subscribe(context.s1)

    context.bollLen = 50  # 布林通道参数
    context.Offset = 1.25  # 布林通道参数
    context.rocCalLen = 30  # 过滤器参数
    context.liqLen = 50  # 自适应出场均线参数
    context.liqDays = context.liqLen


def before_trading(context):  # 每天开盘前判断主力合约是否更新。
    context.s1 = get_dominant_future('J')
    if context.last_main_symbol != context.s1:
        subscribe(context.s1)
        # 如果更新了，设置main_changed这个flag为True
        context.main_changed = True


def handle_bar(context, bar_dict):
    sell_qty = context.portfolio.positions[context.s1].sell_quantity
    buy_qty = context.portfolio.positions[context.s1].buy_quantity

    # 检测当前主力合约，如果发生变化，先对原有合约平仓
    if context.main_changed:
        # 主力合约发变化，平仓
        print('Symbol Changed! before:', context.last_main_symbol, 'after: ', context.s1, context.now)
        # 空单平仓
        if context.portfolio.positions[context.last_main_symbol].sell_quantity != 0:
            buy_close(context.last_main_symbol, 1)
            print('close short:', context.now)
        # 多头平仓
        if context.portfolio.positions[context.last_main_symbol].buy_quantity != 0:
            sell_close(context.last_main_symbol, 1)
            print('close long', context.now)
        context.main_changed = False
        context.last_main_symbol = context.s1

    close = history_bars(context.s1, context.bollLen + 1, '1d', 'close')
    high = history_bars(context.s1, context.bollLen + 1, '1d', 'high')
    low = history_bars(context.s1, context.bollLen + 1, '1d', 'low')

    # 布林通道中轨
    MidLine = talib.SMA(close, context.bollLen)
    Band = np.std(close[-context.bollLen:], ddof=1)  # 计算样本方差
    # 布林上下轨
    UpBand = MidLine + context.Offset * Band
    DnBand = MidLine - context.Offset * Band
    plot('MidLine', MidLine[-1])
    plot('UpBand', UpBand[-1])
    plot('DnBand', DnBand[-1])
    # 进场过滤器
    rocCalc = close - close[-context.rocCalLen]

    # 多头
    # 开仓：满足过滤条件，并且价格突破布林通道上轨
    if sell_qty == 0 and buy_qty == 0:
        # 设置自适应出场均线
        context.liqDays = context.liqLen
        if rocCalc[-1] > 0 and bar_dict[context.s1].high >= UpBand[-1]:
            buy_open(context.s1, 1)
    else:
        context.liqDays = context.liqDays - 1
        context.liqDays = max(context.liqDays, 10)
    # 自适应均线
    liqPoint = talib.SMA(close, context.liqDays)
    plot('liqPoint', liqPoint[-1])

    # 平仓：当自适应出场均线低于布林通道上轨，并且价格下破自适应出场均线
    if buy_qty != 0 and liqPoint[-1] < UpBand[-1] and bar_dict[context.s1].low < liqPoint[-1]:
        sell_close(context.s1, 1)

    # 空头
    # 开仓：满足过滤条件，并且价格突破布林通道下轨
    if sell_qty == 0 and buy_qty == 0:
        if rocCalc[-1] < 0 and bar_dict[context.s1].low <= DnBand[-1]:
            sell_open(context.s1, 1)
    # 平仓：当自适应出场均线高于布林通道下轨，并且价格上破自适应出场均线
    if sell_qty != 0 and liqPoint[-1] > DnBand[-1] and bar_dict[context.s1].high > liqPoint[-1]:
        buy_close(context.s1, 1)
