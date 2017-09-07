import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

'''
 Fix ：函数待修复

 待改进函数，计算出历史时间序列中价格5日收益率，查看5天后的价格，如果更高记作赢，如果更低记作输，如果相等则持平
'''
def get_stats(prices):
    # 设置一个计数器
    i = 5
    # 设置一个空list
    data = []
    # 从第一个到倒数第二个价格
    while i < len(prices)-4:
        # 计算五日收益率，留小数点后2位
        ratio = 0.01 * ((prices[i]/prices[i-5]) //0.01)
        # 如果第五天收盘价更高
        if prices[i+4] > prices[i]:
            # 那结果记赢
            result = 'win'
        # 如果第五天收盘价更低
        if prices[i+4] < prices[i]:
            # 结果记输
            result = 'lose'
        # 收盘价不变的话
        if prices[i] == prices[i+4]:
            # 记平
            result = 'even'
        # 看看该比例有无记载过
        ratio_recorded = False
        # 翻看data
        for data_dict in data:
            # 如果比例被记载过
            if data_dict['value'] == ratio:
                # 那就好，更新输赢
                data_dict[result] += 1
                # 记载过为是
                ratio_recorded = True
        # 如果翻完了发现没记载过，
        if ratio_recorded == False:
            # 那么就记载下来
            data_dict = {'value':ratio, 'win':0, 'lose':0, 'even':0}
            data_dict[result] += 1
            data.append(data_dict)
        # 别忘更新i
        i += 1
    # 转换成DataFrame
    df = pd.DataFrame(data,  columns=['value', 'win','even', 'lose'])
    # 按照value列从小到大排序
    df = df.sort(['value'], ascending = True)
    return(df)

'''
 画图函数，在同一个柱状图上，标记出赢-输-平的状态
'''
def DrawBarPic(stats):
    # 设置图的大小
    fig_size = plt.rcParams["figure.figsize"]
    fig_size[0] = 15
    fig_size[1] = 10

    # 把统计的DataFrame中竖列抽出来
    values = stats['value']
    wins = stats['win']
    evens = stats['even']
    loses = stats['lose']

    # 画输的数目，颜色为红
    p1 = plt.bar(values, loses, width = 0.008, color='r')
    # 画平的数目，颜色为黄，底部在输之上
    p2 = plt.bar(values, evens, width= 0.008,  bottom = loses, color='y')
    # 画赢的数目，颜色为绿，底部在输+平之上
    p3 = plt.bar(values, wins, width=0.008, bottom = evens+loses, color='g')

    # 标注坐标轴和注释
    plt.ylabel('输赢结果',size = 15)
    plt.xlabel('收益率',size = 15)
    plt.legend((p1[0], p2[0],p3[0]), ('输', '平','赢'))

'''
 画图函数，展示输赢的差值
'''
def DrawDValuePic(stats):
    fig_size = plt.rcParams["figure.figsize"]
    fig_size[0] = 15
    fig_size[1] = 10

    # 把统计的DataFrame中竖列抽出来
    values = stats['value']
    wins = stats['win']
    evens = stats['even']
    loses = stats['lose']

    # 画赢数减去输数
    pdifference = plt.bar(values, wins - loses, width=0.008, color='b')

    # 标注坐标轴和注释
    plt.ylabel('赢减去输', size=15)
    plt.xlabel('5日收益率', size=15)

'''
 函数功能：
 寻找指点区间宽度内最优区间

 下面函数的4个输入分别为：
 statistics – 之前算出的DataFrame统计数据
 tick_width – 指标值的最小间隔（跳动值，比如上面的示例里就是0.01）
 least_percentage – 要求区间数据量至少有总数据量的多少
 band_width – 区间的宽度，整数，可理解为进行多少次tick_width的跳动。

 返回一Series，内容 low=区间低点，high=区间高点，ratio=区间赢输比
'''
def find_best_region(statistics, tick_width, least_percentage, band_width):
    # 取出统计df的列
    values = statistics['value']
    loses = statistics['lose']
    wins = statistics['win']
    evens = statistics['even']
    # 算总数据量
    num_data = sum(wins) + sum(loses) + sum(evens)
    # 起始一list
    mydata = []
    # 计算指标统计出的最低值除以间距，取整数，方便后面移动计算。
    low_bound = int(statistics['value'].iloc[0]/tick_width)
    # 计算指标统计出的最高值除以间距，减去区间宽度
    high_bound = int(statistics['value'].iloc[-1]/tick_width - band_width + 1)
    # 对于上限和下限之间的所有整数
    for n in range(low_bound, high_bound ):
        # 选取统计中所对应的区间
        statistics1 = statistics[values >= float(n)*tick_width]
        stat_in_range  = statistics1[values <= float(n + band_width - 1) * tick_width]
        # 计算区间中的赢输比。输数加一，避免除以零。
        ratio = float(sum(stat_in_range['win'])) / float(sum(stat_in_range['lose'])+1)
        # 计算区间中数据量
        range_data = float(sum(stat_in_range['win']) + sum(stat_in_range['lose']) + sum(stat_in_range['even']))
        # 如果区间数据量除以总数据量大于最低数据比
        if range_data / num_data >= least_percentage:
            # 记录区间的最低值，最高值，和区间内的赢输比
            mydata.append({'low': float(n) * tick_width, 'high': float(n+band_width) * tick_width, 'ratio': ratio})
    # 制作DataFrame
    data_table = pd.DataFrame(mydata)
    # 按照赢输比排序
    sorted_table = data_table.sort('ratio', ascending = False)
    # 返回第一行
    return(sorted_table.iloc[0])

'''
 搜索所有区间内的最有区间

 statistics – 之前算出的DataFrame统计数据
 tick_width – 指标值的最小间隔（跳动值，比如上面的示例里就是0.01）
 least_percentage – 要求区间数据量至少有总数据量的多少
 least_width – 最短的区间宽度
 most_width – 最大的区间宽度

# 返回一Series，内容 low=区间低点，high=区间高点，ratio=区间赢输比
'''
def find_absolute_best_region(statistics, tick_width, least_percentage, least_width, most_width):
    # 创建标注列的空DF
    columns = ['low', 'high', 'ratio']
    df = pd.DataFrame(columns = columns)
    # 对于所有在最短和最长标准之间的宽度
    for band_width in range(least_width, most_width + 1):
        # 运行上面函数，得到该宽度的最佳区间
        best_width_region = find_best_region(statistics, tick_width, least_percentage, band_width)
        # 将结果加入DF
        df = df.append(best_width_region, ignore_index = True)
    # 将赢输比从大到小排列
    sorted_table = df.sort('ratio', ascending = False)
    # 返回第一行
    return(sorted_table.iloc[0])