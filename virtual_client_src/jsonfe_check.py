#!/usr/bin/python
#FILE_NAME:check_jsonfe.py
'''deal the json request
'''

import json
#from copy import deepcopy

import http
import log
import etc
#import mail

class Jsonfe_check:
    '''check jsonfe_check
    '''
    
    log =  log.MakeLog()
        
    def __init__(self, client, pagesize):
        self.http_mod = http.Http()
        self.client = client
        self.page_size = pagesize
        self.mid_list = []
        self.purl_list = []

        
        
    def jsonfe_focus_type(self, video_type):
        '''deal the focus request
        '''
        del self.mid_list[0:]
        flag = 1
        base_addr = "jsonfe.funshion.com"
        command = "/?cli=%s&ver=0.1.0&src=wonder&type=%s" % (self.client, video_type)
        (focus_type_resp_flag, focus_type_resp) = self.http_mod.connect_times(base_addr, command, etc.HTTP_RETRY)    
        if focus_type_resp_flag != 1:
            Jsonfe_check.log.logger.error(base_addr + command + "cannt not connect")
            flag = -1
        else:
            try:
                focus_type_dict = json.loads(focus_type_resp)
                if focus_type_dict["return"] == "succ":
                    focus_mid_list = focus_type_dict["data"]["media_list"]
                    for every_mid in focus_mid_list:
                        self.mid_list.append(every_mid["mid"])
                else:
                    flag = -2
                    Jsonfe_check.log.logger.error(base_addr + command + "get the error resp")
            except Exception:
                log.logging.error("focus_type_resp is not standard json format data")    
        return (flag, base_addr + command)            
        
    def get_channel_mid(self, channel):
        '''get the mid of media
        '''
        del self.mid_list[0:]
        flag = 1
        base_addr = "jsonfe.funshion.com"
        command = "/list/?cli=%s&ver=0.1.2&id=&type=%s&order=%s&page=1\
&cate=&region=&rdate=&karma=&pagesize=%s&clarity=&hotrank=&udate=" % (self.client, channel, "pl", self.page_size)
        (channel_resp_flag, channel_resp) = self.http_mod.connect_times(base_addr, command, etc.HTTP_RETRY)
        if channel_resp_flag != 1:
            Jsonfe_check.log.logger.error(base_addr + command + "cant connect")
            flag = -1
        else:
            try:
                channel_dict = json.loads(channel_resp)
                if channel_dict["return"] == "succ":
                    for every_ms in channel_dict["data"]["lists"]:
                        self.mid_list.append(every_ms["mid"])
                else:
                    flag = -2
                    Jsonfe_check.log.logger.error(base_addr + command + "    get the error resp")
            except Exception:
                log.logging.error("channel_resp is not standard json format data")
        return (flag, base_addr + command)

        
        
        
    def get_mid_addr(self, every_mid):
        '''get mid addr
        '''    
        del self.purl_list[0:]
        flag = 1        
        addr_mid = "/media/?cli=%s&ver=0.1.0&mid=%s" % (self.client , every_mid)  
        (addr_resp_flag, addr_resp) = self.http_mod.connect_times(etc.JSON_ADDR, addr_mid, etc.HTTP_RETRY)
        if addr_resp_flag == 1: 
            try:               
                all_addr = json.loads(addr_resp)
                if all_addr["return"] != "succ":
                    flag = -2
                    Jsonfe_check.log.logger.error(etc.JSON_ADDR + addr_mid + "get the eror resp")
                else:
                    mid_type = all_addr["data"]["mtype"]
                    url_dict = all_addr["data"]["pinfos"]
                    if mid_type == "movie":
                        # pass
                        self.get_movie(url_dict)                
                    elif mid_type == "variety":
                        # pass
                        self.get_variety(url_dict)                        
                    elif mid_type == "tv" or mid_type == "cartoon":
                        # pass
                        self.get_tv_cartoon(url_dict)
            except Exception:
                log.logging.error("addr_resp is not standard json format data")  
        else: 
            flag = -1    
            Jsonfe_check.log.logger.error(etc.JSON_ADDR + addr_mid + "error")
        return (flag, etc.JSON_ADDR + addr_mid)
                    
                        
                        
    def get_movie(self, url_dict):
        '''get the movie
        '''
        self.purl_list.append(url_dict["purl"])

    
    def get_variety(self, url_dict):
        '''get the variety
        '''
        for every_info in url_dict["fsps"]:
            self.purl_list.append(every_info["purl"])

    
    def get_tv_cartoon(self, url_dict):
        '''get the tv and cartoon
        '''
        for every_info in url_dict["sort"]:
            all_sort = url_dict["content"][every_info]["fsps"]
            for every_fps in all_sort:
                self.purl_list.append(every_fps["purl"])
                
