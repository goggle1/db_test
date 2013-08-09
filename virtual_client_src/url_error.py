#!/usr/bin/python 
#coding=utf-8
#FILE_NAME=url_error
'''deal the error url
'''

import etc
#import log
import http
import check_error_again
import media_error

class set_tuner_ms:
    '''set ms can use or can't use
    '''
    http_mod = http.Http_urllib()
    
    def __init__(self):
        pass
#        http_mod = http.Http_urllib()


    def  set_ms(self, ms, flag):
        '''set ms status
           set the four Tuner the ms  status : 1(ok) or 0(error)
        '''
        #http://ip:port/mgmt?cmd=modifymsstatus&cs=$ip:sport:mport&status=$status

        for addr in etc.TUNER_IP:
            if addr == "59.53.56.101":
                if ms.find(":80") == -1:
                    url = addr  + ":6002" + "/mgmt?cmd=modifymsstatus&cs="  + ms + ":80:6261" + "&status=%s" % (flag)
                else:
                    url = addr  + ":6002" + "/mgmt?cmd=modifymsstatus&cs="  + ms + ":6261" + "&status=%s" % (flag)
            else:
                if ms.find(":80") == -1:
                    url = addr  + ":8002" + "/mgmt?cmd=modifymsstatus&cs="  + ms + ":80:6261" + "&status=%s" % (flag)
                else:
                    url = addr  + ":8002" + "/mgmt?cmd=modifymsstatus&cs="  + ms + ":6261" + "&status=%s" % (flag)
            #self.http_mod.connect_times(url, etc.HTTP_RETRY)
#            print url
#        mail.send_msstatus_mail(ms, flag)


class url_error:
    '''class url_error
    '''
    def __init__(self):
        self.ms_error_old_dict = {}
        
        self.mp4_url_error_list = []
        self.ts_url_error_list = []
        self.check_ms = check_error_again.check_error_again()

        self.take_ms_old_num = media_error.media_error()
        self.take_ms_new_num = media_error.media_error()


    def append_error_url(self, apad_list, aphone_list, winphone_list, ipad_list, iphone_list):
        '''get all error url
        '''
        ms_error_new_dict = {}
        
        new_mp4_url_list = []
        new_ts_url_list = []
        temp_url_list = []

        temp_url_list = self.take_ms_new_num.media_error_addr(apad_list, "mp4")
        new_mp4_url_list.extend(temp_url_list)

        temp_url_list = self.take_ms_new_num.media_error_addr(aphone_list, "mp4")
        new_mp4_url_list.extend(temp_url_list)

        temp_url_list = self.take_ms_new_num.media_error_addr(winphone_list, "mp4")
        new_mp4_url_list.extend(temp_url_list)
        
        temp_url_list = self.take_ms_new_num.media_error_addr(iphone_list, "ts")
        new_ts_url_list.extend(temp_url_list)
        
        temp_url_list = self.take_ms_new_num.media_error_addr(ipad_list, "ts")
        new_ts_url_list.extend(temp_url_list)


        # check the  old error url 
#        print len(self.mp4_url_error_list)
#        print len(self.ts_url_error_list)
        self.mp4_url_error_list = self.check_ms.check_mp4_list(self.mp4_url_error_list)
        self.ts_url_error_list = self.check_ms.check_ts_list(self.ts_url_error_list)
        
        # get the old error ms num 
        #print len(self.mp4_url_error_list)
        #print len(self.ts_url_error_list)
        self.ms_error_old_dict = self.take_ms_old_num.media_url_num(self.mp4_url_error_list, self.ts_url_error_list)
                            
        #print self.ms_error_old_dict
        # get the new error ms  num         
        ms_error_new_dict = self.take_ms_new_num.meidia_ms_erronum(apad_list, aphone_list, winphone_list, ipad_list, iphone_list)
        #print ms_error_new_dict
        for info in self.ms_error_old_dict:
            if ms_error_new_dict.has_key(info):
                pass
            else:
                ms_error_new_dict[info] = self.ms_error_old_dict[info]
        
        ms_recover_list = []
        ms_new_error_list = []
        (ms_recover_list, ms_new_error_list)=self.ms_error_compare(ms_error_new_dict)
        
        self.total_lastest_error_url(new_mp4_url_list, new_ts_url_list, ms_recover_list, ms_new_error_list)

    def total_lastest_error_url(self, new_mp4_url_list, new_ts_url_list, ms_recover_list, ms_new_error_list):
        '''current time url error
        '''
        temp_mp4_url = []
        temp_ts_url = []
        for every_recover in ms_recover_list:
            for every_url in self.mp4_url_error_list:
                if every_url.find(every_recover) == -1:
                    temp_mp4_url.append(every_url)
            for every_url in self.ts_url_error_list:
                if every_url.find(every_recover) == -1:
                    temp_mp4_url.append(every_url)
                     
        for  every_error in ms_new_error_list:        
            for every_url in new_mp4_url_list:
                if every_url.find(every_error) != -1:
                    temp_mp4_url.append(every_url)

            for every_url in new_ts_url_list:
                if every_url.find(every_error) != -1:
                    temp_ts_url.append(every_url)
                    
        self.mp4_url_error_list = temp_mp4_url[:]
        self.ts_url_error_list = temp_ts_url[:]


    def ms_error_compare(self, ms_error_new_dict):
        ''' set the ms status in tuner mgmt
        '''
        ms_recover_list = []
        # the new find ms error
        ms_error_list = []
        
        ms_take_dict = {}
        if len(ms_error_new_dict) <= etc.MS_NUM:
            for every_info in ms_error_new_dict:
                if ms_error_new_dict[every_info] > etc.MS_ERROR_NUM:
                    ms_take_dict[every_info] = ms_error_new_dict[every_info]

            #set the ms status : 1  the ms has recover
            #the error ms in the old dict but not in the new dict
            for every_info in self.ms_error_old_dict:
                if ms_take_dict.has_key(every_info):
                    continue
                else:
                    #print  every_info , "1"
                    #set_ms(every_info, 1)
                    # take the ms in old_error_dict but not in the new 
                    ms_recover_list.append(every_info)

            # set the ms status : 0 the ms error
            # the ms in the new_error_dict but no in the old dict                 
            for info in ms_take_dict:
                if self.ms_error_old_dict.has_key(info):
                    continue
                else:
                    self.ms_error_old_dict[info] = ms_take_dict[info]
                    #self.set_ms(info, 0)
#                    print info , "0"
                    ms_error_list.append(info)
            # delete the error dict in the old dict  : the ms not exit in the  new dict                 
            for  no_exit_ms  in ms_recover_list:
                del self.ms_error_old_dict[no_exit_ms]
                
            return (ms_recover_list, ms_error_list)
            
        
            
        
if __name__ == "__main__":
    apad_list = [["a;a;a;http://192.168.16.34:8000/fasfasf"]*8]
    aphone_list = apad_list
    winphone_list = apad_list
    ipad_list =  [["a;a;a;a;http://192.168.16.34:8000/fasfasf.m3u8"]*8]
    iphone_list = ipad_list
    #print apad_list
    k = url_error()
    k.append_error_url(apad_list, aphone_list, winphone_list, ipad_list, iphone_list)

    
#    print "sssssssssssssssssssssssssssssssssssssssssssss"
    new_apad_list = [[]*8]
    new_aphone_list = new_apad_list
    new_winphone_list = new_apad_list
    new_ipad_list  = new_apad_list
    new_iphone_list = new_apad_list 
    k.append_error_url(new_apad_list, new_aphone_list, new_winphone_list, new_ipad_list, new_iphone_list)
    
    #url_error_del = url_error()
     
