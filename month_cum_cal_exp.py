#!/usr/bin/env python
# _*_ coding:utf-8 _*_
"""
@author: huanzhiqiang  
@file: month_cum_cal_exp.py
@time: 2021/3/31 15:16
"""
import calendar
import datetime
def add_months(sourcedate, months=0):
	"""
	获取指定月份几个月之后或之前的月份及日期
	:param source_date: 起始日期
	:param months: 月份跨度
	:return: 返回起始日期source_date与months相加之后的日期，格式为datetime.date
	"""
	month = sourcedate.month - 1 + months
	year = sourcedate.year + month // 12
	month = month % 12 + 1
	day = min(sourcedate.day, calendar.monthrange(year,month)[1])
	return datetime.date(year, month, day)

if __name__ == '__main__':
	somedate = datetime.date.today()
	# 当前时间累加10个月份时间计算;
	print(add_months(somedate,10))