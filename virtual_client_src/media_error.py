#!/usr/bin/python
#FILE_NAME: media_error.py

"""total the ms error num
"""


class media_error:
    ''' total  every_ms error num'
    '''

    def __init__(self):
        """ init the ms_error_dict"""
        self.media_error_dict = {}
        
    
    def  meidia_ms_erronum(self, apad_list, aphone_list, winphone_list, ipad_list, iphone_list):
        '''get all of ms error
        '''
        #clear the wrong ms number dict
        self.media_error_dict.clear()
        #all meidia_error
        addr_error_list = []
        # get  apad list 
        error_list = self.media_error_addr(apad_list, "mp4")
        addr_error_list.extend(error_list)

        # get  aphone list 
        error_list = self.media_error_addr(aphone_list, "mp4")
        addr_error_list.extend(error_list)        

        # get  winphone list
        error_list = self.media_error_addr(winphone_list, "mp4")
        addr_error_list.extend(error_list)

        # get  ipad list 
        error_list = self.media_error_addr(ipad_list, "ts")
        addr_error_list.extend(error_list)

        # get  iphone list
        error_list = self.media_error_addr(iphone_list, "ts")
        addr_error_list.extend(error_list)

        #parse all error_media_addr
        for every_addr in addr_error_list:
            self.media_http_parse(every_addr)
        return self.media_error_dict

    
    
    def  media_error_addr(self, error_list, _type):
        """ total all every_client meida _error
        """
        media_error_list = []
        for every_channel in error_list:        
            for every_error in every_channel:
                error = every_error.split(r';')
                error_len = len(error)
                if _type == "mp4":
                    if error_len == 4:
                        media_error_list.append(error[-1])
                if _type == "ts":
                    if error_len == 4 or error_len == 5:
                        media_error_list.append(error[-1])
        return media_error_list
         
    def  media_http_parse(self, http_addr):
        '''parse http addr
        '''
        url = http_addr.split(r'/', 3)
        ms_addr = url[2]
        if self.media_error_dict.has_key(ms_addr):
            self.media_error_dict[ms_addr] += 1
        else:
            self.media_error_dict[ms_addr] = 1


    def  media_url_num(self, ts_list, mp4_list):
        ''' get the ms error num by list 
        '''
        self.media_error_dict = {}
        for every in ts_list:
            self.media_http_parse(every)
        for every in mp4_list:
            self.media_http_parse(every)

        return self.media_error_dict
        
        
        



if __name__ == "__main__":
    # follows for test
    a = ["a;b;c;a//1/ad", "a;b;c;a//1/ad", "a;b;c;c//2"]
    b = ["a;b"]
    c = ["a;b;c;a//1/ad", "a;b;c;a//1/ad", "a;b;c//2"]
    d = [""]
    e = ["a;b;c;a//12.32/fasfa", "a;b;a//7878//f;faf//1234567/afasf"]
    media = media_error()
    mydict = media.meidia_ms_erronum(a, b, c, d, e)
#    for info in mydict:
#        print info
#        print mydict[info]
     
