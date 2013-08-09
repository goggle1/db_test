#!/bin/bash

FILE_NAME=$1

function do_line()
{
	LINE=$1
	
	#----------
	PREFIX=`echo ${LINE:0:10}`
	if [ x"$PREFIX" = x"----------" ];
	then
		AREA=`echo $LINE | awk -F"----------" '{print $2}'`
	else
		BEGIN_IP=`echo $LINE | awk -F"-" '{print $1}'`
		END_IP=`echo $LINE | awk -F"-" '{print $1}'`
		echo "$BEGIN_IP,$END_IP,$AREA"
	fi
	
}

while read line
do
	do_line ${line}
done < ${FILE_NAME}


