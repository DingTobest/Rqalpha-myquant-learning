import pandas as pd
import numpy as np
import statsmodels.api as sm
import talib

def init(context):
    # 在context中保存全局变量
    context.hs300 = "000300.XSHG"
    context.n1 = 18
    context.s1 = 1
    context.s2 = 0.8

def before_trading(context):
    pass

def handle_bar(context, bar_dict):
    high = history_bars(context.hs300, context.n1, '1d', 'high')
    low = history_bars(context.hs300, context.n1, '1d', 'low')

    close = history_bars(context.hs300, context.n1 + 3, '1d', 'close')

    sma = talib.SMA(close, context.n1)

    low = sm.add_constant(low)
    ols = sm.OLS(high,low)
    ols = ols.fit()
    rsrs = ols.params[1]
    if rsrs > context.s1 and sma[-1] > sma[-3]:
        order_percent(context.hs300,1)
    elif rsrs < context.s2:
        order_percent(context.hs300,-1)
    else:
        order_percent(context.hs300,0)

def after_trading(context):
    pass