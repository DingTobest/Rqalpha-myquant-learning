# coding=utf-8

import talib
import numpy as np

'''
 TALIB综合调用函数
 name:函数名称
 price_h：最高价
 price_l：最低价
 price_c：收盘价
 price_v：成交量
 price_o：开盘价
'''
def ta(name, price_h, price_l, price_c, price_v, price_o):
    # function 'MAX'/'MAXINDEX'/'MIN'/'MININDEX'/'MINMAX'/'MINMAXINDEX'/'SUM' is missing
    if name == 'AD':
        return talib.AD(np.array(price_h), np.array(price_l), np.array(price_c), np.asarray(price_v, dtype='float'))
    if name == 'ADOSC':
        return talib.ADOSC(np.array(price_h), np.array(price_l), np.array(price_c), np.asarray(price_v, dtype='float'),
                        fastperiod=2, slowperiod=10)
    if name == 'ADX':
        return talib.ADX(np.array(price_h), np.array(price_l), np.asarray(price_c, dtype='float'), timeperiod=14)
    if name == 'ADXR':
        return talib.ADXR(np.array(price_h), np.array(price_l), np.asarray(price_c, dtype='float'), timeperiod=14)
    if name == 'APO':
        return talib.APO(np.asarray(price_c, dtype='float'), fastperiod=12, slowperiod=26, matype=0)
    if name == 'AROON':
        AROON_DWON, AROON2_UP = talib.AROON(np.array(price_h), np.asarray(price_l, dtype='float'), timeperiod=90)
        return (AROON_DWON, AROON2_UP)
    if name == 'AROONOSC':
        return talib.AROONOSC(np.array(price_h), np.asarray(price_l, dtype='float'), timeperiod=14)
    if name == 'ATR':
        return talib.ATR(np.array(price_h), np.array(price_l), np.asarray(price_c, dtype='float'), timeperiod=14)
    if name == 'AVGPRICE':
        return talib.AVGPRICE(np.array(price_o), np.array(price_h), np.array(price_l), np.asarray(price_c, dtype='float'))
    if name == 'BBANDS':
        BBANDS1, BBANDS2, BBANDS3 = talib.BBANDS(np.asarray(price_c, dtype='float'), matype=MA_Type.T3)
        return BBANDS1
    if name == 'BETA':
        return talib.BETA(np.array(price_h), np.asarray(price_l, dtype='float'), timeperiod=5)
    if name == 'BOP':
        return talib.BOP(np.array(price_o), np.array(price_h), np.array(price_l), np.asarray(price_c, dtype='float'))
    if name == 'CCI':
        return talib.CCI(np.array(price_h), np.array(price_l), np.asarray(price_c, dtype='float'), timeperiod=14)
    if name == 'CDL2CROWS':
        return talib.CDL2CROWS(np.array(price_o), np.array(price_h), np.array(price_l), np.asarray(price_c, dtype='float'))
    if name == 'CDL3BLACKCROWS':
        return talib.CDL3BLACKCROWS(np.array(price_o), np.array(price_h), np.array(price_l),
                                 np.asarray(price_c, dtype='float'))
    if name == 'CDL3INSIDE':
        return talib.CDL3INSIDE(np.array(price_o), np.array(price_h), np.array(price_l),
                             np.asarray(price_c, dtype='float'))
    if name == 'CDL3LINESTRIKE':
        return talib.CDL3LINESTRIKE(np.array(price_o), np.array(price_h), np.array(price_l),
                                 np.asarray(price_c, dtype='float'))
    if name == 'CDL3OUTSIDE':
        return talib.CDL3OUTSIDE(np.array(price_o), np.array(price_h), np.array(price_l),
                              np.asarray(price_c, dtype='float'))
    if name == 'CDL3STARSINSOUTH':
        return talib.CDL3STARSINSOUTH(np.array(price_o), np.array(price_h), np.array(price_l),
                                   np.asarray(price_c, dtype='float'))
    if name == 'CDL3WHITESOLDIERS':
        return talib.CDL3WHITESOLDIERS(np.array(price_o), np.array(price_h), np.array(price_l),
                                    np.asarray(price_c, dtype='float'))
    if name == 'CDLABANDONEDBABY':
        return talib.CDLABANDONEDBABY(np.array(price_o), np.array(price_h), np.array(price_l),
                                   np.asarray(price_c, dtype='float'), penetration=0)
    if name == 'CDLADVANCEBLOCK':
        return talib.CDLADVANCEBLOCK(np.array(price_o), np.array(price_h), np.array(price_l),
                                  np.asarray(price_c, dtype='float'))
    if name == 'CDLBELTHOLD':
        return talib.CDLBELTHOLD(np.array(price_o), np.array(price_h), np.array(price_l),
                              np.asarray(price_c, dtype='float'))
    if name == 'CDLBREAKAWAY':
        return talib.CDLBREAKAWAY(np.array(price_o), np.array(price_h), np.array(price_l),
                               np.asarray(price_c, dtype='float'))
    if name == 'CDLCLOSINGMARUBOZU':
        return talib.CDLCLOSINGMARUBOZU(np.array(price_o), np.array(price_h), np.array(price_l),
                                     np.asarray(price_c, dtype='float'))
    if name == 'CDLCONCEALBABYSWALL':
        return talib.CDLCONCEALBABYSWALL(np.array(price_o), np.array(price_h), np.array(price_l),
                                      np.asarray(price_c, dtype='float'))
    if name == 'CDLCOUNTERATTACK':
        return talib.CDLCOUNTERATTACK(np.array(price_o), np.array(price_h), np.array(price_l),
                                   np.asarray(price_c, dtype='float'))
    if name == 'CDLDARKCLOUDCOVER':
        return talib.CDLDARKCLOUDCOVER(np.array(price_o), np.array(price_h), np.array(price_l),
                                    np.asarray(price_c, dtype='float'), penetration=0)
    if name == 'CDLDOJI':
        return talib.CDLDOJI(np.array(price_o), np.array(price_h), np.array(price_l), np.asarray(price_c, dtype='float'))
    if name == 'CDLDOJISTAR':
        return talib.CDLDOJISTAR(np.array(price_o), np.array(price_h), np.array(price_l),
                              np.asarray(price_c, dtype='float'))
    if name == 'CDLDRAGONFLYDOJI':
        return talib.CDLDRAGONFLYDOJI(np.array(price_o), np.array(price_h), np.array(price_l),
                                   np.asarray(price_c, dtype='float'))
    if name == 'CDLENGULFING':
        return talib.CDLENGULFING(np.array(price_o), np.array(price_h), np.array(price_l),
                               np.asarray(price_c, dtype='float'))
    if name == 'CDLEVENINGDOJISTAR':
        return talib.CDLEVENINGDOJISTAR(np.array(price_o), np.array(price_h), np.array(price_l),
                                     np.asarray(price_c, dtype='float'), penetration=0)
    if name == 'CDLEVENINGSTAR':
        return talib.CDLEVENINGSTAR(np.array(price_o), np.array(price_h), np.array(price_l),
                                 np.asarray(price_c, dtype='float'), penetration=0)
    if name == 'CDLGAPSIDESIDEWHITE':
        return talib.CDLGAPSIDESIDEWHITE(np.array(price_o), np.array(price_h), np.array(price_l),
                                      np.asarray(price_c, dtype='float'))
    if name == 'CDLGRAVESTONEDOJI':
        return talib.CDLGRAVESTONEDOJI(np.array(price_o), np.array(price_h), np.array(price_l),
                                    np.asarray(price_c, dtype='float'))
    if name == 'CDLHAMMER':
        return talib.CDLHAMMER(np.array(price_o), np.array(price_h), np.array(price_l), np.asarray(price_c, dtype='float'))
    if name == 'CDLHANGINGMAN':
        return talib.CDLHANGINGMAN(np.array(price_o), np.array(price_h), np.array(price_l),
                                np.asarray(price_c, dtype='float'))
    if name == 'CDLHARAMI':
        return talib.CDLHARAMI(np.array(price_o), np.array(price_h), np.array(price_l), np.asarray(price_c, dtype='float'))
    if name == 'CDLHARAMICROSS':
        return talib.CDLHARAMICROSS(np.array(price_o), np.array(price_h), np.array(price_l),
                                 np.asarray(price_c, dtype='float'))
    if name == 'CDLHIGHWAVE':
        return talib.CDLHIGHWAVE(np.array(price_o), np.array(price_h), np.array(price_l),
                              np.asarray(price_c, dtype='float'))
    if name == 'CDLHIKKAKE':
        return talib.CDLHIKKAKE(np.array(price_o), np.array(price_h), np.array(price_l),
                             np.asarray(price_c, dtype='float'))
    if name == 'CDLHIKKAKEMOD':
        return talib.CDLHIKKAKEMOD(np.array(price_o), np.array(price_h), np.array(price_l),
                                np.asarray(price_c, dtype='float'))
    if name == 'CDLHOMINGPIGEON':
        return talib.CDLHOMINGPIGEON(np.array(price_o), np.array(price_h), np.array(price_l),
                                  np.asarray(price_c, dtype='float'))
    if name == 'CDLIDENTICAL3CROWS':
        return talib.CDLIDENTICAL3CROWS(np.array(price_o), np.array(price_h), np.array(price_l),
                                     np.asarray(price_c, dtype='float'))
    if name == 'CDLINNECK':
        return talib.CDLINNECK(np.array(price_o), np.array(price_h), np.array(price_l), np.asarray(price_c, dtype='float'))
    if name == 'CDLINVERTEDHAMMER':
        return talib.CDLINVERTEDHAMMER(np.array(price_o), np.array(price_h), np.array(price_l),
                                    np.asarray(price_c, dtype='float'))
    if name == 'CDLKICKING':
        return talib.CDLKICKING(np.array(price_o), np.array(price_h), np.array(price_l),
                             np.asarray(price_c, dtype='float'))
    if name == 'CDLKICKINGBYLENGTH':
        return talib.CDLKICKINGBYLENGTH(np.array(price_o), np.array(price_h), np.array(price_l),
                                     np.asarray(price_c, dtype='float'))

    if name == 'CDLLADDERBOTTOM':
        return talib.CDLLADDERBOTTOM(np.array(price_o), np.array(price_h), np.array(price_l),
                                  np.asarray(price_c, dtype='float'))
    if name == 'CDLLONGLEGGEDDOJI':
        return talib.CDLLONGLEGGEDDOJI(np.array(price_o), np.array(price_h), np.array(price_l),
                                    np.asarray(price_c, dtype='float'))
    if name == 'CDLLONGLINE':
        return talib.CDLLONGLINE(np.array(price_o), np.array(price_h), np.array(price_l),
                              np.asarray(price_c, dtype='float'))
    if name == 'CDLMARUBOZU':
        return talib.CDLMARUBOZU(np.array(price_o), np.array(price_h), np.array(price_l),
                              np.asarray(price_c, dtype='float'))
    if name == 'CDLMATCHINGLOW':
        return talib.CDLMATCHINGLOW(np.array(price_o), np.array(price_h), np.array(price_l),
                                 np.asarray(price_c, dtype='float'))
    if name == 'CDLMATHOLD':
        return talib.CDLMATHOLD(np.array(price_o), np.array(price_h), np.array(price_l),
                             np.asarray(price_c, dtype='float'))
    if name == 'CDLMORNINGDOJISTAR':
        return talib.CDLMORNINGDOJISTAR(np.array(price_o), np.array(price_h), np.array(price_l),
                                     np.asarray(price_c, dtype='float'), penetration=0)
    if name == 'CDLMORNINGSTAR':
        return talib.CDLMORNINGSTAR(np.array(price_o), np.array(price_h), np.array(price_l),
                                 np.asarray(price_c, dtype='float'), penetration=0)
    if name == 'CDLONNECK':
        return talib.CDLONNECK(np.array(price_o), np.array(price_h), np.array(price_l), np.asarray(price_c, dtype='float'))
    if name == 'CDLPIERCING':
        return talib.CDLPIERCING(np.array(price_o), np.array(price_h), np.array(price_l),
                              np.asarray(price_c, dtype='float'))
    if name == 'CDLRICKSHAWMAN':
        return talib.CDLRICKSHAWMAN(np.array(price_o), np.array(price_h), np.array(price_l),
                                 np.asarray(price_c, dtype='float'))
    if name == 'CDLRISEFALL3METHODS':
        return talib.CDLRISEFALL3METHODS(np.array(price_o), np.array(price_h), np.array(price_l),
                                      np.asarray(price_c, dtype='float'))
    if name == 'CDLSEPARATINGLINES':
        return talib.CDLSEPARATINGLINES(np.array(price_o), np.array(price_h), np.array(price_l),
                                     np.asarray(price_c, dtype='float'))
    if name == 'CDLSHOOTINGSTAR':
        return talib.CDLSHOOTINGSTAR(np.array(price_o), np.array(price_h), np.array(price_l),
                                  np.asarray(price_c, dtype='float'))
    if name == 'CDLSHORTLINE':
        return talib.CDLSHORTLINE(np.array(price_o), np.array(price_h), np.array(price_l),
                               np.asarray(price_c, dtype='float'))
    if name == 'CDLSPINNINGTOP':
        return talib.CDLSPINNINGTOP(np.array(price_o), np.array(price_h), np.array(price_l),
                                 np.asarray(price_c, dtype='float'))
    if name == 'CDLSTALLEDPATTERN':
        return talib.CDLSTALLEDPATTERN(np.array(price_o), np.array(price_h), np.array(price_l),
                                    np.asarray(price_c, dtype='float'))
    if name == 'CDLSTICKSANDWICH':
        return talib.CDLSTICKSANDWICH(np.array(price_o), np.array(price_h), np.array(price_l),
                                   np.asarray(price_c, dtype='float'))
    if name == 'CDLTAKURI':
        return talib.CDLTAKURI(np.array(price_o), np.array(price_h), np.array(price_l), np.asarray(price_c, dtype='float'))
    if name == 'CDLTASUKIGAP':
        return talib.CDLTASUKIGAP(np.array(price_o), np.array(price_h), np.array(price_l),
                               np.asarray(price_c, dtype='float'))
    if name == 'CDLTHRUSTING':
        return talib.CDLTHRUSTING(np.array(price_o), np.array(price_h), np.array(price_l),
                               np.asarray(price_c, dtype='float'))
    if name == 'CDLTRISTAR':
        return talib.CDLTRISTAR(np.array(price_o), np.array(price_h), np.array(price_l),
                             np.asarray(price_c, dtype='float'))
    if name == 'CDLUNIQUE3RIVER':
        return talib.CDLUNIQUE3RIVER(np.array(price_o), np.array(price_h), np.array(price_l),
                                  np.asarray(price_c, dtype='float'))
    if name == 'CDLUPSIDEGAP2CROWS':
        return talib.CDLUPSIDEGAP2CROWS(np.array(price_o), np.array(price_h), np.array(price_l),
                                     np.asarray(price_c, dtype='float'))
    if name == 'CDLXSIDEGAP3METHODS':
        return talib.CDLXSIDEGAP3METHODS(np.array(price_o), np.array(price_h), np.array(price_l),
                                      np.asarray(price_c, dtype='float'))
    if name == 'CMO':
        return talib.CMO(np.asarray(price_c, dtype='float'), timeperiod=14)
    if name == 'CORREL':
        return talib.CORREL(np.array(price_h), np.asarray(price_l, dtype='float'), timeperiod=30)
    if name == 'DEMA':
        return talib.DEMA(np.asarray(price_c, dtype='float'), timeperiod=30)
    if name == 'DX':
        return talib.DX(np.array(price_h), np.array(price_l), np.asarray(price_c, dtype='float'), timeperiod=14)
    if name == 'EMA':
        return talib.EMA(np.asarray(price_c, dtype='float'), timeperiod=30)
    if name == 'HT_DCPERIOD':
        return talib.HT_DCPERIOD(np.asarray(price_c, dtype='float'))
    if name == 'HT_DCPHASE':
        return talib.HT_DCPHASE(np.asarray(price_c, dtype='float'))
    if name == 'HT_PHASOR':
        HT_PHASOR1, HT_PHASOR2 = talib.HT_PHASOR(
            np.asarray(price_c, dtype='float'))  # use HT_PHASOR1 for the indication of up and down
        return HT_PHASOR1
    if name == 'HT_SINE':
        HT_SINE1, HT_SINE2 = talib.HT_SINE(np.asarray(price_c, dtype='float'))
        return HT_SINE1
    if name == 'HT_TRENDLINE':
        return talib.HT_TRENDLINE(np.asarray(price_c, dtype='float'))
    if name == 'HT_TRENDMODE':
        return talib.HT_TRENDMODE(np.asarray(price_c, dtype='float'))
    if name == 'KAMA':
        return talib.KAMA(np.asarray(price_c, dtype='float'), timeperiod=30)
    if name == 'LINEARREG':
        return talib.LINEARREG(np.asarray(price_c, dtype='float'), timeperiod=14)
    if name == 'LINEARREG_ANGLE':
        return talib.LINEARREG_ANGLE(np.asarray(price_c, dtype='float'), timeperiod=14)
    if name == 'LINEARREG_INTERCEPT':
        return talib.LINEARREG_INTERCEPT(np.asarray(price_c, dtype='float'), timeperiod=14)
    if name == 'LINEARREG_SLOPE':
        return talib.LINEARREG_SLOPE(np.asarray(price_c, dtype='float'), timeperiod=14)
    if name == 'MA':
        return talib.MA(np.asarray(price_c, dtype='float'), timeperiod=30, matype=0)
    if name == 'MACD':
        MACD1, MACD2, MACD3 = talib.MACD(np.asarray(price_c, dtype='float'), fastperiod=12, slowperiod=26, signalperiod=9)
        return MACD1
    if nam == 'MACDEXT':
        return talib.MACDEXT(np.asarray(price_c, dtype='float'), fastperiod=12, fastmatype=0, slowperiod=26, slowmatype=0,
                          signalperiod=9, signalmatype=0)
    if name == 'MACDFIX':
        MACDFIX1, MACDFIX2, MACDFIX3 = talib.MACDFIX(np.asarray(price_c, dtype='float'), signalperiod=9)
        return MACDFIX1
    if name == 'MAMA':
        MAMA1, MAMA2 = talib.MAMA(np.asarray(price_c, dtype='float'), fastlimit=0, slowlimit=0)
        return MAMA1
    if name == 'MEDPRICE':
        return talib.MEDPRICE(np.array(price_h), np.asarray(price_l, dtype='float'))
    if name == 'MINUS_DI':
        return talib.MINUS_DI(np.array(price_h), np.array(price_l), np.asarray(price_c, dtype='float'), timeperiod=14)
    if name == 'MINUS_DM':
        return talib.MINUS_DM(np.array(price_h), np.asarray(price_l, dtype='float'), timeperiod=14)
    if name == 'MOM':
        return talib.MOM(np.asarray(price_c, dtype='float'), timeperiod=10)
    if name == 'NATR':
        return talib.NATR(np.array(price_h), np.array(price_l), np.asarray(price_c, dtype='float'), timeperiod=14)
    if name == 'OBV':
        return talib.OBV(np.array(price_c), np.asarray(price_v, dtype='float'))
    if name == 'PLUS_DI':
        return talib.PLUS_DI(np.array(price_h), np.array(price_l), np.asarray(price_c, dtype='float'), timeperiod=14)
    if name == 'PLUS_DM':
        return talib.PLUS_DM(np.array(price_h), np.asarray(price_l, dtype='float'), timeperiod=14)
    if name == 'PPO':
        return talib.PPO(np.asarray(price_c, dtype='float'), fastperiod=12, slowperiod=26, matype=0)
    if name == 'ROC':
        return talib.ROC(np.asarray(price_c, dtype='float'), timeperiod=10)
    if name == 'ROCP':
        return talib.ROCP(np.asarray(price_c, dtype='float'), timeperiod=10)
    if name == 'ROCR100':
        return talib.ROCR100(np.asarray(price_c, dtype='float'), timeperiod=10)
    if name == 'RSI':
        return talib.RSI(np.asarray(price_c, dtype='float'), timeperiod=14)
    if name == 'SAR':
        return talib.SAR(np.array(price_h), np.asarray(price_l, dtype='float'), acceleration=0, maximum=0)
    if name == 'SAREXT':
        return talib.SAREXT(np.array(price_h), np.asarray(price_l, dtype='float'), startvalue=0, offsetonreverse=0,
                         accelerationinitlong=0, accelerationlong=0, accelerationmaxlong=0, accelerationinitshort=0,
                         accelerationshort=0, accelerationmaxshort=0)
    if name == 'SMA':
        return talib.SMA(np.asarray(price_c, dtype='float'), timeperiod=30)
    if name == 'STDDEV':
        return talib.STDDEV(np.asarray(price_c, dtype='float'), timeperiod=5, nbdev=1)
    if name == 'STOCH':
        STOCH1, STOCH2 = talib.STOCH(np.array(price_h), np.array(price_l), np.asarray(price_c, dtype='float'),
                                  fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
        return STOCH1
    if name == 'STOCHF':
        STOCHF1, STOCHF2 = talib.STOCHF(np.array(price_h), np.array(price_l), np.asarray(price_c, dtype='float'),
                                     fastk_period=5, fastd_period=3, fastd_matype=0)
        return STOCHF1
    if name == 'STOCHRSI':
        STOCHRSI1, STOCHRSI2 = talib.STOCHRSI(np.asarray(price_c, dtype='float'), timeperiod=14, fastk_period=5,
                                           fastd_period=3, fastd_matype=0)
        return STOCHRSI1
    if name == 'T3':
        return talib.T3(np.asarray(price_c, dtype='float'), timeperiod=5, vfactor=0)
    if name == 'TEMA':
        return talib.TEMA(np.asarray(price_c, dtype='float'), timeperiod=30)
    if name == 'TRANGE':
        return talib.TRANGE(np.array(price_h), np.array(price_l), np.asarray(price_c, dtype='float'))
    if name == 'TRIMA':
        return talib.TRIMA(np.asarray(price_c, dtype='float'), timeperiod=30)
    if name == 'TRIX':
        return talib.TRIX(np.asarray(price_c, dtype='float'), timeperiod=30)
    if name == 'TSF':
        return talib.TSF(np.asarray(price_c, dtype='float'), timeperiod=14)
    if name == 'TYPPRICE':
        return talib.TYPPRICE(np.array(price_h), np.array(price_l), np.asarray(price_c, dtype='float'))
    if name == 'ULTOSC':
        return talib.ULTOSC(np.array(price_h), np.array(price_l), np.asarray(price_c, dtype='float'), timeperiod1=7,
                         timeperiod2=14, timeperiod3=28)
    if name == 'VAR':
        return talib.VAR(np.asarray(price_c, dtype='float'), timeperiod=5, nbdev=1)
    if name == 'WCLPRICE':
        return talib.WCLPRICE(np.array(price_h), np.array(price_l), np.asarray(price_c, dtype='float'))
    if name == 'WILLR':
        return talib.WILLR(np.array(price_h), np.array(price_l), np.asarray(price_c, dtype='float'), timeperiod=14)
    if name == 'WMA':
        return talib.WMA(np.asarray(price_c, dtype='float'), timeperiod=30)