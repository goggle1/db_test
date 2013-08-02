#!/usr/bin/python
#coding=utf-8
## 整理出北京电信通没有命中的请求
## 统计其infohash是否不在北京电信通的机器上

import sys
from iplocation import *

iplib = IPLibrary()
logfile_path = sys.argv[1]

# 1. 过滤出北京电信通的请求
# 2. 过滤出北京电信通没有命中的请求
# 3. 统计这些请求的infohash

logfile = open(logfile_path, "r")
while True :
    line = logfile.readline()
    if line == '':
        break
   
    line = line.strip() 
    datas = line.split(',')
    if len(datas) > 7 :
        ipaddr   = datas[1]
        cid      = datas[6]
        serverip = datas[7]
        print ipaddr,cid,serverip
        city, idc = iplib.get_ip_city_idc(ipaddr) 
        print ipaddr,city,idc
        city, idc = iplib.get_ip_city_idc(serverip)
        print serverip,city,idc
logfile.close()
