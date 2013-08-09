#!/bin/bash

FILE_NAME=$1
IP_QUERY_PREFIX="http://192.168.160.202:4321/iprocess/?cmd=ipquery&ip="
IP_QUERY_PREFIX2="http://whois.pconline.com.cn/ip.jsp?ip="

function do_line()
{
	LINE=$1
	CLIENT_IP=`echo $LINE|awk -F"," '{print $1}'`
	COUNT=`echo $LINE|awk -F"," '{print $2}'`

	#IP_QUERY_URL="${IP_QUERY_PREFIX}${CLIENT_IP}"
        #RESULT=`curl -s "${IP_QUERY_URL}" `
        #AREA=`echo $RESULT|awk -F"[\r=,]" '{print $4}'`
        #ISP=`echo $RESULT|awk -F"[\r=,]" '{print $5}'`	

	IP_QUERY_URL2="${IP_QUERY_PREFIX2}${CLIENT_IP}"
        RESULT2=`curl -s "${IP_QUERY_URL2}" `
        #ISP2=`echo $RESULT2|awk -F"[{}]" '{print $2}'`

	echo "$CLIENT_IP,$COUNT,$RESULT2"
}

while read line
do
	do_line $line
done < ${FILE_NAME} 
