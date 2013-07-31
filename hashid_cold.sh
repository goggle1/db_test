#!/bin/bash
DATE=20130701
mysql -h192.168.8.121 -udbs -pR4XBfuptAH -e"select mediaid from fs_fsplay_stats where currentdate > ${DATE} group by mediaid order by mediaid" corsair_0 > mediaid_${DATE}.list
mysql -h192.168.8.121 -udbs -pR4XBfuptAH -e"select distinct(mediaid) from fs_media_stat order by mediaid" corsair_0 > mediaid_all_${DATE}.list 
diff mediaid_all_${DATE}.list mediaid_${DATE}.list -c > mediaid_diff_${DATE}.list
grep "^\-\ " mediaid_diff_${DATE}.list > mediaid_cold_${DATE}.list

function do_line()
{
	PREFIX=$1
	MEDIA_ID=$2
	
	mysql macross -h192.168.8.101 -P3317 -upublic -pfunshion -e"SELECT hashid FROM fs_dat_file d,fs_media_serials s WHERE d.serialid=s.\`serialid\` AND s.\`media_id\`=${MEDIA_ID}" >> hashid_cold_${DATE}.temp 
}

>hashid_cold_${DATE}.temp

while read line
do
	do_line ${line}
done < mediaid_cold_${DATE}.list

grep -v "hashid" hashid_cold_${DATE}.temp > hashid_cold_${DATE}.list
