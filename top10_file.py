#!/usr/bin/env python
# _*_ coding:utf-8 _*_
"""
@author: huanzhiqiang  
@file: top10_file.py  
@time: 2021/4/2 9:17
"""
import os
import sys
import operator
def gen_dic(topdir):
	dic = {}
	a = os.walk(topdir)
	for p, d, f in a:
		for i in f:
			fn = os.path.join(p, i)
			f_size = os.path.getsize(fn)
			dic[fn] = f_size
	return dic
if __name__ == '__main__':
	dirfile='E:\\BaiduNetdiskDownload'
	# dic = gen_dic(sys.argv[1])
	dic = gen_dic(dirfile)
	# operator.itemgetter字典下标为1的元素排序
	sorted_dic = sorted(dic.items(), key=operator.itemgetter(1), reverse=True)
	for k, v in sorted_dic[:10]:
		print(k, '==>', v)