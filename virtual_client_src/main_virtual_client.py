#!/usr/bin/python
#FILE_NAME: main_virtual_client

""" the main function"""

import threading
import time

import server
import cshandler
import log
import mail
import etc
import data
import jsonfe_check
import jobsfe_check
import media_check
import check_error_again
import media_error
import url_error
import send_mail_per_hour

logger = log.MakeLog()
logger.start()
media_dict = {}

apad_list     = []
aphone_list   = []
winphone_list = []
ipad_list     = []
iphone_list   = []

apad_list_mutex     = threading.Lock()
aphone_list_mutex   = threading.Lock()
winphone_list_mutex = threading.Lock()
ipad_list_mutex     = threading.Lock()
iphone_list_mutex   = threading.Lock()

def get_time():
    '''get system time
    '''
    return "[" + time.strftime("%m-%d::%X", time.localtime(time.time())) + "]"

def check_ts_addr(time_json_addr, jsonfe, jobsfe, media, addr_list, client_error):
    ''' check the media_type of ts
    '''
    for every_mid in jsonfe.mid_list:
        (mid_purl_flag, mid_purl_addr) = jsonfe.get_mid_addr(every_mid)
        time_mid_purl_addr = get_time() + mid_purl_addr    
        if mid_purl_flag != 1:
            addr = time_json_addr + ";" + time_mid_purl_addr
            addr_list.append(addr)
            client_error[0] += 1
        else:
            for every_purl in jsonfe.purl_list:
                (get_media_addr_flag, purl) = jobsfe.get_media_addr(every_purl)
                time_purl = get_time() + purl
                if get_media_addr_flag != 1:
                    addr =  time_json_addr + ";" + time_mid_purl_addr + ";" +  time_purl
                    addr_list.append(addr)
                    client_error[1] += 1
                else:
                    (m3u8_flag, m3u8_addr) = jobsfe.check_m3u8()
                    time_m3u8_addr = get_time() + m3u8_addr 
                    if m3u8_flag != 1:
                        addr = time_json_addr + ";" + time_mid_purl_addr + ";" +  time_purl + ";" + time_m3u8_addr
                        addr_list.append(addr)
                        client_error[2] += 1
                    else:
                        (check_media_flag, media_addr) = media.check_ts_media_times(jobsfe.ts_addr, etc.MS_RETRY)
                        time_media_addr =  get_time() + media_addr                        
                        if check_media_flag == 0:
                            addr = "[Warning]" + time_json_addr + ";" + time_mid_purl_addr + ";" +  time_purl + ";" + time_media_addr
                            addr_list.append(addr) 
                            client_error[2] += 1
                        elif check_media_flag == -1:
                            addr = time_json_addr + ";" + time_mid_purl_addr + ";" +  time_purl + ";" + time_media_addr
                            addr_list.append(addr)
                            client_error[2] += 1

def check_mp4_addr(time_json_addr, jsonfe, jobsfe, media, addr_list, client_error):
    ''' check the media type of mp4
    '''
    for every_mid in jsonfe.mid_list:
        #print every_mid
        (mid_purl_flag, mid_purl_addr) = jsonfe.get_mid_addr(every_mid)
        time_mid_purl_addr = get_time() + mid_purl_addr
        if mid_purl_flag != 1:
            addr = time_json_addr + ";" + time_mid_purl_addr
            addr_list.append(addr)
            client_error[0] += 1
        else:
            #print len(jsonfe.purl_list)
            for every_purl in jsonfe.purl_list:
                (get_media_addr_flag, purl) = jobsfe.get_media_addr(every_purl)
                time_purl = get_time() + purl
                if get_media_addr_flag != 1:
                    addr =  time_json_addr + ";" + time_mid_purl_addr + ";" +  time_purl
                    addr_list.append(addr)
                    client_error[1] += 1
                else:
                    (check_media_flag, media_addr) = media.check_mp4_media_times(jobsfe.jobsfe_addr, etc.MS_RETRY)
                    time_media_addr = get_time() + media_addr
                    if check_media_flag == 0:
                        addr = "[Warning]" + time_json_addr + ";" + time_mid_purl_addr + ";" +  time_purl + ";" + time_media_addr
                        addr_list.append(addr)
                        client_error[2] += 1                        
                    elif check_media_flag == -1:
                        addr = time_json_addr + ";" + time_mid_purl_addr + ";" +  time_purl + ";" + time_media_addr
                        addr_list.append(addr) 
                        client_error[2] += 1                        

