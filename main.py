from bullet import Numbers
import sqlite3
import time
import datetime
import os

from bullet import YesNo

# 清屏
def clearOS():
    os.system('clear')

# 获取当前时间
def getNowTime():
    nowTime = datetime.datetime.now()
    #当前日期
    t1 = nowTime.strftime('%Y-%m-%d %H:%M:%S')
    #转为秒级时间戳
    return time.mktime(time.strptime(t1, '%Y-%m-%d %H:%M:%S'))

# 获取时间间隔
def checkTimes(oldTime):
    nowTime = getNowTime()
    return (datetime.datetime.fromtimestamp(nowTime)-datetime.datetime.fromtimestamp(oldTime)).days

# 打开sqlite3数据库
def openDB():
    conn = sqlite3.connect('db.sqlite3')
    return conn.cursor()

# 对未记住的单词次数加1
def noRemberData(c,conn,id,number):
    number = number + 1
    c.execute("UPDATE main set number={} where id={};".format(number,id))
    conn.commit()

# 对记住的单词进行保存
def remberData(c,conn,id):
    nowTime = getNowTime()
    c.execute("UPDATE main set enddate={} where id={};".format(nowTime,id))
    conn.commit()

# 查询enddate小于1天的数据
def searchData(c,conn):
    cursor = c.execute("select * from main")
    tSum = 0
    fSum = 0
    idD = []
    englishD = []
    chineseD = []
    numberD = []
    # 加载数据
    for row in cursor:
        if row[4] is not None:
            # enddate 小于1天的排除
            timeNumber = checkTimes(row[4])
            if timeNumber < 1:
                continue
        idD.append(row[0])
        englishD.append(row[1])
        chineseD.append(row[2])
        numberD.append(row[3])
    
    if len(idD) == 0 :
        print('今日无复习单词。')
        exit()

    for i in range( len(idD) ):
        prompt = Numbers("{} ".format(englishD[i]), type = int)
        res = prompt.launch()  
        # print(chineseD[i])   
        # 记住的单词处理
        if res == 2:
            # 展示确认是否认错
            print('{} {} [ {} ]'.format(englishD[i],chineseD[i],numberD[i])) 
            nowTime = getNowTime()
            prompt = Numbers("{} ".format(englishD[i]), type = int)
            res = prompt.launch()
            if res == 2:
                str = "UPDATE main set enddate={} where id={}".format(nowTime,idD[i])
                tSum += 1
        # 未记住的单词处理
        if res == 1:
            number = numberD[i] + 1
            str = "UPDATE main set number={} where id={}".format(number,idD[i])
            fSum += 1
        c.execute(str)
        conn.commit()
        clearOS()
        print('{} {} [ {} ]'.format(englishD[i],chineseD[i],numberD[i]))  
    print('本次已记住单词 {} 个，未记住单词 {} 个，共计 {} 个。'.format(tSum,fSum,tSum+fSum))
        
         

def __main__():
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    clearOS()
    searchData(c,conn)
    client = YesNo("已结束，是否重来？", default = 'y')
    res = client.launch()
    if res == True:
        __main__()

__main__()