#!/usr/bin/python
#FILE_NAMR:jobsfe_check.py
'''deal the jobsfe request
'''

import http
import log
import re
import random
import etc
#import mail


class Jobsfe_mp4_check:
    '''check mp jobsfe
    '''
    
    log =  log.MakeLog()
    
    def __init__(self):
        self.http_mod =  http.Http()
        self.jobsfe_addr = ""
       

        

    def get_media_addr(self, every_purl):
        '''get the media server address
        '''
        self.jobsfe_addr = ""
        flag = 1
        purl_list = every_purl.split(r'/', 3)
        purl3 = purl_list[3]
        #del &f=z

        new_purl3 = purl3.replace("&f=z", "")
        purl_base = etc.TUNER_ADDR[random.randint(0, len(etc.TUNER_ADDR)-1)]
        command = new_purl3 + "&src=" + etc.PROVINCE[random.randint(0, len(etc.PROVINCE)-1)] + etc.TUNER_TEST
        (purl_resp_flag, purl_resp) = self.http_mod.connect_times(purl_base, '/' + command, etc.HTTP_RETRY)
        if purl_resp_flag != 1:
            flag = -1
            Jobsfe_mp4_check.log.logger.error(purl_base + '/' + command + "get resp error")
        else:
            self.jobsfe_addr = purl_resp
        return (flag, purl_base + '/' + command)

                
                
class Jobsfe_ts_check:
    ''' check mp4
    '''
    
    log =  log.MakeLog()
    
    def __init__(self):
        self.ts_addr = ""
        self.m3u8_addr = ""
        self.http_urllib = http.Http_urllib()
                
                
    def get_media_addr(self, every_info):
        self.ts_addr = ""
        self.m3u8_addr = ""
        reglax = re.compile(r'\r\n')
        m3u8_flag = 0      
        flag = 1
        purl_list = every_info.split(r'/', 3)
        purl3 = purl_list[3]
        new_purl3 = purl3.replace("&f=z", "")
        url_info = "http://"+etc.TUNER_ADDR[random.randint(0, len(etc.TUNER_ADDR)-1)] + '/' + new_purl3 + "&src=" + etc.PROVINCE[random.randint(0, len(etc.PROVINCE)-1)] + etc.TUNER_TEST
        (purl_resp_flag, purl_resp) = self.http_urllib.connect_times(url_info, etc.HTTP_RETRY)
        if purl_resp_flag == 1:
            k = reglax.split(purl_resp)
            for every_ms in k:
                if every_ms[0:4] == "http":
                    if m3u8_flag == 0:
                        m3u8_flag += 1
                        ms_addr = every_ms.replace("playlist.m3u8", "Ats-1.ts")
                        self.ts_addr = ms_addr
                        self.m3u8_addr = every_ms
        else:
            flag = -1
            Jobsfe_ts_check.log.logger.error(url_info + "cant connect")
        return (flag , url_info)   
    
    def check_m3u8(self):
        """check m3u8"""
        flag = 1    
        (m3u8_resp_flag, m3u8_resp) = self.http_urllib.connect_times(self.m3u8_addr , etc.HTTP_RETRY)
        if m3u8_resp_flag != 1:
            flag = -1            
            Jobsfe_ts_check.log.logger.error(self.m3u8_addr + "cant connect")
        return (flag, self.m3u8_addr)

  
    def check_m3u8_url(self, url):
        """check m3u8"""
        flag = 1    
        (m3u8_resp_flag, m3u8_resp) = self.http_urllib.connect_times(url, etc.HTTP_RETRY)
        if m3u8_resp_flag != 1:
            flag = -1            
            Jobsfe_ts_check.log.logger.error(self.m3u8_addr + "cant connect")
        return flag
  
        
                
                
                        
        