def check_focus_type(jsonfe, jobsfe, media, addr_list, video_type, mp4_ts, client_error):
    ''' check the focus type
    '''
    (focus_mid_flag, mid_addr) = jsonfe.jsonfe_focus_type(video_type)
    time_json_addr = get_time() + mid_addr
    if focus_mid_flag != 1:
        addr_list.append(time_json_addr)
        client_error[0] += 1
    else:
        if mp4_ts == "mp4":
            check_mp4_addr(time_json_addr, jsonfe, jobsfe, media, addr_list, client_error)
        elif mp4_ts == "ts":
            check_ts_addr (time_json_addr, jsonfe, jobsfe, media, addr_list, client_error)

def check_channel(jsonfe, jobsfe, media, addr_list, channel, mp4_ts, client_error):
    ''' check the channel 
    '''
    (channel_mid_flag, mid_addr) = jsonfe.get_channel_mid(channel)
    time_json_addr = get_time() + mid_addr
    if channel_mid_flag != 1:
        addr_list.append(time_json_addr)
        client_error[0] += 1
    else:
        if  mp4_ts == "mp4":
            check_mp4_addr(time_json_addr, jsonfe, jobsfe, media, addr_list, client_error)
        elif mp4_ts == "ts":
            check_ts_addr(time_json_addr, jsonfe, jobsfe, media, addr_list, client_error)        

def take_error(mutex, error_list, client_list):
    '''add the error into client_list
    '''
    mutex.acquire()
    client_list.append(error_list[:])
    mutex.release()
    del error_list[0:]

def check(mutex, jsonfe, jobsfe, media, client_list, mp4_ts, client_error):
    '''the thread function  check fcous and channel
    '''
    error_list = []

    #check the fous
    for video_type in etc.VIDEO_TYPE:
        check_focus_type(jsonfe, jobsfe, media, error_list, video_type, mp4_ts, client_error )
        take_error(mutex, error_list, client_list)

    #check every channel
    for video_type in etc.VIDEO_TYPE:
        check_channel(jsonfe, jobsfe, media, error_list, video_type, mp4_ts, client_error)
        take_error(mutex, error_list, client_list)

def mgmt():
    '''start the mgmt server
    '''
    mgmt_server = server.Server(handler_class = cshandler.CSHandler, port = etc.mgmt_port)
    mgmt_server.run()

def main():
    ''' the main function
    '''
    mp4 = "mp4"
    ts = "ts"
    all_error_num = [0, 0, 0]    
    apad_error = [0, 0, 0]
    aphone_error = [0, 0, 0]
    winphone_error = [0, 0, 0]
    ipad_error = [0, 0, 0]
    iphone_error = [0, 0, 0]
    # the number of ms error
    ms_error_dict = {}
