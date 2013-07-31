#!/bin/bash

LOG="./log.0626"
BEGIN_TIME="2013-06-16"
END_TIME="2013-06-26"

function handle_line()
{
    TYPE=$1
    MEDIA_ID=$2
    echo "TYPE=${TYPE} MEDIA_ID=${MEDIA_ID}"
    SQL=""
    SQL=${SQL}"select end_time from ("
    SQL=${SQL}"  select end_time from fs_ms_task where task_id in ( "
    SQL=${SQL}"    select task_id from ( "
    SQL=${SQL}"        select task_id from fs_task where task_hash in ("
    SQL=${SQL}"          select hashid from ("
    SQL=${SQL}"            select hashid from fs_dat_file where serialid in ("
    SQL=${SQL}"                select serialid from ("
    SQL=${SQL}"                    select serialid from fs_media_serials where media_id=${MEDIA_ID}"
    SQL=${SQL}"                )as tb1"
    SQL=${SQL}"            ) "
    SQL=${SQL}"        ) as tb2"
    SQL=${SQL}"      ) "
    SQL=${SQL}"    ) as tb3"
    SQL=${SQL}"  ) and end_time != '0000-00-00' order by end_time asc limit 1"
    SQL=${SQL}") as tb5 "
    SQL=${SQL}"where end_time >= '${BEGIN_TIME}' and end_time <= '${END_TIME}'"
    #echo ${SQL}

    CMD=""
    CMD=${CMD}"/usr/bin/mysql -h192.168.8.196 -P3306 -upublic -pfunshion"
    CMD=${CMD}" -e\"${SQL}\" macross"
    #echo ${CMD}
    
    TEMP= eval ${CMD}
    #echo $TEMP    
    if [ x"$TEMP" = x"" ]; then
        echo "no  ${TYPE} ${MEDIA_ID}" >> ${LOG}
    else
        echo "yes ${TYPE} ${MEDIA_ID}" >> ${LOG}
    fi
    #echo `${CMD}` > ${MEDIA_ID}.result
    
}

> ${LOG}

while read LINE
do
    #echo $LINE
    handle_line $LINE
done < ./new.0626

