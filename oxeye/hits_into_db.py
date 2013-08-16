#!/usr/bin/python
#coding=utf-8

import sys
import re
import MySQLdb
reload(sys)
sys.setdefaultencoding('utf8')

class DB_MYSQL :
    conn = None
    cur = None
    def connect(self, host, port, user, passwd, db, charset='utf8') :
        self.conn = MySQLdb.connect(host, user, passwd, db, port, charset='utf8')
        self.cur  = self.conn.cursor()
    def execute(self, sql):           
        self.cur.execute(sql)
    def close(self):
        self.cur.close()
        self.conn.close()

db = DB_MYSQL()
db.connect("192.168.160.203", 3306, "admin", "123456", "hits")

log_file_path = sys.argv[1]
log_file = open(log_file_path, "r")
while True :
    line = log_file.readline()
    if line == '':
        break

    try :
        datas = line.split(',')
        if len(datas) >= 10 :
            client_ip   = datas[0].strip()
            client_area = datas[1].strip()
            client_isp  = datas[2].strip()
            hashid      = datas[3].strip()
            ms_ip       = datas[4].strip()
            ms_area     = datas[5].strip()
            ms_isp      = datas[6].strip()
            client_mac  = datas[7].strip()
            buffer_status=datas[8].strip()
            buffer_time = datas[9].strip()
            play_time   = datas[10].strip()
            sql = "insert into hits_oxeye values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', FROM_UNIXTIME('%s'))"%(client_ip, client_area, client_isp, hashid, ms_ip, ms_area, ms_isp, client_mac, buffer_status, buffer_time, play_time)
            print sql
            db.execute(sql)
    except ValueError :
        continue
log_file.close()
db.close()
