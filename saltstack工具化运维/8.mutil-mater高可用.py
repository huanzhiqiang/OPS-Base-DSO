##1.双角色master,提高工具可用性；
##机器分布；
172.20.32.251 salt-master salt-minion
172.20.32.252 salt-master salt-minion

##1.在2个节点上面分别安装Master和Minion
yum install salt-master salt-minion -y

##2.在Minion配置文件中添加多master节点
more /etc/salt/minion
...
# resolved, then the minion will fail to start.
master: 
  - 172.20.32.251
  - 172.20.32.252

##3.同步Master配置文件和状态文件
#在251主机操作
scp -rp /etc/salt/master 172.20.32.252:/etc/salt/
scp -r /srv/salt/ 172.20.32.252:/srv/

#同步Master秘钥对
cd /etc/salt/master/pki && rm -fr master && mkdir master && chmod 700 master/
scp -rp /etc/salt/pki/master/master.pem master.pub 172.20.32.252:/etc/salt/pki/master/

##4.重启Master和Minion服务节点，生效Master和Minion配置文件
systemctl restart salt-master
systemctl restart salt-minion

##5.认证Minion
salt-key 

##6.在2个Master节点执行命令都可以正常工作
[root@local-dev-252 salt]# salt-key -L
Accepted Keys:
dev_251
dev_252
Denied Keys:
Unaccepted Keys:
Rejected Keys:

[root@local-dev-251 master]# salt-key -L
Accepted Keys:
dev_251
dev_252
dev_253
Denied Keys:
Unaccepted Keys:
Rejected Keys:

###############要点；
1.Master配置文件要一样
2.Master file_root路径及状态文件要一样
3.Master 公钥和私钥要一样
4.修改Minion配置中指定Master为列表形式
5.Master接受的minion_id key要保持同步，增删保持一致
6.生产环境可以用nginx做多个master的api负载均衡
7.Master上的key要考虑安全性问题
8.生产环境的状态文件管理可以用git管理
9.还可以通过 failover配置多个multiple masters，相对复杂一些