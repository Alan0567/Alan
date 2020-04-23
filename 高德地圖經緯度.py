import requests
import pandas as pd
import csv
data = pd.read_csv('map.csv',engine='python',encoding='utf-8')#导入地址的csv文件
data = data['地址']#选择地址列

lis = []
def gaode():
    for i in data:
        para = {
            'key':'ef2490f75612cf7ad7c4634455112ea1',
            'address':i,
            'city':'深圳'
        }
        url = 'https://restapi.amap.com/v3/geocode/geo?'
        req = requests.get(url,para)
        req = req.json()
        if req['infocode']=='10000':
            w = req['geocodes'][0]['formatted_address']
            z = req['geocodes'][0]['location']
            print(w)
            print(z)
            d = (w, z)
        else:
            print('查询不到')
        lis.append(d)

    t = ['位置','经纬度']  
    with open('高德地图位置.csv', 'w', newline='',encoding='utf-8')as f:
        writer = csv.writer(f)
        writer.writerow(t)
        writer.writerows(lis)
if __name__ == '__main__':
    gaode()
