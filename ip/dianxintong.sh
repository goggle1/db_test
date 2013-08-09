#!/bin/bash

FILE_NAME=$1
IP_QUERY_PREFIX="http://192.168.160.202:4321/iprocess/?cmd=ipquery&ip="

ISP="电信通"

function do_line()
{
	LINE=$1
        BEGIN_IP=`echo $LINE|awk -F"[\r=,]" '{print $1}'`
        END_IP=`echo $LINE|awk -F"[\r=,]" '{print $2}'`
        AREA=`echo $LINE|awk -F"[\r=,]" '{print $3}'`

	BEGIN_URL="${IP_QUERY_PREFIX}${BEGIN_IP}"
        BEGIN_RESULT=`curl -s "${BEGIN_URL}" `
        BEGIN_AREA=`echo $BEGIN_RESULT|awk -F"[\r=,]" '{print $4}'`	
        BEGIN_ISP=`echo $BEGIN_RESULT|awk -F"[\r=,]" '{print $5}'`	

	END_URL="${IP_QUERY_PREFIX}${END_IP}"
        END_RESULT=`curl -s "${END_URL}" `
        END_AREA=`echo $END_RESULT|awk -F"[\r=,]" '{print $4}'`	
        END_ISP=`echo $END_RESULT|awk -F"[\r=,]" '{print $5}'`	

	DIFF="0"

	if [ x"$AREA" != x"$BEGIN_AREA" ]; 
	then
		DIFF="1"
	fi
	if [ x"$AREA" != x"$END_AREA" ]; 
	then
		DIFF="1"
	fi

	if [ x"$ISP" != x"$BEGIN_ISP" ];
        then
                DIFF="2"
        fi
        if [ x"$ISP" != x"$END_ISP" ];    
        then
                DIFF="2"
        fi	

	echo "$DIFF,$ISP,$AREA,$BEGIN_IP,$BEGIN_ISP,$BEGIN_AREA,$END_IP,$END_ISP,$END_AREA"
}

while read line
do
	do_line $line
done < ${FILE_NAME} 
