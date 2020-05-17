# -*- coding: utf-8 -*-
# @Time    : 2020/3/18 18:58
# @Author  : HoxHou
# @File    : arrow_time.py
# @Software: PyCharm
# When I wrote this, only God and I understood what I was doing
# Now, God only knows
import datetime

import arrow

utc = arrow.utcnow()  # utc时间
now = arrow.now()  # local时间
utc_current_date = utc.format('YYYY-MM-DD')  # 当前utc日期
current_date = now.format('YYYY-MM-DD')  # 当前日期
now_timestamp_s = now.timestamp  # 当前时间戳，单位秒s
utc_timestamp_s = utc.timestamp  # utc时间戳，单位秒s
the_day_before = utc.shift(days=-1)  # 前一天
the_day_after = utc.shift(days=1)  # 次日
two_day_before = utc.shift(days=-2)  # 前两天
last_week = utc.shift(weeks=-1)  # 上一周
last_month = utc.shift(months=-2)  # 前两个月
arrow_get = arrow.get  # arrow更多get操作

if __name__ == '__main__':
    # print(current_date)
    # print(the_day_before)
    # print(two_day_before)
    # print(last_week)
    # print(arrow_get(now_timestamp_s))
    print(type(datetime.datetime.now()))
    print(now.timestamp)
    print(utc.timestamp)
    print(now.shift(days=1).timestamp)
