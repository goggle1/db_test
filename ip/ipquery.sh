#!/bin/bash

FILE_NAME=$1
IP_QUERY_PREFIX="http://192.168.160.202:4321/iprocess/?cmd=ipquery&ip="

function do_line()
{
	CLIENT_IP=$1
	IP_QUERY_URL="${IP_QUERY_PREFIX}${CLIENT_IP}"
        RESULT=`curl -s "${IP_QUERY_URL}" `
        AREA=`echo $RESULT|awk -F"[\r=,]" '{print $4}'`
        ISP=`echo $RESULT|awk -F"[\r=,]" '{print $5}'`	

	echo "$CLIENT_IP,$AREA,$ISP"
}

while read line
do
	do_line $line
done < ${FILE_NAME} 
