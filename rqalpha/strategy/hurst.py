import pandas as pd
import numpy as np
from pandas import Series
from pandas import DataFrame


def init(context):
    context.hs300 = "000300.XSHG"
    # window must larger than 64
    context.WINDOW = 101


def handle_bar(context, bar_dict):
    time_series = history_bars(context.hs300, context.WINDOW, '1d', 'close')
    hurstex = hurst(time_series)
    plot("hurst", hurstex)
    '''
    if abs(hurstex-0.5)<0.05:
        order_target_value(context.s,0)
    elif hurstex>0.5 and :
        order_target_percent(context.s,1)
    elif hurst.ex<0.5:
    '''

    '''
    # 买入卖出条件需要再次调试
    curPosition = context.portfolio.positions[context.hs300].quantity
    if hurstex > 0.55:
        if curPosition == 0:
            order_target_percent(context.hs300, 1)
    elif hurstex < 0.45:
        if curPosition > 0:
            order_target_value(context.hs300, 0)
    '''


def hurst(history):
    daily_return = list(Series(history).pct_change())[1:]
    ranges = ['1', '2', '4', '8', '16', '32']
    lag = Series(index=ranges)
    for i in range(len(ranges)):
        if i == 0:
            lag[i] = len(daily_return)
        else:
            lag[i] = lag[0] // (2 ** i)

    ARS = Series(index=ranges)

    for r in ranges:
        # RS用来存储每一种分割方式中各个片段的R/S值
        RS = list()
        # 第i个片段
        for i in range(int(r)):
            # 用Range存储每一个片段数据
            Range = daily_return[int(i * lag[r]):int((i + 1) * lag[r])]
            mean = np.mean(Range)
            Deviation = Range - mean
            maxi = max(Deviation)
            mini = min(Deviation)
            RS.append(maxi - mini)
            sigma = np.std(Range)
            RS[i] = RS[i] / sigma

        ARS[r] = np.mean(RS)

    lag = np.log10(lag)
    ARS = np.log10(ARS)
    hurst_exponent = np.polyfit(lag, ARS, 1)
    hurst = hurst_exponent[0] * 2
    return hurst