import pandas as pd
import numpy as np
from pandas import Series
from pandas import DataFrame

from statsmodels import regression


def init(context):
    context.hs300 = "000300.XSHG"
    # window must larger than 64
    context.WINDOW = 400


def handle_bar(context, bar_dict):
    time_series = history_bars(context.hs300, context.WINDOW, '1d', 'close')
    hurstex = hurst(time_series)
    #hurstex = Hurst(time_series, 318)
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

# def hurst(ts):
#
#     if not isinstance(ts, Iterable):
#         print 'error'
#         return
#
#     n_min, n_max = 2, len(ts) // 3
#     RSlist = []
#     for cut in range(n_min, n_max):
#         children = len(ts) // cut
#         children_list = [ts[i * children:(i + 1) * children] for i in range(cut)]
#         L = []
#         for a_children in children_list:
#             Ma = np.mean(a_children)
#             Xta = Series(map(lambda x: x - Ma, a_children)).cumsum()
#             Ra = max(Xta) - min(Xta)
#             Sa = np.std(a_children)
#             rs = Ra / Sa
#             L.append(rs)
#         RS = np.mean(L)
#         RSlist.append(RS)
#     return np.polyfit(np.log(range(2 + len(RSlist), 2, -1)), np.log(RSlist), 1)[0]

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
            Deviation = np.cumsum(Range - mean,axis=0)
            #Deviation = Range - mean

            maxi = max(Deviation)
            mini = min(Deviation)
            RS.append(maxi - mini)
            sigma = np.std(Range)
            RS[i] = RS[i] / sigma

        ARS[r] = np.mean(RS)

    lag = np.log10(lag)
    ARS = np.log10(ARS)
    hurst_exponent = np.polyfit(lag, ARS, 1)
    hurst = hurst_exponent[0]
    return hurst

# def Hurst(XX,T):
#     XX = np.array(XX)    #读入时间序列,一维矩阵
#     Lenth = XX.shape[0]     #读取时间序列的总长度，
#     hurst = np.zeros(Lenth)
#     for i in xrange(T,Lenth):
#         X=XX[i-T:i+1]
#         RS = np.zeros(T)      #array
#         logRS = np.zeros(T)   #array
#         logn = np.zeros(T)   #array
#         for n in xrange(10,T):  #每个长度计算一次
#             a = int(T/n)
#             x1 = X[0:n*a].reshape(n,a)   #正向分段,n行a列，每一列为一个子序列
#             x2 = X[(T - a * n): T].reshape(n,a)  #反向分段,n行a列，每一列为一个子序列
#             m1 = np.mean(x1,axis=0)     #按列取均值，1行a列
#             m2 = np.mean(x2,axis=0)     #按列取均值，1行a列
#             p = np.ones((n,1))              #n行，1列
#             y1 = x1 - p * m1                  #n行，a列，对每一列求离差
#             y2 = x2 - p * m2                  #n行，a列，对每一列求离差
#             sig1 = np.std(x1,axis=0)             #1行，a列，对每一列求标准差
#             sig2 = np.std(x2,axis=0)             #1行，a列，对每一列求标准差
#             sum1 = np.cumsum(y1,axis=0)          #n行，a列，求累计离差
#             sum2 = np.cumsum(y2,axis=0)          #n行，a列，求累计离差
#             r1 = np.max(sum1,axis=0) - np.min(sum1,axis=0)      #%1行，a列
#             r2 = np.max(sum2,axis=0) - np.min(sum2,axis=0)      #%1行，a列
#             RS1[n] = np.mean(r1 / sig1,axis=0)        #1行，1列
#             RS2[n] = np.mean(r2 / sig2,axis=0)        #1行，1列
#             RS[n] = 0.5*RS1[n] + 0.5*RS2[n]
#             logRS[n] = np.log(RS[n])
#             logn[n] = np.log(n)
#         R = regression.linear_model.OLS(logRS[10:T],logn[10:T]).fit()
#         hurst[i] = R.params[0]
#     return hurst