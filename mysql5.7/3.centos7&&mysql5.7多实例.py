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

#5.创建多实例数据目录
mkdir -p /data/mysql/330{6,7,8,9}/{data,log,binlog}
chown -R mysql.mysql /data/mysql

#6.配置文件; /etc/my.cnf
[mysqld_multi]
mysqld=/usr/local/mysql/bin/mysqld_safe
mysqladmin=/usr/local/mysql/bin/mysqladmin
log=/var/log/mysql_multi.log

[mysqld1]
datadir=/data/mysql/3306/data
socket=/data/mysql/3306/3306.sock
pid-file=/data/mysql/3306/mysql.pid
port=3306
user=mysql
performance_schema=off
innodb_buffer_pool_size=128M
bind_address=0.0.0.0
skip-name-resolve=0
character-set-server=utf8
collation-server=utf8_unicode_ci
log_error=/data/mysql/3306/log/mysql.log
log-bin=/data/mysql/3306/binlog/mysql-bin
binlog_format=ROW
expire_logs_days=10
server_id=3306
skip-external-locking

[mysqld2]
datadir=/data/mysql/3307/data
socket=/data/mysql/3307/3307.sock
pid-file=/data/mysql/3307/mysql.pid
port=3307
user=mysql
performance_schema=off
innodb_buffer_pool_size=128M
bind_address=0.0.0.0
skip-name-resolve=0
character-set-server=utf8
collation-server=utf8_unicode_ci
log_error=/data/mysql/3307/log/mysql.log
log-bin=/data/mysql/3307/binlog/mysql-bin
binlog_format=ROW
expire_logs_days=10
server_id=3307
skip-external-locking

[mysqld3]
datadir=/data/mysql/3308/data
socket=/data/mysql/3308/3308.sock
pid-file=/data/mysql/3308/mysql.pid
port=3308
user=mysql
performance_schema=off
innodb_buffer_pool_size=128M
bind_address=0.0.0.0
skip-name-resolve=0
character-set-server=utf8	
collation-server=utf8_unicode_ci
log_error=/data/mysql/3308/log/mysql.log
log-bin=/data/mysql/3308/binlog/mysql-bin
binlog_format=ROW
expire_logs_days=10
server_id=3308
skip-external-locking

[mysqld4]
datadir=/data/mysql/3309/data
socket=/data/mysql/3309/3309.sock
pid-file=/data/mysql/3309/mysql.pid
port=3309
user=mysql
performance_schema=off
innodb_buffer_pool_size=128M
bind_address=0.0.0.0
skip-name-resolve=0
character-set-server=utf8
collation-server=utf8_unicode_ci
log_error=/data/mysql/3309/log/mysql.log
log-bin=/data/mysql/3309/binlog/mysql-bin
binlog_format=ROW
expire_logs_days=10
server_id=3309
skip-external-locking

#7.初始化数据库记录下每个实例的临时密码，因为后面我们需要修改这个密码;
/usr/local/mysql/bin/mysqld --initialize-insecure --user=mysql --basedir=/usr/local/mysql --datadir=/data/mysql/3306/data
/usr/local/mysql/bin/mysqld --initialize-insecure --user=mysql --basedir=/usr/local/mysql --datadir=/data/mysql/3307/data
/usr/local/mysql/bin/mysqld --initialize-insecure --user=mysql --basedir=/usr/local/mysql --datadir=/data/mysql/3308/data
/usr/local/mysql/bin/mysqld --initialize-insecure --user=mysql --basedir=/usr/local/mysql --datadir=/data/mysql/3309/data
****记录密码******;

#8.加密认证连接;
/usr/local/mysql/bin/mysql_ssl_rsa_setup --user=mysql --basedir=/usr/local/mysql --datadir=/data/mysql/3306/data
/usr/local/mysql/bin/mysql_ssl_rsa_setup --user=mysql --basedir=/usr/local/mysql --datadir=/data/mysql/3307/data
/usr/local/mysql/bin/mysql_ssl_rsa_setup --user=mysql --basedir=/usr/local/mysql --datadir=/data/mysql/3308/data
/usr/local/mysql/bin/mysql_ssl_rsa_setup --user=mysql --basedir=/usr/local/mysql --datadir=/data/mysql/3309/data

