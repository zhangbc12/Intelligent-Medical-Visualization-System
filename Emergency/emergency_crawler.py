# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import urllib.request
# import requests
# import re, os

import schedule
import time
import datetime
import pytz


def download():
    '''
    :param url:文件链接
    :return: 下载文件，自动创建目录
    '''
    tz = pytz.timezone('Asia/Shanghai')
    now = datetime.datetime.now(tz)

    time1_str = datetime.datetime.strftime(now, '%Y%m%d-%H-%M')
    arr = time1_str.split('-')
    part1 = arr[0]
    num2 = int(arr[1])
    num3 = int(arr[2])

    part2 = 0
    part3 = 0

    if num3 >= 5 and num3 < 20:
        part2 = num2
        part3 = 0
    elif num3 >= 20 and num3 < 35:
        part2 = num2
        part3 = 15
    elif num3 >= 35 and num3 < 50:
        part2 = num2
        part3 = 30
    elif num3 >= 50:
        part2 = num2
        part3 = 45
    else:
        part2 = num2 - 1 if num2 > 0 else 0
        part3 = 45

    temp1 = "https://api.data.gov.hk/v1/historical-archive/get-file?url=https%3A%2F%2Fwww.ha.org.hk%2Fopendata%2Faed%2Faedwtdata-en.json&time="
    temp2 = part1
    temp3_1 = "0" + str(part2) if part2 < 10 else str(part2)
    temp3_2 = "00" if part3 == 0 else str(part3)
    # temp = "https://api.data.gov.hk/v1/historical-archive/get-file?url=https%3A%2F%2Fwww.ha.org.hk%2Fopendata%2Faed%2Faedwtdata-en.json&time=20220523-1745"
    temp = temp1 + temp2 + "-" + temp3_1 + temp3_2
    urllib.request.urlretrieve(temp, "../static/cur.json")


def schedule_download():
    try:
        download()

    except:
        pass
