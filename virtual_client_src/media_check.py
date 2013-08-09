#!/usr/bin/python
#FILE_NAME:check_media.py
'''get the media head
'''
from socket import *

import etc
#import mail
import log


class  Media_check:
    '''check media
    '''
    
    log =  log.MakeLog()
    
    def __init__(self):
        pass
        
        
    def get_resp(self, addr):
        """ get mp4 or ts data from media_server """
     
        i = 0
        data = ""
        mylist = addr.split(r'/')
        ms = mylist[2].split(r':')
        command = '/'.join(mylist[3:])
        HOST = ms[0]
        PORT = int(ms[1])
        content = "GET %s%s HTTP/1.1\r\nHost: %s\r\nConnection: keep-alive\r\nRange: bytes=0-250\r\n\r\n" % ('/', command, ms[0])
        BUFSIZE = 1024
        ADDR = (HOST, PORT)
#        tcpsock = socket(AF_INET, SOCK_STREAM)
#        tcpsock.settimeout(etc.HTTP_TIMEOUT)
        while (i < etc.HTTP_RETRY):
            try:
                tcpsock = socket(AF_INET, SOCK_STREAM)
                tcpsock.settimeout(etc.HTTP_TIMEOUT)
                tcpsock.connect(ADDR)
                tcpsock.send(content)
                data = tcpsock.recv(BUFSIZE)
                data = tcpsock.recv(BUFSIZE)
            except Exception, err:
                Media_check.log.logger.error(err)
            finally:
                tcpsock.close()
            if len(data) < 50:
                i += 1
                Media_check.log.logger.error(addr + "  error the %s time" %(i))
            else:
                return data
        return  data
         
                   
                   
                   
    def check_mp4_media(self, addr):
        '''check the mp4 type  from 16 to 20  is or not = isom
        '''
        flag  = 1
        data = self.get_resp(addr)
        if data == None:
            return (-1, addr)
        if len(data) > 50:
            if data[16:20] != "isom":
                flag = 0
                Media_check.log.logger.error("the video_type error")
        else:
            flag = -1

        return (flag, addr)
            
            
                    
                    
    def check_ts_media(self, addr):
        '''check the ts from 1 to 2 is or not = G@
        '''
        flag = 1
        data = self.get_resp(addr)
        if data == None:
            return(-1, addr)
        if len(data) > 50:
            if data[0:2] != "G@":
                flag = 0
                Media_check.log.logger.error("the video_type error")
        else:
            flag = -1
        return (flag, addr)

    def check_mp4_media_times(self, addr, count):
        '''connect the media_server  times  check mp4
        '''
        i = 0
        while (i< count):
            (addr_flag, addr) = self.check_mp4_media(addr)
            if addr_flag != 1:
                i += 1
            else:
                break
        return (addr_flag, addr)
        
    def check_ts_media_times(self, addr, count):
        ''' connect the media_server times check mp4
        '''
#       flag = 0
        i = 0
        while (i< count):
            (addr_flag, addr) = self.check_ts_media(addr)
            if addr_flag != 1:
                i += 1
            else:
                break
        return (addr_flag, addr)
        
        
                
