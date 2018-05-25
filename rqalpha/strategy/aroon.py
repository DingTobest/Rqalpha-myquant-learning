# -*- coding: utf-8 -*-
# @Time    : 2018-04-06 16:29
# @Author  : Dingzh.tobest
# 文件描述  ： AROON指标测试

import talib
import numpy as np


def init(context):
    # 在context中保存全局变量
    context.s1 = "000300.XSHG"


# before_trading此函数会在每天策略交易开始前被调用，当天只会被调用一次
def before_trading(context):
    pass


# 你选择的证券的数据更新将会触发此段逻辑，例如日或分钟历史数据切片或者是实时数据切片更新
def handle_bar(context, bar_dict):
    highs = history_bars(context.s1, 60, '1d', 'high')
    lows = history_bars(context.s1, 60, '1d', 'low')

    down, up = talib.AROON(np.array(highs), np.array(lows), timeperiod=24)
    down = down[-1]
    up = up[-1]

    if up > down:
        order_target_percent(context.s1, 0.95)
    else:
        order_target_percent(context.s1, 0.0)


# after_trading函数会在每天交易结束后被调用，当天只会被调用一次
def after_trading(context):
    pass