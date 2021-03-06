import json
from urllib.request import urlopen, quote
import requests,csv
import pandas as pd #导入这些库后边都要用到

def getBaidulnglat(address):
    url = 'http://api.map.baidu.com/geocoding/v3/'
    output = 'json'
    ak = 'kuZ19FAQhk8wgLjrXuYU3Y1Mf9t8SNVd'
    add = quote(address) #由于本文城市变量为中文，为防止乱码，先用quote进行编码
    uri = url + '?' + 'address=' + add  + '&output=' + output + '&ak=' + ak
    req = urlopen(uri)
    res = req.read().decode() #将其他编码的字符串解码成unicode
    temp = json.loads(res) #对json数据进行解析
    return temp 

file = open('point.json','w') #建立json数据文件
file1 = open('citys.json','w',encoding="utf-8")
with open('name.csv', encoding="utf-8") as csvfile: #打开csv
    reader = csv.reader(csvfile)
    for line in reader:
        if reader.line_num == 1:
            continue
        b = line[0].strip()                                  # 第一列city
        c = line[1].strip() 
        getcity = getBaidulnglat(b)                               # 调用函数获取API返回包
        lng = getBaidulnglat(b)['result']['location']['lng']      # 调用函数获取经度
        lat = getBaidulnglat(b)['result']['location']['lat']      # 获取纬度
        str_temp = '{"lat":' + str(lat) + ',"lng":' + str(lng) + ',"count":' + str(c) +'},'
        file.write(str_temp) 
        file1.write(str(getcity))
file.close() 
file1.close()