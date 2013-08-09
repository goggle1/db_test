#!/usr/bin/python
#Filename:log.py

"""Control log function."""

import etc
import os.path
#import logging
import logging.handlers


class Singleton(object):
    '''define a singleton class
    '''  
    def __new__(cls, *args, **kw):  
        if not hasattr(cls, '_instance'):  
            orig = super(Singleton, cls)  
            cls._instance = orig.__new__(cls, *args, **kw)  
        return cls._instance  
        
class MakeLog(Singleton):
    '''Log module.Log to the screen and the file with level.'''
    logger = None
    
    def __init__(self):
        self.t_logger = None

    def start(self):
        """Start the log module."""
        
        if os.path.exists("./log/"):
            pass
        else:
            os.mkdir("./log/")
        self.logger = logging.getLogger('MS_Check')
        self.logger.setLevel(logging.DEBUG)
        fh = logging.handlers.TimedRotatingFileHandler('./log/info.log', 'D', 1, 7)
        fh.setLevel(logging.INFO)
        formatter = logging.Formatter("[%(asctime)s][%(levelname)s]%(message)s[file:%(filename)s,func:%(funcName)s,line:%(lineno)d]")
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)        
        if etc.SCREEN_ON == 1:        
            sh = logging.StreamHandler()
            sh.setLevel(logging.DEBUG)
            sh.setFormatter(formatter)
            self.logger.addHandler(sh)       
        
        self.t_logger = logging.getLogger('RECORD_RECEIVE')
        self.t_logger.setLevel(logging.DEBUG)
        t_fh = logging.handlers.TimedRotatingFileHandler('./log/record_receive.log', 'D', 1, 7)
        t_fh.setLevel(logging.INFO)
        t_fh.setFormatter(formatter)
        self.t_logger.addHandler(t_fh)



