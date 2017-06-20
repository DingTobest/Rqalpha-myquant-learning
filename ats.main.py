# coding=utf-8
#ATS
#   Automate Trade Support Platform
#
#   运用rqalpha的回测部分
#   运用vn.py的交易部分
#
#   by dingzhi 2017年3月22日

from rqalpha import main
from rqalpha.utils.config import parse_config
import batchAlgoTrade

import rqalpha

def atsmain(strategyPath):
    configInfo = parse_config({}, strategyPath)
    main.run(configInfo)

def batchExec(strategyName):
    StrategyNameArray = []

    configArray = batchAlgoTrade.setStrategyConfig(strategyName)
    for index in range(len(configArray)):
        strategyInfo = configArray[index]
        print("准备执行的策略==>" + strategyInfo)
        pos1 = strategyInfo.rfind('\\') + 1
        pos2 = strategyInfo.rfind('.')
        StrategyNameArray.append(strategyInfo[pos1: pos2])
        # configInfo = parse_config({}, strategyInfo)
        # main.run(configInfo)
        print("执行结束")

    print("----------开始生成组合报告----------")
    batchAlgoTrade.showAlgoTradeResult(StrategyNameArray)

if __name__ == '__main__':
    # 策略执行方式："singal"-执行单个策略，"batch"-批量执行策略，"download"-下载日线数据
    execFlag = "singal"

    if execFlag == "singal":
        # 单个执行回测
        atsmain("D:\\OpenSourceTradePlatform\\atspy\\rqalpha\\config.yml")
    elif execFlag == "batch":
        # 批量执行回测
        batchExec("ma20")
    elif execFlag == "download":
        # 下载日线数据
        main.update_bundle("D:\\OpenSourceTradePlatform\\atspy\\rqalpha")  # 获取回测数据
    else:
        print("策略执行错误，未知的执行方式")