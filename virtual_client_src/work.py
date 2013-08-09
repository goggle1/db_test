#!/usr/bin/python
#FILE_NAMR:work.py

'''this is the file work.py. defined a class----Work'''

import etc

class Work:
    '''if ms game over add or delete the black_list
    '''
    def __init__(self):
        '''init was passd'''
        pass

    def  set_ms_num(self, num):
        '''set the number of ms'''
        etc.MS_NUM = num
        return  self.query_stat()

    def set_ms_error_num(self, num):
        '''set the upper bound error number'''
        etc.MS_ERROR_NUM = num
        return self.query_stat()

    def query_stat(self):
        '''query the stat of mgmt server'''
#        print "the last query stat"
        return 'return=succ\r\nms_num=%s\r\nms_error_num=%s' % (etc.MS_NUM, etc.MS_ERROR_NUM)

    @classmethod
    def ins(cls):
        '''instance
        '''
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        return cls._instance


