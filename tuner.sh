#!/bin/bash

FILE_NAME=$1
SRC_IP=`echo ${FILE_NAME//.json/}`

IP_QUERY_PREFIX="http://192.168.160.202:4321/iprocess/?cmd=ipquery&ip="

function ip_query()
{
	IP=$1
	IP2=$2

	IP_QUERY_URL="${IP_QUERY_PREFIX}${IP}"
	RESULT=`curl -s "${IP_QUERY_URL}" `
	AREA=`echo $RESULT|awk -F"[\r=,]" '{print $4}'`
	ISP=`echo $RESULT|awk -F"[\r=,]" '{print $5}'`

	IP_QUERY_URL2="${IP_QUERY_PREFIX}${IP2}"
	RESULT2=`curl -s "${IP_QUERY_URL2}" `
	AREA2=`echo $RESULT2|awk -F"[\r=,]" '{print $4}'`
	ISP2=`echo $RESULT2|awk -F"[\r=,]" '{print $5}'`


	echo "$SRC_IP,$IP,$AREA,$ISP,$IP2,$AREA2,$ISP2"
}

IPSS=`awk -F"[,:]" '{for(i=1;i<=NF;i++){if($i~/{\042ip\042/){print $(i+1)} } }' ${FILE_NAME}`
IP=`echo ${IPSS//\"/}`

IPSS2=`awk -F"[,:]" '{for(i=1;i<=NF;i++){if($i~/\[\042http/){print $(i+1)} } }' ${FILE_NAME}`
IP2=${IPSS2//\//}

ip_query $IP $IP2


