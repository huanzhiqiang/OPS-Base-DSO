#1.yum安装相关依赖包;
yum install -y libaio-devel.x86_64

#2.下载二进制安装
wget https://dev.mysql.com/get/Downloads/MySQL-5.7/mysql-5.7.17-linux-glibc2.5-x86_64.tar.gz
tar -zxf mysql-5.7.17-linux-glibc2.5-x86_64.tar.gz -C /usr/local/
cd /usr/local/ && ln -s mysql-5.7.17-linux-glibc2.5-x86_64/ mysql

#3.设置导数据位置;
mkdir -vp /usr/local/mysql/mysql-files

#4.创建mysql运行帐户并给目录mysql权限
useradd -r -s /usr/sbin/nologin mysql
chown -R root.mysql /usr/local/mysql-5.7.17-linux-glibc2.5-x86_64

##5.目录权限
mkdir -p /data/mysql/330{6,7}/{data,log,mysql}
mkdir -p /var/run/mysqld
chown -R mysql.mysql /data/mysql /var/run/mysqld
chmod 750 /var/run/mysqld /data/mysql

#6.配置文件; /etc/my.cnf
[mysqld_multi]
mysqld     = /usr/local/mysql/bin/mysqld_safe
mysqladmin = /usr/local/mysql/bin/mysqladmin


[mysqld3306]
port = 3306
server_id = 3306
basedir =/usr/local/mysql
datadir =/data/mysql/3306/data
log-bin=/data/mysql/3306/log/mysql-bin
socket =/var/run/mysqld/mysql3306.sock
log-error =/var/log/mysqld3306.log
pid-file =/var/run/mysqld/mysqld3306.pid
binlog_format = row
expire_logs_days = 15
binlog-ignore-db=mysql,sys,performance_schema,information_schema

sync_binlog=1
innodb_flush_log_at_trx_commit=1
relay_log = /usr/local/mysql/relaylog3306
log_slave_updates=1
#auto-increment-offset=1
#auto-increment-increment=2
sql_mode=STRICT_TRANS_TABLES

# slave
[mysqld3307]
port = 3307
server_id = 3307
basedir =/usr/local/mysql
datadir =/data/mysql/3307/data
log-bin=/data/mysql/3307/log/mysql-bin
socket =/var/run/mysqld/mysql3307.sock
log-error =/var/log/mysqld3307.log
pid-file =/var/run/mysqld/mysqld3307.pid
binlog_format = row
expire_logs_days = 15
binlog-ignore-db=mysql,sys,performance_schema,information_schema

sync_binlog=1
innodb_flush_log_at_trx_commit=1
relay_log = /usr/local/mysql/relaylog3307
log_slave_updates=1
#auto-increment-offset=2
#auto-increment-increment=2
sql_mode=STRICT_TRANS_TABLES

##8.添加环境变量
echo "PATH=$PATH:/usr/local/mysql/bin  " >> /etc/profile
source /etc/profile

#10.数据库初始化；
/usr/local/mysql/bin/mysqld --initialize-insecure --user=mysql --basedir=/usr/local/mysql --datadir=/data/mysql/3306/data
/usr/local/mysql/bin/mysqld --initialize-insecure --user=mysql --basedir=/usr/local/mysql --datadir=/data/mysql/3307/data

#11.启动服务；
mysqld_multi report
mysqld_multi start 3306,3307
或；
mysqld_multi start /var/run/mysqld/mysql3306.sock,/var/run/mysqld/mysql3307.sock


#12创建库与修改密码；
mysql -uroot -S /var/run/mysqld/mysql3306.sock
GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost' IDENTIFIED BY 'anbang@123' WITH GRANT OPTION;
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'anbang@123' WITH GRANT OPTION;
flush privileges;

CREATE DATABASE `book` CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
###
mysqldump -uroot -panbang@123 -S /tmp/mysql.sock --no-create-info  tt eaj_express_response_message_node  > eaj_express_response_message_node.sql
select * from eaj_express_response_message_node where TIME>"2019-04-24 16:00:00";