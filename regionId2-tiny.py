#!usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import time

import requests
from lxml import etree
from xpinyin import Pinyin


reload(sys)

sys.setdefaultencoding('utf-8')

class Spider():


    def __init__(self):
        self.province = ''
        self.province_code = ''
        self.city = ''
        self.city_code = ''
        self.district = ''
        self.district_code = ''

        self.committee = ''
        self.committee_code = ''
        self.committee_code2 = ''

        self.city_url = ''
        self.district_url = ''
        self.url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/'

        self.headers = {"Host": "www.stats.gov.cn",
           "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; InfoPath.3; .NET4.0C; .NET4.0E)"}

        self.p = Pinyin()

    def get_province(self):

        rep = requests.get(url=self.url, headers=self.headers)
        rep.encoding = "gb2312"
        html = rep.text
        html = etree.HTML(html)

        data = html.xpath('//tr[@class="provincetr"]/td')[0]
        province_url = data.xpath('//a/@href')
        province_url.pop(-1)
        print('###################')
        print(province_url)
        province_name = data.xpath('//a/text()')

        for i in range(len(province_url)):
            province_code = province_url[i][:2]
            self.province = province_name[i]
            print(self.province)
            self.province_code = province_code
            self.city_url = self.url + self.province_code + '.html'
            print("省：" + self.city_url)
            time.sleep(0.5)

            # id, parentId, level, name, mergerName
            self.write_data(self.province_code, '0', 1, self.province, '')
            self.get_city()


    def get_city(self):
        #"""市"""

        rep = requests.get(url=self.city_url, headers=self.headers)
        rep.encoding = "gb2312"
        html = rep.text
        html = etree.HTML(html)

        city_url = html.xpath('//tr[@class="citytr"]/td//a/@href')
        city_data = html.xpath('//tr[@class="citytr"]/td//a/text()')

        city_url = list(set(city_url))
        print(city_url)

        city = city_data[1::2]
        city_code = city_data[::2]

        for i in range(len(city_code)):
            city_code_s = city_code[i][:4]
            self.city = city[i]
            self.city_code = city_code_s
            self.district_url = self.url + '/' + city_url[i]

            print("市：" + self.district_url)
            time.sleep(0.5)
            # id, parentId, level, name, mergerName
            self.write_data( self.city_code, self.province_code, 2, self.city, self.province + self.city)
            self.get_district(self.district_url)



    def get_district(self, url):
        #"""区"""

        rep = requests.get(url=url, headers=self.headers)
        rep.encoding = "gb2312"
        html = rep.text
        html = etree.HTML(html)

        district_data = html.xpath('//tr[@class="countytr"]/td//a/text()')
        district_url = html.xpath('//tr[@class="countytr"]/td//a/@href')
        district_url = list(set(district_url))

        district = district_data[1::2]
        district_code = district_data[::2]

        for i in range(len(district)):
            self.district = district[i]
            self.district_code = district_code[i][:6]

            self.qu_url = self.city_url[:-5] + '/' + district_url[i]

            print("区：" + self.qu_url)
            time.sleep(0.5)
            # id, parentId, level, name, mergerName
            self.write_data(self.district_code, self.city_code, 3, self.district, self.province + self.city + self.district)

    def fix6length(self, value):
        while(len(value) < 6) :
            value = value + "0"

        return value


    def write_data(self, id, parentId, level, name, mergerName):

        pinyin = self.p.get_pinyin(name, '').lower()
        firstLetter = pinyin[0]
        jianpin = self.p.get_initials(name, '').lower()

        data = "INSERT INTO `region` (`Id`,`ParentId`, `Level`,`Name`, `MergerName`, `PinYin`, `JianPin`, `FirstLetter`) " \
               "VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'); \n" % \
               (self.fix6length(id), self.fix6length(parentId), level, name, mergerName, pinyin, jianpin, firstLetter)

        with open('D:\\data_mkiceman-tiny.txt', 'a+') as f:
            f.write(data)

if __name__ == '__main__':
    spider = Spider()
    spider.get_province()
