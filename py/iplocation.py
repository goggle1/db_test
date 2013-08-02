#!/usr/bin/python
#coding=utf-8

## Funshion IP location library
## Author: xiongming@funshion.com
## Date: 2013-07-18

import socket
import struct
import re

#convert ip to long
def ip2long(ipaddr) :
    ip_re = re.compile('\d+\.\d+\.\d+\.\d+')
    if ip_re.match(ipaddr) == None :
        return 0L
    
    longip = 0L
    ip = ipaddr.split('.', 3)
    for i in range(0, len(ip)) :
        if 0 <= long(ip[i]) < 256 :
            longip = longip + long(ip[i]) * (256**(3-i))
        else :
            longip = 0L
            break
    return longip

#convert long to ip address
def long2ip(longip) :
    ipaddr = ''
    for i in range(0, 4) :
        if ipaddr == '' :
            ipaddr = str((longip / (256**(3-i))) % 256)
        else :
            ipaddr = ipaddr + '.' + str((longip / (256**(3-i))) % 256)
        print ipaddr
    return ipaddr

class ipitem :
    def __init__(self, data) :
        datas = data.split(',', 5)
        self.start_ip = ip2long(datas[0])
        self.end_ip   = ip2long(datas[1])
        self.city     = datas[2]
        self.idc      = datas[4]


class IPLibrary :
    iplibrary = []
    iplibrary_by_idc = {}
    iplibrary_by_city = {}
    iplibrary_by_city_idc = {}
    iplibrary_file = ""

    def __init__(self, iplibrary_file = "funshion.all.dat") :
        if iplibrary_file != '' :
            self.iplibrary_file = iplibrary_file

        ipfile = open(self.iplibrary_file, "r")
        content = ipfile.readlines()
        for line in content :
            item = ipitem(line)

            #set iplibrary
            self.iplibrary.append(item)

            #set iplibrary_by_idc
            key = item.idc
            if self.iplibrary_by_idc.get(key) == None :
                self.iplibrary_by_idc[key] = []
            self.iplibrary_by_idc[key].append(item)

            #set iplibrary_by_city
            key = item.city
            if self.iplibrary_by_city.get(key) == None :
                self.iplibrary_by_city[key] = []
            self.iplibrary_by_city[key].append(item)

            #set iplibrary_by_city_idc
            key = item.city + item.idc
            if self.iplibrary_by_city_idc.get(key) == None :
                self.iplibrary_by_city_idc[key] = []
            self.iplibrary_by_city_idc[key].append(item)
        ipfile.close()
        self.iplibrary.sort(key = lambda item : item.start_ip)

    # get ip item, binary search
    def __get_ip_item(self, longip) :
        start_index = 0
        end_index   = len(self.iplibrary) - 1
        while start_index <= end_index :
            index = (start_index + end_index) / 2

            if self.iplibrary[index].start_ip <= longip <= self.iplibrary[index].end_ip :
                return self.iplibrary[index]

            if longip > self.iplibrary[index].end_ip :
                start_index = index + 1
            else :
                end_index = index - 1
        return None

    # get @ip's city
    def get_ip_city(self, ip) :
        longip = ip2long(ip)
        item = self.__get_ip_item(longip)
        if None != item :
            return item.city
        return "未知城市"

    # get @ip's idc
    def get_ip_idc(self, ip) :
        longip = ip2long(ip)
        item = self.__get_ip_item(longip)
        if None != item :
            return item.idc
        return "未知运营商"

    #get @ip's @city and @idc
    def get_ip_city_idc(self, ip) :
        longip = ip2long(ip)
        item = self.__get_ip_item(longip)
        if None != item :
            return (item.city, item.idc)
        return ("未知运营商", "未知城市")

    # check if @ip in @city
    def check_ip_city(self, ip, city) :
        longip = ip2long(ip)
        key = city
        if self.iplibrary_by_city.get(key) != None :
            for item in self.iplibrary_by_city[key] :
                if item.start_ip <= longip <= item.end_ip :
                    return True
        return False

    # check if @ip in @idc
    def check_ip_idc(self, ip, idc) :
        longip = ip2long(ip)
        key = idc
        if self.iplibrary_by_idc.get(key) != None :
            for item in self.iplibrary_by_idc[key] :
                if item.start_ip <= longip <= item.end_ip :
                    return True
        return False

    # check if @ip in @city and @idc
    def check_ip_city_idc(self, ip, city, idc) :
        longip = ip2long(ip)
        key = city + idc
        if self.iplibrary_by_city_idc.get(key) != None :
            for item in self.iplibrary_by_city_idc[key] :
                if item.start_ip <= longip <= item.end_ip :
                        return True
        return False

