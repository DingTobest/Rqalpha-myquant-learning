# coding=utf-8

import urllib2
from bs4 import BeautifulSoup
import pandas
import numpy as np
import time

# 打开广发择时站点的某个策略的信号页面，将页面中的日期和信号信息下载，解析后存入本地csv文件
def download_GFModelSignal(url):
    content = urllib2.urlopen(url).read()
    soup = BeautifulSoup(content, "lxml")
    soup.prettify()

    signalDic = {}
    date = ""
    signal = ""
    for tag in soup.find_all("td"):
        if tag.string == None:
            for child in tag.children:
                if str(child).find("↑") != -1:
                    signal="up"
                elif str(child).find("↓") != -1:
                    signal="down"
                elif str(child).find("↓") != -1:
                    signal="down"
        else:
            date = tag.string

        if date != "" and signal != "":
            return

# 获取所有基金的历史净值信息
def download_fund_data(dir_path):
    fund_infos_df = get_all_fund('D:\\OpenSourceTradePlatform\\fund_info.txt')
    int
    for index, row in fund_infos_df.iterrows():  # 获取每行的index、row
        # index = '000076'
        if index < '240009':
            continue

        print('start to download==> ' + index)
        start_date, end_date = parse_fund_data(index, dir_path)
        fund_infos_df.loc[index, ['start_date']] = start_date
        fund_infos_df.loc[index, ['end_date']] = end_date
        print('download successful==> ' + index)

        file_path = dir_path + 'fund_infos.csv'
        fund_infos_df.to_csv(file_path, encoding='gbk', index=False)

        # break   # 此处break是为了测试的时候在获取完第一个基金的数据后就停止，去掉后即可访问所有的数据了

    print 'success to download all fund infos'
    print fund_infos_df

# 爬虫程序，根据输入的基金编码，去东方财富基金部分上下载所有的历史数据
# 输入参数fund_cdoe：场外基金代码
# 输入参数dir_path：输出文件路径
def parse_fund_data(fund_code, dir_path):
    page_index = 1
    page_count = 1
    histroy_data = []
    while True:
        url = "http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code=%s&page=%s&per=20&sdate=&edate="%(fund_code, str(page_index))
        count = 0
        while True:
            try:
                response = urllib2.urlopen(url, timeout=10.0)
                if (response <> None):
                    break
            except:
                print('链接错误，重新链接')


            time.sleep(5)
            if (count >=5):
                return "获取超时", "获取超时"
            count += 1

        content = response.read()
        soup = BeautifulSoup(content, "lxml")
        soup.prettify()


        for tag in soup.find_all("tbody"):
            for child in tag.children:
                day_data = []
                for child2 in child.children:
                    day_data.append(child2.string)
                    # print(child2.string)
                histroy_data.append(day_data)



        if page_index == 1:
            for child in soup.body.children:
                pos = str(child).find("pages")
                if pos != -1:
                    pos2 = str(child).find(",curpage")
                    page_count = int(str(child)[pos + 6:pos2])
                    break

        if page_index == page_count:
            break

        if page_count == 0:
            return '', ''

        page_index += 1

    histroy_data_array = np.array(histroy_data)
    # print(histroy_data_array)
    if (len(histroy_data[0]) == 7):
        fund_data_df = pandas.DataFrame(histroy_data_array, columns=['date', 'net_value', 'total_value', ' growth_rate', 'apply_status', 'redeem_status', 'poundage'])
    else:
        fund_data_df = pandas.DataFrame(histroy_data_array, columns=['date', 'profit', '7day_yield', 'apply_status', 'redeem_status', 'poundage'])
    # print(fund_data_df)
    fund_data_df = fund_data_df.sort(columns=['date'], axis=0, ascending=True)

    start_date = fund_data_df.iat[0, 0]
    end_date = fund_data_df.iat[-1, 0]
    file_path = dir_path + fund_code + '.csv'
    fund_data_df.to_csv(file_path, encoding='gbk', index=False)

    return start_date, end_date

# 通过格式化后的基金列表文件，获取所有的基金列表和编号，并获取基金的手续费信息，用于之后获取所有的基金的历史净值信息
def get_all_fund(file_name):
    file_object = open(file_name, 'rb')
    try:
        all_the_text = file_object.read().decode("gbk")
    finally:
        file_object.close()

    fund_infos = []
    fund_codes= []
    fund_array = all_the_text.split('\r\n')
    for arr in fund_array:
        infos = arr.split('@')
        # print(arr)
        fund_data = []
        for i in range(len(infos)):
            if i == 0:
                # print(infos[i])
                fund_data.append(infos[i] + '.FUND')
                fund_codes.append(infos[i])
            else:
                info = infos[i]
                fundName = info[:info.index("&")]
                # print(fundName)
                fund_data.append(fundName)
                if not info.endswith('---'):
                    # print('---')
                    # fund_data.append(None)
                # else:
                    charge = info[len(info) - 5:]
                    # print(charge)
                    fund_data.append(charge)

        fund_infos.append(fund_data)

    fund_infos_df = pandas.DataFrame(fund_infos, columns=['fund_code', 'fund_name', 'charge'], index=fund_codes)
    fund_infos_df = fund_infos_df.sort(columns=['fund_code'], axis=0, ascending=True)

    fund_infos_df['start_date'] = None
    fund_infos_df['end_date'] = None

    print '--------get all fund info-------'
    print fund_infos_df
    return fund_infos_df

def main():
    # download_GFModelSignal("http://218.19.190.27/LLThistory.asp")
    download_fund_data('D:\\OpenSourceTradePlatform\\fund_data\\')

    # get_all_fund('D:\\OpenSourceTradePlatform\\fund_info.txt')


if __name__=="__main__":
    main()