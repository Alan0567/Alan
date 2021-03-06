import pandas as pd
import json
from urllib . request import urlopen , quote
import requests

data = pd.read_excel ( '小區.xlsx' ) 
def getlnglat ( address ) : 
    url =  'http://api.map.baidu.com/geocoding/v3/' 
    output =  'json' 
    ak = 'kuZ19FAQhk8wgLjrXuYU3Y1Mf9t8SNVd' #百度地圖ak，具體申請自行百度，提醒需要在“控制台” - “設置” - “啟動服務” - “正逆地理編碼”，啟動
    address =  quote(address) #由於本文地址變量為中文，為防止亂碼，先用quote進行編碼
    uri = url +  '?'  +  'address='  + address   +  '&output='  + output +  '&ak='  + ak
    req =  urlopen(uri) 
    res = req.read( ).decode( )  

    temp = json.loads(res) 
    lat = temp [ 'result' ] [ 'location' ] [ 'lat' ] 
    lng = temp [ 'result' ] [ 'location' ] [ 'lng' ] 
    return lat ,lng # 緯度latitude ， 經度longitude ，
for indexs in data.index : 
    get_location =  getlnglat ( data.loc [ indexs , '圈定區域' ] ) 
    get_lat = get_location [ 0 ] 
    get_lng = get_location [ 1 ] 
    data.loc [ indexs , '緯度' ] = get_lat
    data.loc [ indexs , '經度' ] = get_lng
data.to_csv("test.csv",encoding='utf_8_sig')    