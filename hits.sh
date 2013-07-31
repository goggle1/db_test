#!/bin/bash

FILE_NAME=$1
IP_QUERY_PREFIX="http://192.168.160.202:4321/iprocess/?cmd=ipquery&ip="

function do_line()
{
        LINE=$1
        CLIENT_IP=`echo "$LINE" | awk -F"," '{print $2}'`
        HASH_ID=`echo "$LINE" | awk -F"," '{print $7}'`
        MS_IP=`echo "$LINE" | awk -F"," '{print $8}'`
        
        HASH_ID_UPPER=`echo $HASH_ID|tr [a-z] [A-Z]`
        
        IP_QUERY_URL="${IP_QUERY_PREFIX}${CLIENT_IP}"
        RESULT=`curl -s "${IP_QUERY_URL}" `
        AREA=`echo $RESULT|awk -F"[\r=,]" '{print $4}'`
        ISP=`echo $RESULT|awk -F"[\r=,]" '{print $5}'`
        
	HASH_ID_LEN=`expr length "$HASH_ID_UPPER"`
        if [ $HASH_ID_LEN -eq 32 -o $HASH_ID_LEN -eq 40 ]; 
        then
        	echo "$CLIENT_IP,$AREA,$ISP,$HASH_ID_UPPER,$MS_IP"
        fi
}

while read line
do
        do_line $line
done < ${FILE_NAME}