#9.复制多实例脚本到服务管理目录下; 
cp /usr/local/mysql/support-files/mysqld_multi.server /etc/init.d/mysqld_multi
chmod +x /etc/init.d/mysqld_multi
export PATH=/usr/local/mysql/bin:$PATH

#10.启动实例;
/etc/init.d/mysqld_multi start

#修改实例密码;
mysqladmin -S /data/mysql/3306/3306.sock -uroot -p'dhpqNuDYF7.V' password 'huanzhiqiang@123'
mysqladmin -S /data/mysql/3307/3307.sock -uroot -p'vzmHbq,HS1dk' password 'huanzhiqiang@123'
mysqladmin -S /data/mysql/3308/3308.sock -uroot -p'S<%vBQ6yj722' password 'huanzhiqiang@123'
mysqladmin -S /data/mysql/3309/3309.sock -uroot -p'l/#>?YuO%1Fw' password 'huanzhiqiang@123'

#停止单例;
mysqladmin -uroot -pAa123321 -S /data/mysql/3306/3306.sock shutdown
#启动单例;
/etc/init.d/mysqld_multi start

## 检查实例状态
/etc/init.d/mysql_multi report


#11脚本实现语句查询与登录;
vim mysql_multi.sh
#!/bin/bash
#Author: huanzhiqiang
#Time: 2019-03-30
#Name: mysql_multi.sh
#Description: This is a prod shell script.

port=$1
state=$2
if [ $# -gt 2 ]
  then
    echo "Invalid parameter or too long parameter!"
    exit 1
elif [ $# -eq 0 ]
  then
    echo "Please enter valid parameters!"
    echo "For example: mysql_multi 3306"
    echo "3306=/data/mysql/3306/3306.sock"
    exit 2
elif [ ! -e /data/mysql/${port}/${port}.sock ]
  then
    echo "Please check /data/mysql/${port}/${port}.scok"
    exit 3
fi
arg_N=$#
#difine fuction for command
comm(){
  if [ $arg_N -eq 2 ]
    then
      mysql -uroot -p'Aa123321' -S /data/mysql/${port}/${port}.sock -e "$state" 2>/dev/null
  else [ $arg_N -eq 1 ]
      mysql -uroot -p'Aa123321' -S /data/mysql/${port}/${port}.sock 2>/dev/null
  fi
}
comm

################################################12创建主从复制帐户################
#随机生成机器与db密码;
</dev/urandom tr -dc '1234567890!@#$%qwertQWERTasdfgASDFGzxcvbZXCVB' | head -c18; echo ""

#主库配置备份信息;
./mysql_multi.sh 3306 "grant replication slave on *.* to replbak@'127.0.0.1' identified by 'vc9V7#!DEG!w'"

#同步主库数据;
mysqldump -S /data/mysql/3306/3306.sock -uroot -p'huanzhiqiang@123' -A >/tmp/3306.sql

#查看master
### 显示bin_log文件pos点
./mysql_multi.sh 3306 "show master status"

#导入主库到从库;
CREATE DATABASE IF NOT EXISTS tt DEFAULT CHARSET utf8 COLLATE utf8_general_ci;
mysql -uroot -p'huanzhiqiang@123' -S /data/mysql/3307/3307.sock tt </tmp/3306.sql

#从库设置同步pos点;
change master to
master_host='127.0.0.1',
master_port=3306,
master_user='replbak',
master_password='vc9V7#!DEG!w',
master_log_file='mysql-bin.000001',
master_log_pos=598;

#开启主从;
start slave
show slave status\G


#####AQ;
清除一下bin_log文件
mysql_multi 3306 "reset master"


参考:
二进制数据其它版本;
wget https://downloads.mysql.com/archives/get/file/mysql-5.7.20-linux-glibc2.12-x86_64.tar.gz
https://www.he-jason.com/he-jason/talkops/757.html