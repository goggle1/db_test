#!/usr/bin/python
 
import smtplib
from email.mime.text import MIMEText  

import etc
import log



def send_mail(apad_list, aphone_list, winphone_list, ipad_list, iphone_list, error_num):
    '''send mail
    '''
    
    logger = log.MakeLog()
#    video_ok = "all is ok\n"
    all_list = []
    all_list.append(apad_list)
    all_list.append(aphone_list)
    all_list.append(winphone_list)
    all_list.append(ipad_list)
    all_list.append(iphone_list) 
    fromaddr = "sm@funshion.com"
    toaddrs = etc.ADDRS
#    subject = ""
    username = "sm@funshion.com"
    password = "FUNshion890*()"
    content_str = ""
    subject = "[Virtual Client][Circulate] send mail per hour" 
    
    content_str += "<table cellspacing=\"1\" border=\"1\">"
    content_str += "<tr><td>client</td><td>focus/channel</td><td>media_type</td><td>jsonfe</td><td>jobsfe</td><td>mediaserver</td></tr>"
    content_str += "<tr><td>error_num</td><td></td><td></td><td>%s</td><td>%s</td><td>%s</td></tr>" % (error_num[0], error_num[1], error_num[2])
    
    
    for i  in range(0, 5):
        j = 0
        content_str += "<tr><td>%s</td><td></td><td></td><td></td><td></td><td></td></tr>" % (etc.CLIENT[i])
        content_str += "<tr><td></td><td>focus</td><td></td><td></td><td></td><td></td></tr>"
        client_list = all_list[i]
        for video_type in etc.VIDEO_TYPE:
            if j >= len(client_list):
                break
            content_str +="<tr><td></td><td></td><td>%s</td><td></td><td></td><td></td></tr>" % (video_type) 
            every_error = client_list[j]  
            if len(every_error) == 0:
                content_str += "<tr><td></td><td></td><td></td><td>all is ok</td><td></td><td></td></tr>"                 
            for error_info in every_error:                
                error = error_info.split(r';')
                error_len = len(error)
                if error_len == 1:
                    content_str += "<tr><td></td><td></td><td></td><td><font color=#FF0000>%s</font></td><td></td><td></td></tr>" % (error[0])                        
                elif error_len == 2:
                    content_str += "<tr><td></td><td></td><td></td><td>%s%s<font color=#FF0000>%s</font></td><td></td><td></td></tr>" % (error[0],"||", error[1])
                elif error_len == 3:
                    content_str += "<tr><td></td><td></td><td></td><td>%s%s%s</td><td><font color=#FF0000>%s</font></td><td></td></tr>" % (error[0],"||", error[1],error[2])
                elif error_len == 4:
                    content_str += "<tr><td></td><td></td><td></td><td>%s%s%s</td><td>%s</td><td><font color=#FF0000>%s</font></td></tr>" % (error[0],"||", error[1],error[2],error[3])
                elif error_len == 5:
                    content_str += "<tr><td></td><td></td><td></td><td>%s%s%s</td><td>%s</td><td>%s%s<font color=#FF0000>%s</font></td></tr>" % (error[0],"||", error[1], error[2], error[3],"||", error[4])
            j += 1

        

        content_str += "<tr><td></td><td>channel</td><td></td><td></td><td></td><td></td></tr>"        
        for video_type in etc.VIDEO_TYPE:
            if j >= len(client_list):
                break  
            content_str += "<tr><td></td><td></td><td>%s</td><td></td><td></td><td></td></tr>" %(video_type)         
            every_error = client_list[j]  
            if len(every_error) == 0:
                content_str += "<tr><td></td><td></td><td></td><td>all is ok</td><td></td><td></td></tr>"                 
            for error_info in every_error:                
                error = error_info.split(r';')
                error_len = len(error)
                if error_len == 1:
                    content_str += "<tr><td></td><td></td><td></td><td><font color=#FF0000>%s</font></td><td></td><td></td></tr>" % (error[0])                        
                elif error_len == 2:
                    content_str += "<tr><td></td><td></td><td></td><td>%s%s<font color=#FF0000>%s</font></td><td></td><td></td></tr>" % (error[0],"||", error[1])
                elif error_len == 3:
                    content_str += "<tr><td></td><td></td><td></td><td>%s%s%s</td><td><font color=#FF0000>%s</font></td><td></td></tr>" % (error[0],"||", error[1],error[2])
                elif error_len == 4:
                    content_str += "<tr><td></td><td></td><td></td><td>%s%s%s</td><td>%s</td><td><font color=#FF0000>%s</font></td></tr>" % (error[0],"||", error[1],error[2],error[3])
                elif error_len == 5:
                    content_str += "<tr><td></td><td></td><td></td><td>%s%s%s</td><td>%s</td><td>%s<font color=#FF0000>%s</font></td></tr>" % (error[0],"||", error[1], error[2], error[3], error[4])
            j += 1
            
                                         
    # Add the From: and To: headers at the start!
    msg = MIMEText(content_str, _subtype='html', _charset='gb2312')  
    msg['Subject'] =  subject
    msg['From'] = fromaddr
    msg['To'] = ";".join(toaddrs)             

    try:
        server = smtplib.SMTP('mail.funshion.com', 25, 'mysql1221')
        server.login(username, password)
        server.sendmail(fromaddr, toaddrs, msg.as_string())
        server.quit()
    except (NameError, IOError, UnboundLocalError), err:
        logger.logger.error(err)
        logger.logger.error("send mail failed.")

        
