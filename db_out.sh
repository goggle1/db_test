mysql -h192.168.8.101 -P3317 -upublic -pfunshion  --default-character-set=utf8 macross -e	\
"select a.*, b.room_id, b.ml_room_id, b.server_name, b.server_ip, b.server_port, c.room_name from fs_ms_realstate a, fs_server b, fs_server_location c where a.server_id=b.server_id and (b.room_id=c.room_id or b.ml_room_id=c.room_id) order by a.server_id" \
> ms.list

mysql -h192.168.8.101 -P3317 -upublic -pfunshion  --default-character-set=utf8 macross -e	\
"select server_id, count(*) from fs_mobile_ms_dat where state='dispatching' group by server_id order by count(*) DESC " \
>  dispatching.list

mysql -h192.168.8.101 -P3317 -upublic -pfunshion  --default-character-set=utf8 macross -e	\
"select server_id, count(*) from fs_mobile_ms_dat where state='dispatch-failed' group by server_id order by count(*) DESC " \
>  dispatch_failed.list

mysql -h192.168.8.101 -P3317 -upublic -pfunshion  --default-character-set=utf8 macross -e       \
"select a.*, b.room_id, b.ml_room_id, b.server_name, b.server_ip, b.server_port, c.room_name from fs_ms_realstate a, fs_server b, fs_server_location c where a.free_disk < 100 and b.is_valid =1 and a.server_id=b.server_id and (b.ml_room_id !=0 and b.ml_room_id=c.room_id) order by a.server_id " 	\
> free_disk_less_100.list
