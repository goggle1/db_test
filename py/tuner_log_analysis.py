#!/usr/bin/python
#coding=utf-8

import sys
from iplocation import *

iplib = IPLibrary()
logfile_path = sys.argv[1]

logfile = open(logfile_path, "r")
while True :
    line = logfile.readline()
    if line == '':
        break
    
    datas       = line.split(',')
    if len(datas) >= 8 :
        client_ip   = datas[1]
        infohash    = datas[7].split(';')[0]
        if len(infohash) == 40 :
            server_ip   = datas[7].split(';')[2].split(':')[0]
            client_city, client_idc = iplib.get_ip_city_idc(client_ip)
            server_city, server_idc = iplib.get_ip_city_idc(server_ip)
            print "%s,%s,%s,%s,%s,%s,%s" % (client_ip,client_city,client_idc,infohash,server_ip,server_city,server_idc)
logfile.close()
