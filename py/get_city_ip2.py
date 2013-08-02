#!/usr/bin/python
#coding=utf-8
#获取ip城市和运营商

import sys
from iplocation import *

iplib = IPLibrary()
logfile_path = sys.argv[1]

logfile = open(logfile_path, "r")
while True :
    line = logfile.readline()
    if line == '':
        break
    
    datas = line.split(' ')
    ipaddr   = datas[0].strip()
    city,idc = iplib.get_ip_city_idc(ipaddr)
    print ipaddr,city,idc
logfile.close()
