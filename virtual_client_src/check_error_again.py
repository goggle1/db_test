#!/usr/bin/python
#FILENAME:check_error_again
'''file check_error_again.py
'''
#import jsonfe_check
import jobsfe_check
import media_check
#import http

class check_error_again:
    '''the last check
       check the error again to prevent the mistake error
    ''' 
    def __init__(self):
        self.media = media_check.Media_check()
        self.jobsfe_ts = jobsfe_check.Jobsfe_ts_check()
    
    def check_mp4_again(self, apad_list, aphone_list, winphone_list):
        '''check the error list of mp4: apad aphone winphone
        '''
        apad_list = self.check_mp4(apad_list)
        aphone_list = self.check_mp4(aphone_list)
        winphone_list = self.check_mp4(winphone_list)    
        return (apad_list, aphone_list, winphone_list)        
       
       
    def check_mp4(self, client_list):
        ''' check one client error_list 
        '''

        temp_error_list = []
        temp_client_list = []
        
        for channel_error in client_list:
            temp_error_list = []
            for every_error in channel_error:
                error = every_error.split(r';')
                error_len = len(error)
                if error_len == 4:
                    true_addr_list = error[3].split(']')
                    media_addr = true_addr_list[-1]
                    (flag, url)=self.media.check_mp4_media(media_addr)
                    if flag != 1:
                        temp_error_list.append(every_error)
                else:
                    temp_error_list.append(every_error)
            temp_client_list.append(temp_error_list)
        client_list = temp_client_list
        return client_list
        
    def check_mp4_list(self, mp4_list):
        '''check mp4 url error list
        '''
        temp_error_list = []
        for every_error in mp4_list:
            (flag, url)=self.media.check_mp4_media(every_error)
            if flag != 1:
                temp_error_list.append(every_error)
        mp4_list = temp_error_list
        return mp4_list
        
            
    def check_ts_again(self, ipad_list, iphone_list):
        '''check the error_list of ts: ipad iphone
        '''
        ipad_list = self.check_ts(ipad_list)
        iphone_list = self.check_ts(iphone_list)
        return (ipad_list, iphone_list)        
        
    def check_ts(self, client_list):
        '''check the error_list of ts
        '''
        
        temp_client_list = []
        temp_error_list = []
        for every_channel in client_list:
            temp_error_list = []
            for every_error in every_channel:
                error = every_error.split(r';')
                error_len = len(error)
                if error_len  == 5:
                    true_addr_list = error[4].split(']')
                    media_addr = true_addr_list[-1]
#                    print media_addr                    
                    (flag, url) = self.media.check_ts_media(media_addr)
                    if flag != 1:
                        temp_error_list.append(every_error)
#                    else:
#                        print "check ok"
                else:
                    temp_error_list.append(every_error)
            temp_client_list.append(temp_error_list)
            
        client_list = temp_client_list
        return client_list
        
        
    def check_ts_list(self, ts_list):
        ''' check ms url error
        '''
        temp_error_list = []
        for every_error in ts_list:    
            if every_error.find(".m3u8") == -1:            
                (flag, url) = self.media.check_ts_media(every_error)
                if flag != 1:
                    temp_error_list.append(every_error)
            else:
                flag = self.jobsfe_ts.check_m3u8_url(every_error)
                if flag != 1:
                    temp_error_list.append(every_error)
                 
        ts_list = temp_error_list
        return  ts_list
       
       
