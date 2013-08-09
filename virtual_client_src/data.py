#!/usr/bin/python
#FILE_NAME: data.py
'''data.py. calculate all error
'''

def total_client_error(client_list):
    '''total one clietn error number
    '''
    error_num_list = [0, 0, 0]
    for every_channel_error in client_list:
        for every_error in every_channel_error:
            every_error_list = every_error.split(r';')
            error_len = len(every_error_list)
            if error_len == 1 or error_len == 2:
                error_num_list[0] += 1
            elif error_len == 3:
                error_num_list[1] += 1
            elif error_len == 4 or error_len == 5:
                error_num_list[2] += 1
    return  error_num_list

def total_all_error(apad_list, aphone_list, winphone_list, ipad_list, iphone_list):
    '''total the jsonfe jobsfe and media_server error numeber
    '''
    #total every_client error
    all_error_num = [0, 0, 0]
    apad_error = total_client_error(apad_list)
    aphone_error = total_client_error(aphone_list)
    winphone_error = total_client_error(winphone_list)
    ipad_error = total_client_error(ipad_list)
    iphone_error = total_client_error(iphone_list)
    
    #total the all_error
    all_error_num[0] = apad_error[0] + aphone_error[0] + winphone_error[0] + ipad_error[0] + iphone_error[0]
    all_error_num[1] = apad_error[1] + aphone_error[1] + winphone_error[1] + ipad_error[1] + iphone_error[1]
    all_error_num[2] = apad_error[2] + aphone_error[2] + winphone_error[2] + ipad_error[2] + iphone_error[2]
    return all_error_num
    
    

                
        
    
