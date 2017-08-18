# coding=utf-8

import urllib2
from bs4 import BeautifulSoup
import pandas

# 打开广发择时站点的某个策略的信号页面，将页面中的日期和信号信息下载，解析后存入本地csv文件
def downloadGFModelSignal(url):
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


def main():
    downloadGFModelSignal("http://218.19.190.27/LLThistory.asp")

if __name__=="__main__":
    main()