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
import batch_algo_trade

import rqalpha

def atsmain(strategy_path):
    config_info = parse_config({}, strategy_path)
    main.run(config_info)

def batch_exec(strategy_name):
    strategy_name_array = []

    config_array = batch_algo_trade.set_strategy_config(strategy_name)
    for index in range(len(config_array)):
        strategy_info = config_array[index]
        print("准备执行的策略==>" + strategy_info)
        pos1 = strategy_info.rfind('\\') + 1
        pos2 = strategy_info.rfind('.')
        strategy_name_array.append(strategy_info[pos1: pos2])
        # configInfo = parse_config({}, strategyInfo)
        # main.run(configInfo)
        print("执行结束")

    print("----------开始生成组合报告----------")
    batch_algo_trade.showAlgoTradeResult(strategy_name_array)

if __name__ == '__main__':
    # 策略执行方式："singal"-执行单个策略，"batch"-批量执行策略，"download"-下载日线数据
    exec_flag = "singal"

    if exec_flag == "singal":
        # 单个执行回测
        atsmain("D:\\OpenSourceTradePlatform\\atspy\\rqalpha\\config.yml")
    elif exec_flag == "batch":
        # 批量执行回测
        batch_exec("ma20")
    elif exec_flag == "download":
        # 下载日线数据
        main.update_bundle("D:\\OpenSourceTradePlatform\\atspy\\rqalpha")  # 获取回测数据
    else:
        print("策略执行错误，未知的执行方式")