#!/bin/bash

YESTERDAY=`date "+%Y%m%d%H" -d "$DAYSAGO days ago"`
FILE_NAME="/home/guoqiang/data/${YESTERDAY}.txt"
/usr/bin/mysql -h192.168.8.121 -udbs -pR4XBfuptAH -e"select * from fs_media_stat where web_daynum > 0 order by mediaid" corsair_0 > ${FILE_NAME}
