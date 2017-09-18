# -*- coding: utf-8 -*-
import  xdrlib ,sys
import xlrd
import os
import shutil
import matplotlib; matplotlib.use('Qt5Agg')
from matplotlib import gridspec
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy



templatePath = "D:\\OpenSourceTradePlatform\\atspy\\Template"

def open_excel(file):
    try:
        data = xlrd.open_workbook(file)
        return data
    except:
        print('打开excel文件错误')

# 读取excel文件，生成配置文件和策略脚本文件
def set_strategy_config(fileName, file="D:\\OpenSourceTradePlatform\\atspy\\AlgoTradeConfig", fileType="xlsx"):
    # 初始化目录信息
    excelFile = file + "\\" + fileName + "." + fileType
    ymlFile = file + "\\" + fileName + ".yml"
    strategyTemplateFile = file + "\\" + fileName + ".py"

    configArray = []

    strategyTemlatePath = templatePath + "\\" + fileName
    if os.path.exists(strategyTemlatePath):
        try:
            shutil.rmtree(strategyTemlatePath)
        except:
            print('删除文件夹错误')
            return

    os.makedirs(strategyTemlatePath)
    os.makedirs(strategyTemlatePath + "\\config")
    os.makedirs(strategyTemlatePath + "\\Result")
    os.makedirs(strategyTemlatePath + "\\strategy")

    # 读取config.yml文件
    file_object = open(ymlFile)
    try:
        configInfos = file_object.read()
    finally:
        file_object.close()

    # 读取策略.py文件
    file_object = open(strategyTemplateFile)
    try:
        strategyTemplateInfos = file_object.read()
    finally:
        file_object.close()

    # 读取excel配置信息
    data = open_excel(excelFile)
    table = data.sheets()[0]
    nrows = table.nrows # 行数
    ncols = table.ncols # 列数
    colnames = table.row_values(0) # 标题
    list =[]
    for rowIndex in range(1, nrows):
        row = table.row_values(rowIndex)

        configFilePath = strategyTemlatePath + "\\config\\" + fileName + "_" + str(int(row[0])) + ".yml"
        strategyPath = strategyTemlatePath + "\\strategy\\" + fileName + "_" + str(int(row[0])) + ".py"

        configArray.append(configFilePath)

        strategyInfos = strategyTemplateInfos

        for index in range(len(colnames)):
            if (index == 0):
                tempStr = configInfos.replace("$策略路径$", strategyPath)
                fp = open(configFilePath, 'w')
                fp.write(tempStr)
                fp.close()
            else:
                valueName = int(row[index])
                tag = "$" + colnames[index] + "$"
                strategyInfos = strategyInfos.replace(tag.encode("utf8"), str(valueName))
                if (index == len(colnames) -1):
                    fp = open(strategyPath, 'w')
                    fp.write(strategyInfos)
                    fp.close()

    return configArray

# 分析批量回测结果，展示回测统计信息
def showAlgoTradeResult(StrategyNameArray, resultPath="D:\\OpenSourceTradePlatform\\atspy\\cvsResult"):
    plt.figure(figsize=(16, 9))

    for index in range(len(StrategyNameArray)):
        portfolioFilePath = resultPath + "\\" + StrategyNameArray[index] + "\\portfolio.csv"

        if os.path.exists(portfolioFilePath):
            print("开始解析投资组合数据==>" + portfolioFilePath)
            x = numpy.loadtxt(portfolioFilePath, delimiter=',', skiprows=(1), usecols=(0,), dtype='datetime64[D]')
            y = numpy.loadtxt(portfolioFilePath, delimiter=',', skiprows=(1), usecols=(5,), dtype='float')

            plt.plot(x, y, label = StrategyNameArray[index])

    plt.legend(loc='upper left')
    plt.xlabel("Trade Date")
    plt.ylabel("Portfolio")
    plt.title("BatchAlgoTrade Result")

    print("计算结束，输出统计截图")
    plt.show()


def main():
    configArray = setStrategyConfig("ma20")
    for index in range(len(configArray)):
        print(configArray[index])


if __name__=="__main__":
    main()
