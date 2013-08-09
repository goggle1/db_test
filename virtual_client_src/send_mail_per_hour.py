import threading
import time

import log
import mail
import data
import media_error

log = log.MakeLog()
log.start()

def send_mail_per_hour(apad_list_mutex, aphone_list_mutex, winphone_list_mutex, ipad_list_mutex,
                       iphone_list_mutex, apad_list, aphone_list, winphone_list, ipad_list, iphone_list):
    while 1:
        apad_list_mutex.acquire()
        apad_list_cp = apad_list[:]
        apad_list_mutex.release()
        
        aphone_list_mutex.acquire()
        aphone_list_cp = aphone_list[:]
        aphone_list_mutex.release()
        
        winphone_list_mutex.acquire()
        winphone_list_cp = winphone_list[:]
        winphone_list_mutex.release()
        
        ipad_list_mutex.acquire()
        ipad_list_cp = ipad_list[:]
        ipad_list_mutex.release()
        
        iphone_list_mutex.acquire()
        iphone_list_cp = iphone_list[:]
        iphone_list_mutex.release()
        
        # the number of ms error
        ms_error_dict = {}
        ms_take_dict = {}
        
        #calculate the error num of jsonfe jobsfe medeiaserver        
        all_error_num = data.total_all_error(apad_list_cp, aphone_list_cp, 
                                             winphone_list_cp, ipad_list_cp, iphone_list_cp)    
        #send the report mail
        mail.send_mail(apad_list_cp, aphone_list_cp, 
                       winphone_list_cp, ipad_list_cp, iphone_list_cp, all_error_num )
        #check media_error
        media_ms_error = media_error.media_error()
        ms_error_dict = media_ms_error.meidia_ms_erronum(apad_list_cp, aphone_list_cp, 
                                             winphone_list_cp, ipad_list_cp, iphone_list_cp)
    
        #check_error_url.append_error_url(apad_list, aphone_list, winphone_list, ipad_list, iphone_list)    
        # send the ms error more than 10    
        for every_info in ms_error_dict:
            if ms_error_dict[every_info] > 10:
                ms_take_dict[every_info] = ms_error_dict[every_info]
        if len(ms_take_dict) != 0:               
            mail.send_ms_mail(ms_take_dict)
            
        ms_error_dict.clear()
        ms_take_dict.clear()
        time.sleep(3600)
