[mysqld_multi]
mysqld = /usr/local/mysql/bin/mysqld_safe
mysqladmin =/usr/local/mysql/bin/mysqladmin
log =/var/log/mysqld_multi.log

[mysqld1]
socket = /data/3306/mysql/mysql.sock
port = 3306
pid-file = /data/3306/mysql/mysql.pid
datadir = /data/3306/data
log_bin=/data/3306/log/binlog
server-id = 1
character_set_server=utf8
init_connect='SET NAMES utf8'
max_allowed_packet=16M
lower_case_table_names=1 
sql_mode=NO_ENGINE_SUBSTITUTION,STRICT_TRANS_TABLES
log_bin_trust_function_creators=1

[mysqld2]
socket = /data/3307/mysql/mysql.sock
port = 3307
pid-file = /data/3307/mysql/mysql.pid
datadir = /data/3307/data
log_bin=/data/3307/log/binlog
server-id = 2
character_set_server=utf8
init_connect='SET NAMES utf8'
max_allowed_packet=16M
lower_case_table_names=1 
sql_mode=NO_ENGINE_SUBSTITUTION,STRICT_TRANS_TABLES
log_bin_trust_function_creators=1

[mysqld3]
socket = /data/3308/mysql/mysql.sock
port = 3308
pid-file = /data/3308/mysql/mysql.pid
datadir = /data/3308/data
log_bin=/data/3308/log/binlog
server-id = 3
character_set_server=utf8
init_connect='SET NAMES utf8'
max_allowed_packet=16M
lower_case_table_names=1 
sql_mode=NO_ENGINE_SUBSTITUTION,STRICT_TRANS_TABLES
log_bin_trust_function_creators=1
