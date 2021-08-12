###salt-ssh模式；
1.salt-ssh 是 0.17.0 新引入的一个功能，不需要minion对客户端进行管理，也不需要master。
2.salt-ssh 支持salt大部分的功能：如 grains、modules、state 等
3.salt-ssh 没有使用ZeroMQ的通信架构，执行是串行模式
类似 paramiko、pssh、ansible 这类的工具

##1.配置文件；
[root@local-dev-251 salt]# egrep -v "^#|^$" /etc/salt/roster 
dev_251:
  host: 172.20.32.251
  user: root
  passwd: XXXXXXX
  port: 22
#参数：
# target的信息
    host:        # 远端主机的ip地址或者dns域名
    user:        # 登录的用户
    passwd:      # 用户密码,如果不使用此选项，则默认使用秘钥方式
# 可选的部分
    port:        #ssh端口
    sudo:        #可以通过sudo
    tty:         # 如果设置了sudo，设置这个参数为true
    priv:        # ssh秘钥的文件路径
    timeout:     # 当建立链接时等待响应时间的秒数
    minion_opts: # minion的位置路径
    thin_dir:    # target系统的存储目录，默认是/tmp/salt-<hash>
    cmd_umask:   # 使用salt-call命令的umask值

##2.安装salt-ssh
yum install salt-ssh

##3.进行管理测试
[root@local-dev-251 salt]# salt-ssh '*' test.ping
dev_251:
    True
##4.salt-ssh执行状态模块
salt-ssh '*' state.sls zabbix.zabbix-agentd

#注意事项：
salt-ssh和salt-minion可以共存，salt-minion不依赖于ssh服务