def send_ms_mail(ms_error_dict):
    '''ms error then send email
    '''
    logger = log.MakeLog()

    fromaddr = "sm@funshion.com"
    toaddrs = etc.ADDRS
#    subject = ""
    username = "sm@funshion.com"
    password = "FUNshion890*()"
    content_str = ""
    subject = "[Virtual Client][Circulate]send mail per hour" 
    for every_ms in ms_error_dict:
        content_str = content_str + "ms:%s  error_num:%s" % (every_ms, ms_error_dict[every_ms])
    
    msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n"
           % (fromaddr, ", ".join(toaddrs), subject))
    msg  = msg + content_str
    try:
        server = smtplib.SMTP('mail.funshion.com', 25, 'mysql1221')
        server.login(username, password)
        server.sendmail(fromaddr, toaddrs, msg)
        server.quit()
    except (NameError, IOError, UnboundLocalError), err:
        logger.logger.error(err)
        logger.logger.error("send mail failed.")
        
        
        
def send_msstatus_mail(ms, flag):
    '''send an email if the ms stat exception
    '''
    logger = log.MakeLog()
    fromaddr = "sm@funshion.com"
    toaddrs = etc.ADDRS
#    subject = ""
    username = "sm@funshion.com"
    password = "FUNshion890*()"
#    content_str = ""
    subject = "[Virtual Client][Circulate][set_ms_status] send mail per hour" 
    content_str  = "set ms : %s    status: %s " % (ms, flag)
    msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n"
           % (fromaddr, ", ".join(toaddrs), subject))
    msg  = msg + content_str 
    try:
        server = smtplib.SMTP('mail.funshion.com', 25, 'mysql1221')
        server.login(username, password)
        server.sendmail(fromaddr, toaddrs, msg)
        server.quit()
    except (NameError, IOError, UnboundLocalError), err:
        logger.logger.error(err)
        logger.logger.error("send mail failed.")
        
        
if __name__ == "__main__":
    #send_msstatus_mail("afasdfas", 1)
    ms_dict = {}
    ms_dict["dfafa"] = 1
    #send_ms_mail(ms_dict)
    apad_list     = [[], [], [], [], [], [], [], []]
    aphone_list   = [[], [], [], [], [], [], [], []]
    winphone_list = [[], [], [], [], [], [], [], []]
    ipad_list     = [[], [], [], [], [], [], [], []]
    iphone_list   = [[], [], [], [], [], [], [], []]
    all_error_num = [2, 2, 2]
    send_mail(apad_list, aphone_list, winphone_list, ipad_list, iphone_list, all_error_num)
