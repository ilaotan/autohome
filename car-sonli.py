# encoding:utf-8
# ------------------------------------------------
#    作用：抓取汽车之家车型库
#    日期：2018-03-25
#    作者：呆呆
# ------------------------------------------------
import base64
import cStringIO
import urllib2

import requests
import pymysql
from bs4 import BeautifulSoup
import lxml
import htmllib
import re
import json
import sys

import config_default

configs = config_default.configs

# print configs['full_type_name']['name']

# print configs

# exit()

# print configs.items()

# for key,values in configs.items():
#     print values['name']
# exit
# print 123
# exit()

reload(sys)

sys.setdefaultencoding('utf-8')

HOSTNAME = '127.0.0.1'
USERNAME = 'root'
PASSWORD = 'root'
DATABASE = 'pydata'

conn = pymysql.connect(HOSTNAME, USERNAME, PASSWORD, DATABASE, charset="utf8")
cur = conn.cursor()


# print cur

brandUrl = 'https://car.autohome.com.cn'
seriesUrl = 'https://car.autohome.com.cn/price/series-{}.html'
modelUrl = 'https://car.autohome.com.cn/config/spec/{}.html#pvareaid={}'

# BeautifulSoup用法
'''
soup = BeautifulSoup("<html>data</html>","lxml")
soup = BeautifulSoup('<b name="test" class="boldest">Extremely bold</b>','lxml')
tag = soup.b
# print tag
# print soup.prettify()
# print soup.body
# print type(soup.b)
print soup.name
print soup.b.attrs
print soup.b['class']
print soup.string

print soup.b
print soup.b.string
print type(soup.b.string)

print soup.find_all('b')
soup.find_all(["a", "b"])
soup.find_all("a", limit=2)
soup.find_all(id='link2')

soup.find_all(href=re.compile("elsie"))
soup.find_all("a", class_="sister")
soup.find_all(href=re.compile("elsie"), id='link1')

soup.html.find_all("title")
soup.find_all('b')

print soup.select('#link1')
print soup.select('title')
print soup.select('p #link1')
print soup.select("head > title")
print soup.select('a[class="sister"]')
print soup.select('.sister')

html = ''
soup = BeautifulSoup(html, 'lxml')
print type(soup.select('title'))
print soup.select('title')[0].get_text()

for tag in soup.find_all(re.compile("^b")):
    print(tag.name)

for title in soup.select('title'):
    print title.get_text()
'''

def get_brand():
    res = requests.get('https://car.autohome.com.cn/AsLeftMenu/As_LeftListNew.ashx?typeId=1%20&brandId=0%20&fctId=0%20&seriesId=0')
    if res.status_code == 200:
        res.close()
        soup = BeautifulSoup(res.text, 'lxml')

        data = []
        for letter in soup.select(".cartree-letter"):
            for li in letter.find_next():
                args = li.find("a")
                sub_arg = (letter.get_text(),args['href'],re.findall(u".*\(", args.get_text())[0].replace("(",""),re.findall(u"\d+\.?\d*", args.find("em").get_text())[0])
                data.append(sub_arg)

        return data

def obtain_brand():
    res = requests.get(brandUrl)
    if res.status_code == 200:
        res.close()
        res.encoding = 'gb2312'
        resHtml = res.text

        soup = BeautifulSoup(resHtml,'lxml')

        print soup.find_all(name='div', attrs={"class":"cartree"})

        for div in soup.find_all(name='div', attrs={"class":"cartree-letter"}):
            print div.get_text()

        for letter in soup.select("#cartree .cartree-letter"):
            print letter()

def obtain_series(data):

    host = 'https://car.autohome.com.cn'

    parentPath = 'D:\\test\\'

    for info in data:

        res = requests.get(host+info[1])
        if res.status_code == 200:
            res.close()
        soup = BeautifulSoup(res.text, "lxml")


        # 从url截取出唯一id来 <type 'tuple'>: (u'A', '/price/brand-117.html', u'AC Schnitzer', u'2')
        html = info[1]
        htmlNoEnd = html[:-5]
        id = htmlNoEnd[13:]


        for series in soup.select('div[class="carbradn-pic"] img'):

            src = series.attrs['src']
            origin_file = cStringIO.StringIO(urllib2.urlopen("https:" + src).read())
            base64_str = base64.b64encode(origin_file.getvalue())

            # print id, "data:image/png;base64," + base64_str

            pr = "INSERT INTO `car_brand` (`id`,`first_letter`, `name`,`pic_path`, `base64_data`) VALUES ('%s', '%s', '%s', '%s', '%s');" % (id, info[0], info[2],id +".png" ,"data:image/jpeg;base64," + base64_str)

            f = open(parentPath + id + ".png", 'wb')
            f.write(origin_file.getvalue())
            f.close()

            f2 = open(parentPath +"data.sql", 'a+')
            f2.write(pr)
            f2.write("\r\n")
            f2.close()





def main():
    result = get_brand()
    obtain_series(result)

if '__main__' == __name__:
    main()