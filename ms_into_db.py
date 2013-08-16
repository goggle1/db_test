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
	platform_pc = "0"
	platform_mobile = "0"
	key_file = ""
	password = ""
        if len(datas) >= 13 :
            server_id   	= datas[0].strip()
            server_name 	= datas[1].strip()
            server_ip   	= datas[2].strip()
            server_port 	= datas[3].strip()
            controll_ip 	= datas[4].strip()
            controll_port 	= datas[5].strip()
            task_number 	= datas[6].strip()
            room_id     	= datas[7].strip()
            room_name   	= datas[8].strip()
            server_version 	= datas[9].strip()
            protocol_version    = datas[10].strip()
            is_valid            = datas[11].strip()
            platform         	= datas[12].strip()
            #key_file            = datas[13].strip()
            #password            = datas[14].strip()
		
            if cmp(platform, "mobile") == 0 :
                platform_mobile = "1"
                sql = "insert into mediaserver values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"\
" ON DUPLICATE KEY UPDATE platform_mobile='%s' and key_file='%s' and password = '%s'"\
%(server_id, server_name, server_ip, server_port, controll_ip, controll_port, task_number, room_id, room_name, server_version, protocol_version, is_valid, platform_pc, platform_mobile, key_file, password, \
platform_mobile, key_file, password)
            else :
                platform_pc = "1"
                sql = "insert into mediaserver values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"\
" ON DUPLICATE KEY UPDATE platform_pc='%s' and key_file='%s' and password = '%s'"\
%(server_id, server_name, server_ip, server_port, controll_ip, controll_port, task_number, room_id, room_name, server_version, protocol_version, is_valid, platform_pc, platform_mobile, key_file, password, \
platform_pc, key_file, password)
            print sql
            db.execute(sql)
    except ValueError :
        continue
log_file.close()
db.close()
