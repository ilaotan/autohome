#!usr/bin/env python
# -*- coding:utf-8 -*-
import requests
import re
import time

##系统初始化
urlHeader = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/"
urlHomePage = "index.html"
urlHtml = urlHeader + urlHomePage
##模拟Chrome访问初始化
headers = {"Host": "www.stats.gov.cn",
           "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; InfoPath.3; .NET4.0C; .NET4.0E)"}

##访问国家统计局(2016年统计用区划代码和城乡划分代码(截止2016年07月31日))
htmlHome = requests.get(urlHtml, headers=headers)
htmlHome.encoding = "gb2312"

##正则表达式获取二级网址及省份名称
reObj = re.compile("<a href='([\s\S]*?.html)'>([\s\S]*?)<br/></a>")
arrayProvince = reObj.findall(htmlHome.text)

for i in range(len(arrayProvince)):
    ##for i in range(4,5):
    urlHtml = urlHeader + arrayProvince[i][0]

    htmlCity = requests.get(urlHtml, headers=headers)
    htmlCity.encoding = "gb2312"

    print arrayProvince[i][1]

    reObj = re.compile("<a href='([\s\S]*?.html)'>([\s\S]*?)</a>")
    arrayCity = reObj.findall(htmlCity.text)

    for j in range(len(arrayCity)):
        time.sleep(0.5)
        ##    for j in range(0,1):
        if j % 2 == 0:
            urlHtml = urlHeader + arrayCity[j][0]
            print arrayCity[j][1] + " " + arrayProvince[i][1] + " " + arrayCity[j + 1][1]

            htmlArea = requests.get(urlHtml, headers=headers)
            htmlArea.encoding = "gb2312"

            reObj = re.compile("<td>[\s\S]*?</td>")
            arrayArea = reObj.findall(htmlArea.text)

            for k in range(1, len(arrayArea)):
                if k % 2 == 0:
                    txtAreaInfo = (arrayArea[k - 1] + arrayArea[k]).replace("<td>", "").replace("</td>", ",") \
                        .replace("<a href='", "").replace("'>", ",").replace("</a>", "").split(",")
                    if ".html" in txtAreaInfo[0]:
                        print txtAreaInfo[1] + " " + arrayProvince[i][1] + " " + arrayCity[j + 1][1] + " " + \
                              txtAreaInfo[3]
                    else:
                        print txtAreaInfo[0] + " " + arrayProvince[i][1] + " " + arrayCity[j + 1][1] + " " + \
                              txtAreaInfo[1]
                    time.sleep(0.2)
