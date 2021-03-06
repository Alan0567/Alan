import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import numpy as np
from pandas import Series, DataFrame
import datetime 
import threading
import openpyxl 
def func():
    print("running...")
    timer = threading.Timer(86400, func)
    timer.start()
    #抓取房價
    session = requests.session()
    # User-Agent
    headers ={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.9"}
    all_results=[]
    pages = range(1,2)
    abc = [*pages]
    for page in abc:
            url =("https://sz.centanet.com/chengjiao/baoan/g" + str(page))
            req =session.get(url,headers=headers)
            soup = BeautifulSoup(req.content,'html.parser')
            table = soup.body
            table_rows = table.find_all('div',class_ ="tablerecond-item" )
            for tr in table_rows:
                td = tr.find_all('span')
                data = [i.text for i in td]
                data2 = [elem.strip() for elem in data]
                data2[1] = data2[1].strip().replace("室","")
                data2[2] = data2[2].replace("东","E").replace('南','S').replace('西','W').replace('北','N')
                data2[3] = data[3].strip().replace("高层","H").replace("低层","L").replace("中层","C")
                data2[4] = float(data[4].strip().replace("平",""))
                data2[6] = float(data[6].strip().replace("万",""))
                data2[7] = float(data[7].strip().replace("元/平",""))
                all_results.append(data2)
                time.sleep(1)             
    df = DataFrame(all_results,columns=["楼盘名称","户型","朝向","楼层","面积","成交时间","成交价","单价","经纪人"])
    dt = list(df.loc[:, '成交时间'])
    df['成交时间'] = df['成交时间'].values.tolist()
    df['weekNum'] = pd.to_datetime(dt).strftime("%W") #所处的周是今年第几周
    df['weekDay'] = pd.to_datetime(dt).strftime("%A") #查询周几，返回英文
    df['weekDayNum'] = pd.to_datetime(dt).strftime("%w") #查询周几，返回数字
    df['Year'] = pd.to_datetime(dt).strftime("%Y") # returen Year
    df1 = pd.read_excel('baoan.xlsx',index_col=0)
    day = df1['成交时间'].max()
    new_df = df.loc[(df['成交时间'])>= day]
    df2 = df1.append(new_df)
    df2.drop_duplicates(subset=["楼盘名称","户型","朝向","楼层","面积","成交时间","成交价","单价","经纪人"], keep='first', inplace=True)
    writer = pd.ExcelWriter('baoan.xlsx')
    df2.to_excel(writer,sheet_name='baoan')
    writer.save()
timer = threading.Timer(10, func)

timer.start()