#    ms_error_old_dict = {}
    ms_take_dict = {}
    
    global apad_list
    global aphone_list
    global winphone_list
    global ipad_list
    global iphone_list
    
    global apad_list_mutex
    global aphone_list_mutex
    global winphone_list_mutex
    global ipad_list_mutex
    global iphone_list_mutex

    # hand  the  error url 
    check_error_url = url_error.url_error()

    #begin the mgmgt server to control the ms_error_num
    thre2 = threading.Thread(target = mgmt, args = ())
    thre2.start()    

    media = media_check.Media_check()
    media_ms_error = media_error.media_error()
    #define

    #apad
    jsonfe_mp4_apad = jsonfe_check.Jsonfe_check("apad", etc.APAD_PAGE_SIZE)
    jobsfe_mp4_apad = jobsfe_check.Jobsfe_mp4_check()
    #aphone
    jsonfe_mp4_aphone = jsonfe_check.Jsonfe_check("aphone", etc.APHONE_PAGE_SIZE)
    jobsfe_mp4_aphone = jobsfe_check.Jobsfe_mp4_check()
    #winphone
    jsonfe_mp4_winphone = jsonfe_check.Jsonfe_check("winphone", etc.WINPHONE_PAGE_SIZE)
    jobsfe_mp4_winphone = jobsfe_check.Jobsfe_mp4_check()
    #iphone
    jsonfe_ts_iphone = jsonfe_check.Jsonfe_check("iphone", etc.IPHONE_PAGE_SIZE)
    jobsfe_ts_iphone = jobsfe_check.Jobsfe_ts_check()
    #ipad
    jsonfe_ts_ipad = jsonfe_check.Jsonfe_check("ipad", etc.IPAD_PAGE_SIZE)
    jobsfe_ts_ipad = jobsfe_check.Jobsfe_ts_check()
    #def jobs_mp4 and ts to check err before send report   to reduce the mistake report number     
    check_last_error = check_error_again.check_error_again()

    #start the timer thread for send mail per hour
    timer_thread = threading.Thread(target = send_mail_per_hour.send_mail_per_hour, args = 
                                    (apad_list_mutex, aphone_list_mutex, winphone_list_mutex, 
                                     ipad_list_mutex,iphone_list_mutex, apad_list, aphone_list, 
                                     winphone_list, ipad_list, iphone_list))
    timer_thread.start()
    threads = [0]*5
    while(1):
        threads[0] = threading.Thread(target = check, args = (apad_list_mutex, jsonfe_mp4_apad, jobsfe_mp4_apad, media, apad_list, mp4, apad_error))
        threads[1] = threading.Thread(target = check, args = (aphone_list_mutex, jsonfe_mp4_aphone, jobsfe_mp4_aphone, media, aphone_list, mp4, aphone_error))
        threads[2] = threading.Thread(target = check, args = (winphone_list_mutex, jsonfe_mp4_winphone, jobsfe_mp4_winphone, media, winphone_list, mp4, winphone_error))
        threads[3] = threading.Thread(target = check, args = (ipad_list_mutex, jsonfe_ts_ipad, jobsfe_ts_ipad, media, ipad_list, ts, ipad_error))
        threads[4] = threading.Thread(target = check, args = (iphone_list_mutex, jsonfe_ts_iphone, jobsfe_ts_iphone, media, iphone_list, ts, iphone_error))

        #start all five threads
        for i in  range(len(threads)):
            threads[i].start()

        #join all five threads
        for i in  range(len(threads)):
            threads[i].join()

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
        
        #check the error before send error mail
        for i in [1, 2]:
            (apad_list_cp, aphone_list_cp, winphone_list_cp) = check_last_error.check_mp4_again(apad_list_cp, aphone_list_cp, winphone_list_cp)
            (ipad_list_cp, iphone_list_cp) = check_last_error.check_ts_again(ipad_list_cp, iphone_list_cp)        

        #calculate the error num of jsonfe jobsfe medeiaserver            
        all_error_num = data.total_all_error(apad_list_cp, aphone_list_cp, winphone_list_cp, ipad_list_cp, iphone_list_cp)        
        #send the report mail
        mail.send_mail(apad_list_cp, aphone_list_cp, winphone_list_cp, ipad_list_cp, iphone_list_cp, all_error_num )

        #check media_error
        ms_error_dict = media_ms_error.meidia_ms_erronum(apad_list_cp, aphone_list_cp, winphone_list_cp, ipad_list_cp, iphone_list_cp)

#        check_error_url.append_error_url(apad_list, aphone_list, winphone_list, ipad_list, iphone_list)        
        # send the ms error more than 10        
        for every_info in ms_error_dict:
            if ms_error_dict[every_info] > 10:
                ms_take_dict[every_info] = ms_error_dict[every_info]
        if len(ms_take_dict) != 0:               
            mail.send_ms_mail(ms_take_dict)

        #all_num init to zero
        all_error_num = [0, 0, 0]    
        apad_error = [0, 0, 0]
        aphone_error = [0, 0, 0]
        winphone_error = [0, 0, 0]
        ipad_error = [0, 0, 0]
        iphone_error = [0, 0, 0]    

        # del the (apad aphone winphone ipad iphone) error list
        del apad_list[0:]
        del aphone_list[0:]
        del winphone_list[0:]
        del ipad_list[0:]
        del iphone_list[0:]
        del apad_list_cp[0:]
        del aphone_list_cp[0:]
        del winphone_list_cp[0:]
        del ipad_list_cp[0:]
        del iphone_list_cp[0:]

        # del ms_error_dict
        ms_error_dict.clear()
        ms_take_dict.clear()
    timer_thread.join()

if __name__ == "__main__":
    main()

