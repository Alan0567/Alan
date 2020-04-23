import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import numpy as np
from pandas import Series, DataFrame
import datetime 
import threading
import openpyxl 
# import xlrd
# import xlwt
# from tabulate import tabulate

def func():
    print("haha")
    timer = threading.Timer(86400, func)
    timer.start()

now_time = datetime.datetime.now()
next_time = now_time + datetime.timedelta(days=+1)
next_year = next_time.date().year
next_month = next_time.date().month
next_day = next_time.date().day
next_time = datetime.datetime.strptime(str(next_year)+"-"+str(next_month)+"-"+str(next_day)+" 18:00:00", "%Y-%m-%d %H:%M:%S")
timer_start_time = (next_time - now_time).total_seconds()
print(timer_start_time)
timer = threading.Timer(timer_start_time, func)
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
        time.sleep(0.5)             
        df = DataFrame(all_results,columns=["楼盘名称","户型","朝向","楼层","面积","成交时间","成交价","单价","经纪人"])
        dt = list(df.loc[:, '成交时间'])
        df['成交时间'] = df['成交时间'].values.tolist()
        df['weekNum'] = pd.to_datetime(dt).strftime("%W") #所处的周是今年第几周
        df['weekDay'] = pd.to_datetime(dt).strftime("%A") #查询周几，返回英文
        df['weekDayNum'] = pd.to_datetime(dt).strftime("%w") #查询周几，返回数字
        with pd.ExcelWriter('baoan.xlsx') as writer:  # pylint: disable=abstract-class-instantiated
            df.to_excel(writer, sheet_name='baoan')