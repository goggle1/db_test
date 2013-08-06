#!/bin/bash

LIMIT=1000

FILE_NAME="./dispatching.list"
MS_LIST="./ms.list"
OUT_FILE="dispatching_gt_${LIMIT}.list"

> ${OUT_FILE}

function do_line()
{
	SERVER_ID=$1
	COUNT=$2

	if [ ${COUNT} -ge 1000 ];
	then
		MS_INFO=`grep "^${SERVER_ID}	" ${MS_LIST}`
		echo "${SERVER_ID} ${COUNT} $MS_INFO" >> ${OUT_FILE}
	fi
}

while read line
do
	do_line ${line}
done < ${FILE_NAME}
