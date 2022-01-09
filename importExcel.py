import csv
import sqlite3
import time
import datetime

# 获取当前时间
def getNowTime():
    nowTime = datetime.datetime.now()
    #当前日期
    t1 = nowTime.strftime('%Y-%m-%d %H:%M:%S')
    #转为秒级时间戳
    return time.mktime(time.strptime(t1, '%Y-%m-%d %H:%M:%S'))

with open(r'data.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        nowTime = getNowTime()
        str = "insert into main (english,chinese,adddate) values ('{}','{}',{})".format(row[1],row[2],nowTime)
        print(str)
        conn = sqlite3.connect('db.sqlite3')
        c = conn.cursor()
        c.execute(str)
        conn.commit()