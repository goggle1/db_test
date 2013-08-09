#!/usr/bin/python
#Filename:http.py

"""Deal with the HTTP."""

import httplib
import log
import etc
import urllib2
#import time


class Http_urllib:
    '''http_urllib'''
    def  __init__(self):
        pass

    def http_method(self, url):
        """del with http method  of urllib"""
        
        logger = log.MakeLog()
        try:
            resp = urllib2.urlopen(url, timeout = etc.HTTP_TIMEOUT)
        except Exception, err:
            logger.logger.error(err)
        else:
            if resp.getcode() != 200:
                logger.logger.error('resp status is '+str(resp. status))
                return ''
            try:
                return resp.read()
            except Exception, err_read:
                logger.logger.error(err_read)
        return ''
    
    def connect_times(self, addr, count):
        """HTTP request with addr and content ,total retry count times.
    
        return 0, means all failed;return 1,means success"""
    
        logger = log.MakeLog()
        flag = 0
        i = 0
#        t_cost = 0
        while (i< count):
            resp = self.http_method(addr)
            if resp == '':
                i += 1
                out_str = addr+" request error time:"+str(i)
                logger.logger.error(out_str)
            else:
                out_str = addr+" request success time:"+str(i+1)
                logger.logger.info(out_str)
                flag = 1
                break
        return (flag, resp)





class Http:
    '''Http method'''

    def __init__(self):
        pass

    def http_method(self, url, content):
        """Deal with the HTTP method."""
        
        logger = log.MakeLog()
        try:
            conn = httplib.HTTPConnection(url, timeout = etc.HTTP_TIMEOUT)
            conn.request("GET", content)
            resp = conn.getresponse()
            conn.close()
        except Exception, err:
            logger.logger.error(err)
        else:
            if resp.status == 302:
                return   resp.getheader("Location")
            if resp.status != 200:
                logger.logger.error('resp status is '+str(resp. status))
                return ''
            try:
                return resp.read()
            except Exception, err_read:
                logger.logger.error(err_read)
        return ''
    
    def connect_times(self, addr, content, count):
        """HTTP request with addr and content ,total retry count times.
    
        return 0, means all failed;return 1,means success"""
    
        logger = log.MakeLog()
        flag = 0
        i = 0
#        t_cost = 0
        while (i< count):
            resp = self.http_method(addr, content)
            if resp == '':
                i += 1
                out_str = addr+content+" request error time:"+str(i)
                logger.logger.error(out_str)
            else:
                out_str = addr+content+" request success time:"+str(i+1)
                #logger.logger.info(out_str)
                flag = 1
                break
        return (flag, resp)
        

    

        
